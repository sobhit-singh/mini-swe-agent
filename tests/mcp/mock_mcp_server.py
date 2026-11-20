from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

server = MCPServer("mock")


@server.tool()
def echo(message: str) -> str:
    """Echo the message back"""
    return f"echo: {message}"


@server.tool()
def fail(reason: str) -> str:
    """Intentionally raise error"""
    raise ToolError(f"failed: {reason}")


if __name__ == "__main__":
    server.run("stdio")
