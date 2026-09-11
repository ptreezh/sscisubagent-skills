---
name: machine-learning-research-expert
description: |
  机器学习研究专家。提供系统化机器学习方法，支持模型选择、训练调优、
  特征工程、模型解释、性能评估。核心能力包括：数据准备、模型开发、
  超参数优化、交叉验证、模型部署。适用于预测建模、模式识别、
  数据驱动研究等场景。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "Hastie et al. (2009), Goodfellow et al. (2016)"
---

# 机器学习研究专家 (Machine Learning Research Expert)

## 概述

机器学习研究专家提供从数据到模型的完整工作流程，包括模型选择、特征工程、训练优化、性能评估和模型解释。

## ML工作流程

```
原始数据
    │
    ↓
┌─────────────────┐
│  数据准备       │ ← 清洗、分割、预处理
└────────┬────────┘
         ↓
┌─────────────────┐
│  特征工程       │ ← 选择、构造、转换
└────────┬────────┘
         ↓
┌─────────────────┐
│  模型选择       │ ← 问题类型、数据规模
└────────┬────────┘
         ↓
┌─────────────────┐
│  模型训练       │ ← 参数学习、超参数调优
└────────┬────────┘
         ↓
┌─────────────────┐
│  模型评估       │ ← 交叉验证、测试集
└────────┬────────┘
         ↓
┌─────────────────┐
│  模型解释       │ ← 特征重要性、SHAP
└─────────────────┘
```

## 问题类型与模型

### 监督学习

| 问题类型 | 目标 | 推荐模型 |
|----------|------|----------|
| 二分类 | 0/1预测 | Logistic、SVM、XGBoost |
| 多分类 | 多类别预测 | RF、XGBoost、神经网络 |
| 回归 | 连续值预测 | 线性回归、XGBoost、神经网络 |
| 排序 | 顺序预测 | LambdaMART、RankNet |

### 无监督学习

| 问题类型 | 目标 | 推荐模型 |
|----------|------|----------|
| 聚类 | 分组发现 | K-Means、DBSCAN、GMM |
| 降维 | 特征压缩 | PCA、t-SNE、UMAP |
| 异常检测 | 离群点识别 | Isolation Forest、LOF |

## 特征工程

### 特征类型

```
数值特征
├── 连续型: 年龄、收入
└── 离散型: 计数、等级

类别特征
├── 标称型: 性别、地区
└── 有序型: 教育程度

文本特征
├── 词频: TF-IDF
└── 语义: Word2Vec、BERT

时间特征
├── 周期性: 季节、工作日
└── 趋势性: 时间戳、滞后
```

### 特征转换

| 转换方法 | 适用场景 | 公式 |
|----------|----------|------|
| 标准化 | 正态分布 | (x-μ)/σ |
| 归一化 | 有界范围 | (x-min)/(max-min) |
| 对数变换 | 长尾分布 | log(x+1) |
| Box-Cox | 非正态 | (x^λ-1)/λ |

### 特征选择

```
过滤法
├── 方差阈值: 移除低方差特征
├── 相关性: 移除高相关特征
└── 互信息: 选择高信息量特征

包装法
├── 前向选择: 逐步添加
├── 后向消除: 逐步移除
└── 递归消除: RFE

嵌入法
├── L1正则: LASSO稀疏
├── 树模型: 特征重要性
└── 深度学习: 自动学习
```

## 模型训练

### 训练流程

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 数据分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 交叉验证
model = RandomForestClassifier(n_estimators=100)
cv_scores = cross_val_score(model, X_train, y_train, cv=5)

# 模型训练
model.fit(X_train, y_train)

# 模型评估
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

### 超参数优化

| 方法 | 优点 | 缺点 |
|------|------|------|
| 网格搜索 | 全面 | 计算量大 |
| 随机搜索 | 高效 | 可能遗漏 |
| 贝叶斯优化 | 智能搜索 | 需要工具 |

### 贝叶斯优化示例

```python
from skopt import BayesSearchCV

param_space = {
    'n_estimators': (50, 500),
    'max_depth': (3, 20),
    'min_samples_split': (2, 20),
}

opt = BayesSearchCV(
    RandomForestClassifier(),
    param_space,
    n_iter=50,
    cv=5,
    n_jobs=-1
)
opt.fit(X_train, y_train)
```

## 模型评估

### 分类指标

```
混淆矩阵:
              预测正类  预测负类
实际正类        TP        FN
实际负类        FP        TN

准确率 = (TP+TN)/(TP+TN+FP+FN)
精确率 = TP/(TP+FP)  # 预测正类的准确性
召回率 = TP/(TP+FN)  # 实际正类的覆盖率
F1 = 2×P×R/(P+R)     # 精确率和召回率的调和平均
AUC-ROC = 曲线下面积  # 分类器整体性能
```

### 回归指标

| 指标 | 公式 | 含义 |
|------|------|------|
| MAE | Σ|y-ŷ|/n | 平均绝对误差 |
| MSE | Σ(y-ŷ)²/n | 均方误差 |
| RMSE | √MSE | 均方根误差 |
| R² | 1-SS_res/SS_tot | 解释方差比例 |

### 交叉验证

```
K折交叉验证:
┌───────────────────────┐
│ 测 │ 训 │ 训 │ 训 │ 训 │ → Fold 1
├───────────────────────┤
│ 训 │ 测 │ 训 │ 训 │ 训 │ → Fold 2
├───────────────────────┤
│ 训 │ 训 │ 测 │ 训 │ 训 │ → Fold 3
├───────────────────────┤
│ 训 │ 训 │ 训 │ 测 │ 训 │ → Fold 4
├───────────────────────┤
│ 训 │ 训 │ 训 │ 训 │ 测 │ → Fold 5
└───────────────────────┘

平均性能 = Σ(Fold_i)/K
```

## 模型解释

### 特征重要性

```
树模型特征重要性:
- 基于分裂次数
- 基于信息增益
- 基于排列重要性

线性模型:
- 系数绝对值
- 标准化系数
```

### SHAP值

```python
import shap

# 计算SHAP值
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# 全局解释
shap.summary_plot(shap_values, X_test)

# 局部解释
shap.force_plot(explainer.expected_value, 
                shap_values[0], 
                X_test.iloc[0])
```

### SHAP解释图

```
特征重要性排序:
↑ 特征A  ████████████████  +0.35
│ 特征B  ████████████      +0.28
│ 特征C  ████████          +0.15
│ 特征D  ████              +0.08
↓ 特征E  ██                +0.04

红色: 高特征值  蓝色: 低特征值
```

## 常见问题处理

### 类别不平衡

| 方法 | 描述 |
|------|------|
| 过采样 | SMOTE、ADASYN |
| 欠采样 | RandomUnderSampler |
| 类别权重 | class_weight='balanced' |
| 阈值调整 | 调整分类阈值 |

### 过拟合

```
症状: 训练集表现好，测试集表现差

解决方案:
├── 增加数据量
├── 正则化(L1/L2)
├── 交叉验证
├── 早停(Early Stopping)
├── Dropout(神经网络)
└── 集成方法
```

### 数据泄露

```
常见泄露来源:
├── 目标变量泄漏: 使用未来信息
├── 特征泄露: 包含目标信息
├── 时间泄露: 时间序列分割不当
└── 预处理泄露: 使用全部数据做转换

预防措施:
├── 先分割再预处理
├── 使用Pipeline
├── 检查特征与目标的相关性
└── 时间序列使用时间分割
```

## 使用示例

```
用户: 构建一个预测客户流失的模型

AI: 我将执行完整的ML工作流程：

## 数据概况
- 样本量: 10,000
- 特征数: 25
- 目标分布: 流失20%, 未流失80%

## 特征工程
- 数值特征: 标准化
- 类别特征: One-Hot编码
- 新特征: 客户生命周期、消费频次

## 模型比较(5折交叉验证)
| 模型 | AUC | F1 |
|------|-----|-----|
| Logistic | 0.78 | 0.52 |
| Random Forest | 0.85 | 0.63 |
| XGBoost | 0.87 | 0.66 |
| LightGBM | 0.86 | 0.65 |

## 最优模型: XGBoost
- 测试集AUC: 0.86
- 测试集F1: 0.64

## Top 5 特征重要性
1. 最近活跃天数: 0.28
2. 月消费金额: 0.18
3. 投诉次数: 0.12
4. 会员等级: 0.09
5. 使用时长: 0.08
```

## 工具函数

| 工具 | 功能 |
|------|------|
| `feature_engineer.py` | 特征工程 |
| `model_trainer.py` | 模型训练 |
| `model_evaluator.py` | 模型评估 |
| `model_interpreter.py` | 模型解释 |

## 参考文献

1. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. 2nd ed.
2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*.
3. Molnar, C. (2022). *Interpretable Machine Learning*.
4. Zheng, A., & Casari, A. (2018). *Feature Engineering for Machine Learning*.

---

**技能版本**: 5.0.0  
**方法论标准**: Hastie et al. (2009)  
**创建时间**: 2026-03-15
