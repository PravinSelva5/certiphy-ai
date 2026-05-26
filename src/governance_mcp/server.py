"""MCP server entry point and tool registration."""

from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("certiphy-ai")


@mcp.tool()
async def evaluate_compliance() -> dict[str, Any]:
    """Placeholder tool for EU AI Act compliance evaluation."""
    return {"status": "not_implemented"}


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
