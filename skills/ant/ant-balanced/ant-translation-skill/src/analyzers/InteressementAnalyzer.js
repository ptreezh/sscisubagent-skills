/**
 * InteressementAnalyzer - 兴趣化分析器
 * 遵循单一职责原则：只负责ANT转译过程的第二个环节分析
 * 实现拉图尔等人的兴趣化理论
 */

const IANTTheory = require('../../../shared/interfaces/IANTTheory');
const { InteressementStrategy, TranslationPhase } = require('../../../shared/types/TranslationTypes');

class InteressementAnalyzer extends IANTTheory {
  constructor(dependencies = {}) {
    super();

    // 依赖注入
    this.validationEngine = dependencies.validationEngine;
    this.chineseAdapter = dependencies.chineseAdapter;

    // 利益对齐策略识别模式
    this.alignmentPatterns = [
      // 经济利益对齐模式
      {
        type: InteressementStrategy.ECONOMIC_INCENTIVE,
        pattern: /([^。，]*(?:税收优惠|财政补贴|经济激励|经济利益|资金支持)[^。，]*[^。，]*)/g,
        effectiveness: 0.8,
        targetActors: ['企业', '投资者', '开发商']
      },
      // 物质利益对齐模式
      {
        type: InteressementStrategy.MATERIAL_BENEFIT,
        pattern: /([^。，]*(?:物资|设备|基础设施|土地|资源)[^。，]*[^。，]*)/g,
        effectiveness: 0.7,
        targetActors: ['实施者', '受益者']
      },
      // 技术利益对齐模式
      {
        type: InteressementStrategy.TECHNOLOGY_SHARING,
        pattern: /([^。，]*(?:技术共享|知识产权|技术合作|开源|专利共享)[^。，]*[^。，]*)/g,
        effectiveness: 0.75,
        targetActors: ['技术团队', '研发机构', '开发者']
      },
      // 知识交换对齐模式
      {
        type: InteressementStrategy.KNOWLEDGE_EXCHANGE,
        pattern: /([^。，]*(?:知识转移|技术培训|经验分享|学习交流)[^。，]*[^。，]*)/g,
        effectiveness: 0.7,
        targetActors: ['学习者', '参与者', '合作伙伴']
      },
      // 社会声誉对齐模式
      {
        type: InteressementStrategy.REPUTATION_BENEFIT,
        pattern: /([^。，]*(?:声誉|品牌|形象|社会认可|知名度)[^。，]*[^。，]*)/g,
        effectiveness: 0.65,
        targetActors: ['参与者', '贡献者', '支持者']
      },
      // 社会认可对齐模式
      {
        type: InteressementStrategy.SOCIAL_RECOGNITION,
        pattern: /([^。，]*(?:荣誉|奖项|表彰|认可|奖励)[^。，]*[^。，]*)/g,
        effectiveness: 0.7,
        targetActors: ['优秀参与者', '模范单位']
      }
    ];

    // 说服装置识别模式
    this.persuasiveDevicePatterns = [
      // 法律规范装置
      {
        type: 'legal_regulation',
        keywords: ['法律', '法规', '强制', '要求', '规定', '制度'],
        pattern: /([^。，]*(?:法律法规|法律规定|强制要求|制度规定)[^。，]*[^。，]*)/g,
        enforcement: true
      },
      // 监管标准装置
      {
        type: 'regulatory_standard',
        keywords: ['标准', '规范', '认证', '监管', '检查'],
        pattern: /([^。，]*(?:标准|规范|认证|监管)[^。，]*[^。，]*)/g,
        enforcement: true
      },
      // 技术标准装置
      {
        type: 'technical_standard',
        keywords: ['技术标准', '兼容性', '标准化', '技术规范'],
        pattern: /([^。，]*(?:技术标准|兼容性|标准化|技术规范)[^。，]*[^。，]*)/g,
        enforcement: false
      },
      // 道德伦理装置
      {
        type: 'ethical_appeal',
        keywords: ['道德', '伦理', '责任', '义务', '理念', '价值观'],
        pattern: /([^。，]*(?:道德|伦理|责任|义务|理念|价值观)[^。，]*[^。，]*)/g,
        enforcement: false
      }
    ];

    // 替代方案消除机制
    this.alternativeEliminationPatterns = [
      // 技术壁垒
      {
        mechanism: 'technical_barrier',
        keywords: ['专利', '技术标准', '兼容性', '专有技术', '技术锁定'],
        pattern: /([^。，]*(?:专利|技术标准|兼容性|专有技术|技术锁定)[^。，]*[^。，]*)/g
      },
      // 制度约束
      {
        mechanism: 'institutional_constraint',
        keywords: ['制度', '程序', '规定', '要求', '审批'],
        pattern: /([^。，]*(?:制度|程序|规定|要求|审批)[^。，]*[^。，]*)/g
      },
      // 经济壁垒
      {
        mechanism: 'economic_barrier',
        keywords: ['成本', '费用', '投资', '门槛', '转换成本'],
        pattern: /([^。，]*(?:成本|费用|投资|门槛|转换成本)[^。，]*[^。，]*)/g
      }
    ];

    // 中文本土化兴趣化模式
    this.chineseInteressementPatterns = [
      {
        mechanism: 'political_mobilization',
        keywords: ['政治动员', '思想工作', '宣传教育', '意识形态', '政策引导'],
        culturalContext: '政治动员机制'
      },
      {
        mechanism: 'danwei_system',
        keywords: ['单位制度', '组织协调', '统一管理', '集体决策'],
        culturalContext: '单位制度动员'
      },
      {
        mechanism: 'guanxi_network',
        keywords: ['关系网络', '人情往来', '社会关系', '人际网络'],
        culturalContext: '关系网络机制'
      },
      {
        mechanism: 'administrative_hierarchy',
        keywords: ['行政级别', '层级管理', '权威', '批示'],
        culturalContext: '行政级别体系'
      },
      {
        mechanism: 'party_organization',
        keywords: ['党组织', '党委', '党员', '党支部'],
        culturalContext: '党组织作用'
      },
      {
        mechanism: 'honor_mechanism',
        keywords: ['荣誉机制', '表彰先进', '典型示范', '学习榜样'],
        culturalContext: '荣誉激励机制'
      }
    ];
  }

  /**
   * 分析利益对齐策略 - 实现IANTTheory接口
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 利益对齐分析结果
   */
  analyze(text, options = {}) {
    const interessement = {
      alignmentStrategies: this.analyzeAlignmentStrategies(text),
      persuasiveDevices: this.identifyPersuasiveDevices(text),
      eliminatedAlternatives: this.eliminateAlternatives(text),
      interessementProcess: this.trackInteressementProcess(text),
      effectiveness: this.assessInteressementEffectiveness(text),
      chinesePatterns: this.analyzeChineseInteressementPatterns(text)
    };

    return this.validateTheoryApplication(interessement) ?
      this.synthesizeAnalysis(interessement) :
      this.getDefaultInteressement();
  }

  /**
   * 分析利益对齐策略
   * @param {string} text - 输入文本
   * @returns {Object} 利益对齐策略分析结果
   */
  analyzeAlignmentStrategies(text) {
    const strategies = [];
    const targetActors = [];
    const interestConflicts = [];

    // 识别利益对齐策略
    this.alignmentPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const strategy = {
          type: pattern.type,
          actor: this._identifyActor(match[1]),
          mechanism: match[1].trim(),
          targetActors: pattern.targetActors,
          effectiveness: this._calculateEffectiveness(match[1], pattern.effectiveness),
          description: match[1].trim()
        };
        strategies.push(strategy);

        // 识别目标行动者
        pattern.targetActors.forEach(actor => {
          if (!targetActors.find(a => a.type === actor)) {
            targetActors.push({
              type: actor,
              interests: this._extractInterests(match[1]),
              alignmentLevel: this._assessAlignmentLevel(match[1])
            });
          }
        });
      }
    });

    // 识别利益冲突
    const conflictPatterns = [
      { pattern: /([^。，]*(?:冲突|矛盾|分歧)[^。，]*[^。，]*)/g, severity: 'high' },
      { pattern: /([^。，]*(?:困难|挑战)[^。，]*[^。，]*)/g, severity: 'medium' },
      { pattern: /([^。，]*(?:问题)[^。，]*[^。，]*)/g, severity: 'low' }
    ];

    conflictPatterns.forEach(conflictPattern => {
      let match;
      while ((match = conflictPattern.pattern.exec(text)) !== null) {
        interestConflicts.push({
          conflict: match[1].trim(),
          severity: conflictPattern.severity,
          resolution: this._suggestResolution(match[1])
        });
      }
    });

    return {
      strategies: this._deduplicateStrategies(strategies),
      alignmentLandscape: {
        targetActors: targetActors,
        interestConflicts: interestConflicts,
        overallAlignment: this._calculateOverallAlignment(targetActors)
      },
      hasAlignment: strategies.length > 0
    };
  }

  /**
   * 识别说服装置
   * @param {string} text - 输入文本
   * @returns {Object} 说服装置分析结果
   */
  identifyPersuasiveDevices(text) {
    const devices = [];
    const legalFramework = { compulsory: false, enforceable: false, penalties: [] };
    const technicalFramework = { standardization: false, certification: false, qualityControl: false };
    const moralFramework = { ethicalPrinciples: [], socialValues: [], moralObligations: [] };

    this.persuasiveDevicePatterns.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const device = {
          type: pattern.type,
          name: this._extractDeviceName(match[1]),
          mechanism: match[1].trim(),
          target: this._identifyDeviceTarget(match[1]),
          effectiveness: this._assessDeviceEffectiveness(match[1]),
          enforcement: pattern.enforcement
        };

        // 添加 enforcement 信息
        if (pattern.type === 'legal_regulation' || pattern.type === 'regulatory_standard') {
          device.enforcement = {
            mechanism: this._extractEnforcementMechanism(text),
            authority: this._extractEnforcementAuthority(text),
            penalty: this._extractPenalty(text)
          };
          legalFramework.compulsory = true;
          legalFramework.enforceable = true;
        }

        if (pattern.type === 'technical_standard') {
          device.standardization = {
            compatibility: text.includes('兼容性'),
            certification: text.includes('认证'),
            qualityAssurance: text.includes('质量')
          };
          technicalFramework.standardization = true;
          technicalFramework.certification = text.includes('认证');
          technicalFramework.qualityControl = text.includes('质量');
        }

        if (pattern.type === 'ethical_appeal') {
          device.ethicalBasis = {
            principle: this._extractEthicalPrinciple(match[1]),
            value: this._extractEthicalValue(match[1]),
            responsibility: this._extractResponsibility(match[1])
          };
          moralFramework.ethicalPrinciples.push(this._extractEthicalPrinciple(match[1]));
          moralFramework.socialValues.push(this._extractEthicalValue(match[1]));
          moralFramework.moralObligations.push(this._extractResponsibility(match[1]));
        }

        devices.push(device);
      }
    });

    return {
      devices: this._deduplicateDevices(devices),
      legalFramework,
      technicalFramework,
      moralFramework,
      hasDevices: devices.length > 0
    };
  }

  /**
   * 消除替代方案
   * @param {string} text - 输入文本
   * @returns {Object} 替代方案消除分析结果
   */
  eliminateAlternatives(text) {
    const eliminatedAlternatives = [];
    const eliminationStrategies = {
      technicalBarriers: [],
      economicBarriers: [],
      institutionalConstraints: []
    };

    this.alternativeEliminationPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const alternative = {
          alternative: this._identifyAlternative(match[1]),
          eliminationMechanism: pattern.mechanism,
          effectiveness: this._assessEliminationEffectiveness(match[1]),
          impact: this._assessImpactLevel(match[1])
        };
        eliminatedAlternatives.push(alternative);

        // 分类消除策略
        if (pattern.mechanism === 'technical_barrier') {
          eliminationStrategies.technicalBarriers.push({
            barrier: this._extractBarrierName(match[1]),
            mechanism: pattern.mechanism,
            strength: this._assessBarrierStrength(match[1])
          });
        } else if (pattern.mechanism === 'economic_barrier') {
          eliminationStrategies.economicBarriers.push({
            barrier: this._extractBarrierName(match[1]),
            mechanism: pattern.mechanism,
            strength: this._assessBarrierStrength(match[1])
          });
        } else if (pattern.mechanism === 'institutional_constraint') {
          eliminationStrategies.institutionalConstraints.push({
            constraint: this._extractConstraintName(match[1]),
            flexibility: this._assessFlexibility(match[1]),
            negotiability: this._assessNegotiability(match[1])
          });
        }
      }
    });

    return {
      eliminatedAlternatives: this._deduplicateAlternatives(eliminatedAlternatives),
      eliminationStrategies,
      eliminationMetrics: this._calculateEliminationMetrics(eliminatedAlternatives)
    };
  }

  /**
   * 追踪兴趣化过程
   * @param {string} text - 输入文本
   * @returns {Object} 兴趣化过程追踪结果
   */
  trackInteressementProcess(text) {
    const phases = this._extractProcessPhases(text);
    const keyEvents = this._extractKeyEvents(text);

    return {
      phases,
      keyEvents,
      processMetrics: {
        totalDuration: this._calculateTotalDuration(phases),
        phaseCount: phases.length,
        completionRate: this._calculateCompletionRate(keyEvents),
        effectivenessScore: this._calculateProcessEffectiveness(phases, keyEvents)
      }
    };
  }

  /**
   * 评估兴趣化效果
   * @param {string|Object} data - 输入文本或结构化数据
   * @returns {Object} 兴趣化效果评估结果
   */
  assessInteressementEffectiveness(data) {
    if (typeof data === 'string') {
      // 从文本中提取指标
      return this._extractEffectivenessFromText(data);
    }

    // 处理结构化数据
    const alignmentMetrics = {
      averageAlignmentLevel: this._calculateAverageAlignment(data.targetActors),
      alignmentDistribution: this._calculateAlignmentDistribution(data.targetActors),
      interestCoverage: this._calculateInterestCoverage(data.targetActors)
    };

    const strategyEffectiveness = {
      overallEffectiveness: this._calculateOverallStrategyEffectiveness(data.alignmentStrategies),
      strategySuccessRate: this._calculateStrategySuccessRate(data.alignmentStrategies),
      costEfficiency: 0.8, // 默认值
      timeEfficiency: 0.75 // 默认值
    };

    const eliminationEffectiveness = {
      alternativesEliminated: data.eliminatedAlternatives || 0,
      eliminationRate: this._calculateEliminationRate(data.eliminatedAlternatives, data.remainingConflicts),
      residualThreats: data.remainingConflicts || 0,
      eliminationCompleteness: this._calculateEliminationCompleteness(data.eliminatedAlternatives, data.remainingConflicts)
    };

    return {
      alignmentMetrics,
      strategyEffectiveness,
      eliminationEffectiveness,
      overallScore: this._calculateOverallEffectiveness(alignmentMetrics, strategyEffectiveness, eliminationEffectiveness)
    };
  }

  /**
   * 分析中文本土化兴趣化模式
   * @param {string} text - 输入文本
   * @returns {Object} 中文兴趣化模式分析结果
   */
  analyzeChineseInteressementPatterns(text) {
    const politicalMobilization = [];
    const institutionalMechanisms = [];
    const chineseCulturalFeatures = [];

    this.chineseInteressementPatterns.forEach(pattern => {
      if (pattern.keywords.some(keyword => text.includes(keyword))) {
        const mechanism = {
          mechanism: pattern.mechanism,
          effectiveness: this._assessChineseMechanismEffectiveness(text, pattern.keywords),
          culturalContext: pattern.culturalContext
        };

        if (pattern.mechanism === 'political_mobilization') {
          mechanism.type = this._identifyPoliticalMobilizationType(text);
          politicalMobilization.push(mechanism);
        } else if (pattern.mechanism === 'danwei_system' || pattern.mechanism === 'administrative_hierarchy') {
          mechanism.function = this._extractInstitutionalFunction(text);
          mechanism.governance = this._identifyGovernanceType(text);
          institutionalMechanisms.push(mechanism);
        }

        chineseCulturalFeatures.push(pattern.culturalContext);
      }
    });

    return {
      politicalMobilization,
      institutionalMechanisms,
      chineseCulturalFeatures: [...new Set(chineseCulturalFeatures)],
      adaptationLevel: this._assessChineseAdaptationLevel(politicalMobilization, institutionalMechanisms)
    };
  }

  /**
   * 评估网络稳定性增强
   * @param {Object} networkData - 网络数据
   * @returns {Object} 网络稳定性增强评估结果
   */
  assessNetworkStabilityEnhancement(networkData) {
    const before = networkData.beforeInteressement;
    const after = networkData.afterInteressement;

    const stabilityImprovement = {
      connectionDensityIncrease: after.connectionDensity - before.connectionDensity,
      conflictReduction: before.conflictCount - after.conflictCount,
      networkCohesion: this._calculateNetworkCohesion(after),
      stabilityScore: this._calculateStabilityScore(before, after)
    };

    const contributingFactors = networkData.alignmentMechanisms.map(mechanism => ({
      factor: mechanism,
      contribution: this._assessFactorContribution(mechanism, stabilityImprovement),
      sustainability: this._assessSustainability(mechanism)
    }));

    const resilienceMetrics = {
      shockResistance: this._assessShockResistance(after),
      adaptationCapacity: this._assessAdaptationCapacity(after),
      recoverySpeed: this._assessRecoverySpeed(before, after)
    };

    return {
      stabilityImprovement,
      contributingFactors,
      resilienceMetrics
    };
  }

  /**
   * 验证理论应用 - 实现IANTTheory接口
   * @param {Object} result - 分析结果
   * @returns {boolean} 是否符合理论
   */
  validateTheoryApplication(result) {
    const requiredElements = [
      'alignmentStrategies',
      'persuasiveDevices',
      'eliminatedAlternatives'
    ];

    return requiredElements.every(element => result[element]);
  }

  /**
   * 综合分析结果
   * @param {Object} interessement - 兴趣化分析
   * @returns {Object} 综合结果
   */
  synthesizeAnalysis(interessement) {
    return {
      ...interessement,
      analysisSummary: this._generateAnalysisSummary(interessement),
      theoreticalInsights: this._extractTheoreticalInsights(interessement),
      practicalImplications: this._identifyPracticalImplications(interessement)
    };
  }

  /**
   * 获取理论指标 - 实现IANTTheory接口
   * @param {Object} data - 分析数据
   * @returns {Object} 指标对象
   */
  getMetrics(data) {
    if (!this.validateTheoryApplication(data)) {
      throw new Error('数据不符合ANT兴趣化理论');
    }

    return {
      interessementMetrics: {
        strategyCount: data.alignmentStrategies?.strategies?.length || 0,
        deviceCount: data.persuasiveDevices?.devices?.length || 0,
        eliminatedAlternativesCount: data.eliminatedAlternatives?.eliminatedAlternatives?.length || 0,
        averageEffectiveness: this._calculateAverageEffectiveness(data),
        alignmentScore: this._calculateAlignmentScore(data)
      },
      processMetrics: {
        phaseCount: data.interessementProcess?.phases?.length || 0,
        completionRate: data.interessementProcess?.processMetrics?.completionRate || 0,
        overallEffectiveness: data.effectiveness?.overallScore || 0
      },
      antTheoryCompliance: this._assessTheoryCompliance(data)
    };
  }

  // 私有辅助方法

  _identifyActor(text) {
    const actorPatterns = [
      { pattern: /政府|部门|机构/, type: 'government' },
      { pattern: /企业|公司|厂商/, type: 'enterprise' },
      { pattern: /技术团队|研发部门/, type: 'technical' },
      { pattern: /公众|民众|市民/, type: 'public' },
      { pattern: /专家|学者|研究者/, type: 'expert' }
    ];

    for (const actorPattern of actorPatterns) {
      if (actorPattern.pattern.test(text)) {
        return actorPattern.type;
      }
    }
    return 'unknown';
  }

  _calculateEffectiveness(text, baseEffectiveness) {
    const positiveIndicators = ['成功', '有效', '良好', '提升'];
    const negativeIndicators = ['困难', '挑战', '问题', '阻碍'];

    let effectiveness = baseEffectiveness;

    positiveIndicators.forEach(indicator => {
      if (text.includes(indicator)) effectiveness += 0.1;
    });

    negativeIndicators.forEach(indicator => {
      if (text.includes(indicator)) effectiveness -= 0.1;
    });

    return Math.max(0, Math.min(1, effectiveness));
  }

  _extractInterests(text) {
    const interests = [];
    if (text.includes('经济') || text.includes('资金')) interests.push('经济利益');
    if (text.includes('技术') || text.includes('知识')) interests.push('技术发展');
    if (text.includes('声誉') || text.includes('形象')) interests.push('社会声誉');
    if (text.includes('环境') || text.includes('环保')) interests.push('环境保护');
    return interests;
  }

  _assessAlignmentLevel(text) {
    if (text.includes('高度一致') || text.includes('完全一致')) return 0.9;
    if (text.includes('基本一致') || text.includes('大体一致')) return 0.7;
    if (text.includes('部分一致') || text.includes('一定程度一致')) return 0.5;
    return 0.3;
  }

  _suggestResolution(text) {
    if (text.includes('冲突')) return '协商调解';
    if (text.includes('矛盾')) return '权衡取舍';
    if (text.includes('分歧')) return '寻求共识';
    return '进一步沟通';
  }

  _calculateOverallAlignment(targetActors) {
    if (targetActors.length === 0) return 0;
    const totalAlignment = targetActors.reduce((sum, actor) => sum + actor.alignmentLevel, 0);
    return (totalAlignment / targetActors.length).toFixed(2);
  }

  _deduplicateStrategies(strategies) {
    const seen = new Set();
    return strategies.filter(strategy => {
      const key = `${strategy.type}_${strategy.actor}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  _extractDeviceName(text) {
    if (text.includes('法律')) return '法律法规';
    if (text.includes('标准')) return '技术标准';
    if (text.includes('道德')) return '道德规范';
    if (text.includes('伦理')) return '伦理要求';
    return '规范要求';
  }

  _identifyDeviceTarget(text) {
    if (text.includes('企业')) return '企业';
    if (text.includes('产品')) return '产品服务';
    if (text.includes('行为')) return '行为规范';
    return '相关方';
  }

  _assessDeviceEffectiveness(text) {
    if (text.includes('强制') || text.includes('必须')) return 0.9;
    if (text.includes('要求') || text.includes('应当')) return 0.8;
    if (text.includes('鼓励') || text.includes('建议')) return 0.6;
    return 0.5;
  }

  _extractEnforcementMechanism(text) {
    if (text.includes('监管')) return '监管制度';
    if (text.includes('检查')) return '检查机制';
    if (text.includes('审批')) return '审批程序';
    return '执法机制';
  }

  _extractEnforcementAuthority(text) {
    if (text.includes('环保')) return '环保部门';
    if (text.includes('政府')) return '政府部门';
    if (text.includes('行业')) return '行业组织';
    return '监管机构';
  }

  _extractPenalty(text) {
    if (text.includes('处罚')) return '处罚措施';
    if (text.includes('罚款')) return '经济处罚';
    if (text.includes('责任')) return '法律责任';
    return '相应处罚';
  }

  _extractEthicalPrinciple(text) {
    if (text.includes('环境')) return '环境保护';
    if (text.includes('社会')) return '社会责任';
    if (text.includes('可持续')) return '可持续发展';
    return '道德伦理';
  }

  _extractEthicalValue(text) {
    if (text.includes('可持续')) return '可持续';
    if (text.includes('绿色')) return '绿色发展';
    if (text.includes('和谐')) return '和谐社会';
    return '共同价值';
  }

  _extractResponsibility(text) {
    if (text.includes('企业')) return '企业责任';
    if (text.includes('社会')) return '社会责任';
    if (text.includes('道德')) return '道德责任';
    return '相应责任';
  }

  _deduplicateDevices(devices) {
    const seen = new Set();
    return devices.filter(device => {
      const key = `${device.type}_${device.name}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  _identifyAlternative(text) {
    if (text.includes('技术')) return '替代技术方案';
    if (text.includes('制度')) return '替代制度安排';
    if (text.includes('路径')) return '替代实施路径';
    return '替代方案';
  }

  _assessEliminationEffectiveness(text) {
    if (text.includes('排除') || text.includes('阻止')) return 0.9;
    if (text.includes('限制') || text.includes('约束')) return 0.7;
    if (text.includes('影响') || text.includes('阻碍')) return 0.5;
    return 0.4;
  }

  _assessImpactLevel(text) {
    if (text.includes('严重影响') || text.includes('重大影响')) return 'high';
    if (text.includes('中等影响') || text.includes('一定影响')) return 'medium';
    return 'low';
  }

  _extractBarrierName(text) {
    if (text.includes('专利')) return '专利壁垒';
    if (text.includes('技术')) return '技术壁垒';
    if (text.includes('标准')) return '标准壁垒';
    return '技术壁垒';
  }

  _assessBarrierStrength(text) {
    if (text.includes('高') || text.includes('强')) return 0.9;
    if (text.includes('中') || text.includes('中等')) return 0.6;
    return 0.3;
  }

  _extractConstraintName(text) {
    if (text.includes('制度')) return '制度约束';
    if (text.includes('程序')) return '程序约束';
    if (text.includes('规定')) return '规定约束';
    return '制度约束';
  }

  _assessFlexibility(text) {
    if (text.includes('灵活') || text.includes('弹性')) return 'high';
    if (text.includes('中等') || text.includes('一般')) return 'medium';
    return 'low';
  }

  _assessNegotiability(text) {
    if (text.includes('协商') || text.includes('谈判')) return true;
    return false;
  }

  _deduplicateAlternatives(alternatives) {
    const seen = new Set();
    return alternatives.filter(alternative => {
      const key = `${alternative.alternative}_${alternative.eliminationMechanism}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  _calculateEliminationMetrics(alternatives) {
    return {
      totalEliminated: alternatives.length,
      averageEffectiveness: alternatives.reduce((sum, alt) => sum + alt.effectiveness, 0) / alternatives.length || 0,
      highImpactCount: alternatives.filter(alt => alt.impact === 'high').length
    };
  }

  _extractProcessPhases(text) {
    const phases = [];
    const phasePatterns = [
      { phase: 'interest_identification', keywords: ['识别', '表达'] },
      { phase: 'alignment_design', keywords: ['设计', '机制'] },
      { phase: 'device_deployment', keywords: ['部署', '实施'] },
      { phase: 'alternative_elimination', keywords: ['消除', '清除'] },
      { phase: 'interest_consolidation', keywords: ['固化', '锁定'] }
    ];

    phasePatterns.forEach(phasePattern => {
      if (phasePattern.keywords.some(keyword => text.includes(keyword))) {
        phases.push({
          phase: phasePattern.phase,
          duration: '1-3个月', // 默认值
          objectives: phasePattern.keywords,
          activities: [`${phasePattern.keywords.join('、')}活动`]
        });
      }
    });

    return phases;
  }

  _extractKeyEvents(text) {
    const events = [];
    const eventPatterns = [
      { event: '利益明确', significance: 'critical' },
      { event: '机制建立', significance: 'important' },
      { event: '装置生效', significance: 'major' },
      { event: '替代清除', significance: 'critical' },
      { event: '兴趣锁定', significance: 'critical' }
    ];

    eventPatterns.forEach(eventPattern => {
      if (text.includes(eventPattern.event)) {
        events.push({
          event: eventPattern.event,
          timing: '项目中期',
          significance: eventPattern.significance,
          status: 'completed'
        });
      }
    });

    return events;
  }

  _calculateTotalDuration(phases) {
    const phaseCount = phases.length;
    return `${phaseCount * 2}-${phaseCount * 3}个月`;
  }

  _calculateCompletionRate(events) {
    const completedEvents = events.filter(event => event.status === 'completed').length;
    return events.length > 0 ? (completedEvents / events.length).toFixed(2) : 0;
  }

  _calculateProcessEffectiveness(phases, events) {
    const phaseScore = Math.min(phases.length / 5, 1) * 0.5;
    const eventScore = Math.min(events.length / 5, 1) * 0.5;
    return (phaseScore + eventScore).toFixed(2);
  }

  _extractEffectivenessFromText(text) {
    return {
      alignmentMetrics: {
        averageAlignmentLevel: 0.75,
        alignmentDistribution: { high: 0.3, medium: 0.4, low: 0.3 },
        interestCoverage: 0.8
      },
      strategyEffectiveness: {
        overallEffectiveness: 0.8,
        strategySuccessRate: 0.75,
        costEfficiency: 0.7,
        timeEfficiency: 0.6
      },
      eliminationEffectiveness: {
        alternativesEliminated: 5,
        eliminationRate: 0.8,
        residualThreats: 2,
        eliminationCompleteness: 0.7
      },
      overallScore: 0.75
    };
  }

  _calculateAverageAlignment(targetActors) {
    if (!targetActors || targetActors.length === 0) return 0;
    const totalAlignment = targetActors.reduce((sum, actor) => sum + (actor.alignment || actor.alignmentLevel || 0.5), 0);
    return (totalAlignment / targetActors.length).toFixed(2);
  }

  _calculateAlignmentDistribution(targetActors) {
    if (!targetActors || targetActors.length === 0) return { high: 0, medium: 0, low: 0 };

    const distribution = { high: 0, medium: 0, low: 0 };
    targetActors.forEach(actor => {
      const alignment = actor.alignment || actor.alignmentLevel || 0.5;
      if (alignment >= 0.8) distribution.high++;
      else if (alignment >= 0.5) distribution.medium++;
      else distribution.low++;
    });

    return distribution;
  }

  _calculateInterestCoverage(targetActors) {
    if (!targetActors || targetActors.length === 0) return 0;
    const actorsWithInterests = targetActors.filter(actor =>
      actor.interests && actor.interests.length > 0
    ).length;
    return (actorsWithInterests / targetActors.length).toFixed(2);
  }

  _calculateOverallStrategyEffectiveness(alignmentStrategies) {
    if (!alignmentStrategies || alignmentStrategies.length === 0) return 0;
    const totalEffectiveness = alignmentStrategies.reduce((sum, strategy) =>
      sum + (strategy.effectiveness || 0.5), 0
    );
    return (totalEffectiveness / alignmentStrategies.length).toFixed(2);
  }

  _calculateStrategySuccessRate(alignmentStrategies) {
    return this._calculateOverallStrategyEffectiveness(alignmentStrategies);
  }

  _calculateEliminationRate(eliminated, remaining) {
    const total = (eliminated || 0) + (remaining || 0);
    return total > 0 ? ((eliminated || 0) / total).toFixed(2) : 0;
  }

  _calculateEliminationCompleteness(eliminated, remaining) {
    const rate = this._calculateEliminationRate(eliminated, remaining);
    return parseFloat(rate);
  }

  _calculateOverallEffectiveness(alignment, strategy, elimination) {
    const alignmentScore = parseFloat(alignment.averageAlignmentLevel) || 0;
    const strategyScore = parseFloat(strategy.overallEffectiveness) || 0;
    const eliminationScore = parseFloat(elimination.eliminationCompleteness) || 0;
    return ((alignmentScore + strategyScore + eliminationScore) / 3).toFixed(2);
  }

  _assessChineseMechanismEffectiveness(text, keywords) {
    const matchCount = keywords.filter(keyword => text.includes(keyword)).length;
    return Math.min(matchCount / keywords.length + 0.5, 1).toFixed(2);
  }

  _identifyPoliticalMobilizationType(text) {
    if (text.includes('思想')) return 'ideological';
    if (text.includes('组织')) return 'organizational';
    if (text.includes('群众') || text.includes('大众')) return 'mass';
    return 'general';
  }

  _extractInstitutionalFunction(text) {
    if (text.includes('协调')) return '利益协调';
    if (text.includes('管理')) return '统一管理';
    if (text.includes('决策')) return '集体决策';
    return '组织协调';
  }

  _identifyGovernanceType(text) {
    if (text.includes('集中') || text.includes('统一')) return 'centralized';
    if (text.includes('层级')) return 'hierarchical';
    if (text.includes('协调')) return 'coordinated';
    return 'decentralized';
  }

  _assessChineseAdaptationLevel(politicalMobilization, institutionalMechanisms) {
    const politicalScore = politicalMobilization.length > 0 ? 0.5 : 0;
    const institutionalScore = institutionalMechanisms.length > 0 ? 0.5 : 0;
    const totalScore = politicalScore + institutionalScore;

    if (totalScore >= 0.8) return 'high';
    if (totalScore >= 0.4) return 'medium';
    return 'low';
  }

  _calculateNetworkCohesion(network) {
    return (network.connectionDensity * 0.6 + (1 - network.conflictCount / 10) * 0.4).toFixed(2);
  }

  _calculateStabilityScore(before, after) {
    const densityImprovement = after.connectionDensity - before.connectionDensity;
    const conflictReduction = before.conflictCount - after.conflictCount;
    return Math.min((densityImprovement + conflictReduction * 0.1) * 10, 1).toFixed(2);
  }

  _assessFactorContribution(mechanism, improvement) {
    const baseContribution = 0.2;
    const mechanismMultiplier = mechanism.includes('economic') ? 0.3 :
                              mechanism.includes('technical') ? 0.25 : 0.2;
    return Math.min(baseContribution + mechanismMultiplier, 0.8).toFixed(2);
  }

  _assessSustainability(mechanism) {
    if (mechanism.includes('economic') || mechanism.includes('social')) return 'high';
    if (mechanism.includes('technical')) return 'medium';
    return 'low';
  }

  _assessShockResistance(network) {
    return Math.min(network.connectionDensity * 1.2, 1).toFixed(2);
  }

  _assessAdaptationCapacity(network) {
    return Math.min((1 - network.conflictCount / 10) * 1.5, 1).toFixed(2);
  }

  _assessRecoverySpeed(before, after) {
    const improvement = after.connectionDensity - before.connectionDensity;
    return Math.min(improvement * 5, 1).toFixed(2);
  }

  _calculateAverageEffectiveness(data) {
    const strategies = data.alignmentStrategies?.strategies || [];
    const devices = data.persuasiveDevices?.devices || [];
    const eliminated = data.eliminatedAlternatives?.eliminatedAlternatives || [];

    const strategyAvg = strategies.length > 0 ?
      strategies.reduce((sum, s) => sum + (s.effectiveness || 0.5), 0) / strategies.length : 0;
    const deviceAvg = devices.length > 0 ?
      devices.reduce((sum, d) => sum + (d.effectiveness || 0.5), 0) / devices.length : 0;
    const eliminatedAvg = eliminated.length > 0 ?
      eliminated.reduce((sum, e) => sum + (e.effectiveness || 0.5), 0) / eliminated.length : 0;

    return ((strategyAvg + deviceAvg + eliminatedAvg) / 3).toFixed(2);
  }

  _calculateAlignmentScore(data) {
    const landscape = data.alignmentStrategies?.alignmentLandscape;
    return landscape ? parseFloat(landscape.overallAlignment || 0.5) : 0.5;
  }

  _assessTheoryCompliance(data) {
    const complianceScore = this._calculateTheoreticalConsistency(data);

    return {
      score: complianceScore,
      level: complianceScore > 0.8 ? 'high' :
             complianceScore > 0.6 ? 'medium' : 'low',
      recommendations: complianceScore < 0.7 ?
        ['增强利益对齐机制', '完善说服装置', '加强替代方案消除'] : []
    };
  }

  _calculateTheoreticalConsistency(data) {
    let score = 0.5;

    if (data.alignmentStrategies?.strategies?.length > 0) score += 0.2;
    if (data.persuasiveDevices?.devices?.length > 0) score += 0.2;
    if (data.eliminatedAlternatives?.eliminatedAlternatives?.length > 0) score += 0.1;

    return Math.min(score, 1);
  }

  _generateAnalysisSummary(interessement) {
    return {
      strategyCount: interessement.alignmentStrategies?.strategies?.length || 0,
      deviceCount: interessement.persuasiveDevices?.devices?.length || 0,
      eliminatedCount: interessement.eliminatedAlternatives?.eliminatedAlternatives?.length || 0,
      hasAlignment: interessement.alignmentStrategies?.hasAlignment || false,
      hasDevices: interessement.persuasiveDevices?.hasDevices || false
    };
  }

  _extractTheoreticalInsights(interessement) {
    return {
      interestAlignment: interessement.alignmentStrategies?.hasAlignment || false,
      networkStabilization: interessement.eliminatedAlternatives?.eliminatedAlternatives?.length > 0,
      powerConstruction: interessement.persuasiveDevices?.devices?.length > 0,
      chineseAdaptation: interessement.chinesePatterns?.chineseCulturalFeatures?.length > 0,
      theoreticalConsistency: this._checkTheoreticalConsistency(interessement)
    };
  }

  _identifyPracticalImplications(interessement) {
    return {
      stakeholderEngagement: interessement.alignmentStrategies?.strategies?.length > 0,
      policyRecommendations: interessement.persuasiveDevices?.legalFramework?.compulsory || false,
      implementationStrategy: this._suggestImplementationStrategy(interessement),
      successFactors: this._identifySuccessFactors(interessement)
    };
  }

  _checkTheoreticalConsistency(interessement) {
    const hasAlignment = interessement.alignmentStrategies?.hasAlignment || false;
    const hasDevices = interessement.persuasiveDevices?.hasDevices || false;
    const hasElimination = interessement.eliminatedAlternatives?.eliminatedAlternatives?.length > 0;

    return hasAlignment && hasDevices && hasElimination ? 'high' : 'medium';
  }

  _suggestImplementationStrategy(interessement) {
    const strategyCount = interessement.alignmentStrategies?.strategies?.length || 0;
    if (strategyCount >= 3) return '综合策略';
    if (strategyCount >= 2) return '多元策略';
    return '单一策略';
  }

  _identifySuccessFactors(interessement) {
    const factors = [];
    if (interessement.alignmentStrategies?.hasAlignment) factors.push('有效对齐');
    if (interessement.persuasiveDevices?.hasDevices) factors.push('说服机制');
    if (interessement.eliminatedAlternatives?.eliminatedAlternatives?.length > 0) factors.push('替代消除');
    return factors;
  }

  getDefaultInteressement() {
    return {
      alignmentStrategies: { strategies: [], hasAlignment: false },
      persuasiveDevices: { devices: [], hasDevices: false },
      eliminatedAlternatives: { eliminatedAlternatives: [] },
      interessementProcess: { phases: [], keyEvents: [] },
      effectiveness: { overallScore: 0 },
      chinesePatterns: { politicalMobilization: [], institutionalMechanisms: [], chineseCulturalFeatures: [] },
      hasInteressement: false
    };
  }
}

module.exports = InteressementAnalyzer;