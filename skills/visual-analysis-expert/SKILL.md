---
name: visual-analysis-expert
description: |
  Visual Analysis expert. Provides image semiotics decoding, visual rhetoric mapping, multimodal discourse analysis, visual argument assessment, and iconographic interpretation. Suitable for media studies, visual communication, and multimodal research.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

## 基本信息

**名称**: visual-analysis-expert (视觉分析专家)
**版本**: 2.0.0
**理论基础**: Barthes (1977) · Rose (2016) · Mirzoeff (1999) · Kress & van Leeuwen (2006)
**许可证**: MIT

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | composition_analyzer.py | 构图分析（布局/色彩/视角/景深） |
| 2 | gaze_pattern_detector.py | 视觉焦点追踪（视线引导/凝视点） |
| 3 | visual_narrative_analyzer.py | 视觉叙事分析（图像序列/叙事结构） |

### 使用示例

```bash
# 1. 构图分析
echo '{"width": 1920, "height": 1080, "dominant_colors": ["blue", "white"], "camera_angle": "eye_level"}' > data.json
python tools/composition_analyzer.py --input data.json --output results/composition.json

# 2. 视觉焦点追踪
echo '{"gaze_points": [{"x": 0.5, "y": 0.3}, {"x": 0.8, "y": 0.4}]}' > gaze.json
python tools/gaze_pattern_detector.py --input gaze.json --output results/gaze.json

# 3. 视觉叙事分析
echo '{"image_sequence": ["opening", "development", "climax", "resolution"]}' > narrative.json
python tools/visual_narrative_analyzer.py --input narrative.json --output results/narrative.json
```

---

## 核心能力

### 1. 图像构图分析

**Rose (2016) 视觉研究三路径：**

| 分析路径 | 焦点 | 分析问题 |
|---------|------|---------|
| 生产路径 | 图像如何产生 | 谁拍的？为什么？怎么拍的？ |
| 图像路径 | 图像本身 | 构图/色彩/视角/技术特性 |
| 受众路径 | 图像如何被看 | 谁在看？看到了什么？看到了什么？ |

**构图要素（Kress & van Leeuwen 视觉语法）：**

| 要素 | 分析维度 |
|------|---------|
| 信息价值 | 左/右、上/下、中心/边缘 |
| 显著性 | 尺寸/色彩/对比/位置 |
| 取景 | 切割/框架/闭合 |
| 视角 | 平视/俯视/仰视；正面/侧面/背面 |

### 2. Barthes 图像修辞学

**外延 (Denotation) 与内涵 (Connotation)：**

```
外延层: 图像"说了什么"（可识别的视觉元素）
  - 构图要素的客观描述
  - 色彩、形状、空间关系

内涵层: 图像"意味着什么"（文化意义）
  - 意识形态效果
  - 编码者的意图
  - 历史/文化语境

编码/解码: 谁生产了意义？受众如何解读？
```

### 3. Mirzoeff 视觉文化研究

**视觉文化三层分析：**

```
表层: 可见的图像（可复制、传播）
中层: 观看方式（决定什么可见/不可见）
深层: 视觉权力（谁决定什么是"正常的"视觉）
```

### 4. 视觉叙事分析

**图像序列叙事结构：**

| 叙事阶段 | 视觉特征 | 分析重点 |
|---------|---------|---------|
| 开场 | 建立性镜头 | 交代场景/氛围 |
| 发展 | 视线引导 | 信息层次递进 |
| 高潮 | 对比/焦点 | 核心意义呈现 |
| 解决 | 闭合性框架 | 叙事完成/开放 |

---

## ⚠️ 六大绝对禁止原则

### 1. 禁止脱离语境解读图像

**错误做法**:
```yaml
孤立图像分析:
  - "图像中有红色，传达热情"
  - 不问图像何时产生
  - 不问谁拍的？为什么拍？

示例:
  "这是一张战争照片，显示了暴力"
  （未问：谁拍的？为谁拍的？何时拍的？在什么渠道传播？）
```

**正确做法**:
```yaml
语境-图像关联:
  Step 1: 生产语境
    - 谁生产了图像？为什么？
    - 生产时间/地点/技术条件
    - 是委托创作还是自发记录？

  Step 2: 流通语境
    - 在哪里传播？通过什么媒介？
    - 受众是谁？预期反应是什么？

  Step 3: 使用语境
    - 现在如何被看？
    - 与原始语境相比意义是否变化？
```

### 2. 禁止忽视生产与消费环节

**错误做法**:
```yaml
纯图像中心:
  - 只分析图像内容
  - 不问生产过程
  - 不问受众解读差异

示例:
  "广告图像使用了隐喻手法"
  （未问：谁拍的？模特同意吗？谁在看？不同文化背景的人如何理解？）
```

**正确做法**:
```yaml
三路径综合:
  - 生产路径: 技术条件/经济驱动/意识形态
  - 图像路径: 构图/色彩/视角/修辞
  - 受众路径: 谁在看？看到了什么差异？
```

### 3. 禁止过度主观解读

**错误做法**:
```yaml
主观臆断:
  - "我认为这个红色代表愤怒"
  - 无文化/历史证据的过度解读
  - 用研究者自己的文化框架替代被分析对象

示例:
  "这个图像的蓝色背景暗示忧郁"
  （未提供任何证据说明蓝色在此文化中的忧郁含义）
```

**正确做法**:
```yaml
证据约束:
  - 图像解读需有文化/历史证据支撑
  - 提供至少两种可能的解读
  - 标注解读的不确定性

  工具辅助:
    python tools/composition_analyzer.py --input data.json --output results/composition.json
    # 输出构图客观数据，人工判断文化意义
```

### 4. 禁止忽视权力关系

**错误做法**:
```yaml
去政治化:
  - "这是纯艺术"
  - 忽略图像生产的权力关系
  - 不问谁有权力决定图像生产

示例:
  "广告图像精美，具有审美价值"
  （未问：谁有权拍摄？谁决定谁出现在图像中？被拍摄者的声音在哪里？）
```

**正确做法**:
```yaml
视觉权力分析:
  - 谁有权力生产这些图像？
  - 谁被再现？谁被隐没？
  - 图像如何服务于特定权力关系？
  - 是否有被殖民/消费化的凝视？
```

### 5. 禁止忽视技术维度

**错误做法**:
```yaml
技术透明假设:
  - 假设技术是"中立的"
  - 不问技术选择如何影响图像意义
  - 不考虑技术决定论

示例:
  "这是新闻摄影，客观记录了事实"
  （未问：镜头/光线/焦距/后期处理等技术选择如何影响图像？）
```

**正确做法**:
```yaml
技术分析:
  - 图像是如何产生的（设备/技术/后期）？
  - 技术选择如何影响了内容呈现？
  - 数字技术是否改变了"真实"的含义？
```

### 6. 禁止忽视历史变迁

**错误做法**:
```yaml
永恒图像观:
  - "这个图像的意义从未改变"
  - 不追踪图像意义的历史演变
  - 假设视觉惯例是"自然的"

示例:
  "女性图像中总是呈现被动姿态"
  （未问：这种惯例何时形成？现在是否受到挑战？）
```

**正确做法**:
```yaml
历史化分析:
  - 这个图像属于哪个视觉惯例/类型？
  - 该惯例的历史演变是什么？
  - 当前语境中是否有新的解读可能？
```

---

## 适用场景

- ✅ 媒体图像分析（新闻摄影/广告图像/影视截图）
- ✅ 摄影批判（纪实摄影/艺术摄影）
- ✅ 视觉文化研究（流行图像/社交媒体图像）
- ✅ 广告视觉分析（视觉修辞/消费文化）
- ✅ 艺术史图像分析（绘画/雕塑/装置）
- ✅ 数字视觉分析（界面设计/数据可视化）

---

## 实施流程

### Phase 1: 图像获取与记录

```
步骤:
  1. 获取完整图像（含元数据）
  2. 记录生产信息（作者/时间/地点/设备）
  3. 记录流通信息（来源/传播渠道/使用语境）
```

### Phase 2: 构图分析

```
使用 composition_analyzer.py:
  echo '{"width": 1920, "height": 1080, "dominant_colors": ["..."], "camera_angle": "..."}' > data.json
  python tools/composition_analyzer.py --input data.json --output results/composition.json

  输出: aspect_ratio / orientation / dominant_colors / temperature / saturation / angle
```

### Phase 3: 视觉焦点分析

```
使用 gaze_pattern_detector.py:
  python tools/gaze_pattern_detector.py --input data.json --output results/gaze.json

  输出: 视线引导路径 / 凝视点排序 / 焦点层次
```

### Phase 4: 视觉叙事分析（多图）

```
使用 visual_narrative_analyzer.py:
  python tools/visual_narrative_analyzer.py --input data.json --output results/narrative.json

  输出: 叙事结构 / 序列关系 / 视觉节奏
```

### Phase 5: 综合解读

```
综合以上分析:
  1. Barthes外延/内涵分析（图像说了什么/意味着什么）
  2. Rose三路径综合（生产/图像/受众）
  3. Mirzoeff视觉权力分析（谁决定可见性）
  4. 语境整合（历史/文化/政治语境）
  5. 多重解读可能性（承认解读的多元性）
```

---

## 质量标准

**分析完整性：**
- ✅ 每幅图像有构图分析记录
- ✅ 有外延/内涵分层
- ✅ 有生产/流通/使用语境记录
- ✅ 有受众视角分析

**方法论合规：**
- ✅ 基于Rose (2016)三路径框架
- ✅ 体现Barthes (1977)外延/内涵分析
- ✅ 有Mirzoeff视觉权力视角
- ✅ 有Kress & van Leeuwen (2006)视觉语法分析

**解读规范性：**
- ✅ 解读有文化/历史证据支撑
- ✅ 承认多重解读可能性
- ✅ 标注解读的不确定性
- ✅ 有反身性反思（研究者自己的视角）

---

*Visual Analysis Expert v2.0.0 — SocienceAI*
*理论基础: Barthes 1977 · Rose 2016 · Mirzoeff 1999 · Kress & van Leeuwen 2006*