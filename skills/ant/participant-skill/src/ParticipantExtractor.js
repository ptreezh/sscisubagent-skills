/**
 * ParticipantExtractor - 参与者提取器
 * 遵循单一职责原则：只负责从文本中提取和构建参与者对象
 */

const IExtractor = require('../../../shared/interfaces/IExtractor');
const IAnalyzer = require('../../../shared/interfaces/IAnalyzer');
const { ParticipantType, RelationType, Participant, Relation, AnalysisResult } = require('../../../shared/types/Types');

class ParticipantExtractor extends IExtractor {
  /**
   * 构造函数 - 依赖注入
   * @param {TextAnalyzer} textAnalyzer - 文本分析器
   */
  constructor(textAnalyzer) {
    super();
    if (!textAnalyzer) {
      throw new Error('文本分析器不能为空');
    }
    this.textAnalyzer = textAnalyzer;

    // 关系识别模式
    this.relationPatterns = [
      // 监管关系
      { pattern: /(.+?)(?:监管|管理|监督|指导|领导)(.+?)/, type: RelationType.SUPERVISION },
      // 合作关系
      { pattern: /(.+?)(?:合作|协作|配合|联合|共同)(.+?)/, type: RelationType.COOPERATION },
      // 竞争关系
      { pattern: /(.+?)(?:竞争|对抗|对比)(.+?)/, type: RelationType.COMPETITION },
      // 影响关系
      { pattern: /(.+?)(?:影响|促进|推动|帮助)(.+?)/, type: RelationType.INFLUENCE },
      // 依赖关系
      { pattern: /(.+?)(?:依赖|依靠|需要|基于)(.+?)/, type: RelationType.DEPENDENCY }
    ];
  }

  /**
   * 提取参与者 - 实现IExtractor接口
   * @param {string} text - 输入文本
   * @param {Object} options - 提取选项
   * @returns {AnalysisResult} 分析结果
   */
  extract(text, options = {}) {
    if (text === null || text === undefined) {
      throw new Error('输入文本不能为空');
    }

    const result = new AnalysisResult();

    if (!text || text.trim().length === 0) {
      return result; // 返回空结果
    }

    // 1. 提取参与者模式
    const patterns = this.textAnalyzer.extract(text);

    // 2. 构建参与者对象
    const participants = this._buildParticipants(patterns, text);
    participants.forEach(p => result.addParticipant(p));

    // 3. 提取关系
    const relations = this.extractRelations(participants, text);
    relations.forEach(r => result.addRelation(r));

    // 4. 生成摘要
    result.generateSummary();

    return result;
  }

  /**
   * 构建参与者对象
   * @private
   */
  _buildParticipants(patterns, text) {
    const participants = [];
    const participantMap = new Map();

    patterns.forEach(pattern => {
      const id = this._generateId(pattern.text, pattern.type);

      if (!participantMap.has(id)) {
        const participant = new Participant(
          pattern.text,
          pattern.type,
          this._identifyRole(pattern.text, pattern.type),
          this._assessImportance(pattern.text, text),
          pattern.position
        );

        participantMap.set(id, participant);
        participants.push(participant);
      }
    });

    return participants;
  }

  /**
   * 生成参与者ID
   * @private
   */
  _generateId(text, type) {
    return `${type}_${text.replace(/\s/g, '_')}`;
  }

  /**
   * 识别参与者角色
   * @private
   */
  _identifyRole(text, type) {
    let roles = [];

    if (type === ParticipantType.ORGANIZATION) {
      if (/部|委|局|署/.test(text)) roles.push('政府部门');
      if (/政府/.test(text)) roles.push('政府机构');
      if (/公司|企业|集团/.test(text)) roles.push('企业');
      if (/学|校|院|所/.test(text)) roles.push('学术机构');
      if (/银行|保险|证券/.test(text)) roles.push('金融机构');
    }

    if (type === ParticipantType.INDIVIDUAL) {
      if (/局长|处长|科长|部长|主任/.test(text)) roles.push('管理者');
      if (/教授|研究员|专家/.test(text)) roles.push('专家');
      if (/工程师|技术员/.test(text)) roles.push('技术人员');
    }

    if (type === ParticipantType.CONCEPT) {
      if (/技术|系统|平台/.test(text)) roles.push('技术方案');
      if (/政策|法规|制度/.test(text)) roles.push('政策工具');
    }

    return roles.length > 0 ? roles.join(',') : '未定义';
  }

  /**
   * 评估参与者重要性
   * @private
   */
  _assessImportance(text, fullText) {
    let importance = 0;

    // 基于类型的权重
    if (/部|委|政府|局/.test(text)) importance += 3; // 政府部门权重高
    if (/公司|企业/.test(text)) importance += 2;       // 企业权重中等
    if (/教授|专家|局长/.test(text)) importance += 2;   // 关键人物权重中等

    // 基于出现频率
    const matches = (fullText.match(new RegExp(text, 'g')) || []).length;
    importance += Math.min(matches, 3); // 最多加3分

    // 基于位置（首次出现位置越前越重要）
    const firstPos = fullText.indexOf(text);
    if (firstPos < fullText.length * 0.3) importance += 1;

    if (importance >= 4) return 'high';
    if (importance >= 2) return 'medium';
    return 'low';
  }

  /**
   * 提取关系
   * @param {Array} participants - 参与者数组
   * @param {string} text - 原始文本
   * @returns {Array} 关系数组
   */
  extractRelations(participants, text) {
    const relations = [];

    // 创建参与者名称映射
    const nameToId = new Map();
    participants.forEach(p => nameToId.set(p.name, this._generateId(p.name, p.type)));

    // 使用关系模式识别
    this.relationPatterns.forEach(({ pattern, type }) => {
      let match;
      const regex = new RegExp(pattern);

      while ((match = regex.exec(text)) !== null) {
        const fromText = match[1].trim();
        const toText = match[2].trim();

        const fromId = nameToId.get(fromText);
        const toId = nameToId.get(toText);

        if (fromId && toId && fromId !== toId) {
          const relation = new Relation(
            fromId,
            toId,
            type,
            this._assessRelationStrength(match[0], text),
            match[0]
          );

          relations.push(relation);
        }
      }
    });

    // 去重关系
    return this._deduplicateRelations(relations);
  }

  /**
   * 评估关系强度
   * @private
   */
  _assessRelationStrength(relationText, fullText) {
    let strength = 1;

    // 强关系词
    if (/监管|管理|领导/.test(relationText)) strength = 3;
    if (/合作|协作|联合/.test(relationText)) strength = 2;
    if (/影响|促进/.test(relationText)) strength = 1;

    return strength >= 2.5 ? '强' : strength >= 1.5 ? '中' : '弱';
  }

  /**
   * 去重关系
   * @private
   */
  _deduplicateRelations(relations) {
    const seen = new Set();
    return relations.filter(relation => {
      const key = `${relation.fromId}-${relation.toId}-${relation.type}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  /**
   * 验证提取结果 - 实现IExtractor接口
   * @param {AnalysisResult} result - 分析结果
   * @returns {boolean} 是否有效
   */
  validate(result) {
    return result instanceof AnalysisResult &&
           Array.isArray(result.participants) &&
           Array.isArray(result.relations) &&
           typeof result.summary === 'object';
  }

  /**
   * 获取分析指标 - 实现IAnalyzer接口
   * @param {AnalysisResult} data - 分析数据
   * @returns {Object} 指标对象
   */
  getMetrics(data) {
    if (!this.validate(data)) {
      throw new Error('输入数据格式无效');
    }

    const typeCount = {};
    data.participants.forEach(p => {
      typeCount[p.type] = (typeCount[p.type] || 0) + 1;
    });

    const relationCount = {};
    data.relations.forEach(r => {
      relationCount[r.type] = (relationCount[r.type] || 0) + 1;
    });

    return {
      participantMetrics: {
        total: data.participants.length,
        byType: typeCount,
        highImportance: data.participants.filter(p => p.importance === 'high').length
      },
      relationMetrics: {
        total: data.relations.length,
        byType: relationCount,
        strongRelations: data.relations.filter(r => r.strength === '强').length
      },
      networkMetrics: {
        density: this._calculateDensity(data.participants.length, data.relations.length),
        type: data.summary.networkType
      }
    };
  }

  /**
   * 计算网络密度
   * @private
   */
  _calculateDensity(nodeCount, edgeCount) {
    if (nodeCount < 2) return 0;
    const maxPossibleEdges = nodeCount * (nodeCount - 1) / 2;
    return (edgeCount / maxPossibleEdges).toFixed(2);
  }
}

module.exports = ParticipantExtractor;