/**
 * 数据类型定义 - 遵循单一职责原则
 * 定义所有ANT技能使用的数据结构
 */

/**
 * 参与者类型枚举
 */
const ParticipantType = {
  INDIVIDUAL: 'individual',     // 个人
  ORGANIZATION: 'organization',  // 组织机构
  OBJECT: 'object',             // 物品/技术
  CONCEPT: 'concept'            // 概念/政策
};

/**
 * 关系类型枚举
 */
const RelationType = {
  COOPERATION: 'cooperation',    // 合作关系
  COMPETITION: 'competition',    // 竞争关系
  SUPERVISION: 'supervision',    // 监管关系
  INFLUENCE: 'influence',        // 影响关系
  DEPENDENCY: 'dependency'       // 依赖关系
};

/**
 * 参与者数据结构
 */
class Participant {
  /**
   * @param {string} name - 名称
   * @param {ParticipantType} type - 类型
   * @param {string} role - 角色
   * @param {string} importance - 重要性等级
   * @param {number} position - 文本位置
   */
  constructor(name, type, role = '', importance = 'medium', position = -1) {
    this.name = name;
    this.type = type;
    this.role = role;
    this.importance = importance;
    this.position = position;
    this.connections = [];
  }

  /**
   * 添加连接
   * @param {string} targetId - 目标ID
   */
  addConnection(targetId) {
    if (!this.connections.includes(targetId)) {
      this.connections.push(targetId);
    }
  }
}

/**
 * 关系数据结构
 */
class Relation {
  /**
   * @param {string} fromId - 源参与者ID
   * @param {string} toId - 目标参与者ID
   * @param {RelationType} type - 关系类型
   * @param {string} strength - 关系强度
   * @param {string} description - 关系描述
   */
  constructor(fromId, toId, type, strength = 'medium', description = '') {
    this.fromId = fromId;
    this.toId = toId;
    this.type = type;
    this.strength = strength;
    this.description = description;
  }
}

/**
 * 分析结果数据结构
 */
class AnalysisResult {
  constructor() {
    this.participants = [];
    this.relations = [];
    this.metrics = {};
    this.summary = {};
  }

  /**
   * 添加参与者
   * @param {Participant} participant - 参与者对象
   */
  addParticipant(participant) {
    this.participants.push(participant);
  }

  /**
   * 添加关系
   * @param {Relation} relation - 关系对象
   */
  addRelation(relation) {
    this.relations.push(relation);
  }

  /**
   * 生成摘要
   */
  generateSummary() {
    this.summary = {
      participantCount: this.participants.length,
      relationCount: this.relations.length,
      keyParticipants: this.participants
        .filter(p => p.importance === 'high')
        .map(p => p.name),
      networkType: this._identifyNetworkType()
    };
  }

  _identifyNetworkType() {
    const highImportance = this.participants.filter(p => p.importance === 'high').length;

    if (highImportance === 1) return '星型网络';
    if (highImportance > 3) return '多中心网络';
    if (this.relations.length > this.participants.length) return '密集网络';
    return '稀疏网络';
  }
}

module.exports = {
  ParticipantType,
  RelationType,
  Participant,
  Relation,
  AnalysisResult
};