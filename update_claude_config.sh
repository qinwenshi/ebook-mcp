#!/bin/bash

# 更新Claude Desktop配置脚本
# 使用正确的虚拟环境Python路径

set -e

echo "🔧 更新Claude Desktop配置"
echo "=========================="

# 配置文件路径
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
PROJECT_DIR="/Users/xudongqi/projects/ebook-mcp"

# 使用虚拟环境中的Python
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"

echo "🔍 检查虚拟环境Python..."
if [ ! -x "$VENV_PYTHON" ]; then
    echo "❌ 虚拟环境Python不存在: $VENV_PYTHON"
    echo "请先创建并激活虚拟环境"
    exit 1
fi

echo "✅ 找到虚拟环境Python: $VENV_PYTHON"

# 测试Python版本
PYTHON_VERSION=$("$VENV_PYTHON" --version)
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

# 创建新配置
echo "📝 创建新配置..."

cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "ebook-mcp": {
      "command": "$VENV_PYTHON",
      "args": [
        "$PROJECT_DIR/src/ebook_mcp/main.py"
      ],
      "env": {
        "PYTHONPATH": "$PROJECT_DIR"
      }
    }
  }
}
EOF

echo "✅ 配置已更新"

# 验证配置文件
echo "🧪 验证配置文件..."
if python3 -m json.tool "$CLAUDE_CONFIG_FILE" > /dev/null 2>&1; then
    echo "✅ 配置文件格式正确"
else
    echo "❌ 配置文件格式错误"
    exit 1
fi

echo ""
echo "🎉 配置更新完成！"
echo ""
echo "📋 配置详情:"
echo "Python路径: $VENV_PYTHON"
echo "项目路径: $PROJECT_DIR"
echo "配置文件: $CLAUDE_CONFIG_FILE"
echo ""
echo "🔄 下一步:"
echo "1. 重启Claude Desktop应用程序"
echo "2. 检查MCP服务器连接状态"
echo "3. 测试ebook-mcp工具功能"
echo ""
echo "📄 当前配置内容:"
cat "$CLAUDE_CONFIG_FILE"