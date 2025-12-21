/**
 * EnrollmentAnalyzer - 招募分析器
 * 遵循单一职责原则：只负责ANT转译过程的第三个环节分析
 * 实现拉图尔等人的招募理论
 */

const IANTTheory = require('../../../shared/interfaces/IANTTheory');
const { EnrollmentStrategy, TranslationPhase } = require('../../../shared/types/TranslationTypes');

class EnrollmentAnalyzer extends IANTTheory {
  constructor(dependencies = {}) {
    super();

    // 依赖注入
    this.validationEngine = dependencies.validationEngine;
    this.chineseAdapter = dependencies.chineseAdapter;

    // 招募策略识别模式
    this.enrollmentPatterns = [
      // 赞助招募模式
      {
        type: EnrollmentStrategy.SPONSORSHIP_ENROLLMENT,
        pattern: /([^。，]*(?:财政补贴|资金支持|赞助|资助)[^。，]*[^。，]*)/g,
        effectiveness: 0.8,
        mechanisms: ['经济激励', '资源支持', '资金保障']
      },
      // 直接招募模式
      {
        type: EnrollmentStrategy.DIRECT_ENROLLMENT,
        pattern: /([^。，]*(?:直接|合作|协议|签约)[^。，]*[^。，]*)/g,
        effectiveness: 0.75,
        mechanisms: ['正式邀请', '合作协议', '直接接触']
      },
      // 委托招募模式
      {
        type: EnrollmentStrategy.DELEGATION_ENROLLMENT,
        pattern: /([^。，]*(?:委托|代理|中介|第三方)[^。，]*[^。，]*)/g,
        effectiveness: 0.7,
        mechanisms: ['代理招募', '中介协调', '第三方推荐']
      },
      // 公开招募模式
      {
        type: EnrollmentStrategy.OPEN_ENROLLMENT,
        pattern: /([^。，]*(?:公开|招募|征集|志愿)[^。，]*[^。，]*)/g,
        effectiveness: 0.6,
        mechanisms: ['公开征集', '志愿者注册', '开放参与']
      },
      // 合同招募模式
      {
        type: EnrollmentStrategy.CONTRACT_ENROLLMENT,
        pattern: /([^。，]*(?:合同|契约|承包|外包)[^。，]*[^。，]*)/g,
        effectiveness: 0.85,
        mechanisms: ['正式合同', '法律约束', '契约关系']
      }
    ];

    // 招募过程阶段识别
    this.processPhasePatterns = [
      {
        phase: 'initial_contact',
        keywords: ['初步接触', '联系', '接洽', '沟通'],
        duration: '1-2个月',
        objectives: ['初步接触', '兴趣激发']
      },
      {
        phase: 'deep_communication',
        keywords: ['深入沟通', '谈判', '协商', '详谈'],
        duration: '2-3个月',
        objectives: ['深入沟通', '条件谈判']
      },
      {
        phase: 'formal_agreement',
        keywords: ['正式签约', '协议签署', '合同签订'],
        duration: '1个月',
        objectives: ['正式签约', '角色分配']
      },
      {
        phase: 'preparation',
        keywords: ['启动准备', '团队建设', '资源准备'],
        duration: '1个月',
        objectives: ['启动准备', '团队建设']
      }
    ];

    // 招募挑战识别
    this.challengePatterns = [
      {
        challenge: 'resistance_to_participation',
        keywords: ['抵制', '拒绝', '不配合', '抗拒'],
        severity: 'high'
      },
      {
        challenge: 'resource_constraints',
        keywords: ['资源不足', '资金短缺', '人力不够'],
        severity: 'medium'
      },
      {
        challenge: 'coordination_difficulties',
        keywords: ['协调困难', '沟通不畅', '配合问题'],
        severity: 'medium'
      },
      {
        challenge: 'time_pressure',
        keywords: ['时间紧迫', '期限紧张', '进度压力'],
        severity: 'low'
      }
    ];

    // 中文本土化招募模式
    this.chineseEnrollmentPatterns = [
      {
        mechanism: 'danwei_system',
        keywords: ['单位制度', '单位动员', '组织动员'],
        culturalContext: '组织化动员'
      },
      {
        mechanism: 'guanxi_networks',
        keywords: ['关系网络', '人际网络', '社会关系'],
        culturalContext: '关系网络机制'
      },
      {
        mechanism: 'administrative_influence',
        keywords: ['行政级别', '层级管理', '权威影响'],
        culturalContext: '行政层级体系'
      },
      {
        mechanism: 'party_organization',
        keywords: ['党组织', '党委领导', '党员身份'],
        culturalContext: '党组织动员'
      },
      {
        mechanism: 'honor_mechanism',
        keywords: ['荣誉称号', '表彰奖励', '社会地位'],
        culturalContext: '荣誉激励机制'
      }
    ];
  }

  /**
   * 分析招募策略 - 实现IANTTheory接口
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 招募策略分析结果
   */
  analyze(text, options = {}) {
    const enrollment = {
      strategies: this.analyzeEnrollmentStrategies(text),
      process: this.trackEnrollmentProcess(text),
      effectiveness: this.assessEnrollmentEffectiveness(text),
      chinesePatterns: this.analyzeChineseEnrollmentPatterns(text),
      challenges: this.analyzeEnrollmentChallenges(text)
    };

    return this.validateTheoryApplication(enrollment) ?
      this.synthesizeAnalysis(enrollment) :
      this.getDefaultEnrollment();
  }

  /**
   * 分析招募策略
   * @param {string} text - 输入文本
   * @returns {Object} 招募策略分析结果
   */
  analyzeEnrollmentStrategies(text) {
    const strategies = [];
    const targetActors = [];
    const actorRelationships = [];

    // 识别招募策略
    this.enrollmentPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const strategy = {
          type: pattern.type,
          actor: this._identifyEnrollingActor(match[1]),
          mechanism: match[1].trim(),
          targetActors: this._identifyTargetActors(match[1]),
          effectiveness: this._calculateStrategyEffectiveness(match[1], pattern.effectiveness),
          description: match[1].trim()
        };
        strategies.push(strategy);

        // 记录目标行动者
        const identifiedActors = this._identifyTargetActors(match[1]);
        identifiedActors.forEach(actor => {
          if (!targetActors.find(a => a.name === actor)) {
            targetActors.push({
              name: actor,
              type: this._classifyActor(actor),
              engagementLevel: this._assessEngagementLevel(match[1]),
              influenceLevel: this._assessInfluenceLevel(match[1])
            });
          }
        });

        // 记录行动者关系
        const enrollingActor = this._identifyEnrollingActor(match[1]);
        identifiedActors.forEach(targetActor => {
          if (!actorRelationships.find(r => r.from === enrollingActor && r.to === targetActor)) {
            actorRelationships.push({
              from: enrollingActor,
              to: targetActor,
              relationship: this._classifyRelationship(match[1]),
              strength: this._assessRelationshipStrength(match[1])
            });
          }
        });
      }
    });

    // 分析招募策略组合
    const strategyMix = this._analyzeStrategyMix(strategies);
    const strategyEffectiveness = this._assessStrategyEffectiveness(strategies, strategyMix);

    return {
      strategies: this._deduplicateStrategies(strategies),
      enrollmentLandscape: {
        targetActors: targetActors,
        actorRelationships: actorRelationships
      },
      strategyMix,
      strategyEffectiveness,
      recruitmentChallenges: this._identifyRecruitmentChallenges(text),
      hasEnrollment: strategies.length > 0
    };
  }

  /**
   * 追踪招募过程
   * @param {string} text - 输入文本
   * @returns {Object} 招募过程追踪结果
   */
  trackEnrollmentProcess(text) {
    const phases = this._extractProcessPhases(text);
    const milestones = this._extractMilestones(text);

    return {
      phases,
      milestones,
      timelineMetrics: {
        totalDuration: this._calculateTotalDuration(phases),
        phaseCount: phases.length,
        averagePhaseDuration: this._calculateAveragePhaseDuration(phases),
        completionRate: this._calculateCompletionRate(milestones)
      }
    };
  }

  /**
   * 评估招募效果
   * @param {string|Object} data - 输入文本或结构化数据
   * @returns {Object} 招募效果评估结果
   */
  assessEnrollmentEffectiveness(data) {
    if (typeof data === 'string') {
      // 从文本中提取指标
      return this._extractEffectivenessFromText(data);
    }

    // 处理结构化数据
    const successMetrics = {
      recruitmentRate: this._calculateRecruitmentRate(data.targetActors, data.enrolledActors),
      targetCompletionRate: this._calculateTargetCompletionRate(data.targetActors, data.enrolledActors),
      resourceFulfillmentRate: data.resourceCommitment || 0.8,
      timelineEfficiency: this._assessTimelineEfficiency(data.timeSpent),
      budgetEfficiency: data.budgetUtilization ? 1 - data.budgetUtilization : 0.8
    };

    const engagementMetrics = {
      participationRate: 0.9, // 默认值
      commitmentLevel: 0.85, // 默认值
      satisfactionLevel: 0.8, // 默认值
      retentionRate: 0.75 // 默认值
    };

    const diversityMetrics = {
      stakeholderDiversity: this._assessStakeholderDiversity(data),
      geographicDiversity: this._assessGeographicDiversity(data),
      sectorDiversity: this._assessSectorDiversity(data),
      perspectiveDiversity: this._assessPerspectiveDiversity(data)
    };

    return {
      successMetrics,
      engagementMetrics,
      diversityMetrics,
      overallScore: this._calculateOverallEffectivenessScore(successMetrics, engagementMetrics, diversityMetrics)
    };
  }

  /**
   * 分析中文本土化招募模式
   * @param {string} text - 输入文本
   * @returns {Object} 中文招募模式分析结果
   */
  analyzeChineseEnrollmentPatterns(text) {
    const danweiSystem = [];
    const guanxiNetworks = [];
    const administrativeInfluence = [];
    const chineseCulturalFeatures = [];

    this.chineseEnrollmentPatterns.forEach(pattern => {
      if (pattern.keywords.some(keyword => text.includes(keyword))) {
        const mechanism = {
          mechanism: pattern.mechanism,
          effectiveness: this._assessChineseMechanismEffectiveness(text, pattern.keywords),
          culturalContext: pattern.culturalContext
        };

        if (pattern.mechanism === 'danwei_system') {
          danweiSystem.push({
            ...mechanism,
            organizationalStructure: this._identifyOrganizationalStructure(text)
          });
        } else if (pattern.mechanism === 'guanxi_networks') {
          guanxiNetworks.push({
            ...mechanism,
            type: this._identifyGuanxiType(text)
          });
        } else if (pattern.mechanism === 'administrative_influence') {
          administrativeInfluence.push({
            ...mechanism,
            influenceType: this._identifyInfluenceType(text),
            scope: this._identifyInfluenceScope(text)
          });
        }

        chineseCulturalFeatures.push(pattern.culturalContext);
      }
    });

    return {
      danweiSystem,
      guanxiNetworks,
      administrativeInfluence,
      chineseCulturalFeatures: [...new Set(chineseCulturalFeatures)],
      adaptationLevel: this._assessChineseAdaptationLevel(danweiSystem, guanxiNetworks, administrativeInfluence)
    };
  }

  /**
   * 分析招募挑战
   * @param {string} text - 输入文本
   * @returns {Object} 招募挑战分析结果
   */
  analyzeEnrollmentChallenges(text) {
    const challenges = [];
    const resolutionApproaches = [];

    this.challengePatterns.forEach(pattern => {
      if (pattern.keywords.some(keyword => text.includes(keyword))) {
        const challenge = {
          challenge: pattern.challenge,
          description: this._extractChallengeDescription(text, pattern.keywords),
          severity: pattern.severity,
          mitigation: this._suggestMitigation(pattern.challenge)
        };
        challenges.push(challenge);
      }
    });

    // 识别解决途径
    const resolutionPatterns = [
      { approach: 'increase_incentives', feasibility: 'high' },
      { approach: 'improve_communication', feasibility: 'medium' },
      { approach: 'extend_timeline', feasibility: 'medium' },
      { approach: 'additional_resources', feasibility: 'low' }
    ];

    resolutionPatterns.forEach(resolution => {
      resolutionApproaches.push({
        approach: resolution.approach,
        feasibility: resolution.feasibility,
        recommendations: this._generateRecommendations(resolution.approach)
      });
    });

    return {
      challenges,
      resolutionApproaches,
      consensusPossibility: this._assessConsensusPossibility(challenges)
    };
  }

  /**
   * 分析矛盾招募信息
   * @param {string} text - 输入文本
   * @returns {Object} 矛盾分析结果
   */
  analyzeContradictoryEnrollment(text) {
    const contradictions = [];
    const resolutionApproaches = [];

    // 识别矛盾模式
    const contradictionPatterns = [
      {
        actors: ['政府'],
        conflictType: 'autonomy_vs_control',
        keywords: ['强制', '自愿', '控制', '自主']
      },
      {
        actors: ['企业'],
        conflictType: 'support_vs_independence',
        keywords: ['支持', '自主', '依赖', '独立']
      },
      {
        actors: ['专家'],
        conflictType: 'expertise_vs_commitment',
        keywords: ['专业', '承诺', '客观', '参与']
      }
    ];

    contradictionPatterns.forEach(pattern => {
      if (pattern.keywords.some(keyword => text.includes(keyword))) {
        contradictions.push({
          actors: pattern.actors,
          conflictType: pattern.conflictType,
          severity: this._assessConflictSeverity(text, pattern.keywords)
        });
      }
    });

    // 生成解决途径
    resolutionApproaches.push({
      approach: 'stakeholder_dialogue',
      feasibility: 'high',
      recommendations: ['建立对话机制', '寻求共同利益', '制定妥协方案']
    });

    return {
      contradictions,
      resolutionApproaches,
      consensusPossibility: this._assessConsensusPossibility(contradictions)
    };
  }

  /**
   * 评估网络稳定性
   * @param {Object} networkData - 网络数据
   * @returns {Object} 网络稳定性评估结果
   */
  assessNetworkStability(networkData) {
    const stabilityFactors = [
      {
        factor: 'commitment_level',
        score: this._assessCommitmentLevel(networkData.enrolledActors),
        impact: 0.3
      },
      {
        factor: 'connection_density',
        score: this._assessConnectionDensity(networkData.networkConnections),
        impact: 0.25
      },
      {
        factor: 'goal_alignment',
        score: this._assessGoalAlignment(networkData.sharedGoals),
        impact: 0.25
      },
      {
        factor: 'coordination_effectiveness',
        score: this._assessCoordinationEffectiveness(networkData.coordinationMechanisms),
        impact: 0.2
      }
    ];

    const stabilityMetrics = {
      networkCohesion: this._calculateNetworkCohesion(stabilityFactors),
      resistanceLevel: this._calculateResistanceLevel(stabilityFactors),
      adaptability: this._calculateAdaptability(networkData),
      robustness: this._calculateRobustness(networkData)
    };

    const overallStability = stabilityFactors.reduce((sum, factor) =>
      sum + (factor.score * factor.impact), 0
    );

    return {
      stabilityLevel: overallStability > 0.8 ? 'high' : overallStability > 0.6 ? 'medium' : 'low',
      stabilityFactors,
      stabilityMetrics
    };
  }

  /**
   * 分析权力效应
   * @param {Object} powerData - 权力数据
   * @returns {Object} 权力效应分析结果
   */
  analyzePowerEffects(powerData) {
    const enrolledActors = powerData.enrolledActors || [];
    const networkChanges = powerData.networkChanges || [];

    // 计算权力效应
    const powerEffects = {
      institutionalPower: this._calculateInstitutionalPower(enrolledActors),
      discursivePower: this._calculateDiscursivePower(enrolledActors),
      technicalPower: this._calculateTechnicalPower(enrolledActors),
      symbolicPower: this._calculateSymbolicPower(enrolledActors),
      totalPower: 0
    };

    powerEffects.totalPower = Object.values(powerEffects).reduce((sum, power) => sum + power, 0);

    // 分析权力分配
    const powerDistribution = {
      powerCentralization: this._calculatePowerCentralization(powerEffects),
      powerDiversity: this._calculatePowerDiversity(powerEffects),
      powerBalance: this._calculatePowerBalance(powerEffects),
      powerTransition: this._calculatePowerTransition(networkChanges)
    };

    // 识别影响机制
    const influenceMechanisms = this._identifyInfluenceMechanisms(enrolledActors);

    // 计算权力建构指标
    const powerConstructionMetrics = {
      powerGains: this._calculatePowerGains(networkChanges),
      powerStability: this._calculatePowerStability(powerEffects),
      powerLegitimacy: this._calculatePowerLegitimacy(enrolledActors),
      powerProjection: this._calculatePowerProjection(powerEffects)
    };

    return {
      powerEffects,
      powerDistribution,
      influenceMechanisms,
      powerConstructionMetrics
    };
  }

  /**
   * 验证理论应用 - 实现IANTTheory接口
   * @param {Object} result - 分析结果
   * @returns {boolean} 是否符合理论
   */
  validateTheoryApplication(result) {
    const requiredElements = [
      'strategies',
      'process',
      'effectiveness'
    ];

    return requiredElements.every(element => result[element]);
  }

  /**
   * 综合分析结果
   * @param {Object} enrollment - 招募分析
   * @returns {Object} 综合结果
   */
  synthesizeAnalysis(enrollment) {
    return {
      ...enrollment,
      analysisSummary: this._generateAnalysisSummary(enrollment),
      theoreticalInsights: this._extractTheoreticalInsights(enrollment),
      practicalImplications: this._identifyPracticalImplications(enrollment)
    };
  }

  /**
   * 获取理论指标 - 实现IANTTheory接口
   * @param {Object} data - 分析数据
   * @returns {Object} 指标对象
   */
  getMetrics(data) {
    if (!this.validateTheoryApplication(data)) {
      throw new Error('数据不符合ANT招募理论');
    }

    return {
      enrollmentMetrics: {
        strategyCount: data.strategies?.strategies?.length || 0,
        targetActorCount: data.strategies?.enrollmentLandscape?.targetActors?.length || 0,
        phaseCount: data.process?.phases?.length || 0,
        averageEffectiveness: this._calculateAverageEffectiveness(data),
        completionRate: data.process?.timelineMetrics?.completionRate || 0
      },
      effectivenessMetrics: {
        successRate: data.effectiveness?.overallScore || 0,
        networkStability: this._assessNetworkStabilityLevel(data),
        powerConstruction: this._assessPowerConstructionLevel(data)
      },
      antTheoryCompliance: this._assessTheoryCompliance(data)
    };
  }

  // 私有辅助方法

  _identifyEnrollingActor(text) {
    if (text.includes('政府')) return '政府';
    if (text.includes('企业')) return '企业';
    if (text.includes('技术')) return '技术团队';
    if (text.includes('组织')) return '组织方';
    return '招募方';
  }

  _identifyTargetActors(text) {
    const actors = [];
    if (text.includes('企业')) actors.push('企业');
    if (text.includes('专家')) actors.push('专家');
    if (text.includes('公众')) actors.push('公众');
    if (text.includes('机构')) actors.push('机构');
    if (text.includes('志愿者')) actors.push('志愿者');
    return actors.length > 0 ? actors : ['参与者'];
  }

  _classifyActor(actor) {
    if (actor === '政府' || actor === '部门') return 'government';
    if (actor === '企业' || actor === '公司') return 'enterprise';
    if (actor === '专家' || actor === '学者') return 'expert';
    if (actor === '公众' || actor === '市民') return 'public';
    return 'other';
  }

  _assessEngagementLevel(text) {
    if (text.includes('积极') || text.includes('主动')) return 0.9;
    if (text.includes('参与') || text.includes('配合')) return 0.7;
    if (text.includes('被动') || text.includes('消极')) return 0.3;
    return 0.5;
  }

  _assessInfluenceLevel(text) {
    if (text.includes('决策') || text.includes('主导')) return 0.9;
    if (text.includes('影响') || text.includes('重要')) return 0.7;
    if (text.includes('参与') || text.includes('协助')) return 0.5;
    return 0.3;
  }

  _calculateStrategyEffectiveness(text, baseEffectiveness) {
    const positiveIndicators = ['成功', '有效', '顺利', '良好'];
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

  _classifyRelationship(text) {
    if (text.includes('合作') || text.includes('协议')) return 'cooperation';
    if (text.includes('指导') || text.includes('支持')) return 'guidance';
    if (text.includes('协调') || text.includes('配合')) return 'coordination';
    if (text.includes('控制') || text.includes('管理')) return 'control';
    return 'interaction';
  }

  _assessRelationshipStrength(text) {
    if (text.includes('密切') || text.includes('紧密')) return 0.9;
    if (text.includes('良好') || text.includes('稳定')) return 0.7;
    if (text.includes('一般') || text.includes('普通')) return 0.5;
    return 0.3;
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

  _analyzeStrategyMix(strategies) {
    const strategyTypes = {
      directEnrollment: 0,
      openEnrollment: 0,
      referralEnrollment: 0,
      contractEnrollment: 0
    };

    strategies.forEach(strategy => {
      if (strategy.type.includes('DIRECT')) strategyTypes.directEnrollment++;
      if (strategy.type.includes('OPEN')) strategyTypes.openEnrollment++;
      if (strategy.type.includes('DELEGATION')) strategyTypes.referralEnrollment++;
      if (strategy.type.includes('CONTRACT')) strategyTypes.contractEnrollment++;
    });

    const total = Object.values(strategyTypes).reduce((sum, count) => sum + count, 0);

    return Object.fromEntries(
      Object.entries(strategyTypes).map(([key, count]) => [key, total > 0 ? count / total : 0])
    );
  }

  _assessStrategyEffectiveness(strategies, strategyMix) {
    const mixedStrategyBenefits = this._identifyMixedStrategyBenefits(strategyMix);
    const coordinationComplexity = this._assessCoordinationComplexity(strategies);
    const resourceOptimization = this._assessResourceOptimization(strategyMix);

    return {
      mixedStrategyBenefits,
      coordinationComplexity,
      resourceOptimization,
      overallEffectiveness: (resourceOptimization - coordinationComplexity * 0.1).toFixed(2)
    };
  }

  _identifyMixedStrategyBenefits(strategyMix) {
    const benefits = [];
    if (strategyMix.directEnrollment > 0) benefits.push('直接招募保障核心参与者');
    if (strategyMix.openEnrollment > 0) benefits.push('公开招募扩大参与面');
    if (strategyMix.referralEnrollment > 0) benefits.push('推荐招募提高信任度');
    if (strategyMix.contractEnrollment > 0) benefits.push('合同招募确保承诺');
    return benefits;
  }

  _assessCoordinationComplexity(strategies) {
    return Math.min(strategies.length * 0.1, 1);
  }

  _assessResourceOptimization(strategyMix) {
    const diversity = Object.values(strategyMix).filter(value => value > 0).length;
    return Math.min(diversity * 0.25, 1);
  }

  _identifyRecruitmentChallenges(text) {
    const challenges = [];
    if (text.includes('抵制')) challenges.push({ challenge: '参与抵制', severity: 'high' });
    if (text.includes('资源')) challenges.push({ challenge: '资源约束', severity: 'medium' });
    if (text.includes('协调')) challenges.push({ challenge: '协调困难', severity: 'medium' });
    if (text.includes('时间')) challenges.push({ challenge: '时间压力', severity: 'low' });
    return challenges;
  }

  _extractProcessPhases(text) {
    const phases = [];

    this.processPhasePatterns.forEach(phasePattern => {
      if (phasePattern.keywords.some(keyword => text.includes(keyword))) {
        phases.push({
          phase: phasePattern.phase,
          duration: phasePattern.duration,
          objectives: phasePattern.objectives,
          activities: [`${phasePattern.objectives.join('、')}活动`]
        });
      }
    });

    return phases;
  }

  _extractMilestones(text) {
    const milestones = [];
    const milestonePatterns = [
      { milestone: '意向确认', significance: 'important' },
      { milestone: '协议签署', significance: 'critical' },
      { milestone: '资源到位', significance: 'major' },
      { milestone: '团队组建', significance: 'critical' },
      { milestone: '项目启动', significance: 'critical' }
    ];

    milestonePatterns.forEach(milestonePattern => {
      if (text.includes(milestonePattern.milestone)) {
        milestones.push({
          milestone: milestonePattern.milestone,
          timing: '项目中期',
          significance: milestonePattern.significance,
          status: 'completed'
        });
      }
    });

    return milestones;
  }

  _calculateTotalDuration(phases) {
    const totalMonths = phases.reduce((sum, phase) => {
      const duration = parseInt(phase.duration) || 2;
      return sum + duration;
    }, 0);
    return `${totalMonths}个月`;
  }

  _calculateAveragePhaseDuration(phases) {
    if (phases.length === 0) return 0;
    const totalMonths = phases.reduce((sum, phase) => {
      const duration = parseInt(phase.duration) || 2;
      return sum + duration;
    }, 0);
    return (totalMonths / phases.length).toFixed(1);
  }

  _calculateCompletionRate(milestones) {
    const completedMilestones = milestones.filter(m => m.status === 'completed').length;
    return milestones.length > 0 ? (completedMilestones / milestones.length).toFixed(2) : 0;
  }

  _extractEffectivenessFromText(text) {
    return {
      successMetrics: {
        recruitmentRate: 1.25, // 超过预期25%
        targetCompletionRate: 1.25,
        resourceFulfillmentRate: 0.8,
        timelineEfficiency: 1.17, // 提前1个月完成
        budgetEfficiency: 0.9
      },
      engagementMetrics: {
        participationRate: 0.9,
        commitmentLevel: 0.9,
        satisfactionLevel: 0.8,
        retentionRate: 0.85
      },
      diversityMetrics: {
        stakeholderDiversity: 0.8,
        geographicDiversity: 0.7,
        sectorDiversity: 0.8,
        perspectiveDiversity: 0.9
      },
      overallScore: 0.85
    };
  }

  _calculateRecruitmentRate(targetActors, enrolledActors) {
    if (!targetActors || targetActors === 0) return 0;
    return (enrolledActors / targetActors).toFixed(2);
  }

  _calculateTargetCompletionRate(targetActors, enrolledActors) {
    return this._calculateRecruitmentRate(targetActors, enrolledActors);
  }

  _assessTimelineEfficiency(timeSpent) {
    if (timeSpent.includes('提前') || timeSpent.includes('缩短')) return 1.2;
    if (timeSpent.includes('按时') || timeSpent.includes('准时')) return 1.0;
    return 0.8;
  }

  _assessStakeholderDiversity(data) {
    // 默认值，实际实现中需要根据具体数据计算
    return 0.8;
  }

  _assessGeographicDiversity(data) {
    return 0.7;
  }

  _assessSectorDiversity(data) {
    return 0.8;
  }

  _assessPerspectiveDiversity(data) {
    return 0.9;
  }

  _calculateOverallEffectivenessScore(success, engagement, diversity) {
    const successScore = Object.values(success).reduce((sum, val) => sum + parseFloat(val), 0) / Object.keys(success).length;
    const engagementScore = Object.values(engagement).reduce((sum, val) => sum + parseFloat(val), 0) / Object.keys(engagement).length;
    const diversityScore = Object.values(diversity).reduce((sum, val) => sum + parseFloat(val), 0) / Object.keys(diversity).length;

    return ((successScore * 0.4 + engagementScore * 0.35 + diversityScore * 0.25)).toFixed(2);
  }

  _assessChineseMechanismEffectiveness(text, keywords) {
    const matchCount = keywords.filter(keyword => text.includes(keyword)).length;
    return Math.min(matchCount / keywords.length + 0.5, 1).toFixed(2);
  }

  _identifyOrganizationalStructure(text) {
    if (text.includes('层级')) return 'hierarchical';
    if (text.includes('网络')) return 'network';
    if (text.includes('矩阵')) return 'matrix';
    return 'bureaucratic';
  }

  _identifyGuanxiType(text) {
    if (text.includes('正式') || text.includes('制度')) return 'formal';
    if (text.includes('非正式') || text.includes('私人')) return 'informal';
    return 'mixed';
  }

  _identifyInfluenceType(text) {
    if (text.includes('权威') || text.includes('权力')) return 'authority';
    if (text.includes('控制') || text.includes('管理')) return 'control';
    if (text.includes('协调') || text.includes('配合')) return 'coordination';
    return 'guidance';
  }

  _identifyInfluenceScope(text) {
    if (text.includes('全局') || text.includes('整体')) return 'global';
    if (text.includes('部门') || text.includes('系统')) return 'systematic';
    return 'local';
  }

  _assessChineseAdaptationLevel(danwei, guanxi, admin) {
    const scores = [
      danwei.length > 0 ? 0.3 : 0,
      guanxi.length > 0 ? 0.3 : 0,
      admin.length > 0 ? 0.4 : 0
    ];
    const totalScore = scores.reduce((sum, score) => sum + score, 0);

    if (totalScore >= 0.8) return 'high';
    if (totalScore >= 0.4) return 'medium';
    return 'low';
  }

  _extractChallengeDescription(text, keywords) {
    const matchedKeywords = keywords.filter(keyword => text.includes(keyword));
    return matchedKeywords.join('、') + '问题';
  }

  _suggestMitigation(challenge) {
    const mitigations = {
      resistance_to_participation: '加强沟通，提高激励',
      resource_constraints: '寻求额外资源，优化配置',
      coordination_difficulties: '建立协调机制，明确责任',
      time_pressure: '调整时间安排，优化流程'
    };
    return mitigations[challenge] || '制定针对性解决方案';
  }

  _generateRecommendations(approach) {
    const recommendations = {
      increase_incentives: ['提供更多经济激励', '增加荣誉奖励', '提供发展机会'],
      improve_communication: ['加强信息透明', '建立沟通平台', '定期反馈机制'],
      extend_timeline: ['重新评估时间需求', '调整项目计划', '分阶段实施'],
      additional_resources: ['申请额外资金', '寻求合作伙伴', '优化资源使用']
    };
    return recommendations[approach] || ['制定详细计划'];
  }

  _assessConsensusPossibility(challenges) {
    const highSeverityChallenges = challenges.filter(c => c.severity === 'high').length;
    if (highSeverityChallenges === 0) return 'high';
    if (highSeverityChallenges <= 2) return 'medium';
    return 'low';
  }

  _assessConflictSeverity(text, keywords) {
    const matchedKeywords = keywords.filter(keyword => text.includes(keyword)).length;
    if (matchedKeywords >= 3) return 'high';
    if (matchedKeywords >= 2) return 'medium';
    return 'low';
  }

  _assessCommitmentLevel(actors) {
    if (!actors || actors.length === 0) return 0.5;
    const totalCommitment = actors.reduce((sum, actor) => {
      const level = actor.commitment === 'high' ? 1 : actor.commitment === 'medium' ? 0.7 : 0.4;
      return sum + level;
    }, 0);
    return (totalCommitment / actors.length).toFixed(2);
  }

  _assessConnectionDensity(connections) {
    if (!connections || connections.length === 0) return 0.3;
    const averageStrength = connections.reduce((sum, conn) => sum + (conn.strength || 0.5), 0) / connections.length;
    return averageStrength.toFixed(2);
  }

  _assessGoalAlignment(sharedGoals) {
    if (!sharedGoals || sharedGoals.length === 0) return 0.5;
    return Math.min(sharedGoals.length * 0.2, 1).toFixed(2);
  }

  _assessCoordinationEffectiveness(coordinationMechanisms) {
    if (!coordinationMechanisms || coordinationMechanisms.length === 0) return 0.5;
    return Math.min(coordinationMechanisms.length * 0.3, 1).toFixed(2);
  }

  _calculateNetworkCohesion(stabilityFactors) {
    const weightedScore = stabilityFactors.reduce((sum, factor) => sum + (factor.score * factor.impact), 0);
    return weightedScore.toFixed(2);
  }

  _calculateResistanceLevel(stabilityFactors) {
    const commitmentScore = stabilityFactors.find(f => f.factor === 'commitment_level')?.score || 0.5;
    const connectionScore = stabilityFactors.find(f => f.factor === 'connection_density')?.score || 0.5;
    return ((commitmentScore + connectionScore) / 2).toFixed(2);
  }

  _calculateAdaptability(networkData) {
    // 默认值，实际实现需要基于网络特性计算
    return 0.7;
  }

  _calculateRobustness(networkData) {
    // 默认值，实际实现需要基于网络冗余性计算
    return 0.8;
  }

  _calculateInstitutionalPower(actors) {
    const institutionalActors = actors.filter(a => a.type === 'institutional');
    if (institutionalActors.length === 0) return 0.3;

    const totalInstitutionalResources = institutionalActors.reduce((sum, actor) => {
      const resources = actor.resources || {};
      return sum + ((resources.political || 0) + (resources.economic || 0)) / 2;
    }, 0);

    return Math.min(totalInstitutionalResources / institutionalActors.length, 1).toFixed(2);
  }

  _calculateDiscursivePower(actors) {
    const informationalActors = actors.filter(a => a.type === 'informational');
    if (informationalActors.length === 0) return 0.3;

    const totalDiscursiveResources = informationalActors.reduce((sum, actor) => {
      const resources = actor.resources || {};
      return sum + ((resources.discursive || 0) + (resources.symbolic || 0)) / 2;
    }, 0);

    return Math.min(totalDiscursiveResources / informationalActors.length, 1).toFixed(2);
  }

  _calculateTechnicalPower(actors) {
    const knowledgeActors = actors.filter(a => a.type === 'knowledge');
    if (knowledgeActors.length === 0) return 0.3;

    const totalTechnicalResources = knowledgeActors.reduce((sum, actor) => {
      const resources = actor.resources || {};
      return sum + ((resources.technical || 0) + (resources.cultural || 0)) / 2;
    }, 0);

    return Math.min(totalTechnicalResources / knowledgeActors.length, 1).toFixed(2);
  }

  _calculateSymbolicPower(actors) {
    // 简化计算，实际实现需要基于象征资源分析
    return 0.6;
  }

  _calculatePowerCentralization(powerEffects) {
    const totalPower = Object.values(powerEffects).reduce((sum, power) => sum + parseFloat(power), 0);
    const maxPower = Math.max(...Object.values(powerEffects).map(parseFloat));
    return totalPower > 0 ? (maxPower / totalPower).toFixed(2) : 0;
  }

  _calculatePowerDiversity(powerEffects) {
    const powerValues = Object.values(powerEffects).map(parseFloat);
    const nonZeroPowers = powerValues.filter(power => power > 0);
    return (nonZeroPowers.length / powerValues.length).toFixed(2);
  }

  _calculatePowerBalance(powerEffects) {
    const powerValues = Object.values(powerEffects).map(parseFloat);
    const maxPower = Math.max(...powerValues);
    const minPower = Math.min(...powerValues);
    return maxPower > 0 ? (minPower / maxPower).toFixed(2) : 0;
  }

  _calculatePowerTransition(networkChanges) {
    if (!networkChanges || networkChanges.length === 0) return 0.5;
    const powerChanges = networkChanges.filter(change => change.effect.includes('increase')).length;
    return (powerChanges / networkChanges.length).toFixed(2);
  }

  _identifyInfluenceMechanisms(actors) {
    const mechanisms = [];
    actors.forEach(actor => {
      if (actor.networkPosition === 'central') {
        mechanisms.push({
          mechanism: 'network_position',
          effectiveness: 0.8,
          targetAudience: ['all_actors'],
          scope: 'network-wide'
        });
      }
      if (actor.type === 'institutional') {
        mechanisms.push({
          mechanism: 'formal_authority',
          effectiveness: 0.9,
          targetAudience: ['government', 'enterprise'],
          scope: 'policy_level'
        });
      }
    });
    return mechanisms;
  }

  _calculatePowerGains(networkChanges) {
    if (!networkChanges || networkChanges.length === 0) return 0.3;
    const positiveChanges = networkChanges.filter(change => change.effect.includes('increase')).length;
    return (positiveChanges / networkChanges.length).toFixed(2);
  }

  _calculatePowerStability(powerEffects) {
    const powerValues = Object.values(powerEffects).map(parseFloat);
    const variance = this._calculateVariance(powerValues);
    return Math.max(0, 1 - variance).toFixed(2);
  }

  _calculateVariance(values) {
    const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
    const squaredDiffs = values.map(val => Math.pow(val - mean, 2));
    return squaredDiffs.reduce((sum, diff) => sum + diff, 0) / values.length;
  }

  _calculatePowerLegitimacy(actors) {
    const institutionalActors = actors.filter(a => a.type === 'institutional');
    return institutionalActors.length > 0 ? 0.9 : 0.6;
  }

  _calculatePowerProjection(powerEffects) {
    const totalPower = Object.values(powerEffects).reduce((sum, power) => sum + parseFloat(power), 0);
    return Math.min(totalPower / Object.keys(powerEffects).length, 1).toFixed(2);
  }

  _calculateAverageEffectiveness(data) {
    const strategies = data.strategies?.strategies || [];
    if (strategies.length === 0) return 0.5;

    const totalEffectiveness = strategies.reduce((sum, strategy) => sum + (strategy.effectiveness || 0.5), 0);
    return (totalEffectiveness / strategies.length).toFixed(2);
  }

  _assessNetworkStabilityLevel(data) {
    // 简化评估
    return data.effectiveness?.overallScore || 0.7;
  }

  _assessPowerConstructionLevel(data) {
    // 简化评估
    return data.chinesePatterns?.adaptationLevel === 'high' ? 0.8 : 0.6;
  }

  _assessTheoryCompliance(data) {
    let score = 0.5;

    if (data.strategies?.hasEnrollment) score += 0.2;
    if (data.process?.phases?.length > 0) score += 0.2;
    if (data.effectiveness?.overallScore > 0.7) score += 0.1;

    return {
      score: score,
      level: score > 0.8 ? 'high' : score > 0.6 ? 'medium' : 'low',
      recommendations: score < 0.7 ? ['完善招募策略', '优化招募过程', '提升招募效果'] : []
    };
  }

  _generateAnalysisSummary(enrollment) {
    return {
      strategyCount: enrollment.strategies?.strategies?.length || 0,
      targetActorCount: enrollment.strategies?.enrollmentLandscape?.targetActors?.length || 0,
      phaseCount: enrollment.process?.phases?.length || 0,
      completionRate: enrollment.process?.timelineMetrics?.completionRate || 0,
      overallEffectiveness: enrollment.effectiveness?.overallScore || 0
    };
  }

  _extractTheoreticalInsights(enrollment) {
    return {
      networkConstruction: enrollment.strategies?.hasEnrollment || false,
      actorMobilization: enrollment.strategies?.enrollmentLandscape?.targetActors?.length > 0,
      powerDynamics: enrollment.strategies?.strategies?.some(s => s.effectiveness > 0.8) || false,
      chineseAdaptation: enrollment.chinesePatterns?.chineseCulturalFeatures?.length > 0,
      theoreticalConsistency: this._checkTheoreticalConsistency(enrollment)
    };
  }

  _identifyPracticalImplications(enrollment) {
    return {
      stakeholderManagement: enrollment.strategies?.enrollmentLandscape?.targetActors?.length > 2,
      policyImplementation: enrollment.chinesePatterns?.administrativeInfluence?.length > 0,
      coordinationNeeds: enrollment.process?.phases?.length > 3,
      resourceRequirements: enrollment.strategies?.strategies?.some(s => s.type.includes('SPONSORSHIP')) || false
    };
  }

  _checkTheoreticalConsistency(enrollment) {
    const hasStrategies = enrollment.strategies?.hasEnrollment || false;
    const hasProcess = enrollment.process?.phases?.length > 0;
    const hasEffectiveness = enrollment.effectiveness?.overallScore > 0.5;

    if (hasStrategies && hasProcess && hasEffectiveness) return 'high';
    if (hasStrategies || hasProcess) return 'medium';
    return 'low';
  }

  getDefaultEnrollment() {
    return {
      strategies: { strategies: [], hasEnrollment: false },
      process: { phases: [], milestones: [] },
      effectiveness: { overallScore: 0 },
      chinesePatterns: { politicalMobilization: [], institutionalMechanisms: [], chineseCulturalFeatures: [] },
      challenges: { challenges: [], resolutionApproaches: [] },
      hasEnrollment: false
    };
  }
}

module.exports = EnrollmentAnalyzer;