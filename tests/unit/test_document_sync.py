"""
Unit tests for Document Synchronization.
"""


from src.utils.document_store import Document, DocumentStore


def test_document_creation():
    """Test Document can be created."""
    doc = Document(
        uri="file:///test.m",
        path="C:\\test.m",
        content="function test\nend",
        version=1,
    )

    assert doc.uri == "file:///test.m"
    assert doc.path == "C:\\test.m"
    assert doc.content == "function test\nend"
    assert doc.version == 1


def test_document_store_add():
    """Test DocumentStore can add documents."""
    store = DocumentStore()

    doc = store.add_document(
        uri="file:///test.m",
        path="C:\\test.m",
        content="function test\nend",
    )

    assert store.get_document("file:///test.m") == doc
    assert len(store.get_all_documents()) == 1


def test_document_store_remove():
    """Test DocumentStore can remove documents."""
    store = DocumentStore()

    store.add_document(
        uri="file:///test.m",
        path="C:\\test.m",
        content="test",
    )

    removed = store.remove_document("file:///test.m")
    assert removed is True
    assert store.get_document("file:///test.m") is None
    assert len(store.get_all_documents()) == 0


def test_document_store_get_nonexistent():
    """Test DocumentStore returns None for nonexistent document."""
    store = DocumentStore()

    doc = store.get_document("file:///nonexistent.m")
    assert doc is None


def test_document_store_clear():
    """Test DocumentStore can be cleared."""
    store = DocumentStore()

    store.add_document(
        uri="file:///test1.m",
        path="C:\\test1.m",
        content="test1",
    )
    store.add_document(
        uri="file:///test2.m",
        path="C:\\test2.m",
        content="test2",
    )

    count_before = len(store.get_all_documents())
    store.clear()

    assert len(store.get_all_documents()) == 0
    assert count_before == 2


def test_document_store_update_content():
    """Test DocumentStore can update document content."""
    store = DocumentStore()

    doc = store.add_document(
        uri="file:///test.m",
        path="C:\\test.m",
        content="old content",
    )

    assert doc.version == 0

    # Update content
    updated = store.update_document_content(
        uri="file:///test.m",
        new_content="new content",
    )

    assert updated is not None
    assert updated.version == 1
    assert updated.content == "new content"


def test_document_store_update_nonexistent():
    """Test DocumentStore returns None when updating nonexistent."""
    store = DocumentStore()

    updated = store.update_document_content(
        uri="file:///test.m",
        new_content="new content",
    )

    assert updated is None


def test_document_sync_module_imports():
    """Test that document sync module can be imported."""
    from src.protocol.document_sync import register_document_sync_handlers
    from src.utils.document_store import DocumentStore

    assert register_document_sync_handlers is not None
    assert DocumentStore is not None
