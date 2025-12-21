# SSCI子智能体技能系统 - 详细实现文档

## 1. 技能分解详解

### 1.1 行动者网络理论 (ANT) 技能族

#### ant (基础ANT分析)
- **功能**: 提供行动者网络理论的基础分析框架
- **核心内容**:
  - 行动者识别与分类
  - 网络关系构建
  - 转译过程追踪
  - 网络动态分析
- **实现细节**:
  - 使用NetworkX构建网络图
  - 实现行动者重要性评估算法
  - 提供可视化分析工具

#### ant-participant-identification (参与者识别)
- **功能**: 识别行动者网络中的参与者
- **核心内容**:
  - 人类与非人类行动者识别
  - 行动者特征分析
  - 行动者角色确定
- **实现细节**:
  - 基于文本分析识别潜在行动者
  - 实现行动者分类算法
  - 提供行动者关系映射

#### ant-translation-process (转译过程分析)
- **功能**: 分析行动者网络中的转译过程
- **核心内容**:
  - 问题化阶段分析
  - 利益化阶段分析
  - 征召阶段分析
  - 动员阶段分析
- **实现细节**:
  - 实现四阶段识别算法
  - 提供转译过程可视化
  - 支持转译失败分析

#### ant-network-analysis (网络分析)
- **功能**: 分析行动者网络的结构与动态
- **核心内容**:
  - 网络拓扑分析
  - 关系强度评估
  - 中心性分析
  - 网络演化追踪
- **实现细节**:
  - 实现多种网络分析算法
  - 提供网络可视化工具
  - 支持动态网络分析

#### ant-power-analysis (权力关系分析)
- **功能**: 分析行动者网络中的权力关系
- **核心内容**:
  - 权力流动分析
  - 权力结构识别
  - 权力行使评估
  - 权力效果分析
- **实现细节**:
  - 实现权力关系量化算法
  - 提供权力网络可视化
  - 支持权力影响评估

### 1.2 场域分析 (Field Analysis) 技能族

#### field-analysis (基础场域分析)
- **功能**: 提供布迪厄场域分析的基础框架
- **核心内容**:
  - 场域边界识别
  - 资本分布分析
  - 自主性评估
  - 习性模式分析
- **实现细节**:
  - 基于布迪厄理论构建分析框架
  - 实现场域特征提取算法
  - 提供场域可视化工具

#### field-boundary-identification (边界识别)
- **功能**: 识别和分析社会场域的边界
- **核心内容**:
  - 场域范围确定
  - 边界机制分析
  - 排除机制评估
- **实现细节**:
  - 实现场域边界识别算法
  - 提供边界可视化工具
  - 支持边界稳定性分析

#### field-capital-analysis (资本分析)
- **功能**: 分析场域中的资本类型与分布
- **核心内容**:
  - 经济资本分析
  - 社会资本分析
  - 文化资本分析
  - 象征资本分析
- **实现细节**:
  - 实现多维资本量化算法
  - 提供资本分布可视化
  - 支持资本转换分析

#### field-habitus-analysis (习性分析)
- **功能**: 分析场域中的习性模式
- **核心内容**:
  - 行为倾向分析
  - 认知结构分析
  - 实践逻辑分析
- **实现细节**:
  - 实现习性模式识别算法
  - 提供习性可视化工具
  - 支持习性与场域关系分析

#### field-dynamics-analysis (动力学分析)
- **功能**: 分析场域的动力学过程
- **核心内容**:
  - 场域竞争分析
  - 权力关系变化
  - 资本转换过程
  - 场域演化趋势
- **实现细节**:
  - 实现场域动力学建模
  - 提供演化过程可视化
  - 支持趋势预测分析

### 1.3 扎根理论 (Grounded Theory) 技能族

#### performing-open-coding (开放编码)
- **功能**: 执行扎根理论的开放编码
- **核心内容**:
  - 概念识别
  - 初始编码
  - 持续比较
  - 备忘录撰写
- **实现细节**:
  - 实现自动化概念提取算法
  - 提供编码一致性检验
  - 支持多轮编码迭代

#### performing-axial-coding (轴心编码)
- **功能**: 执行扎根理论的轴心编码
- **核心内容**:
  - 范畴识别
  - 属性维度分析
  - 关系建立
  - Paradigm构建
- **实现细节**:
  - 实现范畴关联分析算法
  - 提供轴心编码可视化
  - 支持Paradigm模型构建

#### performing-selective-coding (选择式编码)
- **功能**: 执行扎根理论的选择式编码
- **核心内容**:
  - 核心范畴识别
  - 故事线构建
  - 理论框架整合
  - 理论饱和度检验
- **实现细节**:
  - 实现核心范畴提取算法
  - 提供理论框架可视化
  - 支持理论整合验证

#### checking-theory-saturation (理论饱和度检验)
- **功能**: 检验扎根理论的饱和度
- **核心内容**:
  - 新概念识别
  - 范畴完善度评估
  - 关系充分性检验
  - 理论完整性评估
- **实现细节**:
  - 实现饱和度量化算法
  - 提供饱和度可视化
  - 支持数据需求预测

#### writing-grounded-theory-memos (备忘录写作)
- **功能**: 撰写扎根理论备忘录
- **核心内容**:
  - 过程记录
  - 反思分析
  - 理论备忘录
  - 编码备忘录
- **实现细节**:
  - 实现备忘录模板系统
  - 提供写作辅助工具
  - 支持备忘录管理

### 1.4 社会网络分析 (SNA) 技能族

#### performing-centrality-analysis (中心性分析)
- **功能**: 执行社会网络中心性分析
- **核心内容**:
  - 度中心性计算
  - 接近中心性计算
  - 介数中心性计算
  - 特征向量中心性计算
- **实现细节**:
  - 实现多种中心性算法
  - 提供中心性可视化
  - 支持中心性比较分析

#### processing-network-data (网络数据处理)
- **功能**: 处理社会网络数据
- **核心内容**:
  - 关系数据收集
  - 矩阵构建
  - 数据清洗验证
  - 多模网络处理
- **实现细节**:
  - 实现数据格式转换工具
  - 提供数据质量检验
  - 支持多种网络格式

#### performing-network-computation (网络计算分析)
- **功能**: 执行社会网络计算分析
- **核心内容**:
  - 网络构建
  - 基础指标计算
  - 社区检测
  - 网络可视化
  - 高级网络分析
- **实现细节**:
  - 实现网络分析算法库
  - 提供可视化工具
  - 支持大规模网络分析

### 1.5 其他技能

#### conflict-resolution (冲突解决)
- **功能**: 研究分歧解决工具
- **核心内容**:
  - 理论分歧处理
  - 方法论分歧处理
  - 价值观分歧处理
  - 建设性对话策略
- **实现细节**:
  - 实现分歧识别算法
  - 提供对话策略推荐
  - 支持共识建立评估

#### dissent-resolution (分歧解决)
- **功能**: 处理学术研究中的不同观点
- **核心内容**:
  - 观点分析
  - 争议识别
  - 建设性对话
  - 共识达成
- **实现细节**:
  - 实现观点聚类算法
  - 提供对话引导工具
  - 支持共识度量

#### research-design (研究设计)
- **功能**: 为社会科学研究提供设计框架
- **核心内容**:
  - 研究问题构建
  - 方法选择
  - 数据收集策略
  - 数据分析策略
- **实现细节**:
  - 实现研究设计模板
  - 提供方法推荐系统
  - 支持设计评估

#### mathematical-statistics (数理统计)
- **功能**: 社会科学研究数理统计分析
- **核心内容**:
  - 描述性统计
  - 推断统计
  - 回归分析
  - 方差分析
  - 因子分析
- **实现细节**:
  - 实现统计分析算法库
  - 提供统计检验工具
  - 支持多种统计模型

#### validity-reliability (信度效度)
- **功能**: 研究信度效度分析
- **核心内容**:
  - 内部一致性分析
  - 重测信度分析
  - 评分者信度分析
  - 构念效度分析
  - 内容效度分析
  - 效标效度分析
- **实现细节**:
  - 实现信度效度计算算法
  - 提供评估报告生成
  - 支持多种量表分析

## 2. 智能体集成详解

### 2.1 ANT专家 (ant-expert)

#### 集成架构
- **核心组件**:
  - ANT理论知识库
  - 网络分析引擎
  - 转译过程追踪器
  - 权力关系分析器

#### 功能实现
- **参与者识别**: 自动识别网络中的行动者
- **关系构建**: 构建行动者间的关系网络
- **转译追踪**: 追踪问题化、利益化、征召、动员过程
- **权力分析**: 分析网络中的权力流动和结构

#### 技术实现
```python
class ANTExpert:
    def __init__(self):
        self.participant_identifier = ParticipantIdentifier()
        self.network_builder = NetworkBuilder()
        self.translation_tracker = TranslationTracker()
        self.power_analyzer = PowerAnalyzer()

    def analyze_network(self, data):
        participants = self.participant_identifier.identify(data)
        network = self.network_builder.build(participants)
        translation_process = self.translation_tracker.track(network)
        power_relations = self.power_analyzer.analyze(network)
        
        return {
            'participants': participants,
            'network': network,
            'translation_process': translation_process,
            'power_relations': power_relations
        }
```

### 2.2 场域分析专家 (field-analysis-expert)

#### 集成架构
- **核心组件**:
  - 场域边界识别器
  - 资本分析引擎
  - 习性分析器
  - 动力学建模器

#### 功能实现
- **边界识别**: 识别场域的范围和边界机制
- **资本分析**: 分析场域中的各类资本分布
- **习性分析**: 分析行动者的习性模式
- **动力学分析**: 分析场域的动态演化过程

#### 技术实现
```python
class FieldAnalysisExpert:
    def __init__(self):
        self.boundary_identifier = BoundaryIdentifier()
        self.capital_analyzer = CapitalAnalyzer()
        self.habitus_analyzer = HabitusAnalyzer()
        self.dynamics_modeler = DynamicsModeler()

    def analyze_field(self, data):
        boundaries = self.boundary_identifier.identify(data)
        capital_distribution = self.capital_analyzer.analyze(data)
        habitus_patterns = self.habitus_analyzer.analyze(data)
        dynamics = self.dynamics_modeler.model(data)
        
        return {
            'boundaries': boundaries,
            'capital_distribution': capital_distribution,
            'habitus_patterns': habitus_patterns,
            'dynamics': dynamics
        }
```

### 2.3 扎根理论专家 (grounded-theory-expert)

#### 集成架构
- **核心组件**:
  - 开放编码器
  - 轴心编码器
  - 选择式编码器
  - 饱和度检验器

#### 功能实现
- **开放编码**: 从数据中提取概念和初始编码
- **轴心编码**: 建立范畴和关系
- **选择式编码**: 构建理论框架
- **饱和度检验**: 检验理论完整性

#### 技术实现
```python
class GroundedTheoryExpert:
    def __init__(self):
        self.open_coder = OpenCoder()
        self.axial_coder = AxialCoder()
        self.selective_coder = SelectiveCoder()
        self.saturation_checker = SaturationChecker()

    def perform_analysis(self, data):
        open_codes = self.open_coder.code(data)
        axial_codes = self.axial_coder.code(open_codes)
        selective_codes = self.selective_coder.code(axial_codes)
        saturation_status = self.saturation_checker.check(selective_codes)
        
        return {
            'open_codes': open_codes,
            'axial_codes': axial_codes,
            'selective_codes': selective_codes,
            'saturation_status': saturation_status
        }
```

### 2.4 社会网络分析专家 (sna-expert)

#### 集成架构
- **核心组件**:
  - 网络构建器
  - 中心性分析器
  - 社区检测器
  - 可视化引擎

#### 功能实现
- **网络构建**: 从数据构建社会网络
- **中心性分析**: 计算节点的各种中心性指标
- **社区检测**: 识别网络中的社区结构
- **网络可视化**: 提供网络结构可视化

#### 技术实现
```python
class SNAExpert:
    def __init__(self):
        self.network_builder = NetworkBuilder()
        self.centrality_analyzer = CentralityAnalyzer()
        self.community_detector = CommunityDetector()
        self.visualizer = NetworkVisualizer()

    def analyze_network(self, data):
        network = self.network_builder.build(data)
        centralities = self.centrality_analyzer.analyze(network)
        communities = self.community_detector.detect(network)
        visualization = self.visualizer.create(network)
        
        return {
            'network': network,
            'centralities': centralities,
            'communities': communities,
            'visualization': visualization
        }
```

## 3. 依赖管理与降级机制详解

### 3.1 智能依赖管理器

#### 架构设计
```python
class SmartDependencyManager:
    def __init__(self):
        self.installed_packages = self.get_installed_packages()
        self.package_mapping = self.load_package_mapping()
    
    def get_installed_packages(self):
        # 获取当前已安装的包
        pass
    
    def load_package_mapping(self):
        # 加载高级包到降级包的映射
        return {
            'advanced_stats': {
                'primary': 'statsmodels',
                'fallback': 'scipy.stats'
            },
            'network_analysis': {
                'primary': 'networkx',
                'fallback': 'custom_implementation'
            }
        }
```

#### 依赖检测与安装
```python
def ensure_dependency(self, package_name):
    if package_name in self.installed_packages:
        return package_name
    
    # 尝试安装包
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return package_name
    except subprocess.CalledProcessError:
        # 安装失败，尝试降级包
        fallback_package = self.get_fallback_package(package_name)
        if fallback_package:
            return self.ensure_dependency(fallback_package)
        else:
            raise DependencyError(f"无法安装或降级依赖包: {package_name}")
```

### 3.2 优雅降级实现

#### 高级功能实现
- **优先使用高级包**:
  - statsmodels: 提供丰富的统计模型
  - NetworkX: 提供全面的网络分析功能
  - scikit-learn: 提供机器学习算法
  - pingouin: 提供高级统计检验

#### 降级机制
- **基础功能实现**:
  - 使用Python标准库实现核心功能
  - 使用numpy和pandas进行数据处理
  - 实现简化的算法替代高级功能

#### 自动切换机制
```python
class FeatureImplementation:
    def __init__(self):
        self.use_advanced = self.check_advanced_packages()
    
    def check_advanced_packages(self):
        try:
            import statsmodels
            import networkx
            return True
        except ImportError:
            return False
    
    def perform_analysis(self, data):
        if self.use_advanced:
            return self.advanced_analysis(data)
        else:
            return self.basic_analysis(data)
    
    def advanced_analysis(self, data):
        # 使用高级包实现
        pass
    
    def basic_analysis(self, data):
        # 使用基础方法实现
        pass
```

### 3.3 依赖配置详解

#### 配置文件结构
```python
# common/dependency_config.py
DEPENDENCY_GROUPS = {
    'basic': [
        'numpy',
        'pandas',
        'networkx'
    ],
    'statistics': [
        'statsmodels',
        'pingouin',
        'scipy'
    ],
    'psychometrics': [
        'factor-analyzer',
        'statsmodels',
        'pingouin'
    ],
    'network_extended': [
        'python-louvain',
        'igraph'
    ]
}

PACKAGE_MAPPING = {
    'statsmodels': {
        'fallback': 'scipy.stats',
        'features': ['regression', 'hypothesis_testing']
    },
    'factor-analyzer': {
        'fallback': 'custom_factor_analysis',
        'features': ['factor_analysis', 'reliability']
    }
}
```

## 4. 代码质量与规范详解

### 4.1 符合agentskills.io规范

#### YAML前言标准
```yaml
---
name: skill-name                    # 1-64字符，小写字母、数字、连字符
description: 功能描述和使用时机      # 1-1024字符，包含关键词
license: MIT
compatibility: 系统要求
metadata:
  domain: 专业领域
  methodology: 核心方法
  complexity: 复杂度级别
  version: 版本号
  integration_type: integration_type
  author: zhangshuren@hznu.edu.cn
  website: http://agentpsy.com
allowed-tools: 工具列表
---
```

#### 结构化格式
- **概述部分**: 技能的目的和意义
- **使用时机**: 明确的使用条件和触发场景
- **快速开始**: 最简单的使用方法
- **核心流程**: 详细的分步指导
- **输出格式**: 标准化的输出格式
- **质量标准**: 质量检查清单
- **深入学习**: 理论基础和实践案例
- **完成标志**: 明确的完成标准

### 4.2 代码质量标准

#### 模块化设计
- **单一职责原则**: 每个模块只负责一个功能
- **高内聚低耦合**: 模块内部高度相关，模块间低依赖
- **接口标准化**: 统一的输入输出接口

#### 错误处理
```python
def robust_function(data):
    try:
        # 核心功能实现
        result = core_processing(data)
        return {'status': 'success', 'result': result}
    except ValidationError as e:
        return {'status': 'error', 'message': f'数据验证失败: {str(e)}'}
    except ProcessingError as e:
        return {'status': 'error', 'message': f'处理失败: {str(e)}'}
    except Exception as e:
        return {'status': 'error', 'message': f'未知错误: {str(e)}'}
```

#### 类型注解
```python
from typing import Dict, List, Optional, Union
import pandas as pd

def analyze_data(data: pd.DataFrame, 
                parameters: Dict[str, Union[str, int, float]]) -> Dict[str, Union[pd.DataFrame, float, str]]:
    """
    分析数据并返回结果
    
    Args:
        data: 输入数据
        parameters: 分析参数
        
    Returns:
        包含分析结果的字典
    """
    pass
```

## 5. 部署与使用详解

### 5.1 安装配置

#### 包管理器配置
```toml
# pyproject.toml
[project]
name = "ssci-subagent-skills"
version = "1.0.0"
description = "SSCI子智能体技能系统"
authors = [{name = "zhangshuren", email = "zhangshuren@hznu.edu.cn"}]

[project.optional-dependencies]
basic = ["numpy", "pandas", "networkx"]
statistics = ["statsmodels", "pingouin", "scipy"]
psychometrics = ["factor-analyzer", "pingouin"]
network_extended = ["python-louvain"]
all = ["ssci-subagent-skills[basic,statistics,psychometrics,network_extended]"]

[tool.uv.sources]
# 配置国内镜像源加速下载
```

#### 安装命令
```bash
# 基础功能安装
uv install ssci-subagent-skills

# 统计功能安装
uv install "ssci-subagent-skills[statistics]"

# 完整功能安装
uv install "ssci-subagent-skills[all]"
```

### 5.2 使用方式

#### 直接调用
```python
from skills.ant import ant_analysis
from skills.field_analysis import field_analysis

# 直接调用技能
result = ant_analysis(data, context)
result = field_analysis(data, context)
```

#### 智能体调用
```python
from experts.ant_expert import ANTExpert
from experts.field_analysis_expert import FieldAnalysisExpert

# 通过专业智能体调用
ant_expert = ANTExpert()
result = ant_expert.analyze_network(data)

field_expert = FieldAnalysisExpert()
result = field_expert.analyze_field(data)
```

## 6. 测试验证详解

### 6.1 单元测试
```python
import unittest
from skills.ant.participant_identification import ParticipantIdentifier

class TestParticipantIdentifier(unittest.TestCase):
    def setUp(self):
        self.identifier = ParticipantIdentifier()
    
    def test_identify_participants(self):
        # 测试参与者识别功能
        data = "测试数据"
        result = self.identifier.identify(data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
```

### 6.2 集成测试
```python
import unittest
from experts.ant_expert import ANTExpert

class TestANTExpertIntegration(unittest.TestCase):
    def setUp(self):
        self.expert = ANTExpert()
    
    def test_complete_analysis(self):
        # 测试完整的分析流程
        data = "完整的测试数据"
        result = self.expert.analyze_network(data)
        
        # 验证结果完整性
        self.assertIn('participants', result)
        self.assertIn('network', result)
        self.assertIn('translation_process', result)
        self.assertIn('power_relations', result)
```

### 6.3 端到端测试
```python
import unittest
from ssci_skills_system import SS CISkillsSystem

class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.system = SS CISkillsSystem()
    
    def test_user_scenario(self):
        # 模拟真实用户使用场景
        user_input = "用户的具体分析请求"
        result = self.system.process_request(user_input)
        
        # 验证结果质量和完整性
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
```

## 7. 性能优化详解

### 7.1 缓存机制
```python
from functools import lru_cache
import hashlib

class CachedAnalyzer:
    @lru_cache(maxsize=128)
    def analyze_with_cache(self, data_hash: str, params: tuple):
        # 使用数据哈希和参数作为缓存键
        data = self.retrieve_data(data_hash)
        return self.perform_analysis(data, params)
    
    def get_data_hash(self, data):
        # 生成数据哈希
        return hashlib.md5(str(data).encode()).hexdigest()
```

### 7.2 并行处理
```python
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp

class ParallelAnalyzer:
    def __init__(self):
        self.max_workers = mp.cpu_count()
    
    def analyze_in_parallel(self, data_list, analysis_func):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(analysis_func, data_list))
        return results
```

## 8. 安全与隐私详解

### 8.1 数据安全
- **数据加密**: 敏感数据在存储和传输过程中加密
- **访问控制**: 限制对敏感数据的访问权限
- **审计日志**: 记录数据访问和处理活动

### 8.2 隐私保护
- **数据脱敏**: 在分析前对个人身份信息进行脱敏
- **最小化原则**: 仅收集和处理必需的数据
- **用户同意**: 确保数据处理符合用户同意

## 9. 维护与更新详解

### 9.1 版本管理
- **语义化版本**: 遵循SemVer标准
- **向后兼容**: 确保新版本向后兼容
- **迁移指南**: 提供版本升级指南

### 9.2 持续集成
- **自动化测试**: 每次提交自动运行测试
- **代码质量检查**: 自动检查代码质量
- **部署自动化**: 自动部署到测试和生产环境