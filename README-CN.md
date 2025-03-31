# Ebook-MCP

[English](https://github.com/onebirdrocks/ebook-mcp/blob/main/README.md) | 中文

<img src="logo.png" alt="ebook-mcp logo" width="132" height="132">


Ebook-MCP 是一个功能强大的电子书处理 Model Context Protocol (MCP) 服务器。基于 [Model Context Protocol](https://github.com/modelcontextprotocol) 构建，它提供了一套标准化的 API，可以无缝集成 LLM 应用程序和电子书处理功能。目前支持 EPUB 和 PDF 格式。

## 使用场景和价值

Ebook-MCP 通过启用与阅读材料的自然语言对话，彻底改变了您与电子书的交互方式。它可以无缝集成到现代 AI 驱动的 IDE（如 Cursor 和 Claude）中，让您能够：

- **智能图书馆管理**：只需简单询问"显示我下载文件夹中的所有 EPUB 文件"或"在我的图书馆中查找关于 GenAI 的书籍"
- **交互式阅读体验**：与您的书籍进行自然对话：
  - "给我简单介绍一下'LLM Engineer Handbook'这本书"
  - "第三章讲了什么内容？"
  - "总结一下这本书中关于 RAG 的要点"
- **主动学习支持**：通过 AI 驱动的交互增强学习效果：
  - "基于第五章中的 RAG 概念创建一个测验"
  - "解释一下本章讨论的各种架构之间的差异"
  - "根据本节的概念给我一些实践练习"
- **内容导航**：使用自然语言查询轻松浏览您的书籍：
  - "查找所有讨论提示工程的章节"
  - "显示关于微调的章节"
  - "带我到讨论向量数据库的部分"

通过架起传统电子书和 AI 功能之间的桥梁，Ebook-MCP 帮助读者通过直观的对话式交互从数字图书馆中获取更多价值。

## 功能特性

### EPUB 支持
- 提取元数据（标题、作者、出版日期等）
- 提取目录
- 提取章节内容（支持 Markdown 输出）
- 批量处理 EPUB 文件

### PDF 支持
- 提取元数据（标题、作者、创建日期等）
- 提取目录
- 按页码提取内容
- 按章节标题提取内容
- 支持 Markdown 输出
- 批量处理 PDF 文件

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/ebook-mcp.git
cd ebook-mcp
```

2. 使用 `uv` 安装依赖：
```bash
uv pip install -r requirements.txt
```

## 使用方法

### 在开发模式下启动 MCP 服务器

运行开发模式服务器：
```bash
uv run mcp dev main.py
```
您可以访问 http://localhost:5173/ 进行测试和调试

### 在生产模式下启动 MCP 服务器

运行生产模式服务器：
```bash
uv run main.py
```

#### 在 Cursor 中配置 MCP

在 Cursor 中添加以下配置：
```bash
"ebook-mcp":{
            "command": "uv",
            "args": [
                "--directory",
                "/Users/onebird/github/ebook-mcp",
                "run",
                "main.py"
            ]
        }
```

### EPUB 处理示例

```python
# 获取目录中的所有 EPUB 文件
epub_files = get_all_epub_files("/path/to/books")

# 获取 EPUB 元数据
metadata = get_metadata("/path/to/book.epub")

# 获取目录
toc = get_toc("/path/to/book.epub")

# 获取特定章节内容（Markdown 格式）
chapter_content = get_chapter_markdown("/path/to/book.epub", "chapter_id")
```

### PDF 处理示例

```python
# 获取目录中的所有 PDF 文件
pdf_files = get_all_pdf_files("/path/to/books")

# 获取 PDF 元数据
metadata = get_pdf_metadata("/path/to/book.pdf")

# 获取目录
toc = get_pdf_toc("/path/to/book.pdf")

# 获取特定页面内容
page_text = get_pdf_page_text("/path/to/book.pdf", 1)
page_markdown = get_pdf_page_markdown("/path/to/book.pdf", 1)

# 获取特定章节内容
chapter_content, page_numbers = get_pdf_chapter_content("/path/to/book.pdf", "Chapter 1")
```

## API 参考

### EPUB APIs

#### `get_all_epub_files(path: str) -> List[str]`
获取指定目录中的所有 EPUB 文件。

#### `get_metadata(epub_path: str) -> Dict[str, Union[str, List[str]]]`
获取 EPUB 文件的元数据。

#### `get_toc(epub_path: str) -> List[Tuple[str, str]]`
获取 EPUB 文件的目录。

#### `get_chapter_markdown(epub_path: str, chapter_id: str) -> str`
获取章节内容的 Markdown 格式。

### PDF APIs

#### `get_all_pdf_files(path: str) -> List[str]`
获取指定目录中的所有 PDF 文件。

#### `get_pdf_metadata(pdf_path: str) -> Dict[str, Union[str, List[str]]]`
获取 PDF 文件的元数据。

#### `get_pdf_toc(pdf_path: str) -> List[Tuple[str, int]]`
获取 PDF 文件的目录。

#### `get_pdf_page_text(pdf_path: str, page_number: int) -> str`
获取特定页面的纯文本内容。

#### `get_pdf_page_markdown(pdf_path: str, page_number: int) -> str`
获取特定页面的 Markdown 格式内容。

#### `get_pdf_chapter_content(pdf_path: str, chapter_title: str) -> Tuple[str, List[int]]`
通过章节标题获取章节内容和对应的页码。

## 依赖项

主要依赖包括：
- ebooklib：EPUB 文件处理
- PyPDF2：基础 PDF 处理
- PyMuPDF：高级 PDF 处理
- beautifulsoup4：HTML 解析
- html2text：HTML 转 Markdown
- pydantic：数据验证
- fastmcp：MCP 服务器框架

## 重要说明

1. PDF 处理依赖于文档的目录。如果目录不可用，某些功能可能无法工作。
2. 对于大型 PDF 文件，建议按页面范围处理，避免一次性加载整个文件。
3. EPUB 章节 ID 必须从目录结构中获取。

## 架构

```
           ┌────────────────────────────┐
           │         代理层             │
           │  - 翻译策略               │
           │  - 风格一致性检查         │
           │  - LLM 调用与交互         │
           └────────────▲─────────────┘
                        │ 工具调用
           ┌────────────┴─────────────┐
           │        MCP 工具层        │
           │  - 提取章节              │
           │  - 写入翻译后的章节      │
           │  - 生成 EPUB             │
           └────────────▲─────────────┘
                        │ 系统/IO 调用
           ┌────────────┴─────────────┐
           │        系统基础层        │
           │  - 文件读取             │
           │  - ebooklib 解析        │
           │  - 文件路径存储/检查    │
           └────────────────────────────┘
```

## 贡献

我们欢迎 Issues 和 Pull Requests！

## 更新日志

### v1.0.0
- 初始发布
- 支持 EPUB 和 PDF 格式
- 基础文件处理 API 