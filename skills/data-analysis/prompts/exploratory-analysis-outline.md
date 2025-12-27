# 探索性分析详纲

## 1. 单变量分析

### 1.1 连续变量分析
- **集中趋势度量**:
  - 均值 (Mean): 算术平均值，对异常值敏感
    ```python
    mean_val = data.mean()
    ```
  - 中位数 (Median): 中间值，对异常值不敏感
    ```python
    median_val = data.median()
    ```
  - 众数 (Mode): 出现频率最高的值
    ```python
    mode_val = data.mode()
    ```
- **离散程度度量**:
  - 方差 (Variance): 数据离散程度的平方
    ```python
    variance = data.var()
    ```
  - 标准差 (Standard Deviation): 数据离散程度
    ```python
    std_dev = data.std()
    ```
  - 四分位距 (Interquartile Range): Q3-Q1
    ```python
    iqr = data.quantile(0.75) - data.quantile(0.25)
    ```
- **分布形状度量**:
  - 偏度 (Skewness): 分布对称性的度量
    - 正偏度: 右尾较长
    - 负偏度: 左尾较长
    - 零偏度: 对称分布
    ```python
    from scipy.stats import skew
    skewness = skew(data)
    ```
  - 峰度 (Kurtosis): 分布尖锐程度的度量
    - 正峰度: 尖峰分布
    - 负峰度: 平峰分布
    - 零峰度: 正态峰度
    ```python
    from scipy.stats import kurtosis
    kurt = kurtosis(data)
    ```

### 1.2 分类变量分析
- **频数分析**:
  - 绝对频数: 每个类别的观测数量
    ```python
    freq_abs = data.value_counts()
    ```
  - 相对频数: 每个类别的比例
    ```python
    freq_rel = data.value_counts(normalize=True)
    ```
- **集中趋势**:
  - 众数: 出现最频繁的类别
- **多样性指标**:
  - 基尼系数: 衡量分类多样性
    ```python
    gini_coefficient = 1 - sum((freq_rel)**2)
    ```
  - 信息熵: 衡量不确定性
    ```python
    from scipy.stats import entropy
    entropy_val = entropy(freq_rel, base=2)
    ```

### 1.3 可视化方法
- **直方图**: 显示连续变量分布
  ```python
  import matplotlib.pyplot as plt
  plt.hist(data, bins=30)
  ```
- **核密度估计**: 平滑的分布估计
  ```python
  import seaborn as sns
  sns.kdeplot(data)
  ```
- **箱线图**: 显示分布和异常值
  ```python
  plt.boxplot(data)
  ```
- **饼图**: 显示分类变量比例
  ```python
  plt.pie(freq_rel.values, labels=freq_rel.index)
  ```

## 2. 双变量分析

### 2.1 连续-连续变量关系
- **相关分析**:
  - 皮尔逊相关: 线性关系度量
    ```python
    from scipy.stats import pearsonr
    corr, p_value = pearsonr(var1, var2)
    ```
  - 斯皮尔曼相关: 单调关系度量
    ```python
    from scipy.stats import spearmanr
    corr, p_value = spearmanr(var1, var2)
    ```
  - 肯德尔相关: 序列相关度量
    ```python
    from scipy.stats import kendalltau
    corr, p_value = kendalltau(var1, var2)
    ```
- **回归分析**:
  - 简单线性回归: Y = β₀ + β₁X + ε
    ```python
    from sklearn.linear_model import LinearRegression
    reg = LinearRegression().fit(X.reshape(-1, 1), Y)
    ```
  - 多项式回归: 捕获非线性关系
- **可视化**:
  - 散点图: 显示两变量关系
  - 气泡图: 添加第三维度信息
  - 回归线: 显示拟合关系

### 2.2 连续-分类变量关系
- **组间比较**:
  - t检验: 两组均值比较
    ```python
    from scipy.stats import ttest_ind
    t_stat, p_val = ttest_ind(group1, group2)
    ```
  - 方差分析: 多组均值比较
    ```python
    from scipy.stats import f_oneway
    f_stat, p_val = f_oneway(group1, group2, group3)
    ```
  - 非参数检验: 非正态数据比较
    ```python
    from scipy.stats import mannwhitneyu
    u_stat, p_val = mannwhitneyu(group1, group2)
    ```
- **可视化**:
  - 箱线图: 比较不同组的分布
  - 小提琴图: 显示分布形状和密度
  - 点图: 显示组均值

### 2.3 分类-分类变量关系
- **关联分析**:
  - 卡方检验: 独立性检验
    ```python
    from scipy.stats import chi2_contingency
    chi2, p_val, dof, expected = chi2_contingency(contingency_table)
    ```
  - Cramér's V: 关联强度度量
    ```python
    cramers_v = np.sqrt(chi2 / (n * (min(r, c) - 1)))
    ```
  - Phi系数: 2x2表关联度量
- **可视化**:
  - 交叉表热图: 显示频率分布
  - 马赛克图: 显示比例关系

## 3. 多变量分析

### 3.1 降维技术
- **主成分分析 (PCA)**:
  - 目的: 降低维度，保留主要信息
  - 步骤:
    1. 标准化数据
    2. 计算协方差矩阵
    3. 计算特征值和特征向量
    4. 选择主要成分
  ```python
  from sklearn.decomposition import PCA
  pca = PCA(n_components=2)
  transformed_data = pca.fit_transform(data)
  ```
- **因子分析**:
  - 目的: 发现潜在结构
  - 类型: 探索性、验证性因子分析
- **多维尺度 (MDS)**:
  - 目的: 在低维空间表示高维距离关系

### 3.2 聚类分析
- **K-均值聚类**:
  - 原理: 最小化簇内平方和
  - 优点: 简单高效
  - 缺点: 需要预设簇数
  ```python
  from sklearn.cluster import KMeans
  kmeans = KMeans(n_clusters=k)
  clusters = kmeans.fit_predict(data)
  ```
- **层次聚类**:
  - 原理: 构建树状聚类结构
  - 优点: 不需要预设簇数
  - 缺点: 计算复杂度高
- **DBSCAN**:
  - 原理: 基于密度的聚类
  - 优点: 可发现任意形状的簇
  - 缺点: 参数选择困难

### 3.3 关联规则挖掘
- **Apriori算法**:
  - 支持度: 规则在数据中出现的频率
  - 置信度: 规则成立的条件概率
  - 提升度: 规则的有用性度量
- **FP-Growth算法**:
  - 更高效的关联规则挖掘方法

## 4. 模式识别与异常检测

### 4.1 模式识别
- **趋势识别**:
  - 线性趋势: 使用线性回归检测
  - 非线性趋势: 使用多项式回归或平滑技术
  - 季节性: 检测周期性模式
- **周期性模式**:
  - 时间序列分解: 趋势、季节性、随机成分
  - 频谱分析: 识别主要频率成分
- **分组模式**:
  - 自然分组: 数据中的自然聚类
  - 异质性: 不同子群的差异

### 4.2 异常检测
- **统计方法**:
  - Z-score: 基于正态分布的异常检测
  - IQR: 基于四分位距的异常检测
- **机器学习方法**:
  - 孤立森林: 隔离异常值
  - 一类SVM: 异常检测
  - 自编码器: 基于重构误差的异常检测

## 5. 假设生成

### 5.1 关系假设
- **因果关系假设**: X导致Y的变化
- **相关关系假设**: X与Y存在相关关系
- **调节关系假设**: Z调节X与Y的关系
- **中介关系假设**: M介导X对Y的影响

### 5.2 差异假设
- **组间差异**: 不同组间存在显著差异
- **时间差异**: 不同时间点存在显著差异
- **情境差异**: 不同情境下存在显著差异

### 5.3 分布假设
- **正态性假设**: 数据服从正态分布
- **方差齐性假设**: 不同组方差相等
- **独立性假设**: 观测值相互独立

## 6. 数据可视化最佳实践

### 6.1 选择合适的图表
- **连续变量分布**: 直方图、密度图、箱线图
- **分类变量分布**: 条形图、饼图、帕累托图
- **两变量关系**: 散点图、气泡图、热图
- **时间序列**: 线图、面积图、阶梯图

### 6.2 可视化原则
- **简洁性**: 避免不必要的装饰
- **清晰性**: 确保信息清晰传达
- **一致性**: 保持风格一致
- **准确性**: 避免误导性表示

### 6.3 高级可视化技术
- **交互式可视化**: 使用Plotly等库
- **多面板图**: 展示多个变量关系
- **动态可视化**: 展示随时间变化的趋势

## 7. 探索性分析报告结构

### 7.1 报告大纲
1. **数据概览**: 数据集基本信息
2. **变量分析**: 单变量分析结果
3. **关系分析**: 双变量和多变量分析
4. **模式发现**: 重要发现和模式
5. **假设生成**: 可验证的假设
6. **建模建议**: 后续建模建议

### 7.2 关键洞察
- **主要发现**: 最重要的发现
- **意外发现**: 意外的模式或关系
- **数据质量**: 数据质量问题和处理建议
- **分析局限**: 探索性分析的局限性

## 8. 统计检验选择指南

### 8.1 单样本检验
- **t检验**: 连续变量，正态分布
- **Wilcoxon符号秩检验**: 连续变量，非正态分布
- **卡方检验**: 分类变量

### 8.2 两样本检验
- **独立t检验**: 两独立组，正态分布
- **Mann-Whitney U检验**: 两独立组，非正态分布
- **配对t检验**: 两相关组，正态分布
- **Wilcoxon符号秩检验**: 两相关组，非正态分布

### 8.3 多样本检验
- **方差分析(ANOVA)**: 多组均值比较，正态分布
- **Kruskal-Wallis检验**: 多组比较，非正态分布
- **卡方检验**: 多组分类变量比较

## 9. 专业术语
- **效应量**: 现象大小的标准化度量
- **统计功效**: 正确拒绝虚假零假设的概率
- **多重比较**: 同时检验多个假设的问题
- **共线性**: 自变量间高度相关
- **交互效应**: 变量间相互影响的效应
- **中介效应**: 变量间通过中介变量的效应

## 10. 参考文献
- Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.
- Wickham, H. (2016). ggplot2: Elegant Graphics for Data Analysis. Springer.
- Hyndman, R. J., & Fan, Y. (1996). Sample quantiles in statistical packages. The American Statistician.
- Cleveland, W. S. (1993). Visualizing Data. Hobart Press.