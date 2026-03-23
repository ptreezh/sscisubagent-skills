# CAS Simulation Expert - 识别的模式

**更新日期**: 2026-03-08
**基于**: 复杂适应系统仿真实战经验

---

## 🎯 高频分析模式

### Pattern 1: 社会扩散ABM仿真

**频率**: 高频 (15次/年)
**成功率**: 90%
**平均时长**: 3-4小时

#### 标准仿真流程

```yaml
Phase 1: 概念建模（1小时）
  Task 1.1: 问题界定（15分钟）
    - 输出: 问题陈述
    - 验证: 适合ABM

  Task 1.2: 主体识别（15分钟）
    - 输出: 主体类型清单
    - 验证: 异质性充分

  Task 1.3: 互动规则设计（30分钟）
    - 输出: 规则文档
    - 验证: 基于理论

Phase 2: 技术实现（1-1.5小时）
  Task 2.1: 仿真环境搭建（20分钟）
    - 输出: 可运行ABM代码
    - 验证: 代码可运行

  Task 2.2: 主体行为编码（30分钟）
    - 输出: 行为规则实现
    - 验证: 行为符合设计

  Task 2.3: 互动机制实现（20分钟）
    - 输出: 互动网络
    - 验证: 网络结构合理

Phase 3: 校准与验证（1-1.5小时）
  Task 3.1: 参数校准（30分钟）
    - 输出: 校准报告
    - 验证: 与真实数据拟合

  Task 3.2: 敏感性分析（30分钟）
    - 输出: 敏感性分析报告
    - 验证: 多情景测试

  Task 3.3: 涌现验证（30分钟）
    - 输出: 涌现机制解释
    - 验证: 理论解释充分
```

#### 质量检查清单

```yaml
模型质量:
  - [ ] 主体异质性充分
  - [ ] 互动规则基于理论
  - [ ] 空间/网络适当
  - [ ] 随机性合理

仿真质量:
  - [ ] 多次运行（蒙特卡洛）
  - [ ] 参数敏感性分析
  - [ ] 涌现模式验证

透明性:
  - [ ] 代码可共享
  - [ ] 参数报告
  - [ ] 结果可复现
```

---

### Pattern 2: 组织演化ABM

**频率**: 中频 (8次/年)
**成功率**: 88%
**平均时长**: 4-5小时

#### 特殊考虑

```yaml
组织ABM特点:
  1. 层级结构
     - 管理层 vs 员工层
     - 权力关系
     - 决策流程

  2. 学习机制
     - 主体学习
     - 适应性改变
     - 策略演化

  3. 制度环境
     - 规则约束
     - 文化影响
     - 外部压力

仿真重点:
  - 组织结构演化
  - 决策机制
  - 创新扩散
```

---

## 🛠️ ABM工具链

### 1. Mesa (Python) - 首选

```python
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

class WealthAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 10

    def step(self):
        # 主体行为规则
        if self.wealth > 0:
            self.wealth -= 1

class WealthModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.datacollector = DataCollector(
            {"wealth": lambda a: a.wealth}
        )
        # 创建主体
        for i in range(N):
            a = WealthAgent(i, self)
            self.grid.place_agent(a, (0, 0))
            self.schedule.add(a)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
```

### 2. NetLogo - 易用

```netlogo
turtles-own [wealth]
breed [rich poor]

to setup
  create-turtles 100 [
    set wealth random 10
    ifelse wealth > 5
      [ set breed rich ]
      [ set breed poor ]
    ]
  ]

to go
  ask turtles [
    if breed = rich
      [ set wealth wealth + 1 ]
  ]
```

### 3. 其他工具

- Repast (Java) - 高性能
- AnyLogic (商业) - 综合
- GAMA - 适合GIS

---

## 🔍 涌现分析模式

### 常见涌现现象

```yaml
1. 路径依赖
   - 锁定效应
   - 历史依赖
   - 早期决策影响

2. 相变
   - 临界点
   - 快速转变
   - 滞后效应

3. 模式形成
   - 空间模式
   - 网络模式
   - 行为模式

4. 系统意外
   - 非预期结果
   - 反直觉行为
   - 崩溃风险
```

---

## 🎓 成功要素

✅ **主体异质性**
   - 属性多样
   - 行为多样
   - 避免同质化

✅ **基于理论**
   - 互动规则基于理论
   - 文献支持
   - 可解释

✅ **充分验证**
   - 多次运行
   - 参数敏感性
   - 模式验证

✅ **完全透明**
   - 代码共享
   - 参数报告
   - 结果可复现

---

## 💡 经验教训

### 成功模式

✅ **逐步构建**
   - 从简单开始
   - 逐步增加复杂性
   - 每步验证

✅ **多次运行**
   - 蒙特卡洛
   - 报告分布
   - 识别随机性

✅ **可视化辅助**
   - 空间可视化
   - 时间序列
   - 网络图

### 常见陷阱

❌ **过度拟合**
   - 追求与现实数据完美匹配
   - 牺牲普遍性
   - 需要平衡

❌ **参数过多**
   - 参数空间太大
   - 难以校准
   - 需要简化

❌ **忽视初始条件**
   - 初始分布影响结果
   - 需要测试多种初始条件
   - 报告初始条件敏感性

---

**版本**: 1.0.0
**最后更新**: 2026-03-08
