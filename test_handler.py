"""Test script for BaseHandler."""

from pygls.server import LanguageServer

from src.handlers.base import BaseHandler


class TestHandler(BaseHandler):
    """Test handler implementation."""

    @property
    def method_name(self) -> str:
        return "textDocument/test"

    async def handle(self, *args, **kwargs):
        return {"status": "ok", "message": "Test handler executed"}


def test_base_handler():
    """Test BaseHandler functionality."""
    print("Testing BaseHandler...")

    # Test 1: Create server and handler instances
    print("\n1. Creating handler instances...")
    server = LanguageServer("test-server", "v1.0")
    handler = TestHandler(server)
    print(f"   Handler: {handler}")
    print(f"   Method name: {handler.method_name}")
    assert handler.method_name == "textDocument/test"
    print("   [OK] Handler instance created successfully")

    # Test 2: Check abstract method enforcement
    print("\n2. Testing abstract method enforcement...")
    try:
        # Try to instantiate BaseHandler directly
        base_handler = BaseHandler(server)
        print("   [FAIL] BaseHandler should not be instantiable")
        return False
    except TypeError as e:
        print(f"   [OK] BaseHandler is abstract: {e}")

    # Test 3: Check handle method is async
    print("\n3. Testing handle method is async...")
    import inspect
    assert inspect.iscoroutinefunction(handler.handle)
    print("   [OK] handle method is async")

    # Test 4: Test handle execution
    print("\n4. Testing handle execution...")
    import asyncio
    result = asyncio.run(handler.handle())
    print(f"   Result: {result}")
    assert result["status"] == "ok"
    print("   [OK] Handle method executes correctly")

    print("\n[OK] All BaseHandler tests passed!")
    return True


if __name__ == "__main__":
    test_base_handler()
