---
name: writing-grounded-theory-memos
description: 撰写扎根理论备忘录，包括过程记录、反思分析、理论备忘录和编码备忘录。当需要记录编码过程、深化理论思考、保存研究发现或进行理论反思时使用此技能。
version: 1.0.0
author: socienceAI.com
tags: [grounded-theory, memo-writing, process-documentation, theoretical-reflection, qualitative-research]
---

# 扎根理论备忘录写作技能 (Writing Grounded Theory Memos)

为扎根理论研究提供系统化的备忘录写作支持，确保研究过程的透明性、可追溯性和理论深度。

## 使用时机

当用户提到以下需求时，使用此技能：
- "写备忘录" 或 "备忘录写作"
- "记录编码过程" 或 "过程记录"
- "理论备忘录" 或 "理论反思"
- "反思分析" 或 "研究反思"
- "扎根理论备忘录" 或 "备忘录管理"
- 需要保存研究发现和思考过程

## 备忘录类型

### 1. 过程备忘录
记录具体的编码操作和思考过程：
- 编码会话的基本信息
- 概念识别和编码决策
- 编码理由和思考过程
- 初步的模式观察
- 下一步行动计划

### 2. 理论备忘录
记录理论概念的发展和关系：
- 理论概念的定义和演化
- 概念间的关系分析
- 新的理论洞察和发现
- 理论空白的识别
- 未来研究方向

### 3. 反思备忘录
对研究过程和结果的深度反思：
- 方法有效性的评估
- 遇到的挑战和解决方案
- 成功经验和失败教训
- 研究过程的改进建议
- 个人成长和收获

### 4. 操作备忘录
记录具体的技术操作和方法选择：
- 软件工具的使用
- 分析方法的选择理由
- 数据处理的技术细节
- 操作中的问题和解决方案

## 脚本调用时机
当需要生成不同类型的备忘录时，调用对应的脚本：
- 生成过程备忘录：`generate_process_memo.py`
- 生成理论备忘录：`generate_theory_memo.py`
- 生成反思备忘录：`generate_reflection_memo.py`
- 生成操作备忘录：`generate_operational_memo.py`
- 备忘录格式化：`format_memo.py`
- 备忘录质量检查：`check_memo_quality.py`

## 统一输入格式
```json
{
  "memo_context": {
    "memo_type": "process|theory|reflection|operational",
    "research_topic": "研究主题",
    "coding_stage": "编码阶段(开放/轴心/选择式)",
    "memo_purpose": "备忘录目的"
  },
  "input_data": {
    "session_info": {
      "date": "会话日期",
      "duration": "持续时间",
      "data_source": "数据来源",
      "participants": "参与者",
      "location": "地点"
    },
    "coding_info": {
      "concepts_identified": [
        {
          "id": "概念ID",
          "name": "概念名称",
          "definition": "概念定义",
          "examples": ["示例列表"]
        }
      ],
      "categories_developed": [
        {
          "id": "范畴ID",
          "name": "范畴名称",
          "properties": "范畴属性",
          "relationships": ["关系列表"]
        }
      ],
      "decisions_made": ["决策列表"],
      "challenges_encountered": ["挑战列表"],
      "solutions_applied": ["解决方案列表"]
    },
    "analysis_content": {
      "patterns_observed": ["观察到的模式"],
      "theoretical_insights": ["理论洞察"],
      "concept_evolution": "概念演化过程",
      "empirical_support": "实证支持",
      "evidence_examples": ["证据示例"]
    },
    "reflection_content": {
      "critical_reflections": ["批判性反思"],
      "method_effectiveness": "方法有效性评估",
      "limitations_identified": ["局限性"],
      "lessons_learned": ["经验教训"],
      "improvement_suggestions": ["改进建议"]
    }
  },
  "output_requirements": {
    "formality_level": "正式程度",
    "detail_level": "详细程度",
    "structure_preference": "结构偏好",
    "audience": "目标读者"
  }
}
```

## 统一输出格式
```json
{
  "summary": {
    "memo_type": "备忘录类型",
    "memo_title": "备忘录标题",
    "creation_date": "创建日期",
    "coding_stage": "编码阶段",
    "processing_time": "处理时间(秒)"
  },
  "details": {
    "memo_content": {
      "header": {
        "title": "标题",
        "date": "日期",
        "author": "作者",
        "coding_stage": "编码阶段"
      },
      "content_sections": [
        {
          "section_title": "章节标题",
          "section_content": "章节内容",
          "content_type": "内容类型"
        }
      ],
      "structured_elements": {
        "key_points": ["要点列表"],
        "decisions": ["决策列表"],
        "reflections": ["反思列表"],
        "next_steps": ["下一步列表"],
        "questions": ["问题列表"]
      }
    },
    "theoretical_components": {
      "new_insights": ["新的理论洞察"],
      "concept_developments": ["概念发展"],
      "theory_connections": ["理论连接"],
      "gaps_identified": ["识别的空白"]
    },
    "process_documentation": {
      "methods_used": ["使用的方法"],
      "challenges_faced": ["面临的挑战"],
      "solutions_developed": ["开发的解决方案"],
      "lessons_learned": ["学到的经验"]
    },
    "quality_indicators": {
      "completeness_score": "完整性分数(0-1)",
      "reflexivity_score": "反思性分数(0-1)",
      "theoretical_depth": "理论深度分数(0-1)",
      "actionability": "可操作性分数(0-1)"
    }
  },
  "formatted_output": {
    "markdown_content": "格式化后的Markdown内容",
    "file_path": "建议的文件路径",
    "naming_suggestion": "命名建议"
  },
  "metadata": {
    "timestamp": "时间戳",
    "version": "版本号",
    "skill": "writing-grounded-theory-memos",
    "processing_stage": "处理阶段"
  }
}
```

## 执行步骤

### 第一步：确定备忘录类型

根据用户需求确定合适的备忘录类型：
- **过程记录** → 调用 `generate_process_memo.py`
- **理论发展** → 调用 `generate_theory_memo.py`
- **反思分析** → 调用 `generate_reflection_memo.py`
- **技术操作** → 调用 `generate_operational_memo.py`

### 第二步：准备输入数据

根据备忘录类型准备相应输入数据：
- 会话信息（时间、数据来源等）
- 编码或分析内容
- 思考过程和理由
- 初步结果和发现
- 遇到的问题和解决方案

### 第三步：执行脚本生成备忘录

使用对应的脚本生成备忘录内容，并通过 `format_memo.py` 进行格式化。

### 第四步：质量检查

使用 `check_memo_quality.py` 进行质量检查，确保备忘录满足标准：
- **及时性**：编码后立即记录
- **具体性**：详细记录具体内容
- **反思性**：包含深度分析
- **连贯性**：保持逻辑连贯

## 质量检查清单

在完成备忘录后，请检查以下项目：

### 完整性检查
- [ ] 包含基本会话信息
- [ ] 记录了决策过程
- [ ] 包含初步分析结果
- [ ] 规划了下一步行动

### 理论深度检查
- [ ] 有深度理论思考
- [ ] 识别了理论洞察
- [ ] 连接了实证数据
- [ ] 提出了理论问题

### 反思质量检查
- [ ] 进行了批判性反思
- [ ] 识别了成功和失败
- [ ] 总结了经验教训
- [ ] 提出了改进方向

### 写作质量检查
- [ ] 语言表达清晰
- [ ] 逻辑结构合理
- [ ] 内容组织有序
- [ ] 格式规范统一

## 备忘录管理建议

### 组织结构
建议按以下方式组织备忘录：
- **memos/process/**：过程备忘录
- **memos/theory/**：理论备忘录
- **memos/reflection/**：反思备忘录
- **memos/operational/**：操作备忘录

### 命名规范
- **过程备忘录**：YYYY-MM-DD-session-N.md
- **理论备忘录**：concept-name-development.md
- **反思备忘录**：YYYY-MM-DD-reflection.md
- **操作备忘录**：tool-name-usage.md

### 定期回顾
- 每周回顾备忘录内容
- 识别理论发展脉络
- 总结经验教训
- 调整研究方向

## 常见问题处理

**问题：不知从何写起**
- 解决：从最基本的信息开始记录
- 技巧：使用提供的标准模板

**问题：内容过于简略**
- 解决：详细记录思考过程和理由
- 方法：问自己"为什么"和"怎么样"

**问题：缺乏理论深度**
- 解决：连接概念与理论框架
- 策略：寻找更广泛的理论意义

**问题：备忘录分散混乱**
- 解决：建立统一的组织系统
- 建议：定期整理和归类

## 完成标志

高质量的备忘录应该：
1. 详细记录了研究过程
2. 体现了深度理论思考
3. 包含了批判性反思
4. 指导了后续研究方向

---

*此技能为扎根理论研究提供全面的备忘录写作支持，确保研究过程的严谨性和理论发展的可追溯性。*