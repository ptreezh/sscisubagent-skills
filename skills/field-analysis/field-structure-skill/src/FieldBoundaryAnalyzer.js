/**
 * FieldBoundaryAnalyzer - 场域边界分析器
 * 遵循单一职责原则：只负责场域边界的识别和分析
 * 实现布迪厄场域理论的核心概念
 */

const IFieldAnalyzer = require('../../../shared/interfaces/IFieldAnalyzer');
const { FieldType, BoundaryType } = require('../../../shared/types/FieldTypes');

class FieldBoundaryAnalyzer extends IFieldAnalyzer {
  constructor() {
    super();

    // 场域边界识别模式
    this.boundaryPatterns = {
      // 内部边界模式
      internalBoundaries: [
        {
          type: BoundaryType.FORMAL,
          pattern: /([^。，]*(?:学科|专业|领域|院系|部门)[^。，]*(?:壁垒|界限|区别|差异)[^。，]*)/g,
          strength: 0.8
        },
        {
          type: BoundaryType.FORMAL,
          pattern: /([^。，]*(?:教授|副教授|讲师|助教)[^。，]*(?:与|和|同)[^。，]*(?:学生|研究生)[^。，]*)/g,
          strength: 0.9
        },
        {
          type: BoundaryType.INFORMAL,
          pattern: /([^。，]*(?:老|新)[^。，]*(?:教师|学者)[^。，]*(?:与|和)[^。，]*(?:青年|中年)[^。，]*教师[^。，]*)/g,
          strength: 0.7
        },
        {
          type: BoundaryType.FORMAL,
          pattern: /([^。，]*(?:学术委员会|评审委员会|理事会)[^。，]*(?:成员|非成员|核心|外围)[^。，]*)/g,
          strength: 0.8
        }
      ],

      // 外部边界模式
      externalBoundaries: [
        {
          source: '政府',
          type: BoundaryType.FORMAL,
          pattern: /([^。，]*(?:教育部|科技部|发改委|工信部)[^。，]*(?:指导|要求|规定|审批)[^。，]*)/g,
          strength: 0.9
        },
        {
          source: '市场',
          type: BoundaryType.INFORMAL,
          pattern: /([^。，]*(?:市场|企业|产业|商业化)[^。，]*(?:影响|要求|压力)[^。，]*)/g,
          strength: 0.7
        },
        {
          source: '社会',
          type: BoundaryType.INFORMAL,
          pattern: /([^。，]*(?:社会|公众|舆论)[^。，]*(?:期望|要求|监督)[^。，]*)/g,
          strength: 0.6
        },
        {
          source: '国际',
          type: BoundaryType.FORMAL,
          pattern: /([^。，]*(?:国际|国外|全球)[^。，]*(?:标准|评价|影响)[^。，]*)/g,
          strength: 0.7
        }
      ],

      // 边界控制机制模式
      controlMechanisms: [
        {
          mechanism: '准入控制',
          type: '资格审查',
          pattern: /([^。，]*(?:进入|获得)[^。，]*(?:需要|要求|必须)[^。，]*(?:考试|资格|认证)[^。，]*)/g,
          effectiveness: 0.8
        },
        {
          mechanism: '专业认证',
          type: '会员资格',
          pattern: /([^。，]*(?:专业|学术)[^。，]*(?:协会|学会)[^。，]*(?:会员|资格)[^。，]*)/g,
          effectiveness: 0.7
        },
        {
          mechanism: '知识壁垒',
          type: '专业要求',
          pattern: /([^。，]*(?:专业知识|技能)[^。，]*(?:要求|标准)[^。，]*)/g,
          effectiveness: 0.6
        },
        {
          mechanism: '资源控制',
          type: '资源分配',
          pattern: /([^。，]*(?:资源|经费)[^。，]*(?:分配|控制)[^。，]*(?:权|机制)[^。，]*)/g,
          effectiveness: 0.8
        }
      ]
    };

    // 渗透性评估关键词
    this.permeabilityKeywords = {
      high: ['开放', '融合', '合作', '交流', '互通', '跨学科', '国际化'],
      low: ['封闭', '独立', '自主', '隔离', '壁垒', '界限分明'],
      changing: ['越来越', '逐渐', '日益', '不断', '持续', '趋势']
    };
  }

  /**
   * 识别内部边界 - 实现IFieldAnalyzer接口
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Array} 内部边界数组
   */
  analyze(text, options = {}) {
    const boundaries = {
      internal: this.identifyInternalBoundaries(text),
      external: this.identifyExternalBoundaries(text),
      mechanisms: this.identifyBoundaryMechanisms(text),
      permeability: this.assessBoundaryPermeability(text)
    };

    return this.validateAnalysisResult(boundaries) ? boundaries : this.getDefaultResult();
  }

  /**
   * 识别内部边界
   * @param {string} text - 输入文本
   * @returns {Array} 内部边界数组
   */
  identifyInternalBoundaries(text) {
    const boundaries = [];

    this.boundaryPatterns.internalBoundaries.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const boundary = {
          type: pattern.type,
          description: match[1].trim(),
          strength: pattern.strength,
          permeability: this._estimatePermeability(match[1])
        };

        boundaries.push(boundary);
      }
    });

    // 去重并按强度排序
    return this._deduplicateBoundaries(boundaries)
      .sort((a, b) => b.strength - a.strength);
  }

  /**
   * 识别外部边界
   * @param {string} text - 输入文本
   * @returns {Array} 外部边界数组
   */
  identifyExternalBoundaries(text) {
    const boundaries = [];

    this.boundaryPatterns.externalBoundaries.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const boundary = {
          source: pattern.source,
          type: pattern.type,
          influence: this._extractInfluence(match[1]),
          strength: pattern.strength,
          description: match[1].trim()
        };

        boundaries.push(boundary);
      }
    });

    // 按来源分组并去重
    return this._groupExternalBoundaries(boundaries);
  }

  /**
   * 识别边界控制机制
   * @param {string} text - 输入文本
   * @returns {Array} 控制机制数组
   */
  identifyBoundaryMechanisms(text) {
    const mechanisms = [];

    this.boundaryPatterns.controlMechanisms.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const mechanism = {
          mechanism: pattern.mechanism,
          type: pattern.type,
          description: match[1].trim(),
          effectiveness: pattern.effectiveness,
          enforcementMethods: this._identifyEnforcementMethods(match[1])
        };

        mechanisms.push(mechanism);
      }
    });

    return mechanisms;
  }

  /**
   * 评估边界渗透性
   * @param {string} text - 输入文本
   * @returns {Object} 渗透性评估结果
   */
  assessBoundaryPermeability(text) {
    const permeabilityAnalysis = {
      overallPermeability: this._calculateOverallPermeability(text),
      specificBoundaries: {
        academic: this._assessAcademicPermeability(text),
        geographic: this._assessGeographicPermeability(text),
        institutional: this._assessInstitutionalPermeability(text),
        disciplinary: this._assessDisciplinaryPermeability(text)
      },
      permeabilityTrends: this._identifyPermeabilityTrends(text)
    };

    return permeabilityAnalysis;
  }

  /**
   * 分析边界变化趋势
   * @param {string} text - 输入文本
   * @returns {Object} 趋势分析结果
   */
  analyzeBoundaryTrends(text) {
    const trendIndicators = this._extractTrendIndicators(text);

    return {
      trends: this._analyzeTrends(trendIndicators),
      overallDirection: this._determineOverallDirection(trendIndicators),
      predictedFuture: this._predictFutureChanges(trendIndicators),
      drivingFactors: this._identifyDrivingFactors(text)
    };
  }

  /**
   * 识别合法性来源
   * @param {string} text - 输入文本
   * @returns {Array} 合法性来源数组
   */
  identifyLegitimacySources(text) {
    const legitimacyPatterns = [
      {
        type: 'expertise',
        keywords: ['学术成果', '专业能力', '知识权威', '专业水平'],
        pattern: /([^。，]*(?:学术|专业)[^。，]*(?:成果|能力|权威|水平)[^。，]*)/g,
        baseStrength: 0.9
      },
      {
        type: 'formal',
        keywords: ['职位', '任命', '制度', '规定'],
        pattern: /([^。，]*(?:职位|任命)[^。，]*(?:权威|合法性)[^。，]*)/g,
        baseStrength: 0.8
      },
      {
        type: 'traditional',
        keywords: ['传统', '资历', '经验', '老'],
        pattern: /([^。，]*(?:传统|资历|经验)[^。，]*(?:权威|地位)[^。，]*)/g,
        baseStrength: 0.6
      },
      {
        type: 'peer',
        keywords: ['同行认可', '学术评价', '专家评议'],
        pattern: /([^。，]*(?:同行|专家)[^。，]*(?:认可|评价|评议)[^。，]*)/g,
        baseStrength: 0.8
      }
    ];

    const legitimacySources = [];

    legitimacyPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const source = {
          type: pattern.type,
          source: match[1].trim(),
          strength: pattern.baseStrength,
          context: this._extractLegitimacyContext(match[1])
        };

        legitimacySources.push(source);
      }
    });

    return legitimacySources;
  }

  /**
   * 验证分析结果 - 实现IFieldAnalyzer接口
   * @param {Object} result - 分析结果
   * @returns {boolean} 是否有效
   */
  validateAnalysisResult(result) {
    return result &&
           Array.isArray(result.internal) &&
           Array.isArray(result.external) &&
           Array.isArray(result.mechanisms) &&
           typeof result.permeability === 'object';
  }

  /**
   * 获取分析指标 - 实现IFieldAnalyzer接口
   * @param {Object} data - 分析数据
   * @returns {Object} 指标对象
   */
  getMetrics(data) {
    if (!this.validateAnalysisResult(data)) {
      throw new Error('输入数据格式无效');
    }

    return {
      boundaryMetrics: {
        internalBoundaryCount: data.internal.length,
        externalBoundaryCount: data.external.length,
        controlMechanismCount: data.mechanisms.length,
        averageBoundaryStrength: this._calculateAverageBoundaryStrength(data),
        overallPermeability: data.permeability.overallPermeability
      },
      complexityMetrics: {
        boundaryComplexity: this._calculateBoundaryComplexity(data),
        controlComplexity: this._calculateControlComplexity(data),
        externalInfluenceLevel: this._calculateExternalInfluence(data)
      },
      stabilityMetrics: {
        boundaryStability: this._assessBoundaryStability(data),
        changeDynamics: this._assessChangeDynamics(data)
      }
    };
  }

  // 私有辅助方法

  /**
   * 估算边界渗透性
   * @private
   */
  _estimatePermeability(description) {
    const highKeywords = ['开放', '合作', '交流'];
    const lowKeywords = ['封闭', '独立', '壁垒'];

    let permeability = 0.5; // 默认中等渗透性

    highKeywords.forEach(keyword => {
      if (description.includes(keyword)) permeability += 0.2;
    });

    lowKeywords.forEach(keyword => {
      if (description.includes(keyword)) permeability -= 0.2;
    });

    return Math.max(0, Math.min(1, permeability));
  }

  /**
   * 提取影响力
   * @private
   */
  _extractInfluence(text) {
    const influencePatterns = [
      { pattern: /指导/, influence: '政策指导' },
      { pattern: /要求/, influence: '具体要求' },
      { pattern: /规定/, influence: '制度规定' },
      { pattern: /影响/, influence: '产生影响' },
      { pattern: /压力/, influence: '施加压力' }
    ];

    for (const pattern of influencePatterns) {
      if (pattern.pattern.test(text)) {
        return pattern.influence;
      }
    }

    return '一般影响';
  }

  /**
   * 识别执行方法
   * @private
   */
  _identifyEnforcementMethods(text) {
    const methods = [];

    if (text.includes('考试')) methods.push('考试制度');
    if (text.includes('评审')) methods.push('评审机制');
    if (text.includes('认证')) methods.push('认证体系');
    if (text.includes('审批')) methods.push('审批程序');

    return methods;
  }

  /**
   * 计算总体渗透性
   * @private
   */
  _calculateOverallPermeability(text) {
    let highCount = 0;
    let lowCount = 0;

    this.permeabilityKeywords.high.forEach(keyword => {
      const regex = new RegExp(keyword, 'g');
      const matches = text.match(regex);
      highCount += matches ? matches.length : 0;
    });

    this.permeabilityKeywords.low.forEach(keyword => {
      const regex = new RegExp(keyword, 'g');
      const matches = text.match(regex);
      lowCount += matches ? matches.length : 0;
    });

    if (highCount + lowCount === 0) return 0.5;

    return highCount / (highCount + lowCount);
  }

  /**
   * 评估学术渗透性
   * @private
   */
  _assessAcademicPermeability(text) {
    const academicKeywords = ['跨学科', ' interdisciplinary', '交叉研究', '合作研究'];
    let score = 0.3; // 基础分

    academicKeywords.forEach(keyword => {
      if (text.toLowerCase().includes(keyword.toLowerCase())) {
        score += 0.2;
      }
    });

    return Math.min(1, score);
  }

  /**
   * 评估地理渗透性
   * @private
   */
  _assessGeographicPermeability(text) {
    const geographicKeywords = ['国际化', '全球', '国际交流', '海外'];
    let score = 0.3;

    geographicKeywords.forEach(keyword => {
      if (text.includes(keyword)) {
        score += 0.2;
      }
    });

    return Math.min(1, score);
  }

  /**
   * 评估制度渗透性
   * @private
   */
  _assessInstitutionalPermeability(text) {
    const institutionalKeywords = ['合作', '联盟', '联合', '协同'];
    let score = 0.3;

    institutionalKeywords.forEach(keyword => {
      if (text.includes(keyword)) {
        score += 0.2;
      }
    });

    return Math.min(1, score);
  }

  /**
   * 评估学科渗透性
   * @private
   */
  _assessDisciplinaryPermeability(text) {
    const disciplinaryKeywords = ['学科融合', '交叉学科', '整合', '综合'];
    let score = 0.3;

    disciplinaryKeywords.forEach(keyword => {
      if (text.includes(keyword)) {
        score += 0.2;
      }
    });

    return Math.min(1, score);
  }

  /**
   * 识别渗透性趋势
   * @private
   */
  _identifyPermeabilityTrends(text) {
    const trends = [];

    this.permeabilityKeywords.changing.forEach(keyword => {
      const regex = new RegExp(`(${keyword}[^。，]*)([^。，]*渗透|[^。，]*开放|[^。，]*融合)`, 'g');
      let match;
      while ((match = regex.exec(text)) !== null) {
        trends.push({
          trend: match[1] + match[2],
          direction: this._determineTrendDirection(match[2]),
          strength: 0.7
        });
      }
    });

    return trends;
  }

  /**
   * 确定趋势方向
   * @private
   */
  _determineTrendDirection(trend) {
    if (trend.includes('增加') || trend.includes('提高') || trend.includes('开放')) {
      return 'increasing';
    }
    if (trend.includes('减少') || trend.includes('降低') || trend.includes('封闭')) {
      return 'decreasing';
    }
    return 'stable';
  }

  /**
   * 去重边界
   * @private
   */
  _deduplicateBoundaries(boundaries) {
    const seen = new Set();
    return boundaries.filter(boundary => {
      const key = `${boundary.type}_${boundary.description}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  /**
   * 按来源分组外部边界
   * @private
   */
  _groupExternalBoundaries(boundaries) {
    const grouped = {};

    boundaries.forEach(boundary => {
      if (!grouped[boundary.source]) {
        grouped[boundary.source] = [];
      }
      grouped[boundary.source].push(boundary);
    });

    return Object.keys(grouped).map(source => ({
      source: source,
      influences: grouped[source],
      totalInfluence: grouped[source].reduce((sum, item) => sum + item.strength, 0),
      mainInfluence: grouped[source][0]?.influence || '一般影响'
    }));
  }

  /**
   * 获取默认结果
   * @private
   */
  getDefaultResult() {
    return {
      internal: [],
      external: [],
      mechanisms: [],
      permeability: {
        overallPermeability: 0.5,
        specificBoundaries: {},
        permeabilityTrends: []
      }
    };
  }

  /**
   * 提取合法性上下文
   * @private
   */
  _extractLegitimacyContext(text) {
    const contexts = [];

    if (text.includes('学术')) contexts.push('学术领域');
    if (text.includes('管理')) contexts.push('管理事务');
    if (text.includes('决策')) contexts.push('决策过程');
    if (text.includes('评价')) contexts.push('评价体系');

    return contexts.length > 0 ? contexts : ['一般情况'];
  }

  /**
   * 提取趋势指标
   * @private
   */
  _extractTrendIndicators(text) {
    const indicators = [];
    const trendRegex = /([^。，]*(?:越来越|逐渐|日益|不断|持续)[^。，]*(?:开放|封闭|融合|独立)[^。，]*)/g;

    let match;
    while ((match = trendRegex.exec(text)) !== null) {
      indicators.push({
        text: match[1],
        direction: this._determineTrendDirection(match[1]),
        subject: this._extractTrendSubject(match[1])
      });
    }

    return indicators;
  }

  /**
   * 提取趋势主题
   * @private
   */
  _extractTrendSubject(trend) {
    if (trend.includes('学科')) return 'disciplinary';
    if (trend.includes('国际')) return 'international';
    if (trend.includes('管理')) return 'administrative';
    if (trend.includes('市场')) return 'market';
    return 'general';
  }

  /**
   * 分析趋势
   * @private
   */
  _analyzeTrends(indicators) {
    const trends = {};

    indicators.forEach(indicator => {
      if (!trends[indicator.subject]) {
        trends[indicator.subject] = {
          trend: 'stable',
          rate: 0,
          drivers: []
        };
      }

      trends[indicator.subject].drivers.push(indicator.text);

      if (indicator.direction === 'increasing') {
        trends[indicator.subject].rate += 0.1;
      } else if (indicator.direction === 'decreasing') {
        trends[indicator.subject].rate -= 0.1;
      }
    });

    // 确定最终趋势
    Object.keys(trends).forEach(subject => {
      if (trends[subject].rate > 0.1) {
        trends[subject].trend = 'opening';
      } else if (trends[subject].rate < -0.1) {
        trends[subject].trend = 'closing';
      } else {
        trends[subject].trend = 'stable';
      }
    });

    return trends;
  }

  /**
   * 确定总体方向
   * @private
   */
  _determineOverallDirection(indicators) {
    if (indicators.length === 0) return 'stable';

    const increasing = indicators.filter(i => i.direction === 'increasing').length;
    const decreasing = indicators.filter(i => i.direction === 'decreasing').length;

    if (increasing > decreasing) return 'opening';
    if (decreasing > increasing) return 'closing';
    return 'stable';
  }

  /**
   * 预测未来变化
   * @private
   */
  _predictFutureChanges(indicators) {
    const direction = this._determineOverallDirection(indicators);
    const confidence = Math.min(0.9, indicators.length * 0.1);

    return {
      direction: direction,
      confidence: confidence,
      timeframe: '3-5年',
      likelihood: confidence > 0.5 ? 'probable' : 'possible'
    };
  }

  /**
   * 识别驱动因素
   * @private
   */
  _identifyDrivingFactors(text) {
    const factors = [];

    const factorPatterns = [
      { name: '技术发展', pattern: /数字|技术|信息化/ },
      { name: '政策改革', pattern: '政策|改革|放权' },
      { name: '市场需求', pattern: '市场|需求|竞争' },
      { name: '国际化', pattern: '国际|全球|海外' },
      { name: '学术发展', pattern: '学术|研究|创新' }
    ];

    factorPatterns.forEach(factor => {
      if (new RegExp(factor.pattern).test(text)) {
        factors.push(factor.name);
      }
    });

    return factors;
  }

  /**
   * 计算平均边界强度
   * @private
   */
  _calculateAverageBoundaryStrength(data) {
    const allBoundaries = [...data.internal, ...data.external];
    if (allBoundaries.length === 0) return 0;

    const totalStrength = allBoundaries.reduce((sum, boundary) => {
      return sum + (boundary.strength || 0);
    }, 0);

    return (totalStrength / allBoundaries.length).toFixed(2);
  }

  /**
   * 计算边界复杂性
   * @private
   */
  _calculateBoundaryComplexity(data) {
    const internalTypes = new Set(data.internal.map(b => b.type));
    const externalSources = new Set(data.external.map(b => b.source));

    return {
      internalComplexity: internalTypes.size,
      externalComplexity: externalSources.size,
      overallComplexity: internalTypes.size + externalSources.size
    };
  }

  /**
   * 计算控制复杂性
   * @private
   */
  _calculateControlComplexity(data) {
    return {
      mechanismCount: data.mechanisms.length,
      averageEffectiveness: this._calculateAverageEffectiveness(data.mechanisms),
      controlCoverage: this._assessControlCoverage(data)
    };
  }

  /**
   * 计算平均有效性
   * @private
   */
  _calculateAverageEffectiveness(mechanisms) {
    if (mechanisms.length === 0) return 0;

    const totalEffectiveness = mechanisms.reduce((sum, mechanism) => {
      return sum + (mechanism.effectiveness || 0);
    }, 0);

    return (totalEffectiveness / mechanisms.length).toFixed(2);
  }

  /**
   * 评估控制覆盖度
   * @private
   */
  _assessControlCoverage(data) {
    const controlAreas = new Set();

    data.mechanisms.forEach(mechanism => {
      controlAreas.add(mechanism.type);
    });

    return controlAreas.size;
  }

  /**
   * 计算外部影响力
   * @private
   */
  _calculateExternalInfluence(data) {
    const totalInfluence = data.external.reduce((sum, boundary) => {
      return sum + (boundary.totalInfluence || 0);
    }, 0);

    return {
      totalInfluence: totalInfluence,
      averageInfluence: data.external.length > 0 ?
        (totalInfluence / data.external.length).toFixed(2) : 0,
      dominantSource: this._findDominantSource(data.external)
    };
  }

  /**
   * 找到主要影响源
   * @private
   */
  _findDominantSource(externalBoundaries) {
    if (externalBoundaries.length === 0) return 'none';

    return externalBoundaries.reduce((dominant, current) => {
      return current.totalInfluence > dominant.totalInfluence ? current : dominant;
    }).source;
  }

  /**
   * 评估边界稳定性
   * @private
   */
  _assessBoundaryStability(data) {
    const stabilityFactors = {
      formalBoundaries: data.internal.filter(b => b.type === 'formal').length,
      highStrengthBoundaries: data.internal.filter(b => b.strength > 0.8).length,
      controlMechanisms: data.mechanisms.length,
      permeability: 1 - data.permeability.overallPermeability
    };

    const stabilityScore = (
      stabilityFactors.formalBoundaries * 0.2 +
      stabilityFactors.highStrengthBoundaries * 0.3 +
      stabilityFactors.controlMechanisms * 0.3 +
      stabilityFactors.permeability * 0.2
    );

    return {
      score: Math.min(1, stabilityScore),
      level: stabilityScore > 0.7 ? 'high' : stabilityScore > 0.4 ? 'medium' : 'low',
      factors: stabilityFactors
    };
  }

  /**
   * 评估变化动态
   * @private
   */
  _assessChangeDynamics(data) {
    const trends = data.permeability.permeabilityTrends;
    const changeIntensity = trends.length;

    return {
      intensity: changeIntensity > 5 ? 'high' : changeIntensity > 2 ? 'medium' : 'low',
      direction: this._determineOverallChangeDirection(trends),
      speed: changeIntensity > 0 ? 'dynamic' : 'static'
    };
  }

  /**
   * 确定总体变化方向
   * @private
   */
  _determineOverallChangeDirection(trends) {
    if (trends.length === 0) return 'stable';

    const increasing = trends.filter(t => t.direction === 'increasing').length;
    const decreasing = trends.filter(t => t.direction === 'decreasing').length;

    if (increasing > decreasing) return 'opening';
    if (decreasing > increasing) return 'closing';
    return 'stable';
  }
}

module.exports = FieldBoundaryAnalyzer;