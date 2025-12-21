/**
 * 资本理论类型定义
 * 严格遵循布迪厄资本理论的概念框架
 */

/**
 * 资本类型枚举
 */
const CapitalType = {
  CULTURAL: 'cultural',           // 文化资本
  SOCIAL: 'social',              // 社会资本
  ECONOMIC: 'economic',          // 经济资本
  SYMBOLIC: 'symbolic',          // 象征资本
  // 中国特色扩展
  POLITICAL: 'political',        // 政治资本
  GUANXI: 'guanxi',             // 关系资本
  INSTITUTIONAL: 'institutional', // 制度资本
  REGIONAL: 'regional'           // 地域资本
};

/**
 * 资本形态枚举
 */
const CapitalForm = {
  EMBODIED: 'embodied',           // 具身化形态
  OBJECTIFIED: 'objectified',     // 客观化形态
  INSTITUTIONALIZED: 'institutionalized' // 制度化形态
};

/**
 * 资本转换效率级别
 */
const ConversionEfficiency = {
  VERY_HIGH: 'very_high',         // 极高效率
  HIGH: 'high',                   // 高效率
  MEDIUM: 'medium',               // 中等效率
  LOW: 'low',                     // 低效率
  VERY_LOW: 'very_low'            // 极低效率
};

/**
 * 资本数据结构
 */
class Capital {
  /**
   * @param {CapitalType} type - 资本类型
   * @param {number} amount - 资本数量 (0-100)
   * @param {CapitalForm} form - 资本形态
   * @param {Object} sources - 资本来源
   * @param {Object} characteristics - 资本特征
   */
  constructor(type, amount, form = CapitalForm.EMBODIED, sources = {}, characteristics = {}) {
    this.id = this._generateId(type, form);
    this.type = type;
    this.amount = Math.max(0, Math.min(100, amount)); // 确保在0-100范围内
    this.form = form;
    this.sources = sources;
    this.characteristics = characteristics;
    this.conversionRates = {};
    this.recognitionLevel = 0.5; // 默认中等认可度
  }

  /**
   * 设置转换率
   * @param {CapitalType} targetType - 目标资本类型
   * @param {number} rate - 转换率 (0-1)
   */
  setConversionRate(targetType, rate) {
    this.conversionRates[targetType] = Math.max(0, Math.min(1, rate));
  }

  /**
   * 获取转换率
   * @param {CapitalType} targetType - 目标资本类型
   * @returns {number} 转换率
   */
  getConversionRate(targetType) {
    return this.conversionRates[targetType] || 0;
  }

  /**
   * 设置认可度
   * @param {number} level - 认可度 (0-1)
   */
  setRecognitionLevel(level) {
    this.recognitionLevel = Math.max(0, Math.min(1, level));
  }

  /**
   * 获取资本价值
   * @returns {number} 资本价值（考虑认可度）
   */
  getValue() {
    return this.amount * this.recognitionLevel;
  }

  /**
   * 生成唯一ID
   * @private
   */
  _generateId(type, form) {
    return `${type}_${form}_${Date.now()}`;
  }
}

/**
 * 资本组合数据结构
 */
class CapitalPortfolio {
  constructor(actorId, actorName) {
    this.actorId = actorId;
    this.actorName = actorName;
    this.capitals = new Map();
    this.conversionHistory = [];
    this.competitionStrategies = [];
    this.reproductionMechanisms = [];
  }

  /**
   * 添加资本
   * @param {Capital} capital - 资本对象
   */
  addCapital(capital) {
    this.capitals.set(capital.type, capital);
  }

  /**
   * 获取资本
   * @param {CapitalType} type - 资本类型
   * @returns {Capital|null} 资本对象
   */
  getCapital(type) {
    return this.capitals.get(type) || null;
  }

  /**
   * 获取总资本价值
   * @returns {number} 总资本价值
   */
  getTotalCapitalValue() {
    let totalValue = 0;
    for (const capital of this.capitals.values()) {
      totalValue += capital.getValue();
    }
    return totalValue;
  }

  /**
   * 获取主导资本类型
   * @returns {CapitalType} 主导资本类型
   */
  getDominantCapitalType() {
    let maxValue = 0;
    let dominantType = null;

    for (const [type, capital] of this.capitals.entries()) {
      if (capital.getValue() > maxValue) {
        maxValue = capital.getValue();
        dominantType = type;
      }
    }

    return dominantType;
  }

  /**
   * 记录资本转换
   * @param {Object} conversion - 转换记录
   */
  recordConversion(conversion) {
    this.conversionHistory.push({
      ...conversion,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加竞争策略
   * @param {Object} strategy - 竞争策略
   */
  addCompetitionStrategy(strategy) {
    this.competitionStrategies.push({
      ...strategy,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加再生产机制
   * @param {Object} mechanism - 再生产机制
   */
  addReproductionMechanism(mechanism) {
    this.reproductionMechanisms.push({
      ...mechanism,
      timestamp: new Date().toISOString()
    });
  }
}

/**
 * 资本转换分析结果
 */
class CapitalConversionAnalysis {
  constructor() {
    this.conversionMatrix = new Map();
    this.conversionEfficiency = {};
    this.conversionBarriers = [];
    this.optimalConversionPaths = [];
    this.conversionStrategies = [];
  }

  /**
   * 设置转换矩阵
   * @param {CapitalType} fromType - 源资本类型
   * @param {CapitalType} toType - 目标资本类型
   * @param {number} efficiency - 转换效率
   */
  setConversionEfficiency(fromType, toType, efficiency) {
    if (!this.conversionMatrix.has(fromType)) {
      this.conversionMatrix.set(fromType, new Map());
    }
    this.conversionMatrix.get(fromType).set(toType, efficiency);

    this.conversionEfficiency[`${fromType}_to_${toType}`] = efficiency;
  }

  /**
   * 获取转换效率
   * @param {CapitalType} fromType - 源资本类型
   * @param {CapitalType} toType - 目标资本类型
   * @returns {number} 转换效率
   */
  getConversionEfficiency(fromType, toType) {
    return this.conversionEfficiency[`${fromType}_to_${toType}`] || 0;
  }

  /**
   * 添加转换障碍
   * @param {Object} barrier - 转换障碍
   */
  addConversionBarrier(barrier) {
    this.conversionBarriers.push(barrier);
  }

  /**
   * 添加最优转换路径
   * @param {Array} path - 转换路径
   */
  addOptimalConversionPath(path) {
    this.optimalConversionPaths.push({
      path: path,
      efficiency: this._calculatePathEfficiency(path),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 计算路径效率
   * @private
   */
  _calculatePathEfficiency(path) {
    let totalEfficiency = 1;
    for (let i = 0; i < path.length - 1; i++) {
      const fromType = path[i];
      const toType = path[i + 1];
      totalEfficiency *= this.getConversionEfficiency(fromType, toType);
    }
    return totalEfficiency;
  }
}

/**
 * 习性模式数据结构
 */
class HabitusPattern {
  /**
   * @param {string} patternName - 模式名称
   * @param {Array<string>} dispositions - 倾向
   * @param {Array<string}> practices - 实践方式
   * @param {Array<string}> expectations - 期望
   * @param {number} strength - 模式强度 (0-1)
   */
  constructor(patternName, dispositions = [], practices = [], expectations = [], strength = 0.5) {
    this.id = this._generateId(patternName);
    this.patternName = patternName;
    this.dispositions = dispositions;
    this.practices = practices;
    this.expectations = expectations;
    this.strength = Math.max(0, Math.min(1, strength));
    this.formationContext = {};
    this.variations = [];
  }

  /**
   * 设置形成背景
   * @param {Object} context - 形成背景
   */
  setFormationContext(context) {
    this.formationContext = context;
  }

  /**
   * 添加变异
   * @param {Object} variation - 变异模式
   */
  addVariation(variation) {
    this.variations.push({
      ...variation,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 预测行为
   * @param {Object} situation - 情境
   * @returns {Object} 行为预测
   */
  predictBehavior(situation) {
    return {
      likelyAction: this._predictAction(situation),
      confidence: this.strength,
      rationalization: this._generateRationalization(situation)
    };
  }

  /**
   * 生成唯一ID
   * @private
   */
  _generateId(patternName) {
    return `habitus_${patternName.replace(/\s+/g, '_').toLowerCase()}_${Date.now()}`;
  }

  /**
   * 预测行动
   * @private
   */
  _predictAction(situation) {
    // 基于倾向预测行动的简化逻辑
    return this.dispositions[0] || 'default_action';
  }

  /**
   * 生成合理化解释
   * @private
   */
  _generateRationalization(situation) {
    return `基于${this.patternName}的行为模式，在${situation.type}情境中的合理反应`;
  }
}

/**
 * 场域竞争动态数据结构
 */
class FieldCompetition {
  constructor(fieldType) {
    this.fieldType = fieldType;
    this.competitionForms = [];
    this.stakeDistribution = {};
    this.competitionRules = [];
    this.conflictAreas = [];
    this.changeDrivers = [];
    this.mobilityOpportunities = [];
  }

  /**
   * 添加竞争形式
   * @param {Object} competition - 竞争形式
   */
  addCompetitionForm(competition) {
    this.competitionForms.push({
      ...competition,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 设置利益分配
   * @param {Object} distribution - 利益分配
   */
  setStakeDistribution(distribution) {
    this.stakeDistribution = distribution;
  }

  /**
   * 添加竞争规则
   * @param {Object} rule - 竞争规则
   */
  addCompetitionRule(rule) {
    this.competitionRules.push(rule);
  }

  /**
   * 添加冲突区域
   * @param {Object} conflict - 冲突区域
   */
  addConflictArea(conflict) {
    this.conflictAreas.push({
      ...conflict,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加变化驱动因素
   * @param {Object} driver - 变化驱动因素
   */
  addChangeDriver(driver) {
    this.changeDrivers.push({
      ...driver,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加流动性机会
   * @param {Object} opportunity - 流动性机会
   */
  addMobilityOpportunity(opportunity) {
    this.mobilityOpportunities.push({
      ...opportunity,
      timestamp: new Date().toISOString()
    });
  }
}

module.exports = {
  CapitalType,
  CapitalForm,
  ConversionEfficiency,
  Capital,
  CapitalPortfolio,
  CapitalConversionAnalysis,
  HabitusPattern,
  FieldCompetition
};