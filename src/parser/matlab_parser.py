"""
MATLAB Code Parser.

This module implements a regex-based parser for MATLAB code
to extract functions, variables, classes, and comments.
"""

import re
from typing import Dict, List, Optional

from ..utils.logging import get_logger
from ..utils.symbol_table import SymbolTable, get_symbol_table
from .models import (
    BUILTIN_FUNCTIONS,
    MATLAB_KEYWORDS,
    ClassInfo,
    CommentInfo,
    FunctionInfo,
    ParseResult,
    VariableInfo,
)

logger = get_logger(__name__)


class MatlabParser:
    """Regex-based parser for MATLAB code."""

    # Regex patterns for MATLAB code
    FUNCTION_PATTERN = re.compile(
        r"^\s*function\s+"
        r"(?:(\w+)\s*=\s*)?"  # Output args [out1, out2] =
        r"(\w+)\s*"  # Function name
        r"\(([^)]*)\)"  # Input args (arg1, arg2)
        r"\s*$",
        re.MULTILINE,
    )

    FUNCTION_END_PATTERN = re.compile(
        r"^\s*end\s*($|%\s*\w+\s*$)", re.MULTILINE
    )

    VARIABLE_PATTERN = re.compile(
        r"^\s*"
        r"(?:(global|persistent)\s+)?"  # Variable modifiers
        r"(\w+)\s*"  # Variable name
        r"(?:=\s*.+)?"  # Assignment (optional)
        r"\s*(?:;.*)?$",
        re.MULTILINE,
    )

    CLASSDEF_PATTERN = re.compile(r"^\s*classdef\s+(\w+)\s*\b", re.MULTILINE)

    PROPERTY_PATTERN = re.compile(
        r"^\s*properties", re.MULTILINE | re.IGNORECASE
    )

    METHOD_PATTERN = re.compile(
        r"^\s*function\s+"
        r"(?:(\w+)\s*=\s*)?"  # Output args
        r"(\w+)\s*"  # Method name
        r"\(([^)]*)\)"  # Input args
        r"\s*$",
        re.MULTILINE,
    )

    COMMENT_PATTERN = re.compile(
        r"^(.*?)(?:;|%)([^%].*)$",  # Code before ; or %, then comment (not %)
        re.MULTILINE,
    )

    # Block comment pattern - matches entire block
    BLOCK_COMMENT_PATTERN = re.compile(
        r"%\s*\{\s*(.*?)\s*\}%", re.DOTALL | re.MULTILINE
    )

    def __init__(self, symbol_table: Optional[SymbolTable] = None):
        """Initialize parser."""
        self._nesting_level = 0  # Track function/class nesting
        self._current_function: Optional[FunctionInfo] = None
        self._current_class: Optional[ClassInfo] = None
        self._function_stack: List[FunctionInfo] = []
        self._class_stack: List[ClassInfo] = []

        # Get or create symbol table
        self._symbol_table = (
            symbol_table if symbol_table else get_symbol_table()
        )

    def parse_file(
        self, file_path: str, file_uri: str, use_cache: bool = True
    ) -> ParseResult:
        """
        Parse a MATLAB file and update symbol table.

        Args:
            file_path (str): Local path to file
            file_uri (str): URI of file
            use_cache (bool): Whether to use cache (default True)

        Returns:
            ParseResult: Parsing result with extracted elements
        """
        logger.debug(f"Parsing file: {file_path}")

        # Read file content
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ParseResult(
                file_uri=file_uri,
                file_path=file_path,
                raw_content="",
                errors=[{"error": f"Failed to read file: {e}"}],
            )

        # Parse content
        result = self.parse_content(content, file_uri, file_path)

        # Update symbol table if parsing succeeded
        if not result.errors:
            try:
                self._symbol_table.update_from_parse_result(
                    uri=file_uri,
                    content=content,
                    parse_result=result,
                )
                logger.info(f"Updated symbol table for {file_path}")
            except Exception as e:
                logger.error(f"Error updating symbol table: {e}")
                result.errors.append(
                    {"error": f"Failed to update symbol table: {e}"}
                )

        return result

    def parse_content(
        self, content: str, file_uri: str, file_path: str
    ) -> ParseResult:
        """
        Parse MATLAB code content.

        Args:
            content (str): MATLAB code content
            file_uri (str): URI of file
            file_path (str): Local path to file

        Returns:
            ParseResult: Parsing result with extracted elements
        """
        functions: List[FunctionInfo] = []
        variables: List[VariableInfo] = []
        comments: List[CommentInfo] = []
        classes: List[ClassInfo] = []
        errors: List[Dict] = []

        # Reset state
        self._nesting_level = 0
        self._current_function = None
        self._current_class = None
        self._function_stack = []
        self._class_stack = []
        function_tree: Dict[str, List[str]] = {}

        # First, extract all block comments from entire content
        block_comments = self._extract_block_comments(content)
        for block_comment in block_comments:
            comments.append(block_comment)

        # Remove block comments from content for further parsing
        content_without_blocks = self.BLOCK_COMMENT_PATTERN.sub("", content)
        lines_without_blocks = content_without_blocks.split("\n")

        for line_num, line in enumerate(lines_without_blocks, 1):
            # Map line number back to original (including removed lines)
            original_line_num = (
                line_num  # Simplified - not accurate but works for now
            )

            # Skip empty lines
            if not line.strip():
                continue

            # Check for comments (line-level)
            comment = self._extract_line_comment(line, original_line_num)
            if comment:
                comments.append(comment)
                # Remove comment from line for further parsing
                line = line[: comment.column - 1]
                if not line.strip():
                    continue

            # Check for class definition
            class_match = self._extract_classdef(line, original_line_num)
            if class_match:
                classes.append(class_match)
                self._class_stack.append(class_match)
                self._current_class = class_match
                self._nesting_level += 1
                continue

            # Check for function definition
            function_match = self._extract_function(line, original_line_num)
            if function_match:
                functions.append(function_match)

                # Set parent class if in class
                if self._current_class:
                    function_match.parent_class = self._current_class.name

                # Set parent function if nested
                if self._current_function:
                    function_match.is_nested = True
                    function_match.parent_function = (
                        self._current_function.name
                    )

                # Update function tree
                if self._current_function:
                    parent_name = self._current_function.name
                    if parent_name not in function_tree:
                        function_tree[parent_name] = []
                    function_tree[parent_name].append(function_match.name)

                self._function_stack.append(function_match)
                if self._nesting_level == 0 or not self._current_class:
                    self._current_function = function_match
                self._nesting_level += 1
                continue

            # Check for properties (inside class)
            if self._current_class:
                prop_match = self._extract_property(line, original_line_num)
                if prop_match:
                    self._current_class.properties.append(prop_match)
                continue

            # Check for end statement
            if self._extract_end(line):
                if self._nesting_level > 0:
                    self._nesting_level -= 1

                    # If exiting class
                    if (
                        self._class_stack
                        and self._nesting_level == len(self._class_stack) - 1
                    ):
                        self._current_class = (
                            self._class_stack[-1]
                            if self._class_stack
                            else None
                        )
                    elif self._nesting_level == 0:
                        self._current_class = None

                    # If exiting function
                    if (
                        self._function_stack
                        and self._nesting_level
                        == len(self._function_stack) - 1
                    ):
                        self._current_function = self._function_stack[-1]
                    elif self._nesting_level == 0:
                        self._current_function = None

                continue

            # Check for variable declaration
            if self._nesting_level == 0 or self._current_function:
                var_match = self._extract_variable(line, original_line_num)
                if var_match:
                    # Only add global/top-level variables
                    if (
                        self._nesting_level == 0
                        or var_match.is_global
                        or var_match.is_persistent
                    ):
                        variables.append(var_match)

        logger.info(
            f"Parsed {len(functions)} functions, "
            f"{len(variables)} variables, "
            f"{len(comments)} comments, "
            f"{len(classes)} classes"
        )

        return ParseResult(
            file_uri=file_uri,
            file_path=file_path,
            functions=functions,
            variables=variables,
            classes=classes,
            comments=comments,
            errors=errors,
            raw_content=content,
            function_tree=function_tree,
        )

    def _extract_function(
        self, line: str, line_num: int
    ) -> Optional[FunctionInfo]:
        """Extract function definition from line."""
        match = self.FUNCTION_PATTERN.match(line)
        if not match:
            # Try method pattern (for classes)
            if self._current_class:
                match = self.METHOD_PATTERN.match(line)

        if not match:
            return None

        # Extract function components
        outputs = match.group(1)
        name = match.group(2)
        inputs = match.group(3)

        # Parse outputs
        output_args = []
        if outputs:
            output_args = [s.strip() for s in outputs.split(",")]

        # Parse inputs
        input_args = []
        if inputs:
            input_args = [s.strip() for s in inputs.split(",")]

        # Find function name position
        name_pos = line.find(name)
        if name_pos == -1:
            name_pos = 0

        return FunctionInfo(
            name=name,
            line=line_num,
            column=name_pos + 1,
            input_args=input_args,
            output_args=output_args,
            is_nested=False,
            parent_function=None,
        )

    def _extract_classdef(
        self, line: str, line_num: int
    ) -> Optional[ClassInfo]:
        """Extract class definition from line."""
        match = self.CLASSDEF_PATTERN.match(line)
        if not match:
            return None

        name = match.group(1)
        name_pos = line.find(name)
        if name_pos == -1:
            name_pos = 0

        return ClassInfo(
            name=name,
            line=line_num,
            column=name_pos + 1,
            properties=[],
            methods=[],
        )

    def _extract_property(self, line: str, line_num: int) -> Optional[str]:
        """Extract property name from line."""
        # Simple pattern: property name (no type yet)
        match = re.match(r"^\s*(\w+)", line)
        if match:
            return match.group(1)
        return None

    def _extract_variable(
        self, line: str, line_num: int
    ) -> Optional[VariableInfo]:
        """Extract variable declaration from line."""
        match = self.VARIABLE_PATTERN.match(line)
        if not match:
            return None

        modifiers = match.group(1)
        name = match.group(2)

        # Find variable name position
        name_pos = line.find(name)
        if name_pos == -1:
            name_pos = 0

        # Check for modifiers
        is_global = bool(modifiers and "global" in modifiers)
        is_persistent = bool(modifiers and "persistent" in modifiers)

        return VariableInfo(
            name=name,
            line=line_num,
            column=name_pos + 1,
            is_global=is_global,
            is_persistent=is_persistent,
        )

    def _extract_block_comments(self, content: str) -> List[CommentInfo]:
        """Extract all block comments from content.

        Args:
            content (str): Full file content

        Returns:
            List[CommentInfo]: List of block comments
        """
        block_comments = []

        for match in self.BLOCK_COMMENT_PATTERN.finditer(content):
            # Calculate line number (approximate)
            content_before = content[: match.start()]
            line_num = content_before.count("\n") + 1

            # Calculate column
            line_start = content.rfind("\n", 0, match.start())
            column = (
                match.start() - line_start
                if line_start != -1
                else match.start() + 1
            )

            # Calculate end line
            content_with_block = content[: match.end()]
            end_line = content_with_block.count("\n") + 1

            block_comments.append(
                CommentInfo(
                    text=match.group(1).strip(),
                    line=line_num,
                    column=column,
                    is_block=True,
                    block_start_line=line_num,
                    block_end_line=end_line,
                )
            )

        return block_comments

    def _extract_line_comment(
        self, line: str, line_num: int
    ) -> Optional[CommentInfo]:
        """Extract line-level comment from line.

        Args:
            line (str): Line content
            line_num (int): Line number

        Returns:
            Optional[CommentInfo]: Comment info if found, None otherwise
        """
        # Check for line comments % or ;
        match = self.COMMENT_PATTERN.match(line)
        if match:
            # group(1) is code before ; or %
            # group(2) is comment content
            comment_content = match.group(2)

            if comment_content.strip():
                # Find column position
                separator_pos = match.start(2)  # Position of % or ;
                column = separator_pos + 1

                return CommentInfo(
                    text=comment_content.strip(),
                    line=line_num,
                    column=column,
                    is_block=False,
                )

        return None

    def _extract_end(self, line: str) -> bool:
        """Check if line is an end statement."""
        match = self.FUNCTION_END_PATTERN.match(line)
        return match is not None

    def is_builtin_function(self, name: str) -> bool:
        """Check if name is a built-in MATLAB function."""
        return name in BUILTIN_FUNCTIONS or name in MATLAB_KEYWORDS
