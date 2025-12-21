/**
 * TextAnalyzer - 文本分析器
 * 遵循单一职责原则：只负责文本处理和模式识别
 */

const IExtractor = require('../../../shared/interfaces/IExtractor');
const { ParticipantType } = require('../../../shared/types/Types');

class TextAnalyzer extends IExtractor {
  constructor() {
    super();
    // 政府部门模式
    this.govPatterns = [
      /([^\s，。、]*(?:部|委|局|署|署|厅|司|处|科|办|院|所|中心|委员会|领导小组)[^\s，。、]*)/g,
      /([^\s，。、]*(?:政府|市政府|省政府|县政府|镇政府)[^\s，。、]*)/g
    ];

    // 企业组织模式
    this.companyPatterns = [
      /([^\s，。、]*(?:公司|集团|企业|厂|有限|股份|科技|网络)[^\s，。、]*)/g,
      /(华为|阿里巴巴|腾讯|百度|小米|字节跳动|京东|美团|滴滴|携程)/g
    ];

    // 个人角色模式
    this.personPatterns = [
      /([王李张刘陈杨黄周吴徐孙马朱胡郭何高林罗郑梁谢宋唐许韩冯邓曹彭曾萧田董袁潘于蒋蔡余杜叶程苏魏吕丁任沈姚卢姜崔钟谭陆汪范金石廖贾夏韦付方白邹孟熊秦邱江尹薛闫段雷侯龙史陶黎贺顾毛郝龚邵万钱严覃武戴莫孔向汤)[^\s，。、]*(?:局长|处长|科长|部长|主任|司长|厅长|市长|县长|镇长|书记|主席|教授|专家|工程师|研究员|顾问|总监|经理)[^\s，。、]*)/g
    ];

    // 技术/概念模式
    this.conceptPatterns = [
      /([^\s，。、]*(?:人工智能|大数据|云计算|物联网|区块链|5G|数字经济|智能制造|新能源|环保|技术|系统|平台)[^\s，。、]*)/g,
      /([^\s，。、]*(?:政策|法规|标准|规划|方案|办法|制度|机制)[^\s，。、]*)/g
    ];
  }

  /**
   * 预处理文本
   * @param {string} text - 原始文本
   * @returns {string} 处理后的文本
   */
  preprocess(text) {
    if (!text) return '';

    return text
      .trim() // 去除首尾空格
      .replace(/\s+/g, ' ') // 合并多个空格
      .replace(/[，。、；：！？""]/g, ' '); // 标点替换为空格
  }

  /**
   * 提取参与者模式 - 实现IExtractor接口
   * @param {string} text - 输入文本
   * @param {Object} options - 提取选项
   * @returns {Array} 匹配的模式数组
   */
  extract(text, options = {}) {
    const patterns = this.extractParticipantPatterns(text);
    return this.validate(patterns) ? patterns : [];
  }

  /**
   * 提取所有参与者模式
   * @param {string} text - 输入文本
   * @returns {Array} 参与者模式数组
   */
  extractParticipantPatterns(text) {
    const patterns = [];
    const processedText = this.preprocess(text);

    // 提取政府部门
    patterns.push(...this._extractByPatterns(processedText, this.govPatterns, ParticipantType.ORGANIZATION));

    // 提取企业组织
    patterns.push(...this._extractByPatterns(processedText, this.companyPatterns, ParticipantType.ORGANIZATION));

    // 提取个人角色
    patterns.push(...this._extractByPatterns(processedText, this.personPatterns, ParticipantType.INDIVIDUAL));

    // 提取技术概念
    patterns.push(...this._extractByPatterns(processedText, this.conceptPatterns, ParticipantType.CONCEPT));

    // 去重
    return this._deduplicatePatterns(patterns);
  }

  /**
   * 根据模式提取文本
   * @private
   */
  _extractByPatterns(text, patterns, type) {
    const results = [];

    patterns.forEach(pattern => {
      let match;
      while ((match = pattern.exec(text)) !== null) {
        const matchedText = match[1].trim();
        if (matchedText.length > 1) { // 过滤太短的匹配
          results.push({
            text: matchedText,
            type: type,
            position: match.index,
            confidence: this._calculateConfidence(matchedText, type)
          });
        }
      }
    });

    return results;
  }

  /**
   * 计算匹配置信度
   * @private
   */
  _calculateConfidence(text, type) {
    let confidence = 0.5; // 基础置信度

    // 根据类型和关键词调整置信度
    if (type === ParticipantType.ORGANIZATION) {
      if (/部|委|局|署|政府|公司|集团/.test(text)) confidence += 0.3;
      if (text.length > 3) confidence += 0.1;
    }

    if (type === ParticipantType.INDIVIDUAL) {
      if (/局长|处长|教授|工程师|主任/.test(text)) confidence += 0.4;
    }

    if (type === ParticipantType.CONCEPT) {
      if (/技术|政策|系统|平台|人工智能/.test(text)) confidence += 0.3;
    }

    return Math.min(confidence, 1.0);
  }

  /**
   * 去重模式
   * @private
   */
  _deduplicatePatterns(patterns) {
    const seen = new Set();
    return patterns.filter(pattern => {
      const key = `${pattern.text}-${pattern.type}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  /**
   * 验证提取结果 - 实现IExtractor接口
   * @param {Array} results - 提取结果
   * @returns {boolean} 是否有效
   */
  validate(results) {
    if (!Array.isArray(results)) return false;
    if (results.length === 0) return true; // 空结果是有效的

    return results.every(result =>
      result &&
      typeof result.text === 'string' &&
      result.text.length > 0 &&
      Object.values(ParticipantType).includes(result.type) &&
      typeof result.confidence === 'number' &&
      result.confidence >= 0 &&
      result.confidence <= 1
    );
  }

  /**
   * 获取关键词列表
   * @param {string} text - 输入文本
   * @returns {Array} 关键词数组
   */
  getKeywords(text) {
    const processedText = this.preprocess(text);
    const keywords = processedText.split(' ').filter(word => word.length > 1);
    return [...new Set(keywords)]; // 去重
  }
}

module.exports = TextAnalyzer;