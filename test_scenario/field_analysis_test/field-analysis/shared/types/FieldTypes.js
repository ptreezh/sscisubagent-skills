/**
 * 场域理论类型定义
 * 严格遵循布迪厄场域理论的概念框架
 */

/**
 * 场域类型枚举
 */
const FieldType = {
  ACADEMIC: 'academic',           // 学术场域
  ECONOMIC: 'economic',           // 经济场域
  POLITICAL: 'political',         // 政治场域
  CULTURAL: 'cultural',           // 文化场域
  EDUCATIONAL: 'educational',     // 教育场域
  BUREAUCRATIC: 'bureaucratic',   // 科层场域
  SOCIAL: 'social',              // 社会场域
  RELIGIOUS: 'religious',         // 宗教场域
  LEGAL: 'legal',                // 法律场域
  MEDIA: 'media'                 // 媒体场域
};

/**
 * 自主性级别枚举
 */
const AutonomyLevel = {
  VERY_HIGH: 'very_high',         // 极高自主性
  HIGH: 'high',                   // 高自主性
  MEDIUM: 'medium',               // 中等自主性
  LOW: 'low',                     // 低自主性
  VERY_LOW: 'very_low'            // 极低自主性
};

/**
 * 场域边界类型
 */
const BoundaryType = {
  INTERNAL: 'internal',           // 内部边界
  EXTERNAL: 'external',           // 外部边界
  PERMEABLE: 'permeable',         // 可渗透边界
  IMPERMEABLE: 'impermeable',     // 不可渗透边界
  FORMAL: 'formal',               // 正式边界
  INFORMAL: 'informal'            // 非正式边界
};

/**
 * 场域数据结构
 */
class Field {
  /**
   * @param {string} name - 场域名称
   * @param {FieldType} type - 场域类型
   * @param {Object} context - 场域背景
   * @param {string} description - 场域描述
   */
  constructor(name, type, context = {}, description = '') {
    this.id = this._generateId(name, type);
    this.name = name;
    this.type = type;
    this.context = context;
    this.description = description;
    this.boundaries = null;
    this.autonomy = null;
    this.positions = [];
    this.rules = [];
    this.powerStructure = null;
  }

  /**
   * 设置场域边界
   * @param {FieldBoundary} boundary - 场域边界
   */
  setBoundary(boundary) {
    this.boundaries = boundary;
  }

  /**
   * 设置自主性评估
   * @param {FieldAutonomy} autonomy - 自主性评估
   */
  setAutonomy(autonomy) {
    this.autonomy = autonomy;
  }

  /**
   * 添加场域位置
   * @param {FieldPosition} position - 场域位置
   */
  addPosition(position) {
    this.positions.push(position);
  }

  /**
   * 添加游戏规则
   * @param {FieldRule} rule - 游戏规则
   */
  addRule(rule) {
    this.rules.push(rule);
  }

  /**
   * 设置权力结构
   * @param {PowerStructure} powerStructure - 权力结构
   */
  setPowerStructure(powerStructure) {
    this.powerStructure = powerStructure;
  }

  /**
   * 生成唯一ID
   * @private
   */
  _generateId(name, type) {
    return `${type}_${name.replace(/\s+/g, '_').toLowerCase()}`;
  }
}

/**
 * 场域边界数据结构
 */
class FieldBoundary {
  constructor() {
    this.internalBoundaries = [];
    this.externalBoundaries = [];
    this.boundaryMechanisms = [];
    this.permeabilityLevels = {};
    this.legitimacySources = [];
  }

  /**
   * 添加内部边界
   * @param {Object} boundary - 内部边界
   */
  addInternalBoundary(boundary) {
    this.internalBoundaries.push(boundary);
  }

  /**
   * 添加外部边界
   * @param {Object} boundary - 外部边界
   */
  addExternalBoundary(boundary) {
    this.externalBoundaries.push(boundary);
  }

  /**
   * 添加边界机制
   * @param {Object} mechanism - 边界控制机制
   */
  addBoundaryMechanism(mechanism) {
    this.boundaryMechanisms.push(mechanism);
  }

  /**
   * 设置边界渗透性
   * @param {BoundaryType} boundaryType - 边界类型
   * @param {number} permeability - 渗透性程度 (0-1)
   */
  setPermeability(boundaryType, permeability) {
    this.permeabilityLevels[boundaryType] = permeability;
  }
}

/**
 * 场域自主性数据结构
 */
class FieldAutonomy {
  constructor() {
    this.overallScore = 0;
    this.economicAutonomy = 0;
    this.politicalAutonomy = 0;
    this.culturalAutonomy = 0;
    this.externalPressures = [];
    this.internalLegitimacy = 0;
    this.autonomyTrends = [];
  }

  /**
   * 计算总体自主性得分
   */
  calculateOverallScore() {
    const weights = {
      economic: 0.3,
      political: 0.3,
      cultural: 0.4
    };

    this.overallScore = (
      this.economicAutonomy * weights.economic +
      this.politicalAutonomy * weights.political +
      this.culturalAutonomy * weights.cultural
    );

    return this.overallScore;
  }

  /**
   * 添加外部压力
   * @param {Object} pressure - 外部压力
   */
  addExternalPressure(pressure) {
    this.externalPressures.push(pressure);
  }

  /**
   * 设置自主性趋势
   * @param {string} trend - 趋势描述
   */
  setAutonomyTrend(trend) {
    this.autonomyTrends.push({
      trend: trend,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 获取自主性级别
   * @returns {AutonomyLevel} 自主性级别
   */
  getAutonomyLevel() {
    if (this.overallScore >= 0.8) return AutonomyLevel.VERY_HIGH;
    if (this.overallScore >= 0.6) return AutonomyLevel.HIGH;
    if (this.overallScore >= 0.4) return AutonomyLevel.MEDIUM;
    if (this.overallScore >= 0.2) return AutonomyLevel.LOW;
    return AutonomyLevel.VERY_LOW;
  }
}

/**
 * 场域位置数据结构
 */
class FieldPosition {
  /**
   * @param {string} name - 位置名称
   * @param {number} powerLevel - 权力级别 (0-1)
   * @param {Array<string>} capitalRequirements - 资本要求
   * @param {Array<string}> habitusExpectations - 习性期望
   */
  constructor(name, powerLevel, capitalRequirements = [], habitusExpectations = []) {
    this.name = name;
    this.powerLevel = powerLevel;
    this.capitalRequirements = capitalRequirements;
    this.habitusExpectations = habitusExpectations;
    this.occupants = [];
    this.mobilityBarriers = [];
    this.stabilityLevel = 'medium';
  }

  /**
   * 添加位置占据者
   * @param {Object} occupant - 占据者信息
   */
  addOccupant(occupant) {
    this.occupants.push(occupant);
  }

  /**
   * 添加流动性障碍
   * @param {Object} barrier - 流动性障碍
   */
  addMobilityBarrier(barrier) {
    this.mobilityBarriers.push(barrier);
  }

  /**
   * 设置稳定性级别
   * @param {string} stability - 稳定性级别
   */
  setStabilityLevel(stability) {
    this.stabilityLevel = stability;
  }
}

/**
 * 游戏规则数据结构
 */
class FieldRule {
  /**
   * @param {string} name - 规则名称
   * @param {string} type - 规则类型
   * @param {string} description - 规则描述
   * @param {number} importance - 重要性级别 (0-1)
   */
  constructor(name, type, description, importance = 0.5) {
    this.name = name;
    this.type = type;
    this.description = description;
    this.importance = importance;
    this.enforcementMechanisms = [];
    this.violationConsequences = [];
  }

  /**
   * 添加执行机制
   * @param {Object} mechanism - 执行机制
   */
  addEnforcementMechanism(mechanism) {
    this.enforcementMechanisms.push(mechanism);
  }

  /**
   * 添加违规后果
   * @param {Object} consequence - 违规后果
   */
  addViolationConsequence(consequence) {
    this.violationConsequences.push(consequence);
  }
}

/**
 * 权力结构数据结构
 */
class PowerStructure {
  constructor() {
    this.powerCenters = [];
    this.powerRelations = [];
    this.powerForms = [];
    this.legitimacySources = [];
    this.conflictAreas = [];
    this.stabilityAssessment = 'stable';
  }

  /**
   * 添加权力中心
   * @param {Object} powerCenter - 权力中心
   */
  addPowerCenter(powerCenter) {
    this.powerCenters.push(powerCenter);
  }

  /**
   * 添加权力关系
   * @param {Object} powerRelation - 权力关系
   */
  addPowerRelation(powerRelation) {
    this.powerRelations.push(powerRelation);
  }

  /**
   * 添加权力形式
   * @param {Object} powerForm - 权力形式
   */
  addPowerForm(powerForm) {
    this.powerForms.push(powerForm);
  }

  /**
   * 添加合法性来源
   * @param {Object} legitimacySource - 合法性来源
   */
  addLegitimacySource(legitimacySource) {
    this.legitimacySources.push(legitimacySource);
  }

  /**
   * 设置稳定性评估
   * @param {string} stability - 稳定性评估
   */
  setStabilityAssessment(stability) {
    this.stabilityAssessment = stability;
  }
}

module.exports = {
  FieldType,
  AutonomyLevel,
  BoundaryType,
  Field,
  FieldBoundary,
  FieldAutonomy,
  FieldPosition,
  FieldRule,
  PowerStructure
};