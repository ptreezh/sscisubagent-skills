/**
 * ProblematizationAnalyzer - 问题化分析器
 * 遵循单一职责原则：只负责ANT转译过程的第一个环节分析
 * 完整实现布迪厄的问题化理论
 */

const IANTTheory = require('../../../shared/interfaces/IANTTheory');
const { ProblematizationType } = require('../../../shared/types/TranslationTypes');

class ProblematizationAnalyzer extends IANTTheory {
  constructor() {
    super();

    // 问题化识别模式
    this.problemPatterns = [
      // 问题定义模式
      {
        type: ProblematizationType.PROBLEM_DEFINITION,
        pattern: /([^。，]*(?:问题|挑战|困境|困难|危机)[^。，]*(?:需要|必须|应该|亟待)[^。，]*)/g,
        severityWeights: {
          '危机': 1.0,
          '困境': 0.8,
          '挑战': 0.6,
          '问题': 0.5,
          '困难': 0.4
        }
      },
      // 解决方案模式
      {
        type: ProblematizationType.SOLUTION_PROPOSAL,
        pattern: /([^。，]*(?:解决|处理|应对|克服)[^。，]*(?:问题|挑战|困境)[^。，]*(?:的)?([^。，]*方案|办法|措施|路径)[^。，]*)/g,
        feasibilityIndicators: [
          '可行性',
          '成本效益',
          '可操作性',
          '可持续性'
        ]
      },
      // 必经节点模式
      {
        type: ProblematizationType.OBLIGATORY_PASSAGE,
        pattern: /([^。，]*必须通过[^。，]*([^(，。]*)(?:审批|许可|认证|标准)[^。，]*)/g,
        controlKeywords: [
          '审批权',
          '决定权',
          '控制权',
          '监督权'
        ]
      }
    ];

    // 争议识别关键词
    this.controversyKeywords = {
      conflict: ['冲突', '矛盾', '对立', '争议', '分歧'],
      stakeholders: ['支持', '反对', '担忧', '质疑', '主张'],
      values: ['利益', '价值', '原则', '标准', '理念']
    };
  }

  /**
   * 分析问题化过程 - 实现IANTTheory接口
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 问题化分析结果
   */
  analyze(text, options = {}) {
    const problematization = {
      problems: this.identifyProblems(text),
      solutions: this.identifySolutions(text),
      obligatoryPassagePoints: this.identifyObligatoryPassagePoints(text),
      controversyDefinition: this.defineControversy(text),
      legitimacySources: this.identifyLegitimacySources(text),
      problemComplexity: this.analyzeComplexity(text)
    };

    return this.validateTheoryApplication(problematization) ?
      this.synthesizeAnalysis(problematization) :
      this.getDefaultProblematization();
  }

  /**
   * 识别问题定义
   * @param {string} text - 输入文本
   * @returns {Array} 问题列表
   */
  identifyProblems(text) {
    const problems = [];

    this.problemPatterns
      .filter(pattern => pattern.type === ProblematizationType.PROBLEM_DEFINITION)
      .forEach(pattern => {
        let match;
        while ((match = pattern.pattern.exec(text)) !== null) {
          const problem = {
            type: pattern.type,
            description: match[1].trim(),
            severity: this._calculateSeverity(match[1], pattern.severityWeights),
            urgency: this._assessUrgency(match[1]),
            stakeholders: this._identifyStakeholders(match[1]),
            scope: this._assessScope(match[1]),
            timestamp: new Date().toISOString()
          };

          problems.push(problem);
        }
      });

    return this._deduplicateProblems(problems);
  }

  /**
   * 识别解决方案
   * @param {string} text - 输入文本
   * @returns {Array} 解决方案列表
   */
  identifySolutions(text) {
    const solutions = [];

    this.problemPatterns
      .filter(pattern => pattern.type === ProblematizationType.SOLUTION_PROPOSAL)
      .forEach(pattern => {
        let match;
        while ((match = pattern.pattern.exec(text)) !== null) {
          const solution = {
            type: pattern.type,
            description: match[2] ? match[2].trim() : match[1].trim(),
            feasibility: this._assessFeasibility(match[1], pattern.feasibilityIndicators),
            barriers: this._identifyBarriers(match[1]),
            resources: this._identifyRequiredResources(match[1]),
            timeframe: this._assessTimeframe(match[1])
          };

          solutions.push(solution);
        }
      });

    return solutions;
  }

  /**
   * 识别必经节点
   * @param {string} text - 输入文本
   * @returns {Array} 必经节点列表
   */
  identifyObligatoryPassagePoints(text) {
    const passagePoints = [];

    this.problemPatterns
      .filter(pattern => pattern.type === ProblematizationType.OBLIGATORY_PASSAGE)
      .forEach(pattern => {
        let match;
        while ((match = pattern.pattern.exec(text)) !== null) {
          const passagePoint = {
            name: match[2] || match[1],
            description: match[1].trim(),
            necessity: 'critical',
            controlLevel: this._assessControlLevel(match[1], pattern.controlKeywords),
            bypassOptions: this._identifyBypassOptions(match[1]),
            enforcementMechanism: this._identifyEnforcement(match[1])
          };

          passagePoints.push(passagePoint);
        }
      });

    return passagePoints;
  }

  /**
   * 定义争议
   * @param {string} text - 输入文本
   * @returns {string} 争议定义
   */
  defineControversy(text) {
    const conflictIndicators = this._extractConflictIndicators(text);
    const stakeholderPositions = this._extractStakeholderPositions(text);
    const valueConflicts = this._extractValueConflicts(text);

    if (conflictIndicators.length === 0) {
      return '无明显争议';
    }

    return this._synthesizeControversy(conflictIndicators, stakeholderPositions, valueConflicts);
  }

  /**
   * 识别合法性来源
   * @param {string} text - 输入文本
   * @returns {Array} 合法性来源列表
   */
  identifyLegitimacySources(text) {
    const legitimacyPatterns = [
      {
        type: 'legal',
        keywords: ['法规', '法律', '政策', '制度'],
        pattern: /([^。，]*(?:法规|法律|政策|制度)[^。，]*[^。，]*)/g
      },
      {
        type: 'expertise',
        keywords: ['专家', '学者', '科研', '学术'],
        pattern: /([^。，]*(?:专家|学者|科研|学术)[^。，]*[^。，]*)/g
      },
      {
        type: 'procedural',
        keywords: ['程序', '标准', '规范', '流程'],
        pattern: /([^。，]*(?:程序|标准|规范|流程)[^。，]*[^。，]*)/g
      },
      {
        type: 'political',
        keywords: ['政府', '部门', '官方', '权威'],
        pattern: /([^。，]*(?:政府|部门|官方|权威)[^。，]*[^。，]*)/g
      }
    ];

    const sources = [];

    legitimacyPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const source = {
          type: pattern.type,
          description: match[1].trim(),
          strength: this._assessLegitimacyStrength(match[1], pattern.keywords)
        };

        sources.push(source);
      }
    });

    return this._deduplicateLegitimacySources(sources);
  }

  /**
   * 分析问题复杂性
   * @param {string} text - 输入文本
   * @returns {Object} 复杂性分析结果
   */
  analyzeComplexity(text) {
    return {
      dimensions: this._identifyProblemDimensions(text),
      interconnectedness: this._assessInterconnectedness(text),
      uncertaintyLevel: this._assessUncertainty(text),
      stakeholderComplexity: this._analyzeStakeholderComplexity(text),
      complexityLevel: this._calculateOverallComplexity(text)
    };
  }

  /**
   * 验证理论应用 - 实现IANTTheory接口
   * @param {Object} result - 分析结果
   * @returns {boolean} 是否符合理论
   */
  validateTheoryApplication(result) {
    const requiredElements = [
      'problems',
      'solutions',
      'obligatoryPassagePoints'
    ];

    return requiredElements.every(element =>
      result[element] && Array.isArray(result[element])
    );
  }

  /**
   * 综合分析结果
   * @param {Object} problematization - 问题化分析
   * @returns {Object} 综合结果
   */
  synthesizeAnalysis(problematization) {
    return {
      ...problematization,
      analysisSummary: this._generateAnalysisSummary(problematization),
      theoreticalInsights: this._extractTheoreticalInsights(problematization),
      practicalImplications: this._identifyPracticalImplications(problematization)
    };
  }

  /**
   * 获取理论指标 - 实现IANTTheory接口
   * @param {Object} data - 分析数据
   * @returns {Object} 指标对象
   */
  getMetrics(data) {
    if (!this.validateTheoryApplication(data)) {
      throw new Error('数据不符合ANT问题化理论');
    }

    return {
      problematizationMetrics: {
        problemCount: data.problems.length,
        solutionCount: data.solutions.length,
        passagePointCount: data.obligatoryPassagePoints.length,
        averageSeverity: this._calculateAverageSeverity(data.problems),
        complexityScore: data.problemComplexity.complexityLevel
      },
      controversyMetrics: {
        hasControversy: data.controversyDefinition !== '无明显争议',
        legitimacySources: data.legitimacySources.length,
        conflictIntensity: this._assessConflictIntensity(data.controversyDefinition)
      },
      antTheoryCompliance: this._assessTheoryCompliance(data)
    };
  }

  // 私有辅助方法

  /**
   * 计算问题严重性
   * @private
   */
  _calculateSeverity(text, weights) {
    let severity = 0.5; // 基础严重性

    Object.entries(weights).forEach(([keyword, weight]) => {
      if (text.includes(keyword)) {
        severity = Math.max(severity, weight);
      }
    });

    return severity;
  }

  /**
   * 评估紧急性
   * @private
   */
  _assessUrgency(text) {
    const urgencyKeywords = ['紧急', '亟待', '立即', '马上', '必须'];
    let urgency = 0.3;

    urgencyKeywords.forEach(keyword => {
      if (text.includes(keyword)) {
        urgency += 0.2;
      }
    });

    return Math.min(1, urgency);
  }

  /**
   * 识别利益相关者
   * @private
   */
  _identifyStakeholders(text) {
    const stakeholders = [];

    const stakeholderPatterns = [
      { pattern: /([^，。]*(?:政府|部门|机构)[^，。]*)/g, type: 'government' },
      { pattern: /([^，。]*(?:企业|公司|厂商)[^，。]*)/g, type: 'enterprise' },
      { pattern: /([^，。]*(?:公众|民众|公民)[^，。]*)/g, type: 'public' },
      { pattern: /([^，。]*(?:专家|学者|研究者)[^，。]*)/g, type: 'expert' }
    ];

    stakeholderPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        stakeholders.push({
          name: match[1].trim(),
          type: pattern.type
        });
      }
    });

    return stakeholders;
  }

  /**
   * 评估范围
   * @private
   */
  _assessScope(text) {
    if (text.includes('全球') || text.includes('国际')) return 'global';
    if (text.includes('国家') || text.includes('全国')) return 'national';
    if (text.includes('区域') || text.includes('地方')) return 'regional';
    return 'local';
  }

  /**
   * 评估可行性
   * @private
   */
  _assessFeasibility(text, indicators) {
    let feasibility = 0.5;

    indicators.forEach(indicator => {
      if (text.includes(indicator)) {
        feasibility += 0.1;
      }
    });

    const positiveIndicators = ['可行', '有效', '成功', '优化'];
    const negativeIndicators = ['困难', '挑战', '风险', '障碍'];

    positiveIndicators.forEach(indicator => {
      if (text.includes(indicator)) feasibility += 0.1;
    });

    negativeIndicators.forEach(indicator => {
      if (text.includes(indicator)) feasibility -= 0.1;
    });

    return Math.max(0, Math.min(1, feasibility));
  }

  /**
   * 获取默认问题化结果
   * @private
   */
  getDefaultProblematization() {
    return {
      problems: [],
      solutions: [],
      obligatoryPassagePoints: [],
      controversyDefinition: '无明显争议',
      legitimacySources: [],
      problemComplexity: {
        dimensions: [],
        interconnectedness: 0,
        uncertaintyLevel: 'low',
        stakeholderComplexity: 'simple'
      },
      hasProblematization: false
    };
  }

  /**
   * 去重问题
   * @private
   */
  _deduplicateProblems(problems) {
    const seen = new Set();
    return problems.filter(problem => {
      const key = problem.description;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  /**
   * 去重合法性来源
   * @private
   */
  _deduplicateLegitimacySources(sources) {
    const seen = new Set();
    return sources.filter(source => {
      const key = `${source.type}_${source.description}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  /**
   * 生成分析摘要
   * @private
   */
  _generateAnalysisSummary(problematization) {
    return {
      totalProblems: problematization.problems.length,
      criticalProblems: problematization.problems.filter(p => p.severity > 0.7).length,
      hasControversy: problematization.controversyDefinition !== '无明显争议',
      hasObligatoryPoints: problematization.obligatoryPassagePoints.length > 0,
      completenessLevel: this._calculateCompleteness(problematization)
    };
  }

  /**
   * 提取理论洞察
   * @private
   */
  _extractTheoreticalInsights(problematization) {
    return {
      networkStabilization: problematization.obligatoryPassagePoints.length > 0,
      powerConstruction: problematization.legitimacySources.length > 0,
      controversyResolution: problematization.controversyDefinition !== '无明显争议',
      complexityLevel: problematization.problemComplexity.complexityLevel,
      theoreticalConsistency: this._checkTheoreticalConsistency(problematization)
    };
  }

  /**
   * 识别实践意义
   * @private
   */
  _identifyPracticalImplications(problematization) {
    return {
      policyRecommendations: problematization.solutions.length > 0,
      stakeholderActions: this._suggestStakeholderActions(problematization),
      implementationChallenges: this._identifyImplementationChallenges(problematization),
      successFactors: this._identifySuccessFactors(problematization)
    };
  }

  /**
   * 计算平均严重性
   * @private
   */
  _calculateAverageSeverity(problems) {
    if (problems.length === 0) return 0;

    const totalSeverity = problems.reduce((sum, problem) => sum + problem.severity, 0);
    return (totalSeverity / problems.length).toFixed(2);
  }

  /**
   * 计算理论合规性
   * @private
   */
  _assessTheoryCompliance(data) {
    const complianceScore = this._calculateTheoreticalConsistency(data);

    return {
      score: complianceScore,
      level: complianceScore > 0.8 ? 'high' :
             complianceScore > 0.6 ? 'medium' : 'low',
      recommendations: complianceScore < 0.7 ?
        ['增强问题定义的清晰度', '完善解决方案的可行性分析'] : []
    };
  }
}

module.exports = ProblematizationAnalyzer;