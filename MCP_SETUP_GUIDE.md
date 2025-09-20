# Claude Desktop MCP 配置指南

## 📋 配置步骤

### 1. 复制配置文件

将以下配置内容复制到你的Claude Desktop配置文件中：

**配置文件路径：**
```
/Users/xudongqi/Library/Application Support/Claude/claude_desktop_config.json
```

**配置内容：**
```json
{
  "mcpServers": {
    "ebook-mcp": {
      "command": "python",
      "args": ["/Users/xudongqi/projects/ebook-mcp/src/ebook_mcp/main.py"],
      "env": {
        "PYTHONPATH": "/Users/xudongqi/projects/ebook-mcp"
      }
    }
  }
}
```

### 2. 确保环境准备

在配置之前，请确保：

1. **Python环境已激活**：
   ```bash
   cd /Users/xudongqi/projects/ebook-mcp
   source venv/bin/activate
   ```

2. **依赖已安装**：
   ```bash
   pip install -e .
   ```

3. **测试MCP服务器**：
   ```bash
   python src/ebook_mcp/main.py
   ```

### 3. 重启Claude Desktop

配置完成后，重启Claude Desktop应用程序以加载新的MCP服务器。

## 🔧 配置说明

### 基本配置项

- **`command`**: 执行命令，这里是`python`
- **`args`**: 传递给命令的参数，指向MCP服务器脚本
- **`env`**: 环境变量，设置PYTHONPATH确保模块可以正确导入

### 高级配置选项

如果需要更多配置，可以使用以下完整配置：

```json
{
  "mcpServers": {
    "ebook-mcp": {
      "command": "python",
      "args": ["/Users/xudongqi/projects/ebook-mcp/src/ebook_mcp/main.py"],
      "env": {
        "PYTHONPATH": "/Users/xudongqi/projects/ebook-mcp",
        "LOG_LEVEL": "INFO"
      }
    }
  },
  "globalShortcuts": [],
  "updater": {
    "checkForUpdates": true
  }
}
```

## 🚀 使用方法

配置成功后，在Claude Desktop中你可以：

### EPUB文件操作
- 获取目录结构：`请帮我获取这个EPUB文件的目录`
- 提取章节内容：`请提取第3章的内容`
- 获取元数据：`这本书的作者和出版信息是什么？`

### PDF文件操作
- 获取目录：`请显示这个PDF的目录结构`
- 提取页面内容：`请提取第10页的内容`
- 章节提取：`请提取"第一章"的完整内容`

## 🔍 可用工具

配置成功后，以下工具将在Claude Desktop中可用：

### EPUB工具
- `get_all_epub_files`: 获取指定目录下的所有EPUB文件
- `get_toc`: 获取EPUB文件的目录结构
- `get_meta`: 获取EPUB文件的元数据
- `extract_chapter_from_epub`: 提取EPUB文件的特定章节

### PDF工具
- `get_all_pdf_files`: 获取指定目录下的所有PDF文件
- `get_pdf_toc`: 获取PDF文件的目录结构
- `get_pdf_page_text`: 获取PDF特定页面的文本
- `get_pdf_page_markdown`: 获取PDF特定页面的Markdown格式内容
- `get_pdf_chapter_content`: 根据章节标题提取PDF内容

## ❗ 故障排除

### 常见问题

1. **MCP服务器无法启动**
   - 检查Python路径是否正确
   - 确认虚拟环境已激活
   - 验证依赖是否已安装

2. **工具调用失败**
   - 检查文件路径是否存在
   - 确认文件格式是否支持
   - 查看Claude Desktop的错误日志

3. **配置不生效**
   - 确认JSON格式正确
   - 重启Claude Desktop
   - 检查配置文件路径

### 测试配置

可以使用以下命令测试MCP服务器是否正常工作：

```bash
cd /Users/xudongqi/projects/ebook-mcp
source venv/bin/activate
python mcp_demo.py
```

## 📚 更多资源

- [MCP官方文档](https://modelcontextprotocol.io/)
- [Claude Desktop文档](https://claude.ai/desktop)
- [ebook-mcp项目README](./README.md)