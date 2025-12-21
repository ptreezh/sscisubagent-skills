/**
 * ANT Translation Skill - 行动者网络转译技能主入口
 * 遵循单一职责原则：只负责整合和协调四个转译环节的分析器
 * 实现完整的ANT转译过程分析
 */

const ProblematizationAnalyzer = require('./analyzers/ProblematizationAnalyzer');
const InteressementAnalyzer = require('./analyzers/InteressementAnalyzer');
const EnrollmentAnalyzer = require('./analyzers/EnrollmentAnalyzer');
const MobilizationAnalyzer = require('./analyzers/MobilizationAnalyzer');
const TranslationSynthesizer = require('./synthesizers/TranslationSynthesizer');
const OutputFormatter = require('../utils/OutputFormatter');

class TranslationSkill {
  constructor(dependencies = {}) {
    // 依赖注入，遵循DIP原则
    this.problematizationAnalyzer = dependencies.problematizationAnalyzer ||
      new ProblematizationAnalyzer();
    this.interessementAnalyzer = dependencies.interessementAnalyzer ||
      new InteressementAnalyzer(dependencies);
    this.enrollmentAnalyzer = dependencies.enrollmentAnalyzer ||
      new EnrollmentAnalyzer(dependencies);
    this.mobilizationAnalyzer = dependencies.mobilizationAnalyzer ||
      new MobilizationAnalyzer(dependencies);
    this.synthesizer = dependencies.synthesizer ||
      new TranslationSynthesizer();
    this.formatter = dependencies.formatter ||
      new OutputFormatter();
  }

  /**
   * 执行完整的ANT转译分析
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 完整的转译分析结果
   */
  async analyze(text, options = {}) {
    // 参数验证
    if (!text || typeof text !== 'string') {
      throw new Error('输入文本不能为空且必须是字符串');
    }

    // 分析选项设置
    const analysisOptions = {
      language: 'zh-CN',
      depth: 'medium', // quick, medium, deep
      includeChineseContext: true,
      validateTheory: true,
      ...options
    };

    try {
      // 第一步：问题化分析 (Problematization)
      const problematizationResult = this.problematizationAnalyzer.analyze(text, analysisOptions);

      // 第二步：兴趣化分析 (Interessement)
      const interessementResult = this.interessementAnalyzer.analyze(text, analysisOptions);

      // 第三步：招募分析 (Enrollment)
      const enrollmentResult = this.enrollmentAnalyzer.analyze(text, analysisOptions);

      // 第四步：动员分析 (Mobilization)
      const mobilizationResult = this.mobilizationAnalyzer.analyze(text, analysisOptions);

      // 第五步：综合分析
      const synthesisResult = await this.synthesizer.synthesize({
        problematization: problematizationResult,
        interessement: interessementResult,
        enrollment: enrollmentResult,
        mobilization: mobilizationResult
      }, analysisOptions);

      // 第六步：格式化输出
      const formattedResult = this.formatter.format(synthesisResult, analysisOptions);

      return formattedResult;

    } catch (error) {
      console.error('ANT转译分析过程中发生错误:', error);
      return {
        error: error.message,
        success: false,
        partialResults: this._getPartialResults(text, analysisOptions)
      };
    }
  }

  /**
   * 快速分析 - 只分析核心要素
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 快速分析结果
   */
  async quickAnalyze(text, options = {}) {
    return this.analyze(text, {
      ...options,
      depth: 'quick',
      validateTheory: false
    });
  }

  /**
   * 深度分析 - 包含所有理论细节
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 深度分析结果
   */
  async deepAnalyze(text, options = {}) {
    return this.analyze(text, {
      ...options,
      depth: 'deep',
      validateTheory: true,
      includeChineseContext: true
    });
  }

  /**
   * 单独分析问题化环节
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 问题化分析结果
   */
  async analyzeProblematization(text, options = {}) {
    return this.problematizationAnalyzer.analyze(text, options);
  }

  /**
   * 单独分析兴趣化环节
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 兴趣化分析结果
   */
  async analyzeInteressement(text, options = {}) {
    return this.interessementAnalyzer.analyze(text, options);
  }

  /**
   * 单独分析招募环节
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 招募分析结果
   */
  async analyzeEnrollment(text, options = {}) {
    return this.enrollmentAnalyzer.analyze(text, options);
  }

  /**
   * 单独分析动员环节
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 动员分析结果
   */
  async analyzeMobilization(text, options = {}) {
    return this.mobilizationAnalyzer.analyze(text, options);
  }

  /**
   * 验证分析结果的理论一致性
   * @param {Object} analysisResult - 分析结果
   * @returns {Object} 验证结果
   */
  validateTheoreticalConsistency(analysisResult) {
    const validationResults = {
      problematization: this.problematizationAnalyzer.validateTheoryApplication(
        analysisResult.problematization || {}
      ),
      interessement: this.interessementAnalyzer.validateTheoryApplication(
        analysisResult.interessement || {}
      ),
      enrollment: this.enrollmentAnalyzer.validateTheoryApplication(
        analysisResult.enrollment || {}
      ),
      mobilization: this.mobilizationAnalyzer.validateTheoryApplication(
        analysisResult.mobilization || {}
      )
    };

    const overallConsistency = Object.values(validationResults).every(valid => valid);
    const consistencyScore = Object.values(validationResults).filter(valid => valid).length / 4;

    return {
      validationResults,
      overallConsistency,
      consistencyScore,
      recommendations: this._generateValidationRecommendations(validationResults)
    };
  }

  /**
   * 获取分析指标
   * @param {Object} analysisResult - 分析结果
   * @returns {Object} 分析指标
   */
  getMetrics(analysisResult) {
    const metrics = {
      problematization: this.problematizationAnalyzer.getMetrics(
        analysisResult.problematization || {}
      ),
      interessement: this.interessementAnalyzer.getMetrics(
        analysisResult.interessement || {}
      ),
      enrollment: this.enrollmentAnalyzer.getMetrics(
        analysisResult.enrollment || {}
      ),
      mobilization: this.mobilizationAnalyzer.getMetrics(
        analysisResult.mobilization || {}
      )
    };

    return {
      ...metrics,
      overall: this._calculateOverallMetrics(metrics)
    };
  }

  /**
   * 获取技能信息
   * @returns {Object} 技能信息
   */
  getSkillInfo() {
    return {
      name: 'ANT Translation Skill',
      version: '1.0.0',
      description: '行动者网络理论转译过程分析技能',
      capabilities: [
        '问题化分析 (Problematization)',
        '兴趣化分析 (Interessement)',
        '招募分析 (Enrollment)',
        '动员分析 (Mobilization)',
        '综合转译分析',
        '中文本土化适配'
      ],
      supportedLanguages: ['zh-CN', 'en-US'],
      outputFormats: ['quick', 'medium', 'deep'],
      theoreticalFramework: 'Actor-Network Theory (ANT)',
      chineseLocalization: true,
      validationLevel: 'comprehensive'
    };
  }

  /**
   * 获取分析状态
   * @param {string} analysisId - 分析ID
   * @returns {Object} 分析状态
   */
  getAnalysisStatus(analysisId) {
    // 这里可以实现分析进度跟踪
    return {
      id: analysisId,
      status: 'completed',
      progress: 100,
      startedAt: new Date().toISOString(),
      completedAt: new Date().toISOString()
    };
  }

  /**
   * 取消分析
   * @param {string} analysisId - 分析ID
   * @returns {boolean} 是否成功取消
   */
  cancelAnalysis(analysisId) {
    // 这里可以实现分析取消逻辑
    return true;
  }

  // 私有辅助方法

  /**
   * 获取部分分析结果
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 部分分析结果
   * @private
   */
  _getPartialResults(text, options) {
    try {
      return {
        problematization: this.problematizationAnalyzer.analyze(text, options),
        basicInfo: {
          textLength: text.length,
          language: options.language || 'zh-CN',
          timestamp: new Date().toISOString()
        }
      };
    } catch (error) {
      return {
        error: error.message
      };
    }
  }

  /**
   * 生成验证建议
   * @param {Object} validationResults - 验证结果
   * @returns {Array} 建议列表
   * @private
   */
  _generateValidationRecommendations(validationResults) {
    const recommendations = [];

    Object.entries(validationResults).forEach(([phase, isValid]) => {
      if (!isValid) {
        switch (phase) {
          case 'problematization':
            recommendations.push('加强问题定义的清晰度和完整性');
            break;
          case 'interessement':
            recommendations.push('完善利益对齐机制的说服装置');
            break;
          case 'enrollment':
            recommendations.push('优化招募策略的有效性');
            break;
          case 'mobilization':
            recommendations.push('强化动员机制的网络稳定性');
            break;
        }
      }
    });

    if (recommendations.length === 0) {
      recommendations.push('分析结果完全符合ANT理论要求');
    }

    return recommendations;
  }

  /**
   * 计算总体指标
   * @param {Object} metrics - 各环节指标
   * @returns {Object} 总体指标
   * @private
   */
  _calculateOverallMetrics(metrics) {
    const calculateAverage = (key) => {
      const values = Object.values(metrics).map(phaseMetrics => {
        const relevantMetrics = phaseMetrics.antTheoryCompliance ||
                             phaseMetrics.effectivenessMetrics ||
                             phaseMetrics.mobilizationMetrics;
        return relevantMetrics?.[key] || 0;
      });
      return values.length > 0 ? (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2) : 0;
    };

    return {
      averageEffectiveness: calculateAverage('overallScore') || calculateAverage('overallEffectiveness'),
      averageCompleteness: calculateAverage('completenessLevel') || calculateAverage('completionRate'),
      theoreticalConsistency: calculateAverage('score') || calculateAverage('overallScore'),
      chineseAdaptationLevel: this._assessChineseAdaptation(metrics),
      analysisQuality: this._assessAnalysisQuality(metrics)
    };
  }

  /**
   * 评估中文适配水平
   * @param {Object} metrics - 指标
   * @returns {string} 适配水平
   * @private
   */
  _assessChineseAdaptation(metrics) {
    const chineseAdaptations = Object.values(metrics).map(phaseMetrics => {
      return phaseMetrics.chinesePatterns?.chineseCulturalFeatures?.length > 0 ||
             phaseMetrics.chinesePatterns?.chineseCulturalFeatures?.length > 0;
    }).filter(Boolean).length;

    const adaptationRate = chineseAdaptations / 4;
    if (adaptationRate >= 0.75) return 'high';
    if (adaptationRate >= 0.5) return 'medium';
    return 'low';
  }

  /**
   * 评估分析质量
   * @param {Object} metrics - 指标
   * @returns {string} 分析质量
   * @private
   */
  _assessAnalysisQuality(metrics) {
    const qualityScores = Object.values(metrics).map(phaseMetrics => {
      return parseFloat(phaseMetrics.antTheoryCompliance?.score || 0) ||
             parseFloat(phaseMetrics.effectivenessMetrics?.overallEffectiveness || 0);
    });

    const averageQuality = qualityScores.reduce((sum, score) => sum + score, 0) / qualityScores.length;

    if (averageQuality >= 0.8) return 'excellent';
    if (averageQuality >= 0.6) return 'good';
    if (averageQuality >= 0.4) return 'fair';
    return 'poor';
  }
}

module.exports = TranslationSkill;