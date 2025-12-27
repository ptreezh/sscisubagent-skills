/**
 * 竞争分析技能实现
 * 遵循agentskills.io规范和渐进式披露原则
 * 定量分析程序化，定性分析AI化
 */

class CompetitiveAnalysisSkill {
  constructor() {
    this.skillId = "competitive-analysis";
    this.version = "2.0.0";
    this.name = "竞争分析";
    this.description = "基于竞争战略理论，对企业竞争环境、竞争对手、竞争优势和竞争策略进行全面分析";
    
    // 初始化模块
    this.dataCollector = new CompetitiveDataCollectionModule();
    this.analyzer = new CompetitiveAnalysisModule();
    this.validator = new CompetitiveValidationModule();
    this.reporter = new CompetitiveReportingModule();
  }

  /**
   * 执行技能主方法
   * 实现渐进式披露：根据focusAreas参数决定分析详略程度
   */
  async execute(inputs) {
    try {
      // 验证输入参数
      this.validateInputs(inputs);
      
      // 收集竞争数据
      const competitiveData = await this.dataCollector.collect(inputs.companyData);
      
      // 执行分析（可选择关注领域以控制上下文）
      const analysisResults = await this.analyzer.analyze(
        competitiveData, 
        inputs.focusAreas || null,  // 支持指定关注领域
        inputs.detailedAnalysis || false  // 支持详细/摘要分析
      );
      
      // 验证结果
      const validatedResults = await this.validator.validate(analysisResults);
      
      // 生成报告（支持不同详细程度）
      const finalReport = await this.reporter.generate(
        validatedResults, 
        inputs.detailedReport || false,
        inputs.analysisDepth || 'standard'
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
 * 竞争数据收集模块
 * 程序化执行竞争数据收集
 */
class CompetitiveDataCollectionModule {
  async collect(companyData) {
    // 并行收集竞争相关信息
    const [marketData, competitorData, industryData, strategicData] = await Promise.allSettled([
      this.getMarketData(companyData),
      this.getCompetitorData(companyData),
      this.getIndustryData(companyData),
      this.getStrategicData(companyData)
    ]);
    
    return {
      companyProfile: companyData,
      marketData: marketData.status === 'fulfilled' ? marketData.value : null,
      competitorData: competitorData.status === 'fulfilled' ? competitorData.value : null,
      industryData: industryData.status === 'fulfilled' ? industryData.value : null,
      strategicData: strategicData.status === 'fulfilled' ? strategicData.value : null
    };
  }
  
  async getMarketData(companyData) {
    // 模拟从市场研究获取数据
    return {
      marketSize: 15000000000, // 市场规模150亿美元
      growthRate: 0.085, // 增长率8.5%
      marketShare: 0.18, // 公司市场份额18%
      marketConcentration: 0.65, // 市场集中度65%
      competitiveIntensity: 0.72 // 竞争强度0-1，1为最高
    };
  }
  
  async getCompetitorData(companyData) {
    // 模拟从竞争情报获取数据
    return {
      keyCompetitors: [
        {
          name: "主要竞争对手A",
          marketShare: 0.25,
          revenue: 3750000000,
          strategy: "差异化",
          strengths: ["品牌知名度", "技术创新"],
          weaknesses: ["成本结构较高"]
        },
        {
          name: "主要竞争对手B",
          marketShare: 0.22,
          revenue: 3300000000,
          strategy: "成本领先",
          strengths: ["成本控制", "规模效应"],
          weaknesses: ["产品创新不足"]
        },
        {
          name: "主要竞争对手C",
          marketShare: 0.15,
          revenue: 2250000000,
          strategy: "聚焦",
          strengths: ["细分市场专业性"],
          weaknesses: ["规模较小"]
        }
      ],
      competitiveDynamics: {
        priceCompetition: 0.6,
        innovationCompetition: 0.8,
        marketingCompetition: 0.7
      }
    };
  }
  
  async getIndustryData(companyData) {
    // 模拟从行业分析获取数据
    return {
      industryLifeCycle: "成熟期",
      regulatoryEnvironment: "中等监管",
      technologyDisruptionLevel: 0.75, // 0-1，1为最高
      barriersToEntry: 0.6, // 0-1，1为最高
      supplierPower: 0.4, // 0-1，1为最高
      buyerPower: 0.65, // 0-1，1为最高
      substituteThreat: 0.35 // 0-1，1为最高
    };
  }
  
  async getStrategicData(companyData) {
    // 模拟从战略分析获取数据
    return {
      valueProposition: "高性价比解决方案",
      competitiveStrategy: "混合型（成本领先+差异化）",
      coreCompetencies: ["技术整合能力", "客户关系管理"],
      competitiveAdvantages: ["专利技术", "供应链效率", "品牌声誉"],
      pricingPosition: "中高端"
    };
  }
}

/**
 * 竞争分析模块
 * 定量计算程序化，定性分析AI化
 */
class CompetitiveAnalysisModule {
  async analyze(data, focusAreas = null, detailed = false) {
    // 根据focusAreas决定分析详略程度，实现渐进式披露
    const analysis = {};
    
    // 市场竞争分析（定量+定性）
    if (!focusAreas || focusAreas.includes('marketCompetitiveness')) {
      analysis.marketCompetitiveness = await this.analyzeMarketCompetitiveness(data, detailed);
    }
    
    // 竞争对手分析（定量+定性）
    if (!focusAreas || focusAreas.includes('competitorAnalysis')) {
      analysis.competitorAnalysis = await this.analyzeCompetitorAnalysis(data, detailed);
    }
    
    // 竞争定位分析（定量+定性）
    if (!focusAreas || focusAreas.includes('competitivePositioning')) {
      analysis.competitivePositioning = await this.analyzeCompetitivePositioning(data, detailed);
    }
    
    // 五力模型分析（定量+定性）
    if (!focusAreas || focusAreas.includes('fiveForcesAnalysis')) {
      analysis.fiveForcesAnalysis = await this.analyzeFiveForcesAnalysis(data, detailed);
    }
    
    // 竞争优势分析（定量+定性）
    if (!focusAreas || focusAreas.includes('competitiveAdvantage')) {
      analysis.competitiveAdvantage = await this.analyzeCompetitiveAdvantage(data, detailed);
    }
    
    // 市场份额分析（定量，程序化）
    if (!focusAreas || focusAreas.includes('marketShare')) {
      analysis.marketShare = await this.analyzeMarketShare(data, detailed);
    }
    
    // 定价策略分析（定量+定性）
    if (!focusAreas || focusAreas.includes('pricingStrategy')) {
      analysis.pricingStrategy = await this.analyzePricingStrategy(data, detailed);
    }
    
    // 差异化策略分析（定量+定性）
    if (!focusAreas || focusAreas.includes('differentiationStrategy')) {
      analysis.differentiationStrategy = await this.analyzeDifferentiationStrategy(data, detailed);
    }
    
    return {
      competitiveElements: analysis,
      competitiveData: data,
      analysisTimestamp: new Date().toISOString()
    };
  }
  
  async analyzeMarketCompetitiveness(data, detailed = false) {
    // 分析市场竞争情况
    const marketData = data.marketData;
    if (!marketData) {
      return {
        intensity: "数据不足",
        assessment: "需要完整市场竞争数据"
      };
    }
    
    const intensity = this.assessCompetitiveIntensity(marketData.competitiveIntensity);
    const concentration = marketData.marketConcentration;
    const growthRate = marketData.growthRate;
    
    const result = {
      intensity: intensity,
      marketConcentration: concentration,
      growthRate: growthRate,
      competitivePressure: this.calculateCompetitivePressure(marketData),
      assessment: `处于${intensity}竞争环境，市场集中度${concentration > 0.6 ? '较高' : '较低'}`
    };
    
    if (detailed) {
      result.detailedAnalysis = {
        marketSize: marketData.marketSize,
        concentrationRatio: concentration,
        competitiveDynamics: "高创新竞争，中等价格竞争",
        entryBarriers: "中等进入壁垒",
        exitBarriers: "中等退出壁垒"
      };
    }
    
    return result;
  }
  
  assessCompetitiveIntensity(score) {
    if (score >= 0.8) return "极高";
    if (score >= 0.6) return "激烈";
    if (score >= 0.4) return "中等";
    return "温和";
  }
  
  calculateCompetitivePressure(marketData) {
    // 综合计算竞争压力（0-1）
    const concentrationPressure = marketData.marketConcentration * 0.4;
    const growthPressure = (1 - marketData.growthRate) * 0.3;
    const intensityPressure = marketData.competitiveIntensity * 0.3;
    
    return Math.min(1, concentrationPressure + growthPressure + intensityPressure);
  }
  
  async analyzeCompetitorAnalysis(data, detailed = false) {
    // 分析主要竞争对手
    const competitorData = data.competitorData;
    
    if (!competitorData || !competitorData.keyCompetitors) {
      return {
        keyCompetitors: [],
        competitiveLandscape: "数据不足",
        assessment: "需要竞争对手详细信息"
      };
    }
    
    const competitors = competitorData.keyCompetitors;
    
    const result = {
      keyCompetitors: competitors,
      competitiveLandscape: this.describeCompetitiveLandscape(competitors),
      competitiveDynamics: competitorData.competitiveDynamics,
      top3Share: competitors.slice(0, 3).reduce((sum, comp) => sum + comp.marketShare, 0)
    };
    
    if (detailed) {
      result.detailedCompetitorAnalysis = {
        competitorProfiles: competitors.map(competitor => ({
          ...competitor,
          competitivePosition: this.assessCompetitorPosition(competitor),
          threatLevel: this.assessThreatLevel(competitor)
        })),
        competitiveIntensity: competitorData.competitiveDynamics,
        competitorRankings: this.rankCompetitors(competitors),
        strategicMoves: "近期主要竞争对手战略动向"
      };
    }
    
    return result;
  }
  
  describeCompetitiveLandscape(competitors) {
    const totalShare = competitors.reduce((sum, comp) => sum + comp.marketShare, 0);
    
    if (totalShare > 0.6) {
      return "高度集中的竞争格局";
    } else if (totalShare > 0.4) {
      return "中等集中的竞争格局";
    } else {
      return "分散的竞争格局";
    }
  }
  
  assessCompetitorPosition(competitor) {
    if (competitor.marketShare > 0.25) return "市场领导者";
    if (competitor.marketShare > 0.15) return "市场挑战者";
    if (competitor.marketShare > 0.05) return "市场追随者";
    return "市场补缺者";
  }
  
  assessThreatLevel(competitor) {
    const strategy = competitor.strategy.toLowerCase();
    const marketShare = competitor.marketShare;
    
    if (marketShare > 0.2 && strategy === "growth") return "高威胁";
    if (marketShare > 0.1 || strategy.includes("aggressive")) return "中等威胁";
    return "低威胁";
  }
  
  rankCompetitors(competitors) {
    return [...competitors]
      .sort((a, b) => b.marketShare - a.marketShare)
      .map((comp, index) => ({ ...comp, rank: index + 1 }));
  }
  
  async analyzeCompetitivePositioning(data, detailed = false) {
    // 分析竞争定位
    const strategicData = data.strategicData;
    const marketData = data.marketData;
    
    const result = {
      valueProposition: strategicData?.valueProposition || "待评估",
      competitiveStrategy: strategicData?.competitiveStrategy || "待评估",
      positioningType: this.identifyPositioningType(strategicData),
      competitivePosition: this.assessCompetitivePosition(strategicData, marketData),
      differentiators: strategicData?.competitiveAdvantages || []
    };
    
    if (detailed) {
      result.detailedPositioning = {
        valueProposition: result.valueProposition,
        strategyType: result.competitiveStrategy,
        positioningMap: "基于价格和差异化的产品定位图",
        competitiveBenchmark: "与主要竞争对手的对比",
        positioningEffectiveness: this.assessPositioningEffectiveness(strategicData, marketData)
      };
    }
    
    return result;
  }
  
  identifyPositioningType(strategicData) {
    if (!strategicData) return "待评估";
    
    const strategy = strategicData.competitiveStrategy?.toLowerCase() || "";
    
    if (strategy.includes("cost")) return "成本定位";
    if (strategy.includes("differentiation")) return "差异化定位";
    if (strategy.includes("focus") || strategy.includes("niche")) return "聚焦定位";
    return "混合定位";
  }
  
  assessCompetitivePosition(strategicData, marketData) {
    if (!marketData) return "待评估";
    
    const marketShare = marketData.marketShare;
    
    if (marketShare > 0.25) return "市场领导者";
    if (marketShare > 0.15) return "市场挑战者";
    if (marketShare > 0.05) return "市场追随者";
    return "市场补缺者";
  }
  
  assessPositioningEffectiveness(strategicData, marketData) {
    if (!strategicData || !marketData) return "待评估";
    
    const marketShare = marketData.marketShare;
    const strategy = strategicData.competitiveStrategy;
    
    // 基于市场地位和策略匹配度评估
    if (marketShare > 0.2 && strategy.includes("differentiation")) return "优秀";
    if (marketShare > 0.1 && strategy.includes("cost")) return "良好";
    return "一般";
  }
  
  async analyzeFiveForcesAnalysis(data, detailed = false) {
    // 分析波特五力模型
    const industryData = data.industryData;
    
    if (!industryData) {
      return {
        rivalryIntensity: "数据不足",
        threatNewEntrants: "数据不足",
        supplierPower: "数据不足",
        buyerPower: "数据不足",
        substituteThreat: "数据不足"
      };
    }
    
    const result = {
      rivalryIntensity: industryData.competitiveIntensity || 0.7, // 假设较高竞争强度
      threatNewEntrants: industryData.barriersToEntry ? 1 - industryData.barriersToEntry : 0.5,
      supplierPower: industryData.supplierPower,
      buyerPower: industryData.buyerPower,
      substituteThreat: industryData.substituteThreat,
      overallAttractiveness: this.calculateIndustryAttractiveness(industryData)
    };
    
    if (detailed) {
      result.detailedFiveForces = {
        rivalryAnalysis: this.analyzeRivalry(industryData),
        newEntrantsAnalysis: this.analyzeNewEntrants(industryData),
        supplierAnalysis: this.analyzeSuppliers(industryData),
        buyerAnalysis: this.analyzeBuyers(industryData),
        substitutesAnalysis: this.analyzeSubstitutes(industryData)
      };
    }
    
    return result;
  }
  
  calculateIndustryAttractiveness(industryData) {
    // 行业吸引力计算（越低越有吸引力）
    const rivalry = industryData.competitiveIntensity || 0.7;
    const newEntrants = industryData.barriersToEntry ? 1 - industryData.barriersToEntry : 0.5;
    const supplierPower = industryData.supplierPower || 0.5;
    const buyerPower = industryData.buyerPower || 0.5;
    const substitutes = industryData.substituteThreat || 0.5;
    
    return (rivalry + newEntrants + supplierPower + buyerPower + substitutes) / 5;
  }
  
  analyzeRivalry(industryData) {
    return {
      intensity: this.scaleToDescriptor(industryData.competitiveIntensity || 0.7),
      drivers: ["市场增长率", "固定成本比例", "产品差异化"],
      implications: "高竞争强度可能压缩利润空间"
    };
  }
  
  analyzeNewEntrants(industryData) {
    const barriers = industryData.barriersToEntry ? 1 - industryData.barriersToEntry : 0.5;
    return {
      threatLevel: this.scaleToDescriptor(barriers),
      keyBarriers: ["资本要求", "品牌忠诚度", "政府政策"],
      implications: barriers > 0.6 ? "进入威胁较低" : "进入威胁较高"
    };
  }
  
  analyzeSuppliers(industryData) {
    return {
      powerLevel: this.scaleToDescriptor(industryData.supplierPower || 0.5),
      sourcesOfPower: ["供应集中度", "转换成本", "供应商前向整合"],
      implications: "供应商议价能力影响成本结构"
    };
  }
  
  analyzeBuyers(industryData) {
    return {
      powerLevel: this.scaleToDescriptor(industryData.buyerPower || 0.65),
      sourcesOfPower: ["购买集中度", "产品标准化", "转换成本"],
      implications: "买方议价能力影响定价权"
    };
  }
  
  analyzeSubstitutes(industryData) {
    return {
      threatLevel: this.scaleToDescriptor(industryData.substituteThreat || 0.35),
      substituteTypes: ["直接替代品", "间接替代品"],
      implications: "替代品威胁影响定价和市场份额"
    };
  }
  
  scaleToDescriptor(score) {
    if (score >= 0.8) return "极高";
    if (score >= 0.6) return "高";
    if (score >= 0.4) return "中等";
    if (score >= 0.2) return "低";
    return "极低";
  }
  
  async analyzeCompetitiveAdvantage(data, detailed = false) {
    // 分析竞争优势
    const strategicData = data.strategicData;
    const marketData = data.marketData;
    
    const result = {
      sources: strategicData?.competitiveAdvantages || [],
      sustainability: this.assessSustainability(strategicData),
      valueChain: this.analyzeValueChain(strategicData),
      competitiveEdge: this.calculateCompetitiveEdge(strategicData, marketData),
      durability: this.assessDurability(strategicData)
    };
    
    if (detailed) {
      result.detailedAdvantage = {
        coreCompetencies: strategicData?.coreCompetencies,
        competitiveAssets: this.identifyCompetitiveAssets(strategicData),
        advantageSources: result.sources,
        sustainabilityFactors: ["资源稀缺性", "能力复杂性", "价值独特性"],
        imitationDifficulty: this.assessImitationDifficulty(strategicData)
      };
    }
    
    return result;
  }
  
  assessSustainability(strategicData) {
    if (!strategicData || !strategicData.competitiveAdvantages) return "待评估";
    
    const advantages = strategicData.competitiveAdvantages;
    if (advantages.some(adv => adv.toLowerCase().includes("patent") || adv.toLowerCase().includes("brand"))) {
      return "高";
    } else if (advantages.some(adv => adv.toLowerCase().includes("process") || adv.toLowerCase().includes("system"))) {
      return "中等";
    }
    return "低";
  }
  
  analyzeValueChain(strategicData) {
    if (!strategicData || !strategicData.coreCompetencies) return "待评估";
    
    const competencies = strategicData.coreCompetencies;
    return {
      primaryActivities: competencies.filter(comp => 
        comp.toLowerCase().includes("delivery") || 
        comp.toLowerCase().includes("service") ||
        comp.toLowerCase().includes("sales")
      ).length > 0 ? "优势明显" : "待加强",
      supportActivities: competencies.filter(comp => 
        comp.toLowerCase().includes("technology") || 
        comp.toLowerCase().includes("procurement") ||
        comp.toLowerCase().includes("hr")
      ).length > 0 ? "优势明显" : "待加强"
    };
  }
  
  calculateCompetitiveEdge(marketData) {
    if (!marketData) return 0.5;
    
    // 基于市场份额和竞争强度计算竞争优势
    const marketShare = marketData.marketShare || 0.18;
    const competitiveIntensity = marketData.competitiveIntensity || 0.7;
    
    return marketShare * (1 - competitiveIntensity/2);
  }
  
  assessDurability(strategicData) {
    const advantages = strategicData?.competitiveAdvantages || [];
    let durabilityScore = 0;
    
    for (const advantage of advantages) {
      const lowerAdv = advantage.toLowerCase();
      if (lowerAdv.includes("patent") || lowerAdv.includes("brand") || lowerAdv.includes("reputation")) {
        durabilityScore += 2; // 高耐久性
      } else if (lowerAdv.includes("process") || lowerAdv.includes("system")) {
        durabilityScore += 1; // 中等耐久性
      }
    }
    
    if (durabilityScore >= 4) return "高";
    if (durabilityScore >= 2) return "中等";
    return "低";
  }
  
  identifyCompetitiveAssets(strategicData) {
    if (!strategicData) return [];
    
    const assets = [];
    if (strategicData.competitiveAdvantages) {
      assets.push(...strategicData.competitiveAdvantages);
    }
    if (strategicData.coreCompetencies) {
      assets.push(...strategicData.coreCompetencies);
    }
    
    return [...new Set(assets)]; // 去重
  }
  
  assessImitationDifficulty(strategicData) {
    const advantages = strategicData?.competitiveAdvantages || [];
    let difficultyScore = 0;
    
    for (const advantage of advantages) {
      const lowerAdv = advantage.toLowerCase();
      if (lowerAdv.includes("patent") || lowerAdv.includes("proprietary")) {
        difficultyScore += 3; // 很难模仿
      } else if (lowerAdv.includes("brand") || lowerAdv.includes("culture") || lowerAdv.includes("relationships")) {
        difficultyScore += 2; // 较难模仿
      } else if (lowerAdv.includes("process") || lowerAdv.includes("system")) {
        difficultyScore += 1; // 一般难度
      }
    }
    
    if (difficultyScore >= 6) return "很高";
    if (difficultyScore >= 4) return "较高";
    if (difficultyScore >= 2) return "一般";
    return "较低";
  }
  
  async analyzeMarketShare(data, detailed = false) {
    // 分析市场份额
    const marketData = data.marketData;
    const competitorData = data.competitorData;
    
    const result = {
      currentShare: marketData?.marketShare || 0,
      relativeShare: this.calculateRelativeShare(marketData, competitorData),
      trend: this.assessShareTrend(marketData),
      competitivePosition: this.assessMarketPosition(marketData?.marketShare)
    };
    
    if (detailed) {
      result.detailedShareAnalysis = {
        currentMarketShare: result.currentShare,
        relativeShare: result.relativeShare,
        historicalTrend: "待历史数据",
        marketPosition: result.competitivePosition,
        shareGrowthPotential: this.assessShareGrowthPotential(marketData, competitorData)
      };
    }
    
    return result;
  }
  
  calculateRelativeShare(marketData, competitorData) {
    if (!marketData || !competitorData || !competitorData.keyCompetitors) return 0;
    
    // 相对市场份额 = 本公司份额 / 主要竞争对手份额
    const ourShare = marketData.marketShare || 0;
    const largestCompetitorShare = Math.max(...competitorData.keyCompetitors.map(c => c.marketShare));
    
    return largestCompetitorShare > 0 ? ourShare / largestCompetitorShare : 0;
  }
  
  assessShareTrend(marketData) {
    if (!marketData) return "待评估";
    
    // 基于当前市场份额和市场增长率评估趋势
    const share = marketData.marketShare;
    const growth = marketData.growthRate;
    
    if (share > 0.2 && growth > 0.08) return "强劲增长";
    if (share > 0.15 && growth > 0.05) return "稳定增长";
    if (share < 0.1 && growth < 0.03) return "缓慢增长";
    return "稳定";
  }
  
  assessMarketPosition(marketShare) {
    if (marketShare === undefined) return "待评估";
    
    if (marketShare > 0.3) return "市场领导者";
    if (marketShare > 0.2) return "市场领导者";
    if (marketShare > 0.15) return "市场挑战者";
    if (marketShare > 0.1) return "市场挑战者";
    if (marketShare > 0.05) return "市场追随者";
    return "市场补缺者";
  }
  
  assessShareGrowthPotential(marketData, competitorData) {
    if (!marketData || !competitorData) return 0.05; // 假设5%增长潜力
    
    const currentShare = marketData.marketShare || 0;
    const growthRate = marketData.growthRate || 0.08;
    const competitivePressure = marketData.competitiveIntensity || 0.7;
    
    // 基于当前份额、市场增长率和竞争压力评估增长潜力
    if (currentShare < 0.15 && growthRate > 0.07 && competitivePressure < 0.7) {
      return 0.15; // 高增长潜力
    } else if (currentShare < 0.25 && growthRate > 0.05) {
      return 0.10; // 中等增长潜力
    } else {
      return 0.05; // 低增长潜力
    }
  }
  
  async analyzePricingStrategy(data, detailed = false) {
    // 分析定价策略
    const strategicData = data.strategicData;
    const marketData = data.marketData;
    const competitorData = data.competitorData;
    
    const result = {
      approach: strategicData?.pricingPosition || "待评估",
      competitiveness: this.assessPricingCompetitiveness(strategicData, competitorData),
      flexibility: this.assessPricingFlexibility(marketData),
      effectiveness: this.assessPricingEffectiveness(strategicData, marketData)
    };
    
    if (detailed) {
      result.detailedPricing = {
        pricingApproach: result.approach,
        competitivePositioning: result.competitiveness,
        pricingPower: "待具体数据",
        priceSensitivity: "待市场研究数据",
        pricingOptimizationOpportunities: ["差异化定价", "动态定价"]
      };
    }
    
    return result;
  }
  
  assessPricingCompetitiveness(strategicData, competitorData) {
    if (!strategicData || !competitorData || !competitorData.keyCompetitors) {
      return "待评估";
    }
    
    const ourPosition = strategicData.pricingPosition?.toLowerCase() || "";
    const avgCompetitorPrice = competitorData.keyCompetitors.reduce((sum, comp) => sum + comp.revenue * comp.marketShare, 0) / 
                               competitorData.keyCompetitors.reduce((sum, comp) => sum + comp.marketShare, 0);
    
    if (ourPosition.includes("high") || ourPosition.includes("premium")) return "溢价定位";
    if (ourPosition.includes("low") || ourPosition.includes("cost")) return "成本定位";
    return "竞争性定价";
  }
  
  assessPricingFlexibility(marketData) {
    if (!marketData) return "待评估";
    
    const competitiveIntensity = marketData.competitiveIntensity || 0.7;
    
    if (competitiveIntensity > 0.8) return "低";
    if (competitiveIntensity > 0.6) return "中等";
    return "高";
  }
  
  assessPricingEffectiveness(strategicData, marketData) {
    if (!strategicData || !marketData) return "待评估";
    
    const marketShare = marketData.marketShare || 0;
    const pricingPosition = strategicData.pricingPosition || "";
    
    // 基于市场份额和定价策略评估有效性
    if (marketShare > 0.2 && pricingPosition.includes("premium")) return "高";
    if (marketShare > 0.15 && pricingPosition.includes("value")) return "高";
    if (marketShare < 0.1) return "待改进";
    return "中等";
  }
  
  async analyzeDifferentiationStrategy(data, detailed = false) {
    // 分析差异化策略
    const strategicData = data.strategicData;
    
    const result = {
      dimensions: strategicData?.competitiveAdvantages || [],
      effectiveness: this.assessDifferentiationEffectiveness(strategicData),
      uniqueness: this.assessUniqueness(strategicData),
      perceivedValue: this.assessPerceivedValue(strategicData)
    };
    
    if (detailed) {
      result.detailedDifferentiation = {
        differentiationDimensions: result.dimensions,
        customerPerception: "待市场调研数据",
        competitorDifferentiation: "待竞争分析数据",
        differentiationSustainability: result.effectiveness,
        valueCreation: "通过差异化创造的额外价值"
      };
    }
    
    return result;
  }
  
  assessDifferentiationEffectiveness(strategicData) {
    if (!strategicData || !strategicData.competitiveAdvantages) return "待评估";
    
    const advantages = strategicData.competitiveAdvantages;
    const differentiationWords = ["innovation", "quality", "service", "technology", "design", "brand"];
    
    const diffCount = advantages.filter(adv => 
      differentiationWords.some(word => adv.toLowerCase().includes(word))
    ).length;
    
    if (diffCount >= 3) return "高";
    if (diffCount >= 2) return "中等";
    return "低";
  }
  
  assessUniqueness(strategicData) {
    if (!strategicData || !strategicData.competitiveAdvantages) return "待评估";
    
    const advantages = strategicData.competitiveAdvantages;
    // 假设包含"proprietary"、"patent"、"exclusive"等词汇表示独特性
    const uniqueCount = advantages.filter(adv => 
      adv.toLowerCase().includes("proprietary") || 
      adv.toLowerCase().includes("patent") || 
      adv.toLowerCase().includes("exclusive") ||
      adv.toLowerCase().includes("unique")
    ).length;
    
    if (uniqueCount >= 2) return "高度独特";
    if (uniqueCount >= 1) return "中等独特";
    return "一般";
  }
  
  assessPerceivedValue(strategicData) {
    if (!strategicData) return "待评估";
    
    // 基于价值主张和竞争优势评估客户感知价值
    const valueProp = strategicData.valueProposition?.toLowerCase() || "";
    const advantages = strategicData.competitiveAdvantages || [];
    
    if (valueProp.includes("high value") || valueProp.includes("premium")) {
      return "高感知价值";
    } else if (advantages.length > 3) {
      return "中等感知价值";
    }
    return "待提升";
  }
}

/**
 * 竞争验证模块
 */
class CompetitiveValidationModule {
  async validate(analysisResults) {
    const validationResults = {
      dataCompleteness: await this.checkDataCompleteness(analysisResults),
      calculationAccuracy: await this.checkCalculationAccuracy(analysisResults),
      consistency: await this.checkConsistency(analysisResults),
      strategicAlignment: await this.checkStrategicAlignment(analysisResults)
    };
    
    const overallScore = this.calculateOverallScore(validationResults);
    
    return {
      ...analysisResults,
      validation: validationResults,
      overallValidationScore: overallScore
    };
  }
  
  async checkDataCompleteness(results) {
    const sourceData = results.competitiveData;
    const completenessFactors = {
      marketData: !!sourceData.marketData,
      competitorData: !!sourceData.competitorData,
      industryData: !!sourceData.industryData,
      strategicData: !!sourceData.strategicData
    };
    
    const factorCount = Object.values(completenessFactors).filter(Boolean).length;
    const completenessScore = (factorCount / 4) * 100;
    
    return {
      factors: completenessFactors,
      completenessScore: completenessScore,
      level: completenessScore >= 75 ? "high" : completenessScore >= 50 ? "medium" : "low"
    };
  }
  
  async checkCalculationAccuracy(results) {
    // 验证竞争计算的准确性
    const elements = results.competitiveElements;
    const issues = [];
    
    // 验证市场份额总和的合理性
    if (elements.competitorAnalysis && elements.competitiveElements) {
      const competitors = elements.competitorAnalysis.keyCompetitors || [];
      const totalCompetitorShare = competitors.reduce((sum, comp) => sum + comp.marketShare, 0);
      const companyShare = elements.marketShare?.currentShare || 0;
      
      // 确保市场份额总和合理（允许一定误差）
      if (totalCompetitorShare + companyShare > 1.5) {
        issues.push("竞争对手市场份额总和异常");
      }
    }
    
    // 验证五力模型分数的合理性
    if (elements.fiveForcesAnalysis) {
      const forces = elements.fiveForcesAnalysis;
      for (const [key, value] of Object.entries(forces)) {
        if (typeof value === 'number' && (value < 0 || value > 1)) {
          issues.push(`${key} 数值应在0-1之间`);
        }
      }
    }
    
    return {
      issues: issues,
      accuracyLevel: issues.length === 0 ? "high" : "medium",
      accuracyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 15))
    };
  }
  
  async checkConsistency(results) {
    // 检查分析结果的内在一致性
    const elements = results.competitiveElements;
    const issues = [];
    
    // 检查竞争定位与市场份额的一致性
    if (elements.competitivePositioning && elements.marketShare) {
      const position = elements.competitivePositioning.competitivePosition;
      const marketShare = elements.marketShare.competitivePosition;
      
      if (position === "市场领导者" && marketShare !== "市场领导者") {
        issues.push("竞争定位与市场份额评估不一致");
      }
    }
    
    return {
      issues: issues,
      consistencyLevel: issues.length === 0 ? "high" : "medium",
      consistencyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 25))
    };
  }
  
  async checkStrategicAlignment(results) {
    // 检查战略一致性
    const elements = results.competitiveElements;
    const alignmentIssues = [];
    
    // 检查竞争策略与竞争优势的一致性
    if (elements.competitivePositioning && elements.competitiveAdvantage) {
      const strategy = elements.competitivePositioning.competitiveStrategy?.toLowerCase() || "";
      const advantages = elements.competitiveAdvantage.sources || [];
      
      if (strategy.includes("differentiation") && advantages.length === 0) {
        alignmentIssues.push("差异化策略与竞争优势不匹配");
      }
    }
    
    return {
      issues: alignmentIssues,
      alignmentLevel: alignmentIssues.length === 0 ? "high" : "medium",
      alignmentScore: alignmentIssues.length === 0 ? 100 : Math.max(0, 100 - (alignmentIssues.length * 20))
    };
  }
  
  calculateOverallScore(validationResults) {
    const { dataCompleteness, calculationAccuracy, consistency, strategicAlignment } = validationResults;
    
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
      (strategicAlignment.alignmentScore * weights.alignment)
    );
  }
}

/**
 * 竞争分析报告生成模块
 * 支持渐进式披露：根据需求生成不同详细程度的报告
 */
class CompetitiveReportingModule {
  async generate(analysisResults, detailed = false, depth = 'standard') {
    const report = {
      analysisSummary: this.createExecutiveSummary(analysisResults),
      keyMetrics: this.extractKeyMetrics(analysisResults),
      competitiveElements: detailed ? 
        analysisResults.competitiveElements : 
        this.createSummaryElements(analysisResults.competitiveElements),
      recommendations: await this.generateRecommendations(analysisResults),
      metadata: {
        generationTime: new Date().toISOString(),
        validationScore: analysisResults.overallValidationScore,
        detailLevel: detailed ? "detailed" : "summary"
      }
    };
    
    // 详细模式下添加额外内容
    if (detailed) {
      report.fullAnalysis = analysisResults.competitiveElements;
      report.validationDetails = analysisResults.validation;
    }
    
    return report;
  }
  
  createExecutiveSummary(results) {
    const elements = results.competitiveElements;
    
    return {
      executiveSummary: `对${results.competitiveData.companyProfile.name}的竞争分析显示，该企业在${this.getOverallCompetitiveAssessment(results)}，总体验证得分为${results.overallValidationScore}分。`,
      keyFindings: [
        `竞争定位: ${elements.competitivePositioning?.competitivePosition || 'N/A'}`,
        `市场份额: ${(elements.marketShare?.currentShare || 0) * 100}%`,
        `竞争优势: ${elements.competitiveAdvantage?.sustainability || 'N/A'}`
      ],
      overallAssessment: this.assessCompetitiveHealth(results.overallValidationScore)
    };
  }
  
  getOverallCompetitiveAssessment(results) {
    const elements = results.competitiveElements;
    const scores = [
      this.mapCompetitivePositionToScore(elements.competitivePositioning?.competitivePosition),
      elements.fiveForcesAnalysis?.overallAttractiveness ? 100 * (1 - elements.fiveForcesAnalysis.overallAttractiveness) : 60,
      this.mapSustainabilityToScore(elements.competitiveAdvantage?.sustainability),
      elements.marketShare?.currentShare ? elements.marketShare.currentShare * 100 : 60
    ];
    
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    
    if (avgScore >= 80) return "具有强有力的竞争地位";
    if (avgScore >= 65) return "具有良好的竞争地位";
    if (avgScore >= 50) return "竞争地位一般，需关注";
    return "竞争地位较弱，需重大改进";
  }
  
  mapCompetitivePositionToScore(position) {
    if (!position) return 60;
    if (position.includes("领导者")) return 90;
    if (position.includes("挑战者")) return 75;
    if (position.includes("追随者")) return 60;
    if (position.includes("补缺者")) return 50;
    return 60;
  }
  
  mapSustainabilityToScore(sustainability) {
    if (!sustainability) return 60;
    if (sustainability === "高") return 85;
    if (sustainability === "中等") return 70;
    if (sustainability === "低") return 50;
    return 60;
  }
  
  assessCompetitiveHealth(score) {
    if (score >= 85) return "优秀 - 竞争地位稳固，策略有效";
    if (score >= 70) return "良好 - 竞争地位较强";
    if (score >= 50) return "一般 - 部分竞争指标需要关注";
    return "需改进 - 竞争地位存在明显不足";
  }
  
  extractKeyMetrics(results) {
    const elements = results.competitiveElements;
    
    return {
      marketShare: elements.marketShare?.currentShare,
      competitivePosition: elements.competitivePositioning?.competitivePosition,
      competitiveAdvantage: elements.competitiveAdvantage?.sustainability,
      rivalryIntensity: elements.fiveForcesAnalysis?.rivalryIntensity,
      threatLevel: elements.fiveForcesAnalysis?.threatNewEntrants,
      differentiationEffectiveness: elements.differentiationStrategy?.effectiveness
    };
  }
  
  createSummaryElements(elements) {
    // 为摘要模式创建简化元素
    const summary = {};
    
    for (const [key, value] of Object.entries(elements)) {
      if (value && typeof value === 'object') {
        summary[key] = {
          status: this.createElementStatus(key, value),
          score: this.extractElementScore(key, value)
        };
      } else {
        summary[key] = value;
      }
    }
    
    return summary;
  }
  
  createElementStatus(elementKey, elementValue) {
    switch(elementKey) {
      case 'marketCompetitiveness':
        return `竞争${elementValue.intensity || 'N/A'}`;
      case 'competitiveAdvantage':
        return `优势${elementValue.sustainability || 'N/A'}`;
      case 'marketShare':
        return `份额${elementValue.competitivePosition || 'N/A'}`;
      case 'differentiationStrategy':
        return `差异化${elementValue.effectiveness || 'N/A'}`;
      default:
        return '已分析';
    }
  }
  
  extractElementScore(elementKey, elementValue) {
    switch(elementKey) {
      case 'competitiveAdvantage':
        return elementValue.sustainability === '高' ? 90 : 
               elementValue.sustainability === '中等' ? 75 : 50;
      case 'marketShare':
        return elementValue.currentShare ? elementValue.currentShare * 100 : 0;
      case 'pricingStrategy':
        return elementValue.effectiveness === '高' ? 90 : 
               elementValue.effectiveness === '中等' ? 75 : 50;
      default:
        return null;
    }
  }
  
  async generateRecommendations(results) {
    const recommendations = [];
    const elements = results.competitiveElements;
    const validation = results.validation;
    
    // 基于验证结果的建议
    if (validation.strategicAlignment.issues.length > 0) {
      recommendations.push(`解决战略一致性问题: ${validation.strategicAlignment.issues.join(', ')}`);
    }
    
    // 基于具体分析结果的建议
    if (elements.competitiveAdvantage?.sustainability === "低") {
      recommendations.push("加强核心竞争力构建，提升竞争优势可持续性");
    }
    
    if (elements.differentiationStrategy?.effectiveness === "低") {
      recommendations.push("强化差异化策略，提升产品和服务独特性");
    }
    
    if (elements.fiveForcesAnalysis?.rivalryIntensity > 0.8) {
      recommendations.push("制定应对高竞争强度的策略，如差异化或聚焦策略");
    }
    
    if (results.overallValidationScore < 70) {
      recommendations.push("加强竞争情报收集，提升分析准确性");
    }
    
    return recommendations.length > 0 ? recommendations : 
           ["企业竞争地位整体良好，继续保持现有竞争策略"];
  }
}

// 导出技能类
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CompetitiveAnalysisSkill;
}