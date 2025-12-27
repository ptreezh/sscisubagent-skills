/**
 * 资本分析技能实现
 * 遵循agentskills.io规范和渐进式披露原则
 * 定量分析程序化，定性分析AI化
 */

class CapitalAnalysisSkill {
  constructor() {
    this.skillId = "capital-analysis";
    this.version = "2.0.0";
    this.name = "资本分析";
    this.description = "基于现代金融理论，对企业资本结构和融资策略进行分析";
    
    // 初始化模块
    this.dataCollector = new CapitalDataCollectionModule();
    this.analyzer = new CapitalAnalysisModule();
    this.validator = new CapitalValidationModule();
    this.reporter = new CapitalReportingModule();
  }

  /**
   * 执行技能主方法
   * 实现渐进式披露：根据focusAreas参数决定分析详略程度
   */
  async execute(inputs) {
    try {
      // 验证输入参数
      this.validateInputs(inputs);
      
      // 收集财务数据
      const financialData = await this.dataCollector.collect(inputs.companyData);
      
      // 执行分析（可选择关注领域以控制上下文）
      const analysisResults = await this.analyzer.analyze(
        financialData, 
        inputs.focusAreas || null,  // 支持指定关注领域
        inputs.detailedAnalysis || false  // 支持详细/摘要分析
      );
      
      // 验证结果
      const validatedResults = await this.validator.validate(analysisResults);
      
      // 生成报告（支持不同详细程度）
      const finalReport = await this.reporter.generate(
        validatedResults, 
        inputs.detailedReport || false,
        inputs.comparativeAnalysis || false
      );
      
      return {
        success: true,
        data: finalReport,
        metadata: {
          skillId: this.skillId,
          version: this.version,
          executionTime: new Date().toISOString(),
          contextLevel: inputs.detailedReport ? "detailed" : "summary",
          focusAreas: inputs.focusAreas || "all"
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
 * 资本数据收集模块
 * 程序化执行财务数据收集
 */
class CapitalDataCollectionModule {
  async collect(companyData) {
    // 并行收集财务相关信息
    const [financialStatements, marketData, creditInfo, industryData] = await Promise.allSettled([
      this.getFinancialStatements(companyData),
      this.getMarketData(companyData),
      this.getCreditInformation(companyData),
      this.getIndustryData(companyData)
    ]);
    
    return {
      companyProfile: companyData,
      financialStatements: financialStatements.status === 'fulfilled' ? financialStatements.value : null,
      marketData: marketData.status === 'fulfilled' ? marketData.value : null,
      creditInfo: creditInfo.status === 'fulfilled' ? creditInfo.value : null,
      industryData: industryData.status === 'fulfilled' ? industryData.value : null
    };
  }
  
  async getFinancialStatements(companyData) {
    // 模拟从财务报表获取数据
    return {
      balanceSheet: {
        totalAssets: 10000000000, // 总资产
        totalLiabilities: 4000000000, // 总负债
        shareholdersEquity: 6000000000, // 股东权益
        currentAssets: 6000000000, // 流动资产
        currentLiabilities: 2000000000 // 流动负债
      },
      incomeStatement: {
        revenue: 5000000000, // 营业收入
        netIncome: 500000000, // 净利润
        ebit: 800000000, // 息税前利润
        interestExpense: 100000000 // 利息费用
      },
      cashFlowStatement: {
        operatingCashFlow: 700000000, // 经营现金流
        investingCashFlow: -300000000, // 投资现金流
        financingCashFlow: -100000000 // 筹资现金流
      }
    };
  }
  
  async getMarketData(companyData) {
    // 模拟从市场获取数据
    return {
      marketCap: 15000000000, // 市值
      stockPrice: 50.00, // 股价
      peRatio: 30.0, // 市盈率
      pbRatio: 2.5 // 市净率
    };
  }
  
  async getCreditInformation(companyData) {
    // 模拟从信用机构获取信息
    return {
      creditRating: "A",
      debtCapacity: 2000000000,
      borrowingCost: 0.045 // 借款成本4.5%
    };
  }
  
  async getIndustryData(companyData) {
    // 模拟获取行业基准数据
    return {
      industryAverage: {
        debtToEquity: 0.55,
        roe: 0.12,
        roa: 0.06,
        interestCoverage: 8.0
      },
      competitivePosition: "行业前20%"
    };
  }
}

/**
 * 资本分析模块
 * 定量计算程序化，定性分析AI化
 */
class CapitalAnalysisModule {
  async analyze(data, focusAreas = null, detailed = false) {
    // 根据focusAreas决定分析详略程度，实现渐进式披露
    const analysis = {};
    
    // 资本结构分析（定量，程序化）
    if (!focusAreas || focusAreas.includes('capitalStructure')) {
      analysis.capitalStructure = await this.analyzeCapitalStructure(data, detailed);
    }
    
    // 融资模式分析（定量+定性）
    if (!focusAreas || focusAreas.includes('financingPattern')) {
      analysis.financingPattern = await this.analyzeFinancingPattern(data, detailed);
    }
    
    // 投资策略分析（定量+定性）
    if (!focusAreas || focusAreas.includes('investmentStrategy')) {
      analysis.investmentStrategy = await this.analyzeInvestmentStrategy(data, detailed);
    }
    
    // 风险状况分析（定量+定性）
    if (!focusAreas || focusAreas.includes('riskProfile')) {
      analysis.riskProfile = await this.analyzeRiskProfile(data, detailed);
    }
    
    // 估值分析（定量，程序化）
    if (!focusAreas || focusAreas.includes('valuationMetrics')) {
      analysis.valuationMetrics = await this.analyzeValuationMetrics(data, detailed);
    }
    
    // 现金流分析（定量，程序化）
    if (!focusAreas || focusAreas.includes('cashFlowAnalysis')) {
      analysis.cashFlowAnalysis = await this.analyzeCashFlow(data, detailed);
    }
    
    // 融资需求分析（定量+定性）
    if (!focusAreas || focusAreas.includes('financingNeeds')) {
      analysis.financingNeeds = await this.analyzeFinancingNeeds(data, detailed);
    }
    
    // 投资者关系分析（定性）
    if (!focusAreas || focusAreas.includes('investorRelations')) {
      analysis.investorRelations = await this.analyzeInvestorRelations(data, detailed);
    }
    
    return {
      capitalElements: analysis,
      financialData: data,
      analysisTimestamp: new Date().toISOString()
    };
  }
  
  async analyzeCapitalStructure(data, detailed = false) {
    // 程序化计算资本结构指标
    const fs = data.financialStatements;
    if (!fs || !fs.balanceSheet) {
      return {
        debtToEquity: "数据不足",
        debtRatio: "数据不足",
        equityRatio: "数据不足",
        analysis: "需要完整财务报表数据"
      };
    }
    
    const bs = fs.balanceSheet;
    const debtToEquity = bs.totalLiabilities / bs.shareholdersEquity;
    const debtRatio = bs.totalLiabilities / bs.totalAssets;
    const equityRatio = bs.shareholdersEquity / bs.totalAssets;
    
    // 评估合理性
    const assessment = this.assessCapitalStructureReasonableness(debtToEquity, data.industryData);
    
    const result = {
      debtToEquity: parseFloat(debtToEquity.toFixed(4)),
      debtRatio: parseFloat(debtRatio.toFixed(4)),
      equityRatio: parseFloat(equityRatio.toFixed(4)),
      assessment: assessment,
      leverageMetrics: {
        debtToEquity: parseFloat(debtToEquity.toFixed(4)),
        debtRatio: parseFloat(debtRatio.toFixed(4)),
        equityRatio: parseFloat(equityRatio.toFixed(4)),
        debtToAsset: parseFloat(debtRatio.toFixed(4))
      }
    };
    
    // 详细分析包含更多指标
    if (detailed) {
      result.comprehensiveMetrics = {
        debtToEquity: parseFloat(debtToEquity.toFixed(4)),
        debtRatio: parseFloat(debtRatio.toFixed(4)),
        equityRatio: parseFloat(equityRatio.toFixed(4)),
        debtToAsset: parseFloat(debtRatio.toFixed(4)),
        equityMultiplier: bs.totalAssets / bs.shareholdersEquity,
        longTermDebtRatio: (bs.totalLiabilities - 2000000000) / bs.totalAssets // 假设长期负债
      };
    }
    
    return result;
  }
  
  assessCapitalStructureReasonableness(debtToEquity, industryData) {
    if (!industryData || !industryData.industryAverage) {
      // 一般标准
      if (debtToEquity > 1.0) return "债务比例偏高";
      if (debtToEquity < 0.3) return "债务比例偏低";
      return "债务比例合理";
    }
    
    const industryAverage = industryData.industryAverage.debtToEquity;
    if (debtToEquity > industryAverage * 1.5) return "显著高于行业平均";
    if (debtToEquity < industryAverage * 0.5) return "显著低于行业平均";
    return "与行业平均基本一致";
  }
  
  async analyzeFinancingPattern(data, detailed = false) {
    // 分析融资模式
    const fs = data.financialStatements;
    const credit = data.creditInfo;
    
    const result = {
      primarySources: ["股权融资", "债务融资"],
      financingStrategy: "股权债权平衡策略",
      costMetrics: {
        estimatedWACC: 0.075, // 7.5%加权平均资本成本
        debtCost: credit?.borrowingCost || 0.05,
        equityCost: 0.09 // 假设9%
      },
      structureAssessment: "融资结构相对均衡"
    };
    
    if (detailed) {
      result.detailedPattern = {
        equityFinancing: 60 + "%",
        debtFinancing: 40 + "%",
        internalFunding: "主要为留存收益",
        financingDiversity: "多渠道融资，风险分散"
      };
    }
    
    return result;
  }
  
  async analyzeInvestmentStrategy(data, detailed = false) {
    // 分析投资策略
    const fs = data.financialStatements;
    
    const result = {
      investmentFocus: ["业务扩张", "研发创新", "数字化转型"],
      allocationPattern: {
        growthInvestment: 60 + "%",
        maintenanceInvestment: 40 + "%"
      },
      efficiencyMetrics: {
        roic: 0.12, // 投资资本回报率
        roi: 0.15   // 投资回报率
      }
    };
    
    if (detailed) {
      result.detailedStrategy = {
        capexAllocation: {
          "研发投资": 35 + "%",
          "产能扩张": 25 + "%",
          "技术升级": 20 + "%",
          "并购整合": 20 + "%"
        },
        investmentCriteria: ["ROIC > WACC", "战略协同", "风险可控"],
        portfolioDiversity: "业务线和地域多元化"
      };
    }
    
    return result;
  }
  
  async analyzeRiskProfile(data, detailed = false) {
    // 分析风险状况
    const fs = data.financialStatements;
    
    const result = {
      riskType: {
        financialRisk: "中等",
        marketRisk: "中等",
        liquidityRisk: "低"
      },
      riskMetrics: {
        interestCoverage: fs?.incomeStatement ? 
          fs.incomeStatement.ebit / fs.incomeStatement.interestExpense : null,
        debtServiceCoverage: 3.5 // 假设值
      },
      riskManagement: "建立了风险管理体系"
    };
    
    if (detailed) {
      result.comprehensiveRiskProfile = {
        creditRisk: "低",
        marketRisk: "中等",
        operationalRisk: "中等",
        liquidityRisk: "低",
        concentrationRisk: "业务相对分散",
        hedgingStrategies: ["利率对冲", "汇率对冲"]
      };
    }
    
    return result;
  }
  
  async analyzeValuationMetrics(data, detailed = false) {
    // 计算估值指标
    const fs = data.financialStatements;
    const market = data.marketData;
    
    const result = {
      valuationMultiples: {
        pe: market?.peRatio || null,
        pb: market?.pbRatio || null,
        evEbitda: null // 需要更多信息计算
      },
      valueAssessment: market?.peRatio ? 
        (market.peRatio > 25 ? "估值偏高" : "估值合理") : "需要市场数据"
    };
    
    if (detailed) {
      result.fullValuation = {
        marketCap: market?.marketCap,
        enterpriseValue: market?.marketCap + 4000000000 - null, // 市值+净债务
        valuationRatios: {
          pe: market?.peRatio,
          pb: market?.pbRatio,
          ps: market?.marketCap / fs?.incomeStatement?.revenue,
          pcf: market?.marketCap / fs?.cashFlowStatement?.operatingCashFlow
        }
      };
    }
    
    return result;
  }
  
  async analyzeCashFlow(data, detailed = false) {
    // 分析现金流状况
    const fs = data.financialStatements;
    
    const result = {
      operatingCash: fs?.cashFlowStatement?.operatingCashFlow || 0,
      investmentCash: fs?.cashFlowStatement?.investingCashFlow || 0,
      financingCash: fs?.cashFlowStatement?.financingCashFlow || 0,
      freeCashFlow: (fs?.cashFlowStatement?.operatingCashFlow || 0) - Math.abs(fs?.cashFlowStatement?.investingCashFlow || 0),
      cashEfficiency: "现金流状况良好"
    };
    
    if (detailed) {
      result.detailedCashFlow = {
        operatingCashFlow: fs?.cashFlowStatement?.operatingCashFlow,
        investingCashFlow: fs?.cashFlowStatement?.investingCashFlow,
        financingCashFlow: fs?.cashFlowStatement?.financingCashFlow,
        freeCashFlow: result.freeCashFlow,
        cashConversionCycle: "需要更多运营数据",
        cashPerShare: (fs?.cashFlowStatement?.operatingCashFlow || 0) / (data.marketData?.marketCap / data.marketData?.stockPrice || 1)
      };
    }
    
    return result;
  }
  
  async analyzeFinancingNeeds(data, detailed = false) {
    // 分析融资需求
    const fs = data.financialStatements;
    
    const result = {
      nearTermNeeds: ["业务扩张资金", "债务重组"],
      estimatedAmount: 1500000000,
      financingPriority: ["成本最低优先", "控制权影响最小优先"]
    };
    
    if (detailed) {
      result.comprehensiveNeeds = {
        growthFinancing: 1000000000,
        workingCapital: 300000000,
        debtRefinancing: 200000000,
        financingOptions: ["增发股票", "发行债券", "银行贷款"]
      };
    }
    
    return result;
  }
  
  async analyzeInvestorRelations(data, detailed = false) {
    // 分析投资者关系
    const market = data.marketData;
    
    const result = {
      investorType: ["机构投资者", "个人投资者"],
      marketPerception: market?.peRatio ? 
        (market.peRatio > 20 ? "市场评价较高" : "市场评价适中") : "需要市场数据",
      communicationEffectiveness: "建立了有效的投资者沟通机制"
    };
    
    if (detailed) {
      result.detailedRelations = {
        shareholderStructure: "机构投资者占主导",
        disclosureQuality: "信息披露及时充分",
        engagementLevel: "投资者参与度高",
        esgConsideration: "重视ESG因素"
      };
    }
    
    return result;
  }
}

/**
 * 资本验证模块
 */
class CapitalValidationModule {
  async validate(analysisResults) {
    const validationResults = {
      dataCompleteness: await this.checkDataCompleteness(analysisResults),
      calculationAccuracy: await this.checkCalculationAccuracy(analysisResults),
      consistency: await this.checkConsistency(analysisResults),
      industryAlignment: await this.checkIndustryAlignment(analysisResults)
    };
    
    const overallScore = this.calculateOverallScore(validationResults);
    
    return {
      ...analysisResults,
      validation: validationResults,
      overallValidationScore: overallScore
    };
  }
  
  async checkDataCompleteness(results) {
    const sourceData = results.financialData;
    const completenessFactors = {
      financialStatements: !!sourceData.financialStatements,
      marketData: !!sourceData.marketData,
      industryBenchmarks: !!sourceData.industryData
    };
    
    const factorCount = Object.values(completenessFactors).filter(Boolean).length;
    const completenessScore = (factorCount / 3) * 100;
    
    return {
      factors: completenessFactors,
      completenessScore: completenessScore,
      level: completenessScore >= 66 ? "high" : completenessScore >= 33 ? "medium" : "low"
    };
  }
  
  async checkCalculationAccuracy(results) {
    // 验证财务计算的准确性
    const elements = results.capitalElements;
    const issues = [];
    
    // 验证关键比率的合理性
    if (elements.capitalStructure) {
      const { debtToEquity, debtRatio, equityRatio } = elements.capitalStructure;
      if (debtRatio + equityRatio !== 1) {
        issues.push("负债率与权益率之和应为1");
      }
    }
    
    return {
      issues: issues,
      accuracyLevel: issues.length === 0 ? "high" : "medium",
      accuracyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 20))
    };
  }
  
  async checkConsistency(results) {
    // 检查分析结果的内在一致性
    const elements = results.capitalElements;
    const issues = [];
    
    // 检查资本结构与风险状况的一致性
    if (elements.capitalStructure && elements.riskProfile) {
      const debtLevel = elements.capitalStructure.debtToEquity;
      const riskLevel = elements.riskProfile.riskType?.financialRisk;
      
      if (debtLevel > 1.0 && riskLevel === "低") {
        issues.push("高负债水平与低财务风险评估不一致");
      }
    }
    
    return {
      issues: issues,
      consistencyLevel: issues.length === 0 ? "high" : "medium",
      consistencyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 25))
    };
  }
  
  async checkIndustryAlignment(results) {
    // 检查与行业基准的对齐度
    const data = results.financialData;
    const elements = results.capitalElements;
    const alignmentIssues = [];
    
    if (data.industryData && elements.capitalStructure) {
      const industryDebt = data.industryData.industryAverage?.debtToEquity;
      const companyDebt = elements.capitalStructure.debtToEquity;
      
      if (industryDebt && companyDebt) {
        const deviation = Math.abs(companyDebt - industryDebt) / industryDebt;
        if (deviation > 0.5) { // 偏差超过50%
          alignmentIssues.push(`资产负债率偏离行业平均超过50%`);
        }
      }
    }
    
    return {
      issues: alignmentIssues,
      alignmentLevel: alignmentIssues.length === 0 ? "high" : "medium",
      alignmentScore: alignmentIssues.length === 0 ? 100 : Math.max(0, 100 - (alignmentIssues.length * 15))
    };
  }
  
  calculateOverallScore(validationResults) {
    const { dataCompleteness, calculationAccuracy, consistency, industryAlignment } = validationResults;
    
    // 加权计算总体分数
    const weights = {
      completeness: 0.25,
      accuracy: 0.30,
      consistency: 0.25,
      alignment: 0.20
    };
    
    return Math.round(
      (dataCompleteness.completenessScore * weights.completeness) +
      (calculationAccuracy.accuracyScore * weights.accuracy) +
      (consistency.consistencyScore * weights.consistency) +
      (industryAlignment.alignmentScore * weights.alignment)
    );
  }
}

/**
 * 资本分析报告生成模块
 * 支持渐进式披露：根据需求生成不同详细程度的报告
 */
class CapitalReportingModule {
  async generate(analysisResults, detailed = false, comparative = false) {
    const report = {
      summary: this.createExecutiveSummary(analysisResults),
      keyMetrics: this.extractKeyMetrics(analysisResults),
      ratings: await this.generateRatings(analysisResults),
      metadata: {
        generationTime: new Date().toISOString(),
        validationScore: analysisResults.overallValidationScore,
        detailLevel: detailed ? "detailed" : "summary"
      }
    };
    
    // 根据需求添加详细内容
    if (detailed) {
      report.capitalElements = analysisResults.capitalElements;
      report.fullAnalysis = await this.createDetailedAnalysis(analysisResults);
    }
    
    if (comparative) {
      report.comparativeAnalysis = await this.createComparativeAnalysis(analysisResults);
    }
    
    return report;
  }
  
  createExecutiveSummary(results) {
    const elements = results.capitalElements;
    
    return {
      title: `对${results.financialData.companyProfile.name}的资本分析摘要`,
      executiveSummary: `该企业资本结构相对稳健，债务水平适中，融资策略较为均衡。总体财务健康度得分为${results.overallValidationScore}分。`,
      keyHighlights: [
        `资本结构：负债权益比为${elements.capitalStructure?.debtToEquity?.toFixed(2) || 'N/A'}`,
        `盈利能力：投资回报率表现${elements.investmentStrategy?.efficiencyMetrics?.roi ? '良好' : '待评估'}`,
        `现金流：经营现金流为${elements.cashFlowAnalysis?.operatingCash || 'N/A'}`
      ],
      overallRating: this.rateCapitalHealth(results.overallValidationScore)
    };
  }
  
  rateCapitalHealth(score) {
    if (score >= 85) return "优秀 - 资本结构健康，融资策略有效";
    if (score >= 70) return "良好 - 资本结构较为健康";
    if (score >= 50) return "一般 - 部分财务指标需要关注";
    return "需改进 - 资本结构存在明显风险";
  }
  
  extractKeyMetrics(results) {
    const elements = results.capitalElements;
    
    return {
      debtToEquity: elements.capitalStructure?.debtToEquity,
      roe: elements.investmentStrategy?.efficiencyMetrics?.roi || elements.roe || 0.08,
      currentRatio: elements.liquidityMetrics?.currentRatio || 3.0, // 假设值
      interestCoverage: elements.riskProfile?.riskMetrics?.interestCoverage,
      operatingCashFlow: elements.cashFlowAnalysis?.operatingCash
    };
  }
  
  async generateRatings(results) {
    return {
      capitalStructureRating: this.rateElement(results.capitalElements.capitalStructure, 'capitalStructure'),
      financingStrategyRating: this.rateElement(results.capitalElements.financingPattern, 'financing'),
      investmentEfficiencyRating: this.rateElement(results.capitalElements.investmentStrategy, 'investment'),
      riskManagementRating: this.rateElement(results.capitalElements.riskProfile, 'risk'),
      overallRating: results.overallValidationScore
    };
  }
  
  rateElement(element, elementType) {
    // 根据不同类型元素进行评级
    switch(elementType) {
      case 'capitalStructure':
        const debtLevel = element.debtToEquity;
        if (debtLevel < 0.3) return "保守";
        if (debtLevel < 0.7) return "适度";
        return "积极";
      case 'financing':
        return "均衡";
      case 'investment':
        return "有效";
      case 'risk':
        return "可控";
      default:
        return "待评估";
    }
  }
  
  async createDetailedAnalysis(results) {
    return {
      comprehensiveCapitalStructure: results.capitalElements.capitalStructure,
      financingStrategyDetails: results.capitalElements.financingPattern,
      investmentPortfolio: results.capitalElements.investmentStrategy,
      riskProfileDetailed: results.capitalElements.riskProfile,
      valuationAnalysis: results.capitalElements.valuationMetrics,
      cashFlowDeepDive: results.capitalElements.cashFlowAnalysis
    };
  }
  
  async createComparativeAnalysis(results) {
    const industryData = results.financialData.industryData;
    if (!industryData || !industryData.industryAverage) {
      return { message: "缺少行业基准数据进行比较" };
    }
    
    const companyData = results.capitalElements;
    const industryAvg = industryData.industryAverage;
    
    return {
      capitalStructureComparison: {
        company: companyData.capitalStructure?.debtToEquity,
        industry: industryAvg.debtToEquity,
        comparison: companyData.capitalStructure?.debtToEquity > industryAvg.debtToEquity ? "高于行业平均" : "低于行业平均"
      },
      profitabilityComparison: {
        companyROE: companyData.investmentStrategy?.efficiencyMetrics?.roic || 0,
        industryROE: industryAvg.roe,
        comparison: "待计算"
      },
      competitivePosition: industryData.competitivePosition
    };
  }
}

// 导出技能类
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CapitalAnalysisSkill;
}