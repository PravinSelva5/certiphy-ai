"""Smoke tests for the MCP server module."""

import governance_mcp.server as server_module


def test_server_module_imports() -> None:
    """Server module should import without error."""
    assert server_module.mcp is not None
