#!/usr/bin/env python3
"""
Polymarket Trading MCP Server

This server provides tools for interacting with Polymarket events and managing trading accounts.
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional, Union

# MCP server imports
try:
    from mcp.server.fastmcp import FastMCP
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolRequest,
        CallToolResult,
        ListToolsRequest,
        ListToolsResult,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
except ImportError:
    print("MCP library not found. Please install: pip install mcp")
    sys.exit(1)

# Import our existing modules
from api.getEvent import PolymarketAPI, Event, Market, Tag, to_llm_friendly_format

# Global instances
api = PolymarketAPI()

# 创建FastMCP服务器实例，使用标准名称"server"
server = FastMCP(name="polymarket-trading-server")

@server.tool("get_events")
async def get_events(active_only: bool = True, limit: int = 10, offset: int = 0) -> str:
    """获取Polymarket事件列表
    
    Args:
        active_only: 是否只返回活跃事件
        limit: 每页返回的事件数量
        offset: 偏移量，用于分页
    """
    try:
        events = api.get_events(active_only=active_only, limit=limit, offset=offset)
        return to_llm_friendly_format(events)
    except Exception as e:
        return f"获取事件时发生错误: {str(e)}"

@server.tool("get_markets")
async def get_markets(active_only: bool = True, limit: int = 10, offset: int = 0) -> str:
    """获取Polymarket市场列表
    
    Args:
        active_only: 是否只返回活跃市场
        limit: 每页返回的市场数量
        offset: 偏移量，用于分页
    """
    try:
        markets = api.get_markets(active_only=active_only, limit=limit, offset=offset)
        return to_llm_friendly_format(markets)
    except Exception as e:
        return f"获取市场时发生错误: {str(e)}"

@server.tool("get_event_by_id")
async def get_event_by_id(event_id: str) -> str:
    """通过ID获取特定事件详情
    
    Args:
        event_id: 事件ID
    """
    try:
        event = api.get_event_by_id(event_id)
        return to_llm_friendly_format(event)
    except Exception as e:
        return f"获取事件详情时发生错误: {str(e)}"

@server.tool("get_market_by_id")
async def get_market_by_id(market_id: str) -> str:
    """通过ID获取特定市场详情
    
    Args:
        market_id: 市场ID
    """
    try:
        market = api.get_market_by_id(market_id)
        return to_llm_friendly_format(market)
    except Exception as e:
        return f"获取市场详情时发生错误: {str(e)}"

async def main():
    """Main entry point"""
    # 使用stdio运行FastMCP服务器
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main()) 