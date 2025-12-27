/**
 * 信息验证专家技能实现
 * 遵循agentskills.io规范和渐进式披露原则
 * 定量分析程序化，定性分析AI化
 */

class InformationVerificationSkill {
  constructor() {
    this.skillId = "information-verification";
    this.version = "2.0.0";
    this.name = "信息验证专家";
    this.description = "基于信息科学和验证理论，对企业信息来源、准确性、可信度和时效性进行全面验证";
    
    // 初始化模块
    this.validationProcessor = new InformationValidationProcessor();
    this.sourceVerifier = new SourceVerificationModule();
    this.accuracyValidator = new AccuracyValidationModule();
    this.credibilityAssessor = new CredibilityAssessmentModule();
    this.integrityChecker = new DataIntegrityModule();
    this.reporter = new InformationReportingModule();
  }

  /**
   * 执行技能主方法
   * 实现渐进式披露：根据参数决定验证详略程度
   */
  async execute(inputs) {
    try {
      // 验证输入参数
      this.validateInputs(inputs);
      
      // 根据验证类型执行相应的验证
      let verificationResult;
      const config = inputs.config || {};
      const depth = config.depth || 'standard';
      
      switch(inputs.verificationType) {
        case 'source-verification':
          verificationResult = await this.sourceVerifier.verify(inputs.information, config);
          break;
        case 'accuracy-check':
          verificationResult = await this.accuracyValidator.validate(inputs.information, config);
          break;
        case 'credibility-assessment':
          verificationResult = await this.credibilityAssessor.assess(inputs.information, config);
          break;
        case 'data-integrity':
          verificationResult = await this.integrityChecker.check(inputs.information, config);
          break;
        case 'comprehensive-verification':
          verificationResult = await this.performComprehensiveVerification(inputs.information, config);
          break;
        default:
          // 默认执行基本验证
          verificationResult = await this.performBasicVerification(inputs.information, config);
      }
      
      // 生成验证报告
      const finalReport = await this.reporter.generate({
        verificationType: inputs.verificationType,
        result: verificationResult,
        recommendations: await this.generateRecommendations(verificationResult, inputs)
      }, depth);
      
      return {
        success: true,
        data: finalReport,
        metadata: {
          skillId: this.skillId,
          version: this.version,
          executionTime: new Date().toISOString(),
          contextLevel: depth,
          verificationType: inputs.verificationType
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
    if (!inputs || !inputs.information) {
      throw new Error("缺少必需的information参数");
    }
    
    if (!inputs.verificationType) {
      throw new Error("缺少必需的verificationType参数");
    }
  }

  /**
   * 执行综合验证
   */
  async performComprehensiveVerification(information, config) {
    // 并行执行多种验证
    const [sourceResult, accuracyResult, credibilityResult, integrityResult] = 
      await Promise.allSettled([
        this.sourceVerifier.verify(information, config),
        this.accuracyValidator.validate(information, config),
        this.credibilityAssessor.assess(information, config),
        this.integrityChecker.check(information, config)
      ]);
    
    const results = {
      source: sourceResult.status === 'fulfilled' ? sourceResult.value : null,
      accuracy: accuracyResult.status === 'fulfilled' ? accuracyResult.value : null,
      credibility: credibilityResult.status === 'fulfilled' ? credibilityResult.value : null,
      integrity: integrityResult.status === 'fulfilled' ? integrityResult.value : null
    };
    
    // 计算综合验证结果
    const allScores = [
      results.source?.confidenceScore || 0,
      results.accuracy?.confidenceScore || 0,
      results.credibility?.confidenceScore || 0,
      results.integrity?.confidenceScore || 0
    ].filter(score => score > 0);
    
    const overallScore = allScores.length > 0 
      ? allScores.reduce((a, b) => a + b, 0) / allScores.length 
      : 0;
    
    const issues = [];
    for (const [key, result] of Object.entries(results)) {
      if (result && result.issues) {
        issues.push(...result.issues.map(issue => ({
          ...issue,
          verificationType: key
        })));
      }
    }
    
    return {
      isVerified: overallScore >= 70,
      confidenceScore: overallScore,
      details: {
        sourceCredibility: results.source?.confidenceScore || 0,
        accuracyLevel: results.accuracy?.confidenceScore || 0,
        credibilityScore: results.credibility?.confidenceScore || 0,
        integrityScore: results.integrity?.confidenceScore || 0
      },
      issues: issues
    };
  }

  /**
   * 执行基本验证
   */
  async performBasicVerification(information, config) {
    // 执行基础的验证流程
    const sourceResult = await this.sourceVerifier.verify(information, config);
    
    return {
      isVerified: sourceResult.isVerified,
      confidenceScore: sourceResult.confidenceScore,
      details: sourceResult.details,
      issues: sourceResult.issues || []
    };
  }

  /**
   * 生成验证建议
   */
  async generateRecommendations(verificationResult, inputs) {
    const recommendations = [];
    
    // 根据验证结果生成建议
    if (verificationResult.confidenceScore < 70) {
      recommendations.push("验证置信度较低，建议使用更多权威信息源进行交叉验证");
    }
    
    if (verificationResult.issues && verificationResult.issues.length > 0) {
      const criticalIssues = verificationResult.issues.filter(issue => issue.severity === 'critical');
      if (criticalIssues.length > 0) {
        recommendations.push("发现严重验证问题，需要立即核实相关信息");
      }
    }
    
    // 根据验证类型提供特定建议
    switch(inputs.verificationType) {
      case 'source-verification':
        recommendations.push("确认信息来源的权威性和更新频率");
        break;
      case 'accuracy-check':
        recommendations.push("使用多个独立数据源验证关键数据点");
        break;
      case 'timeliness-check':
        recommendations.push("建立信息更新提醒机制，确保信息时效性");
        break;
    }
    
    return recommendations;
  }
}

/**
 * 信息验证处理器
 * 程序化执行基础验证任务
 */
class InformationValidationProcessor {
  async process(rawInformation) {
    // 信息预处理
    return {
      original: rawInformation,
      processed: this.normalizeInformation(rawInformation),
      metadata: this.extractMetadata(rawInformation)
    };
  }
  
  normalizeInformation(info) {
    // 标准化信息格式
    if (typeof info === 'string') {
      try {
        return JSON.parse(info);
      } catch {
        return { text: info };
      }
    }
    return info;
  }
  
  extractMetadata(info) {
    // 提取信息元数据
    const metadata = {
      size: JSON.stringify(info).length,
      type: typeof info,
      contains: []
    };
    
    if (typeof info === 'object') {
      metadata.contains = Object.keys(info);
    }
    
    return metadata;
  }
}

/**
 * 来源验证模块
 * 验证信息来源的可信度
 */
class SourceVerificationModule {
  async verify(information, config = {}) {
    const processedInfo = await new InformationValidationProcessor().process(information);
    const source = processedInfo.processed.source || processedInfo.processed.dataSource || 'unknown';
    
    // 检查是否为权威信息源
    const authoritativeSources = config.authoritativeSources || [
      '政府官网', '上市公司公告', '官方统计数据', 
      '学术期刊', '权威媒体', '行业协会'
    ];
    
    const isAuthoritative = authoritativeSources.some(authSource => 
      source.toLowerCase().includes(authSource.toLowerCase())
    );
    
    // 评估来源可信度
    const credibilityFactors = {
      authority: isAuthoritative ? 0.9 : 0.3,
      reputation: this.assessSourceReputation(source),
      independence: this.assessSourceIndependence(processedInfo.processed),
      transparency: this.assessSourceTransparency(processedInfo.processed)
    };
    
    const credibilityScore = this.calculateCredibilityScore(credibilityFactors);
    
    // 检查来源问题
    const issues = this.identifySourceIssues(processedInfo.processed, credibilityFactors);
    
    return {
      isVerified: credibilityScore >= 70,
      confidenceScore: credibilityScore,
      details: {
        source: source,
        isAuthoritative: isAuthoritative,
        credibilityFactors: credibilityFactors,
        reviewDate: new Date().toISOString()
      },
      issues: issues
    };
  }
  
  assessSourceReputation(source) {
    // 简化的来源声誉评估
    const authoritativeSources = [
      '政府', '官方', '上市', '统计', '学术', '研究', '协会'
    ];
    
    if (authoritativeSources.some(term => 
      source.toLowerCase().includes(term)
    )) {
      return 0.9;
    }
    
    // 检查是否为可疑来源
    const suspiciousSources = [
      'unverified', 'anonymous', 'rumor', 'speculation'
    ];
    
    if (suspiciousSources.some(term => 
      source.toLowerCase().includes(term.toLowerCase())
    )) {
      return 0.2;
    }
    
    return 0.6; // 默认中等声誉
  }
  
  assessSourceIndependence(info) {
    // 评估来源独立性
    if (info.hasOwnProperty('fundedBy') || info.hasOwnProperty('sponsoredBy')) {
      return 0.4; // 有资金关系，独立性较低
    }
    return 0.8; // 默认较高独立性
  }
  
  assessSourceTransparency(info) {
    // 评估来源透明度
    const hasAuthor = info.hasOwnProperty('author') || info.hasOwnProperty('authorName');
    const hasDate = info.hasOwnProperty('date') || info.hasOwnProperty('publishedDate');
    const hasMethodology = info.hasOwnProperty('methodology') || info.hasOwnProperty('sourceMethod');
    
    const transparencyScore = (hasAuthor ? 0.3 : 0) + 
                             (hasDate ? 0.3 : 0) + 
                             (hasMethodology ? 0.4 : 0);
    
    return transparencyScore;
  }
  
  calculateCredibilityScore(factors) {
    // 计算综合可信度分数
    const weights = {
      authority: 0.3,
      reputation: 0.3,
      independence: 0.2,
      transparency: 0.2
    };
    
    return Math.round(
      factors.authority * weights.authority * 100 +
      factors.reputation * weights.reputation * 100 +
      factors.independence * weights.independence * 100 +
      factors.transparency * weights.transparency * 100
    );
  }
  
  identifySourceIssues(info, factors) {
    const issues = [];
    
    if (factors.authority < 0.5) {
      issues.push({
        type: 'low-authority-source',
        severity: 'high',
        description: '信息来源权威性不足',
        suggestion: '使用官方或权威第三方来源验证信息'
      });
    }
    
    if (factors.independence < 0.5) {
      issues.push({
        type: 'potential-bias',
        severity: 'medium',
        description: '信息来源可能存在利益关联',
        suggestion: '寻找独立第三方验证'
      });
    }
    
    if (factors.transparency < 0.5) {
      issues.push({
        type: 'lack-of-transparency',
        severity: 'medium',
        description: '信息来源透明度不足',
        suggestion: '寻找提供更多信息的来源'
      });
    }
    
    return issues;
  }
}

/**
 * 准确性验证模块
 * 验证信息内容的准确性
 */
class AccuracyValidationModule {
  async validate(information, config = {}) {
    const processedInfo = await new InformationValidationProcessor().process(information);
    const tolerance = config.toleranceLevel || 0.05; // 默认5%容差
    
    // 检查数据格式和逻辑
    const formatIssues = this.checkFormatIssues(processedInfo.processed);
    if (formatIssues.length > 0) {
      return {
        isVerified: false,
        confidenceScore: 30,
        details: {
          formatCompliance: false,
          formatIssues: formatIssues
        },
        issues: formatIssues
      };
    }
    
    // 检查逻辑一致性
    const logicIssues = this.checkLogicIssues(processedInfo.processed);
    
    // 评估准确性
    const accuracyScore = this.calculateAccuracyScore(processedInfo.processed, tolerance);
    
    // 合并问题
    const allIssues = [...formatIssues, ...logicIssues];
    
    return {
      isVerified: accuracyScore >= 70 && allIssues.length === 0,
      confidenceScore: accuracyScore,
      details: {
        formatCompliance: formatIssues.length === 0,
        logicConsistency: logicIssues.length === 0,
        toleranceLevel: tolerance,
        accuracyAssessment: this.getAccuracyLevel(accuracyScore)
      },
      issues: allIssues
    };
  }
  
  checkFormatIssues(info) {
    const issues = [];
    
    // 检查数值格式
    for (const [key, value] of Object.entries(info)) {
      if (typeof value === 'string') {
        // 检查是否应该是数值但格式错误
        if (key.toLowerCase().includes('amount') || 
            key.toLowerCase().includes('revenue') ||
            key.toLowerCase().includes('number') ||
            key.toLowerCase().includes('percentage')) {
          const numValue = parseFloat(value);
          if (isNaN(numValue) && value.trim() !== '') {
            issues.push({
              type: 'format-error',
              severity: 'high',
              description: `字段 ${key} 应为数值格式，但实际为: ${value}`,
              suggestion: `将 ${key} 转换为正确的数值格式`
            });
          }
        }
      }
    }
    
    return issues;
  }
  
  checkLogicIssues(info) {
    const issues = [];
    
    // 检查逻辑一致性
    if (typeof info === 'object') {
      // 检查收入和利润的逻辑关系
      if (info.netProfit && info.revenue && info.netProfit > info.revenue) {
        issues.push({
          type: 'logic-error',
          severity: 'critical',
          description: '净利润不应大于营业收入',
          suggestion: '检查数据准确性'
        });
      }
      
      // 检查比例数据的逻辑
      if (info.percentage && typeof info.percentage === 'number' && 
          (info.percentage < 0 || info.percentage > 100)) {
        issues.push({
          type: 'logic-error',
          severity: 'high',
          description: '百分比数据超出合理范围(0-100%)',
          suggestion: '确认百分比数据的计算方法'
        });
      }
      
      // 检查日期逻辑
      if (info.startDate && info.endDate) {
        const start = new Date(info.startDate);
        const end = new Date(info.endDate);
        if (start > end) {
          issues.push({
            type: 'logic-error',
            severity: 'high',
            description: '开始日期不应晚于结束日期',
            suggestion: '检查日期数据的准确性'
          });
        }
      }
    }
    
    return issues;
  }
  
  calculateAccuracyScore(info, tolerance) {
    // 基于逻辑检查结果计算准确性分数
    const logicIssues = this.checkLogicIssues(info);
    const formatIssues = this.checkFormatIssues(info);
    
    const totalIssues = logicIssues.length + formatIssues.length;
    
    // 基础分数为100，每个问题扣10分
    let score = Math.max(0, 100 - (totalIssues * 10));
    
    // 如果有严重问题，分数更低
    const criticalIssues = [...logicIssues, ...formatIssues].filter(issue => issue.severity === 'critical');
    score = Math.max(0, score - (criticalIssues.length * 20));
    
    return score;
  }
  
  getAccuracyLevel(score) {
    if (score >= 90) return '非常高';
    if (score >= 80) return '高';
    if (score >= 70) return '中等';
    if (score >= 60) return '较低';
    return '低';
  }
}

/**
 * 可信度评估模块
 * 评估信息的整体可信度
 */
class CredibilityAssessmentModule {
  async assess(information, config = {}) {
    const processedInfo = await new InformationValidationProcessor().process(information);
    
    // 多维度评估可信度
    const assessment = {
      consistency: this.assessConsistency(processedInfo.processed),
      plausibility: this.assessPlausibility(processedInfo.processed),
      corroboration: this.assessCorroboration(processedInfo.processed),
      documentation: this.assessDocumentation(processedInfo.processed)
    };
    
    const credibilityScore = this.calculateCredibilityScore(assessment);
    const issues = this.identifyCredibilityIssues(processedInfo.processed, assessment);
    
    return {
      isVerified: credibilityScore >= 75,
      confidenceScore: credibilityScore,
      details: {
        ...assessment,
        overallCredibility: this.getCredibilityLevel(credibilityScore)
      },
      issues: issues
    };
  }
  
  assessConsistency(info) {
    // 评估信息内部一致性
    if (typeof info !== 'object') return 0.5;
    
    let consistentCount = 0;
    let totalCount = 0;
    
    // 检查数值间的一致性
    if (info.total && info.part1 && info.part2) {
      totalCount++;
      if (Math.abs(info.total - (info.part1 + info.part2)) < info.total * 0.01) { // 1%容差
        consistentCount++;
      }
    }
    
    // 检查百分比总和
    if (info.percentage1 && info.percentage2 && info.percentage3) {
      totalCount++;
      const totalPercentage = info.percentage1 + info.percentage2 + info.percentage3;
      if (Math.abs(totalPercentage - 100) < 1) {
        consistentCount++;
      }
    }
    
    return totalCount > 0 ? consistentCount / totalCount : 0.7; // 默认中等一致
  }
  
  assessPlausibility(info) {
    // 评估信息的合理性
    if (typeof info !== 'object') return 0.5;
    
    // 检查异常值
    const checks = [];
    
    // 检查收入增长率是否合理
    if (info.revenueGrowth) {
      if (Math.abs(info.revenueGrowth) > 200) { // 超过200%的增长需要验证
        checks.push(0.3); // 合理性较低
      } else if (Math.abs(info.revenueGrowth) > 50) {
        checks.push(0.6); // 中等合理性
      } else {
        checks.push(0.9); // 高合理性
      }
    }
    
    // 检查员工数量是否合理
    if (info.numberOfEmployees) {
      if (info.numberOfEmployees > 1000000) {
        checks.push(0.4); // 对于大部分公司，员工数过高
      } else if (info.numberOfEmployees > 0) {
        checks.push(0.8); // 合理范围
      } else {
        checks.push(0.2); // 负数或零可能有问题
      }
    }
    
    return checks.length > 0 ? checks.reduce((a, b) => a + b, 0) / checks.length : 0.7;
  }
  
  assessCorroboration(info) {
    // 评估信息可验证性（基于可用的验证信息）
    // 在实际实现中，这会查询其他数据源进行交叉验证
    // 这里我们基于信息的详细程度进行评估
    
    if (typeof info !== 'object') return 0.4;
    
    const keys = Object.keys(info);
    const detailedFields = keys.filter(key => 
      key.toLowerCase().includes('date') || 
      key.toLowerCase().includes('source') ||
      key.toLowerCase().includes('method') ||
      key.toLowerCase().includes('reference')
    );
    
    return detailedFields.length > 0 ? 0.8 : 0.5;
  }
  
  assessDocumentation(info) {
    // 评估信息的文档完整性
    if (typeof info !== 'object') return 0.3;
    
    const hasDate = info.hasOwnProperty('date') || info.hasOwnProperty('publishedDate');
    const hasSource = info.hasOwnProperty('source') || info.hasOwnProperty('dataSource');
    const hasMethod = info.hasOwnProperty('method') || info.hasOwnProperty('methodology');
    
    const documentationScore = (hasDate ? 0.3 : 0) + 
                              (hasSource ? 0.4 : 0) + 
                              (hasMethod ? 0.3 : 0);
    
    return documentationScore;
  }
  
  calculateCredibilityScore(assessment) {
    const weights = {
      consistency: 0.25,
      plausibility: 0.3,
      corroboration: 0.25,
      documentation: 0.2
    };
    
    return Math.round(
      assessment.consistency * weights.consistency * 100 +
      assessment.plausibility * weights.plausibility * 100 +
      assessment.corroboration * weights.corroboration * 100 +
      assessment.documentation * weights.documentation * 100
    );
  }
  
  identifyCredibilityIssues(info, assessment) {
    const issues = [];
    
    if (assessment.consistency < 0.6) {
      issues.push({
        type: 'inconsistency',
        severity: 'high',
        description: '信息内部存在不一致',
        suggestion: '检查数据计算和记录方法'
      });
    }
    
    if (assessment.plausibility < 0.5) {
      issues.push({
        type: 'implausibility',
        severity: 'high',
        description: '信息内容不合理',
        suggestion: '验证信息来源和计算方法'
      });
    }
    
    if (assessment.documentation < 0.5) {
      issues.push({
        type: 'poor-documentation',
        severity: 'medium',
        description: '信息缺乏必要的文档支撑',
        suggestion: '提供更多来源和方法说明'
      });
    }
    
    return issues;
  }
  
  getCredibilityLevel(score) {
    if (score >= 90) return '非常高';
    if (score >= 80) return '高';
    if (score >= 70) return '中等';
    if (score >= 60) return '较低';
    return '低';
  }
}

/**
 * 数据完整性检查模块
 * 检查数据的完整性
 */
class DataIntegrityModule {
  async check(information, config = {}) {
    const processedInfo = await new InformationValidationProcessor().process(information);
    
    // 检查完整性
    const completenessResult = this.assessCompleteness(processedInfo.processed);
    const integrityResult = this.assessIntegrity(processedInfo.processed);
    
    const issues = [
      ...this.identifyCompletenessIssues(processedInfo.processed),
      ...this.identifyIntegrityIssues(processedInfo.processed)
    ];
    
    const overallScore = Math.round((completenessResult.score + integrityResult.score) / 2);
    
    return {
      isVerified: overallScore >= 80 && issues.length === 0,
      confidenceScore: overallScore,
      details: {
        completeness: completenessResult,
        integrity: integrityResult,
        requiredFields: completenessResult.requiredPresent,
        optionalFields: completenessResult.optionalPresent
      },
      issues: issues
    };
  }
  
  assessCompleteness(info) {
    if (typeof info !== 'object') {
      return {
        score: 30,
        requiredPresent: 0,
        optionalPresent: 0,
        totalRequired: 1,
        totalOptional: 0
      };
    }
    
    // 定义关键字段
    const requiredFields = [
      'name', 'date', 'value', 'source', 'type', 
      'revenue', 'profit', 'assets', 'liabilities'
    ];
    
    const optionalFields = [
      'description', 'methodology', 'contact', 
      'industry', 'location', 'employees'
    ];
    
    let requiredPresent = 0;
    let optionalPresent = 0;
    
    for (const field of requiredFields) {
      if (info.hasOwnProperty(field) && info[field] != null && info[field] !== '') {
        requiredPresent++;
      }
    }
    
    for (const field of optionalFields) {
      if (info.hasOwnProperty(field) && info[field] != null && info[field] !== '') {
        optionalPresent++;
      }
    }
    
    const score = Math.round((requiredPresent / requiredFields.length) * 100);
    
    return {
      score: score,
      requiredPresent: requiredPresent,
      optionalPresent: optionalPresent,
      totalRequired: requiredFields.length,
      totalOptional: optionalFields.length
    };
  }
  
  assessIntegrity(info) {
    // 检查数据结构完整性
    if (typeof info !== 'object') {
      return {
        score: 40,
        issues: ['数据类型不正确']
      };
    }
    
    const issues = [];
    
    // 检查是否有空值
    for (const [key, value] of Object.entries(info)) {
      if (value === null || value === undefined || value === '') {
        issues.push(`字段 ${key} 为空`);
      }
    }
    
    // 检查数据类型
    for (const [key, value] of Object.entries(info)) {
      if (key.toLowerCase().includes('date') && typeof value === 'string') {
        const date = new Date(value);
        if (isNaN(date.getTime())) {
          issues.push(`日期字段 ${key} 格式不正确: ${value}`);
        }
      }
    }
    
    const score = Math.max(0, 100 - (issues.length * 10));
    
    return {
      score: score,
      issues: issues
    };
  }
  
  identifyCompletenessIssues(info) {
    const issues = [];
    
    if (typeof info === 'object') {
      // 检查关键字段缺失
      const requiredFields = ['name', 'date', 'value'];
      for (const field of requiredFields) {
        if (!info.hasOwnProperty(field) || info[field] == null || info[field] === '') {
          issues.push({
            type: 'missing-required-field',
            severity: 'high',
            description: `缺少关键字段: ${field}`,
            suggestion: `提供完整的 ${field} 信息`
          });
        }
      }
    } else {
      issues.push({
        type: 'invalid-format',
        severity: 'critical',
        description: '信息格式不正确，无法解析',
        suggestion: '提供结构化的信息'
      });
    }
    
    return issues;
  }
  
  identifyIntegrityIssues(info) {
    const issues = [];
    
    if (typeof info === 'object') {
      // 检查数据类型错误
      for (const [key, value] of Object.entries(info)) {
        if (key.toLowerCase().includes('amount') || 
            key.toLowerCase().includes('revenue') ||
            key.toLowerCase().includes('number')) {
          if (typeof value !== 'number' && isNaN(parseFloat(value))) {
            issues.push({
              type: 'type-mismatch',
              severity: 'high',
              description: `字段 ${key} 应为数值类型，实际为 ${typeof value}`,
              suggestion: `将 ${key} 转换为数值类型`
            });
          }
        }
      }
    }
    
    return issues;
  }
}

/**
 * 信息验证报告生成模块
 */
class InformationReportingModule {
  async generate(reportData, depth = 'standard') {
    const { verificationType, result, recommendations } = reportData;
    
    // 根据深度生成不同详细程度的报告
    if (depth === 'basic') {
      return this.generateBasicReport(verificationType, result, recommendations);
    } else if (depth === 'comprehensive') {
      return this.generateComprehensiveReport(verificationType, result, recommendations);
    } else {
      return this.generateStandardReport(verificationType, result, recommendations);
    }
  }
  
  generateBasicReport(verificationType, result, recommendations) {
    return {
      verification: {
        type: verificationType,
        result: {
          isVerified: result.isVerified,
          confidenceScore: result.confidenceScore,
          summary: `验证结果: ${result.isVerified ? '通过' : '未通过'}, 置信度: ${result.confidenceScore}%`
        }
      },
      recommendations: recommendations,
      dataQualityReport: {
        overallScore: result.confidenceScore,
        resultSummary: result.isVerified ? '验证通过' : '验证未通过',
        issuesCount: result.issues ? result.issues.length : 0
      },
      metadata: {
        generationTime: new Date().toISOString(),
        depth: 'basic',
        validationScore: result.confidenceScore
      }
    };
  }
  
  generateStandardReport(verificationType, result, recommendations) {
    return {
      verification: {
        type: verificationType,
        result: {
          isVerified: result.isVerified,
          confidenceScore: result.confidenceScore,
          details: result.details,
          issues: result.issues || []
        }
      },
      recommendations: recommendations,
      dataQualityReport: {
        overallScore: result.confidenceScore,
        strengths: this.extractStrengths(result),
        weaknesses: this.extractWeaknesses(result),
        issues: result.issues || [],
        riskLevel: this.assessRiskLevel(result)
      },
      metadata: {
        generationTime: new Date().toISOString(),
        depth: 'standard',
        validationScore: result.confidenceScore
      }
    };
  }
  
  generateComprehensiveReport(verificationType, result, recommendations) {
    return {
      verification: {
        type: verificationType,
        result: {
          isVerified: result.isVerified,
          confidenceScore: result.confidenceScore,
          details: result.details,
          issues: result.issues || [],
          rawResult: result // 包含原始结果以便深入分析
        }
      },
      recommendations: recommendations,
      dataQualityReport: {
        overallScore: result.confidenceScore,
        detailedAnalysis: {
          ...result.details,
          issuesBreakdown: this.categorizeIssues(result.issues || [])
        },
        strengths: this.extractStrengths(result),
        weaknesses: this.extractWeaknesses(result),
        verificationSteps: [
          '数据格式检查',
          '逻辑一致性验证',
          '来源可信度评估',
          '完整性检查'
        ],
        issues: result.issues || [],
        riskLevel: this.assessRiskLevel(result),
        confidenceInterval: this.calculateConfidenceInterval(result.confidenceScore)
      },
      metadata: {
        generationTime: new Date().toISOString(),
        depth: 'comprehensive',
        validationScore: result.confidenceScore,
        verificationProcess: {
          steps: ['input-validation', 'multi-dimension-check', 'result-aggregation', 'report-generation'],
          duration: 'processed'
        }
      }
    };
  }
  
  extractStrengths(result) {
    const strengths = [];
    
    if (result.confidenceScore >= 90) strengths.push('高置信度');
    if (result.details?.sourceCredibility >= 90) strengths.push('来源权威');
    if (result.details?.accuracyLevel >= 85) strengths.push('准确性高');
    if (result.details?.completenessScore >= 90) strengths.push('数据完整');
    if (result.details?.timelinessScore >= 90) strengths.push('时效性强');
    
    return strengths.length > 0 ? strengths : ['信息质量良好'];
  }
  
  extractWeaknesses(result) {
    const weaknesses = [];
    
    if (result.confidenceScore < 70) weaknesses.push('整体置信度较低');
    if (result.details?.sourceCredibility < 70) weaknesses.push('来源可信度不足');
    if (result.details?.accuracyLevel < 70) weaknesses.push('准确性待提高');
    if (result.issues && result.issues.length > 0) {
      weaknesses.push(`存在 ${result.issues.length} 个验证问题`);
    }
    
    return weaknesses;
  }
  
  assessRiskLevel(result) {
    if (result.confidenceScore >= 90) return 'low';
    if (result.confidenceScore >= 75) return 'medium-low';
    if (result.confidenceScore >= 60) return 'medium';
    if (result.confidenceScore >= 40) return 'medium-high';
    return 'high';
  }
  
  categorizeIssues(issues) {
    const categories = {
      critical: [],
      high: [],
      medium: [],
      low: []
    };
    
    for (const issue of issues) {
      categories[issue.severity].push(issue);
    }
    
    return categories;
  }
  
  calculateConfidenceInterval(score) {
    // 简化的置信区间计算
    const margin = 5; // 简化为±5%的边界
    return {
      lowerBound: Math.max(0, score - margin),
      upperBound: Math.min(100, score + margin),
      confidenceLevel: '95%'
    };
  }
}

// 导出技能类
if (typeof module !== 'undefined' && module.exports) {
  module.exports = InformationVerificationSkill;
}