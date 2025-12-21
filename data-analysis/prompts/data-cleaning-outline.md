# 数据清洗详纲

## 1. 数据质量评估

### 1.1 完整性评估
- **缺失值分析**:
  - **缺失率计算**:
    ```python
    missing_rate = df.isnull().sum() / len(df)
    ```
    - 全局缺失率: 整个数据集的缺失率
    - 变量缺失率: 每个变量的缺失率
    - 记录缺失率: 每条记录的缺失率
  - **缺失模式识别**:
    - 完全随机缺失 (MCAR): 缺失与任何变量无关
    - 随机缺失 (MAR): 缺失与观测变量相关
    - 非随机缺失 (MNAR): 缺失与未观测变量相关
  - **缺失影响评估**:
    - 对统计分析的影响
    - 对建模结果的影响
    - 对推断有效性的影响

### 1.2 准确性评估
- **异常值检测**:
  - **统计方法**:
    - Z-score方法: |z| > 3 为异常值
      ```python
      z_scores = np.abs((data - data.mean()) / data.std())
      outliers = data[z_scores > 3]
      ```
    - IQR方法: 超出Q1-1.5*IQR或Q3+1.5*IQR
      ```python
      Q1 = data.quantile(0.25)
      Q3 = data.quantile(0.75)
      IQR = Q3 - Q1
      outliers = data[(data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)]
      ```
  - **可视化方法**:
    - 箱线图: 直观显示异常值
    - 散点图: 识别多元异常值
    - 直方图: 识别分布尾部异常
  - **机器学习方法**:
    - Isolation Forest: 隔离森林算法
    - Local Outlier Factor: 局部异常因子
    - One-Class SVM: 单类支持向量机

### 1.3 一致性评估
- **格式一致性**:
  - 数据类型一致性: 确保同类数据使用相同数据类型
  - 格式统一性: 统一日期、电话、地址等格式
  - 编码一致性: 统一分类变量编码
- **逻辑一致性**:
  - 逻辑约束检查: 检查数据间的逻辑关系
  - 业务规则检查: 检查是否符合业务规则
  - 范围检查: 检查数值是否在合理范围

## 2. 缺失值处理策略

### 2.1 缺失机制识别
- **MCAR (Missing Completely At Random)**:
  - 特征: 缺失与任何变量都无关
  - 处理: 可以安全删除缺失记录
  - 检验: Little's MCAR test
- **MAR (Missing At Random)**:
  - 特征: 缺失与观测变量相关，与未观测值无关
  - 处理: 使用插值或建模方法
  - 检验: 比较缺失组与非缺失组特征
- **MNAR (Missing Not At Random)**:
  - 特征: 缺失与未观测值相关
  - 处理: 需要专门的敏感性分析
  - 检验: 模式分析、专家判断

### 2.2 缺失值处理方法
- **删除方法**:
  - 删除缺失记录 (Listwise deletion):
    - 适用: 缺失率低(<5%)且MCAR
    - 优点: 简单直接
    - 缺点: 可能丢失重要信息
    ```python
    df_clean = df.dropna()
    ```
  - 删除缺失变量 (Pairwise deletion):
    - 适用: 特定分析中某些变量缺失
    - 优点: 保留更多信息
    - 缺点: 不同分析可能使用不同样本
- **填充方法**:
  - 统计量填充:
    - 均值填充: 适用于正态分布数据
      ```python
      df['var'].fillna(df['var'].mean(), inplace=True)
      ```
    - 中位数填充: 适用于偏态分布数据
      ```python
      df['var'].fillna(df['var'].median(), inplace=True)
      ```
    - 众数填充: 适用于分类数据
      ```python
      df['var'].fillna(df['var'].mode()[0], inplace=True)
      ```
  - 高级填充方法:
    - KNN填充: 基于相似记录填充
      ```python
      from sklearn.impute import KNNImputer
      imputer = KNNImputer(n_neighbors=5)
      df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
      ```
    - 多重插补: 生成多个完整数据集
      ```python
      from sklearn.experimental import enable_iterative_imputer
      from sklearn.impute import IterativeImputer
      imputer = IterativeImputer(random_state=42)
      df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
      ```
    - 模型预测: 使用模型预测缺失值

### 2.3 缺失值处理决策框架
1. **评估缺失率**:
   - 缺失率 < 5%: 考虑删除或简单填充
   - 缺失率 5%-15%: 使用高级填充方法
   - 缺失率 > 15%: 仔细评估，可能需要重新收集数据
2. **识别缺失机制**: 确定缺失模式
3. **选择处理方法**: 基于缺失机制和数据特征
4. **验证处理效果**: 检查处理后的数据质量

## 3. 异常值处理策略

### 3.1 异常值检测方法
- **单变量异常值检测**:
  - 统计方法:
    - Z-score方法: |z| > 3 为异常值
    - Modified Z-score: 基于中位数绝对偏差
      ```python
      from scipy import stats
      modified_z_scores = 0.6745 * (data - data.median()) / data.mad()
      outliers = data[np.abs(modified_z_scores) > 3.5]
      ```
    - IQR方法: 超出1.5倍四分位距
  - 可视化方法:
    - 箱线图: 直观显示异常值
    - 直方图: 识别分布尾部异常
    - Q-Q图: 识别偏离正态分布的点
- **多变量异常值检测**:
  - Mahalanobis距离: 考虑变量间相关性的距离
    ```python
    from scipy.spatial.distance import mahalanobis
    # 计算马氏距离
    ```
  - 孤立森林: 基于树的异常检测
    ```python
    from sklearn.ensemble import IsolationForest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    outliers = iso_forest.fit_predict(X)
    ```
  - 局部异常因子: 基于密度的异常检测
    ```python
    from sklearn.neighbors import LocalOutlierFactor
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
    outliers = lof.fit_predict(X)
    ```

### 3.2 异常值处理方法
- **保留异常值**:
  - 适用: 异常值代表重要信息
  - 方法: 标记但保留异常值
  - 优点: 保留完整信息
  - 缺点: 可能影响模型性能
- **修正异常值**:
  - 适用: 确认为录入错误
  - 方法: 使用合理值替换
  - 优点: 纠正错误数据
  - 缺点: 需要专业知识
- **删除异常值**:
  - 适用: 确认为错误数据
  - 方法: 直接删除异常记录
  - 优点: 提高数据质量
  - 缺点: 丢失数据信息
- **分组处理**:
  - 适用: 异常值在特定条件下合理
  - 方法: 将异常值分组分析
  - 优点: 保持信息完整性
  - 缺点: 增加分析复杂性

### 3.3 异常值处理决策框架
1. **识别异常值**: 使用多种方法识别
2. **分析原因**: 确定异常值产生的原因
3. **评估影响**: 评估异常值对分析的影响
4. **选择策略**: 基于原因和影响选择策略
5. **验证效果**: 检查处理后的数据质量

## 4. 数据标准化与变换

### 4.1 数据标准化方法
- **最小-最大标准化**:
  - 公式: (x - min) / (max - min)
  - 适用: 已知数据范围，需要缩放到特定范围
  - 优点: 结果范围明确
  - 缺点: 对异常值敏感
  ```python
  from sklearn.preprocessing import MinMaxScaler
  scaler = MinMaxScaler()
  scaled_data = scaler.fit_transform(data)
  ```
- **Z-score标准化**:
  - 公式: (x - mean) / std
  - 适用: 数据近似正态分布
  - 优点: 对异常值相对不敏感
  - 缺点: 需要数据近似正态分布
  ```python
  from sklearn.preprocessing import StandardScaler
  scaler = StandardScaler()
  standardized_data = scaler.fit_transform(data)
  ```
- **Robust标准化**:
  - 公式: (x - median) / IQR
  - 适用: 数据包含异常值
  - 优点: 对异常值不敏感
  - 缺点: 可能改变数据分布
  ```python
  from sklearn.preprocessing import RobustScaler
  scaler = RobustScaler()
  robust_scaled_data = scaler.fit_transform(data)
  ```

### 4.2 数据变换方法
- **对数变换**:
  - 适用: 右偏分布数据
  - 优点: 减少偏度，稳定方差
  - 缺点: 只适用于正值数据
  ```python
  import numpy as np
  log_transformed = np.log(data + 1)  # +1处理零值
  ```
- **平方根变换**:
  - 适用: 计数数据或轻度偏态数据
  - 优点: 减少偏度
  - 缺点: 只适用于非负数据
- **Box-Cox变换**:
  - 适用: 正值数据，需要正态化
  - 优点: 自动选择最优变换参数
  - 缺点: 只适用于正值数据
  ```python
  from scipy import stats
  transformed_data, lambda_param = stats.boxcox(data)
  ```

### 4.3 分类变量处理
- **标签编码**:
  - 适用: 有序分类变量
  - 优点: 保持顺序信息
  - 缺点: 引入人为数值关系
  ```python
  from sklearn.preprocessing import LabelEncoder
  le = LabelEncoder()
  encoded_labels = le.fit_transform(categorical_data)
  ```
- **独热编码**:
  - 适用: 无序分类变量
  - 优点: 避免人为数值关系
  - 缺点: 增加维度
  ```python
  from sklearn.preprocessing import OneHotEncoder
  ohe = OneHotEncoder(sparse=False)
  one_hot_encoded = ohe.fit_transform(categorical_data)
  ```
- **目标编码**:
  - 适用: 高基数分类变量
  - 优点: 减少维度，利用目标信息
  - 缺点: 可能导致过拟合
  ```python
  # 计算每个类别的目标变量均值
  target_mean = df.groupby('category')['target'].mean()
  df['category_encoded'] = df['category'].map(target_mean)
  ```

## 5. 数据一致性检查

### 5.1 格式统一化
- **日期格式统一**:
  - 统一日期格式: YYYY-MM-DD
  - 时区处理: 统一使用UTC或其他标准时区
  - 精度处理: 统一时间精度
- **文本格式统一**:
  - 大小写统一: 统一使用大写或小写
  - 空白字符: 去除多余空格、制表符
  - 特殊字符: 标准化特殊字符表示
- **数值格式统一**:
  - 小数位数: 统一小数位数
  - 千分位: 统一使用千分位分隔符
  - 负数表示: 统一负数表示方法

### 5.2 逻辑一致性检查
- **范围检查**:
  - 数值范围: 检查数值是否在合理范围
  - 分类范围: 检查分类值是否在预定义范围内
- **逻辑约束**:
  - 年龄与出生日期: 检查年龄与出生日期的一致性
  - 总额与分项: 检查总额是否等于分项之和
  - 业务规则: 检查是否符合业务逻辑规则
- **唯一性检查**:
  - 主键唯一性: 检查主键的唯一性
  - 业务唯一性: 检查业务层面的唯一性要求

## 6. 清洗质量评估

### 6.1 清洗前后对比
- **完整性对比**:
  - 缺失率变化: 清洗前后缺失率对比
  - 记录数变化: 清洗前后记录数对比
  - 变量数变化: 清洗前后变量数对比
- **准确性对比**:
  - 异常值减少: 清洗前后异常值数量对比
  - 分布改善: 清洗前后数据分布对比
- **一致性对比**:
  - 格式统一性: 清洗前后格式统一性对比
  - 逻辑一致性: 清洗前后逻辑一致性对比

### 6.2 清洗效果评估
- **统计指标**:
  - 均值、中位数、标准差变化
  - 偏度、峰度变化
  - 相关性变化
- **可视化评估**:
  - 清洗前后分布对比图
  - 清洗前后箱线图对比
  - 清洗前后散点图对比

## 7. 清洗策略文档

### 7.1 策略选择依据
- **数据特征**: 基于数据类型和分布特征
- **分析目标**: 基于后续分析需求
- **业务背景**: 基于业务知识和领域理解
- **资源约束**: 基于时间和计算资源限制

### 7.2 策略验证
- **效果验证**: 清洗效果是否达到预期
- **影响评估**: 清洗是否改变了数据的有用信息
- **可重现性**: 清洗过程是否可重现
- **可扩展性**: 清洗策略是否适用于新数据

## 8. 专业术语
- **MCAR**: Missing Completely At Random（完全随机缺失）
- **MAR**: Missing At Random（随机缺失）
- **MNAR**: Missing Not At Random（非随机缺失）
- **Z-score**: 标准化分数
- **IQR**: Interquartile Range（四分位距）
- **LOF**: Local Outlier Factor（局部异常因子）
- **Robust Scaling**: 鲁棒缩放
- **Target Encoding**: 目标编码

## 9. 参考文献
- van der Walt, S., et al. (2019). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research.
- Wickham, H. (2014). Tidy data. Journal of Statistical Software.
- Little, R. J. A. (1988). A test of missing completely at random for multivariate data with missing values. Journal of the American Statistical Association.
- Aggarwal, C. C. (2017). Outlier Analysis. Springer.