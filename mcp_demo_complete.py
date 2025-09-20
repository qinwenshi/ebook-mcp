#!/usr/bin/env python3
"""
完整的MCP客户端调用演示
演示如何通过MCP协议调用ebook-mcp服务的所有功能
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

async def demo_mcp_vs_direct():
    """演示MCP调用与直接代码调用的对比"""
    client = EbookMCPClient()
    
    try:
        # 连接到ebook-mcp服务器
        tools = await client.connect_to_server("src/ebook_mcp/main.py")
        
        print("=" * 80)
        print("🚀 ebook-mcp MCP服务调用完整演示")
        print("=" * 80)
        
        # 显示可用工具
        print("\n📋 可用的MCP工具:")
        epub_tools = []
        pdf_tools = []
        
        for tool in tools:
            if 'epub' in tool.name.lower():
                epub_tools.append(tool)
            elif 'pdf' in tool.name.lower():
                pdf_tools.append(tool)
        
        print("\n📚 EPUB相关工具:")
        for tool in epub_tools:
            print(f"  • {tool.name}: {tool.description}")
        
        print("\n📄 PDF相关工具:")
        for tool in pdf_tools:
            print(f"  • {tool.name}: {tool.description}")
        
        print("\n" + "=" * 80)
        print("🔍 MCP调用 vs 直接代码调用对比")
        print("=" * 80)
        
        # 演示1: MCP调用获取EPUB文件
        print("\n📚 演示1: 通过MCP获取EPUB文件")
        print("-" * 50)
        
        # 使用Downloads目录作为示例
        downloads_dir = os.path.expanduser("~/Downloads")
        print(f"搜索目录: {downloads_dir}")
        
        try:
            result1 = await client.call_tool("get_all_epub_files", {"path": downloads_dir})
            if result1.content and len(result1.content) > 0:
                epub_files_text = result1.content[0].text
                print(f"MCP调用结果: {epub_files_text}")
                epub_files = json.loads(epub_files_text)
                print(f"找到 {len(epub_files)} 个EPUB文件")
            else:
                print("MCP调用: 未找到EPUB文件")
        except Exception as e:
            print(f"MCP调用出错: {e}")
        
        # 对比：直接代码调用
        print("\n对比 - 直接代码调用:")
        try:
            # 这里我们模拟直接调用
            from src.ebook_mcp.tools.epub_helper import get_all_epub_files
            direct_result = get_all_epub_files(downloads_dir)
            print(f"直接调用结果: {direct_result}")
            print(f"找到 {len(direct_result)} 个EPUB文件")
        except Exception as e:
            print(f"直接调用出错: {e}")
        
        print("\n" + "=" * 80)
        print("📊 MCP vs 直接调用的优缺点对比")
        print("=" * 80)
        
        comparison_table = """
┌─────────────────┬─────────────────────────┬─────────────────────────┐
│     特性        │       MCP调用           │      直接代码调用       │
├─────────────────┼─────────────────────────┼─────────────────────────┤
│ 标准化程度      │ ✅ 高度标准化           │ ❌ 依赖具体实现         │
│ 跨语言支持      │ ✅ 支持多种语言         │ ❌ 仅限Python           │
│ 进程隔离        │ ✅ 独立进程，安全       │ ❌ 同进程，可能冲突     │
│ 错误处理        │ ✅ 统一错误格式         │ ❌ 各种异常类型         │
│ 调用开销        │ ❌ 有进程间通信开销     │ ✅ 直接函数调用         │
│ 调试便利性      │ ❌ 需要额外调试工具     │ ✅ 直接调试             │
│ 部署复杂度      │ ❌ 需要配置MCP服务      │ ✅ 直接导入使用         │
│ 版本管理        │ ✅ 服务端统一管理       │ ❌ 客户端依赖管理       │
│ 功能扩展        │ ✅ 服务端升级即可       │ ❌ 需要更新客户端       │
│ 资源管理        │ ✅ 服务端统一管理       │ ❌ 客户端各自管理       │
└─────────────────┴─────────────────────────┴─────────────────────────┘
        """
        print(comparison_table)
        
        print("\n🎯 使用建议:")
        print("• 生产环境、多语言项目 → 推荐MCP调用")
        print("• 快速原型、单一语言项目 → 可考虑直接调用")
        print("• 需要高度标准化的API → 推荐MCP调用")
        print("• 性能敏感的场景 → 可考虑直接调用")
        
        print("\n" + "=" * 80)
        print("✅ 完整演示结束!")
        print("=" * 80)
        
    except Exception as e:
        logger.error(f"演示过程中出错: {e}")
        print(f"❌ 错误: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(demo_mcp_vs_direct())