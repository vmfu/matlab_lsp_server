# LSP MATLAB Server Architecture

Document describing the architecture and design decisions of LSP MATLAB Server.

## Overview

LSP MATLAB Server is an event-driven Language Server Protocol (LSP) implementation built with Python and pygls framework. The server provides intelligent code editing features for MATLAB files (.m, .mlx).

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   LSP Client (IDE)                 │
└────────────────────────────────────┬────────────────────┘
                             │ LSP Protocol
                             │ (JSON-RPC)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              LSP MATLAB Server (pygls)          │
└────────────────────────────────────┬────────────────────┘
                             │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
       ▼                       ▼                       ▼
┌─────────────┐    ┌─────────────────┐    ┌──────────────┐
│  Handlers   │    │   Protocol      │    │   Features   │
│             │    │                 │    │              │
│ Completion  │    │ Document Sync   │    │ Manager      │
│ Hover       │    │ Lifecycle      │    │              │
│ Definition  │    │                 │    │              │
│ References  │    └─────────────────┘    └──────┬───────┘
│ Code Action  │                                 │
│ Document    │                          ┌──────────────┴─────────────┐
│ Formatting  │                          │   Parser &   │              │
│ Workspace   │                          │  Symbol     │    ┌─────────┤
└─────────────┘                          │   Table     │    │ Analyzer │
                                         └──────────────┘    └─────────┘
```

### Components

#### 1. LSP Server Core (`src/server.py`)
- Entry point for LSP server
- Initialization of pygls server
- Registration of LSP handlers
- Configuration management

#### 2. Protocol Layer (`src/protocol/`)

##### Document Sync (`document_sync.py`)
- `didOpen` - File opened event
- `didClose` - File closed event
- `didChange` - Content changed event
- `didSave` - File saved event
- Document caching for efficient access

##### Lifecycle (`lifecycle.py`)
- `initialize` - Server initialization
- `initialized` - Client ready
- `shutdown` - Server shutdown
- `exit` - Server exit

#### 3. Handlers Layer (`src/handlers/`)

##### Base Handler (`base.py`)
- Abstract base class for all LSP handlers
- Common utility methods
- Logging integration

##### Completion Handler (`completion.py`)
- Code completion suggestions
- Relevance ranking algorithm
- Built-in MATLAB functions
- Keyword completions

##### Hover Handler (`hover.py`)
- Documentation on hover
- Symbol information display
- Markdown formatting
- Position-based lookup

##### Definition Handler (`definition.py`)
- Go-to-definition navigation
- Cross-file symbol search
- Location generation
- Multiple definition support

##### References Handler (`references.py`)
- Find-all-references
- Cross-file reference search
- includeDeclaration parameter
- Location list generation

##### Code Action Handler (`code_action.py`)
- Quick fix suggestions
- Diagnostic analysis
- Fix generation
- Edit application

##### Document Symbol Handler (`document_symbol.py`)
- Document structure outline
- Hierarchical symbol tree
- Symbol kind mapping
- Nested function support

##### Workspace Symbol Handler (`workspace_symbol.py`)
- Project-wide symbol search
- Fuzzy matching
- Kind filtering
- Symbol information generation

##### Formatting Handler (`formatting.py`)
- Automatic code formatting
- Indentation management
- End keyword alignment
- Configurable style

##### Diagnostics Handler (`diagnostics.py`)
- Diagnostic publishing
- Mlint integration
- Severity mapping
- Error display

#### 4. Parser Layer (`src/parser/`)

##### MATLAB Parser (`matlab_parser.py`)
- Regex-based MATLAB syntax parser
- Function extraction
- Variable extraction
- Comment extraction
- Class parsing
- Nested structure support

##### Models (`models.py`)
- Data classes for parse results
- `ParseResult` - Complete parse information
- `FunctionInfo` - Function details
- `ClassInfo` - Class details
- `CommentInfo` - Comment details

#### 5. Symbol Table (`src/utils/symbol_table.py`)

##### Symbol Storage
- In-memory symbol indexing
- Multi-key indexing (name, URI, scope)
- Fast lookup operations
- Global instance for all handlers

##### Symbol Types
- Functions (nested and standalone)
- Variables (global and persistent)
- Classes (MATLAB classes)
- Properties (class properties)
- Methods (class methods)

#### 6. Cache Manager (`src/utils/cache.py`)

##### Caching Strategy
- In-memory LRU cache
- TTL (Time-To-Live) expiration
- Content-based invalidation
- Statistics tracking

##### Cache Types
- Parse result cache
- Mlint analysis cache
- Symbol lookup cache

#### 7. Analyzer Layer (`src/analyzer/`)

##### Base Analyzer (`base_analyzer.py`)
- Abstract analyzer interface
- Result model
- Diagnostic format

##### Mlint Analyzer (`mlint_analyzer.py`)
- MATLAB mlint integration
- Output parsing
- Diagnostic mapping
- Async execution support

#### 8. Features Manager (`src/features/feature_manager.py`)

##### Capability Management
- LSP server capabilities
- Feature enable/disable
- Configuration options
- Provider registration

#### 9. Utilities (`src/utils/`)

##### Logging (`logging.py`)
- Configurable logging levels
- Structured logging
- Request tracing
- Performance logging

##### Performance (`performance.py`)
- LRU cache implementation
- Debouncing utilities
- Time measurement decorator
- Optimization helpers

##### Configuration (`config.py`)
- Server settings
- Environment variables
- Default values
- Validation

##### Document Store (`document_store.py`)
- Document content caching
- Version tracking
- Efficient lookup

## Data Flow

### 1. File Open Flow

```
LSP Client → didOpen → Document Sync → Document Store
              ↓
         Parser → Symbol Table → Handlers
```

### 2. Completion Flow

```
LSP Client → completion → Completion Handler → Symbol Table
              ↓                      ↓
         Symbol Table → Ranking → LSP Client
```

### 3. Go-to-Definition Flow

```
LSP Client → definition → Definition Handler → Symbol Table
              ↓                           ↓
         Position Lookup → Location → LSP Client
```

### 4. Diagnostics Flow

```
File Change → didChange → Document Sync → Analyzer
                                      ↓
                                 Mlint → Diagnostics Handler → LSP Client
```

## Design Decisions

### 1. Regex-Based Parser
**Decision**: Use regex for MATLAB parsing
**Rationale**:
- Faster than full AST for large files
- Simpler implementation
- Easier to extend for new syntax

**Trade-offs**:
- Less precise than AST
- More complex nested structures
- Harder to validate syntax

### 2. In-Memory Symbol Table
**Decision**: Store symbols in memory
**Rationale**:
- Faster lookups (O(1) for direct access)
- No disk I/O latency
- Simpler implementation

**Trade-offs**:
- Symbol table cleared on server restart
- Memory usage grows with project size
- No persistence across sessions

### 3. Event-Driven Architecture
**Decision**: Use pygls event system
**Rationale**:
- Clean separation of concerns
- Easy to add new features
- Standard LSP patterns

**Trade-offs**:
- Requires understanding LSP events
- Event order dependencies
- Debugging event chains

### 4. Cache-First Approach
**Decision**: Cache all expensive operations
**Rationale**:
- Significant performance improvement
- Reduced CPU usage
- Better user experience

**Trade-offs**:
- Cache invalidation complexity
- Stale data risk
- Memory overhead

### 5. Handler-First Design
**Decision**: Implement each LSP feature as separate handler
**Rationale**:
- Clear module boundaries
- Independent testing
- Easy to enable/disable features

**Trade-offs**:
- More files in project
- Boilerplate code
- Handler initialization overhead

## Performance Considerations

### 1. Parser Performance
- **Issue**: Regex parsing can be slow for large files
- **Solution**: Incremental parsing, result caching
- **Metric**: <100ms for 1000 line file

### 2. Symbol Table Performance
- **Issue**: Linear search in symbol table
- **Solution**: LRU cache for common lookups
- **Metric**: <1ms for symbol lookup

### 3. Handler Performance
- **Issue**: Blocking handler calls
- **Solution**: Async execution for I/O operations
- **Metric**: <50ms for completion

### 4. Cache Performance
- **Issue**: Cache memory growth
- **Solution**: LRU eviction, TTL expiration
- **Metric**: Max 100MB cache size

## Scalability

### Current Limitations
1. **File Size**: Optimal for files <10,000 lines
2. **Symbol Count**: Optimal for <50,000 symbols
3. **Project Size**: Tested with ~500 files
4. **Concurrent Users**: Single user per server instance

### Future Improvements
1. **Incremental Parsing**: Parse only changed lines
2. **Persistent Cache**: Cache to disk for restart
3. **Index Database**: SQLite for large symbol tables
4. **Async I/O**: Non-blocking file operations
5. **Multi-User**: Support for concurrent users

## Testing Strategy

### Unit Tests
- Test each component independently
- Mock external dependencies
- Focus on edge cases
- Coverage target: >80%

### Integration Tests
- Test handler chains
- Real file scenarios
- LSP protocol compliance
- Coverage target: >70%

### Performance Tests
- Measure handler latency
- Profile bottlenecks
- Memory usage monitoring
- Benchmark large files

## Security Considerations

### 1. Input Validation
- Validate file paths
- Sanitize user input
- Prevent path traversal

### 2. Resource Limits
- Max file size: 10MB
- Max symbol count: 100,000
- Max cache entries: 10,000

### 3. Error Handling
- Graceful degradation
- No uncaught exceptions
- Proper logging

## Dependencies

### Core Dependencies
- `pygls` - LSP framework
- `lsprotocol` - LSP types
- `python` - 3.10+

### Development Dependencies
- `pytest` - Testing
- `pytest-cov` - Coverage
- `black` - Formatting
- `flake8` - Linting
- `isort` - Import sorting

### External Tools
- `mlint` - MATLAB linting (optional)
- `python` - Execution environment

## Future Architecture

### Phase 5: Advanced Features (Planned)
- Signature Help - function parameter hints
- Rename - symbol refactoring
- Code Lens - in-line references
- Semantic Tokens - enhanced highlighting
- Folding - code structure folding

### Phase 6: Production Readiness (Planned)
- PyPI package
- Multi-platform testing
- Documentation site
- CI/CD pipeline
- Version management

## Maintenance

### Adding New Features

1. Create handler in `src/handlers/`
2. Register in `FeatureManager`
3. Add tests in `tests/unit/`
4. Update `README.md`
5. Update `CHANGELOG.md`

### Debugging

1. Enable DEBUG logging
2. Check symbol table contents
3. Verify parse results
4. Profile performance
5. Test with real .m files

### Version Compatibility

- LSP: 3.17
- MATLAB: R2020b+ (partial)
- Python: 3.10+

## Conclusion

LSP MATLAB Server uses a layered, event-driven architecture optimized for performance and maintainability. The design follows LSP best practices while providing MATLAB-specific optimizations for code intelligence.
