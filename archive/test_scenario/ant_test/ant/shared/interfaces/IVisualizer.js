/**
 * 可视化器接口 - 遵循接口隔离原则
 * 定义可视化操作
 */
class IVisualizer {
  /**
   * 生成可视化数据
   * @param {Object} data - 输入数据
   * @param {Object} options - 可视化选项
   * @returns {Object} 可视化数据结构
   */
  generate(data, options = {}) {
    throw new Error('Method must be implemented');
  }

  /**
   * 渲染可视化
   * @param {Object} vizData - 可视化数据
   * @returns {string} 渲染结果
   */
  render(vizData) {
    throw new Error('Method must be implemented');
  }
}

module.exports = IVisualizer;