"""
Data models for MATLAB parser.

This module defines data structures for representing
MATLAB code elements (functions, variables, etc.).
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VariableInfo:
    """Represents a MATLAB variable declaration.

    Attributes:
        name (str): Variable name
        type (str): Variable type (if inferred)
        line (int): Line number where variable is declared
        column (int): Column number where variable is declared
        is_global (bool): Whether variable is global
        is_persistent (bool): Whether variable is persistent
    """

    name: str
    type: Optional[str] = None
    line: int = 1
    column: int = 1
    is_global: bool = False
    is_persistent: bool = False


@dataclass
class FunctionInfo:
    """Represents a MATLAB function definition.

    Attributes:
        name (str): Function name
        line (int): Line number where function is defined
        column (int): Column number where function is defined
        end_line (int): Line number where function ends
        end_column (int): Column number where function ends
        input_args (List[str]): List of input parameter names
        output_args (List[str]): List of output parameter names
        is_nested (bool): Whether this is a nested function
        parent_function (str): Parent function name (if nested)
        parent_class (str): Parent class name (if method)
        docstring (Optional[str]): Function documentation
        variables (List[VariableInfo]): Variables defined in this function
    """

    name: str
    line: int = 1
    column: int = 1
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    input_args: List[str] = field(default_factory=list)
    output_args: List[str] = field(default_factory=list)
    is_nested: bool = False
    parent_function: Optional[str] = None
    parent_class: Optional[str] = None
    docstring: Optional[str] = None
    variables: List[VariableInfo] = field(default_factory=list)


@dataclass
class ClassInfo:
    """Represents a MATLAB class definition.

    Attributes:
        name (str): Class name
        line (int): Line number where class is defined
        column (int): Column number where class is defined
        end_line (int): Line number where class ends
        properties (List[str]): List of property names
        methods (List[FunctionInfo]): List of method definitions
        docstring (Optional[str]): Class documentation
    """

    name: str
    line: int = 1
    column: int = 1
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    properties: List[str] = field(default_factory=list)
    methods: List[FunctionInfo] = field(default_factory=list)
    docstring: Optional[str] = None


@dataclass
class CommentInfo:
    """Represents a MATLAB comment.

    Attributes:
        text (str): Comment text (without % prefix)
        line (int): Line number where comment is
        column (int): Column number where comment starts
        is_block (bool): Whether this is a block comment %{ ... %}
        block_start_line (Optional[int]): Line where block comment starts
        block_end_line (Optional[int]): Line where block comment ends
    """

    text: str
    line: int = 1
    column: int = 1
    is_block: bool = False
    block_start_line: Optional[int] = None
    block_end_line: Optional[int] = None


@dataclass
class ParseResult:
    """Result of parsing a MATLAB file.

    Attributes:
        file_uri (str): URI of the parsed file
        file_path (str): Local path to the parsed file
        functions (
            List[FunctionInfo]
        ): List of function definitions (top-level and nested)
        variables (
            List[VariableInfo]
        ): List of variable declarations (global only)
        classes (List[ClassInfo]): List of class definitions
        comments (List[CommentInfo]): List of comments
        errors (List[Dict]): List of parsing errors
        raw_content (str): Raw file content
        function_tree (
            Dict[str, List[str]]
        ): Function hierarchy (parent -> children)
    """

    file_uri: str
    file_path: str
    functions: List[FunctionInfo] = field(default_factory=list)
    variables: List[VariableInfo] = field(default_factory=list)
    classes: List[ClassInfo] = field(default_factory=list)
    comments: List[CommentInfo] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    raw_content: str = ""
    function_tree: Dict[str, List[str]] = field(
        default_factory=dict
    )  # Parent -> children


# Built-in MATLAB functions and keywords
BUILTIN_FUNCTIONS = {
    "abs",
    "acos",
    "asin",
    "atan",
    "atan2",
    "ceil",
    "cos",
    "cosh",
    "exp",
    "factorial",
    "floor",
    "gcd",
    "hypot",
    "log",
    "log10",
    "log2",
    "max",
    "min",
    "mod",
    "nthroot",
    "pow",
    "prod",
    "real",
    "rem",
    "round",
    "sec",
    "sech",
    "sign",
    "sin",
    "sinh",
    "sqrt",
    "tan",
    "tanh",
    "eye",
    "ones",
    "zeros",
    "rand",
    "randn",
    "linspace",
    "linspace",
    "logspace",
    "meshgrid",
    "ndgrid",
    "eig",
    "eigs",
    "svd",
    "lu",
    "qr",
    "chol",
    "eig",
    "fft",
    "ifft",
    "fft2",
    "ifft2",
    "cell",
    "struct",
    "num2cell",
    "num2struct",
    "size",
    "length",
    "ndims",
    "numel",
    "isa",
    "isnumeric",
    "ischar",
    "islogical",
    "isinteger",
    "isfloat",
    "strfind",
    "strcmp",
    "strncmp",
    "strrep",
    "lower",
    "upper",
    "char",
    "double",
    "single",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "logical",
    "sparse",
    "full",
    "cat",
    "horzcat",
    "vertcat",
    "permute",
    "ipermute",
    "reshape",
    "squeeze",
    "sub2ind",
    "ind2sub",
    "shiftdim",
    "circshift",
    "find",
    "cumsum",
    "cumprod",
    "diff",
    "repmat",
    "kron",
    "all",
    "any",
    "exist",
    "strcmpi",
    "strmatch",
    "datestr",
    "datenum",
    "datevec",
    "weekday",
    "calendar",
    "clock",
    "etime",
    "cputime",
    "tic",
    "toc",
    "pause",
    "drawnow",
    "save",
    "load",
    "clear",
    "close",
    "fopen",
    "fclose",
    "fprintf",
    "fscanf",
    "fgets",
    "disp",
    "input",
    "keyboard",
    "error",
    "warning",
    "help",
    "doc",
    "which",
    "type",
    "ver",
    "license",
    "version",
}

MATLAB_KEYWORDS = {
    "function",
    "end",
    "if",
    "else",
    "elseif",
    "for",
    "while",
    "switch",
    "case",
    "otherwise",
    "break",
    "continue",
    "return",
    "global",
    "persistent",
    "try",
    "catch",
    "classdef",
    "properties",
    "methods",
    "events",
    "enumeration",
    "import",
    "export",
    "package",
}
