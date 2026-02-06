# API Документация

Документация по API LSP MATLAB Server.

## Содержание

- [LSP Сервер](#lsp-сервер)
- [LSP Методы](#lsp-методы)
- [Конфигурация](#конфигурация)
- [Модели данных](#модели-данных)
- [Утилиты](#утилиты)

---

## LSP Сервер

### `MatLSServer`

Основной класс LSP сервера для MATLAB.

```python
from src.protocol.lifecycle import MatLSServer
```

#### Методы

##### `__init__(protocol: LanguageServerProtocol)`

Создает экземпляр сервера MATLAB.

**Параметры**:
- `protocol` (LanguageServerProtocol): Протокол LSP

**Пример**:
```python
from pygls.workspace import Workspace
from src.protocol.lifecycle import MatLSServer

server = MatLSServer()
```

---

## LSP Методы

### Lifecycle Methods

#### `initialize(params: InitializeParams) -> InitializeResult`

Инициализация LSP сервера. Первый вызываемый метод клиентом.

**Параметры**:
```python
from lsprotocol.types import InitializeParams

params = InitializeParams(
    process_id=1234,
    root_uri="file:///C:/project",
    capabilities=client_capabilities
)
```

**Возвращает**: `InitializeResult`

**Пример ответа**:
```python
{
    "capabilities": {
        "text_document_sync": 1,
        "completion_provider": {
            "trigger_characters": [".", "("],
            "resolve_provider": False
        },
        "hover_provider": True,
        "definition_provider": True,
        "diagnostic_provider": {
            "inter_file_dependencies": True,
            "workspace_diagnostics": False
        }
    }
}
```

#### `initialized(params: InitializedResult) -> None`

Уведомление об успешной инициализации.

**Параметры**:
```python
from lsprotocol.types import InitializedResult
```

#### `shutdown() -> None`

Подготовка к завершению работы сервера.

#### `exit() -> None`

Завершение работы сервера.

---

### Document Synchronization

#### `textDocument/didOpen(params: DidOpenTextDocumentParams) -> None`

Уведомление об открытии документа.

**Параметры**:
```python
from lsprotocol.types import DidOpenTextDocumentParams

params = DidOpenTextDocumentParams(
    text_document=TextDocumentItem(
        uri="file:///C:/project/test.m",
        language_id="matlab",
        version=1,
        text="function foo() end"
    )
)
```

#### `textDocument/didChange(params: DidChangeTextDocumentParams) -> None`

Уведомление об изменении содержимого документа.

**Параметры**:
```python
from lsprotocol.types import DidChangeTextDocumentParams

params = DidChangeTextDocumentParams(
    text_document=VersionedTextDocumentIdentifier(
        uri="file:///C:/project/test.m",
        version=2
    ),
    content_changes=[
        TextDocumentContentChangeEvent(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0)
            ),
            text="% New comment\n"
        )
    ]
)
```

#### `textDocument/didClose(params: DidCloseTextDocumentParams) -> None`

Уведомление о закрытии документа.

#### `textDocument/didSave(params: DidSaveTextDocumentParams) -> None`

Уведомление о сохранении документа.

---

### Completion

#### `textDocument/completion(params: CompletionParams) -> CompletionList`

Предоставляет варианты автодополнения.

**Параметры**:
```python
from lsprotocol.types import CompletionParams

params = CompletionParams(
    text_document=TextDocumentIdentifier(uri="file:///C:/project/test.m"),
    position=Position(line=2, character=5)
)
```

**Возвращает**: `CompletionList`

**Пример ответа**:
```python
{
    "is_incomplete": False,
    "items": [
        CompletionItem(
            label="plot",
            kind=CompletionItemKind.Function,
            detail="function plot(x, y)",
            documentation="Create a 2-D line plot",
            insert_text="plot",
            sort_text="plot"
        ),
        CompletionItem(
            label="plot3",
            kind=CompletionItemKind.Function,
            detail="function plot3(x, y, z)",
            documentation="Create a 3-D line plot",
            insert_text="plot3",
            sort_text="plot3"
        )
    ]
}
```

**CompletionItemKind** поддерживаемые типы:
- `Function` - MATLAB функции
- `Variable` - переменные
- `Class` - классы MATLAB
- `Method` - методы классов
- `Property` - свойства классов

---

### Hover

#### `textDocument/hover(params: HoverParams) -> Hover`

Предоставляет информацию при наведении курсора.

**Параметры**:
```python
from lsprotocol.types import HoverParams

params = HoverParams(
    text_document=TextDocumentIdentifier(uri="file:///C:/project/test.m"),
    position=Position(line=1, character=3)
)
```

**Возвращает**: `Hover`

**Пример ответа**:
```python
{
    "contents": {
        "kind": "markdown",
        "value": "```matlab\nfunction plot(x, y)\n```\n\nCreate a 2-D line plot\n\n**Parameters:**\n- `x`: Vector of x-coordinates\n- `y`: Vector of y-coordinates"
    },
    "range": {
        "start": {"line": 1, "character": 0},
        "end": {"line": 1, "character": 4}
    }
}
```

---

### Definition

#### `textDocument/definition(params: DefinitionParams) -> Location | Location[]`

Переход к определению символа.

**Параметры**:
```python
from lsprotocol.types import DefinitionParams

params = DefinitionParams(
    text_document=TextDocumentIdentifier(uri="file:///C:/project/test.m"),
    position=Position(line=2, character=8)
)
```

**Возвращает**: `Location` или `Location[]`

**Пример ответа**:
```python
{
    "uri": "file:///C:/project/myfunction.m",
    "range": {
        "start": {"line": 0, "character": 9},
        "end": {"line": 0, "character": 20}
    }
}
```

---

### References

#### `textDocument/references(params: ReferenceParams) -> Location[]`

Поиск всех использований символа.

**Параметры**:
```python
from lsprotocol.types import ReferenceParams

params = ReferenceParams(
    text_document=TextDocumentIdentifier(uri="file:///C:/project/test.m"),
    position=Position(line=2, character=8),
    context=ReferenceContext(include_declaration=True)
)
```

**Возвращает**: `Location[]`

**Пример ответа**:
```python
[
    {
        "uri": "file:///C:/project/test.m",
        "range": {
            "start": {"line": 2, "character": 5},
            "end": {"line": 2, "character": 15}
        }
    },
    {
        "uri": "file:///C:/project/other.m",
        "range": {
            "start": {"line": 5, "character": 10},
            "end": {"line": 5, "character": 20}
        }
    }
]
```

---

### Document Symbol

#### `textDocument/documentSymbol(params: DocumentSymbolParams) -> DocumentSymbol[] | SymbolInformation[]`

Предоставляет структуру документа.

**Параметры**:
```python
from lsprotocol.types import DocumentSymbolParams

params = DocumentSymbolParams(
    text_document=TextDocumentIdentifier(uri="file:///C:/project/test.m")
)
```

**Возвращает**: `DocumentSymbol[]`

**Пример ответа**:
```python
[
    {
        "name": "myFunction",
        "detail": "function myFunction(x, y)",
        "kind": SymbolKind.Function,
        "range": {
            "start": {"line": 0, "character": 0},
            "end": {"line": 10, "character": 3}
        },
        "selection_range": {
            "start": {"line": 0, "character": 9},
            "end": {"line": 0, "character": 20}
        },
        "children": [
            {
                "name": "nestedFunction",
                "detail": "function nestedFunction()",
                "kind": SymbolKind.Function,
                "range": {
                    "start": {"line": 5, "character": 4},
                    "end": {"line": 7, "character": 7}
                }
            }
        ]
    }
]
```

---

### Code Action

#### `textDocument/codeAction(params: CodeActionParams) -> CodeAction[]`

Предоставляет исправления кода.

**Параметры**:
```python
from lsprotocol.types import CodeActionParams

params = CodeActionParams(
    text_document=TextDocumentIdentifier(uri="file:///C:/project/test.m"),
    range=Range(
        start=Position(line=2, character=0),
        end=Position(line=2, character=20)
    ),
    context=CodeActionContext(
        diagnostics=[
            Diagnostic(
                range=Range(
                    start=Position(line=2, character=5),
                    end=Position(line=2, character=15)
                ),
                message="Undefined function or variable 'x'."
            )
        ]
    )
)
```

**Возвращает**: `CodeAction[]`

**Пример ответа**:
```python
[
    {
        "title": "Remove unused variable",
        "kind": "quickfix",
        "diagnostics": [...],
        "edit": {
            "documentChanges": [
                TextDocumentEdit(
                    text_document=VersionedTextDocumentIdentifier(
                        uri="file:///C:/project/test.m",
                        version=2
                    ),
                    edits=[
                        TextEdit(
                            range=Range(
                                start=Position(line=2, character=0),
                                end=Position(line=2, character=20)
                            ),
                            new_text=""
                        )
                    ]
                )
            ]
        }
    }
]
```

---

### Formatting

#### `textDocument/formatting(params: DocumentFormattingParams) -> TextEdit[]`

Форматирование всего документа.

**Параметры**:
```python
from lsprotocol.types import DocumentFormattingParams, FormattingOptions

params = DocumentFormattingParams(
    text_document=TextDocumentIdentifier(uri="file:///C:/project/test.m"),
    options=FormattingOptions(
        tab_size=4,
        insert_spaces=True
    )
)
```

**Возвращает**: `TextEdit[]`

**Пример ответа**:
```python
[
    {
        "range": {
            "start": {"line": 0, "character": 0},
            "end": {"line": 0, "character": 20}
        },
        "new_text": "    function myFunction()"
    }
]
```

---

## Конфигурация

### Файл конфигурации

`.matlab-lsprc.json` в корне проекта:

```json
{
  "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
  "maxDiagnostics": 100,
  "diagnosticRules": {
    "all": true,
    "unusedVariable": true,
    "missingSemicolon": false
  },
  "formatting": {
    "indentSize": 4,
    "insertSpaces": true
  },
  "completion": {
    "enableSnippets": true,
    "maxSuggestions": 50
  }
}
```

### Конфигурация через workspace/didChangeConfiguration

Клиент может отправить конфигурацию:

```json
{
  "method": "workspace/didChangeConfiguration",
  "params": {
    "settings": {
      "matlab": {
        "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
        "maxDiagnostics": 100
      }
    }
  }
}
```

---

## Модели данных

### FunctionInfo

```python
@dataclass
class FunctionInfo:
    name: str
    line: int
    column: int
    end_line: int
    end_column: int
    parameters: List[str]
    return_values: List[str]
    is_nested: bool = False
    documentation: Optional[str] = None
```

### VariableInfo

```python
@dataclass
class VariableInfo:
    name: str
    line: int
    column: int
    type_hint: Optional[str] = None
    is_global: bool = False
    is_persistent: bool = False
```

### ClassInfo

```python
@dataclass
class ClassInfo:
    name: str
    line: int
    column: int
    end_line: int
    end_column: int
    properties: List[PropertyInfo]
    methods: List[MethodInfo]
    documentation: Optional[str] = None
```

### PropertyInfo

```python
@dataclass
class PropertyInfo:
    name: str
    line: int
    column: int
    type_hint: Optional[str] = None
    access: str = "public"  # public, protected, private
    documentation: Optional[str] = None
```

### MethodInfo

```python
@dataclass
class MethodInfo:
    name: str
    line: int
    column: int
    parameters: List[str]
    return_type: Optional[str] = None
    access: str = "public"
    is_static: bool = False
    documentation: Optional[str] = None
```

### ParseResult

```python
@dataclass
class ParseResult:
    uri: str
    functions: List[FunctionInfo]
    variables: List[VariableInfo]
    classes: List[ClassInfo]
    comments: List[CommentInfo]
    parse_errors: List[ParseError]
    timestamp: float
```

---

## Утилиты

### CacheManager

```python
from src.utils.cache import CacheManager

cache = CacheManager()

# Сохранить результат парсинга
cache.set_parse_result("file:///path/to/test.m", parse_result)

# Получить результат
result = cache.get_parse_result("file:///path/to/test.m")

# Инвалидировать кэш
cache.invalidate("file:///path/to/test.m")

# Очистить весь кэш
cache.clear()
```

### ConfigManager

```python
from src.utils.config import ConfigManager

config = ConfigManager()

# Получить путь к MATLAB
matlab_path = config.get_matlab_path()

# Получить правила диагностики
rules = config.get_diagnostic_rules()

# Получить настройки форматирования
formatting = config.get_formatting_options()

# Перезагрузить конфигурацию
config.reload()
```

### Logger

```python
from src.utils.logging import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## Диагностика

### LSP Diagnostic Severity

- `Error` (1) - Критические ошибки
- `Warning` (2) - Предупреждения
- `Information` (3) - Информационные сообщения
- `Hint` (4) - Подсказки

### mlint to LSP Diagnostic Mapping

| mlint ID | Описание | LSP Severity |
|----------|-----------|--------------|
| CP019 | Call to undefined function | Error |
| CP010 | Value assigned to variable might be unused | Warning |
| CP014 | Variable appears to change size | Information |
| CP006 | Multiple end statements close this block | Error |

### Пример диагностики

```python
Diagnostic(
    range=Range(
        start=Position(line=2, character=5),
        end=Position(line=2, character=15)
    ),
    message="Undefined function or variable 'x'.",
    severity=DiagnosticSeverity.Error,
    source="matlab-mlint",
    code="CP019",
    code_description=CodeDescription(
        href="https://www.mathworks.com/help/matlab/ref/CP019.html"
    ),
    tags=[DiagnosticTag.Unnecessary]
)
```

---

## Ошибки

### Server Error Codes

| Код | Описание |
|-----|----------|
| -32600 | Invalid Request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
| -32800 | Request cancelled |

### Custom Error Codes

| Код | Описание |
|-----|----------|
| 1001 | MATLAB not found |
| 1002 | Parse error |
| 1003 | Analysis timeout |

---

## Типизация

### Использование lsprotocol

```python
from lsprotocol.types import (
    InitializeParams,
    InitializeResult,
    CompletionParams,
    CompletionList,
    CompletionItem,
    CompletionItemKind
)
```

### Custom Types

```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class MatlabSymbol:
    name: str
    kind: SymbolKind
    location: Location
    documentation: Optional[str] = None
```

---

## События

### Server Events

```python
# Настройка обработчиков событий
@server.feature(
    "textDocument/didOpen",
    DidOpenTextDocumentParams
)
def did_open(server: MatLSServer, params: DidOpenTextDocumentParams):
    pass

# Или через декоратор
from pygls.protocol import language_server_protocol

@language_server_protocol.feature("textDocument/didOpen")
def handle_did_open(ls, params: DidOpenTextDocumentParams):
    pass
```

---

## Дополнительные возможности

### Workspace Symbols

```
workspace/symbol(params: WorkspaceSymbolParams) -> SymbolInformation[]
```

Поиск символов по всему рабочему пространству.

**Параметры**:
```python
params = WorkspaceSymbolParams(query="myFunction")
```

### Execute Command

```
workspace/executeCommand(params: ExecuteCommandParams) -> Any
```

Выполнение пользовательских команд сервера.

**Поддерживаемые команды**:
- `matlint.analyzeFile` - Анализировать файл
- `matlint.refreshCache` - Обновить кэш
- `matlint.restartServer` - Перезапустить сервер

---

## Примеры использования

### Python клиент

```python
from pygls.client import LanguageServerClient
from lsprotocol.types import InitializeParams
import asyncio

async def main():
    client = LanguageServerClient("python", ["server.py", "--stdio"])

    await client.start()

    result = await client.initialize(InitializeParams(
        process_id=1234,
        root_uri="file:///C:/project",
        capabilities={}
    ))

    print(f"Server capabilities: {result.capabilities}")

    await client.shutdown()
    await client.stop()

asyncio.run(main())
```

### Прямое JSON-RPC

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "processId": 1234,
    "rootUri": "file:///C:/project",
    "capabilities": {}
  }
}
```

---

## Информация о версии

Получение версии сервера:

```
python server.py --version
```

**Пример вывода**:
```
MATLAB LSP Server v0.1.0
LSP Version: 3.17.0
Python: 3.10.0
```

---

## Справка

Для получения помощи:

```bash
python server.py --help
```

---

> **Примечание**: Данная документация API постоянно обновляется по мере развития проекта. Для получения самой актуальной информации используйте MCP инструменты:
> - **context7 MCP** - для анализа исходного кода pygls и официальной документации LSP
> - **z_ai MCP** - для генерации примеров использования API
> - **DuckDuckGo MCP** - для поиска обновлений спецификации LSP
> - **z_ai_tools MCP** - для анализа примеров кода из изображений и диаграмм
