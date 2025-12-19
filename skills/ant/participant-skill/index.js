/**
 * ANT Participant Skill - 参与者识别技能主入口
 * 遵循SOLID原则：单一职责、开闭、依赖倒置
 */

const TextAnalyzer = require('./src/TextAnalyzer');
const ParticipantExtractor = require('./src/ParticipantExtractor');

class AntParticipantSkill {
  constructor(options = {}) {
    // 依赖注入，遵循依赖倒置原则
    this.textAnalyzer = new TextAnalyzer();
    this.participantExtractor = new ParticipantExtractor(this.textAnalyzer);

    // 配置选项
    this.options = {
      enableLogging: options.enableLogging || false,
      maxTextLength: options.maxTextLength || 10000,
      confidenceThreshold: options.confidenceThreshold || 0.5,
      ...options
    };
  }

  /**
   * 技能主方法 - 执行参与者识别
   * @param {string} text - 输入文本
   * @param {Object} userOptions - 用户选项
   * @returns {Object} 分析结果
   */
  async execute(text, userOptions = {}) {
    try {
      // 输入验证
      this._validateInput(text);

      // 合并选项
      const finalOptions = { ...this.options, ...userOptions };

      // 执行分析
      const result = await this._performAnalysis(text, finalOptions);

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
  _validateInput(text) {
    if (text === null || text === undefined) {
      throw new Error('输入文本不能为空');
    }

    if (typeof text !== 'string') {
      throw new Error('输入必须是字符串类型');
    }

    if (text.length > this.options.maxTextLength) {
      throw new Error(`输入文本过长，最大支持${this.options.maxTextLength}字符`);
    }
  }

  /**
   * 执行分析
   * @private
   */
  async _performAnalysis(text, options) {
    if (options.enableLogging) {
      console.log(`[AntParticipantSkill] 开始分析文本，长度: ${text.length}`);
    }

    // 核心分析逻辑
    const startTime = Date.now();
    const result = this.participantExtractor.extract(text);
    const endTime = Date.now();

    // 添加性能指标
    result.performance = {
      executionTime: endTime - startTime,
      textLength: text.length,
      participantCount: result.participants.length,
      relationCount: result.relations.length
    };

    if (options.enableLogging) {
      console.log(`[AntParticipantSkill] 分析完成，耗时: ${result.performance.executionTime}ms`);
    }

    return result;
  }

  /**
   * 结果后处理
   * @private
   */
  _postProcessResult(result, options) {
    // 过滤低置信度结果
    if (options.confidenceThreshold > 0) {
      result.participants = result.participants.filter(p =>
        this._calculateOverallConfidence(p) >= options.confidenceThreshold
      );
    }

    // 按重要性排序
    result.participants.sort((a, b) => {
      const importanceOrder = { high: 3, medium: 2, low: 1 };
      return importanceOrder[b.importance] - importanceOrder[a.importance];
    });

    // 生成最终输出格式
    return this._formatOutput(result);
  }

  /**
   * 计算总体置信度
   * @private
   */
  _calculateOverallConfidence(participant) {
    // 综合多个因素计算置信度
    let confidence = 0.7; // 基础置信度

    if (participant.role !== '未定义') confidence += 0.1;
    if (participant.importance === 'high') confidence += 0.1;
    if (participant.connections.length > 0) confidence += 0.1;

    return Math.min(confidence, 1.0);
  }

  /**
   * 格式化输出
   * @private
   */
  _formatOutput(result) {
    return {
      // 第1层：核心概念
      overview: {
        title: '参与者网络分析',
        totalParticipants: result.summary.participantCount,
        keyParticipants: result.summary.keyParticipants,
        networkType: result.summary.networkType,
        description: this._generateDescription(result)
      },

      // 第2层：关键发现
      summary: {
        participants: result.participants.slice(0, 5).map(p => ({
          name: p.name,
          type: p.type,
          role: p.role,
          importance: p.importance
        })),
        relations: result.relations.slice(0, 3).map(r => ({
          from: this._getParticipantName(r.fromId, result.participants),
          to: this._getParticipantName(r.toId, result.participants),
          type: r.type,
          strength: r.strength
        })),
        metrics: this.participantExtractor.getMetrics(result)
      },

      // 第3层：详细数据
      details: {
        participants: result.participants,
        relations: result.relations,
        performance: result.performance
      },

      // 元数据
      metadata: {
        skillName: 'ant-participant-skill',
        version: '2.0.0',
        timestamp: new Date().toISOString(),
        processingTime: result.performance.executionTime
      }
    };
  }

  /**
   * 获取参与者名称
   * @private
   */
  _getParticipantName(participantId, participants) {
    const participant = participants.find(p =>
      this._generateId(p.name, p.type) === participantId
    );
    return participant ? participant.name : participantId;
  }

  /**
   * 生成参与者ID
   * @private
   */
  _generateId(text, type) {
    return `${type}_${text.replace(/\s/g, '_')}`;
  }

  /**
   * 生成描述
   * @private
   */
  _generateDescription(result) {
    const types = {};
    result.participants.forEach(p => {
      types[p.type] = (types[p.type] || 0) + 1;
    });

    const typeDesc = Object.entries(types)
      .map(([type, count]) => `${count}个${this._getTypeName(type)}`)
      .join('、');

    return `识别出${result.summary.participantCount}个参与者，包括${typeDesc}，形成${result.summary.networkType}结构。`;
  }

  /**
   * 获取类型名称
   * @private
   */
  _getTypeName(type) {
    const typeNames = {
      individual: '个人',
      organization: '组织',
      object: '物品',
      concept: '概念'
    };
    return typeNames[type] || type;
  }

  /**
   * 错误处理
   * @private
   */
  _handleError(error) {
    if (this.options.enableLogging) {
      console.error(`[AntParticipantSkill] 错误:`, error.message);
    }
  }

  /**
   * 获取技能信息
   */
  getInfo() {
    return {
      name: 'ant-participant-skill',
      description: 'ANT参与者识别技能，从中文文本中识别参与者及其关系',
      version: '2.0.0',
      capabilities: [
        '参与者识别',
        '关系分析',
        '重要性评估',
        '网络结构分析'
      ],
      supportedLanguages: ['zh-CN'],
      maxTextLength: this.options.maxTextLength
    };
  }
}

module.exports = AntParticipantSkill;