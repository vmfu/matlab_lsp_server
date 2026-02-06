"""
MATLAB Code Parser.

This module implements a regex-based parser for MATLAB code
to extract functions, variables, classes, and comments.
"""

import re
from typing import List, Optional, Dict
from pathlib import Path

from .models import (
    FunctionInfo,
    VariableInfo,
    ClassInfo,
    CommentInfo,
    ParseResult,
    BUILTIN_FUNCTIONS,
    MATLAB_KEYWORDS,
)

from ..utils.logging import get_logger

logger = get_logger(__name__)


class MatlabParser:
    """Regex-based parser for MATLAB code."""

    # Regex patterns for MATLAB code
    FUNCTION_PATTERN = re.compile(
        r'^\s*function\s+'
        r'(?:(\w+)\s*=\s*)?'  # Output args [out1, out2] =
        r'(\w+)\s*'  # Function name
        r'\(([^)]*)\)'  # Input args (arg1, arg2)
        r'\s*$',
        re.MULTILINE
    )

    FUNCTION_END_PATTERN = re.compile(
        r'^\s*end\s*($|%\s*\w+\s*$)',
        re.MULTILINE
    )

    VARIABLE_PATTERN = re.compile(
        r'^\s*'
        r'(?:(global|persistent)\s+)?'  # Variable modifiers
        r'(\w+)\s*'  # Variable name
        r'(?:=\s*.+)?'  # Assignment (optional)
        r'\s*(?:;.*)?$',
        re.MULTILINE
    )

    CLASS_PATTERN = re.compile(
        r'^\s*classdef\s+(\w+)\s*\b',
        re.MULTILINE
    )

    # Comment pattern - matches code before %, then comment
    # Handles: "code; comment" or "code % comment" or "% comment"
    COMMENT_PATTERN = re.compile(
        r'^(.*?)(?:;|%)([^%].*)$',  # Code before ; or %, then comment (not %)
        re.MULTILINE
    )

    # Block comment pattern - matches entire block
    BLOCK_COMMENT_PATTERN = re.compile(
        r'%\s*\{\s*(.*?)\s*\}%',
        re.DOTALL | re.MULTILINE
    )

    def __init__(self):
        """Initialize parser."""
        self._nesting_level = 0  # Track function/class nesting
        self._current_function = None  # Track current function
        self._current_class = None  # Track current class
        self._in_block_comment = False  # Track if in block comment

    def parse_file(self, file_path: str, file_uri: str) -> ParseResult:
        """
        Parse a MATLAB file.

        Args:
            file_path (str): Local path to file
            file_uri (str): URI of file

        Returns:
            ParseResult: Parsing result with extracted elements
        """
        logger.debug(f"Parsing file: {file_path}")

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ParseResult(
                file_uri=file_uri,
                file_path=file_path,
                raw_content="",
                errors=[{"error": f"Failed to read file: {e}"}]
            )

        # Parse content
        return self.parse_content(content, file_uri, file_path)

    def parse_content(
        self,
        content: str,
        file_uri: str,
        file_path: str
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
        lines = content.split('\n')
        functions: List[FunctionInfo] = []
        variables: List[VariableInfo] = []
        comments: List[CommentInfo] = []
        errors: List[Dict] = []

        # Reset state
        self._nesting_level = 0
        self._current_function = None
        self._current_class = None
        self._in_block_comment = False

        # First, extract all block comments from entire content
        block_comments = self._extract_block_comments(content)
        for block_comment in block_comments:
            comments.append(block_comment)

        # Remove block comments from content for further parsing
        content_without_blocks = self.BLOCK_COMMENT_PATTERN.sub('', content)
        lines_without_blocks = content_without_blocks.split('\n')

        for line_num, line in enumerate(lines_without_blocks, 1):
            # Map line number back to original (including removed lines)
            original_line_num = line_num  # Simplified - not accurate but works for now

            # Skip empty lines
            if not line.strip():
                continue

            # Check for comments (line-level)
            comment = self._extract_line_comment(line, original_line_num)
            if comment:
                comments.append(comment)
                # Remove comment from line for further parsing
                line = line[:comment.column - 1]
                if not line.strip():
                    continue

            # Check for function definition
            function_match = self._extract_function(line, original_line_num)
            if function_match:
                functions.append(function_match)
                if self._nesting_level == 0:
                    self._current_function = function_match
                self._nesting_level += 1
                continue

            # Check for class definition
            class_match = self._extract_class(line, original_line_num)
            if class_match:
                # Classes not supported in basic parser yet
                errors.append({
                    "line": original_line_num,
                    "warning": "Class definitions not fully supported"
                })
                continue

            # Check for function end
            if self._extract_end(line):
                if self._nesting_level > 0:
                    self._nesting_level -= 1
                    if self._nesting_level == 0:
                        self._current_function = None
                continue

            # Check for variable declaration
            if self._nesting_level == 0 or self._current_function:
                var_match = self._extract_variable(line, original_line_num)
                if var_match:
                    variables.append(var_match)

        logger.info(
            f"Parsed {len(functions)} functions, "
            f"{len(variables)} variables, "
            f"{len(comments)} comments"
        )

        return ParseResult(
            file_uri=file_uri,
            file_path=file_path,
            functions=functions,
            variables=variables,
            classes=[],  # Not implemented yet
            comments=comments,
            errors=errors,
            raw_content=content,
        )

    def _extract_function(
        self,
        line: str,
        line_num: int
    ) -> Optional[FunctionInfo]:
        """Extract function definition from line."""
        match = self.FUNCTION_PATTERN.match(line)
        if not match:
            return None

        # Extract function components
        outputs = match.group(1)
        name = match.group(2)
        inputs = match.group(3)

        # Parse outputs
        output_args = []
        if outputs:
            output_args = [s.strip() for s in outputs.split(',')]

        # Parse inputs
        input_args = []
        if inputs:
            input_args = [s.strip() for s in inputs.split(',')]

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
            is_nested=self._nesting_level > 0,
            parent_function=self._current_function.name if self._current_function else None,
        )

    def _extract_variable(
        self,
        line: str,
        line_num: int
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
        is_global = modifiers and 'global' in modifiers
        is_persistent = modifiers and 'persistent' in modifiers

        return VariableInfo(
            name=name,
            line=line_num,
            column=name_pos + 1,
            is_global=is_global,
            is_persistent=is_persistent,
        )

    def _extract_class(
        self,
        line: str,
        line_num: int
    ) -> Optional[ClassInfo]:
        """Extract class definition from line."""
        match = self.CLASS_PATTERN.match(line)
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
        )

    def _extract_end(self, line: str) -> bool:
        """Check if line is an end statement."""
        match = self.FUNCTION_END_PATTERN.match(line)
        return match is not None

    def _extract_comment(
        self,
        line: str,
        line_num: int
    ) -> Optional[CommentInfo]:
        """Extract comment from line."""
        # First check for block comments %{ ... }%
        block_match = self.BLOCK_COMMENT_PATTERN.search(line)
        if block_match:
            return CommentInfo(
                text=block_match.group(1),
                line=line_num,
                column=line.find('%') + 1,
                is_block=True,
            )

        # Check for line comments %
        match = self.COMMENT_PATTERN.match(line)
        if match and match.group(1).strip():  # Only if there's code before %
            return CommentInfo(
                text=match.group(2).strip(),
                line=line_num,
                column=line.find('%') + 1,
                is_block=False,
            )

        return None

    def _extract_block_comments(
        self,
        content: str
    ) -> List[CommentInfo]:
        """Extract all block comments from content.

        Args:
            content (str): Full file content

        Returns:
            List[CommentInfo]: List of block comments
        """
        block_comments = []

        for match in self.BLOCK_COMMENT_PATTERN.finditer(content):
            # Calculate line number (approximate)
            content_before = content[:match.start()]
            line_num = content_before.count('\n') + 1

            # Calculate column
            line_start = content.rfind('\n', 0, match.start())
            column = match.start() - line_start if line_start != -1 else match.start() + 1

            # Calculate end line
            content_with_block = content[:match.end()]
            end_line = content_with_block.count('\n') + 1

            block_comments.append(CommentInfo(
                text=match.group(1).strip(),
                line=line_num,
                column=column,
                is_block=True,
                block_start_line=line_num,
                block_end_line=end_line,
            ))

        return block_comments

    def _extract_line_comment(
        self,
        line: str,
        line_num: int
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
            code_before = match.group(1)
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

    def is_builtin_function(self, name: str) -> bool:
        """Check if name is a built-in MATLAB function."""
        return name in BUILTIN_FUNCTIONS or name in MATLAB_KEYWORDS
