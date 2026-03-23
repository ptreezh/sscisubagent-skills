# CAS多主体建模 - 完整工具链

## 🛠️ 建模工具栈

### 1. NetLogo (首选 - 易用)
- **特点**: 图形化界面，内置模型库
- **适用**: 快速原型、教学、演示
- **语言**: NetLogo语言
- **文档**: [ccl.northwestern.edu/netlogo/](https://ccl.northwestern.edu/netlogo/)

**示例模型**:
```netlogo
turtles-own [see-friends]  ; 主体属性
breed [ born-turtles ]   ; 互动规则
ask turtles [ move ]     ; 行为执行
```

### 2. Mesa (Python - 灵活)
- **特点**: Python框架，可扩展性强
- **适用**: 研究级模型、大规模仿真
- **安装**: `pip install mesa`
- **文档**: [mesa.readthedocs.io](https://mesa.readthedocs.io/)

**示例代码**:
```python
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation

class WealthAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 10

    def step(self):
        # 主体行为规则
        self.wealth += 1

class WealthModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        # 创建主体
        for i in range(N):
            a = WealthAgent(i, self)
            self.grid.place_agent(a, (0, 0))
            self.schedule.add(a)

    def step(self):
        self.schedule.step()
```

### 3. Repast (Java - 高性能)
- **特点**: 高性能、企业级
- **适用**: 超大规模仿真
- **文档**: [repast.sourceforge.net/](https://repast.sourceforge.net/)

### 4. AnyLogic (商业 - 综合)
- **特点**: ABM+SD+DES集成
- **适用**: 商业项目、教学
- **价格**: 商业软件

---

## 📊 建模流程

### Phase 1: 概念建模 (Week 1)

**Task**: 界定研究问题和主体异质性

**产出**:
- 研究问题文档
- 主体属性清单
- 互动规则设计

### Phase 2: 技术实现 (Weeks 2-3)

**Task**: 编码ABM模型

**产出**:
- 可运行的ABM代码 (NetLogo/Python)
- 参数配置文件
- 初始条件设置

### Phase 3: 验证与分析 (Weeks 4-6)

**Task**: 模式验证、敏感性分析

**产出**:
- 仿真数据
- 统计分析报告
- 可视化图表

---

## 🐍 Python快速开始

### 安装Mesa
```bash
pip install mesa
```

### 创建简单模型
```python
# cas_model.py
from mesa import Agent, Model
from mesa.datacollection import DataCollector

class MoneyAgent(Agent):
    """具有货币的主体"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        if self.wealth > 0:
            self.wealth -= 1

class MoneyModel(Model):
    """货币交换模型"""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            {"wealth": lambda a: a.wealth}
        )
        # 创建主体
        for i in range(N):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
```

### 运行仿真
```bash
python cas_model.py
```

---

## 📈 输出要求

- [ ] 可运行代码
- [ ] 参数文档
- [ ] 仿真数据 (CSV)
- [ ] 可视化图表
- [ ] 敏感性分析报告

---

**版本**: 5.0.0-ai-cli-native
**支持**: NetLogo, Mesa, Repast, AnyLogic
