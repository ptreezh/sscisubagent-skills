# 系统动力学建模 - 完整工具链

## 🛠️ 建模工具栈

### 1. Vensim (首选 - 专业)
- **特点**: 图形化建模、因果回路图、存量流量图
- **适用**: 政策分析、商业建模、学术研究
- **网站**: [vensim.com](https://vensim.com/)
- **价格**: 学术/商业版

**核心功能**:
- Tree-shaped causal loop diagrams
- Stock & Flow diagrams
- Equation editor
- Reality check
- Sensitivity analysis

### 2. Stella (易用 - 教学)
- **特点**: 图形化、直观
- **适用**: 教学、快速原型
- **网站**: [iseesystems.com/stella/](https://iseesystems.com/stella/)

### 3. Insight Maker (免费 - Web)
- **特点**: 在线、免费、开源
- **适用**: 快速原型、Web分享
- **网站**: [insightmaker.org](https://insightmaker.org/)

### 4. PySD (Python - 编程)
- **特点**: Python框架、可编程
- **安装**: `pip install pysd`
- **文档**: [pysd.readthedocs.io](https://pysd.readthedocs.io/)

**示例代码**:
```python
import pysd

# 定义SD模型
model = pysd.read_vensim('model.mdl')

# 运行仿真
result = model.run(params={'param1': 10})

# 绘制结果
result.plot()
```

---

## 📊 建模流程

### Phase 1: 问题界定 (Week 1)

**Task**: 动态问题识别

**产出**:
- 动态问题陈述
- 关键变量清单
- 参考模式（历史数据）

### Phase 2: 系统建模 (Weeks 2-3)

**Task**: CLD + SFD建模

**产出**:
- 因果回路图 (CLD)
- 存量流量图 (SFD)
- 模型方程

### Phase 3: 仿真分析 (Weeks 4-6)

**Task**: 校准、敏感性、政策测试

**产出**:
- 校准报告
- 敏感性分析
- 政策情景报告

---

## 🐍 Vensim快速开始

### 1. 创建因果回路图

```
Population
  → Births (R+)  [正反馈]
  → Deaths (B-)  [负反馈]

Births = Population * Birth_Rate
Deaths = Population * Death_Rate
```

### 2. 创建存量流量图

```
Stock: Population
  Inflow: Births
  Outflow: Deaths

Population(t) = Population(t-dt) + (Births - Deaths) * dt
```

### 3. 添加延迟

```
Information Delay:感知延迟
Material Delay:交付延迟
```

### 4. 运行仿真

### 5. 敏感性分析

---

## 🐍 PySD快速开始

### 安装
```bash
pip install pysd matplotlib
```

### 创建模型
```python
import pysd
import matplotlib.pyplot as plt

# 定义模型
model = """
Population = INTEGRAL(Births - Deaths)
Births = Population * Birth_Rate
Deaths = Population * Death_Rate
"""

# 读取模型
mdl = pysd.read_vensim(model)

# 运行
stocks = mdl.run(params={'Birth_Rate': 0.1, 'Death_Rate': 0.08})

# 绘制
stocks['Population'].plot()
plt.show()
```

---

## 📈 输出要求

- [ ] CLD图 (PNG/PDF)
- [ ] SFD图 (PNG/PDF)
- [ ] 方程文档
- [ ] 仿真数据 (CSV)
- [ ] 行为模式图
- [ ] 敏感性分析报告
- [ ] 政策建议报告

---

**版本**: 5.0.0-ai-cli-native
**支持**: Vensim, Stella, Insight Maker, PySD
