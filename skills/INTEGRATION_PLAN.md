# 文献智能体与论文下载技能集成方案

**创建日期**: 2025-12-28
**状态**: 待集成

---

## 🔍 当前状况分析

### literature-expert 智能体

**文件位置**:
- `agents/literature-expert.md`
- `agents/literature-expert-v2.md`

**核心技能配置**:
```yaml
core_skills:
  - processing-citations
  - writing
  - validity-reliability
```

**问题**:
1. ❌ 这些技能在 `archive/skills/` 中，主要是指导性内容
2. ❌ **缺少实际的论文检索和下载能力**
3. ❌ archive中的 `literature-search-skill.md` 明确说明"**不提供任何文献下载功能**"

### 新建的论文下载技能

| 技能 | 平台 | 语言 | 功能 | 状态 |
|------|------|------|------|------|
| `pubscholar-auto-search` | PubScholar | 中文 | 自动搜索+下载 | ✅ 已创建，**未关联** |
| `arxiv-paper-search` | arXiv | 英文 | API搜索+下载 | ✅ 已创建，**未关联** |

**问题**:
- ❌ 两个新技能与 literature-expert **没有任何关联**
- ❌ literature-expert 不知道这两个技能的存在
- ❌ 用户需要手动选择技能，无法自动触发

---

## 🎯 集成目标

让 literature-expert 智能体能够：
1. ✅ **识别用户需求** - 自动判断需要中文还是英文论文
2. ✅ **自动调用技能** - 触发 pubscholar-auto-search 或 arxiv-paper-search
3. ✅ **整合结果** - 统一返回中英文文献结果
4. ✅ **提供指导** - 基于检索结果提供质量评估和趋势分析

---

## 🔧 集成方案

### 方案1: 更新 literature-expert 的 core_skills（推荐）

更新 `agents/literature-expert.md` 和 `agents/literature-expert-v2.md`:

```yaml
---
name: literature-expert
description: 文献管理专家，整合中英文论文检索、下载、引用管理和研究趋势分析。
core_skills:
  - pubscholar-auto-search    # 中文论文检索下载
  - arxiv-paper-search        # 英文论文检索下载
  - processing-citations       # 引用格式化
  - validity-reliability       # 质量评估
---
```

**优点**:
- ✅ 简单直接
- ✅ 符合现有架构
- ✅ AI可以自动调用这两个技能

**实现步骤**:
1. 编辑 literature-expert.md
2. 添加技能关联说明
3. 更新触发条件

### 方案2: 创建统一接口技能

创建新技能 `literature-integration`:

**文件**: `skills/literature-integration/SKILL.md`

```markdown
---
name: literature-integration
description: 中英文文献检索统一接口，自动判断并调用合适的检索技能。
core_skills:
  - pubscholar-auto-search
  - arxiv-paper-search
---

# 文献检索统一接口

## 自动路由逻辑

当用户提出文献检索需求时：
1. **语言检测**: 中文→pubscholar, 英文→arxiv
2. **平台检测**: 提到"PubScholar"→pubscholar, "arXiv"→arxiv
3. **默认行为**: 同时检索中英文文献

## 使用示例

```python
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import SynchronousPubScholarSearcher
from skills.arxiv_paper_search.scripts.arxiv_searcher import ArxivPaperSearcher

def search_papers(query, language='both'):
    results = []

    if language in ['chinese', 'both']:
        cn_searcher = SynchronousPubScholarSearcher()
        results.extend(cn_searcher.search(query))

    if language in ['english', 'both']:
        en_searcher = ArxivPaperSearcher()
        results.extend(en_searcher.search(query))

    return results
```
```

**优点**:
- ✅ 提供统一接口
- ✅ 自动语言检测
- ✅ 结果合并去重

### 方案3: literature-expert 作为协调器

让 literature-expert 作为**主控智能体**，协调其他技能：

```markdown
## 协调能力

### 自动技能调用
当用户需要文献检索时：
1. 识别检索需求（语言、平台、领域）
2. 自动调用对应技能：
   - 中文论文 → pubscholar-auto-search
   - 英文论文 → arxiv-paper-search
   - 引用格式化 → processing-citations
   - 质量评估 → validity-reliability
3. 整合多个技能的结果
4. 提供综合分析和建议

### 工作流程示例
```
用户: "帮我找关于数字鸿沟的论文"
  ↓
literature-expert 识别需求:
  - 关键词: 数字鸿沟
  - 语言: 中文
  ↓
调用 pubscholar-auto-search
  ↓
接收检索结果
  ↓
提供质量评估和趋势分析
  ↓
返回综合报告
```
```

**优点**:
- ✅ literature-expert 作为中心协调器
- ✅ 整合所有文献相关能力
- ✅ 提供端到端服务

---

## 📋 推荐实施方案

### 混合方案（方案1 + 方案3）

#### 步骤1: 更新 literature-expert 配置

**编辑文件**: `agents/literature-expert-v2.md`

```yaml
---
name: literature-expert
description: 文献管理专家，整合中英文论文检索、下载、引用管理和研究趋势分析。
model: claude-3-5-sonnet-20241022
core_skills:
  - pubscholar-auto-search    # 中文论文检索下载（新增）
  - arxiv-paper-search        # 英文论文检索下载（新增）
  - processing-citations       # 引用格式化
  - validity-reliability       # 质量评估
  - writing                   # 学术写作
---
```

#### 步骤2: 添加技能调用说明

在 literature-expert 中添加：

```markdown
## 📚 可用技能

### 自动检索技能
- **pubscholar-auto-search**: 中文论文检索（PubScholar平台）
  - 触发: "搜索中文论文"、"在PubScholar搜索"
  - 功能: 浏览器自动化、智能关键词扩展

- **arxiv-paper-search**: 英文论文检索（arXiv平台）
  - 触发: "搜索英文论文"、"在arXiv搜索"
  - 功能: API集成、批量下载摘要/PDF

### 辅助技能
- **processing-citations**: 引用格式化（GB/T 7714）
- **validity-reliability**: 文献质量评估
- **writing**: 学术写作指导

## 🔄 自动工作流程

### 场景1: 中文文献检索
```
用户: "搜索关于人工智能的中文论文"
  ↓
literature-expert 识别:
  - 语言: 中文
  - 关键词: 人工智能
  ↓
调用: pubscholar-auto-search
  ↓
返回: 中文论文列表 + 质量评估
```

### 场景2: 英文文献检索
```
用户: "在arXiv搜索transformer相关论文"
  ↓
literature-expert 识别:
  - 平台: arXiv
  - 关键词: transformer
  ↓
调用: arxiv-paper-search
  ↓
返回: 英文论文列表 + 引用格式
```

### 场景3: 中英文综合检索
```
用户: "帮我找关于社会网络分析的文献"
  ↓
literature-expert 识别:
  - 语言: 未指定 → 同时检索中英文
  ↓
并发调用:
  - pubscholar-auto-search → 中文结果
  - arxiv-paper-search → 英文结果
  ↓
整合并去重
  ↓
返回: 中英文文献列表 + 综合分析
```
```

#### 步骤3: 创建示例配置文件

创建 `agents/literature-expert-integration.md`:

```markdown
# 文献智能体集成配置

## 技能关联

| 智能体 | 关联技能 | 触发条件 |
|--------|---------|---------|
| literature-expert | pubscholar-auto-search | 中文论文检索 |
| literature-expert | arxiv-paper-search | 英文论文检索 |
| literature-expert | processing-citations | 引用格式化 |
| literature-expert | validity-reliability | 质量评估 |

## 调用示例

### Claude Code 调用方式

```python
# 文献智能体内部调用
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import SynchronousPubScholarSearcher
from skills.arxiv_paper_search.scripts.arxiv_searcher import ArxivPaperSearcher

# 根据用户需求自动选择
if is_chinese_query(user_query):
    searcher = SynchronousPubScholarSearcher()
    results = searcher.search(extract_keywords(user_query))
else:
    searcher = ArxivPaperSearcher()
    results = searcher.search(extract_keywords(user_query))
```

## 预期效果

- ✅ 用户只需说出需求，智能体自动选择合适的技能
- ✅ 中英文文献自动合并
- ✅ 提供端到端的文献服务
```

---

## 🎯 实施优先级

### 高优先级（立即实施）

1. **更新 literature-expert-v2.md**
   - 添加 pubscholar-auto-search 到 core_skills
   - 添加 arxiv-paper-search 到 core_skills
   - 添加技能调用说明

2. **测试集成**
   - 验证技能能否被自动调用
   - 测试中英文文献检索流程

### 中优先级（后续实施）

3. **创建 literature-integration 技能**
   - 统一接口
   - 自动语言检测
   - 结果合并去重

4. **优化工作流程**
   - 添加结果质量评估
   - 提供研究趋势分析

### 低优先级（可选）

5. **添加更多平台**
   - PubMed（生物医学）
   - IEEE Xplore（工程）
   - Google Scholar（通用）

---

## ✅ 预期效果

### 集成前

```python
# 用户需要手动选择技能
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import SynchronousPubScholarSearcher

searcher = SynchronousPubScholarSearcher()
results = searcher.search("人工智能")
```

**问题**:
- ❌ 需要知道具体技能名称
- ❌ 需要手动导入代码
- ❌ 需要判断使用哪个技能

### 集成后

```python
# 用户只需表达需求
user_query = "帮我找关于人工智能的论文"

# literature-expert 自动:
# 1. 识别语言（中文）
# 2. 调用 pubscholar-auto-search
# 3. 返回结果 + 质量评估
# 4. 提供引用格式化建议
```

**优势**:
- ✅ 自然语言交互
- ✅ 自动技能选择
- ✅ 端到端服务
- ✅ 综合分析报告

---

## 📝 总结

### 当前状态

| 项目 | 状态 |
|------|------|
| literature-expert 智能体 | ✅ 存在 |
| pubscholar-auto-search 技能 | ✅ 已创建，**未关联** |
| arxiv-paper-search 技能 | ✅ 已创建，**未关联** |
| 三个组件的集成 | ❌ **未完成** |

### 需要做什么

1. ✅ 更新 literature-expert 的 core_skills 配置
2. ✅ 添加技能调用说明到 literature-expert
3. ✅ 创建集成示例和文档
4. ⏳ 测试集成效果
5. ⏳ 根据测试结果优化

### 预期收益

- 🎯 **用户体验**: 从"手动选择技能"到"自动智能匹配"
- 🎯 **功能整合**: 文献检索、下载、管理一站式
- 🎯 **智能化**: 自动语言检测、质量评估、趋势分析

---

**文档日期**: 2025-12-28
**作者**: Claude Code
**状态**: 待实施
