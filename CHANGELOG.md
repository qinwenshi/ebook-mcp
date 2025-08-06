# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.5] - 2025-08-06

### 🔧 重构 (Refactored)
- **依赖管理现代化**: 移除 `requirements.txt`，完全使用 `pyproject.toml` 管理依赖
  - 删除 `requirements.txt` 文件
  - 更新所有README文件中的安装指令
  - 统一使用现代Python包管理标准
  - 简化安装流程：`uv pip install -e .` 或 `pip install -e .`

- **PDF处理优化**: 移除 `PyPDF2` 依赖，完全使用 `PyMuPDF`
  - 从 `pdf_helper.py` 中移除 `PyPDF2` 导入和 `get_meta_pypdf2` 函数
  - 更新 `pyproject.toml`，移除 `PyPDF2` 依赖
  - 删除 `test_pdf_metadata_comparison.py` 测试文件
  - 更新相关测试，移除 `PyPDF2` 相关测试
  - 修改 `pymupdf_metadata_demo.py`，移除 `PyPDF2` 比较逻辑
  - 增强PDF元数据提取功能，提供更丰富的元数据信息

### 🌍 新增功能 (Added)
- **国际化支持**: 添加多语言README文档
  - 新增德文README (`README-DE.md`)
  - 新增法文README (`README-FR.md`)
  - 新增日文README (`README-JP.md`)
  - 新增韩文README (`README-KR.md`)
  - 添加Kiro翻译工具配置 (`.kiro/hooks/readme-translation-hook.kiro.hook`)

### 🔧 技术改进 (Technical Improvements)
- **依赖管理**: 符合现代Python项目标准 (PEP 518/621)
- **PDF处理**: 提高性能和稳定性，减少依赖冲突
- **测试覆盖**: 所有测试通过 (76 passed, 5 skipped)
- **代码质量**: 简化代码结构，提高可维护性

### 📝 文档更新 (Documentation)
- 更新所有README文件中的安装指令
- 添加多语言支持文档
- 更新MCP客户端示例文档
- 改进项目文档的可访问性

### 🗑️ 移除 (Removed)
- `requirements.txt` 文件
- `PyPDF2` 依赖和相关代码
- `test_pdf_metadata_comparison.py` 测试文件
- 过时的安装指令引用

### 🔄 向后兼容性 (Backward Compatibility)
- ✅ 保持API兼容性，无需修改现有代码
- ✅ 所有MCP工具正常工作
- ✅ 功能完整性得到保证

### 📦 安装说明 (Installation)
```bash
# 开发环境
git clone <repository-url>
cd ebook-mcp
uv pip install -e .
# 或
pip install -e .

# 运行测试
./run_tests.sh
# 或
pytest src/ebook_mcp/tests/
```

### 🎯 影响评估 (Impact Assessment)
- **正面影响**:
  - 简化依赖管理
  - 提高PDF处理性能
  - 增强国际化支持
  - 减少维护复杂度
  - 符合现代Python项目标准

- **潜在影响**:
  - 用户需要更新安装方式
  - 移除了PyPDF2的特定功能（已由PyMuPDF替代）

### 🔄 迁移指南 (Migration Guide)
对于现有用户：
1. 删除 `requirements.txt` 文件（如果存在）
2. 使用 `uv pip install -e .` 重新安装
3. 更新CI/CD配置（如果使用requirements.txt）

---

## [1.0.4] - 2025-08-05

### 🔧 修复 (Fixed)
- 修复EPUB章节提取中的子章节截断问题
- 添加 `get_epub_chapter_markdown_fixed` 工具
- 改进章节边界检测逻辑
- 更新相关测试和文档

### 📝 文档更新 (Documentation)
- 添加 `HOW-TO-TEST.md` 测试文档
- 更新测试运行脚本
- 改进错误处理和日志记录

## [1.0.3] - 2025-08-04

### 🌟 新增功能 (Added)
- 添加完整的单元测试套件
- 创建测试配置文件和运行脚本
- 添加测试文档和示例

### 🔧 改进 (Improved)
- 改进错误处理机制
- 优化代码结构和可读性
- 增强测试覆盖率

## [1.0.2] - 2025-08-03

### 🌟 新增功能 (Added)
- 添加PDF章节内容提取功能
- 支持按章节标题提取内容
- 添加Markdown格式输出支持

### 🔧 改进 (Improved)
- 优化PDF元数据提取
- 改进错误处理
- 更新API文档

## [1.0.1] - 2025-08-02

### 🔧 修复 (Fixed)
- 修复PDF处理中的兼容性问题
- 改进EPUB元数据提取
- 优化文件路径处理

### 📝 文档更新 (Documentation)
- 更新安装说明
- 添加使用示例
- 改进API文档

## [1.0.0] - 2025-08-01

### 🌟 初始发布 (Initial Release)
- EPUB和PDF格式支持
- 基本文件处理API
- MCP客户端示例 - Claude, DeepSeek, OpenAI
- 支持从PyPI运行服务器
- 基本的元数据提取功能
- 表格内容提取支持
- 章节内容提取功能

---

## 版本说明 (Version Notes)

### 语义化版本控制
- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 变更类型
- **Added**: 新功能
- **Changed**: 对现有功能的变更
- **Deprecated**: 已经不建议使用，准备很快移除的功能
- **Removed**: 已经移除的功能
- **Fixed**: 对bug的修复
- **Security**: 对安全性的改进 