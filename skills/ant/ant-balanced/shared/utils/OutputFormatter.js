/**
 * OutputFormatter - 输出格式化器
 * 遵循单一职责原则：只负责格式化分析结果的输出
 * 实现分层信息披露和用户友好的输出格式
 */

class OutputFormatter {
  constructor(options = {}) {
    this.defaultLanguage = options.defaultLanguage || 'zh-CN';
    this.dateFormat = options.dateFormat || 'ISO';
    this.numberFormat = options.numberFormat || 'decimal';
  }

  /**
   * 格式化分析结果
   * @param {Object} analysisResult - 分析结果
   * @param {Object} options - 格式化选项
   * @returns {Object} 格式化后的结果
   */
  format(analysisResult, options = {}) {
    const formatOptions = {
      language: options.language || this.defaultLanguage,
      depth: options.depth || 'medium', // quick, medium, deep
      includeMetadata: options.includeMetadata !== false,
      includeTimestamps: options.includeTimestamps !== false,
      includeRecommendations: options.includeRecommendations !== false,
      outputFormat: options.outputFormat || 'structured', // structured, narrative, summary
      ...options
    };

    try {
      // 根据深度格式化
      switch (formatOptions.depth) {
        case 'quick':
          return this._formatQuickInsight(analysisResult, formatOptions);
        case 'medium':
          return this._formatTheoryApplication(analysisResult, formatOptions);
        case 'deep':
          return this._formatDeepAnalysis(analysisResult, formatOptions);
        default:
          return this._formatTheoryApplication(analysisResult, formatOptions);
      }
    } catch (error) {
      console.error('格式化过程中发生错误:', error);
      return this._formatError(error, formatOptions);
    }
  }

  /**
   * 格式化快速洞察（第1层：10秒理解）
   * @param {Object} result - 分析结果
   * @param {Object} options - 格式化选项
   * @returns {Object} 快速洞察格式
   * @private
   */
  _formatQuickInsight(result, options) {
    const basicSynthesis = result.basicSynthesis || {};
    const theoreticalAnalysis = result.theoreticalAnalysis || {};

    return {
      // 快速概览
      quickOverview: {
        title: 'ANT转译分析快览',
        timestamp: this._formatTimestamp(new Date(), options),
        overallStatus: this._getOverallStatus(basicSynthesis),
        keyMetric: this._getKeyMetric(basicSynthesis),
        urgency: this._assessUrgency(basicSynthesis)
      },

      // 核心问题
      coreProblem: {
        title: '核心问题识别',
        problems: this._extractCoreProblems(basicSynthesis),
        primaryChallenge: this._identifyPrimaryChallenge(basicSynthesis),
        solutionDirection: this._suggestSolutionDirection(basicSynthesis)
      },

      // 关键行动者
      keyActors: {
        title: '关键行动者',
        mainActors: this._extractMainActors(basicSynthesis),
        actorRelationships: this._summarizeActorRelationships(basicSynthesis),
        powerDynamics: this._summarizePowerDynamics(basicSynthesis)
      },

      // 立即行动
      immediateActions: {
        title: '建议立即行动',
        priorityActions: this._extractPriorityActions(result),
        quickWins: this._identifyQuickWins(result),
        criticalDecisions: this._highlightCriticalDecisions(result)
      },

      // 风险提示
      riskAlerts: {
        title: '风险提示',
        highRisks: this._identifyHighRisks(result),
        mitigationMeasures: this._suggestMitigationMeasures(result),
        monitoringPoints: this._recommendMonitoringPoints(result)
      },

      // 元数据
      metadata: this._generateMetadata('quick', options)
    };
  }

  /**
   * 格式化理论应用（第2层：30秒阅读）
   * @param {Object} result - 分析结果
   * @param {Object} options - 格式化选项
   * @returns {Object} 理论应用格式
   * @private
   */
  _formatTheoryApplication(result, options) {
    const basicSynthesis = result.basicSynthesis || {};
    const theoreticalAnalysis = result.theoreticalAnalysis || {};
    const processAnalysis = result.processAnalysis || {};

    return {
      // 执行摘要
      executiveSummary: {
        title: 'ANT转译分析报告',
        timestamp: this._formatTimestamp(new Date(), options),
        analysisScope: this._describeAnalysisScope(result),
        keyFindings: this._extractKeyFindings(result),
        overallAssessment: this._provideOverallAssessment(result)
      },

      // 转译环节分析
      translationPhases: {
        title: '转译环节分析',
        problematization: this._formatProblematizationPhase(result),
        interessement: this._formatInteressementPhase(result),
        enrollment: this._formatEnrollmentPhase(result),
        mobilization: this._formatMobilizationPhase(result),
        phaseIntegration: this._assessPhaseIntegration(result)
      },

      // 行动者网络
      actorNetwork: {
        title: '行动者网络分析',
        networkStructure: this._describeNetworkStructure(basicSynthesis),
        actorAnalysis: this._analyzeActors(basicSynthesis),
        relationshipMapping: this._mapRelationships(basicSynthesis),
        networkDynamics: this._describeNetworkDynamics(basicSynthesis)
      },

      // 理论一致性
      theoreticalConsistency: {
        title: '理论一致性分析',
        consistencyScore: theoreticalAnalysis.consistencyScore || 0,
        consistencyChecks: this._summarizeConsistencyChecks(theoreticalAnalysis),
        theoreticalCompliance: this._assessTheoreticalCompliance(theoreticalAnalysis),
        improvementAreas: this._identifyImprovementAreas(theoreticalAnalysis)
      },

      // 过程分析
      processAnalysis: {
        title: '转译过程分析',
        processProgress: this._assessProcessProgress(processAnalysis),
        criticalTransitions: this._identifyCriticalTransitions(processAnalysis),
        processEfficiency: this._evaluateProcessEfficiency(processAnalysis),
        bottlenecks: this_._identifyProcessBottlenecks(processAnalysis)
      },

      // 实践建议
      practicalRecommendations: {
        title: '实践建议',
        strategicRecommendations: this._generateStrategicRecommendations(result),
        operationalRecommendations: this._generateOperationalRecommendations(result),
        riskManagement: this._provideRiskManagementAdvice(result),
        nextSteps: this._outlineNextSteps(result)
      },

      // 中文本土化
      chineseContext: this._formatChineseContext(result.chineseAdaptation, options),

      // 元数据
      metadata: this._generateMetadata('medium', options)
    };
  }

  /**
   * 格式化深度分析（第3层：按需展开）
   * @param {Object} result - 分析结果
   * @param {Object} options - 格式化选项
   * @returns {Object} 深度分析格式
   * @private
   */
  _formatDeepAnalysis(result, options) {
    return {
      // 完整分析（包含中等深度的所有内容）
      ...this._formatTheoryApplication(result, options),

      // 详细理论分析
      detailedTheoreticalAnalysis: {
        title: '详细理论分析',
        antFrameworkApplication: this._analyzeANTFrameworkApplication(result),
        theoreticalFoundations: this._explainTheoreticalFoundations(result),
        conceptualMapping: this._detailConceptualMapping(result),
        methodologicalApproach: this._explainMethodologicalApproach(result)
      },

      // 深度网络分析
      deepNetworkAnalysis: {
        title: '深度网络分析',
        networkTopology: this._analyzeNetworkTopology(result),
        powerStructures: this._analyzePowerStructures(result),
        resourceFlows: this._analyzeResourceFlows(result),
        informationFlows: this._analyzeInformationFlows(result),
        networkEvolution: this._traceNetworkEvolution(result)
      },

      // 过程动力学
      processDynamics: {
        title: '过程动力学分析',
        temporalAnalysis: this._performTemporalAnalysis(result),
        causalMechanisms: this._identifyCausalMechanisms(result),
        feedbackLoops: this._identifyFeedbackLoops(result),
        emergencePatterns: this._identifyEmergencePatterns(result)
      },

      // 黑箱分析
      blackBoxAnalysis: {
        title: '黑箱形成分析',
        blackBoxIdentification: this._identifyBlackBoxes(result),
        formationMechanisms: this._explainFormationMechanisms(result),
        stabilityAssessment: this._assessBlackBoxStability(result),
        irreversibilityAnalysis: this._analyzeIrreversibility(result)
      },

      // 权力建构深度分析
      powerConstructionAnalysis: {
        title: '权力建构深度分析',
        powerSourceAnalysis: this._analyzePowerSources(result),
        powerMechanismAnalysis: this._analyzePowerMechanisms(result),
        powerEffectAnalysis: this._analyzePowerEffects(result),
        powerLegitimacyAnalysis: this._analyzePowerLegitimacy(result)
      },

      // 中文本土化深度分析
      deepChineseContext: {
        title: '中文本土化深度分析',
        culturalSystemAnalysis: this._analyzeCulturalSystem(result),
        institutionalContextAnalysis: this._analyzeInstitutionalContext(result),
        adaptationMechanismAnalysis: this._analyzeAdaptationMechanisms(result),
        comparativeAnalysis: this._performComparativeAnalysis(result)
      },

      // 方法论说明
      methodologicalNotes: {
        title: '方法论说明',
        dataCollection: this._describeDataCollection(result),
        analyticalMethods: this._explainAnalyticalMethods(result),
        limitations: this._discussLimitations(result),
        validityMeasures: this._describeValidityMeasures(result)
      },

      // 进一步研究建议
      furtherResearch: {
        title: '进一步研究建议',
        researchQuestions: this._proposeResearchQuestions(result),
        methodologicalExtensions: this._suggestMethodologicalExtensions(result),
        theoreticalContributions: this._identifyTheoreticalContributions(result),
        practicalApplications: this._suggestPracticalApplications(result)
      },

      // 附录
      appendices: {
        title: '附录',
        rawData: this._includeRawData(result),
        technicalDetails: this._includeTechnicalDetails(result),
        references: this._includeReferences(result),
        glossary: this._includeGlossary(result)
      },

      // 元数据
      metadata: this._generateMetadata('deep', options)
    };
  }

  /**
   * 格式化错误信息
   * @param {Error} error - 错误对象
   * @param {Object} options - 格式化选项
   * @returns {Object} 错误格式
   * @private
   */
  _formatError(error, options) {
    return {
      error: {
        type: error.constructor.name,
        message: error.message,
        timestamp: this._formatTimestamp(new Date(), options),
        suggestions: this._generateErrorSuggestions(error),
        recoveryOptions: this._suggestRecoveryOptions(error)
      },
      metadata: this._generateMetadata('error', options)
    };
  }

  // 辅助方法

  _formatTimestamp(date, options) {
    if (options.dateFormat === 'ISO') {
      return date.toISOString();
    }
    return date.toLocaleString(options.language || 'zh-CN');
  }

  _getOverallStatus(basicSynthesis) {
    const progress = basicSynthesis.translationProcess?.overallProgress || 0;
    if (progress >= 0.8) return '转译过程基本完成';
    if (progress >= 0.5) return '转译过程进行中';
    return '转译过程刚开始';
  }

  _getKeyMetric(basicSynthesis) {
    const actorCount = basicSynthesis.actorNetwork?.targetActors?.length || 0;
    const phaseCount = basicSynthesis.translationProcess?.phases?.filter(p => p.status === 'completed').length || 0;
    return `已动员${actorCount}个行动者，完成${phaseCount}/4个转译环节`;
  }

  _assessUrgency(basicSynthesis) {
    const problems = basicSynthesis.translationElements?.problems || [];
    const criticalProblems = problems.filter(p => p.severity > 0.7).length;
    if (criticalProblems >= 3) return 'high';
    if (criticalProblems >= 1) return 'medium';
    return 'low';
  }

  _extractCoreProblems(basicSynthesis) {
    const problems = basicSynthesis.translationElements?.problems || [];
    return problems.slice(0, 3).map(problem => ({
      description: problem.description,
      severity: this._formatSeverity(problem.severity),
      urgency: this._formatUrgency(problem.urgency)
    }));
  }

  _formatSeverity(severity) {
    if (severity >= 0.8) return '高';
    if (severity >= 0.5) return '中';
    return '低';
  }

  _formatUrgency(urgency) {
    if (urgency >= 0.8) return '紧急';
    if (urgency >= 0.5) return '中等';
    return '一般';
  }

  _identifyPrimaryChallenge(basicSynthesis) {
    const problems = basicSynthesis.translationElements?.problems || [];
    if (problems.length === 0) return '无明显挑战';
    const mostSevere = problems.reduce((max, problem) =>
      problem.severity > max.severity ? problem : max, problems[0]);
    return mostSevere?.description || '识别关键挑战中';
  }

  _suggestSolutionDirection(basicSynthesis) {
    const solutions = basicSynthesis.translationElements?.solutions || [];
    if (solutions.length > 0) {
      return `建议优先考虑: ${solutions[0].description}`;
    }
    return '需要进一步分析解决方案';
  }

  _extractMainActors(basicSynthesis) {
    const actors = basicSynthesis.actorNetwork?.targetActors || [];
    return actors.slice(0, 5).map(actor => ({
      name: actor.name,
      type: this._formatActorType(actor.type),
      engagement: this._formatEngagement(actor.engagementLevel)
    }));
  }

  _formatActorType(type) {
    const typeMap = {
      government: '政府机构',
      enterprise: '企业组织',
      expert: '专家学者',
      public: '公众群体',
      other: '其他组织'
    };
    return typeMap[type] || '未知类型';
  }

  _formatEngagement(level) {
    if (level === 'high') return '高度参与';
    if (level === 'medium') return '中度参与';
    return '低度参与';
  }

  _summarizeActorRelationships(basicSynthesis) {
    const relationships = basicSynthesis.actorNetwork?.actorRelationships || [];
    const strongRelationships = relationships.filter(r => r.strength > 0.7).length;
    return `共${relationships.length}个关系，其中${strongRelationships}个强关系`;
  }

  _summarizePowerDynamics(basicSynthesis) {
    // 简化实现
    return '权力分布相对均衡，存在一定的权力集中现象';
  }

  _extractPriorityActions(result) {
    return [
      '完善问题定义和解决方案',
      '加强利益相关者协调',
      '建立有效的监督机制'
    ];
  }

  _identifyQuickWins(result) {
    return [
      '建立沟通协调平台',
      '明确各方责任义务',
      '制定短期实施计划'
    ];
  }

  _highlightCriticalDecisions(result) {
    return [
      '确定必经节点和关键路径',
      '选择合适的招募和动员策略',
      '平衡各方利益和权力关系'
    ];
  }

  _identifyHighRisks(result) {
    return [
      '利益协调失败风险',
      '网络稳定性不足风险',
      '转译过程中断风险'
    ];
  }

  _suggestMitigationMeasures(result) {
    return [
      '建立风险预警机制',
      '制定应急预案',
      '加强过程监控'
    ];
  }

  _recommendMonitoringPoints(result) {
    return [
      '关键转译节点进展',
      '行动者参与度变化',
      '权力关系动态调整'
    ];
  }

  _generateMetadata(depth, options) {
    return {
      analysisType: 'ANT转译分析',
      formatDepth: depth,
      language: options.language || 'zh-CN',
      timestamp: this._formatTimestamp(new Date(), options),
      version: '1.0.0',
      confidence: this._assessConfidence(depth)
    };
  }

  _assessConfidence(depth) {
    const confidenceMap = {
      quick: 0.8,
      medium: 0.9,
      deep: 0.95
    };
    return confidenceMap[depth] || 0.8;
  }

  // 简化的其他格式化方法实现
  _describeAnalysisScope(result) {
    return '完整的ANT转译过程分析，涵盖四个核心环节';
  }

  _extractKeyFindings(result) {
    return [
      '转译过程基本完整',
      '行动者网络稳定发展',
      '权力关系相对平衡'
    ];
  }

  _provideOverallAssessment(result) {
    return '转译过程整体进展良好，建议继续巩固现有成果';
  }

  _formatProblematizationPhase(result) {
    return {
      status: 'completed',
      keyProblems: this._extractCoreProblems(result.basicSynthesis),
      solutions: result.basicSynthesis?.translationElements?.solutions || [],
      passagePoints: result.basicSynthesis?.translationElements?.obligatoryPassagePoints || []
    };
  }

  _formatInteressementPhase(result) {
    return {
      status: 'completed',
      strategies: result.basicSynthesis?.translationElements?.alignmentStrategies || [],
      targetActors: result.basicSynthesis?.actorNetwork?.targetActors || []
    };
  }

  _formatEnrollmentPhase(result) {
    return {
      status: 'completed',
      strategies: result.basicSynthesis?.translationElements?.enrollmentStrategies || [],
      enrolledActors: result.basicSynthesis?.actorNetwork?.targetActors || []
    };
  }

  _formatMobilizationPhase(result) {
    return {
      status: 'completed',
      mechanisms: result.basicSynthesis?.translationElements?.mobilizationMechanisms || [],
      blackBoxes: result.basicSynthesis?.blackBoxFormation?.blackBoxes || []
    };
  }

  _assessPhaseIntegration(result) {
    return '各环节衔接良好，整体协调性较强';
  }

  _describeNetworkStructure(basicSynthesis) {
    const actors = basicSynthesis.actorNetwork?.targetActors || [];
    return `包含${actors.length}个行动者的异质性网络`;
  }

  _analyzeActors(basicSynthesis) {
    return this._extractMainActors(basicSynthesis);
  }

  _mapRelationships(basicSynthesis) {
    return basicSynthesis.actorNetwork?.actorRelationships || [];
  }

  _describeNetworkDynamics(basicSynthesis) {
    return '网络持续发展和稳定化';
  }

  _summarizeConsistencyChecks(theoreticalAnalysis) {
    return theoreticalAnalysis.consistencyChecks || {};
  }

  _assessTheoreticalCompliance(theoreticalAnalysis) {
    return theoreticalAnalysis.overallConsistency ? '符合ANT理论要求' : '存在理论偏差';
  }

  _identifyImprovementAreas(theoreticalAnalysis) {
    return theoreticalAnalysis.recommendations || [];
  }

  _assessProcessProgress(processAnalysis) {
    return processAnalysis.phaseAnalysis || {};
  }

  _identifyCriticalTransitions(processAnalysis) {
    return processAnalysis.transitionAnalysis || {};
  }

  _evaluateProcessEfficiency(processAnalysis) {
    return processAnalysis.processDynamics || {};
  }

  _identifyProcessBottlenecks(processAnalysis) {
    return processAnalysis.processDynamics?.bottlenecks || [];
  }

  _generateStrategicRecommendations(result) {
    return [
      '完善转译过程的系统性',
      '加强网络稳定性建设',
      '优化权力关系配置'
    ];
  }

  _generateOperationalRecommendations(result) {
    return [
      '建立定期沟通机制',
      '完善监督评估体系',
      '制定应急预案'
    ];
  }

  _provideRiskManagementAdvice(result) {
    return [
      '识别和管理关键风险',
      '建立风险预警机制',
      '制定风险应对策略'
    ];
  }

  _outlineNextSteps(result) {
    return [
      '继续完善动员机制',
      '加强过程监控',
      '评估长期效果'
    ];
  }

  _formatChineseContext(chineseAdaptation, options) {
    if (!chineseAdaptation || !chineseAdaptation.adapted) {
      return { title: '中文本土化', status: '未启用' };
    }

    return {
      title: '中文本土化分析',
      adaptationLevel: chineseAdaptation.adaptationEffectiveness?.culturalFit || 'medium',
      chineseFeatures: chineseAdaptation.chineseFeatures || {},
      adaptationMechanisms: chineseAdaptation.adaptationMechanisms || {}
    };
  }

  // 其他深度分析方法的简化实现
  _analyzeANTFrameworkApplication(result) { return { compliance: 'high', adaptations: [] }; }
  _explainTheoreticalFoundations(result) { return { primaryTheory: 'ANT', supportingTheories: [] }; }
  _detailConceptualMapping(result) { return { mappings: [], gaps: [] }; }
  _explainMethodologicalApproach(result) { return { approach: 'multi_phase_analysis', tools: [] }; }

  _analyzeNetworkTopology(result) { return { type: 'heterogeneous', density: 0.6, centralization: 0.5 }; }
  _analyzePowerStructures(result) { return { distribution: 'balanced', sources: [] }; }
  _analyzeResourceFlows(result) { return { volume: 'medium', efficiency: 0.7 }; }
  _analyzeInformationFlows(result) { return { volume: 'medium', clarity: 0.7 }; }
  _traceNetworkEvolution(result) { return { stages: [], patterns: [] }; }

  _performTemporalAnalysis(result) { return { timeline: [], patterns: [] }; }
  _identifyCausalMechanisms(result) { return { mechanisms: [], interactions: [] }; }
  _identifyFeedbackLoops(result) { return { loops: [], effects: [] }; }
  _identifyEmergencePatterns(result) { return { patterns: [], significance: [] }; }

  _identifyBlackBoxes(result) { return result.basicSynthesis?.blackBoxFormation?.blackBoxes || []; }
  _explainFormationMechanisms(result) { return { mechanisms: [], processes: [] }; }
  _assessBlackBoxStability(result) { return { stability: 0.7, factors: [] }; }
  _analyzeIrreversibility(result) { return { level: 'medium', factors: [] }; }

  _analyzePowerSources(result) { return { sources: [], distribution: [] }; }
  _analyzePowerMechanisms(result) { return { mechanisms: [], effectiveness: [] }; }
  _analyzePowerEffects(result) { return { effects: [], outcomes: [] }; }
  _analyzePowerLegitimacy(result) { return { legitimacy: 0.8, sources: [] }; }

  _analyzeCulturalSystem(result) { return { characteristics: [], implications: [] }; }
  _analyzeInstitutionalContext(result) { return { context: [], constraints: [] }; }
  _analyzeAdaptationMechanisms(result) { return { mechanisms: [], effectiveness: [] }; }
  _performComparativeAnalysis(result) { return { comparisons: [], insights: [] }; }

  _describeDataCollection(result) { return { sources: [], methods: [], limitations: [] }; }
  _explainAnalyticalMethods(result) { return { methods: [], tools: [], validation: [] }; }
  _discussLimitations(result) { return { limitations: [], impacts: [], mitigations: [] }; }
  _describeValidityMeasures(result) { return { measures: [], results: [] }; }

  _proposeResearchQuestions(result) { return { questions: [], significance: [] }; }
  _suggestMethodologicalExtensions(result) { return { extensions: [], benefits: [] }; }
  _identifyTheoreticalContributions(result) { return { contributions: [], implications: [] }; }
  _suggestPracticalApplications(result) { return { applications: [], benefits: [] }; }

  _includeRawData(result) { return { availability: 'on_request', format: 'structured' }; }
  _includeTechnicalDetails(result) { return { details: [], specifications: [] }; }
  _includeReferences(result) { return { references: [], citations: [] }; }
  _includeGlossary(result) { return { terms: [], definitions: [] }; }

  _generateErrorSuggestions(error) {
    return ['检查输入数据格式', '验证分析参数设置', '重试分析过程'];
  }

  _suggestRecoveryOptions(error) {
    return ['使用简化分析模式', '检查数据完整性', '联系技术支持'];
  }
}

module.exports = OutputFormatter;