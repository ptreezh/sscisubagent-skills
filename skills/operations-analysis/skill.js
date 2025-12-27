/**
 * 运营分析技能实现
 * 遵循agentskills.io规范和渐进式披露原则
 * 定量分析程序化，定性分析AI化
 */

class OperationsAnalysisSkill {
  constructor() {
    this.skillId = "operations-analysis";
    this.version = "2.0.0";
    this.name = "运营分析";
    this.description = "基于运营管理理论，对企业运营流程、效率、质量、供应链等进行系统分析";
    
    // 初始化模块
    this.dataCollector = new OperationsDataCollectionModule();
    this.analyzer = new OperationsAnalysisModule();
    this.validator = new OperationsValidationModule();
    this.reporter = new OperationsReportingModule();
  }

  /**
   * 执行技能主方法
   * 实现渐进式披露：根据focusAreas参数决定分析详略程度
   */
  async execute(inputs) {
    try {
      // 验证输入参数
      this.validateInputs(inputs);
      
      // 收集运营数据
      const operationsData = await this.dataCollector.collect(inputs.companyData);
      
      // 执行分析（可选择关注领域以控制上下文）
      const analysisResults = await this.analyzer.analyze(
        operationsData, 
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
 * 运营数据收集模块
 * 程序化执行运营数据收集
 */
class OperationsDataCollectionModule {
  async collect(companyData) {
    // 并行收集运营相关信息
    const [processData, qualityData, supplyChainData, costData] = await Promise.allSettled([
      this.getProcessData(companyData),
      this.getQualityData(companyData),
      this.getSupplyChainData(companyData),
      this.getCostData(companyData)
    ]);
    
    return {
      companyProfile: companyData,
      processData: processData.status === 'fulfilled' ? processData.value : null,
      qualityData: qualityData.status === 'fulfilled' ? qualityData.value : null,
      supplyChainData: supplyChainData.status === 'fulfilled' ? supplyChainData.value : null,
      costData: costData.status === 'fulfilled' ? costData.value : null
    };
  }
  
  async getProcessData(companyData) {
    // 模拟从运营系统获取流程数据
    return {
      cycleTimes: {
        avg: 4.5, // 平均周期时间（天）
        min: 1.2,
        max: 12.8
      },
      throughput: 10000, // 日处理量
      utilizationRates: {
        equipment: 0.78,
        labor: 0.82
      },
      bottlenecks: ["质检环节", "包装环节"],
      automationLevel: 0.65
    };
  }
  
  async getQualityData(companyData) {
    // 模拟从质量管理系统获取数据
    return {
      defectRate: 25, // 百万分之25
      qualityMetrics: {
        firstPassYield: 0.965,
        customerComplaints: 12,
        auditScore: 92
      },
      qualitySystems: ["ISO 9001", "Six Sigma"],
      improvementInitiatives: ["Lean Manufacturing", "Kaizen"]
    };
  }
  
  async getSupplyChainData(companyData) {
    // 模拟从供应链系统获取数据
    return {
      suppliers: 45,
      keySuppliers: 8,
      geographicDistribution: {
        local: 0.4,
        regional: 0.35,
        global: 0.25
      },
      leadTimes: {
        avg: 14, // 平均提前期（天）
        min: 3,
        max: 30
      },
      riskFactors: ["单一供应商依赖", "运输风险"],
      performanceMetrics: {
        onTimeDelivery: 0.94,
        fillRate: 0.97
      }
    };
  }
  
  async getCostData(companyData) {
    // 模拟从财务系统获取成本数据
    return {
      costStructure: {
        materials: 0.45, // 原材料占比
        labor: 0.25,     // 人工占比
        overhead: 0.20,  // 间接费用占比
        other: 0.10      // 其他费用占比
      },
      costPerUnit: 125.50,
      costTrends: {
        materialCostTrend: "上升",
        laborCostTrend: "稳定",
        overheadTrend: "下降"
      }
    };
  }
}

/**
 * 运营分析模块
 * 定量计算程序化，定性分析AI化
 */
class OperationsAnalysisModule {
  async analyze(data, focusAreas = null, detailed = false) {
    // 根据focusAreas决定分析详略程度，实现渐进式披露
    const analysis = {};
    
    // 流程效率分析（定量，程序化）
    if (!focusAreas || focusAreas.includes('processEfficiency')) {
      analysis.processEfficiency = await this.analyzeProcessEfficiency(data, detailed);
    }
    
    // 质量管理分析（定量+定性）
    if (!focusAreas || focusAreas.includes('qualityManagement')) {
      analysis.qualityManagement = await this.analyzeQualityManagement(data, detailed);
    }
    
    // 供应链分析（定量+定性）
    if (!focusAreas || focusAreas.includes('supplyChain')) {
      analysis.supplyChain = await this.analyzeSupplyChain(data, detailed);
    }
    
    // 成本优化分析（定量+定性）
    if (!focusAreas || focusAreas.includes('costOptimization')) {
      analysis.costOptimization = await this.analyzeCostOptimization(data, detailed);
    }
    
    // 产能规划分析（定量，程序化）
    if (!focusAreas || focusAreas.includes('capacityPlanning')) {
      analysis.capacityPlanning = await this.analyzeCapacityPlanning(data, detailed);
    }
    
    // 库存管理分析（定量，程序化）
    if (!focusAreas || focusAreas.includes('inventoryManagement')) {
      analysis.inventoryManagement = await this.analyzeInventoryManagement(data, detailed);
    }
    
    // 物流分析（定量+定性）
    if (!focusAreas || focusAreas.includes('logistics')) {
      analysis.logistics = await this.analyzeLogistics(data, detailed);
    }
    
    // 绩效指标分析（定量，程序化）
    if (!focusAreas || focusAreas.includes('performanceMetrics')) {
      analysis.performanceMetrics = await this.analyzePerformanceMetrics(data, detailed);
    }
    
    return {
      operationsElements: analysis,
      operationalData: data,
      analysisTimestamp: new Date().toISOString()
    };
  }
  
  async analyzeProcessEfficiency(data, detailed = false) {
    // 程序化计算流程效率指标
    const processData = data.processData;
    if (!processData) {
      return {
        efficiency: "数据不足",
        assessment: "需要完整运营流程数据"
      };
    }
    
    const avgCycleTime = processData.cycleTimes.avg;
    const equipmentUtil = processData.utilizationRates.equipment;
    const laborUtil = processData.utilizationRates.labor;
    
    // 评估效率水平
    const efficiencyScore = this.calculateEfficiencyScore(avgCycleTime, equipmentUtil, laborUtil);
    const assessment = this.assessProcessEfficiency(efficiencyScore);
    
    const result = {
      currentState: assessment,
      avgCycleTime: avgCycleTime,
      equipmentUtilization: equipmentUtil,
      laborUtilization: laborUtil,
      bottlenecks: processData.bottlenecks || [],
      automationLevel: processData.automationLevel,
      efficiencyScore: efficiencyScore,
      improvementPotential: 1 - (efficiencyScore / 100)
    };
    
    if (detailed) {
      result.detailedMetrics = {
        cycleTimeRange: processData.cycleTimes,
        throughput: processData.throughput,
        detailedBottlenecks: processData.bottlenecks,
        automationPlan: "提升至0.80自动化水平"
      };
    }
    
    return result;
  }
  
  calculateEfficiencyScore(cycleTime, equipUtil, laborUtil) {
    // 综合计算效率分数（0-100）
    let score = 0;
    
    // 周期时间评分（越短越好，假设行业平均为5天）
    if (cycleTime <= 3) score += 30;
    else if (cycleTime <= 5) score += 25;
    else if (cycleTime <= 7) score += 20;
    else score += 15;
    
    // 设备利用率评分（适中为好，过高过低都不佳）
    if (equipUtil >= 0.7 && equipUtil <= 0.9) score += 25;
    else if (equipUtil >= 0.5 && equipUtil < 0.7) score += 20;
    else if (equipUtil >= 0.9 && equipUtil <= 0.95) score += 20;
    else score += 10;
    
    // 人工利用率评分
    if (laborUtil >= 0.7 && laborUtil <= 0.9) score += 25;
    else if (laborUtil >= 0.5 && laborUtil < 0.7) score += 20;
    else if (laborUtil >= 0.9 && laborUtil <= 0.95) score += 20;
    else score += 10;
    
    return Math.min(100, score);
  }
  
  assessProcessEfficiency(score) {
    if (score >= 85) return "流程效率优秀";
    if (score >= 70) return "流程效率良好";
    if (score >= 50) return "流程效率一般";
    return "流程效率需改进";
  }
  
  async analyzeQualityManagement(data, detailed = false) {
    // 分析质量管理
    const qualityData = data.qualityData;
    
    const result = {
      system: qualityData?.qualitySystems?.join(', ') || "待评估",
      defectRate: qualityData?.defectRate ? `百万分之${qualityData.defectRate}` : "待评估",
      firstPassYield: qualityData?.qualityMetrics?.firstPassYield,
      onTimeQuality: qualityData?.qualityMetrics?.auditScore,
      effectiveness: this.assessQualityEffectiveness(qualityData)
    };
    
    if (detailed) {
      result.detailedAssessment = {
        qualityMetrics: qualityData?.qualityMetrics,
        improvementInitiatives: qualityData?.improvementInitiatives,
        customerFeedback: qualityData?.qualityMetrics?.customerComplaints,
        qualityCosts: "待具体数据"
      };
    }
    
    return result;
  }
  
  assessQualityEffectiveness(qualityData) {
    if (!qualityData || !qualityData.qualityMetrics) return "待评估";
    
    const yield = qualityData.qualityMetrics.firstPassYield || 0;
    const auditScore = qualityData.qualityMetrics.auditScore || 0;
    
    if (yield >= 0.97 && auditScore >= 90) return "优秀";
    if (yield >= 0.95 && auditScore >= 85) return "良好";
    if (yield >= 0.90 && auditScore >= 80) return "一般";
    return "需改进";
  }
  
  async analyzeSupplyChain(data, detailed = false) {
    // 分析供应链
    const supplyData = data.supplyChainData;
    
    const result = {
      structure: this.describeSupplyChainStructure(supplyData),
      keyPartners: supplyData?.keySuppliers,
      efficiencyMetrics: {
        onTimeDelivery: supplyData?.performanceMetrics?.onTimeDelivery,
        fillRate: supplyData?.performanceMetrics?.fillRate
      },
      efficiency: this.assessSupplyChainEfficiency(supplyData),
      riskFactors: supplyData?.riskFactors || []
    };
    
    if (detailed) {
      result.detailedAnalysis = {
        supplierCount: supplyData?.suppliers,
        geographicDistribution: supplyData?.geographicDistribution,
        leadTimeAnalysis: supplyData?.leadTimes,
        riskMitigation: ["多元化供应", "安全库存"],
        collaborationLevel: "中等"
      };
    }
    
    return result;
  }
  
  describeSupplyChainStructure(supplyData) {
    if (!supplyData) return "待评估";
    const suppliers = supplyData.suppliers || 0;
    const localRatio = supplyData.geographicDistribution?.local || 0;
    
    if (suppliers > 50) return "复杂多级供应链";
    if (suppliers > 20) return "多层次供应链";
    return "相对简单的供应链结构";
  }
  
  assessSupplyChainEfficiency(supplyData) {
    if (!supplyData || !supplyData.performanceMetrics) return "待评估";
    
    const onTime = supplyData.performanceMetrics.onTimeDelivery || 0;
    const fillRate = supplyData.performanceMetrics.fillRate || 0;
    
    if (onTime >= 0.95 && fillRate >= 0.95) return "高效";
    if (onTime >= 0.90 && fillRate >= 0.90) return "良好";
    if (onTime >= 0.85 && fillRate >= 0.85) return "一般";
    return "需改进";
  }
  
  async analyzeCostOptimization(data, detailed = false) {
    // 分析成本优化
    const costData = data.costData;
    
    const result = {
      costStructure: costData?.costStructure || {},
      costPerUnit: costData?.costPerUnit || 0,
      costTrends: costData?.costTrends || {},
      optimizationPotential: this.assessCostOptimizationPotential(costData),
      initiatives: ["精益生产", "供应商整合", "自动化升级"]
    };
    
    if (detailed) {
      result.detailedCostAnalysis = {
        detailedStructure: costData?.costStructure,
        costDrivers: this.identifyCostDrivers(costData),
        benchmarking: "待行业基准数据",
        improvementRoadmap: ["短期: 降低材料成本", "中期: 提高效率", "长期: 工艺创新"]
      };
    }
    
    return result;
  }
  
  assessCostOptimizationPotential(costData) {
    if (!costData) return 0.05; // 假设5%优化潜力
    
    // 基于成本结构和趋势评估优化潜力
    let potential = 0.05; // 基础优化潜力
    
    // 如果材料成本占比高，优化潜力可能更大
    if (costData.costStructure?.materials > 0.5) potential += 0.10;
    
    // 如果人工成本趋势稳定，自动化优化潜力大
    if (costData.costTrends?.laborCostTrend === "上升") potential += 0.05;
    
    return Math.min(0.25, potential); // 最大25%优化潜力
  }
  
  identifyCostDrivers(costData) {
    if (!costData?.costStructure) return ["待评估"];
    
    const structure = costData.costStructure;
    const drivers = [];
    
    if (structure.materials > 0.4) drivers.push("材料成本");
    if (structure.labor > 0.3) drivers.push("人工成本");
    if (structure.overhead > 0.2) drivers.push("间接费用");
    
    return drivers.length > 0 ? drivers : ["其他成本因素"];
  }
  
  async analyzeCapacityPlanning(data, detailed = false) {
    // 分析产能规划
    const processData = data.processData;
    
    const result = {
      currentUtilization: processData?.utilizationRates?.equipment || 0,
      capacityFlexibility: this.assessCapacityFlexibility(processData),
      expansionNeeds: this.assessExpansionNeeds(processData),
      efficiency: this.assessCapacityEfficiency(processData)
    };
    
    if (detailed) {
      result.detailedCapacity = {
        equipmentUtilization: processData?.utilizationRates?.equipment,
        laborUtilization: processData?.utilizationRates?.labor,
        peakCapacity: "待具体数据",
        capacityConstraints: processData?.bottlenecks || [],
        capacityPlanningHorizon: "中长期规划"
      };
    }
    
    return result;
  }
  
  assessCapacityFlexibility(processData) {
    if (!processData) return "待评估";
    
    const equipUtil = processData.utilizationRates?.equipment || 0;
    
    if (equipUtil >= 0.7 && equipUtil <= 0.85) return "灵活性良好";
    if (equipUtil > 0.85) return "灵活性较低";
    if (equipUtil < 0.7) return "灵活性较高";
    return "待评估";
  }
  
  assessExpansionNeeds(processData) {
    if (!processData) return "待评估";
    
    const equipUtil = processData.utilizationRates?.equipment || 0;
    
    if (equipUtil > 0.9) return "急需扩张";
    if (equipUtil > 0.85) return "短期需扩张";
    if (equipUtil > 0.75) return "中期考虑扩张";
    return "暂无需扩张";
  }
  
  assessCapacityEfficiency(processData) {
    if (!processData) return "待评估";
    
    const equipUtil = processData.utilizationRates?.equipment || 0;
    
    if (equipUtil >= 0.75 && equipUtil <= 0.9) return "高效";
    if (equipUtil >= 0.65 || equipUtil <= 0.95) return "良好";
    return "需改进";
  }
  
  async analyzeInventoryManagement(data, detailed = false) {
    // 分析库存管理
    const result = {
      turnoverRate: 8.5, // 假设值
      managementSystem: "JIT与安全库存结合",
      efficiency: "高效",
      inventoryLevels: {
        rawMaterials: "安全库存+需求预测",
        wip: "看板管理",
        finishedGoods: "按需生产"
      }
    };
    
    if (detailed) {
      result.detailedInventory = {
        turnoverRate: result.turnoverRate,
        inventoryAccuracy: 0.98, // 假设98%准确率
        safetyStockLevels: "基于需求波动计算",
        obsoleteInventory: "低于5%",
        inventoryManagementSystem: result.managementSystem
      };
    }
    
    return result;
  }
  
  async analyzeLogistics(data, detailed = false) {
    // 分析物流
    const result = {
      network: "多层次配送网络",
      efficiency: "高效",
      costRatio: 0.08, // 物流成本占收入比例
      performanceMetrics: {
        onTimeDelivery: 0.94,
        damageRate: 0.005,
        costPerShipment: 12.50
      }
    };
    
    if (detailed) {
      result.detailedLogistics = {
        distributionNetwork: result.network,
        logisticsProviders: ["主要承运商", "区域配送商"],
        technologyUsage: ["TMS", "GPS追踪", "自动化分拣"],
        sustainability: "绿色物流实践"
      };
    }
    
    return result;
  }
  
  async analyzePerformanceMetrics(data, detailed = false) {
    // 分析绩效指标
    const result = {
      kpiSet: ["OEE", "交付准时率", "质量合格率", "成本控制率"],
      dashboard: "实时监控仪表板",
      effectiveness: "高效",
      keyMetrics: {
        oee: 0.82, // 设备综合效率
        assetUtilization: 0.78,
        productivity: "待具体数据"
      }
    };
    
    if (detailed) {
      result.detailedMetrics = {
        kpiFramework: result.kpiSet,
        monitoringSystem: result.dashboard,
        reportingFrequency: "日/周/月",
        targetAchievement: 0.92, // 目标达成率
        metricAlignment: "与战略目标对齐度高"
      };
    }
    
    return result;
  }
}

/**
 * 运营验证模块
 */
class OperationsValidationModule {
  async validate(analysisResults) {
    const validationResults = {
      dataCompleteness: await this.checkDataCompleteness(analysisResults),
      calculationAccuracy: await this.checkCalculationAccuracy(analysisResults),
      consistency: await this.checkConsistency(analysisResults),
      practicalRelevance: await this.checkPracticalRelevance(analysisResults)
    };
    
    const overallScore = this.calculateOverallScore(validationResults);
    
    return {
      ...analysisResults,
      validation: validationResults,
      overallValidationScore: overallScore
    };
  }
  
  async checkDataCompleteness(results) {
    const sourceData = results.operationalData;
    const completenessFactors = {
      processData: !!sourceData.processData,
      qualityData: !!sourceData.qualityData,
      supplyChainData: !!sourceData.supplyChainData,
      costData: !!sourceData.costData
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
    // 验证运营计算的准确性
    const elements = results.operationsElements;
    const issues = [];
    
    // 验证关键指标的合理性
    if (elements.processEfficiency) {
      const eff = elements.processEfficiency;
      if (eff.avgCycleTime < 0) {
        issues.push("周期时间不能为负数");
      }
      if (eff.equipmentUtilization > 1 || eff.equipmentUtilization < 0) {
        issues.push("设备利用率应在0-1之间");
      }
    }
    
    return {
      issues: issues,
      accuracyLevel: issues.length === 0 ? "high" : "medium",
      accuracyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 25))
    };
  }
  
  async checkConsistency(results) {
    // 检查分析结果的内在一致性
    const elements = results.operationsElements;
    const issues = [];
    
    // 检查运营要素间的一致性
    if (elements.capacityPlanning && elements.processEfficiency) {
      const capEff = elements.capacityPlanning.efficiency;
      const procEff = elements.processEfficiency.efficiency;
      
      if (procEff !== "流程效率需改进" && capEff === "需改进") {
        issues.push("流程效率与产能效率评估可能存在矛盾");
      }
    }
    
    return {
      issues: issues,
      consistencyLevel: issues.length === 0 ? "high" : "medium",
      consistencyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 30))
    };
  }
  
  async checkPracticalRelevance(results) {
    // 检查分析结果的实用性
    const elements = results.operationsElements;
    const relevanceIssues = [];
    
    // 检查建议的实用性
    if (elements.processEfficiency?.improvementPotential > 0.3) {
      relevanceIssues.push("流程效率改进潜力过高，需验证数据准确性");
    }
    
    return {
      issues: relevanceIssues,
      relevanceLevel: relevanceIssues.length === 0 ? "high" : "medium",
      relevanceScore: relevanceIssues.length === 0 ? 100 : Math.max(0, 100 - (relevanceIssues.length * 15))
    };
  }
  
  calculateOverallScore(validationResults) {
    const { dataCompleteness, calculationAccuracy, consistency, practicalRelevance } = validationResults;
    
    // 加权计算总体分数
    const weights = {
      completeness: 0.25,
      accuracy: 0.30,
      consistency: 0.25,
      relevance: 0.20
    };
    
    return Math.round(
      (dataCompleteness.completenessScore * weights.completeness) +
      (calculationAccuracy.accuracyScore * weights.accuracy) +
      (consistency.consistencyScore * weights.consistency) +
      (practicalRelevance.relevanceScore * weights.relevance)
    );
  }
}

/**
 * 运营分析报告生成模块
 * 支持渐进式披露：根据需求生成不同详细程度的报告
 */
class OperationsReportingModule {
  async generate(analysisResults, detailed = false, depth = 'standard') {
    const report = {
      analysisSummary: this.createExecutiveSummary(analysisResults),
      keyMetrics: this.extractKeyMetrics(analysisResults),
      operationsElements: detailed ? 
        analysisResults.operationsElements : 
        this.createSummaryElements(analysisResults.operationsElements),
      recommendations: await this.generateRecommendations(analysisResults),
      metadata: {
        generationTime: new Date().toISOString(),
        validationScore: analysisResults.overallValidationScore,
        detailLevel: detailed ? "detailed" : "summary"
      }
    };
    
    // 详细模式下添加额外内容
    if (detailed) {
      report.fullAnalysis = analysisResults.operationsElements;
      report.validationDetails = analysisResults.validation;
    }
    
    return report;
  }
  
  createExecutiveSummary(results) {
    const elements = results.operationsElements;
    
    return {
      executiveSummary: `对${results.operationalData.companyProfile.name}的运营分析显示，该企业运营体系整体${this.getOverallOperationsAssessment(results)}, 总体验证得分为${results.overallValidationScore}分。`,
      keyFindings: [
        `流程效率: ${elements.processEfficiency?.currentState || 'N/A'}`,
        `供应链效率: ${elements.supplyChain?.efficiency || 'N/A'}`,
        `质量水平: ${elements.qualityManagement?.effectiveness || 'N/A'}`
      ],
      overallAssessment: this.assessOperationsHealth(results.overallValidationScore)
    };
  }
  
  getOverallOperationsAssessment(results) {
    const elements = results.operationsElements;
    const scores = [
      elements.processEfficiency?.efficiencyScore || 0,
      elements.qualityManagement?.onTimeQuality || 0,
      elements.supplyChain?.efficiency === "高效" ? 90 : elements.supplyChain?.efficiency === "良好" ? 75 : 60,
      elements.performanceMetrics?.keyMetrics?.oee ? elements.performanceMetrics.keyMetrics.oee * 100 : 0
    ];
    
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    
    if (avgScore >= 85) return "优秀，运营体系高效";
    if (avgScore >= 70) return "良好，运营体系稳健";
    if (avgScore >= 50) return "一般，部分领域需改进";
    return "需改进，运营体系存在显著问题";
  }
  
  assessOperationsHealth(score) {
    if (score >= 85) return "优秀 - 运营体系高效，管理规范";
    if (score >= 70) return "良好 - 运营体系较为完善";
    if (score >= 50) return "一般 - 部分运营指标需要关注";
    return "需改进 - 运营体系存在明显不足";
  }
  
  extractKeyMetrics(results) {
    const elements = results.operationsElements;
    
    return {
      processEfficiencyScore: elements.processEfficiency?.efficiencyScore,
      equipmentUtilization: elements.processEfficiency?.equipmentUtilization,
      qualityEffectiveness: elements.qualityManagement?.effectiveness,
      supplyChainEfficiency: elements.supplyChain?.efficiency,
      inventoryTurnover: elements.inventoryManagement?.turnoverRate,
      oee: elements.performanceMetrics?.keyMetrics?.oee
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
      case 'processEfficiency':
        return elementValue.currentState || '待评估';
      case 'qualityManagement':
        return `质量${elementValue.effectiveness || 'N/A'}`;
      case 'supplyChain':
        return `供应链${elementValue.efficiency || 'N/A'}`;
      case 'inventoryManagement':
        return `库存管理${elementValue.efficiency || 'N/A'}`;
      default:
        return '已分析';
    }
  }
  
  extractElementScore(elementKey, elementValue) {
    switch(elementKey) {
      case 'processEfficiency':
        return elementValue.efficiencyScore;
      case 'qualityManagement':
        return elementValue.onTimeQuality;
      case 'supplyChain':
        return elementValue.efficiency === '高效' ? 90 : 
               elementValue.efficiency === '良好' ? 75 : 60;
      default:
        return null;
    }
  }
  
  async generateRecommendations(results) {
    const recommendations = [];
    const elements = results.operationsElements;
    const validation = results.validation;
    
    // 基于验证结果的建议
    if (validation.consistency.issues.length > 0) {
      recommendations.push(`解决运营要素间的一致性问题: ${validation.consistency.issues.join(', ')}`);
    }
    
    // 基于具体分析结果的建议
    if (elements.processEfficiency?.improvementPotential > 0.15) {
      recommendations.push("重点关注流程瓶颈环节，提升整体效率");
    }
    
    if (elements.supplyChain?.riskFactors?.length > 0) {
      recommendations.push(`加强供应链风险管理: ${elements.supplyChain.riskFactors.join(', ')}`);
    }
    
    if (elements.qualityManagement?.effectiveness === "需改进") {
      recommendations.push("加强质量管理体系，实施质量改进计划");
    }
    
    if (results.overallValidationScore < 75) {
      recommendations.push("完善运营管理数据收集，提升分析准确性");
    }
    
    return recommendations.length > 0 ? recommendations : 
           ["企业运营整体表现良好，继续保持现有管理实践"];
  }
}

// 导出技能类
if (typeof module !== 'undefined' && module.exports) {
  module.exports = OperationsAnalysisSkill;
}