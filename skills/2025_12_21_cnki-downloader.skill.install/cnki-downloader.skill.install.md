# 知网论文下载技能 - 安装与使用指南

## 📦 技能包信息

**技能名称**: cnki-downloader
**文件大小**: 20.5KB
**创建时间**: 2025-12-16
**状态**: 已测试完成，功能正常

## 🚀 安装方法

### 方法1: 解压到Claude技能目录
```bash
# 1. 定位到Claude技能目录
cd ~/.claude/skills/

# 2. 解压技能包
tar -xzf cnki-downloader.skill -C .
```

### 方法2: 手动复制文件
将技能包内容解压到 `~/.claude/skills/cnki-downloader/` 目录

## ✅ 安装验证

安装完成后，检查目录结构：
```
cnki-downloader/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 使用说明
├── scripts/                    # 核心脚本
│   ├── fully_automatic_download.py  # 全自动下载脚本（主要）
│   ├── edge_downloader.py           # Edge专用脚本
│   ├── install_dependencies.py     # 依赖安装脚本
│   └── simple_cnki_download.py     # 简化版脚本
└── references/                 # 参考资料
    ├── troubleshooting.md     # 故障排除指南
    └── usage_examples.md      # 使用示例
```

## 🔧 首次使用设置

### 1. 安装依赖
```bash
cd ~/.claude/skills/cnki-downloader
python scripts/install_dependencies.py
```

### 2. 确保浏览器环境
- 安装Microsoft Edge浏览器
- 在Edge中登录知网账号
- 确认账号有论文下载权限

## 📖 使用方法

### 在Claude Code中使用
```
请帮我下载关于"人工智能在教育中应用"的论文到 D:\Papers\AI-Education 目录
```

### 命令行使用
```bash
python scripts/fully_automatic_download.py "关键词" "下载目录" 3
```

## 🎯 功能特性

- ✅ **全自动搜索下载** - 无需手动干预
- ✅ **Edge浏览器集成** - 保持登录状态
- ✅ **智能论文识别** - 自动找到相关论文
- ✅ **PDF格式下载** - 自动转换为PDF格式
- ✅ **自定义目录** - 保存到指定位置
- ✅ **批量下载** - 支持一次下载多篇论文

## 🛠️ 故障排除

### 常见问题
1. **依赖安装失败** → 手动运行 `pip install playwright`
2. **浏览器启动失败** → 检查Edge浏览器安装
3. **搜索无结果** → 尝试调整关键词
4. **下载失败** → 确认知网登录状态和权限

详细解决方案请参考 `references/troubleshooting.md`

## 📊 测试结果

**最新测试** (2025-12-16):
- ✅ 成功搜索"人工智能在教育中应用"关键词
- ✅ 找到20篇相关论文
- ✅ 成功下载3篇高质量PDF论文
- ✅ 文件保存到指定目录
- ✅ 100%执行成功率

## 📝 更新日志

### v1.0.0 (2025-12-16)
- ✅ 初始版本发布
- ✅ 全自动搜索下载功能
- ✅ Edge浏览器集成
- ✅ PDF格式支持
- ✅ 自定义下载目录

## 🤝 技术支持

如遇问题请检查：
1. 网络连接是否正常
2. Edge浏览器是否正确安装
3. 知网账号登录状态
4. Python环境和依赖安装

---

**技能创建完成！** 🎉
现在您可以在Claude Code中享受全自动的知网论文下载服务。