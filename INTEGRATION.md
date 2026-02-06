# Инструкция по интеграции в TUI Crush

Документация по интеграции MATLAB LSP Server в TUI Crush.

## Содержание

- [Обзор](#обзор)
- [Требования](#требования)
- [Установка](#установка)
- [Настройка TUI Crush](#настройка-tui-crush)
- [Проверка интеграции](#проверка-интеграции)
- [Использование](#использование)
- [Устранение проблем](#устранение-проблем)
- [Конфигурация для других редакторов](#конфигурация-для-других-редакторов)

---

## Обзор

**TUI Crush** - это терминальный UI AI-ассистент с поддержкой Language Server Protocol. MATLAB LSP Server можно интегрировать для обеспечения:

- 🔍 Диагностики ошибок и предупреждений
- 💡 Автодополнения кода
- 📖 Подсказок при наведении
- 🔗 Перехода к определениям
- 📑 Навигации по структуре файла

---

## Требования

1. **TUI Crush**: Последняя версия с поддержкой LSP
2. **Python**: 3.10 или новее
3. **MATLAB**: R2020b или новее (для mlint)
4. **MATLAB LSP Server**: Установленный и сконфигурированный

---

## Установка

### 1. Клонирование и установка сервера

```bash
# Клонируйте репозиторий
git clone https://github.com/your-username/lsp_matlab_for_windows.git
cd lsp_matlab_for_windows

# Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка пути к MATLAB

Создайте файл `.matlab-lsprc.json` в корне проекта:

```json
{
  "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
  "maxDiagnostics": 100,
  "diagnosticRules": {
    "all": true
  }
}
```

Или установите переменную окружения:

```batch
setx MATLAB_PATH "C:\Program Files\MATLAB\R2023b\bin\win64"
```

### 3. Проверка работы сервера

```bash
# Запуск в режиме тестирования
python server.py --tcp --port 4389

# В другом терминале проверьте подключение
telnet localhost 4389
```

---

## Настройка TUI Crush

### Базовая конфигурация

Откройте файл `.crush.json` и добавьте LSP конфигурацию:

```json
{
  "$schema": "https://charm.land/crush.json",
  "providers": {
    // ... существующие провайдеры
  },
  "models": {
    // ... существующие модели
  },
  "options": {
    // ... существующие опции
  },
  "mcp": {
    // ... существующие MCP серверы
  },
  "lsp": {
    "matlab": {
      "command": "python",
      "args": [
        "C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows/server.py",
        "--stdio"
      ],
      "filetypes": ["matlab", "m"],
      "rootPatterns": [
        ".git",
        ".matlab-lsprc.json"
      ],
      "workspace": [
        "C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows"
      ],
      "settings": {
        "matlab": {
          "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64"
        }
      }
    }
  }
}
```

### Полная конфигурация с расширенными опциями

```json
{
  "$schema": "https://charm.land/crush.json",
  "providers": {
    // ... провайдеры
  },
  "models": {
    // ... модели
  },
  "options": {
    "debug_lsp": true,
    "auto_lsp": true,
    "tui": {
      "compact_mode": false
    }
  },
  "lsp": {
    "matlab": {
      "command": "python",
      "args": [
        "C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows/server.py",
        "--stdio",
        "--verbose"
      ],
      "filetypes": ["matlab", "m"],
      "rootPatterns": [
        ".git",
        ".matlab-lsprc.json",
        "project.m"
      ],
      "workspace": [
        "C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows",
        "C:/Users/MSI/Desktop/other/matlab/project"
      ],
      "settings": {
        "matlab": {
          "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
          "maxDiagnostics": 100,
          "diagnosticRules": {
            "all": true,
            "unusedVariable": true,
            "missingSemicolon": false
          },
          "completion": {
            "enableSnippets": true,
            "maxSuggestions": 50
          },
          "formatting": {
            "indentSize": 4,
            "insertSpaces": true
          }
        }
      },
      "env": {
        "PYTHONPATH": "C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows/src",
        "MATLAB_PATH": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64"
      },
      "initializationOptions": {
        "maxNumberOfProblems": 100,
        "trace": "verbose"
      }
    }
  }
}
```

### Параметры конфигурации

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `command` | string | Да | Команда для запуска сервера |
| `args` | array | Да | Аргументы командной строки |
| `filetypes` | array | Да | Список ассоциируемых расширений файлов |
| `rootPatterns` | array | Нет | Паттерны для определения корня проекта |
| `workspace` | array | Да | Путь к рабочим каталогам |
| `settings` | object | Нет | Настройки сервера |
| `env` | object | Нет | Переменные окружения |
| `initializationOptions` | object | Нет | Опции инициализации |

---

## Проверка интеграции

### 1. Запуск TUI Crush

```bash
crush
```

### 2. Открытие MATLAB файла

```bash
# В TUI Crush
:e C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows/for_tests/test_matlab_lsp_simple.m
```

### 3. Проверка LSP статуса

TUI Crush покажет:
- Статус подключения к LSP серверу
- Количество диагностики в текущем файле
- Возможности сервера (completion, hover, definition и т.д.)

### 4. Тестирование функций

#### Диагностика

```matlab
% test.m
function simple_test()
    x = 10
    y = x + z  % Ошибка: z не определена - должно быть подсвечено
    result = undefined_function(x)  % Ошибка: функция не существует
end
```

Ожидаемый результат:
- Красное подчеркивание для строк с ошибками
- Сообщение об ошибке при наведении

#### Автодополнение

```matlab
% Начните вводить
pl
% Нажмите Tab или Ctrl+Space для автодополнения
% Должны появиться варианты: plot, plot3, plotyy и т.д.
```

#### Переход к определению

```matlab
% В одном файле
function main()
    % Наведите на myFunction и нажмите gd
    result = myFunction(10);
end

function result = myFunction(x)
    result = x * 2;
end
```

Нажмите `gd` (go to definition) для перехода.

---

## Использование

### Горячие клавиши TUI Crush

| Команда | Горячая клавиша | Описание |
|---------|-----------------|----------|
| Автодополнение | `Ctrl+Space` | Показать список дополнений |
| Подсказка | `K` | Показать информацию о символе |
| Переход к определению | `gd` | Перейти к определению |
| Переход обратно | `Ctrl+o` | Вернуться назад |
| Список диагностик | `]d` / `[d` | Следующая/предыдущая диагностика |
| Список символов файла | `Ctrl+Shift+o` | Структура документа |
| Список символов проекта | `Ctrl+t` | Символы рабочей области |

### Командная строка TUI Crush

```
:LspInfo              - Информация о LSP серверах
:LspRestart           - Перезапустить LSP сервер
:LspStop              - Остановить LSP сервер
:LspStart             - Запустить LSP сервер
:Diagnostics          - Показать все диагностики
:WorkspaceSymbol      - Поиск символов проекта
:DocumentSymbol       - Структура текущего файла
:CodeAction           - Исправления для текущего курсора
```

### Примеры использования

#### Просмотр диагностики

```
:Diagnostics
```

Покажет список всех проблем в проекте:
```
Errors: 2, Warnings: 3
  test.m:3 - CP019: Undefined function or variable 'z'
  test.m:4 - CP019: Undefined function 'undefined_function'
  test.m:5 - CP010: Value assigned to 'result' might be unused
```

#### Поиск символов проекта

```
:WorkspaceSymbol
```

Введите имя функции для поиска:
```
Query: plot
Results:
  plot.m - plot (function)
  plot3.m - plot3 (function)
  my_plot.m - my_plot (function)
```

#### Быстрое исправление

Наведите на ошибку и выполните:
```
:CodeAction
```

Покажет доступные исправления.

---

## Устранение проблем

### Сервер не запускается

**Симптом**: TUI Crush не может подключиться к LSP серверу

**Решения**:

1. Проверьте путь к Python:
```json
"command": "C:/Python310/python.exe"
```

2. Проверьте путь к серверу:
```json
"args": [
  "C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows/server.py",
  "--stdio"
]
```

3. Проверьте зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите сервер вручную для проверки:
```bash
python server.py --verbose
```

5. Проверьте логи TUI Crush:
```json
{
  "options": {
    "debug_lsp": true
  }
}
```

### MATLAB не найден

**Симптом**: Сервер сообщает, что MATLAB mlint не найден

**Решения**:

1. Укажите правильный путь:
```json
{
  "lsp": {
    "matlab": {
      "settings": {
        "matlab": {
          "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64"
        }
      }
    }
  }
}
```

2. Или используйте переменную окружения:
```batch
setx MATLAB_PATH "C:\Program Files\MATLAB\R2023b\bin\win64"
```

3. Проверьте, что mlint.exe существует:
```batch
dir "C:\Program Files\MATLAB\R2023b\bin\win64\mlint.exe"
```

### Диагностика не появляется

**Симптом**: Нет подсветки ошибок в .m файлах

**Решения**:

1. Убедитесь, что файл имеет расширение `.m`
2. Проверьте, что filetype распознается:
```
:set filetype?
```

3. Перезапустите LSP сервер:
```
:LspRestart
```

4. Включите отладку:
```json
{
  "options": {
    "debug_lsp": true
  }
}
```

5. Проверьте правила диагностики:
```json
{
  "lsp": {
    "matlab": {
      "settings": {
        "matlab": {
          "diagnosticRules": {
            "all": true
          }
        }
      }
    }
  }
}
```

### Автодополнение не работает

**Симптом**: Нет подсказок при вводе кода

**Решения**:

1. Проверьте, что completion включен в возможностях:
```
:LspInfo
```

2. Убедитесь, что сервер инициализирован:
```
:lua print(vim.lsp.get_active_clients())
```

3. Проверьте настройки автодополнения:
```json
{
  "lsp": {
    "matlab": {
      "settings": {
        "matlab": {
          "completion": {
            "enableSnippets": true
          }
        }
      }
    }
  }
}
```

### Медленная работа

**Симптом**: Задержки при редактировании

**Решения**:

1. Уменьшите количество диагностики:
```json
{
  "lsp": {
    "matlab": {
      "settings": {
        "matlab": {
          "maxDiagnostics": 50
        }
      }
    }
  }
}
```

2. Отключите ненужные правила:
```json
{
  "lsp": {
    "matlab": {
      "settings": {
        "matlab": {
          "diagnosticRules": {
            "all": false,
            "unusedVariable": true,
            "undefinedFunction": true
          }
        }
      }
    }
  }
}
```

3. Увеличьте лимиты кэша:
```json
{
  "lsp": {
    "matlab": {
      "settings": {
        "matlab": {
          "cache": {
            "maxSize": 1000
          }
        }
      }
    }
  }
}
```

---

## Конфигурация для других редакторов

### VS Code

```json
// .vscode/settings.json
{
  "matlab-lsp.matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
  "files.associations": {
    "*.m": "matlab"
  }
}
```

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "matlab",
      "request": "launch",
      "name": "Run MATLAB Code",
      "program": "${file}"
    }
  ]
}
```

### Neovim

```lua
-- init.lua
local lspconfig = require('lspconfig')

lspconfig.matlab_lsp.setup {
  cmd = { 'python', 'C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows/server.py', '--stdio' },
  filetypes = { 'matlab', 'm' },
  root_dir = lspconfig.util.root_pattern('.git', '.matlab-lsprc.json'),
  settings = {
    matlab = {
      matlabPath = "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
      maxDiagnostics = 100
    }
  }
}
```

### Vim

```vim
" .vimrc
autocmd BufRead,BufNewFile *.m set filetype=matlab

if executable('python')
  au User lsp_setup call lsp#register_server({
    \ 'name': 'matlab-lsp',
    \ 'cmd': {server_info->['python', 'C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows/server.py', '--stdio']},
    \ 'whitelist': ['matlab', 'm'],
    \ 'workspace_config': {
    \   'matlab': {
    \     'matlabPath': 'C:\\Program Files\\MATLAB\\R2023b\\bin\\win64'
    \   }
    \ }
    \ })
endif
```

### Emacs

```elisp
;; init.el
(use-package lsp-mode
  :hook ((matlab-mode . lsp))
  :commands lsp)

(use-package lsp-matlab
  :after lsp-mode
  :config
  (setq lsp-matlab-server-path "python")
  (setq lsp-matlab-server-args '("C:/Users/MSI/Desktop/projects/lsp_matlab_for_windows/server.py" "--stdio"))
  (setq lsp-matlab-matlab-path "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64"))
```

---

## Продвинутая конфигурация

### Несколько рабочих пространств

```json
{
  "lsp": {
    "matlab": {
      "workspace": [
        "C:/project1",
        "C:/project2",
        "C:/project3"
      ]
    }
  }
}
```

### Проектная конфигурация

Создайте `.matlab-lsprc.json` в каждом проекте:

```json
{
  "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
  "exclude": [
    "**/*.m~",
    "**/deprecated/**",
    "**/tests/fixtures/**"
  ],
  "include": [
    "**/*.m",
    "**/*.mlx"
  ]
}
```

### Конфигурация диагностики по типу

```json
{
  "lsp": {
    "matlab": {
      "settings": {
        "matlab": {
          "diagnosticRules": {
            "syntax": true,
            "runtime": true,
            "style": false,
            "unusedVariable": true,
            "missingSemicolon": false
          }
        }
      }
    }
  }
}
```

---

## Мониторинг и отладка

### Просмотр LSP логов

Включите отладку в `.crush.json`:

```json
{
  "options": {
    "debug_lsp": true
  }
}
```

Логи будут доступны в:
- Вывод TUI Crush
- Файл логов сервера (если настроен)

### Проверка серверных сообщений

```bash
# Запуск в TCP режиме для просмотра сообщений
python server.py --tcp --port 4389 --verbose

# Отправьте JSON-RPC сообщение для теста
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | nc localhost 4389
```

---

## Примеры рабочих конфигураций

### Минимальная конфигурация

```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["C:/path/to/server.py", "--stdio"],
      "filetypes": ["matlab", "m"],
      "workspace": ["C:/my/matlab/project"]
    }
  }
}
```

### Конфигурация для разработки

```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["C:/path/to/server.py", "--stdio", "--verbose"],
      "filetypes": ["matlab", "m"],
      "workspace": ["C:/my/matlab/project"],
      "settings": {
        "matlab": {
          "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
          "diagnosticRules": {
            "all": true
          }
        }
      }
    }
  }
}
```

### Конфигурация для production

```json
{
  "lsp": {
    "matlab": {
      "command": "python",
      "args": ["C:/path/to/server.py", "--stdio"],
      "filetypes": ["matlab", "m"],
      "workspace": ["C:/my/matlab/project"],
      "settings": {
        "matlab": {
          "matlabPath": "C:\\Program Files\\MATLAB\\R2023b\\bin\\win64",
          "maxDiagnostics": 50,
          "diagnosticRules": {
            "all": false,
            "syntax": true,
            "runtime": true
          }
        }
      }
    }
  }
}
```

---

## Дополнительные ресурсы

- [TUI Crush Documentation](https://charm.sh/crush/)
- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [pygls Documentation](https://pygls.readthedocs.io/)
- [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура сервера
- [DOCUMENTATION.md](DOCUMENTATION.md) - API документация

---

> **Примечание**: При возникновении проблем с интеграцией используйте MCP инструменты для:
> - **z_ai MCP** - генерации конфигураций и решения проблем
> - **context7 MCP** - получения актуальной документации по TUI Crush и LSP
> - **DuckDuckGo MCP** - поиска аналогичных конфигураций и решений
> - **z_ai_tools MCP** - анализа логов и сообщений об ошибках из скриншотов
> - **Filesystem MCP** - проверки структуры проекта и путей к файлам
>
> Пример использования агента:
> ```
> agent: "Найди конфигурации TUI Crush для LSP серверов, проанализируй и предложи оптимальную настройку"
> ```
