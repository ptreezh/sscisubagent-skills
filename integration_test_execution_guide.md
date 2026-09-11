# Planning-with-Files 集成测试执行指南

## 测试执行概述

本指南提供具体的测试执行步骤，用于验证planning-with-files与三个分析技能的集成效果。

## 测试环境准备

### 1. 验证文件结构
确认以下目录结构存在：
```
D:\ssciskills\
├── sscisubagent-skills\
│   ├── skills\
│   │   ├── grounded-theory-expert\
│   │   ├── ant\
│   │   ├── field-analysis\
│   │   └── planning-with-files.md
```

### 2. 验证所需文件
确保以下文件存在并可访问：
- 所有技能的SKILL.md文件已更新
- planning-with-files.md支撑技能定义存在
- 原有的基础文件(task_plan.md, findings.md, progress.md)在主目录存在

## 扎根分析技能测试执行

### 测试1：依赖关系验证
**目标**：验证扎根分析技能正确声明对planning-with-files的依赖

**步骤**：
1. 打开 `D:\ssciskills\sscisubagent-skills\skills\grounded-theory-expert\SKILL.md`
2. 验证文件头部包含 `dependencies: - planning-with-files`
3. 验证详细指令中包含集成点标记（【Integration Point】）
4. 验证"集成功能"部分提及planning-with-files

**预期结果**：
- 依赖声明存在
- 集成点标记遍布所有分析阶段
- 集成功能部分提及planning-with-files

### 测试2：文件结构验证
**目标**：验证扎根分析技能目录中有正确的planning-with-files结构

**步骤**：
1. 检查 `D:\ssciskills\sscisubagent-skills\skills\grounded-theory-expert\` 目录
2. 验证存在以下文件：
   - task_plan.md
   - findings.md
   - progress.md

**预期结果**：
- 三个文件都存在
- 文件内容符合各自的功能定位

### 测试3：模拟执行流程
**目标**：模拟扎根分析技能调用planning-with-files的过程

**步骤**：
1. 模拟启动扎根分析
2. 验证是否调用planning-with-files进行初始化
3. 模拟开放编码阶段，验证是否更新findings.md和progress.md
4. 模拟轴心编码阶段，验证是否再次更新文件
5. 重复后续阶段，验证每个阶段的文件更新

**预期结果**：
- 每个分析阶段都会触发planning-with-files的相应操作
- 三文件内容随分析进程逐步更新
- 进度状态准确反映分析进展

## ANT分析技能测试执行

### 测试1：依赖关系验证
**目标**：验证ANT分析技能正确声明对planning-with-files的依赖

**步骤**：
1. 打开 `D:\ssciskills\sscisubagent-skills\skills\ant\SKILL.md`
2. 验证文件头部包含 `dependencies: - planning-with-files`
3. 验证详细指令中包含集成点标记（【Integration Point】）
4. 验证"核心流程"部分包含与planning-with-files的交互协议

**预期结果**：
- 依赖声明存在
- 集成点标记遍布所有分析阶段
- 集成协议部分提及planning-with-files

### 测试2：文件结构验证
**目标**：验证ANT分析技能目录中有正确的planning-with-files结构

**步骤**：
1. 检查 `D:\ssciskills\sscisubagent-skills\skills\ant\` 目录
2. 验证存在以下文件：
   - task_plan.md
   - findings.md
   - progress.md

**预期结果**：
- 三个文件都存在
- 文件内容符合ANT分析的特定需求

### 测试3：模拟执行流程
**目标**：模拟ANT分析技能调用planning-with-files的过程

**步骤**：
1. 模拟启动ANT分析
2. 验证是否调用planning-with-files进行初始化
3. 模拟行动者映射阶段，验证是否更新findings.md和progress.md
4. 模拟网络分析阶段，验证是否再次更新文件
5. 重复后续阶段，验证每个阶段的文件更新

**预期结果**：
- 每个分析阶段都会触发planning-with-files的相应操作
- 三文件内容随分析进程逐步更新
- 进度状态准确反映分析进展

## 场域分析技能测试执行

### 测试1：依赖关系验证
**目标**：验证场域分析技能正确声明对planning-with-files的依赖

**步骤**：
1. 打开 `D:\ssciskills\sscisubagent-skills\skills\field-analysis\SKILL.md`
2. 验证文件头部包含 `dependencies: - planning-with-files`
3. 验证详细指令中包含集成点标记（【Integration Point】）
4. 验证"详细指令"部分包含与planning-with-files的交互协议

**预期结果**：
- 依赖声明存在
- 集成点标记遍布所有分析阶段
- 集成协议部分提及planning-with-files

### 测试2：文件结构验证
**目标**：验证场域分析技能目录中有正确的planning-with-files结构

**步骤**：
1. 检查 `D:\ssciskills\sscisubagent-skills\skills\field-analysis\` 目录
2. 验证存在以下文件：
   - task_plan.md
   - findings.md
   - progress.md

**预期结果**：
- 三个文件都存在
- 文件内容符合场域分析的特定需求

### 测试3：模拟执行流程
**目标**：模拟场域分析技能调用planning-with-files的过程

**步骤**：
1. 模拟启动场域分析
2. 验证是否调用planning-with-files进行初始化
3. 模拟场域识别阶段，验证是否更新findings.md和progress.md
4. 模拟场域映射阶段，验证是否再次更新文件
5. 重复后续阶段，验证每个阶段的文件更新

**预期结果**：
- 每个分析阶段都会触发planning-with-files的相应操作
- 三文件内容随分析进程逐步更新
- 进度状态准确反映分析进展

## 集成验证测试

### 测试1：跨技能一致性验证
**目标**：验证三个技能使用planning-with-files的方式一致

**步骤**：
1. 比较三个技能的集成点标记格式
2. 验证调用planning-with-files的方式是否一致
3. 检查文件结构的相似性
4. 确认参数传递的一致性

**预期结果**：
- 集成点标记格式统一
- 调用方式一致
- 文件结构相似
- 参数传递规范统一

### 测试2：数据完整性验证
**目标**：验证分析过程中数据的完整性和一致性

**步骤**：
1. 检查task_plan.md中的任务状态是否准确
2. 验证findings.md中的记录是否完整
3. 确认progress.md中的进度是否同步
4. 验证跨文件数据的一致性

**预期结果**：
- 任务状态准确反映实际进度
- 发现记录完整且详细
- 进度信息实时更新
- 跨文件数据保持一致

## 测试执行记录表

### 扎根分析技能测试记录
| 测试编号 | 测试项目 | 执行状态 | 结果 | 备注 |
|---------|----------|----------|------|------|
| GT-01 | 依赖关系验证 | [ ] |  |  |
| GT-02 | 文件结构验证 | [ ] |  |  |
| GT-03 | 模拟执行流程 | [ ] |  |  |

### ANT分析技能测试记录
| 测试编号 | 测试项目 | 执行状态 | 结果 | 备注 |
|---------|----------|----------|------|------|
| ANT-01 | 依赖关系验证 | [ ] |  |  |
| ANT-02 | 文件结构验证 | [ ] |  |  |
| ANT-03 | 模拟执行流程 | [ ] |  |  |

### 场域分析技能测试记录
| 测试编号 | 测试项目 | 执行状态 | 结果 | 备注 |
|---------|----------|----------|------|------|
| FA-01 | 依赖关系验证 | [ ] |  |  |
| FA-02 | 文件结构验证 | [ ] |  |  |
| FA-03 | 模拟执行流程 | [ ] |  |  |

### 集成验证测试记录
| 测试编号 | 测试项目 | 执行状态 | 结果 | 备注 |
|---------|----------|----------|------|------|
| IV-01 | 跨技能一致性验证 | [ ] |  |  |
| IV-02 | 数据完整性验证 | [ ] |  |  |

## 问题记录与解决方案

### 常见问题
1. 文件权限不足
2. 依赖声明格式错误
3. 集成点标记缺失
4. 文件路径错误

### 解决方案
1. 确保足够的文件系统权限
2. 验证YAML格式正确性
3. 检查所有分析阶段是否包含集成点
4. 验证所有文件路径准确性

## 测试完成标准

- 所有测试项目执行完成
- 90%以上测试项目通过
- 未通过项目有明确解决方案
- 测试报告完整提交