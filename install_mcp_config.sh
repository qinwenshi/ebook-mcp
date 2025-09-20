#!/bin/bash

# Claude Desktop MCP 配置安装脚本
# 自动将ebook-mcp配置添加到Claude Desktop

set -e

echo "🚀 Claude Desktop MCP 配置安装脚本"
echo "=================================="

# 配置文件路径
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
PROJECT_DIR="/Users/xudongqi/projects/ebook-mcp"

# 检查Claude Desktop配置目录是否存在
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo "❌ Claude Desktop配置目录不存在: $CLAUDE_CONFIG_DIR"
    echo "请先安装并运行Claude Desktop应用程序"
    exit 1
fi

echo "✅ 找到Claude Desktop配置目录"

# 备份现有配置文件
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "📋 备份现有配置文件..."
    cp "$CLAUDE_CONFIG_FILE" "$CLAUDE_CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ 配置文件已备份"
fi

# 创建新的配置内容
echo "📝 创建MCP配置..."

# 检查是否已有配置文件
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    # 读取现有配置并合并
    echo "🔄 合并现有配置..."
    
    # 使用Python脚本来合并JSON配置
    python3 << EOF
import json
import os

config_file = "$CLAUDE_CONFIG_FILE"
project_dir = "$PROJECT_DIR"

# 读取现有配置
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

# 确保mcpServers存在
if 'mcpServers' not in config:
    config['mcpServers'] = {}

# 添加ebook-mcp配置
config['mcpServers']['ebook-mcp'] = {
    "command": "python",
    "args": [f"{project_dir}/src/ebook_mcp/main.py"],
    "env": {
        "PYTHONPATH": project_dir
    }
}

# 写回配置文件
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ MCP配置已添加到Claude Desktop")
EOF

else
    # 创建新的配置文件
    echo "📄 创建新的配置文件..."
    cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "ebook-mcp": {
      "command": "python",
      "args": ["$PROJECT_DIR/src/ebook_mcp/main.py"],
      "env": {
        "PYTHONPATH": "$PROJECT_DIR"
      }
    }
  }
}
EOF
    echo "✅ 新配置文件已创建"
fi

echo ""
echo "🎉 配置安装完成！"
echo ""
echo "📋 下一步操作："
echo "1. 重启Claude Desktop应用程序"
echo "2. 在对话中测试MCP工具是否可用"
echo ""
echo "🔧 测试命令："
echo "cd $PROJECT_DIR"
echo "source venv/bin/activate"
echo "python mcp_demo.py"
echo ""
echo "📚 查看完整指南："
echo "cat $PROJECT_DIR/MCP_SETUP_GUIDE.md"