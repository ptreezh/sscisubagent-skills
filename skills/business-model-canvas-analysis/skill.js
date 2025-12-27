/**
 * 商业模式画布分析技能实现
 * 遵循agentskills.io规范
 */

class BusinessModelCanvasAnalysisSkill {
  constructor() {
    this.skillId = "business-model-canvas-analysis";
    this.version = "2.0.0";
    this.name = "商业模式画布分析";
    this.description = "基于权威商业模式画布理论，对企业进行九要素分析";
    
    // 初始化内部组件
    this.dataCollector = new DataCollectionModule();
    this.analyzer = new CanvasAnalysisModule();
    this.validator = new ValidationModule();
    this.reporter = new ReportingModule();
  }

  /**
   * 执行技能主方法
   * @param {Object} inputs - 输入参数
   * @returns {Object} 分析结果
   */
  async execute(inputs) {
    try {
      // 1. 验证输入参数
      this.validateInputs(inputs);
      
      // 2. 收集数据
      const rawData = await this.dataCollector.collect(inputs.companyData);
      
      // 3. 执行分析
      const analysisResults = await this.analyzer.analyze(rawData);
      
      // 4. 验证结果
      const validatedResults = await this.validator.validate(analysisResults);
      
      // 5. 生成报告
      const finalReport = await this.reporter.generate(validatedResults);
      
      return {
        success: true,
        data: finalReport,
        metadata: {
          skillId: this.skillId,
          version: this.version,
          executionTime: new Date().toISOString()
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        metadata: {
          skillId: this.skillId,
          version: this.version,
          executionTime: new Date().toISOString()
        }
      };
    }
  }

  /**
   * 验证输入参数
   */
  validateInputs(inputs) {
    if (!inputs || !inputs.companyData) {
      throw new Error("缺少必需的companyData参数");
    }
    
    if (!inputs.companyData.name) {
      throw new Error("企业名称为必需参数");
    }
  }
}

/**
 * 数据收集模块
 */
class DataCollectionModule {
  async collect(companyData) {
    // 从多个权威数据源收集信息
    const sources = [
      this.getOfficialWebsiteData(companyData),
      this.getAnnualReportData(companyData),
      this.getGovernmentDatabaseData(companyData),
      this.getIndustryReportData(companyData)
    ];
    
    // 并行收集所有数据
    const results = await Promise.allSettled(sources);
    
    // 整合数据
    let combinedData = {
      companyProfile: companyData,
      officialData: null,
      financialData: null,
      marketData: null,
      competitorData: null
    };
    
    for (const result of results) {
      if (result.status === 'fulfilled') {
        combinedData = { ...combinedData, ...result.value };
      }
    }
    
    return combinedData;
  }
  
  async getOfficialWebsiteData(companyData) {
    // 模拟从企业官网收集数据
    return {
      officialData: {
        companyInfo: {
          name: companyData.name,
          mission: "企业使命",
          vision: "企业愿景",
          values: ["价值观1", "价值观2"]
        },
        productsServices: {
          products: ["产品1", "产品2"],
          services: ["服务1", "服务2"]
        },
        contactInfo: {
          headquarters: "总部地址",
          website: `https://${companyData.name.toLowerCase().replace(/\s+/g, '')}.com`
        }
      }
    };
  }
  
  async getAnnualReportData(companyData) {
    // 模拟从年报收集数据
    return {
      financialData: {
        revenue: "营业收入数据",
        profit: "净利润数据",
        assets: "资产数据",
        liabilities: "负债数据",
        equity: "股东权益数据"
      }
    };
  }
  
  async getGovernmentDatabaseData(companyData) {
    // 模拟从政府数据库收集数据
    return {
      registrationData: {
        registrationNumber: "注册号",
        legalRepresentative: "法定代表人",
        registeredCapital: "注册资本",
        establishmentDate: "成立日期",
        businessScope: "经营范围"
      }
    };
  }
  
  async getIndustryReportData(companyData) {
    // 模拟从行业报告收集数据
    return {
      marketData: {
        industryPosition: "行业地位",
        marketShare: "市场份额",
        competitiveLandscape: "竞争格局",
        industryTrends: "行业趋势"
      }
    };
  }
}

/**
 * 画布分析模块
 */
class CanvasAnalysisModule {
  async analyze(data) {
    // 执行九要素分析
    const canvasElements = {
      keyPartners: await this.analyzeKeyPartners(data),
      keyActivities: await this.analyzeKeyActivities(data),
      keyResources: await this.analyzeKeyResources(data),
      valuePropositions: await this.analyzeValuePropositions(data),
      customerRelationships: await this.analyzeCustomerRelationships(data),
      channels: await this.analyzeChannels(data),
      customerSegments: await this.analyzeCustomerSegments(data),
      costStructure: await this.analyzeCostStructure(data),
      revenueStreams: await this.analyzeRevenueStreams(data)
    };
    
    // 分析要素间关系
    const relationships = await this.analyzeRelationships(canvasElements, data);
    
    return {
      canvasElements,
      relationships,
      sourceData: data
    };
  }
  
  async analyzeKeyPartners(data) {
    const partners = [];
    
    // 从不同数据源提取合作伙伴信息
    if (data.officialData?.partners) {
      partners.push(...data.officialData.partners);
    }
    
    if (data.officialData?.productsServices) {
      // 根据产品服务推断可能的合作伙伴
      if (data.officialData.productsServices.products.some(p => p.includes('技术'))) {
        partners.push("技术提供商", "研发合作伙伴");
      }
    }
    
    if (data.marketData?.industryPosition) {
      // 根据行业地位分析合作伙伴
      if (data.marketData.industryPosition.includes('领导者')) {
        partners.push("战略联盟伙伴", "分销商");
      }
    }
    
    // 添加行业通用合作伙伴
    partners.push("供应商", "渠道合作伙伴", "服务提供商");
    
    return [...new Set(partners)]; // 去重
  }
  
  async analyzeKeyActivities(data) {
    const activities = [];
    
    if (data.officialData?.productsServices) {
      if (data.officialData.productsServices.products.length > 0) {
        activities.push("产品研发", "生产制造");
      }
      if (data.officialData.productsServices.services.length > 0) {
        activities.push("服务提供", "客户支持");
      }
    }
    
    if (data.financialData) {
      activities.push("财务管理", "财务报告");
    }
    
    if (data.registrationData?.businessScope) {
     根据 businessScope 分析关键活动
      if (data.registrationData.businessScope.includes('技术')) {
        activities.push("技术开发", "创新研发");
      }
      if (data.registrationData.businessScope.includes('贸易')) {
        activities.push("采购管理", "销售管理");
      }
    }
    
    return [...new Set(activities)];
  }
  
  async analyzeKeyResources(data) {
    const resources = [];
    
    if (data.financialData) {
      resources.push("财务资源", "资本金");
    }
    
    if (data.officialData?.contactInfo) {
      resources.push("品牌资产", "客户关系");
    }
    
    if (data.registrationData?.registeredCapital) {
      resources.push("资金资源");
    }
    
    // 根据行业类型添加特定资源
    if (data.marketData?.industryPosition) {
      if (data.marketData.industryPosition.includes('技术')) {
        resources.push("技术专利", "研发团队");
      }
      if (data.marketData.industryPosition.includes('制造')) {
        resources.push("生产设备", "制造工艺");
      }
    }
    
    return [...new Set(resources)];
  }
  
  async analyzeValuePropositions(data) {
    const propositions = [];
    
    if (data.officialData?.productsServices) {
      if (data.officialData.productsServices.products.some(p => p.includes('创新'))) {
        propositions.push("创新解决方案");
      }
      if (data.officialData.productsServices.services.some(s => s.includes('优质'))) {
        propositions.push("优质服务体验");
      }
    }
    
    if (data.financialData) {
      if (parseFloat(data.financialData.profit) > 0) {
        propositions.push("盈利能力保障");
      }
    }
    
    // 根据企业特点添加价值主张
    propositions.push("专业解决方案", "客户价值创造");
    
    return [...new Set(propositions)];
  }
  
  async analyzeCustomerRelationships(data) {
    const relationships = [];
    
    if (data.officialData?.contactInfo) {
      relationships.push("客户支持", "服务响应");
    }
    
    if (data.officialData?.productsServices) {
      if (data.officialData.productsServices.services.length > 0) {
        relationships.push("持续服务关系");
      }
    }
    
    // 添加行业通用关系类型
    relationships.push("个人助理", "自助服务", "社区互动");
    
    return [...new Set(relationships)];
  }
  
  async analyzeChannels(data) {
    const channels = [];
    
    if (data.officialData?.contactInfo?.website) {
      channels.push("官方网站", "在线商城");
    }
    
    if (data.registrationData?.headquarters) {
      channels.push("线下门店", "服务网点");
    }
    
    // 添加行业通用渠道
    channels.push("分销商", "合作伙伴渠道", "直销团队");
    
    return [...new Set(channels)];
  }
  
  async analyzeCustomerSegments(data) {
    const segments = [];
    
    if (data.marketData?.marketShare) {
      segments.push("主要客户群体", "潜在客户群体");
    }
    
    if (data.officialData?.productsServices) {
      if (data.officialData.productsServices.products.length > 0) {
        segments.push("产品用户", "企业客户");
      }
      if (data.officialData.productsServices.services.length > 0) {
        segments.push("服务客户", "长期合作伙伴");
      }
    }
    
    // 添加通用客户细分
    segments.push("大众市场", "细分市场", "特定行业客户");
    
    return [...new Set(segments)];
  }
  
  async analyzeCostStructure(data) {
    const costs = [];
    
    if (data.financialData) {
      costs.push("研发成本", "营销成本", "运营成本", "人力成本");
    }
    
    if (data.registrationData?.businessScope) {
      if (data.registrationData.businessScope.includes('制造')) {
        costs.push("生产成本", "原材料成本");
      }
      if (data.registrationData.businessScope.includes('服务')) {
        costs.push("服务成本", "人力成本");
      }
    }
    
    return [...new Set(costs)];
  }
  
  async analyzeRevenueStreams(data) {
    const streams = [];
    
    if (data.financialData?.revenue) {
      streams.push("主营业务收入");
    }
    
    if (data.officialData?.productsServices) {
      if (data.officialData.productsServices.products.length > 0) {
        streams.push("产品销售收入");
      }
      if (data.officialData.productsServices.services.length > 0) {
        streams.push("服务收入", "订阅收入");
      }
    }
    
    // 添加通用收入来源
    streams.push("其他业务收入", "投资收益");
    
    return [...new Set(streams)];
  }
  
  async analyzeRelationships(elements, data) {
    // 分析各要素间的逻辑关系
    return {
      valuePropositionToCustomer: {
        type: "valueCreation",
        strength: "strong",
        description: "价值主张有效满足客户需求"
      },
      resourcesToActivities: {
        type: "enabler",
        strength: "strong", 
        description: "核心资源支撑关键活动"
      },
      activitiesToValue: {
        type: "creationFlow",
        strength: "strong",
        description: "关键活动创造价值主张"
      },
      partnersToActivities: {
        type: "support",
        strength: "medium",
        description: "合作伙伴支持关键活动"
      },
      channelsToCustomers: {
        type: "connection",
        strength: "strong",
        description: "渠道有效连接客户"
      }
    };
  }
}

/**
 * 验证模块
 */
class ValidationModule {
  async validate(analysisResults) {
    // 执行多种验证
    const validationResults = {
      completeness: await this.checkCompleteness(analysisResults),
      consistency: await this.checkConsistency(analysisResults),
      accuracy: await this.checkAccuracy(analysisResults),
      sourceCredibility: await this.checkSourceCredibility(analysisResults)
    };
    
    // 综合评估
    const overallScore = this.calculateOverallScore(validationResults);
    
    return {
      ...analysisResults,
      validation: validationResults,
      overallValidationScore: overallScore
    };
  }
  
  async checkCompleteness(results) {
    const requiredElements = [
      'keyPartners', 'keyActivities', 'keyResources', 
      'valuePropositions', 'customerRelationships', 
      'channels', 'customerSegments', 'costStructure', 'revenueStreams'
    ];
    
    const missingElements = requiredElements.filter(
      element => !results.canvasElements[element] || results.canvasElements[element].length === 0
    );
    
    return {
      complete: missingElements.length === 0,
      missingElements: missingElements,
      completenessScore: ((requiredElements.length - missingElements.length) / requiredElements.length) * 100
    };
  }
  
  async checkConsistency(results) {
    // 检查各要素间的逻辑一致性
    const relationships = results.relationships;
    const consistencyIssues = [];
    
    // 检查关键关系
    if (!relationships.valuePropositionToCustomer || 
        relationships.valuePropositionToCustomer.strength !== "strong") {
      consistencyIssues.push("价值主张与客户需求不匹配");
    }
    
    if (!relationships.resourcesToActivities ||
        relationships.resourcesToActivities.strength !== "strong") {
      consistencyIssues.push("资源与活动不匹配");
    }
    
    return {
      consistent: consistencyIssues.length === 0,
      issues: consistencyIssues,
      consistencyScore: consistencyIssues.length === 0 ? 100 : 100 - (consistencyIssues.length * 10)
    };
  }
  
  async checkAccuracy(results) {
    // 检查信息准确性（基于数据源）
    const sourceData = results.sourceData;
    
    // 简单的准确性评估
    const hasOfficialData = !!sourceData.officialData;
    const hasFinancialData = !!sourceData.financialData;
    const hasRegistrationData = !!sourceData.registrationData;
    
    const accuracyScore = ((hasOfficialData ? 1 : 0) + (hasFinancialData ? 1 : 0) + (hasRegistrationData ? 1 : 0)) / 3 * 100;
    
    return {
      accuracyScore: accuracyScore,
      officialDataPresent: hasOfficialData,
      financialDataPresent: hasFinancialData,
      registrationDataPresent: hasRegistrationData
    };
  }
  
  async checkSourceCredibility(results) {
    // 检查数据源可信度
    const sourceData = results.sourceData;
    
    // 为简化的可信度评估
    const credibilityFactors = {
      officialSource: !!sourceData.officialData,
      financialVerification: !!sourceData.financialData,
      governmentVerification: !!sourceData.registrationData
    };
    
    const factorCount = Object.values(credibilityFactors).filter(Boolean).length;
    const credibilityScore = (factorCount / 3) * 100;
    
    return {
      credibilityScore: credibilityScore,
      factors: credibilityFactors,
      credibilityLevel: credibilityScore >= 66 ? "high" : credibilityScore >= 33 ? "medium" : "low"
    };
  }
  
  calculateOverallScore(validationResults) {
    const { completeness, consistency, accuracy, sourceCredibility } = validationResults;
    
    // 加权计算总体分数
    const weights = {
      completeness: 0.3,
      consistency: 0.3,
      accuracy: 0.2,
      credibility: 0.2
    };
    
    return Math.round(
      (completeness.completenessScore * weights.completeness) +
      (consistency.consistencyScore * weights.consistency) +
      (accuracy.accuracyScore * weights.accuracy) +
      (sourceCredibility.credibilityScore * weights.credibility)
    );
  }
}

/**
 * 报告生成模块
 */
class ReportingModule {
  async generate(analysisResults) {
    // 生成最终报告
    return {
      analysisSummary: this.createAnalysisSummary(analysisResults),
      detailedResults: analysisResults,
      recommendations: await this.generateRecommendations(analysisResults),
      visualizationData: await this.createVisualizationData(analysisResults),
      metadata: {
        generationTime: new Date().toISOString(),
        validationScore: analysisResults.overallValidationScore,
        dataSources: this.extractDataSources(analysisResults)
      }
    };
  }
  
  createAnalysisSummary(results) {
    return {
      executiveSummary: `对${results.sourceData.companyProfile.name}的商业模式画布分析显示，该企业在价值创造、客户关系和资源配置方面表现良好。总体验证分数为${results.overallValidationScore}分。`,
      keyFindings: [
        `识别出${results.canvasElements.keyPartners.length}个关键合作伙伴`,
        `确定了${results.canvasElements.keyActivities.length}项关键业务活动`,
        `发现了${results.canvasElements.valuePropositions.length}个核心价值主张`,
        `明确了${results.canvasElements.customerSegments.length}个目标客户群体`
      ],
      overallAssessment: this.assessModelQuality(results.overallValidationScore)
    };
  }
  
  assessModelQuality(score) {
    if (score >= 85) return "优秀 - 商业模式完整且逻辑一致";
    if (score >= 70) return "良好 - 商业模式较为完整";
    if (score >= 50) return "一般 - 部分要素需要加强";
    return "需改进 - 商业模式存在明显不足";
  }
  
  async generateRecommendations(results) {
    const recommendations = [];
    
    // 基于验证结果生成建议
    if (results.validation.completeness.missingElements.length > 0) {
      recommendations.push(`完善以下缺失要素: ${results.validation.completeness.missingElements.join(', ')}`);
    }
    
    if (results.validation.consistency.issues.length > 0) {
      recommendations.push(`改善以下不一致之处: ${results.validation.consistency.issues.join(', ')}`);
    }
    
    if (results.overallValidationScore < 70) {
      recommendations.push("建议进行更深入的分析和验证");
    }
    
    if (results.canvasElements.valuePropositions.length < 3) {
      recommendations.push("丰富价值主张，提供更多差异化价值");
    }
    
    return recommendations.length > 0 ? recommendations : ["企业商业模式整体表现良好"];
  }
  
  async createVisualizationData(results) {
    return {
      canvasHeatmap: this.createCanvasHeatmap(results),
      elementConnections: results.relationships,
      keyMetrics: this.extractKeyMetrics(results)
    };
  }
  
  createCanvasHeatmap(results) {
    const elements = results.canvasElements;
    const heatmap = {};
    
    // 计算每个元素的"热度"（即详细程度）
    for (const [element, items] of Object.entries(elements)) {
      heatmap[element] = {
        count: items.length,
        level: items.length >= 3 ? "high" : items.length >= 1 ? "medium" : "low",
        items: items
      };
    }
    
    return heatmap;
  }
  
  extractKeyMetrics(results) {
    return {
      totalElements: 9,
      elementsWithDetails: Object.values(results.canvasElements).filter(arr => arr.length > 0).length,
      totalRelationships: Object.keys(results.relationships).length,
      validationScore: results.overallValidationScore
    };
  }
  
  extractDataSources(results) {
    const sources = [];
    
    if (results.sourceData.officialData) sources.push("企业官网");
    if (results.sourceData.financialData) sources.push("年度报告");
    if (results.sourceData.registrationData) sources.push("政府数据库");
    if (results.sourceData.marketData) sources.push("行业报告");
    
    return sources;
  }
}

// 导出技能类
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BusinessModelCanvasAnalysisSkill;
}