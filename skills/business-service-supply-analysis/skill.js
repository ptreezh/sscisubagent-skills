/**
 * 业务服务供给关系分析技能实现
 * 遵循agentskills.io规范和渐进式披露原则
 */

class BusinessServiceSupplyAnalysisSkill {
  constructor() {
    this.skillId = "business-service-supply-analysis";
    this.version = "2.0.0";
    this.name = "业务服务供给关系分析";
    this.description = "专门分析商业生态系统中业务服务供给关系的技能";
    
    // 初始化模块
    this.dataProcessor = new ServiceSupplyDataProcessor();
    this.supplyChainAnalyzer = new SupplyChainAnalysisModule();
    this.valueFlowAnalyzer = new ValueFlowAnalysisModule();
    this.resourceAnalyzer = new ResourceAllocationModule();
    this.efficiencyAnalyzer = new ProcessEfficiencyModule();
    this.validator = new ValidationModule();
    this.reporter = new ServiceSupplyReportingModule();
  }

  /**
   * 执行技能主方法
   * 实现渐进式披露：根据analysisDepth参数决定分析详略程度
   */
  async execute(inputs) {
    try {
      // 验证输入参数
      this.validateInputs(inputs);
      
      // 处理服务供给数据
      const processedData = await this.dataProcessor.process(inputs);
      
      // 执行各种分析
      const focusAreas = inputs.focusAreas || ['all'];
      const depth = inputs.analysisDepth || 'standard';
      
      const analysisResults = {};
      
      if (focusAreas.includes('all') || focusAreas.includes('supply-chain')) {
        analysisResults.supplyChainAnalysis = await this.supplyChainAnalyzer.analyze(
          processedData.entities, 
          processedData.supplyRelationships,
          depth
        );
      }
      
      if (focusAreas.includes('all') || focusAreas.includes('value-flow')) {
        analysisResults.valueFlowAnalysis = await this.valueFlowAnalyzer.analyze(
          processedData.entities, 
          processedData.services, 
          processedData.supplyRelationships,
          depth
        );
      }
      
      if (focusAreas.includes('all') || focusAreas.includes('resource-allocation')) {
        analysisResults.resourceAllocation = await this.resourceAnalyzer.analyze(
          processedData.entities, 
          processedData.services, 
          processedData.supplyRelationships,
          depth
        );
      }
      
      if (focusAreas.includes('all') || focusAreas.includes('process-efficiency')) {
        analysisResults.processEfficiency = await this.efficiencyAnalyzer.analyze(
          processedData.entities, 
          processedData.supplyRelationships,
          depth
        );
      }
      
      // 分析供需平衡
      analysisResults.supplyDemandBalance = await this.analyzeSupplyDemandBalance(
        processedData.entities, 
        processedData.services, 
        processedData.supplyRelationships
      );
      
      // 验证结果
      const validatedResults = await this.validator.validate({
        ...analysisResults,
        sourceData: processedData
      });
      
      // 生成报告
      const finalReport = await this.reporter.generate(
        validatedResults, 
        depth
      );
      
      return {
        success: true,
        data: finalReport,
        metadata: {
          skillId: this.skillId,
          version: this.version,
          executionTime: new Date().toISOString(),
          contextLevel: depth
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
    if (!inputs || !inputs.entities || !inputs.services || !inputs.supplyRelationships) {
      throw new Error("缺少必需的entities、services或supplyRelationships参数");
    }
    
    if (!Array.isArray(inputs.entities) || !Array.isArray(inputs.services) || !Array.isArray(inputs.supplyRelationships)) {
      throw new Error("entities、services和supplyRelationships必须是数组");
    }
  }
  
  /**
   * 分析供需平衡
   */
  async analyzeSupplyDemandBalance(entities, services, relationships) {
    // 计算供给和需求的平衡
    const supplyByProvider = {};
    const demandByConsumer = {};
    
    for (const rel of relationships) {
      // 记录供给
      supplyByProvider[rel.provider] = (supplyByProvider[rel.provider] || 0) + (rel.quantity || 1);
      
      // 记录需求
      demandByConsumer[rel.consumer] = (demandByConsumer[rel.consumer] || 0) + (rel.quantity || 1);
    }
    
    // 识别供需不平衡
    const imbalances = [];
    
    // 检查供给方
    for (const entity of entities) {
      const totalSupply = supplyByProvider[entity.id] || 0;
      if (totalSupply === 0 && entity.type === 'provider') {
        imbalances.push({
          entity: entity.id,
          type: 'underutilized-provider',
          description: `${entity.name}作为服务提供商但没有提供服务`
        });
      }
    }
    
    // 检查需求方
    for (const entity of entities) {
      const totalDemand = demandByConsumer[entity.id] || 0;
      if (totalDemand === 0 && entity.type === 'consumer') {
        imbalances.push({
          entity: entity.id,
          type: 'unmet-consumer',
          description: `${entity.name}作为服务消费者但没有获得服务`
        });
      }
    }
    
    // 计算供需比率
    const supplyTotal = Object.values(supplyByProvider).reduce((a, b) => a + b, 0);
    const demandTotal = Object.values(demandByConsumer).reduce((a, b) => a + b, 0);
    const balanceRatio = demandTotal > 0 ? supplyTotal / demandTotal : 0;
    
    return {
      supplyByProvider: supplyByProvider,
      demandByConsumer: demandByConsumer,
      balanceRatio: balanceRatio,
      balanceState: this.getBalanceState(balanceRatio),
      imbalances: imbalances,
      totalSupply: supplyTotal,
      totalDemand: demandTotal
    };
  }
  
  getBalanceState(ratio) {
    if (ratio > 1.2) return 'supply-excess';
    if (ratio < 0.8) return 'supply-deficit';
    return 'balanced';
  }
}

/**
 * 服务供给数据处理器
 * 程序化执行数据预处理任务
 */
class ServiceSupplyDataProcessor {
  async process(inputs) {
    const entities = this.processEntities(inputs.entities);
    const services = this.processServices(inputs.services, entities);
    const relationships = this.processRelationships(inputs.supplyRelationships, entities, services);
    
    return {
      entities: entities,
      services: services,
      supplyRelationships: relationships,
      processedTimestamp: new Date().toISOString()
    };
  }
  
  processEntities(rawEntities) {
    // 标准化实体数据
    return rawEntities.map(entity => ({
      id: entity.id,
      name: entity.name || '未知实体',
      type: entity.type || 'unknown',
      capabilities: entity.capabilities || [],
      serviceCapacity: this.estimateServiceCapacity(entity)
    }));
  }
  
  processServices(rawServices, entities) {
    // 标准化服务数据并关联提供商
    return rawServices.map(service => {
      const provider = entities.find(e => e.id === service.provider);
      
      return {
        id: service.id,
        name: service.name || '未知服务',
        type: service.type || 'unknown',
        provider: service.provider,
        providerName: provider ? provider.name : '未知提供商',
        complexity: this.estimateServiceComplexity(service)
      };
    });
  }
  
  processRelationships(rawRelationships, entities, services) {
    // 标准化关系数据并添加衍生属性
    return rawRelationships.map(rel => {
      const provider = entities.find(e => e.id === rel.provider);
      const consumer = entities.find(e => e.id === rel.consumer);
      const service = services.find(s => s.id === rel.service);
      
      return {
        provider: rel.provider,
        consumer: rel.consumer,
        service: rel.service,
        quantity: rel.quantity || 1,
        quality: rel.quality || 0.7, // 默认中等质量
        providerName: provider ? provider.name : '未知',
        consumerName: consumer ? consumer.name : '未知',
        serviceName: service ? service.name : '未知',
        value: this.calculateValue(rel.quantity, rel.quality),
        efficiency: this.calculateEfficiency(rel)
      };
    });
  }
  
  estimateServiceCapacity(entity) {
    // 基于实体能力和资源估算服务容量
    const baseCapacity = entity.capabilities ? entity.capabilities.length * 10 : 5;
    return Math.max(1, baseCapacity);
  }
  
  estimateServiceComplexity(service) {
    // 估算服务复杂度
    return 0.5; // 默认中等复杂度
  }
  
  calculateValue(quantity, quality) {
    // 计算服务价值
    return (quantity || 1) * (quality || 0.7);
  }
  
  calculateEfficiency(rel) {
    // 计算服务提供效率
    return (rel.quality || 0.7) / (rel.quantity || 1);
  }
}

/**
 * 供应链分析模块
 */
class SupplyChainAnalysisModule {
  async analyze(entities, relationships, depth = 'standard') {
    // 构建供应链网络
    const network = this.buildSupplyNetwork(relationships);
    
    // 分析供应链结构
    const structure = this.analyzeStructure(network, entities);
    
    // 评估供应链韧性
    const resilience = this.assessResilience(network, entities);
    
    // 深度分析
    let detailedAnalysis = {};
    if (depth === 'comprehensive') {
      detailedAnalysis = {
        bottlenecks: this.identifyBottlenecks(network),
        alternatives: this.assessAlternatives(network),
        risks: this.assessRisks(network)
      };
    }
    
    return {
      network: network,
      structure: structure,
      resilience: resilience,
      efficiency: this.calculateEfficiency(relationships),
      ...(depth === 'comprehensive' ? detailedAnalysis : {})
    };
  }
  
  buildSupplyNetwork(relationships) {
    const network = {
      nodes: new Set(),
      edges: [],
      adjacency: {},
      reverseAdjacency: {}
    };
    
    for (const rel of relationships) {
      network.nodes.add(rel.provider);
      network.nodes.add(rel.consumer);
      
      network.edges.push({
        from: rel.provider,
        to: rel.consumer,
        service: rel.service,
        quantity: rel.quantity,
        quality: rel.quality
      });
      
      // 构建邻接表
      if (!network.adjacency[rel.provider]) {
        network.adjacency[rel.provider] = [];
      }
      network.adjacency[rel.provider].push({
        to: rel.consumer,
        service: rel.service,
        quantity: rel.quantity
      });
      
      // 构建反向邻接表
      if (!network.reverseAdjacency[rel.consumer]) {
        network.reverseAdjacency[rel.consumer] = [];
      }
      network.reverseAdjacency[rel.consumer].push({
        from: rel.provider,
        service: rel.service,
        quantity: rel.quantity
      });
    }
    
    return network;
  }
  
  analyzeStructure(network, entities) {
    // 分析供应链结构特征
    const nodeCount = network.nodes.size;
    const edgeCount = network.edges.length;
    
    // 计算每个节点的度数
    const degrees = {};
    for (const node of network.nodes) {
      const outDegree = (network.adjacency[node] || []).length;
      const inDegree = (network.reverseAdjacency[node] || []).length;
      degrees[node] = { in: inDegree, out: outDegree, total: inDegree + outDegree };
    }
    
    // 识别关键节点
    const keyNodes = Object.entries(degrees)
      .sort((a, b) => b[1].total - a[1].total)
      .slice(0, 5)
      .map(([nodeId, degree]) => {
        const entity = entities.find(e => e.id === nodeId);
        return {
          id: nodeId,
          name: entity ? entity.name : '未知',
          degrees: degree,
          type: entity ? entity.type : 'unknown'
        };
      });
    
    return {
      nodeCount: nodeCount,
      edgeCount: edgeCount,
      density: nodeCount > 1 ? edgeCount / (nodeCount * (nodeCount - 1)) : 0,
      averagePathLength: this.estimateAveragePathLength(network),
      keyNodes: keyNodes,
      degrees: degrees
    };
  }
  
  estimateAveragePathLength(network) {
    // 估算平均路径长度（简化计算）
    const nodes = Array.from(network.nodes);
    if (nodes.length < 2) return 0;
    
    // 简化的估算：基于网络密度
    const density = network.edges.length / (nodes.length * (nodes.length - 1));
    return Math.max(1, Math.round(1 / Math.max(density, 0.1)));
  }
  
  assessResilience(network, entities) {
    // 评估供应链韧性
    const resilienceFactors = {
      diversification: this.calculateDiversificationScore(network, entities),
      flexibility: this.calculateFlexibilityScore(network),
      redundancy: this.calculateRedundancyScore(network)
    };
    
    const overallResilience = (resilienceFactors.diversification + 
                              resilienceFactors.flexibility + 
                              resilienceFactors.redundancy) / 3;
    
    return {
      ...resilienceFactors,
      overallScore: overallResilience,
      level: overallResilience > 0.7 ? 'high' : overallResilience > 0.4 ? 'medium' : 'low'
    };
  }
  
  calculateDiversificationScore(network, entities) {
    // 计算多样化分数
    let totalDiversity = 0;
    let entityCount = 0;
    
    for (const entity of entities) {
      if (entity.type === 'provider') {
        const outgoingRelationships = network.adjacency[entity.id] || [];
        const uniqueServices = new Set(outgoingRelationships.map(rel => rel.service));
        const diversity = uniqueServices.size / Math.max(1, outgoingRelationships.length);
        totalDiversity += diversity;
        entityCount++;
      }
    }
    
    return entityCount > 0 ? totalDiversity / entityCount : 0.5;
  }
  
  calculateFlexibilityScore(network) {
    // 计算灵活性分数
    // 基于节点的替代路径数量
    const flexibility = Object.keys(network.adjacency).length / network.nodes.size;
    return Math.min(1.0, flexibility);
  }
  
  calculateRedundancyScore(network) {
    // 计算冗余度分数
    // 基于是否存在多个路径提供相同服务
    let redundantConnections = 0;
    let totalConnections = network.edges.length;
    
    // 简单的冗余评估：检查是否有多个供应商提供给同一消费者
    const consumerSuppliers = {};
    for (const edge of network.edges) {
      if (!consumerSuppliers[edge.to]) {
        consumerSuppliers[edge.to] = new Set();
      }
      consumerSuppliers[edge.to].add(edge.from);
    }
    
    for (const suppliers of Object.values(consumerSuppliers)) {
      if (suppliers.size > 1) {
        redundantConnections += 1;
      }
    }
    
    return totalConnections > 0 ? redundantConnections / Object.keys(consumerSuppliers).length : 0;
  }
  
  identifyBottlenecks(network) {
    // 识别供应链瓶颈
    const bottlenecks = [];
    
    for (const nodeId in network.adjacency) {
      const outgoing = network.adjacency[nodeId] || [];
      const incoming = network.reverseAdjacency[nodeId] || [];
      
      // 如果某个节点的输出远大于输入，可能是瓶颈
      if (outgoing.length > 3 && incoming.length < 2) {
        bottlenecks.push({
          nodeId: nodeId,
          type: 'supply-bottleneck',
          reason: '输出连接过多，输入连接过少'
        });
      }
    }
    
    return bottlenecks;
  }
  
  assessAlternatives(network) {
    // 评估替代方案
    const alternatives = [];
    
    for (const consumerId in network.reverseAdjacency) {
      const suppliers = network.reverseAdjacency[consumerId];
      if (suppliers.length < 2) {
        alternatives.push({
          consumer: consumerId,
          type: 'low-alternatives',
          supplierCount: suppliers.length,
          recommendation: '增加供应商多样性'
        });
      }
    }
    
    return alternatives;
  }
  
  assessRisks(network) {
    // 评估供应链风险
    const risks = [];
    
    // 高度依赖单个供应商的风险
    for (const consumerId in network.reverseAdjacency) {
      const suppliers = network.reverseAdjacency[consumerId];
      if (suppliers.length === 1) {
        risks.push({
          type: 'single-supplier-risk',
          affected: consumerId,
          description: '高度依赖单一供应商'
        });
      }
    }
    
    return risks;
  }
  
  calculateEfficiency(relationships) {
    // 计算供应链效率
    if (relationships.length === 0) return 0;
    
    const avgQuality = relationships.reduce((sum, rel) => sum + (rel.quality || 0.7), 0) / relationships.length;
    const avgEfficiency = relationships.reduce((sum, rel) => sum + (rel.quantity > 0 ? (rel.quality || 0.7) / rel.quantity : 0.7), 0) / relationships.length;
    
    return (avgQuality + avgEfficiency) / 2;
  }
}

/**
 * 价值流分析模块
 */
class ValueFlowAnalysisModule {
  async analyze(entities, services, relationships, depth = 'standard') {
    // 计算价值流
    const valueFlows = this.calculateValueFlows(entities, services, relationships);
    
    // 分析价值创造和传递
    const valueCreation = this.analyzeValueCreation(entities, services, relationships);
    
    // 评估价值流效率
    const efficiency = this.assessValueFlowEfficiency(entities, relationships);
    
    // 深度分析
    let detailedAnalysis = {};
    if (depth === 'comprehensive') {
      detailedAnalysis = {
        valueLeakage: this.identifyValueLeakage(entities, relationships),
        optimizationPoints: this.identifyOptimizationPoints(entities, relationships),
        valueAddedAnalysis: this.performValueAddedAnalysis(entities, relationships)
      };
    }
    
    return {
      valueFlows: valueFlows,
      valueCreation: valueCreation,
      efficiency: efficiency,
      ...(depth === 'comprehensive' ? detailedAnalysis : {})
    };
  }
  
  calculateValueFlows(entities, services, relationships) {
    // 计算价值流：跟踪价值从上游到下游的流动
    const valueByEntity = {};
    const valueByService = {};
    
    for (const rel of relationships) {
      const value = (rel.quantity || 1) * (rel.quality || 0.7);
      
      // 按实体记录价值流
      valueByEntity[rel.provider] = (valueByEntity[rel.provider] || 0) + value;
      valueByEntity[rel.consumer] = (valueByEntity[rel.consumer] || 0) + value;
      
      // 按服务记录价值流
      valueByService[rel.service] = (valueByService[rel.service] || 0) + value;
    }
    
    return {
      byEntity: valueByEntity,
      byService: valueByService,
      totalValue: Object.values(valueByEntity).reduce((a, b) => a + b, 0) / 2 // 除以2避免重复计算
    };
  }
  
  analyzeValueCreation(entities, services, relationships) {
    // 分析价值创造点
    const creationPoints = [];
    
    for (const entity of entities) {
      const entityRelationships = relationships.filter(
        rel => rel.provider === entity.id
      );
      
      if (entityRelationships.length > 0) {
        const totalValue = entityRelationships.reduce(
          (sum, rel) => sum + ((rel.quantity || 1) * (rel.quality || 0.7)), 
          0
        );
        
        creationPoints.push({
          entity: entity.id,
          name: entity.name,
          type: entity.type,
          totalValue: totalValue,
          serviceCount: entityRelationships.length
        });
      }
    }
    
    // 按价值排序
    creationPoints.sort((a, b) => b.totalValue - a.totalValue);
    
    return {
      primaryCreationPoints: creationPoints.slice(0, 5),
      totalValueCreated: creationPoints.reduce((sum, point) => sum + point.totalValue, 0),
      valueCreationDistribution: creationPoints
    };
  }
  
  assessValueFlowEfficiency(entities, relationships) {
    // 评估价值流效率
    if (relationships.length === 0) return 0.5;
    
    // 计算平均质量水平
    const avgQuality = relationships.reduce((sum, rel) => sum + (rel.quality || 0.7), 0) / relationships.length;
    
    // 计算价值转化效率
    let totalInputValue = 0;
    let totalOutputValue = 0;
    
    for (const rel of relationships) {
      // 假设消费者获得的价值 = 提供者投入的价值 * 质量因子
      totalInputValue += (rel.quantity || 1);
      totalOutputValue += (rel.quantity || 1) * (rel.quality || 0.7);
    }
    
    const transformationEfficiency = totalInputValue > 0 ? totalOutputValue / totalInputValue : 1.0;
    
    // 综合效率 = 平均质量 * 转化效率
    return (avgQuality * 0.6 + transformationEfficiency * 0.4);
  }
  
  identifyValueLeakage(entities, relationships) {
    // 识别价值流失点
    const leakagePoints = [];
    
    for (const entity of entities) {
      const outgoing = relationships.filter(rel => rel.provider === entity.id);
      const incoming = relationships.filter(rel => rel.consumer === entity.id);
      
      const outgoingValue = outgoing.reduce((sum, rel) => sum + (rel.quantity || 1) * (rel.quality || 0.7), 0);
      const incomingValue = incoming.reduce((sum, rel) => sum + (rel.quantity || 1) * (rel.quality || 0.7), 0);
      
      const netValue = outgoingValue - incomingValue;
      
      if (netValue < 0) { // 价值流入大于流出，可能是价值消耗点
        leakagePoints.push({
          entity: entity.id,
          type: 'value-consumer',
          netValue: netValue,
          description: `${entity.name}是价值消费者，净消耗${Math.abs(netValue).toFixed(2)}单位价值`
        });
      } else if (netValue > incomingValue * 2) { // 提供的价值远超获得的价值
        leakagePoints.push({
          entity: entity.id,
          type: 'value-producer',
          netValue: netValue,
          description: `${entity.name}是价值生产者，净产生${netValue.toFixed(2)}单位价值`
        });
      }
    }
    
    return leakagePoints;
  }
  
  identifyOptimizationPoints(entities, relationships) {
    // 识别优化点
    const optimizationPoints = [];
    
    // 低质量服务
    for (const rel of relationships) {
      if (rel.quality < 0.5) {
        optimizationPoints.push({
          type: 'low-quality-service',
          relationship: rel,
          recommendation: '提升服务质量或替换服务提供商'
        });
      }
    }
    
    return optimizationPoints;
  }
  
  performValueAddedAnalysis(entities, relationships) {
    // 执行增值分析
    const addedValue = {};
    
    for (const entity of entities) {
      const provided = relationships.filter(rel => rel.provider === entity.id);
      const consumed = relationships.filter(rel => rel.consumer === entity.id);
      
      const providedValue = provided.reduce((sum, rel) => sum + (rel.quantity || 1) * (rel.quality || 0.7), 0);
      const consumedValue = consumed.reduce((sum, rel) => sum + (rel.quantity || 1) * (rel.quality || 0.7), 0);
      
      addedValue[entity.id] = {
        provided: providedValue,
        consumed: consumedValue,
        netAddedValue: providedValue - consumedValue
      };
    }
    
    return addedValue;
  }
}

/**
 * 资源分配分析模块
 */
class ResourceAllocationModule {
  async analyze(entities, services, relationships, depth = 'standard') {
    // 分析资源分配效率
    const allocationEfficiency = this.assessAllocationEfficiency(entities, services, relationships);
    
    // 识别资源瓶颈
    const bottlenecks = this.identifyResourceBottlenecks(entities, relationships);
    
    // 分析资源配置均衡性
    const balance = this.assessResourceBalance(entities, relationships);
    
    // 深度分析
    let detailedAnalysis = {};
    if (depth === 'comprehensive') {
      detailedAnalysis = {
        capacityUtilization: this.calculateCapacityUtilization(entities, relationships),
        allocationOptimization: this.suggestAllocationOptimizations(entities, relationships),
        resourceConstraints: this.identifyResourceConstraints(entities, relationships)
      };
    }
    
    return {
      allocationEfficiency: allocationEfficiency,
      bottlenecks: bottlenecks,
      balance: balance,
      ...(depth === 'comprehensive' ? detailedAnalysis : {})
    };
  }
  
  assessAllocationEfficiency(entities, services, relationships) {
    // 评估资源分配效率
    const providerUtilization = {};
    
    for (const entity of entities) {
      if (entity.type === 'provider') {
        const providedServices = relationships.filter(rel => rel.provider === entity.id);
        const totalCapacity = entity.serviceCapacity || 10;
        const actualUtilization = providedServices.length;
        
        providerUtilization[entity.id] = {
          capacity: totalCapacity,
          utilization: actualUtilization,
          efficiency: totalCapacity > 0 ? actualUtilization / totalCapacity : 0,
          optimal: actualUtilization <= totalCapacity
        };
      }
    }
    
    // 计算整体效率
    const efficiencies = Object.values(providerUtilization).map(p => p.efficiency);
    const avgEfficiency = efficiencies.length > 0 ? 
      efficiencies.reduce((a, b) => a + b, 0) / efficiencies.length : 0.5;
    
    return {
      byProvider: providerUtilization,
      averageEfficiency: avgEfficiency,
      efficiencyLevel: avgEfficiency > 0.8 ? 'high' : avgEfficiency > 0.5 ? 'medium' : 'low'
    };
  }
  
  identifyResourceBottlenecks(entities, relationships) {
    // 识别资源瓶颈
    const bottlenecks = [];
    
    for (const entity of entities) {
      if (entity.type === 'provider') {
        const incoming = relationships.filter(rel => rel.consumer === entity.id); // 依赖此提供商的连接
        const outgoing = relationships.filter(rel => rel.provider === entity.id); // 该提供商提供的服务
        
        if (incoming.length > outgoing.length * 2) {
          bottlenecks.push({
            entity: entity.id,
            type: 'demand-bottleneck',
            description: `${entity.name}作为提供商，服务需求(${incoming.length})远超服务提供能力(${outgoing.length})`
          });
        }
      }
    }
    
    return bottlenecks;
  }
  
  assessResourceBalance(entities, relationships) {
    // 评估资源配置均衡性
    const providerLoad = {};
    const consumerLoad = {};
    
    for (const entity of entities) {
      if (entity.type === 'provider') {
        const provided = relationships.filter(rel => rel.provider === entity.id);
        providerLoad[entity.id] = {
          entity: entity.id,
          load: provided.length,
          name: entity.name
        };
      } else if (entity.type === 'consumer') {
        const consumed = relationships.filter(rel => rel.consumer === entity.id);
        consumerLoad[entity.id] = {
          entity: entity.id,
          load: consumed.length,
          name: entity.name
        };
      }
    }
    
    // 计算负载均衡度
    const providerLoads = Object.values(providerLoad).map(p => p.load);
    const consumerLoads = Object.values(consumerLoad).map(c => c.load);
    
    const providerBalance = this.calculateBalance(providerLoads);
    const consumerBalance = this.calculateBalance(consumerLoads);
    
    return {
      providerBalance: providerBalance,
      consumerBalance: consumerBalance,
      overallBalance: (providerBalance + consumerBalance) / 2
    };
  }
  
  calculateBalance(loads) {
    if (loads.length <= 1) return 1.0;
    
    const avg = loads.reduce((a, b) => a + b, 0) / loads.length;
    if (avg === 0) return 1.0;
    
    const variance = loads.reduce((a, b) => a + Math.pow(b - avg, 2), 0) / loads.length;
    const coefficientOfVariation = Math.sqrt(variance) / avg;
    
    // 变异系数越小，均衡度越高
    return Math.max(0, 1 - coefficientOfVariation);
  }
  
  calculateCapacityUtilization(entities, relationships) {
    // 计算容量利用率
    const utilization = {};
    
    for (const entity of entities) {
      const providedServices = relationships.filter(rel => rel.provider === entity.id);
      const capacity = entity.serviceCapacity || 10;
      const utilizationRate = capacity > 0 ? providedServices.length / capacity : 0;
      
      utilization[entity.id] = {
        entity: entity.id,
        name: entity.name,
        capacity: capacity,
        utilized: providedServices.length,
        rate: utilizationRate,
        status: utilizationRate > 1.0 ? 'overloaded' : utilizationRate > 0.8 ? 'high' : 'normal'
      };
    }
    
    return utilization;
  }
  
  suggestAllocationOptimizations(entities, relationships) {
    // 建议分配优化
    const suggestions = [];
    
    // 过载的提供商
    for (const entity of entities) {
      const provided = relationships.filter(rel => rel.provider === entity.id);
      const capacity = entity.serviceCapacity || 10;
      
      if (provided.length > capacity) {
        suggestions.push({
          type: 'overloaded-provider',
          entity: entity.id,
          currentLoad: provided.length,
          capacity: capacity,
          recommendation: `增加${entity.name}的服务容量或重新分配部分服务`
        });
      }
    }
    
    // 未充分利用的提供商
    for (const entity of entities) {
      if (entity.type === 'provider') {
        const provided = relationships.filter(rel => rel.provider === entity.id);
        const capacity = entity.serviceCapacity || 10;
        
        if (provided.length < capacity * 0.3) {
          suggestions.push({
            type: 'underutilized-provider',
            entity: entity.id,
            currentLoad: provided.length,
            capacity: capacity,
            recommendation: `提高${entity.name}的利用率或考虑减少容量`
          });
        }
      }
    }
    
    return suggestions;
  }
  
  identifyResourceConstraints(entities, relationships) {
    // 识别资源约束
    const constraints = [];
    
    // 供应商容量约束
    for (const entity of entities) {
      if (entity.type === 'provider') {
        const provided = relationships.filter(rel => rel.provider === entity.id);
        const capacity = entity.serviceCapacity || 10;
        
        if (provided.length >= capacity) {
          constraints.push({
            type: 'capacity-constraint',
            entity: entity.id,
            constraint: 'service-capacity',
            current: provided.length,
            limit: capacity,
            description: `${entity.name}已达到服务容量上限`
          });
        }
      }
    }
    
    return constraints;
  }
}

/**
 * 流程效率分析模块
 */
class ProcessEfficiencyModule {
  async analyze(entities, relationships, depth = 'standard') {
    // 分析流程效率指标
    const efficiencyMetrics = this.calculateEfficiencyMetrics(entities, relationships);
    
    // 识别效率瓶颈
    const bottlenecks = this.identifyEfficiencyBottlenecks(entities, relationships);
    
    // 评估流程优化潜力
    const optimizationPotential = this.assessOptimizationPotential(entities, relationships);
    
    // 深度分析
    let detailedAnalysis = {};
    if (depth === 'comprehensive') {
      detailedAnalysis = {
        processFlowAnalysis: this.analyzeProcessFlow(entities, relationships),
        performanceIndicators: this.calculatePerformanceIndicators(relationships),
        efficiencyTrends: this.assessEfficiencyTrends(relationships)
      };
    }
    
    return {
      efficiencyMetrics: efficiencyMetrics,
      bottlenecks: bottlenecks,
      optimizationPotential: optimizationPotential,
      ...(depth === 'comprehensive' ? detailedAnalysis : {})
    };
  }
  
  calculateEfficiencyMetrics(entities, relationships) {
    // 计算效率指标
    if (relationships.length === 0) return { averageQuality: 0.7, averageEfficiency: 0.5 };
    
    const avgQuality = relationships.reduce((sum, rel) => sum + (rel.quality || 0.7), 0) / relationships.length;
    const avgEfficiency = relationships.reduce((sum, rel) => sum + this.calculateSingleEfficiency(rel), 0) / relationships.length;
    
    return {
      averageQuality: avgQuality,
      averageEfficiency: avgEfficiency,
      totalRelationships: relationships.length,
      efficiencyScore: (avgQuality * 0.6 + avgEfficiency * 0.4)
    };
  }
  
  calculateSingleEfficiency(rel) {
    // 计算单个关系的效率
    return (rel.quality || 0.7) / Math.max(1, rel.quantity || 1);
  }
  
  identifyEfficiencyBottlenecks(entities, relationships) {
    // 识别效率瓶颈
    const bottlenecks = [];
    
    // 低质量关系
    for (const rel of relationships) {
      if (rel.quality < 0.4) {
        bottlenecks.push({
          type: 'low-quality-relationship',
          relationship: rel,
          efficiency: rel.quality,
          description: `低质量服务关系：${rel.providerName} -> ${rel.consumerName}`
        });
      }
    }
    
    // 高负载节点
    const loadByEntity = {};
    for (const rel of relationships) {
      loadByEntity[rel.provider] = (loadByEntity[rel.provider] || 0) + 1;
      loadByEntity[rel.consumer] = (loadByEntity[rel.consumer] || 0) + 1;
    }
    
    for (const [entityId, load] of Object.entries(loadByEntity)) {
      if (load > relationships.length * 0.2) { // 承担超过20%的负载
        const entity = entities.find(e => e.id === entityId);
        bottlenecks.push({
          type: 'high-load-entity',
          entity: entityId,
          load: load,
          description: `${entity?.name || entityId}承担过高负载(${load}/${relationships.length})`
        });
      }
    }
    
    return bottlenecks;
  }
  
  assessOptimizationPotential(entities, relationships) {
    // 评估优化潜力
    const avgEfficiency = relationships.length > 0 ? 
      relationships.reduce((sum, rel) => sum + (rel.quality || 0.7), 0) / relationships.length : 0.7;
    
    const potential = Math.min(1.0, (1.0 - avgEfficiency) * 2); // 假设可以提升到接近1.0
    
    return {
      currentLevel: avgEfficiency,
      potentialImprovement: potential,
      optimizationPriority: potential > 0.5 ? 'high' : potential > 0.2 ? 'medium' : 'low'
    };
  }
  
  analyzeProcessFlow(entities, relationships) {
    // 分析流程流
    const flowAnalysis = {
      entryPoints: [],
      exitPoints: [],
      intermediatePoints: [],
      flowPaths: []
    };
    
    const providers = new Set(relationships.map(rel => rel.provider));
    const consumers = new Set(relationships.map(rel => rel.consumer));
    
    // 找出只提供不消费的实体（入口）
    for (const provider of providers) {
      if (!consumers.has(provider)) {
        flowAnalysis.entryPoints.push(provider);
      }
    }
    
    // 找出只消费不提供的实体（出口）
    for (const consumer of consumers) {
      if (!providers.has(consumer)) {
        flowAnalysis.exitPoints.push(consumer);
      }
    }
    
    // 找出既提供又消费的实体（中间）
    for (const entity of entities) {
      if (providers.has(entity.id) && consumers.has(entity.id)) {
        flowAnalysis.intermediatePoints.push(entity.id);
      }
    }
    
    return flowAnalysis;
  }
  
  calculatePerformanceIndicators(relationships) {
    // 计算性能指标
    return {
      qualityIndicator: relationships.length > 0 ? 
        relationships.reduce((sum, rel) => sum + (rel.quality || 0.7), 0) / relationships.length : 0.7,
      quantityIndicator: relationships.length,
      valueIndicator: relationships.length > 0 ? 
        relationships.reduce((sum, rel) => sum + ((rel.quantity || 1) * (rel.quality || 0.7)), 0) : 0,
      efficiencyIndicator: relationships.length > 0 ? 
        relationships.reduce((sum, rel) => sum + this.calculateSingleEfficiency(rel), 0) / relationships.length : 0.5
    };
  }
  
  assessEfficiencyTrends(relationships) {
    // 评估效率趋势（在有时间维度数据时更有意义）
    // 当前基于质量分布进行简单评估
    const highQuality = relationships.filter(rel => (rel.quality || 0) >= 0.8).length;
    const lowQuality = relationships.filter(rel => (rel.quality || 0) < 0.5).length;
    
    return {
      highQualityRatio: relationships.length > 0 ? highQuality / relationships.length : 0,
      lowQualityRatio: relationships.length > 0 ? lowQuality / relationships.length : 0,
      overallTrend: highQuality > lowQuality * 2 ? 'improving' : lowQuality > highQuality ? 'declining' : 'stable'
    };
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
      efficiencyValidity: await this.checkEfficiencyValidity(analysisResults)
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
    const hasRequiredData = sourceData && sourceData.entities && sourceData.services && sourceData.supplyRelationships;
    
    return {
      score: hasRequiredData ? 100 : 40,
      level: hasRequiredData ? "high" : "low",
      missingElements: hasRequiredData ? [] : ["sourceData", "entities", "services", "relationships"]
    };
  }
  
  async checkCalculationAccuracy(results) {
    const issues = [];
    
    // 检查效率分数是否在有效范围内
    if (results.supplyChainAnalysis?.efficiency != null) {
      if (results.supplyChainAnalysis.efficiency < 0 || results.supplyChainAnalysis.efficiency > 1) {
        issues.push(`供应链效率分数超出范围: ${results.supplyChainAnalysis.efficiency}`);
      }
    }
    
    if (results.valueFlowAnalysis?.efficiency != null) {
      if (results.valueFlowAnalysis.efficiency < 0 || results.valueFlowAnalysis.efficiency > 1) {
        issues.push(`价值流效率分数超出范围: ${results.valueFlowAnalysis.efficiency}`);
      }
    }
    
    return {
      issues: issues,
      accuracyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 15))
    };
  }
  
  async checkConsistency(results) {
    const issues = [];
    
    // 检查供需平衡分析的一致性
    if (results.supplyDemandBalance) {
      const { totalSupply, totalDemand } = results.supplyDemandBalance;
      if (totalSupply < 0 || totalDemand < 0) {
        issues.push("供需总量不能为负数");
      }
    }
    
    return {
      issues: issues,
      consistencyScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 20))
    };
  }
  
  async checkEfficiencyValidity(results) {
    const issues = [];
    
    // 检查各种效率指标的有效性
    if (results.resourceAllocation?.allocationEfficiency?.averageEfficiency != null) {
      const eff = results.resourceAllocation.allocationEfficiency.averageEfficiency;
      if (eff < 0 || eff > 1) {
        issues.push(`资源分配效率超出范围: ${eff}`);
      }
    }
    
    return {
      issues: issues,
      validityScore: issues.length === 0 ? 100 : Math.max(0, 100 - (issues.length * 18))
    };
  }
  
  calculateOverallScore(validationResults) {
    const { dataCompleteness, calculationAccuracy, consistency, efficiencyValidity } = validationResults;
    
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
      (efficiencyValidity.validityScore * weights.validity)
    );
  }
}

/**
 * 服务供给报告生成模块
 */
class ServiceSupplyReportingModule {
  async generate(analysisResults, depth = 'standard') {
    const report = {
      supplyChainAnalysis: analysisResults.supplyChainAnalysis,
      valueFlowAnalysis: analysisResults.valueFlowAnalysis,
      resourceAllocation: analysisResults.resourceAllocation,
      processEfficiency: analysisResults.processEfficiency,
      supplyDemandBalance: analysisResults.supplyDemandBalance,
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
        efficiencyMetrics: analysisResults.processEfficiency.performanceIndicators,
        resourceConstraints: analysisResults.resourceAllocation.resourceConstraints,
        optimizationPoints: analysisResults.resourceAllocation.allocationOptimization
      };
    }
    
    return report;
  }
  
  async generateRecommendations(results) {
    const recommendations = [];
    
    // 基于供需平衡的建议
    const balance = results.supplyDemandBalance;
    if (balance.balanceState === 'supply-deficit') {
      recommendations.push("当前服务供给不足，建议增加服务提供商或提升现有提供商的能力");
    } else if (balance.balanceState === 'supply-excess') {
      recommendations.push("当前服务供给过剩，建议优化资源配置或拓展服务需求");
    }
    
    // 基于供应链效率的建议
    const supplyChain = results.supplyChainAnalysis;
    if (supplyChain.resilience.overallScore < 0.5) {
      recommendations.push("供应链韧性不足，建议增加供应商多样性以降低风险");
    }
    
    // 基于价值流效率的建议
    const valueFlow = results.valueFlowAnalysis;
    if (valueFlow.efficiency < 0.6) {
      recommendations.push("价值流效率偏低，建议优化服务质量和流程");
    }
    
    // 基于资源分配的建议
    const resourceAlloc = results.resourceAllocation;
    if (resourceAlloc.allocationEfficiency.averageEfficiency < 0.6) {
      recommendations.push("资源分配效率有待提升，建议优化资源配置");
    }
    
    // 基于流程效率的建议
    const processEff = results.processEfficiency;
    if (processEff.optimizationPotential.potentialImprovement > 0.4) {
      recommendations.push("流程优化潜力较大，建议重点关注效率提升");
    }
    
    // 基于瓶颈识别的建议
    const allBottlenecks = [
      ...(results.supplyChainAnalysis.bottlenecks || []),
      ...(results.resourceAllocation.bottlenecks || []),
      ...(results.processEfficiency.bottlenecks || [])
    ];
    
    if (allBottlenecks.length > 0) {
      recommendations.push(`识别到${allBottlenecks.length}个瓶颈点，需要优先解决`);
    }
    
    return recommendations.length > 0 ? recommendations : [
      "业务服务供给关系整体运行良好，继续保持当前策略"
    ];
  }
}

// 导出技能类
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BusinessServiceSupplyAnalysisSkill;
}