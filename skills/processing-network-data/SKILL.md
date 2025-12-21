---
name: processing-network-data
description: 处理社会网络数据，包括关系数据收集、矩阵构建、数据清洗验证和多模网络处理。当需要从问卷、访谈、观察或数字记录中提取关系数据，构建标准化的网络矩阵时使用此技能。
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [social-network-analysis, network-data-processing, data-cleaning, matrix-construction, relational-data]
---

# 网络数据处理技能 (Processing Network Data)

## Overview
专门用于社会网络研究的数据收集和预处理，将原始关系数据转换为标准化的网络分析格式。

## When to Use This Skill
Use this skill when the user requests:
- Processing of social network data from various sources
- Conversion of relational data to network format
- Cleaning and validation of network data
- Construction of adjacency matrices or edgelists
- Integration of multiple data sources into network format
- Preparation of network data for analysis
- Handling of multiplex or multimodal network data
- Transformation of survey or interview data into network format

## Quick Start
When a user requests network data processing:
1. **Identify** the data source type (survey, interview, observation, digital traces)
2. **Extract** relational information from raw data
3. **Clean** and validate the extracted relationships
4. **Format** data into standard network representation
5. **Validate** the network data quality and completeness

## Core Functions (Progressive Disclosure)

### Primary Functions
- **Data Format Recognition**: Identify and classify input data formats
- **Basic Relation Extraction**: Extract fundamental relationship data
- **Simple Data Cleaning**: Perform basic data cleaning and validation
- **Matrix Construction**: Build basic adjacency matrices

### Secondary Functions
- **Multi-source Integration**: Integrate data from multiple sources
- **Advanced Cleaning**: Perform sophisticated data cleaning
- **Attribute Processing**: Handle node and edge attributes
- **Quality Validation**: Validate data quality and completeness

### Advanced Functions
- **Temporal Network Processing**: Handle time-series network data
- **Multiplex Network Construction**: Build networks with multiple relationship types
- **Missing Data Imputation**: Fill missing relationships using appropriate methods
- **Validation and Verification**: Comprehensive data validation and verification

## Detailed Instructions

### 1. Data Source Identification
   - Identify the type of data source (questionnaire, interview, observation, digital traces)
   - Assess the structure and organization of the data
   - Determine the appropriate processing pipeline
   - Identify potential data quality issues
   - Plan the extraction strategy

### 2. Relational Data Extraction
   - Extract relationships from questionnaire data
   - Parse relationships from interview transcripts
   - Code relationships from observation records
   - Mine relationships from digital traces
   - Handle multiple relationship types

### 3. Data Cleaning and Validation
   - Identify and handle missing values
   - Detect and address data inconsistencies
   - Validate relationship data accuracy
   - Normalize data formats and representations
   - Check for data integrity

### 4. Network Matrix Construction
   - Create node lists with appropriate identifiers
   - Build adjacency matrices (binary, weighted, directed)
   - Handle different network types (single-mode, multi-mode)
   - Process node and edge attributes
   - Create standardized network formats

### 5. Attribute Integration
   - Integrate node attributes (demographics, characteristics)
   - Process edge attributes (strength, type, duration)
   - Handle temporal attributes for dynamic networks
   - Validate attribute data consistency
   - Map attributes to network structure

### 6. Quality Assurance
   - Verify network data completeness
   - Check for data accuracy and consistency
   - Assess potential biases in data collection
   - Validate network construction procedures
   - Document data processing decisions

### 7. Output Generation
   - Generate standardized network data files
   - Create data quality reports
   - Produce network statistics and metrics
   - Document processing procedures
   - Provide recommendations for analysis

## Parameters
- `data_source_type`: Type of source data (survey, interview, observation, digital)
- `network_type`: Type of network (binary, weighted, directed, undirected, bipartite)
- `relationship_types`: Types of relationships to extract (friendship, advice, collaboration, etc.)
- `attribute_handling`: How to handle node/edge attributes (include, exclude, summarize)
- `missing_data_strategy`: Strategy for handling missing data (omit, impute, estimate)
- `validation_level`: Level of validation to perform (basic, comprehensive, extensive)
- `output_format`: Desired output format (edgelist, adjacency matrix, graphml, etc.)

## Examples

### Example 1: Survey Data Processing
User: "Convert my social network survey data to network format for analysis"
Response: Extract relationships from survey responses, create adjacency matrix, validate data quality, generate network file.

### Example 2: Interview Data Processing
User: "Process my interview data to extract relationship information"
Response: Identify relationships in interview transcripts, code relationship types, construct network, validate accuracy.

### Example 3: Digital Trace Processing
User: "Extract network data from email communication logs"
Response: Parse email logs, identify sender-receiver relationships, create communication network, analyze patterns.

## Quality Standards

- Apply systematic data processing procedures
- Maintain data integrity throughout processing
- Validate the accuracy of relationship extraction
- Document all processing steps and decisions
- Consider cultural context in Chinese network data

## Output Format

- Processed network data in standard format
- Data quality assessment report
- Relationship extraction documentation
- Network statistics and basic metrics
- Processing procedure documentation

## Resources
- Social network data processing literature
- Data cleaning and validation guides
- Examples of network data processing in Chinese context
- Software tools for network data processing

## Metadata
- Compatibility: Claude 3.5 Sonnet and above
- Domain: Social Network Analysis, Data Processing
- Language: Optimized for Chinese research context

## 使用时机

当用户提到以下需求时，使用此技能：
- "网络数据处理" 或 "关系数据处理"
- "问卷数据处理" 或 "社会网络问卷"
- "关系提取" 或 "关系数据挖掘"
- "矩阵构建" 或 "邻接矩阵"
- "数据清洗" 或 "数据验证"
- 需要从原始数据中构建社会网络

## 数据类型识别

### 1. 问卷数据
- **自我中心网络问卷**：围绕个体的关系网络
- **整体网络问卷**：群体内的关系网络
- **名生成器问卷**：重要关系人的识别
- **名解释器问卷**：关系特征的详细描述

### 2. 访谈数据
- **深度访谈记录**：文本形式的关系描述
- **焦点小组讨论**：多人互动关系记录
- **半结构化访谈**：标准化问题收集的关系信息

### 3. 观察数据
- **参与观察记录**：实地观察的互动关系
- **系统观察数据**：标准化观察表格记录的关系
- **非参与观察**：外部观察者记录的关系模式

### 4. 数字数据
- **社交媒体数据**：微博、微信等平台的关系数据
- **通信记录**：电话、短信等通信关系
- **邮件数据**：组织内的邮件往来关系

## 执行步骤

### 第一步：数据格式识别和导入

1. **识别数据来源类型**
   - 确定数据是问卷、访谈、观察还是数字记录
   - 检查数据的结构化和程度
   - 评估数据的完整性和质量

2. **数据格式标准化**
   - 统一时间格式和日期表示
   - 标准化人员ID和命名规则
   - 处理编码和字符集问题

3. **数据导入和初步检查**
   ```python
   # 示例：不同格式数据的导入
   if data_format == 'excel':
       df = pd.read_excel(file_path)
   elif data_format == 'csv':
       df = pd.read_csv(file_path, encoding='utf-8')
   elif data_format == 'json':
       with open(file_path, 'r', encoding='utf-8') as f:
           data = json.load(f)
   ```

### 第二步：关系数据提取

1. **问卷关系提取**
   - 提取社会网络问卷中的关系提名
   - 处理关系强度评分
   - 识别关系类型（朋友、同事、家人等）

2. **访谈文本关系挖掘**
   ```python
   # 从访谈文本中提取关系
   def extract_relationships_from_text(text):
       # 使用正则表达式和关键词匹配
       relationship_patterns = [
           r'(\w+)\s*[和|与]\s*(\w+)\s*[是|为|有].*关系',
           r'(\w+)\s*[认识|了解]\s*(\w+)',
           r'(\w+)\s*[向|对]\s*(\w+)\s*[寻求|请求].*帮助'
       ]

       relationships = []
       for pattern in relationship_patterns:
           matches = re.findall(pattern, text)
           relationships.extend(matches)

       return relationships
   ```

3. **观察数据关系编码**
   - 编码观察到的互动行为
   - 记录互动频率和强度
   - 识别互动模式

4. **数字数据关系挖掘**
   - 解析社交媒体关注关系
   - 分析通信频率和模式
   - 提取网络交互特征

### 第三步：网络矩阵构建

1. **确定节点列表**
   ```python
   # 构建完整的节点列表
   def create_node_list(relationship_data):
       nodes = set()
       for rel in relationship_data:
           nodes.add(rel['source'])
           nodes.add(rel['target'])
       return sorted(list(nodes))
   ```

2. **构建邻接矩阵**
   ```python
   # 构建邻接矩阵
   def build_adjacency_matrix(nodes, relationships, weighted=False):
       n = len(nodes)
       adjacency_matrix = np.zeros((n, n))

       node_index = {node: i for i, node in enumerate(nodes)}

       for rel in relationships:
           i = node_index[rel['source']]
           j = node_index[rel['target']]

           if weighted:
               adjacency_matrix[i][j] = rel.get('weight', 1)
           else:
               adjacency_matrix[i][j] = 1
               if not rel.get('directed', False):
                   adjacency_matrix[j][i] = 1

       return adjacency_matrix
   ```

3. **处理特殊网络类型**
   - **有向网络**：区分关系的方向性
   - **加权网络**：考虑关系强度
   - **多值网络**：处理多种关系类型
   - **动态网络**：考虑时间维度

### 第四步：数据清洗和验证

1. **缺失值处理**
   - 识别关系数据中的缺失值
   - 使用适当方法填补缺失关系
   - 记录缺失值处理过程

2. **异常值检测**
   ```python
   # 异常关系检测
   def detect_outlier_relationships(adjacency_matrix, threshold=3):
       degrees = np.sum(adjacency_matrix, axis=1)
       mean_degree = np.mean(degrees)
       std_degree = np.std(degrees)

       outliers = []
       for i, degree in enumerate(degrees):
           if abs(degree - mean_degree) > threshold * std_degree:
               outliers.append(i)

       return outliers
   ```

3. **数据一致性检查**
   - 验证关系的对等性（双向关系）
   - 检查数据逻辑一致性
   - 识别和处理矛盾数据

4. **质量评估指标**
   - 数据完整度：有效数据的比例
   - 一致性得分：数据内部一致程度
   - 可靠性评估：数据可信度

### 第五步：属性数据整合

1. **节点属性整合**
   - 合并多个来源的节点属性
   - 处理属性数据的缺失和冲突
   - 标准化属性数据格式

2. **边属性处理**
   - 处理关系强度、频率等边属性
   - 标准化不同类型的关系属性
   - 创建多维度关系特征

3. **时间属性编码**
   - 处理关系的开始和结束时间
   - 计算关系持续时间
   - 分析关系的时间模式

## 输出格式要求

### 标准网络数据文件
- **节点列表**：包含所有节点及其属性
- **边列表**：包含所有关系及其属性
- **邻接矩阵**：标准格式的连接矩阵
- **元数据文件**：数据处理过程的详细记录

### 数据质量报告
- **数据来源说明**
- **处理步骤记录**
- **质量评估结果**
- **局限性说明**

### 可视化预览
- **网络结构概览**
- **节点属性分布**
- **关系强度分布**
- **数据质量指标图**

## 质量控制标准

### 数据完整性检查
- [ ] 所有关键节点都包含在数据中
- [ ] 关系数据覆盖充分
- [ ] 属性数据完整
- [ ] 时间信息准确

### 数据一致性验证
- [ ] 关系方向性正确
- [ ] 权重数值合理
- [ ] 属性数据逻辑一致
- [ ] 编码标准统一

### 处理过程质量
- [ ] 数据转换步骤清晰
- [ ] 缺失值处理合理
- [ ] 异常值处理恰当
- [ ] 记录详细完整

### 中文语境适配
- [ ] 中文名称处理正确
- [ ] 中文关系类型识别准确
- [ ] 文化背景考虑充分
- [ ] 术语使用规范

## 常见问题处理

**问题：问卷数据格式不统一**
- 解决：设计标准化的数据清洗流程
- 方法：创建灵活的数据解析规则

**问题：访谈文本关系识别困难**
- 解决：结合自然语言处理技术
- 策略：使用关键词匹配和机器学习方法

**问题：数据质量参差不齐**
- 解决：建立多层次的质量控制体系
- 技术：自动化检测 + 人工验证

**问题：多源数据整合困难**
- 解决：设计统一的数据模型
- 方法：使用标准化的数据交换格式

## 技术工具推荐

### 数据处理库
- **Pandas**：数据处理和分析
- **NumPy**：数值计算
- **OpenRefine**：数据清洗工具
- **NLTK/jieba**：中文文本处理

### 网络分析库
- **NetworkX**：网络数据结构
- **igraph**：高性能网络分析
- **graph-tool**：大规模网络分析

### 可视化工具
- **Matplotlib**：基础绘图
- **Seaborn**：统计可视化
- **Plotly**：交互式可视化

## 完成标准

高质量的网络数据处理应该：
1. 生成标准化的网络数据文件
2. 提供详细的数据处理记录
3. 确保数据的准确性和一致性
4. 包含完整的数据质量评估报告

---

*此技能为中文社会科学网络研究提供全面的数据处理支持，确保从原始数据到标准化网络文件的准确转换。*