/**
 * ANT转译理论类型定义
 * 严格遵循行动者网络理论的转译概念框架
 */

/**
 * 转译环节类型枚举
 */
const TranslationPhase = {
  PROBLEMATIZATION: 'problematization',     // 问题化
  INTERESSEMENT: 'interessement',           // 兴趣化
  ENROLLMENT: 'enrollment',                 // 招募
  MOBILIZATION: 'mobilization'              // 动员
};

/**
 * 问题化类型枚举
 */
const ProblematizationType = {
  PROBLEM_DEFINITION: 'problem_definition',   // 问题定义
  SOLUTION_PROPOSAL: 'solution_proposal',     // 解决方案
  OBLIGATORY_PASSAGE: 'obligatory_passage',   // 必经节点
  CONTROVERSY_FRAME: 'controversy_frame'       // 争议框架
};

/**
 * 兴趣化机制类型枚举
 */
const InteressementMechanism = {
  INCENTIVE_ALIGNMENT: 'incentive_alignment',   // 激励对齐
  PERSUASIVE_DEVICES: 'persuasive_devices',     // 说服装置
  ALTERNATIVE_ELIMINATION: 'alternative_elimination', // 替代方案消除
  INTEREST_REDEFINITION: 'interest_redefinition'   // 利益重新定义
};

/**
 * 招募策略类型枚举
 */
const EnrollmentStrategy = {
  DIRECT_ENROLLMENT: 'direct_enrollment',       // 直接招募
  SPONSORSHIP_ENROLLMENT: 'sponsorship_enrollment', // 赞助招募
  DELEGATION_ENROLLMENT: 'delegation_enrollment', // 委托招募
  COERCIVE_ENROLLMENT: 'coercive_enrollment'      // 强制招募
};

/**
 * 动员效果类型枚举
 */
const MobilizationEffect = {
  NETWORK_STABILIZATION: 'network_stabilization', // 网络稳定化
  BLACK_BOX_FORMATION: 'black_box_formation',     // 黑箱形成
  POWER_CONSOLIDATION: 'power_consolidation',     // 权力巩固
  LEGITIMACY_ESTABLISHMENT: 'legitimacy_establishment' // 合法性建立
};

/**
 * 转译过程数据结构
 */
class TranslationProcess {
  constructor(actorId, actorName, context) {
    this.id = this._generateId(actorId);
    this.actorId = actorId;
    this.actorName = actorName;
    this.context = context;

    this.phases = {
      problematization: null,
      interessement: null,
      enrollment: null,
      mobilization: null
    };

    this.timeline = [];
    this.obligatoryPassagePoints = [];
    this.controversyFrames = [];
    this.devices = [];
    this.actors = [];
  }

  /**
   * 设置问题化阶段
   * @param {Problematization} problematization - 问题化分析
   */
  setProblematization(problematization) {
    this.phases.problematization = problematization;
    this.addTimelineEvent('problematization_start', problematization.timestamp);
  }

  /**
   * 设置兴趣化阶段
   * @param {Interessement} interessement - 兴趣化分析
   */
  setInteressement(interessement) {
    this.phases.interessement = interessement;
    this.addTimelineEvent('interessement_start', interessement.timestamp);
  }

  /**
   * 设置招募阶段
   * @param {Enrollment} enrollment - 招募分析
   */
  setEnrollment(enrollment) {
    this.phases.enrollment = enrollment;
    this.addTimelineEvent('enrollment_start', enrollment.timestamp);
  }

  /**
   * 设置动员阶段
   * @param {Mobilization} mobilization - 动员分析
   */
  setMobilization(mobilization) {
    this.phases.mobilization = mobilization;
    this.addTimelineEvent('mobilization_start', mobilization.timestamp);
  }

  /**
   * 添加必经节点
   * @param {Object} passagePoint - 必经节点
   */
  addObligatoryPassagePoint(passagePoint) {
    this.obligatoryPassagePoints.push({
      ...passagePoint,
      id: this._generateId('opp'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加争议框架
   * @param {Object} controversy - 争议框架
   */
  addControversyFrame(controversy) {
    this.controversyFrames.push({
      ...controversy,
      id: this._generateId('controversy'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加装置或设备
   * @param {Object} device - 装置或设备
   */
  addDevice(device) {
    this.devices.push({
      ...device,
      id: this._generateId('device'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加行动者
   * @param {Object} actor - 行动者信息
   */
  addActor(actor) {
    this.actors.push({
      ...actor,
      id: this._generateId('actor'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加时间线事件
   * @private
   */
  addTimelineEvent(eventType, timestamp) {
    this.timeline.push({
      type: eventType,
      timestamp: timestamp || new Date().toISOString()
    });
  }

  /**
   * 评估转译完整性
   * @returns {Object} 完整性评估
   */
  assessCompleteness() {
    const phases = Object.keys(this.phases);
    const completedPhases = phases.filter(phase => this.phases[phase] !== null);

    return {
      totalPhases: phases.length,
      completedPhases: completedPhases.length,
      completenessRate: completedPhases.length / phases.length,
      missingPhases: phases.filter(phase => this.phases[phase] === null),
      isComplete: completedPhases.length === phases.length
    };
  }

  /**
   * 分析转译效果
   * @returns {Object} 效果分析
   */
  analyzeTranslationEffects() {
    const completeness = this.assessCompleteness();

    return {
      completeness: completeness,
      stabilityLevel: this._assessNetworkStability(),
      powerEffects: this._analyzePowerEffects(),
      legitimationLevel: this._assessLegitimation(),
      controversyResolution: this._analyzeControversyResolution()
    };
  }

  /**
   * 生成唯一ID
   * @private
   */
  _generateId(prefix) {
    return `${prefix}_${this.actorId}_${Date.now()}`;
  }

  /**
   * 评估网络稳定性
   * @private
   */
  _assessNetworkStability() {
    let stability = 0.5; // 基础稳定性

    if (this.phases.mobilization && this.phases.mobilization.effects) {
      if (this.phases.mobilization.effects.includes(MobilizationEffect.NETWORK_STABILIZATION)) {
        stability += 0.3;
      }
      if (this.phases.mobilization.effects.includes(MobilizationEffect.BLACK_BOX_FORMATION)) {
        stability += 0.2;
      }
    }

    return Math.min(1, stability);
  }

  /**
   * 分析权力效应
   * @private
   */
  _analyzePowerEffects() {
    const powerEffects = {
      positionalPower: 0,
      discursivePower: 0,
      networkPower: 0,
      totalPower: 0
    };

    if (this.phases.mobilization && this.phases.mobilization.powerGains) {
      powerEffects.positionalPower = this.phases.mobilization.powerGains.positional || 0;
      powerEffects.discursivePower = this.phases.mobilization.powerGains.discursive || 0;
      powerEffects.networkPower = this.phases.mobilization.powerGains.network || 0;
    }

    powerEffects.totalPower = (powerEffects.positionalPower +
                               powerEffects.discursivePower +
                               powerEffects.networkPower) / 3;

    return powerEffects;
  }

  /**
   * 评估合法性
   * @private
   */
  _assessLegitimation() {
    let legitimation = 0.5;

    if (this.phases.problematization && this.phases.problematization.legitimacySources) {
      legitimation += this.phases.problematization.legitimacySources.length * 0.1;
    }

    if (this.phases.mobilization && this.phases.mobilization.effects) {
      if (this.phases.mobilization.effects.includes(MobilizationEffect.LEGITIMACY_ESTABLISHMENT)) {
        legitimation += 0.3;
      }
    }

    return Math.min(1, legitimation);
  }

  /**
   * 分析争议解决
   * @private
   */
  _analyzeControversyResolution() {
    if (this.controversyFrames.length === 0) {
      return { status: 'no_controversy', resolution: 'complete' };
    }

    const resolvedFrames = this.controversyFrames.filter(frame =>
      frame.resolution && frame.resolution.status === 'resolved'
    );

    return {
      totalControversies: this.controversyFrames.length,
      resolvedControversies: resolvedFrames.length,
      resolutionRate: resolvedFrames.length / this.controversyFrames.length,
      status: this.controversyFrames.length > resolvedFrames.length ? 'partial' : 'complete'
    };
  }
}

/**
 * 问题化分析数据结构
 */
class Problematization {
  constructor() {
    this.problems = [];
    this.solutions = [];
    this.obligatoryPassagePoints = [];
    this.controversyDefinition = '';
    this.legitimacySources = [];
    this.timestamp = new Date().toISOString();
  }

  /**
   * 添加问题
   * @param {Object} problem - 问题定义
   */
  addProblem(problem) {
    this.problems.push({
      ...problem,
      id: this._generateId('problem'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加解决方案
   * @param {Object} solution - 解决方案
   */
  addSolution(solution) {
    this.solutions.push({
      ...solution,
      id: this._generateId('solution'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 设置争议定义
   * @param {string} definition - 争议定义
   */
  setControversyDefinition(definition) {
    this.controversyDefinition = definition;
  }

  /**
   * 添加合法性来源
   * @param {Object} legitimacy - 合法性来源
   */
  addLegitimacySource(legitimacy) {
    this.legitimacySources.push({
      ...legitimacy,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 生成唯一ID
   * @private
   */
  _generateId(prefix) {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

/**
 * 兴趣化分析数据结构
 */
class Interessement {
  constructor() {
    this.mechanisms = [];
    this.devices = [];
    this.interestAlignment = {};
    this.alternativeElimination = [];
    this.timestamp = new Date().toISOString();
  }

  /**
   * 添加机制
   * @param {Object} mechanism - 兴趣化机制
   */
  addMechanism(mechanism) {
    this.mechanisms.push({
      ...mechanism,
      id: this._generateId('mechanism'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加装置
   * @param {Object} device - 装置或设备
   */
  addDevice(device) {
    this.devices.push({
      ...device,
      id: this._generateId('device'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 设置利益对齐
   * @param {Object} alignment - 利益对齐分析
   */
  setInterestAlignment(alignment) {
    this.interestAlignment = alignment;
  }

  /**
   * 添加替代方案消除
   * @param {Object} elimination - 替代方案消除
   */
  addAlternativeElimination(elimination) {
    this.alternativeElimination.push({
      ...elimination,
      id: this._generateId('elimination'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 生成唯一ID
   * @private
   */
  _generateId(prefix) {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

/**
 * 招募分析数据结构
 */
class Enrollment {
  constructor() {
    this.strategies = [];
    this.enrolledActors = [];
    this.sponsors = [];
    this.enrollmentChallenges = [];
    this.timestamp = new Date().toISOString();
  }

  /**
   * 添加策略
   * @param {Object} strategy - 招募策略
   */
  addStrategy(strategy) {
    this.strategies.push({
      ...strategy,
      id: this._generateId('strategy'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加已招募的行动者
   * @param {Object} actor - 已招募的行动者
   */
  addEnrolledActor(actor) {
    this.enrolledActors.push({
      ...actor,
      id: this._generateId('enrolled'),
      enrollmentDate: new Date().toISOString()
    });
  }

  /**
   * 添加赞助者
   * @param {Object} sponsor - 赞助者信息
   */
  addSponsor(sponsor) {
    this.sponsors.push({
      ...sponsor,
      id: this._generateId('sponsor'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加招募挑战
   * @param {Object} challenge - 招募挑战
   */
  addEnrollmentChallenge(challenge) {
    this.enrollmentChallenges.push({
      ...challenge,
      id: this._generateId('challenge'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 生成唯一ID
   * @private
   */
  _generateId(prefix) {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

/**
 * 动员分析数据结构
 */
class Mobilization {
  constructor() {
    this.effects = [];
    this.blackBoxes = [];
    this.powerGains = {};
    this.stabilityMechanisms = [];
    this.legitimationProcesses = [];
    this.timestamp = new Date().toISOString();
  }

  /**
   * 添加效果
   * @param {Object} effect - 动员效果
   */
  addEffect(effect) {
    this.effects.push({
      ...effect,
      id: this._generateId('effect'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加黑箱
   * @param {Object} blackBox - 黑箱信息
   */
  addBlackBox(blackBox) {
    this.blackBoxes.push({
      ...blackBox,
      id: this._generateId('blackbox'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 设置权力获得
   * @param {Object} power - 权力获得分析
   */
  setPowerGains(power) {
    this.powerGains = power;
  }

  /**
   * 添加稳定性机制
   * @param {Object} mechanism - 稳定性机制
   */
  addStabilityMechanism(mechanism) {
    this.stabilityMechanisms.push({
      ...mechanism,
      id: this._generateId('stability'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 添加合法性过程
   * @param {Object} process - 合法性过程
   */
  addLegitimationProcess(process) {
    this.legitimationProcesses.push({
      ...process,
      id: this._generateId('legitimacy'),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 生成唯一ID
   * @private
   */
  _generateId(prefix) {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

module.exports = {
  TranslationPhase,
  ProblematizationType,
  InteressementMechanism,
  EnrollmentStrategy,
  MobilizationEffect,
  TranslationProcess,
  Problematization,
  Interessement,
  Enrollment,
  Mobilization
};