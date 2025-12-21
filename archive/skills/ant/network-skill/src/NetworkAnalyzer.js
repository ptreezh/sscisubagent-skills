/**
 * NetworkAnalyzer - 网络分析器
 * 遵循单一职责原则：只负责网络结构分析和指标计算
 */

const IAnalyzer = require('../../../shared/interfaces/IAnalyzer');

class NetworkAnalyzer extends IAnalyzer {
  constructor() {
    super();
    this.analysisCache = new Map(); // 缓存分析结果
  }

  /**
   * 分析网络 - 实现IAnalyzer接口
   * @param {Array} participants - 参与者数组
   * @param {Array} relations - 关系数组
   * @param {Object} options - 分析选项
   * @returns {Object} 分析结果
   */
  analyze(participants, relations, options = {}) {
    // 输入验证
    if (!Array.isArray(participants) || !Array.isArray(relations)) {
      throw new Error('输入数据必须是数组');
    }

    // 缓存键
    const cacheKey = this._generateCacheKey(participants, relations);
    if (this.analysisCache.has(cacheKey)) {
      return this.analysisCache.get(cacheKey);
    }

    // 核心分析
    const result = {
      networkOverview: this._analyzeOverview(participants, relations),
      networkStructure: this._analyzeStructure(participants, relations),
      keyPlayers: this.findKeyPlayers(participants, relations),
      networkMetrics: this.getMetrics({ participants, relations }),
      communities: this.detectCommunities(participants, relations)
    };

    // 缓存结果
    this.analysisCache.set(cacheKey, result);

    return result;
  }

  /**
   * 分析网络概览
   * @private
   */
  _analyzeOverview(participants, relations) {
    const nodeCount = participants.length;
    const edgeCount = relations.length;

    return {
      totalNodes: nodeCount,
      totalEdges: edgeCount,
      networkDensity: this.calculateNetworkDensity(nodeCount, edgeCount),
      averageDegree: nodeCount > 0 ? (2 * edgeCount) / nodeCount : 0,
      isConnected: this._isConnected(participants, relations)
    };
  }

  /**
   * 分析网络结构
   * @private
   */
  _analyzeStructure(participants, relations) {
    const networkType = this._identifyNetworkType(participants, relations);
    const centralPlayer = this._findCentralPlayer(participants, relations);

    return {
      type: networkType,
      centralPlayer: centralPlayer,
      peripheryPlayers: this._findPeripheryPlayers(participants, centralPlayer),
      keyPlayers: this._findKeyPlayers(participants, relations)
    };
  }

  /**
   * 识别网络类型
   * @private
   */
  _identifyNetworkType(participants, relations) {
    const nodeCount = participants.length;
    const edgeCount = relations.length;

    if (nodeCount === 0) return '空网络';
    if (nodeCount === 1) return '单节点网络';

    const density = this.calculateNetworkDensity(nodeCount, edgeCount);
    const highImportanceNodes = participants.filter(p => p.importance === 'high').length;

    // 根据密度和关键节点数量判断网络类型
    if (highImportanceNodes === 1) return '星型网络';
    if (highImportanceNodes > 3) return '多中心网络';
    if (density > 0.5) return '密集网络';
    if (density > 0.2) return '中等密度网络';
    return '稀疏网络';
  }

  /**
   * 查找中心玩家
   * @private
   */
  _findCentralPlayer(participants, relations) {
    if (participants.length === 0) return null;

    const degreeCentrality = this._calculateDegreeCentrality(participants, relations);

    // 找到度中心性最高的节点
    let centralPlayer = null;
    let maxDegree = 0;

    Object.entries(degreeCentrality).forEach(([nodeId, degree]) => {
      if (degree > maxDegree) {
        maxDegree = degree;
        centralPlayer = nodeId;
      }
    });

    return this._getNodeName(centralPlayer, participants);
  }

  /**
   * 查找外围玩家
   * @private
   */
  _findPeripheryPlayers(participants, centralPlayer) {
    if (!centralPlayer || participants.length <= 1) return [];

    // 返回非中心玩家的其他玩家
    return participants
      .filter(p => p.name !== centralPlayer)
      .map(p => p.name);
  }

  /**
   * 查找关键玩家
   * @private
   */
  _findKeyPlayers(participants, relations) {
    const keyPlayers = this.findKeyPlayers(participants, relations);
    return keyPlayers.map(p => p.name);
  }

  /**
   * 查找关键玩家（详细分析）
   */
  findKeyPlayers(participants, relations) {
    if (participants.length === 0) return [];

    const degreeCentrality = this._calculateDegreeCentrality(participants, relations);
    const betweennessCentrality = this.calculateBetweennessCentrality(
      participants.map(p => this._getNodeId(p)),
      relations
    );

    // 综合度中心性和中介中心性
    const keyPlayers = participants.map(p => {
      const nodeId = this._getNodeId(p);
      return {
        ...p,
        degreeCentrality: degreeCentrality[nodeId] || 0,
        betweennessCentrality: betweennessCentrality[nodeId] || 0,
        centralityScore: (degreeCentrality[nodeId] || 0) * 0.5 + (betweennessCentrality[nodeId] || 0) * 0.5
      };
    });

    // 按中心性分数排序
    return keyPlayers.sort((a, b) => b.centralityScore - a.centralityScore);
  }

  /**
   * 计算度中心性
   * @private
   */
  _calculateDegreeCentrality(participants, relations) {
    const centrality = {};

    // 初始化
    participants.forEach(p => {
      centrality[this._getNodeId(p)] = 0;
    });

    // 计算每个节点的度
    relations.forEach(relation => {
      if (centrality[relation.fromId] !== undefined) {
        centrality[relation.fromId]++;
      }
      if (centrality[relation.toId] !== undefined) {
        centrality[relation.toId]++;
      }
    });

    return centrality;
  }

  /**
   * 计算网络密度
   */
  calculateNetworkDensity(nodeCount, edgeCount) {
    if (nodeCount < 2) return 0;
    const maxPossibleEdges = nodeCount * (nodeCount - 1) / 2;
    return (edgeCount / maxPossibleEdges).toFixed(2);
  }

  /**
   * 计算中介中心性
   */
  calculateBetweennessCentrality(nodeIds, relations) {
    const betweenness = {};
    const adjacencyList = this._buildAdjacencyList(nodeIds, relations);

    // 初始化
    nodeIds.forEach(id => {
      betweenness[id] = 0;
    });

    // 对每对节点计算最短路径
    for (let i = 0; i < nodeIds.length; i++) {
      for (let j = i + 1; j < nodeIds.length; j++) {
        const paths = this._findAllShortestPaths(nodeIds[i], nodeIds[j], adjacencyList);

        // 更新经过节点的中介中心性
        paths.forEach(path => {
          for (let k = 1; k < path.length - 1; k++) {
            betweenness[path[k]] += 1;
          }
        });
      }
    }

    return betweenness;
  }

  /**
   * 构建邻接表
   * @private
   */
  _buildAdjacencyList(nodeIds, relations) {
    const adjacencyList = {};

    // 初始化邻接表
    nodeIds.forEach(id => {
      adjacencyList[id] = [];
    });

    // 添加边
    relations.forEach(relation => {
      if (adjacencyList[relation.fromId] && !adjacencyList[relation.fromId].includes(relation.toId)) {
        adjacencyList[relation.fromId].push(relation.toId);
      }
      if (adjacencyList[relation.toId] && !adjacencyList[relation.toId].includes(relation.fromId)) {
        adjacencyList[relation.toId].push(relation.fromId);
      }
    });

    return adjacencyList;
  }

  /**
   * 查找所有最短路径
   * @private
   */
  _findAllShortestPaths(start, end, adjacencyList) {
    const queue = [[start]];
    const visited = new Set();
    const shortestPaths = [];
    let shortestLength = Infinity;

    while (queue.length > 0) {
      const path = queue.shift();
      const current = path[path.length - 1];

      if (path.length > shortestLength) continue;

      if (current === end) {
        shortestLength = path.length;
        shortestPaths.push(path);
        continue;
      }

      if (visited.has(current)) continue;

      visited.add(current);

      for (const neighbor of adjacencyList[current] || []) {
        if (!path.includes(neighbor)) {
          queue.push([...path, neighbor]);
        }
      }
    }

    return shortestPaths;
  }

  /**
   * 检测社区
   */
  detectCommunities(participants, relations) {
    if (participants.length === 0) return [];

    // 使用简单的连通分量算法
    const nodeIds = participants.map(p => this._getNodeId(p));
    const adjacencyList = this._buildAdjacencyList(nodeIds, relations);
    const visited = new Set();
    const communities = [];

    for (const nodeId of nodeIds) {
      if (!visited.has(nodeId)) {
        const community = this._dfsCommunity(nodeId, adjacencyList, visited);

        if (community.length > 0) {
          communities.push({
            id: `community_${communities.length + 1}`,
            members: community,
            size: community.length,
            density: this._calculateCommunityDensity(community, relations)
          });
        }
      }
    }

    return communities;
  }

  /**
   * 深度优先搜索社区
   * @private
   */
  _dfsCommunity(startNodeId, adjacencyList, visited) {
    const community = [];
    const stack = [startNodeId];

    while (stack.length > 0) {
      const nodeId = stack.pop();

      if (visited.has(nodeId)) continue;

      visited.add(nodeId);
      community.push(nodeId);

      for (const neighbor of adjacencyList[nodeId] || []) {
        if (!visited.has(neighbor)) {
          stack.push(neighbor);
        }
      }
    }

    return community;
  }

  /**
   * 计算社区密度
   * @private
   */
  _calculateCommunityDensity(communityNodes, relations) {
    const internalEdges = relations.filter(r =>
      communityNodes.includes(r.fromId) && communityNodes.includes(r.toId)
    ).length;

    const nodeCount = communityNodes.length;
    if (nodeCount < 2) return 0;

    const maxPossibleEdges = nodeCount * (nodeCount - 1) / 2;
    return (internalEdges / maxPossibleEdges).toFixed(2);
  }

  /**
   * 检查网络是否连通
   * @private
   */
  _isConnected(participants, relations) {
    if (participants.length === 0) return true;

    const nodeIds = participants.map(p => this._getNodeId(p));
    const adjacencyList = this._buildAdjacencyList(nodeIds, relations);
    const visited = new Set();

    // 从第一个节点开始DFS
    this._dfsCommunity(nodeIds[0], adjacencyList, visited);

    return visited.size === nodeIds.length;
  }

  /**
   * 获取分析指标 - 实现IAnalyzer接口
   */
  getMetrics(data) {
    if (!data || !data.participants || !data.relations) {
      throw new Error('输入数据格式无效');
    }

    const { participants, relations } = data;
    const nodeCount = participants.length;
    const edgeCount = relations.length;

    return {
      networkMetrics: {
        nodeCount,
        edgeCount,
        density: this.calculateNetworkDensity(nodeCount, edgeCount),
        averageDegree: nodeCount > 0 ? (2 * edgeCount) / nodeCount : 0,
        isConnected: this._isConnected(participants, relations)
      },
      participantMetrics: {
        highImportance: participants.filter(p => p.importance === 'high').length,
        mediumImportance: participants.filter(p => p.importance === 'medium').length,
        lowImportance: participants.filter(p => p.importance === 'low').length
      },
      relationMetrics: {
        supervision: relations.filter(r => r.type === 'supervision').length,
        cooperation: relations.filter(r => r.type === 'cooperation').length,
        competition: relations.filter(r => r.type === 'competition').length,
        influence: relations.filter(r => r.type === 'influence').length,
        dependency: relations.filter(r => r.type === 'dependency').length
      }
    };
  }

  /**
   * 生成缓存键
   * @private
   */
  _generateCacheKey(participants, relations) {
    const participantHash = participants.map(p => p.name).sort().join('|');
    const relationHash = relations.map(r => `${r.fromId}-${r.toId}`).sort().join('|');
    return `${participantHash}_${relationHash}`;
  }

  /**
   * 获取节点ID
   * @private
   */
  _getNodeId(participant) {
    return `${participant.type}_${participant.name.replace(/\s/g, '_')}`;
  }

  /**
   * 获取节点名称
   * @private
   */
  _getNodeName(nodeId, participants) {
    const participant = participants.find(p => this._getNodeId(p) === nodeId);
    return participant ? participant.name : nodeId;
  }
}

module.exports = NetworkAnalyzer;