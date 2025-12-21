/**
 * ANT Network Skill - 网络分析技能主入口
 * 遵循SOLID原则：单一职责、开闭、依赖倒置
 */

const NetworkAnalyzer = require('./src/NetworkAnalyzer');
const Visualizer = require('./src/Visualizer');

class AntNetworkSkill {
  constructor(options = {}) {
    // 依赖注入，遵循依赖倒置原则
    this.networkAnalyzer = new NetworkAnalyzer();
    this.visualizer = new Visualizer();

    // 配置选项
    this.options = {
      enableLogging: options.enableLogging || false,
      maxNodes: options.maxNodes || 100,
      enableVisualization: options.enableVisualization !== false,
      layout: options.layout || 'force_directed',
      ...options
    };
  }

  /**
   * 技能主方法 - 执行网络分析
   * @param {Object} participantData - 参与者数据（来自ant-participant-skill）
   * @param {Object} userOptions - 用户选项
   * @returns {Object} 分析结果
   */
  async execute(participantData, userOptions = {}) {
    try {
      // 输入验证
      this._validateInput(participantData);

      // 合并选项
      const finalOptions = { ...this.options, ...userOptions };

      // 执行分析
      const result = await this._performAnalysis(participantData, finalOptions);

      // 后处理
      return this._postProcessResult(result, finalOptions);

    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  /**
   * 输入验证
   * @private
   */
  _validateInput(data) {
    if (!data) {
      throw new Error('输入数据不能为空');
    }

    if (!data.details || !data.details.participants) {
      throw new Error('缺少参与者数据');
    }

    if (!Array.isArray(data.details.participants)) {
      throw new Error('参与者数据必须是数组');
    }

    if (data.details.participants.length > this.options.maxNodes) {
      throw new Error(`参与者数量超过最大限制${this.options.maxNodes}个`);
    }
  }

  /**
   * 执行分析
   * @private
   */
  async _performAnalysis(participantData, options) {
    if (options.enableLogging) {
      console.log(`[AntNetworkSkill] 开始网络分析，参与者数量: ${participantData.details.participants.length}`);
    }

    const startTime = Date.now();

    // 提取核心数据
    const participants = participantData.details.participants;
    const relations = participantData.details.relations || [];

    // 核心分析逻辑
    const analysisResult = this.networkAnalyzer.analyze(participants, relations, options);

    // 可视化处理
    let visualizationResult = null;
    if (options.enableVisualization) {
      visualizationResult = this.visualizer.generate(analysisResult, {
        layout: options.layout,
        width: options.width || 800,
        height: options.height || 600
      });
    }

    const endTime = Date.now();

    // 添加性能指标
    analysisResult.performance = {
      executionTime: endTime - startTime,
      participantCount: participants.length,
      relationCount: relations.length,
      analysisType: 'network_analysis'
    };

    if (options.enableLogging) {
      console.log(`[AntNetworkSkill] 分析完成，耗时: ${analysisResult.performance.executionTime}ms`);
    }

    return {
      analysis: analysisResult,
      visualization: visualizationResult
    };
  }

  /**
   * 结果后处理
   * @private
   */
  _postProcessResult(result, options) {
    const analysis = result.analysis;

    // 生成最终输出格式
    const formattedResult = {
      // 第1层：核心概念
      overview: {
        title: '网络关系分析',
        networkType: analysis.networkStructure.type,
        keyPlayers: analysis.networkStructure.keyPlayers.slice(0, 3),
        centralPlayer: analysis.networkStructure.centralPlayer,
        description: this._generateNetworkDescription(analysis)
      },

      // 第2层：关键发现
      summary: {
        networkMetrics: analysis.networkOverview,
        keyPlayersAnalysis: analysis.keyPlayers.slice(0, 5).map(p => ({
          name: p.name,
          role: p.role,
          centralityScore: p.centralityScore.toFixed(2),
          connections: p.connections.length
        })),
        communities: analysis.communities.slice(0, 3).map(c => ({
          id: c.id,
          size: c.size,
          density: c.density
        }))
      },

      // 第3层：详细数据
      details: {
        networkStructure: analysis.networkStructure,
        allKeyPlayers: analysis.keyPlayers,
        communities: analysis.communities,
        networkMetrics: analysis.networkMetrics
      },

      // 可视化数据
      visualization: result.visualization,

      // 元数据
      metadata: {
        skillName: 'ant-network-skill',
        version: '2.0.0',
        timestamp: new Date().toISOString(),
        processingTime: analysis.performance.executionTime,
        visualizationEnabled: options.enableVisualization
      }
    };

    // 添加可视化HTML（如果启用）
    if (result.visualization && options.enableVisualization) {
      try {
        formattedResult.visualizationHTML = this.visualizer.render(result.visualization);
      } catch (vizError) {
        console.warn('可视化生成失败:', vizError.message);
      }
    }

    return formattedResult;
  }

  /**
   * 生成网络描述
   * @private
   */
  _generateNetworkDescription(analysis) {
    const { networkOverview, networkStructure } = analysis;

    const densityDesc = networkOverview.networkDensity > 0.5 ? '密集' :
                       networkOverview.networkDensity > 0.2 ? '中等密度' : '稀疏';

    const connectivityDesc = networkOverview.isConnected ? '连通' : '非连通';

    let description = `网络包含${networkOverview.totalNodes}个节点和${networkOverview.totalEdges}条边，`;

    if (networkStructure.centralPlayer) {
      description += `以${networkStructure.centralPlayer}为中心形成${networkStructure.type}，`;
    }

    description += `网络密度为${networkOverview.networkDensity}，属于${densityDesc}${connectivityDesc}网络。`;

    if (analysis.communities.length > 1) {
      description += `网络包含${analysis.communities.length}个社区结构。`;
    }

    return description;
  }

  /**
   * 错误处理
   * @private
   */
  _handleError(error) {
    if (this.options.enableLogging) {
      console.error(`[AntNetworkSkill] 错误:`, error.message);
    }
  }

  /**
   * 获取技能信息
   */
  getInfo() {
    return {
      name: 'ant-network-skill',
      description: 'ANT网络关系分析技能，分析参与者网络的结构和关键特征',
      version: '2.0.0',
      capabilities: [
        '网络结构分析',
        '关键玩家识别',
        '社区检测',
        '网络可视化',
        '关系强度分析'
      ],
      supportedLanguages: ['zh-CN'],
      maxNodes: this.options.maxNodes,
      supportedLayouts: ['force_directed', 'circular', 'hierarchical']
    };
  }

  /**
   * 验证分析结果质量
   * @param {Object} result - 分析结果
   * @returns {Object} 质量评估
   */
  validateResult(result) {
    const quality = {
      score: 0,
      issues: [],
      suggestions: []
    };

    try {
      // 检查基本结构
      if (!result.analysis || !result.analysis.networkOverview) {
        quality.issues.push('缺少网络概览数据');
        return quality;
      }

      // 检查数据完整性
      const { networkOverview, keyPlayers, communities } = result.analysis;

      if (networkOverview.totalNodes === 0) {
        quality.issues.push('网络中没有节点');
        quality.suggestions.push('请检查输入数据是否包含有效参与者');
      }

      if (networkOverview.totalEdges === 0 && networkOverview.totalNodes > 1) {
        quality.issues.push('网络中没有关系连接');
        quality.suggestions.push('考虑检查参与者之间是否定义了关系');
      }

      // 计算质量分数
      let score = 100;

      // 数据完整性评分
      if (networkOverview.totalNodes > 0) score += 10;
      if (networkOverview.totalEdges > 0) score += 10;
      if (keyPlayers.length > 0) score += 10;
      if (communities.length > 0) score += 5;

      // 网络质量评分
      if (networkOverview.networkDensity > 0.2) score += 5;
      if (networkOverview.isConnected) score += 5;

      quality.score = Math.min(score, 100);

      // 根据分数给出建议
      if (quality.score < 70) {
        quality.suggestions.push('建议增加参与者或关系以改善网络分析质量');
      }

    } catch (error) {
      quality.issues.push(`验证过程中出错: ${error.message}`);
    }

    return quality;
  }
}

module.exports = AntNetworkSkill;