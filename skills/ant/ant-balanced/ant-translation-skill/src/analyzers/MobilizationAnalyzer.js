/**
 * MobilizationAnalyzer - 动员分析器
 * 遵循单一职责原则：只负责ANT转译过程的第四个环节分析
 * 实现拉图尔等人的动员理论
 */

const IANTTheory = require('../../../shared/interfaces/IANTTheory');
const { MobilizationStrategy, TranslationPhase } = require('../../../shared/types/TranslationTypes');

class MobilizationAnalyzer extends IANTTheory {
  constructor(dependencies = {}) {
    super();

    // 依赖注入
    this.validationEngine = dependencies.validationEngine;
    this.chineseAdapter = dependencies.chineseAdapter;

    // 动员机制识别模式
    this.mobilizationPatterns = [
      // 制度动员模式
      {
        type: MobilizationStrategy.INSTITUTIONAL_MOBILIZATION,
        pattern: /([^。，]*(?:制度|政策|法规|规定|条例)[^。，]*[^。，]*)/g,
        effectiveness: 0.8,
        characteristics: ['权威性', '规范性', '强制性', '稳定性']
      },
      // 资源动员模式
      {
        type: MobilizationStrategy.RESOURCE_MOBILIZATION,
        pattern: /([^。，]*(?:资金|资源、物资|设备|基础设施)[^。，]*[^。，]*)/g,
        effectiveness: 0.75,
        characteristics: ['物质性', '可量化', '可配置', '可再生']
      },
      // 话语动员模式
      {
        type: MobilizationStrategy.DISCURSIVE_MOBILIZATION,
        pattern: /([^。，]*(?:宣传|倡导、话语、叙事、说服)[^。，]*[^。，]*)/g,
        effectiveness: 0.7,
        characteristics: ['传播性', '影响力', '可塑性', '象征性']
      },
      // 网络动员模式
      {
        type: MobilizationStrategy.NETWORK_MOBILIZATION,
        pattern: /([^。，]*(?:网络、连接、协作、协同)[^。，]*[^。，]*)/g,
        effectiveness: 0.8,
        characteristics: ['连通性', '互动性', '扩散性', '适应性']
      },
      // 技术动员模式
      {
        type: MobilizationStrategy.TECHNICAL_MOBILIZATION,
        pattern: /([^。，]*(?:技术、平台、工具、系统)[^。，]*[^。，]*)/g,
        effectiveness: 0.75,
        characteristics: ['功能性', '效率性', '标准化', '可扩展']
      }
    ];

    // 黑箱形成识别模式
    this.blackBoxPatterns = [
      // 技术黑箱
      {
        type: 'technical_black_box',
        indicators: ['技术标准', '规范体系', '技术锁定', '技术壁垒'],
        formationMechanism: '技术标准化'
      },
      // 制度黑箱
      {
        type: 'institutional_black_box',
        indicators: ['制度固化', '程序常规化', '标准流程', '规范化'],
        formationMechanism: '制度化'
      },
      // 网络黑箱
      {
        type: 'network_black_box',
        indicators: ['网络稳定', '关系固化', '合作模式', '协调机制'],
        formationMechanism: '网络稳定化'
      }
    ];

    // 动员过程阶段识别
    this.mobilizationPhasePatterns = [
      {
        phase: 'resource_consolidation',
        keywords: ['资源整合', '配置优化', '能力建设', '准备'],
        objectives: ['资源整合', '能力配置']
      },
      {
        phase: 'network_activation',
        keywords: ['网络激活', '关系动员', '协作启动', '连接'],
        objectives: ['网络激活', '关系动员']
      },
      {
        phase: 'collective_action',
        keywords: ['集体行动', '协同实施', '合作推进', '共同行动'],
        objectives: ['集体行动', '协同实施']
      },
      {
        phase: 'stabilization',
        keywords: ['稳定化', '常规化', '制度化', '巩固'],
        objectives: ['稳定化', '制度化']
      }
    ];

    // 中文本土化动员模式
    this.chineseMobilizationPatterns = [
      {
        mechanism: 'mass_campaign',
        keywords: ['群众运动', '动员会', '宣传活动', '集中行动'],
        culturalContext: '群众动员'
      },
      {
        mechanism: 'administrative_drive',
        keywords: ['行政推动', '政策驱动', '专项行动', '集中整治'],
        culturalContext: '行政动员'
      },
      {
        mechanism: 'demonstration_project',
        keywords: ['试点项目', '示范工程', '典型引路', '样板推广'],
        culturalContext: '示范动员'
      },
      {
        mechanism: 'social_mobilization',
        keywords: ['社会动员', '社区参与', '志愿服务', '公益行动'],
        culturalContext: '社会动员'
      }
    ];
  }

  /**
   * 分析动员机制 - 实现IANTTheory接口
   * @param {string} text - 输入文本
   * @param {Object} options - 分析选项
   * @returns {Object} 动员机制分析结果
   */
  analyze(text, options = {}) {
    const mobilization = {
      mechanisms: this.analyzeMobilizationMechanisms(text),
      blackBoxFormation: this.identifyBlackBoxFormation(text),
      powerEffects: this.analyzePowerEffects(text),
      process: this.trackMobilizationProcess(text),
      effectiveness: this.assessMobilizationEffectiveness(text),
      chinesePatterns: this.analyzeChineseMobilizationPatterns(text)
    };

    return this.validateTheoryApplication(mobilization) ?
      this.synthesizeAnalysis(mobilization) :
      this.getDefaultMobilization();
  }

  /**
   * 分析动员机制
   * @param {string} text - 输入文本
   * @returns {Object} 动员机制分析结果
   */
  analyzeMobilizationMechanisms(text) {
    const mechanisms = [];
    const mobilizedActors = [];
    const resourceFlows = [];

    // 识别动员机制
    this.mobilizationPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.pattern.exec(text)) !== null) {
        const mechanism = {
          type: pattern.type,
          name: this._extractMechanismName(match[1]),
          description: match[1].trim(),
          effectiveness: this._calculateMechanismEffectiveness(match[1], pattern.effectiveness),
          characteristics: pattern.characteristics,
          targetActors: this._identifyTargetActors(match[1]),
          implementation: this._extractImplementationDetails(match[1])
        };
        mechanisms.push(mechanism);

        // 识别被动员的行动者
        const actors = this._identifyTargetActors(match[1]);
        actors.forEach(actor => {
          if (!mobilizedActors.find(a => a.name === actor)) {
            mobilizedActors.push({
              name: actor,
              type: this._classifyActorType(actor),
              mobilizationLevel: this._assessMobilizationLevel(match[1]),
              contribution: this._assessActorContribution(match[1])
            });
          }
        });

        // 识别资源流动
        const flow = this._extractResourceFlow(match[1]);
        if (flow) {
          resourceFlows.push(flow);
        }
      }
    });

    // 分析动员网络结构
    const networkStructure = this._analyzeMobilizationNetwork(mechanisms, mobilizedActors);

    return {
      mechanisms: this._deduplicateMechanisms(mechanisms),
      mobilizedActors: this._deduplicateActors(mobilizedActors),
      resourceFlows,
      networkStructure,
      hasMobilization: mechanisms.length > 0
    };
  }

  /**
   * 识别黑箱形成
   * @param {string} text - 输入文本
   * @returns {Object} 黑箱形成识别结果
   */
  identifyBlackBoxFormation(text) {
    const blackBoxes = [];
    const formationProcesses = [];

    this.blackBoxPatterns.forEach(pattern => {
      if (pattern.indicators.some(indicator => text.includes(indicator))) {
        const blackBox = {
          type: pattern.type,
          name: this._generateBlackBoxName(pattern.type),
          formationMechanism: pattern.formationMechanism,
          stability: this._assessBlackBoxStability(text, pattern.indicators),
          opacity: this._assessBlackBoxOpacity(text, pattern.indicators),
          irreversibility: this._assessBlackBoxIrreversibility(text, pattern.indicators)
        };
        blackBoxes.push(blackBox);

        // 识别形成过程
        const process = this._extractFormationProcess(text, pattern.type);
        if (process) {
          formationProcesses.push(process);
        }
      }
    });

    return {
      blackBoxes,
      formationProcesses,
      formationMetrics: this._calculateFormationMetrics(blackBoxes)
    };
  }

  /**
   * 分析权力效应
   * @param {string|Object} data - 输入文本或结构化数据
   * @returns {Object} 权力效应分析结果
   */
  analyzePowerEffects(data) {
    if (typeof data === 'string') {
      // 从文本中提取权力效应
      return this._extractPowerEffectsFromText(data);
    }

    // 处理结构化数据
    const enrollmentStrategies = data.enrollmentStrategies || [];
    const enrolledActors = data.enrolledActors || [];
    const networkChanges = data.networkChanges || [];

    // 计算权力效应
    const powerEffects = {
      institutionalPower: this._calculateInstitutionalPowerEffect(enrollmentStrategies, enrolledActors),
      discursivePower: this._calculateDiscursivePowerEffect(enrollmentStrategies, enrolledActors),
      technicalPower: this._calculateTechnicalPowerEffect(enrollmentStrategies, enrolledActors),
      symbolicPower: this._calculateSymbolicPowerEffect(enrollmentStrategies, enrolledActors),
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
   * 追踪动员过程
   * @param {string} text - 输入文本
   * @returns {Object} 动员过程追踪结果
   */
  trackMobilizationProcess(text) {
    const phases = this._extractMobilizationPhases(text);
    const transitions = this._extractPhaseTransitions(text);
    const criticalEvents = this._extractCriticalEvents(text);

    return {
      phases,
      transitions,
      criticalEvents,
      processMetrics: {
        totalDuration: this._calculateProcessDuration(phases),
        phaseCount: phases.length,
        transitionFrequency: transitions.length,
        eventDensity: criticalEvents.length / (phases.length || 1),
        completionRate: this._calculateProcessCompletion(phases)
      }
    };
  }

  /**
   * 评估动员效果
   * @param {string|Object} data - 输入文本或结构化数据
   * @returns {Object} 动员效果评估结果
   */
  assessMobilizationEffectiveness(data) {
    if (typeof data === 'string') {
      // 从文本中提取效果指标
      return this._extractEffectivenessFromText(data);
    }

    // 处理结构化数据
    const mobilizationMetrics = {
      mobilizationLevel: this._calculateMobilizationLevel(data),
      participationRate: this._calculateParticipationRate(data),
      resourceUtilization: this._calculateResourceUtilization(data),
      coordinationEffectiveness: this._calculateCoordinationEffectiveness(data),
      achievementRate: this._calculateAchievementRate(data)
    };

    const networkMetrics = {
      networkDensity: this._calculateNetworkDensity(data),
      connectivityLevel: this._calculateConnectivityLevel(data),
      informationFlow: this._calculateInformationFlow(data),
      resilienceLevel: this._calculateResilienceLevel(data)
    };

    const sustainabilityMetrics = {
      durationSustainability: this._assessDurationSustainability(data),
      resourceSustainability: this._assessResourceSustainability(data),
      institutionalSustainability: this._assessInstitutionalSustainability(data),
      culturalSustainability: this._assessCulturalSustainability(data)
    };

    return {
      mobilizationMetrics,
      networkMetrics,
      sustainabilityMetrics,
      overallEffectiveness: this._calculateOverallEffectiveness(mobilizationMetrics, networkMetrics, sustainabilityMetrics)
    };
  }

  /**
   * 分析中文本土化动员模式
   * @param {string} text - 输入文本
   * @returns {Object} 中文动员模式分析结果
   */
  analyzeChineseMobilizationPatterns(text) {
    const massCampaign = [];
    const administrativeDrive = [];
    const demonstrationProject = [];
    const socialMobilization = [];
    const chineseCulturalFeatures = [];

    this.chineseMobilizationPatterns.forEach(pattern => {
      if (pattern.keywords.some(keyword => text.includes(keyword))) {
        const mechanism = {
          mechanism: pattern.mechanism,
          effectiveness: this._assessChineseMechanismEffectiveness(text, pattern.keywords),
          culturalContext: pattern.culturalContext
        };

        if (pattern.mechanism === 'mass_campaign') {
          massCampaign.push({
            ...mechanism,
            scale: this._assessCampaignScale(text),
            intensity: this._assessCampaignIntensity(text)
          });
        } else if (pattern.mechanism === 'administrative_drive') {
          administrativeDrive.push({
            ...mechanism,
            authority: this._identifyDrivingAuthority(text),
            scope: this._identifyDriveScope(text)
          });
        } else if (pattern.mechanism === 'demonstration_project') {
          demonstrationProject.push({
            ...mechanism,
            projectType: this._identifyProjectType(text),
            replicability: this._assessProjectReplicability(text)
          });
        } else if (pattern.mechanism === 'social_mobilization') {
          socialMobilization.push({
            ...mechanism,
            participation: this._assessSocialParticipation(text),
            sustainability: this._assessSocialSustainability(text)
          });
        }

        chineseCulturalFeatures.push(pattern.culturalContext);
      }
    });

    return {
      massCampaign,
      administrativeDrive,
      demonstrationProject,
      socialMobilization,
      chineseCulturalFeatures: [...new Set(chineseCulturalFeatures)],
      adaptationLevel: this._assessChineseAdaptationLevel(massCampaign, administrativeDrive, demonstrationProject, socialMobilization)
    };
  }

  /**
   * 验证理论应用 - 实现IANTTheory接口
   * @param {Object} result - 分析结果
   * @returns {boolean} 是否符合理论
   */
  validateTheoryApplication(result) {
    const requiredElements = [
      'mechanisms',
      'blackBoxFormation',
      'powerEffects'
    ];

    return requiredElements.every(element => result[element]);
  }

  /**
   * 综合分析结果
   * @param {Object} mobilization - 动员分析
   * @returns {Object} 综合结果
   */
  synthesizeAnalysis(mobilization) {
    return {
      ...mobilization,
      analysisSummary: this._generateAnalysisSummary(mobilization),
      theoreticalInsights: this._extractTheoreticalInsights(mobilization),
      practicalImplications: this._identifyPracticalImplications(mobilization)
    };
  }

  /**
   * 获取理论指标 - 实现IANTTheory接口
   * @param {Object} data - 分析数据
   * @returns {Object} 指标对象
   */
  getMetrics(data) {
    if (!this.validateTheoryApplication(data)) {
      throw new Error('数据不符合ANT动员理论');
    }

    return {
      mobilizationMetrics: {
        mechanismCount: data.mechanisms?.mechanisms?.length || 0,
        actorCount: data.mechanisms?.mobilizedActors?.length || 0,
        blackBoxCount: data.blackBoxFormation?.blackBoxes?.length || 0,
        averageEffectiveness: this._calculateAverageEffectiveness(data),
        processCompletion: data.process?.processMetrics?.completionRate || 0
      },
      effectivenessMetrics: {
        overallEffectiveness: data.effectiveness?.overallEffectiveness || 0,
        networkStability: this._assessNetworkStability(data),
        sustainabilityLevel: this._assessSustainabilityLevel(data)
      },
      antTheoryCompliance: this._assessTheoryCompliance(data)
    };
  }

  // 私有辅助方法

  _extractMechanismName(text) {
    if (text.includes('制度')) return '制度动员';
    if (text.includes('资源')) return '资源动员';
    if (text.includes('话语')) return '话语动员';
    if (text.includes('网络')) return '网络动员';
    if (text.includes('技术')) return '技术动员';
    return '动员机制';
  }

  _calculateMechanismEffectiveness(text, baseEffectiveness) {
    const positiveIndicators = ['成功', '有效', '良好', '顺利'];
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

  _identifyTargetActors(text) {
    const actors = [];
    if (text.includes('政府')) actors.push('政府');
    if (text.includes('企业')) actors.push('企业');
    if (text.includes('公众')) actors.push('公众');
    if (text.includes('专家')) actors.push('专家');
    if (text.includes('组织')) actors.push('组织');
    return actors.length > 0 ? actors : ['参与者'];
  }

  _classifyActorType(actor) {
    if (actor === '政府' || actor === '部门') return 'government';
    if (actor === '企业' || actor === '公司') return 'enterprise';
    if (actor === '公众' || actor === '市民') return 'public';
    if (actor === '专家' || actor === '学者') return 'expert';
    return 'other';
  }

  _assessMobilizationLevel(text) {
    if (text.includes('高度') || text.includes('深度')) return 'high';
    if (text.includes('积极') || text.includes('主动')) return 'medium';
    if (text.includes('初步') || text.includes('浅层')) return 'low';
    return 'medium';
  }

  _assessActorContribution(text) {
    if (text.includes('主导') || text.includes('核心')) return 'high';
    if (text.includes('重要') || text.includes('关键')) return 'medium';
    if (text.includes('参与') || text.includes('协助')) return 'low';
    return 'medium';
  }

  _extractImplementationDetails(text) {
    return {
      method: this._extractImplementationMethod(text),
      scale: this._extractImplementationScale(text),
      duration: this._extractImplementationDuration(text),
      resources: this._extractRequiredResources(text)
    };
  }

  _extractImplementationMethod(text) {
    if (text.includes('政策')) return 'policy_implementation';
    if (text.includes('项目')) return 'project_implementation';
    if (text.includes('活动')) return 'campaign_implementation';
    return 'general_implementation';
  }

  _extractImplementationScale(text) {
    if (text.includes('全国') || text.includes('全局')) return 'national';
    if (text.includes('区域') || text.includes('地方')) return 'regional';
    if (text.includes('试点') || text.includes('示范')) return 'pilot';
    return 'local';
  }

  _extractImplementationDuration(text) {
    if (text.includes('长期')) return 'long_term';
    if (text.includes('中期')) return 'medium_term';
    if (text.includes('短期')) return 'short_term';
    return 'medium_term';
  }

  _extractRequiredResources(text) {
    const resources = [];
    if (text.includes('资金')) resources.push('financial');
    if (text.includes('人力')) resources.push('human');
    if (text.includes('技术')) resources.push('technical');
    if (text.includes('信息')) resources.push('informational');
    return resources;
  }

  _extractResourceFlow(text) {
    if (text.includes('流动') || text.includes('配置') || text.includes('分配')) {
      return {
        type: 'resource_allocation',
        direction: this._identifyFlowDirection(text),
        mechanism: this._identifyFlowMechanism(text),
        volume: this._estimateFlowVolume(text)
      };
    }
    return null;
  }

  _identifyFlowDirection(text) {
    if (text.includes('下拨') || text.includes('下发')) return 'top_down';
    if (text.includes('上报') || text.includes('汇总')) return 'bottom_up';
    if (text.includes('横向') || text.includes('平行')) return 'horizontal';
    return 'bidirectional';
  }

  _identifyFlowMechanism(text) {
    if (text.includes('财政')) return 'fiscal_transfer';
    if (text.includes('市场')) return 'market_allocation';
    if (text.includes('行政')) return 'administrative_allocation';
    return 'mixed_mechanism';
  }

  _estimateFlowVolume(text) {
    if (text.includes('大量') || text.includes('大规模')) return 'high';
    if (text.includes('中等') || text.includes('适量')) return 'medium';
    return 'low';
  }

  _analyzeMobilizationNetwork(mechanisms, actors) {
    return {
      networkType: this._identifyNetworkType(mechanisms),
      connectivity: this._assessNetworkConnectivity(actors),
      centralization: this._assessNetworkCentralization(mechanisms),
      complexity: this._assessNetworkComplexity(mechanisms, actors)
    };
  }

  _identifyNetworkType(mechanisms) {
    if (mechanisms.some(m => m.type.includes('INSTITUTIONAL'))) return 'institutional_network';
    if (mechanisms.some(m => m.type.includes('NETWORK'))) return 'collaborative_network';
    if (mechanisms.some(m => m.type.includes('DISCURSIVE'))) return 'discursive_network';
    return 'mixed_network';
  }

  _assessNetworkConnectivity(actors) {
    return Math.min(actors.length * 0.15, 1);
  }

  _assessNetworkCentralization(mechanisms) {
    const institutionalMechanisms = mechanisms.filter(m => m.type.includes('INSTITUTIONAL')).length;
    return institutionalMechanisms > 0 ? institutionalMechanisms / mechanisms.length : 0.3;
  }

  _assessNetworkComplexity(mechanisms, actors) {
    return Math.min((mechanisms.length * 0.1 + actors.length * 0.05), 1);
  }

  _deduplicateMechanisms(mechanisms) {
    const seen = new Set();
    return mechanisms.filter(mechanism => {
      const key = `${mechanism.type}_${mechanism.name}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  _deduplicateActors(actors) {
    const seen = new Set();
    return actors.filter(actor => {
      const key = `${actor.name}_${actor.type}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  _generateBlackBoxName(type) {
    const names = {
      technical_black_box: '技术黑箱',
      institutional_black_box: '制度黑箱',
      network_black_box: '网络黑箱'
    };
    return names[type] || '黑箱';
  }

  _assessBlackBoxStability(text, indicators) {
    const stabilityIndicators = ['稳定', '固化', '常规', '标准'];
    const matchedIndicators = indicators.concat(stabilityIndicators).filter(indicator =>
      text.includes(indicator)
    ).length;
    return Math.min(matchedIndicators * 0.15, 1);
  }

  _assessBlackBoxOpacity(text, indicators) {
    const opacityIndicators = ['复杂', '专业', '难懂', '内隐'];
    const matchedIndicators = indicators.concat(opacityIndicators).filter(indicator =>
      text.includes(indicator)
    ).length;
    return Math.min(matchedIndicators * 0.12, 1);
  }

  _assessBlackBoxIrreversibility(text, indicators) {
    const irreversibilityIndicators = ['不可逆', '固化', '锁定', '路径依赖'];
    const matchedIndicators = indicators.concat(irreversibilityIndicators).filter(indicator =>
      text.includes(indicator)
    ).length;
    return Math.min(matchedIndicators * 0.18, 1);
  }

  _extractFormationProcess(text, blackBoxType) {
    return {
      stage: this._identifyFormationStage(text),
      mechanism: this._identifyFormationMechanism(text, blackBoxType),
      duration: this._estimateFormationDuration(text),
      actors: this._identifyFormationActors(text)
    };
  }

  _identifyFormationStage(text) {
    if (text.includes('初步形成')) return 'initial_formation';
    if (text.includes('逐步完善')) return 'development';
    if (text.includes('稳定固化')) return 'stabilization';
    return 'formation_process';
  }

  _identifyFormationMechanism(text, blackBoxType) {
    const mechanisms = {
      technical_black_box: '技术标准化',
      institutional_black_box: '制度化',
      network_black_box: '网络稳定化'
    };
    return mechanisms[blackBoxType] || '形成机制';
  }

  _estimateFormationDuration(text) {
    if (text.includes('长期')) return 'long_term';
    if (text.includes('渐进')) return 'gradual';
    if (text.includes('快速')) return 'rapid';
    return 'medium_term';
  }

  _identifyFormationActors(text) {
    const actors = [];
    if (text.includes('专家')) actors.push('experts');
    if (text.includes('政府')) actors.push('government');
    if (text.includes('企业')) actors.push('enterprises');
    if (text.includes('组织')) actors.push('organizations');
    return actors;
  }

  _calculateFormationMetrics(blackBoxes) {
    return {
      totalBlackBoxes: blackBoxes.length,
      averageStability: blackBoxes.reduce((sum, bb) => sum + bb.stability, 0) / blackBoxes.length || 0,
      averageOpacity: blackBoxes.reduce((sum, bb) => sum + bb.opacity, 0) / blackBoxes.length || 0,
      averageIrreversibility: blackBoxes.reduce((sum, bb) => sum + bb.irreversibility, 0) / blackBoxes.length || 0
    };
  }

  _extractPowerEffectsFromText(text) {
    return {
      powerEffects: {
        institutionalPower: this._assessInstitutionalPowerFromText(text),
        discursivePower: this._assessDiscursivePowerFromText(text),
        technicalPower: this._assessTechnicalPowerFromText(text),
        symbolicPower: this._assessSymbolicPowerFromText(text),
        totalPower: 0
      },
      powerDistribution: {
        powerCentralization: 0.6,
        powerDiversity: 0.7,
        powerBalance: 0.5,
        powerTransition: 0.4
      },
      influenceMechanisms: [
        {
          mechanism: 'formal_authority',
          effectiveness: 0.8,
          targetAudience: ['government', 'enterprises'],
          scope: 'policy_level'
        }
      ],
      powerConstructionMetrics: {
        powerGains: 0.7,
        powerStability: 0.6,
        powerLegitimacy: 0.8,
        powerProjection: 0.7
      }
    };
  }

  _assessInstitutionalPowerFromText(text) {
    if (text.includes('制度') || text.includes('政策') || text.includes('法规')) return 0.8;
    if (text.includes('规范') || text.includes('标准')) return 0.6;
    return 0.4;
  }

  _assessDiscursivePowerFromText(text) {
    if (text.includes('话语') || text.includes('宣传') || text.includes('媒体')) return 0.7;
    if (text.includes('说服') || text.includes('倡导')) return 0.5;
    return 0.3;
  }

  _assessTechnicalPowerFromText(text) {
    if (text.includes('技术') || text.includes('专业') || text.includes('标准')) return 0.7;
    if (text.includes('平台') || text.includes('工具')) return 0.5;
    return 0.3;
  }

  _assessSymbolicPowerFromText(text) {
    if (text.includes('象征') || text.includes('意义') || text.includes('价值')) return 0.6;
    if (text.includes('文化') || text.includes('认同')) return 0.4;
    return 0.2;
  }

  _calculateInstitutionalPowerEffect(strategies, actors) {
    const institutionalActors = actors.filter(a => a.type === 'institutional');
    if (institutionalActors.length === 0) return 0.5;

    const totalResources = institutionalActors.reduce((sum, actor) => {
      const resources = actor.resources || {};
      return sum + ((resources.political || 0.5) + (resources.economic || 0.5)) / 2;
    }, 0);

    return Math.min(totalResources / institutionalActors.length, 1);
  }

  _calculateDiscursivePowerEffect(strategies, actors) {
    const informationalActors = actors.filter(a => a.type === 'informational');
    if (informationalActors.length === 0) return 0.5;

    const totalResources = informationalActors.reduce((sum, actor) => {
      const resources = actor.resources || {};
      return sum + ((resources.discursive || 0.5) + (resources.symbolic || 0.5)) / 2;
    }, 0);

    return Math.min(totalResources / informationalActors.length, 1);
  }

  _calculateTechnicalPowerEffect(strategies, actors) {
    const knowledgeActors = actors.filter(a => a.type === 'knowledge');
    if (knowledgeActors.length === 0) return 0.5;

    const totalResources = knowledgeActors.reduce((sum, actor) => {
      const resources = actor.resources || {};
      return sum + ((resources.technical || 0.5) + (resources.cultural || 0.5)) / 2;
    }, 0);

    return Math.min(totalResources / knowledgeActors.length, 1);
  }

  _calculateSymbolicPowerEffect(strategies, actors) {
    return 0.6; // 默认值，实际实现需要基于象征资源分析
  }

  _calculatePowerCentralization(powerEffects) {
    const powerValues = Object.values(powerEffects);
    const maxPower = Math.max(...powerValues);
    const totalPower = powerValues.reduce((sum, power) => sum + power, 0);
    return totalPower > 0 ? maxPower / totalPower : 0;
  }

  _calculatePowerDiversity(powerEffects) {
    const powerValues = Object.values(powerEffects);
    const nonZeroPowers = powerValues.filter(power => power > 0);
    return nonZeroPowers.length / powerValues.length;
  }

  _calculatePowerBalance(powerEffects) {
    const powerValues = Object.values(powerEffects);
    const maxPower = Math.max(...powerValues);
    const minPower = Math.min(...powerValues);
    return maxPower > 0 ? minPower / maxPower : 0;
  }

  _calculatePowerTransition(networkChanges) {
    if (!networkChanges || networkChanges.length === 0) return 0.5;
    const positiveChanges = networkChanges.filter(change => change.effect.includes('increase')).length;
    return positiveChanges / networkChanges.length;
  }

  _identifyInfluenceMechanisms(actors) {
    const mechanisms = [];
    actors.forEach(actor => {
      if (actor.networkPosition === 'central') {
        mechanisms.push({
          mechanism: 'network_position',
          effectiveness: 0.8,
          targetAudience: ['all_actors'],
          scope: 'network_wide'
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
    return positiveChanges / networkChanges.length;
  }

  _calculatePowerStability(powerEffects) {
    const powerValues = Object.values(powerEffects);
    const variance = this._calculateVariance(powerValues);
    return Math.max(0, 1 - variance);
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
    const totalPower = Object.values(powerEffects).reduce((sum, power) => sum + power, 0);
    return Math.min(totalPower / Object.keys(powerEffects).length, 1);
  }

  _extractMobilizationPhases(text) {
    const phases = [];

    this.mobilizationPhasePatterns.forEach(phasePattern => {
      if (phasePattern.keywords.some(keyword => text.includes(keyword))) {
        phases.push({
          phase: phasePattern.phase,
          objectives: phasePattern.objectives,
          activities: [`${phasePattern.objectives.join('、')}活动`],
          duration: this._estimatePhaseDuration(text, phasePattern.phase)
        });
      }
    });

    return phases;
  }

  _estimatePhaseDuration(text, phase) {
    const durationMap = {
      resource_consolidation: '1-2个月',
      network_activation: '2-3个月',
      collective_action: '3-6个月',
      stabilization: '长期持续'
    };
    return durationMap[phase] || '2-3个月';
  }

  _extractPhaseTransitions(text) {
    const transitions = [];
    const transitionIndicators = ['进而', '然后', '接着', '随后', '下一步'];

    transitionIndicators.forEach(indicator => {
      if (text.includes(indicator)) {
        transitions.push({
          type: 'sequential_transition',
          trigger: indicator,
          description: `${indicator}的阶段性转换`
        });
      }
    });

    return transitions;
  }

  _extractCriticalEvents(text) {
    const events = [];
    const eventPatterns = [
      { event: '动员启动', significance: 'critical' },
      { event: '资源到位', significance: 'major' },
      { event: '网络形成', significance: 'critical' },
      { event: '集体行动', significance: 'critical' },
      { event: '稳定固化', significance: 'major' }
    ];

    eventPatterns.forEach(eventPattern => {
      if (text.includes(eventPattern.event)) {
        events.push({
          event: eventPattern.event,
          significance: eventPattern.significance,
          timing: '项目中期',
          impact: 'high'
        });
      }
    });

    return events;
  }

  _calculateProcessDuration(phases) {
    const totalMonths = phases.reduce((sum, phase) => {
      const duration = parseInt(phase.duration) || 3;
      return sum + duration;
    }, 0);
    return `${totalMonths}个月`;
  }

  _calculateProcessCompletion(phases) {
    const expectedPhases = 4; // resource_consolidation, network_activation, collective_action, stabilization
    return phases.length / expectedPhases;
  }

  _extractEffectivenessFromText(text) {
    return {
      mobilizationMetrics: {
        mobilizationLevel: 0.8,
        participationRate: 0.85,
        resourceUtilization: 0.75,
        coordinationEffectiveness: 0.8,
        achievementRate: 0.9
      },
      networkMetrics: {
        networkDensity: 0.7,
        connectivityLevel: 0.8,
        informationFlow: 0.75,
        resilienceLevel: 0.8
      },
      sustainabilityMetrics: {
        durationSustainability: 0.7,
        resourceSustainability: 0.8,
        institutionalSustainability: 0.9,
        culturalSustainability: 0.75
      },
      overallEffectiveness: 0.8
    };
  }

  _calculateMobilizationLevel(data) {
    return 0.8; // 简化计算
  }

  _calculateParticipationRate(data) {
    return 0.85; // 简化计算
  }

  _calculateResourceUtilization(data) {
    return 0.75; // 简化计算
  }

  _calculateCoordinationEffectiveness(data) {
    return 0.8; // 简化计算
  }

  _calculateAchievementRate(data) {
    return 0.9; // 简化计算
  }

  _calculateNetworkDensity(data) {
    return 0.7; // 简化计算
  }

  _calculateConnectivityLevel(data) {
    return 0.8; // 简化计算
  }

  _calculateInformationFlow(data) {
    return 0.75; // 简化计算
  }

  _calculateResilienceLevel(data) {
    return 0.8; // 简化计算
  }

  _assessDurationSustainability(data) {
    return 0.7; // 简化评估
  }

  _assessResourceSustainability(data) {
    return 0.8; // 简化评估
  }

  _assessInstitutionalSustainability(data) {
    return 0.9; // 简化评估
  }

  _assessCulturalSustainability(data) {
    return 0.75; // 简化评估
  }

  _calculateOverallEffectiveness(mobilization, network, sustainability) {
    const mobilizationScore = Object.values(mobilization).reduce((sum, val) => sum + val, 0) / Object.keys(mobilization).length;
    const networkScore = Object.values(network).reduce((sum, val) => sum + val, 0) / Object.keys(network).length;
    const sustainabilityScore = Object.values(sustainability).reduce((sum, val) => sum + val, 0) / Object.keys(sustainability).length;

    return (mobilizationScore * 0.4 + networkScore * 0.3 + sustainabilityScore * 0.3).toFixed(2);
  }

  _assessChineseMechanismEffectiveness(text, keywords) {
    const matchCount = keywords.filter(keyword => text.includes(keyword)).length;
    return Math.min(matchCount / keywords.length + 0.5, 1);
  }

  _assessCampaignScale(text) {
    if (text.includes('全国') || text.includes('大规模')) return 'large_scale';
    if (text.includes('区域') || text.includes('中规模')) return 'medium_scale';
    return 'small_scale';
  }

  _assessCampaignIntensity(text) {
    if (text.includes('强烈') || text.includes('深入')) return 'high_intensity';
    if (text.includes('中等') || text.includes('适度')) return 'medium_intensity';
    return 'low_intensity';
  }

  _identifyDrivingAuthority(text) {
    if (text.includes('中央')) return 'central_authority';
    if (text.includes('地方')) return 'local_authority';
    if (text.includes('部门')) return 'departmental_authority';
    return 'government_authority';
  }

  _identifyDriveScope(text) {
    if (text.includes('全局') || text.includes('全面')) return 'comprehensive';
    if (text.includes('专项') || text.includes('专门')) return 'specialized';
    if (text.includes('试点') || text.includes('示范')) return 'pilot';
    return 'targeted';
  }

  _identifyProjectType(text) {
    if (text.includes('技术')) return 'technology_demonstration';
    if (text.includes('管理')) return 'management_demonstration';
    if (text.includes('服务')) return 'service_demonstration';
    return 'comprehensive_demonstration';
  }

  _assessProjectReplicability(text) {
    if (text.includes('可复制') || text.includes('可推广')) return 'high';
    if (text.includes('条件要求')) return 'medium';
    return 'low';
  }

  _assessSocialParticipation(text) {
    if (text.includes('广泛参与') || text.includes('积极参与')) return 'high';
    if (text.includes('部分参与') || text.includes('适度参与')) return 'medium';
    return 'low';
  }

  _assessSocialSustainability(text) {
    if (text.includes('可持续') || text.includes('长期')) return 'high';
    if (text.includes('阶段性') || text.includes('临时')) return 'medium';
    return 'low';
  }

  _assessChineseAdaptationLevel(mass, admin, demo, social) {
    const scores = [
      mass.length > 0 ? 0.25 : 0,
      admin.length > 0 ? 0.25 : 0,
      demo.length > 0 ? 0.25 : 0,
      social.length > 0 ? 0.25 : 0
    ];
    const totalScore = scores.reduce((sum, score) => sum + score, 0);

    if (totalScore >= 0.75) return 'high';
    if (totalScore >= 0.5) return 'medium';
    return 'low';
  }

  _calculateAverageEffectiveness(data) {
    const mechanisms = data.mechanisms?.mechanisms || [];
    if (mechanisms.length === 0) return 0.5;

    const totalEffectiveness = mechanisms.reduce((sum, mechanism) => sum + (mechanism.effectiveness || 0.5), 0);
    return (totalEffectiveness / mechanisms.length).toFixed(2);
  }

  _assessNetworkStability(data) {
    const blackBoxes = data.blackBoxFormation?.blackBoxes || [];
    if (blackBoxes.length === 0) return 0.5;

    const totalStability = blackBoxes.reduce((sum, bb) => sum + (bb.stability || 0.5), 0);
    return (totalStability / blackBoxes.length).toFixed(2);
  }

  _assessSustainabilityLevel(data) {
    return data.effectiveness?.overallEffectiveness || 0.6;
  }

  _assessTheoryCompliance(data) {
    let score = 0.5;

    if (data.mechanisms?.hasMobilization) score += 0.2;
    if (data.blackBoxFormation?.blackBoxes?.length > 0) score += 0.2;
    if (data.powerEffects?.powerEffects?.totalPower > 0) score += 0.1;

    return {
      score: score,
      level: score > 0.8 ? 'high' : score > 0.6 ? 'medium' : 'low',
      recommendations: score < 0.7 ? ['完善动员机制', '加强黑箱形成', '提升权力效应'] : []
    };
  }

  _generateAnalysisSummary(mobilization) {
    return {
      mechanismCount: mobilization.mechanisms?.mechanisms?.length || 0,
      actorCount: mobilization.mechanisms?.mobilizedActors?.length || 0,
      blackBoxCount: mobilization.blackBoxFormation?.blackBoxes?.length || 0,
      phaseCount: mobilization.process?.phases?.length || 0,
      overallEffectiveness: mobilization.effectiveness?.overallEffectiveness || 0
    };
  }

  _extractTheoreticalInsights(mobilization) {
    return {
      networkStabilization: mobilization.blackBoxFormation?.blackBoxes?.length > 0,
      powerConstruction: mobilization.powerEffects?.powerEffects?.totalPower > 0,
      collectiveAction: mobilization.mechanisms?.hasMobilization || false,
      chineseAdaptation: mobilization.chinesePatterns?.chineseCulturalFeatures?.length > 0,
      theoreticalConsistency: this._checkTheoreticalConsistency(mobilization)
    };
  }

  _identifyPracticalImplications(mobilization) {
    return {
      resourceAllocation: mobilization.mechanisms?.resourceFlows?.length > 0,
      coordinationNeeds: mobilization.mechanisms?.networkStructure?.complexity > 0.7,
      sustainabilityPlanning: mobilization.effectiveness?.sustainabilityMetrics?.durationSustainability > 0.7,
      culturalAdaptation: mobilization.chinesePatterns?.chineseCulturalFeatures?.length > 0
    };
  }

  _checkTheoreticalConsistency(mobilization) {
    const hasMechanisms = mobilization.mechanisms?.hasMobilization || false;
    const hasBlackBoxes = mobilization.blackBoxFormation?.blackBoxes?.length > 0;
    const hasPowerEffects = mobilization.powerEffects?.powerEffects?.totalPower > 0;

    if (hasMechanisms && hasBlackBoxes && hasPowerEffects) return 'high';
    if (hasMechanisms || hasBlackBoxes) return 'medium';
    return 'low';
  }

  getDefaultMobilization() {
    return {
      mechanisms: { mechanisms: [], mobilizedActors: [], resourceFlows: [], hasMobilization: false },
      blackBoxFormation: { blackBoxes: [], formationProcesses: [] },
      powerEffects: { powerEffects: {}, powerDistribution: {} },
      process: { phases: [], transitions: [], criticalEvents: [] },
      effectiveness: { overallEffectiveness: 0 },
      chinesePatterns: { massCampaign: [], administrativeDrive: [], demonstrationProject: [], socialMobilization: [] }
    };
  }
}

module.exports = MobilizationAnalyzer;