#!/usr/bin/env python3
"""
测试MCP连接的脚本
用于验证ebook-mcp服务器是否能正常工作
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

async def test_mcp_server():
    """测试MCP服务器连接"""
    print("🧪 测试MCP服务器连接...")
    
    # 1. 测试服务器启动
    print("\n1️⃣ 测试服务器启动...")
    try:
        # 启动服务器进程
        process = subprocess.Popen(
            [sys.executable, "src/ebook_mcp/main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent
        )
        
        # 发送初始化消息
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # 发送消息
        message_str = json.dumps(init_message) + "\n"
        process.stdin.write(message_str)
        process.stdin.flush()
        
        # 等待响应
        time.sleep(2)
        
        # 检查进程状态
        if process.poll() is None:
            print("✅ 服务器启动成功")
            
            # 发送工具列表请求
            tools_message = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            tools_str = json.dumps(tools_message) + "\n"
            process.stdin.write(tools_str)
            process.stdin.flush()
            
            time.sleep(1)
            
            # 终止进程
            process.terminate()
            process.wait()
            
            print("✅ MCP服务器测试完成")
            return True
        else:
            print("❌ 服务器启动失败")
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"错误信息: {stderr_output}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def check_python_environment():
    """检查Python环境"""
    print("🔍 检查Python环境...")
    
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    # 检查关键依赖
    required_packages = [
        ('fastmcp', 'fastmcp'),
        ('ebooklib', 'ebooklib'), 
        ('PyPDF2', 'PyPDF2'),
        ('pydantic', 'pydantic'),
        ('beautifulsoup4', 'bs4')
    ]
    
    missing_packages = []
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} - 缺失")
            missing_packages.append(display_name)
    
    if missing_packages:
        print(f"\n⚠️  缺失的包: {', '.join(missing_packages)}")
        print("请运行: pip install -e .")
        return False
    
    print("✅ 所有依赖包都已安装")
    return True

def check_file_structure():
    """检查文件结构"""
    print("\n📁 检查文件结构...")
    
    required_files = [
        "src/ebook_mcp/main.py",
        "src/ebook_mcp/__init__.py",
        "src/ebook_mcp/tools/epub_helper.py",
        "src/ebook_mcp/tools/pdf_helper.py",
        "pyproject.toml"
    ]
    
    project_root = Path(__file__).parent
    missing_files = []
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 缺失")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  缺失的文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有必需文件都存在")
    return True

def generate_config_suggestions():
    """生成配置建议"""
    print("\n📋 Claude Desktop配置建议...")
    
    python_path = sys.executable
    project_path = str(Path(__file__).parent.absolute())
    main_py_path = f"{project_path}/src/ebook_mcp/main.py"
    
    configs = {
        "最简配置": {
            "mcpServers": {
                "ebook-mcp": {
                    "command": python_path,
                    "args": [main_py_path]
                }
            }
        },
        "完整配置": {
            "mcpServers": {
                "ebook-mcp": {
                    "command": python_path,
                    "args": [main_py_path],
                    "env": {
                        "PYTHONPATH": project_path
                    }
                }
            }
        }
    }
    
    for name, config in configs.items():
        print(f"\n{name}:")
        print(json.dumps(config, indent=2, ensure_ascii=False))

async def main():
    """主函数"""
    print("🔧 ebook-mcp 连接诊断工具")
    print("=" * 50)
    
    # 检查环境
    env_ok = check_python_environment()
    files_ok = check_file_structure()
    
    if not (env_ok and files_ok):
        print("\n❌ 环境检查失败，请先修复上述问题")
        return
    
    # 测试MCP服务器
    server_ok = await test_mcp_server()
    
    if server_ok:
        print("\n🎉 所有测试通过！")
        print("\n📝 下一步:")
        print("1. 将配置复制到Claude Desktop配置文件")
        print("2. 重启Claude Desktop")
        print("3. 测试工具功能")
    else:
        print("\n❌ MCP服务器测试失败")
        print("请检查错误信息并修复问题")
    
    # 生成配置建议
    generate_config_suggestions()

if __name__ == "__main__":
    asyncio.run(main())