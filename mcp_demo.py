#!/usr/bin/env python3
"""
真正的MCP客户端调用示例
演示如何通过MCP协议调用ebook-mcp服务，而不是直接使用其代码
"""

import asyncio
import json
import logging
import os
from contextlib import AsyncExitStack
from typing import Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EbookMCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        
    async def connect_to_server(self, server_script_path: str):
        """连接到MCP服务器"""
        logger.info(f"正在连接到MCP服务器: {server_script_path}")
        
        # 配置服务器参数
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )
        
        # 建立连接
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        
        # 初始化会话
        await self.session.initialize()
        logger.info("MCP服务器连接成功")
        
        # 列出可用工具
        tools_response = await self.session.list_tools()
        logger.info(f"可用工具: {[tool.name for tool in tools_response.tools]}")
        return tools_response.tools
    
    async def call_tool(self, tool_name: str, arguments: dict):
        """调用MCP工具"""
        logger.info(f"调用工具: {tool_name}, 参数: {arguments}")
        
        try:
            result = await self.session.call_tool(tool_name, arguments)
            logger.info(f"工具调用成功")
            return result
        except Exception as e:
            logger.error(f"工具调用失败: {e}")
            raise
    
    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()

async def demo_ebook_mcp():
    """演示ebook-mcp的MCP调用"""
    client = EbookMCPClient()
    
    try:
        # 连接到ebook-mcp服务器
        tools = await client.connect_to_server("src/ebook_mcp/main.py")
        
        print("=" * 60)
        print("🚀 ebook-mcp MCP服务调用演示")
        print("=" * 60)
        
        # 显示可用工具
        print("\n📋 可用的MCP工具:")
        for tool in tools:
            print(f"  • {tool.name}: {tool.description}")
        
        print("\n" + "=" * 60)
        print("📚 演示1: 获取所有EPUB文件")
        print("=" * 60)
        
        # 调用get_all_epub_files工具，使用当前目录
        current_dir = os.getcwd()
        print(f"搜索目录: {current_dir}")
        result1 = await client.call_tool("get_all_epub_files", {"path": current_dir})
        # 处理MCP返回的内容
        if result1.content and len(result1.content) > 0:
            epub_files_text = result1.content[0].text
            print(f"结果: {epub_files_text}")
            epub_files = json.loads(epub_files_text)
        else:
            epub_files = []
            print("未找到EPUB文件")
        
        print("\n" + "=" * 60)
        print("📖 演示2: 获取EPUB目录")
        print("=" * 60)
        if epub_files:
            epub_path = epub_files[0]
            print(f"选择的EPUB文件: {epub_path}")
            
            # 调用get_toc工具
            result2 = await client.call_tool("get_toc", {"epub_path": epub_path})
            if result2.content and len(result2.content) > 0:
                toc_text = result2.content[0].text
                print(f"目录结构: {toc_text}")
            else:
                print("无法获取目录结构")
        
        print("\n" + "=" * 60)
        print("📄 演示3: 获取EPUB元数据")
        print("=" * 60)
        
        if epub_files:
            # 调用get_meta工具
            result3 = await client.call_tool("get_meta", {"epub_path": epub_path})
            if result3.content and len(result3.content) > 0:
                meta_text = result3.content[0].text
                print(f"元数据: {meta_text}")
            else:
                print("无法获取元数据")
        
        print("\n" + "=" * 60)
        print("✅ MCP调用演示完成!")
        print("=" * 60)
        
        print("\n🔍 对比说明:")
        print("• 这是真正的MCP协议调用，通过stdio与服务器通信")
        print("• 服务器运行在独立进程中，提供标准化的MCP接口")
        print("• 客户端通过工具调用获取数据，而不是直接导入Python模块")
        print("• 这种方式支持跨语言调用，更符合MCP设计理念")
        
    except Exception as e:
        logger.error(f"演示过程中出错: {e}")
        print(f"❌ 错误: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(demo_ebook_mcp())