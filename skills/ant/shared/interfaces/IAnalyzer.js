/**
 * 分析器接口 - 遵循接口隔离原则
 * 定义通用的分析操作
 */
class IAnalyzer {
  /**
   * 分析数据
   * @param {Array|Object} data - 输入数据
   * @param {Object} options - 分析选项
   * @returns {Object} 分析结果
   */
  analyze(data, options = {}) {
    throw new Error('Method must be implemented');
  }

  /**
   * 获取分析指标
   * @param {Object} data - 数据
   * @returns {Object} 指标结果
   */
  getMetrics(data) {
    throw new Error('Method must be implemented');
  }
}

module.exports = IAnalyzer;