/**
 * IANTTheory - ANT理论核心接口
 * 定义行动者网络理论的抽象概念和操作
 */

/**
 * ANT理论核心接口
 */
class IANTTheory {
  /**
   * 执行ANT理论分析
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 理论分析结果
   */
  analyze(text, options = {}) {
    throw new Error('Method must be implemented');
  }

  /**
   * 验证理论应用是否符合ANT原则
   * @param {Object} result - 分析结果
   * @returns {boolean} 是否符合理论
   */
  validateTheoryApplication(result) {
    throw new Error('Method must be implemented');
  }

  /**
   * 获取理论分析指标
   * @param {Object} data - 分析数据
   * @returns {Object} 指标对象
   */
  getMetrics(data) {
    throw new Error('Method must be implemented');
  }
}

/**
 * 转译环节接口 - 遵循接口隔离原则
 */
class ITranslationPhase extends IANTTheory {
  /**
   * 获取转译阶段类型
   * @returns {string} 阶段类型
   */
  getPhaseType() {
    throw new Error('Method must be implemented');
  }

  /**
   * 验证转译逻辑
   * @param {Object} data - 转译数据
   * @returns {Object} 验证结果
   */
  validateTranslation(data) {
    throw new Error('Method must be implemented');
  }
}

/**
 * 问题化定义接口
 */
class IProblemDefinition {
  /**
   * 定义问题
   * @param {string} text - 输入文本
   * @returns {Array} 问题定义列表
   */
  defineProblems(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 识别必经节点
   * @param {string} text - 输入文本
   * @returns {Array} 必经节点列表
   */
  identifyObligatoryPassagePoints(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 定义争议框架
   * @param {string} text - 输入文本
   * @returns {Object} 争议框架
   */
  defineControversy(text) {
    throw new Error('Method must be implemented');
  }
}

/**
 * 兴趣对齐接口
 */
class IInterestAlignment {
  /**
   * 分析利益对齐机制
   * @param {string} text - 输入文本
   * @returns {Object} 利益对齐分析
   */
  analyzeAlignment(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 识别说服装置
   * @param {string} text - 输入文本
   * @returns {Array} 说服装置列表
   */
  identifyPersuasiveDevices(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 消除替代方案
   * @param {string} text - 输入文本
   * @returns {Array} 消除策略
   */
  eliminateAlternatives(text) {
    throw new Error('Method must be implemented');
  }
}

/**
 * 参与者招募接口
 */
class IActorEnrollment {
  /**
   * 分析招募策略
   * @param {string} text - 输入文本
   * @returns {Object} 招募策略分析
   */
  analyzeEnrollmentStrategies(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 追踪招募过程
   * @param {string} text - 输入文本
   * @returns {Array} 招募记录
   */
  trackEnrollmentProcess(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 评估招募效果
   * @param {Object} enrollmentData - 招募数据
   * @returns {Object} 效果评估
   */
  assessEnrollmentEffectiveness(enrollmentData) {
    throw new Error('Method must be implemented');
  }
}

/**
 * 网络动员接口
 */
class INetworkMobilization {
  /**
   * 分析动员机制
   * @param {string} text - 输入文本
   * @returns {Object} 动员机制分析
   */
  analyzeMobilizationMechanisms(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 评估网络稳定性
   * @param {Object} networkData - 网络数据
   * @returns {Object} 稳定性评估
   */
  assessNetworkStability(networkData) {
    throw new Error('Method must be implemented');
  }

  /**
   * 识别黑箱形成
   * @param {string} text - 输入文本
   * @returns {Array} 黑箱列表
   */
  identifyBlackBoxFormation(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 分析权力效应
   * @param {Object} mobilizationData - 动员数据
   * @returns {Object} 权力效应分析
   */
  analyzePowerEffects(mobilizationData) {
    throw new Error('Method must be implemented');
  }
}

/**
 * 中文本土化适配接口
 */
class IChineseAdapter {
  /**
   * 适配中文语境
   * @param {Object} westernConcepts - 西方概念
   * @returns {Object} 中文适配结果
   */
  adaptChineseContext(westernConcepts) {
    throw new Error('Method must be implemented');
  }

  /**
   * 识别本土特征
   * @param {string} text - 中文文本
   * @returns {Object} 本土特征
   */
  identifyChineseFeatures(text) {
    throw new Error('Method must be implemented');
  }

  /**
   * 映射概念术语
   * @param {string} concept - 概念
   * @returns {string} 中文术语
   */
  mapConceptTerm(concept) {
    throw new Error('Method must be implemented');
  }
}

/**
 * 理论验证引擎接口
 */
class IValidationEngine {
  /**
   * 验证理论完整性
   * @param {Object} analysisResult - 分析结果
   * @returns {Object} 完整性验证
   */
  validateCompleteness(analysisResult) {
    throw new Error('Method must be implemented');
  }

  /**
   * 验证理论一致性
   * @param {Object} analysisResult - 分析结果
   * @returns {Object} 一致性验证
   */
  validateConsistency(analysisResult) {
    throw new Error('Method must be implemented');
  }

  /**
   * 验证理论准确性
   * @param {Object} analysisResult - 分析结果
   * @returns {Object} 准确性验证
   */
  validateAccuracy(analysisResult) {
    throw new Error('Method must be implemented');
  }
}

module.exports = {
  IANTTheory,
  ITranslationPhase,
  IProblemDefinition,
  IInterestAlignment,
  IActorEnrollment,
  INetworkMobilization,
  IChineseAdapter,
  IValidationEngine
};