/**
 * 提取器接口 - 遵循接口隔离原则
 * 定义通用的提取操作
 */
class IExtractor {
  /**
   * 提取数据
   * @param {string} text - 输入文本
   * @param {Object} options - 提取选项
   * @returns {Array} 提取结果
   */
  extract(text, options = {}) {
    throw new Error('Method must be implemented');
  }

  /**
   * 验证提取结果
   * @param {Array} results - 提取结果
   * @returns {boolean} 是否有效
   */
  validate(results) {
    throw new Error('Method must be implemented');
  }
}

module.exports = IExtractor;