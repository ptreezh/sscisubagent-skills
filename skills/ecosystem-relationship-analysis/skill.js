/**
 * 生态系统关系分析技能实现
 * 遵循agentskills.io规范和渐进式披露原则
 */

class EcosystemRelationshipAnalysisSkill {
  constructor() {
    this.skillId = "ecosystem-relationship-analysis";
    this.version = "2.0.0";
    this.name = "生态系统关系分析";
    this.description = "专门分析商业生态系统中各主体间关系的技能";
    
    // 初始化模块
    this.dataProcessor = new EcosystemDataProcessor();
    this.relationshipAnalyzer = new RelationshipAnalysisModule();
    this.networkAnalyzer = new NetworkAnalysisModule();
    this.validator = new ValidationModule();
    this.reporter = new EcosystemReportingModule();
  }

  /**
   * 执行技能主方法
   * 实现渐进式披露：根据analysisDepth参数决定分析详略程度
   */
  async execute(inputs) {
    try {
      // 验证输入参数
      this.validateInputs(inputs);
      
      // 处理生态系统数据
      const processedData = await this.dataProcessor.process(inputs);
      
      // 执行关系分析
      const analysisResults = await this.relationshipAnalyzer.analyze(
        processedData.entities, 
        processedData.relationships,
        inputs.relationshipTypes || ['all'],
        inputs.analysisDepth || 'standard'
      );
      
      // 执行网络分析
      const networkResults = await this.networkAnalyzer.analyze(
        processedData.entities, 
        processedData.relationships
      );
      
      // 合并分析结果
      const combinedResults = {
        ...analysisResults,
        networkProperties: networkResults,
        sourceData: processedData
      };
      
      // 验证结果
      const validatedResults = await this.validator.validate(combinedResults);
      
      // 生成报告
      const finalReport = await this.reporter.generate(
        validatedResults, 
        inputs.analysisDepth || 'standard'
      );
      
      return {
        success: true,
        data: finalReport,
        metadata: {
          skillId: this.skillId,
          version: this.version,
          executionTime: new Date().toISOString(),
          contextLevel: inputs.analysisDepth || 'standard'
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
    if (!inputs || !inputs.entities || !inputs.relationships) {
      throw new Error("缺少必需的entities或relationships参数");
    }
    
    if (!Array.isArray(inputs.entities) || !Array.isArray(inputs.relationships)) {
      throw new Error("entities和relationships必须是数组");
    }
  }
}

/**
 * 生态系统数据处理器
 * 程序化执行数据预处理任务
 */
class EcosystemDataProcessor {
  async process(inputs) {
    const entities = this.processEntities(inputs.entities);
    const relationships = this.processRelationships(inputs.relationships, entities);
    
    return {
      entities: entities,
      relationships: relationships,
      processedTimestamp: new Date().toISOString()
    };
  }
  
  processEntities(rawEntities) {
    // 标准化实体数据
    return rawEntities.map(entity => ({
      id: entity.id,
      name: entity.name || '未知实体',
      type: entity.type || 'unknown',
      characteristics: entity.characteristics || {},
      importance: this.calculateEntityImportance(entity)
    }));
  }
  
  processRelationships(rawRelationships, entities) {
    // 标准化关系数据并添加缺失信息
    return rawRelationships.map(rel => ({
      source: rel.source,
      target: rel.target,
      type: rel.type || 'unknown',
      strength: rel.strength || 0.5,
      bidirectional: rel.bidirectional || false,
      description: rel.description || this.generateRelationshipDescription(rel, entities)
    }));
  }
  
  calculateEntityImportance(entity) {
    // 基于实体特征计算重要性分数
    const characteristics = entity.characteristics || {};
    let score = 0.5; // 默认分数
    
    // 根据特征调整重要性
    if (characteristics.marketCap) {
      score += Math.min(0.3, Math.log10(characteristics.marketCap / 1000000) / 10);
    }
    if (characteristics.employees) {
      score += Math.min(0.2, Math.log10(characteristics.employees) / 5);
    }
    if (characteristics.influence) {
      score += characteristics.influence / 200; // 假设影响力度量为0-100
    }
    
    return Math.min(1.0, Math.max(0.1, score));
  }
  
  generateRelationshipDescription(rel, entities) {
    const sourceEntity = entities.find(e => e.id === rel.source);
    const targetEntity = entities.find(e => e.id === rel.target);
    
    if (sourceEntity && targetEntity) {
      return `${sourceEntity.name}与${targetEntity.name}之间存在${rel.type}关系`;
    }
    return `实体${rel.source}与实体${rel.target}的关系`;
  }
}

/**
 * 关系分析模块
 * 分析不同类型的生态系统关系
 */
class RelationshipAnalysisModule {
  async analyze(entities, relationships, focusTypes = ['all'], depth = 'standard') {
    // 根据focusTypes分析特定关系类型
    const allTypes = focusTypes.includes('all') ? 
      [...new Set(relationships.map(r => r.type))] : 
      focusTypes;
    
    const relationshipTypes = {};
    
    for (const type of allTypes) {
      relationshipTypes[type] = await this.analyzeRelationshipType(
        entities, 
        relationships, 
        type, 
        depth
      );
    }
    
    // 识别关键关系
    const keyRelationships = await this.identifyKeyRelationships(relationships, entities);
    
    return {
      relationshipTypes: relationshipTypes,
      keyRelationships: keyRelationships,
      analysisSummary: this.createAnalysisSummary(relationshipTypes, keyRelationships)
    };
  }
  
  async analyzeRelationshipType(entities, relationships, type, depth) {
    const typeRelationships = relationships.filter(r => r.type === type);
    
    if (typeRelationships.length === 0) {
      return {
        count: 0,
        avgStrength: 0,
        entitiesInvolved: [],
        characteristics: {}
      };
    }
    
    // 计算关系统计信息
    const avgStrength = typeRelationships.reduce((sum, r) => sum + r.strength, 0) / typeRelationships.length;
    
    // 识别参与的实体
    const entityIds = [...new Set(typeRelationships.flatMap(r => [r.source, r.target]))];
    const entitiesInvolved = entities.filter(e => entityIds.includes(e.id));
    
    // 深度分析
    let characteristics = {};
    if (depth === 'comprehensive') {
      characteristics = {
        strengthDistribution: this.calculateStrengthDistribution(typeRelationships),
        centralEntities: this.identifyCentralEntities(typeRelationships),
        stabilityFactors: this.assessStabilityFactors(type, typeRelationships)
      };
    }
    
    return {
      count: typeRelationships.length,
      avgStrength: avgStrength,
      entitiesInvolved: entitiesInvolved,
      characteristics: characteristics
    };
  }
  
  calculateStrengthDistribution(relationships) {
    const distribution = {
      weak: relationships.filter(r => r.strength < 0.3).length,
      medium: relationships.filter(r => r.strength >= 0.3 && r.strength < 0.7).length,
      strong: relationships.filter(r => r.strength >= 0.7).length
    };
    
    return {
      ...distribution,
      total: relationships.length,
      percentages: {
        weak: relationships.length > 0 ? (distribution.weak / relationships.length) * 100 : 0,
        medium: relationships.length > 0 ? (distribution.medium / relationships.length) * 100 : 0,
        strong: relationships.length > 0 ? (distribution.strong / relationships.length) * 100 : 0
      }
    };
  }
  
  identifyCentralEntities(relationships) {
    // 计算每个实体的关系度数（连接数）
    const degreeMap = {};
    relationships.forEach(rel => {
      degreeMap[rel.source] = (degreeMap[rel.source] || 0) + 1;
      degreeMap[rel.target] = (degreeMap[rel.target] || 0) + 1;
    });
    
    // 返回度数最高的实体
    const entries = Object.entries(degreeMap).sort((a, b) => b[1] - a[1]);
    return entries.slice(0, 5).map(([id, count]) => ({ id, connections: count }));
  }
  
  assessStabilityFactors(type, relationships) {
    // 根据关系类型评估稳定性因素
    const factors = {
      type: type,
      stabilityIndicators: []
    };
    
    switch(type) {
      case 'cooperation':
        factors.stabilityIndicators = ['合同约束', '利益共享', '长期协议'];
        break;
      case 'supply':
        factors.stabilityIndicators = ['供应稳定性', '价格协议', '质量标准'];
        break;
      case 'investment':
        factors.stabilityIndicators = ['股权关系', '利益绑定', '治理结构'];
        break;
      case 'regulation':
        factors.stabilityIndicators = ['合规要求', '监督机制', '法律约束'];
        break;
      default:
        factors.stabilityIndicators = ['关系协议', '互惠机制', '市场约束'];
    }
    
    return factors;
  }
  
  async identifyKeyRelationships(relationships, entities) {
    // 识别关键关系：高强度关系或连接重要实体的关系
    const keyRelationships = relationships
      .map(rel => {
        const sourceEntity = entities.find(e => e.id === rel.source);
        const targetEntity = entities.find(e => e.id === rel.target);
        
        const sourceImportance = sourceEntity ? sourceEntity.importance : 0.5;
        const targetImportance = targetEntity ? targetEntity.importance : 0.5;
        
        // 关键关系分数 = 强度 × (源实体重要性 + 目标实体重要性)
        const keyScore = rel.strength * (sourceImportance + targetImportance);
        
        return {
          ...rel,
          keyScore: keyScore,
          sourceImportance: sourceImportance,
          targetImportance: targetImportance
        };
      })
      .sort((a, b) => b.keyScore - a.keyScore)
      .slice(0, 10); // 只取前10个关键关系
    
    return keyRelationships;
  }
  
  createAnalysisSummary(relationshipTypes, keyRelationships) {
    const totalCount = Object.values(relationshipTypes).reduce((sum, type) => sum + type.count, 0);
    const avgStrength = Object.values(relationshipTypes).reduce((sum, type) => sum + (type.avgStrength || 0), 0) / 
                      Object.keys(relationshipTypes).length;
    
    return {
      totalRelationships: totalCount,
      averageStrength: avgStrength,
      relationshipTypeCount: Object.keys(relationshipTypes).length,
      keyRelationshipCount: keyRelationships.length,
      primaryTypes: Object.keys(relationshipTypes).slice(0, 3)
    };
  }
}

/**
 * 网络分析模块
 * 分析生态系统网络的整体属性
 */
class NetworkAnalysisModule {
  async analyze(entities, relationships) {
    // 计算网络拓扑属性
    const topology = this.calculateNetworkTopology(entities, relationships);
    
    // 计算中心性指标
    const centralities = this.calculateCentralities(entities, relationships);
    
    // 识别社区结构
    const communities = this.identifyCommunities(entities, relationships);
    
    // 评估网络健康度
    const health = this.assessNetworkHealth(topology, centralities);
    
    return {
      topology: topology,
      centralities: centralities,
      communities: communities,
      health: health
    };
  }
  
  calculateNetworkTopology(entities, relationships) {
    const totalEntities = entities.length;
    const totalRelationships = relationships.length;
    const possibleRelationships = totalEntities > 1 ? totalEntities * (totalEntities - 1) : 0;
    
    return {
      entityCount: totalEntities,
      relationshipCount: totalRelationships,
      density: possibleRelationships > 0 ? totalRelationships / possibleRelationships : 0,
      averageDegree: totalEntities > 0 ? (totalRelationships * 2) / totalEntities : 0,
      connectedComponents: this.findConnectedComponents(entities, relationships)
    };
  }
  
  findConnectedComponents(entities, relationships) {
    // 简单的连通分量算法
    const visited = new Set();
    const components = [];
    
    for (const entity of entities) {
      if (!visited.has(entity.id)) {
        const component = [];
        this.dfs(entity.id, relationships, visited, component);
        components.push(component);
      }
    }
    
    return {
      count: components.length,
      largestComponent: Math.max(...components.map(c => c.length), 0),
      distribution: components.map(c => c.length).sort((a, b) => b - a)
    };
  }
  
  dfs(startId, relationships, visited, component) {
    visited.add(startId);
    component.push(startId);
    
    // 查找与当前实体相关的所有关系
    for (const rel of relationships) {
      if (rel.source === startId && !visited.has(rel.target)) {
        this.dfs(rel.target, relationships, visited, component);
      } else if (rel.target === startId && !visited.has(rel.source)) {
        this.dfs(rel.source, relationships, visited, component);
      }
    }
  }
  
  calculateCentralities(entities, relationships) {
    // 计算度中心性
    const degreeCentralities = this.calculateDegreeCentralities(relationships);
    
    // 计算邻近中心性（简化版）
    const closenessCentralities = this.calculateClosenessCentralities(entities, relationships);
    
    // 计算介数中心性（简化版）
    const betweennessCentralities = this.calculateBetweennessCentralities(entities, relationships);
    
    return {
      degree: degreeCentralities,
      closeness: closenessCentralities,
      betweenness: betweennessCentralities
    };
  }
  
  calculateDegreeCentralities(relationships) {
    const degrees = {};
    
    for (const rel of relationships) {
      degrees[rel.source] = (degrees[rel.source] || 0) + 1;
      degrees[rel.target] = (degrees[rel.target] || 0) + 1;
    }
    
    return degrees;
  }
  
  calculateClosenessCentralities(entities, relationships) {
    // 简化的邻近中心性计算
    const centralities = {};
    
    for (const entity of entities) {
      // 基于连接数的简化计算
      const connections = Object.values(this.calculateDegreeCentralities(relationships))[entity.id] || 0;
      centralities[entity.id] = connections > 0 ? connections / entities.length : 0;
    }
    
    return centralities;
  }
  
  calculateBetweennessCentralities(entities, relationships) {
    // 简化的介数中心性计算
    const centralities = {};
    
    for (const entity of entities) {
      // 基于度中心性的简化计算
      const degree = Object.values(this.calculateDegreeCentralities(relationships))[entity.id] || 0;
      centralities[entity.id] = degree / Math.max(1, entities.length - 1);
    }
    
    return centralities;
  }
  
  identifyCommunities(entities, relationships) {
    // 简化的社区检测（基于关系强度和类型）
    const communities = [];
    const entityToCommunity = new Map();
    
    // 使用简单的聚类方法（基于强关系）
    let communityId = 0;
    
    for (const rel of relationships) {
      if (rel.strength > 0.7) { // 强关系阈值
        const sourceCommunity = entityToCommunity.get(rel.source);
        const targetCommunity = entityToCommunity.get(rel.target);
        
        if (sourceCommunity === undefined && targetCommunity === undefined) {
          // 两个实体都不在社区中，创建新社区
          entityToCommunity.set(rel.source, communityId);
          entityToCommunity.set(rel.target, communityId);
          communities.push({
            id: communityId,
            entities: [rel.source, rel.target],
            relationships: [rel.id || `${rel.source}-${rel.target}`]
          });
          communityId++;
        } else if (sourceCommunity !== undefined && targetCommunity === undefined) {
          // 目标实体加入源实体的社区
          entityToCommunity.set(rel.target, sourceCommunity);
          communities.find(c => c.id === sourceCommunity).entities.push(rel.target);
        } else if (sourceCommunity === undefined && targetCommunity !== undefined) {
          // 源实体加入目标实体的社区
          entityToCommunity.set(rel.source, targetCommunity);
          communities.find(c => c.id === targetCommunity).entities.push(rel.source);
        } else if (sourceCommunity !== targetCommunity) {
          // 合并两个社区
          const sourceComm = communities.find(c => c.id === sourceCommunity);
          const targetComm = communities.find(c => c.id === targetCommunity);
          
          // 将目标社区的所有实体合并到源社区
          for (const entity of targetComm.entities) {
            entityToCommunity.set(entity, sourceCommunity);
          }
          sourceComm.entities = [...new Set([...sourceComm.entities, ...targetComm.entities])];
          sourceComm.relationships = [...new Set([...sourceComm.relationships, ...targetComm.relationships, rel.id || `${rel.source}-${rel.target}`])];
          
          // 移除目标社区
          communities.splice(communities.indexOf(targetComm), 1);
        }
      }
    }
    
    return {
      count: communities.length,
      communities: communities,
      entityToCommunity: Object.fromEntries(entityToCommunity)
    };
  }
  
  assessNetworkHealth(topology, centralities) {
    // 评估网络健康度的综合指标
    const density = topology.density;
    const avgDegree = topology.averageDegree;
    const componentCount = topology.connectedComponents.count;
    
    // 计算健康度分数（0-100）
    let healthScore = 50; // 基础分数
    
    // 密度影响（0.1-0.9的密度范围较健康）
    if (density >= 0.1 && density <= 0.9) {
      healthScore += 20;
    } else if (density > 0) {
      healthScore += 10;
    }
    
    // 平均度影响（每个实体至少有1个连接较健康）
    if (avgDegree >= 1) {
      healthScore += 15;
    }
    
    // 连通分量影响（单一连通分量最健康）
    if (componentCount === 1) {
      healthScore += 15;
    } else if (componentCount <= 3) {
      healthScore += 5;
    }
    
    // 中心性分布影响（不过度中心化较健康）
    const maxCentrality = Math.max(...Object.values(centralities.degree), 0);
    const avgCentrality = Object.values(centralities.degree).reduce((a, b) => a + b, 0) / Object.keys(centralities.degree).length;
    if (maxCentrality <= avgCentrality * 2) { // 没有过度中心化的节点
      healthScore += 10;
    }
    
    return {
      score: Math.min(100, Math.max(0, healthScore)),
      indicators: {
        density: density,
        connectivity: topology.connectedComponents.count,
        averageDegree: avgDegree,
        centralization: maxCentrality > 0 ? maxCentrality / Object.keys(centralities.degree).length : 0
      },
      assessment: this.getHealthAssessment(healthScore)
    };
  }
  
  getHealthAssessment(score) {
    if (score >= 80) return "非常健康 - 网络结构稳定，连接适度";
    if (score >= 60) return "健康 - 网络结构基本稳定";
    if (score >= 40) return "一般 - 网络存在一些结构问题";
    return "不健康 - 网络连接稀疏或过度集中";
  }
}

/**
 * 验证模块
 */
class ValidationModule {
  async validate(analysisResults) {
    const validationResults = {
      dataCompleteness: await this.checkDataCompleteness(analysisResults),
      calculationAccuracy: await this.checkCalculationAccuracy(analysisResults),
      consistency: await this.checkConsistency(analysisResults),
      networkValidity: await this.checkNetworkValidity(analysisResults)
    };
    
    const overallScore = this.calculateOverallScore(validationResults);
    
    return {
      ...analysisResults,
      validation: validationResults,
      overallValidationScore: overallScore
    };
  }
  
  async checkDataCompleteness(results) {
    const sourceData = results.sourceData;
    const relationships = results.relationshipTypes;
    
    const completenessScore = sourceData && relationships ? 100 : 60;
    
    return {
      score: completenessScore,
      level: completenessScore >= 80 ? "high" : completenessScore >= 50 ? "medium" : "low",
      missingElements: sourceData ? [] : ["sourceData"]
    };
  }
  
  async checkCalculationAccuracy(results) {
    // 检查计算结果的准确性
    const issues = [];
    
    // 检查关系强度是否在有效范围内
    if (results.keyRelationships) {
      for (const rel of results.keyRelationships) {
        if (rel.strength < 0 || rel.strength > 1) {
          issues.push(`关系强度超出有效范围: ${rel.strength}`);
        }
      }
    }
    
    return {
      issues: issues,
      accuracyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 10))
    };
  }
  
  async checkConsistency(results) {
    // 检查分析结果的一致性
    const issues = [];
    
    // 检查网络拓扑属性的一致性
    if (results.networkProperties && results.sourceData) {
      const expectedRelCount = results.sourceData.relationships.length;
      const actualRelCount = results.relationshipAnalysis?.analysisSummary?.totalRelationships;
      
      if (expectedRelCount !== actualRelCount) {
        issues.push(`关系数量不一致: 期望${expectedRelCount}, 实际${actualRelCount}`);
      }
    }
    
    return {
      issues: issues,
      consistencyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 15))
    };
  }
  
  async checkNetworkValidity(results) {
    // 检查网络分析结果的有效性
    const issues = [];
    
    if (results.networkProperties?.topology) {
      const topo = results.networkProperties.topology;
      if (topo.density < 0 || topo.density > 1) {
        issues.push(`网络密度超出有效范围: ${topo.density}`);
      }
    }
    
    return {
      issues: issues,
      validityScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 20))
    };
  }
  
  calculateOverallScore(validationResults) {
    const { dataCompleteness, calculationAccuracy, consistency, networkValidity } = validationResults;
    
    // 加权计算总体分数
    const weights = {
      completeness: 0.25,
      accuracy: 0.30,
      consistency: 0.25,
      validity: 0.20
    };
    
    return Math.round(
      (dataCompleteness.score * weights.completeness) +
      (calculationAccuracy.accuracyScore * weights.accuracy) +
      (consistency.consistencyScore * weights.consistency) +
      (networkValidity.validityScore * weights.validity)
    );
  }
}

/**
 * 生态系统报告生成模块
 */
class EcosystemReportingModule {
  async generate(analysisResults, depth = 'standard') {
    const report = {
      relationshipAnalysis: this.createRelationshipAnalysisReport(analysisResults),
      ecosystemHealth: this.createEcosystemHealthReport(analysisResults),
      recommendations: await this.generateRecommendations(analysisResults),
      metadata: {
        generationTime: new Date().toISOString(),
        validationScore: analysisResults.overallValidationScore,
        detailLevel: depth
      }
    };
    
    // 根据深度添加额外信息
    if (depth === 'comprehensive') {
      report.detailedAnalysis = {
        networkProperties: analysisResults.networkProperties,
        entityCentralities: analysisResults.networkProperties?.centralities,
        communityStructure: analysisResults.networkProperties?.communities
      };
    }
    
    return report;
  }
  
  createRelationshipAnalysisReport(results) {
    return {
      summary: results.relationshipAnalysis.analysisSummary,
      relationshipTypes: results.relationshipAnalysis.relationshipTypes,
      keyRelationships: results.relationshipAnalysis.keyRelationships,
      networkCharacteristics: results.networkProperties
    };
  }
  
  createEcosystemHealthReport(results) {
    return {
      overallHealth: results.networkProperties.health,
      structuralIndicators: {
        connectivity: results.networkProperties.topology.connectedComponents,
        density: results.networkProperties.topology.density,
        centralization: results.networkProperties.health.indicators.centralization
      },
      stabilityFactors: this.extractStabilityFactors(results)
    };
  }
  
  extractStabilityFactors(results) {
    // 从分析结果中提取稳定性因素
    const factors = [];
    
    if (results.relationshipAnalysis.relationshipTypes) {
      for (const [type, data] of Object.entries(results.relationshipAnalysis.relationshipTypes)) {
        factors.push({
          type: type,
          count: data.count,
          avgStrength: data.avgStrength,
          stabilityIndicators: data.characteristics?.stabilityFactors || {}
        });
      }
    }
    
    return factors;
  }
  
  async generateRecommendations(results) {
    const recommendations = [];
    
    // 基于网络健康度的建议
    const health = results.networkProperties.health;
    if (health.score < 60) {
      recommendations.push("网络连接性不足，建议加强实体间的合作关系");
    }
    
    // 基于中心性的建议
    const centralities = results.networkProperties.centralities;
    const maxDegree = Math.max(...Object.values(centralities.degree));
    const avgDegree = Object.values(centralities.degree).reduce((a, b) => a + b, 0) / Object.keys(centralities.degree).length;
    
    if (maxDegree > avgDegree * 3) {
      recommendations.push("网络过度依赖少数中心节点，建议分散风险");
    }
    
    // 基于连通分量的建议
    const components = results.networkProperties.topology.connectedComponents;
    if (components.count > 1) {
      recommendations.push(`网络存在${components.count}个独立子网，建议加强跨子网连接`);
    }
    
    // 基于关系类型的建议
    const relationshipTypes = results.relationshipAnalysis.relationshipTypes;
    if (relationshipTypes.competition && relationshipTypes.cooperation) {
      const compCount = relationshipTypes.competition.count || 0;
      const coopCount = relationshipTypes.cooperation.count || 0;
      
      if (compCount > coopCount * 2) {
        recommendations.push("竞争关系过多，建议促进更多合作关系以增强生态稳定性");
      }
    }
    
    return recommendations.length > 0 ? recommendations : [
      "生态系统整体结构健康，继续保持当前发展策略"
    ];
  }
}

// 导出技能类
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EcosystemRelationshipAnalysisSkill;
}