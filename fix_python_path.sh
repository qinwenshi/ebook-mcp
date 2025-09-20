#!/bin/bash

# Python路径修复脚本
# 自动检测系统Python路径并更新Claude Desktop配置

set -e

echo "🔧 Python路径修复脚本"
echo "===================="

# 配置文件路径
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
PROJECT_DIR="/Users/xudongqi/projects/ebook-mcp"

echo "🔍 检测Python路径..."

# 检测可用的Python路径
PYTHON_PATHS=(
    "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3"
    "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3"
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
    "/usr/bin/python3"
    "/opt/homebrew/bin/python3"
    "/usr/local/bin/python3"
)

FOUND_PYTHON=""

for python_path in "${PYTHON_PATHS[@]}"; do
    if [ -x "$python_path" ]; then
        echo "✅ 找到Python: $python_path"
        FOUND_PYTHON="$python_path"
        break
    fi
done

if [ -z "$FOUND_PYTHON" ]; then
    echo "❌ 未找到可用的Python解释器"
    echo "请确保Python已正确安装"
    exit 1
fi

echo "🎯 使用Python路径: $FOUND_PYTHON"

# 测试Python是否可以运行
echo "🧪 测试Python..."
if ! "$FOUND_PYTHON" --version > /dev/null 2>&1; then
    echo "❌ Python无法正常运行: $FOUND_PYTHON"
    exit 1
fi

PYTHON_VERSION=$("$FOUND_PYTHON" --version)
echo "✅ Python版本: $PYTHON_VERSION"

# 检查Claude Desktop配置目录
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo "❌ Claude Desktop配置目录不存在: $CLAUDE_CONFIG_DIR"
    echo "请先安装并运行Claude Desktop应用程序"
    exit 1
fi

# 备份现有配置
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "📋 备份现有配置..."
    cp "$CLAUDE_CONFIG_FILE" "$CLAUDE_CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 创建修正后的配置
echo "📝 创建修正后的配置..."

python3 << EOF
import json
import os

config_file = "$CLAUDE_CONFIG_FILE"
project_dir = "$PROJECT_DIR"
python_path = "$FOUND_PYTHON"

# 读取现有配置或创建新配置
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

# 确保mcpServers存在
if 'mcpServers' not in config:
    config['mcpServers'] = {}

# 更新ebook-mcp配置
config['mcpServers']['ebook-mcp'] = {
    "command": python_path,
    "args": [f"{project_dir}/src/ebook_mcp/main.py"],
    "env": {
        "PYTHONPATH": project_dir
    }
}

# 写回配置文件
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ 配置已更新")
EOF

echo ""
echo "🎉 Python路径修复完成！"
echo ""
echo "📋 配置详情:"
echo "Python路径: $FOUND_PYTHON"
echo "项目路径: $PROJECT_DIR"
echo "配置文件: $CLAUDE_CONFIG_FILE"
echo ""
echo "🔄 下一步:"
echo "1. 重启Claude Desktop应用程序"
echo "2. 测试MCP功能是否正常"
echo ""
echo "🧪 测试命令:"
echo "cd $PROJECT_DIR"
echo "source venv/bin/activate"
echo "python mcp_demo.py"