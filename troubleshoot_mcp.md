# MCP 服务器连接问题排查指南

## 问题现象
- Claude Desktop 显示 "MCP server disconnected"
- 无法使用 ebook-mcp 工具

## 已执行的修复步骤

### 1. ✅ Python 路径修复
- 检测到系统 Python 路径：`/Library/Frameworks/Python.framework/Versions/3.10/bin/python3`
- 已更新 Claude Desktop 配置文件
- 备份了原配置文件

### 2. ✅ MCP 服务器测试
- 服务器可以正常启动
- 日志显示："Server is starting....."

## 下一步操作

### 立即执行
1. **重启 Claude Desktop 应用程序**
   - 完全退出 Claude Desktop
   - 重新启动应用程序
   - 等待 MCP 服务器重新连接

### 验证连接
2. **检查连接状态**
   - 在 Claude Desktop 中查看是否显示 ebook-mcp 工具
   - 尝试使用任一 EPUB 或 PDF 工具

### 如果仍有问题
3. **进一步诊断**
   ```bash
   # 检查配置文件
   cat "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
   
   # 手动测试服务器
   cd /Users/xudongqi/projects/ebook-mcp
   source venv/bin/activate
   python src/ebook_mcp/main.py
   ```

## 当前配置详情
- **Python 路径**: `/Library/Frameworks/Python.framework/Versions/3.10/bin/python3`
- **项目路径**: `/Users/xudongqi/projects/ebook-mcp`
- **主程序**: `src/ebook_mcp/main.py`
- **环境变量**: `PYTHONPATH=/Users/xudongqi/projects/ebook-mcp`

## 常见问题解决

### 问题 1: Python 版本不匹配
```bash
# 检查 Python 版本
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 --version
```

### 问题 2: 依赖包缺失
```bash
cd /Users/xudongqi/projects/ebook-mcp
source venv/bin/activate
pip install -e .
```

### 问题 3: 权限问题
```bash
# 确保脚本有执行权限
chmod +x src/ebook_mcp/main.py
```

## 成功标志
- Claude Desktop 不再显示断开连接消息
- 可以看到并使用以下工具：
  - `get_all_epub_files`
  - `get_meta`
  - `extract_chapter_from_epub`
  - `get_all_pdf_files`
  - `extract_text_from_pdf`
  - `extract_images_from_pdf`

## 联系支持
如果问题持续存在，请提供：
1. Claude Desktop 版本
2. macOS 版本
3. Python 版本
4. 错误日志（如有）