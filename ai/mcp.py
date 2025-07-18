from langchain_mcp_adapters.client import MultiServerMCPClient
from config.logger import logger as log

mcp_server = {
    "fetch": {
        "transport": "sse",
        "url": "https://mcp.api-inference.modelscope.net/a30b4276b9cc40/sse",
        "headers": {},
    },
    "amap-maps": {
        "transport": "sse",
        "url": "https://mcp.api-inference.modelscope.net/521a918ab5864b/sse",
        "headers": {},
    }
}

tool_list = []

    # "amap": {
    #     "transport": "sse",
    #     "url": "https://api.qnaigc.com/v1/mcp/sse/0ff8223a9cd74d10a1c6c4508a1378ee",
    #     "headers": {},
    # },
    # "bing": {
    #     "transport": "sse",
    #     "url": "https://api.qnaigc.com/v1/mcp/sse/19c19e3622eb45b9a482c44d2e761402",
    #     "headers": {},
    # }

# 异步获取 MCP 工具并合并到现有工具列表
async def get_all_tools():
    # MCP 工具
    try:
        client = MultiServerMCPClient(mcp_server)
        mcp_tools = await client.get_tools() 
        tool_list.extend(mcp_tools)
        log.info(f"MCP 工具获取成功，数量: {len(tool_list)}")
        return tool_list
    except Exception as e:
        log.info(f"MCP 工具获取失败，使用本地工具: {e}")
        return tool_list