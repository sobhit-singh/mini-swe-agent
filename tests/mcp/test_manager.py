import sys
from pathlib import Path

from minisweagent.mcp.config import MCPConfig, MCPServerConfig
from minisweagent.mcp.manager import MCPManager

MOCK_SERVER_SCRIPT = str(Path(__file__).parent / "mock_mcp_server.py")


def test_mcp_manager_lifecycle_and_tools():
    config = MCPConfig(
        servers={
            "test_server": MCPServerConfig(
                command=sys.executable,
                args=[MOCK_SERVER_SCRIPT],
            )
        }
    )
    manager = MCPManager(config)
    manager.start()
    try:
        tools = manager.get_tools()
        assert len(tools) == 2
        tool_names = [t["function"]["name"] for t in tools]
        assert "test_server__echo" in tool_names
        assert "test_server__fail" in tool_names

        # Execute echo
        res = manager.execute({"tool_name": "test_server__echo", "arguments": {"message": "hello world"}})
        assert res["returncode"] == 0
        assert "echo: hello world" in res["output"]

        # Execute fail
        fail_res = manager.execute({"tool_name": "test_server__fail", "arguments": {"reason": "boom"}})
        assert fail_res["returncode"] == 1
        assert "boom" in fail_res["output"] or "boom" in fail_res["exception_info"]
    finally:
        manager.close()
