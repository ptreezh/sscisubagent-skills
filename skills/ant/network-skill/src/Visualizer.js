/**
 * Visualizer - 网络可视化器
 * 遵循单一职责原则：只负责网络数据可视化
 */

const IVisualizer = require('../../../shared/interfaces/IVisualizer');

class Visualizer extends IVisualizer {
  constructor() {
    super();
    this.defaultOptions = {
      width: 800,
      height: 600,
      nodeSize: 20,
      fontSize: 12,
      layout: 'force_directed',
      colors: {
        individual: '#3498db',      // 蓝色 - 个人
        organization: '#e74c3c',    // 红色 - 组织
        object: '#2ecc71',          // 绿色 - 物品
        concept: '#f39c12'          // 橙色 - 概念
      }
    };
  }

  /**
   * 生成可视化数据 - 实现IVisualizer接口
   * @param {Object} analysisData - 网络分析数据
   * @param {Object} options - 可视化选项
   * @returns {Object} 可视化数据结构
   */
  generate(analysisData, options = {}) {
    const finalOptions = { ...this.defaultOptions, ...options };

    // 验证输入
    this._validateAnalysisData(analysisData);

    // 构建节点数据
    const nodes = this._buildNodes(analysisData, finalOptions);

    // 构建边数据
    const edges = this._buildEdges(analysisData, finalOptions);

    // 计算布局
    const layout = this._calculateLayout(nodes, edges, finalOptions);

    return {
      metadata: {
        width: finalOptions.width,
        height: finalOptions.height,
        nodeCount: nodes.length,
        edgeCount: edges.length,
        layout: finalOptions.layout,
        timestamp: new Date().toISOString()
      },
      nodes: this._positionNodes(nodes, layout, finalOptions),
      edges: edges,
      legend: this._generateLegend(finalOptions.colors),
      styles: this._generateStyles(finalOptions)
    };
  }

  /**
   * 渲染可视化 - 实现IVisualizer接口
   * @param {Object} vizData - 可视化数据
   * @returns {string} 渲染结果
   */
  render(vizData) {
    if (!vizData || !vizData.nodes || !vizData.edges) {
      throw new Error('无效的可视化数据');
    }

    // 生成HTML格式的可视化
    return this._renderHTML(vizData);
  }

  /**
   * 验证分析数据
   * @private
   */
  _validateAnalysisData(data) {
    if (!data || typeof data !== 'object') {
      throw new Error('分析数据不能为空');
    }

    if (!data.keyPlayers || !Array.isArray(data.keyPlayers)) {
      throw new Error('缺少关键玩家数据');
    }

    if (!data.networkOverview || typeof data.networkOverview !== 'object') {
      throw new Error('缺少网络概览数据');
    }
  }

  /**
   * 构建节点数据
   * @private
   */
  _buildNodes(analysisData, options) {
    const nodes = [];

    // 添加参与者节点
    if (analysisData.keyPlayers) {
      analysisData.keyPlayers.forEach((player, index) => {
        nodes.push({
          id: this._generateNodeId(player),
          label: player.name,
          type: player.type,
          importance: player.importance,
          centrality: player.centralityScore || 0,
          color: options.colors[player.type] || '#95a5a6',
          size: this._calculateNodeSize(player, options),
          group: this._getNodeGroup(player.type),
          index: index
        });
      });
    }

    return nodes;
  }

  /**
   * 构建边数据
   * @private
   */
  _buildEdges(analysisData, options) {
    const edges = [];

    // 如果有原始关系数据，添加关系边
    if (analysisData.details && analysisData.details.relations) {
      analysisData.details.relations.forEach((relation, index) => {
        edges.push({
          id: `edge_${index}`,
          from: relation.fromId,
          to: relation.toId,
          label: this._getRelationLabel(relation.type),
          type: relation.type,
          strength: relation.strength,
          width: this._calculateEdgeWidth(relation.strength),
          color: this._getEdgeColor(relation.type),
          style: this._getEdgeStyle(relation.strength)
        });
      });
    }

    return edges;
  }

  /**
   * 计算布局
   * @private
   */
  _calculateLayout(nodes, edges, options) {
    switch (options.layout) {
      case 'force_directed':
        return this._forceDirectedLayout(nodes, edges, options);
      case 'circular':
        return this._circularLayout(nodes, options);
      case 'hierarchical':
        return this._hierarchicalLayout(nodes, options);
      default:
        return this._forceDirectedLayout(nodes, edges, options);
    }
  }

  /**
   * 力导向布局
   * @private
   */
  _forceDirectedLayout(nodes, edges, options) {
    const positions = [];
    const centerX = options.width / 2;
    const centerY = options.height / 2;

    // 简化的力导向算法
    nodes.forEach((node, i) => {
      const angle = (2 * Math.PI * i) / nodes.length;
      const radius = Math.min(options.width, options.height) * 0.3;

      positions.push({
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle)
      });
    });

    return positions;
  }

  /**
   * 圆形布局
   * @private
   */
  _circularLayout(nodes, options) {
    const positions = [];
    const centerX = options.width / 2;
    const centerY = options.height / 2;
    const radius = Math.min(options.width, options.height) * 0.35;

    nodes.forEach((node, i) => {
      const angle = (2 * Math.PI * i) / nodes.length;
      positions.push({
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle)
      });
    });

    return positions;
  }

  /**
   * 层次布局
   * @private
   */
  _hierarchicalLayout(nodes, options) {
    const positions = [];
    const levels = this._groupNodesByLevel(nodes);
    const levelHeight = options.height / (levels.length + 1);

    levels.forEach((level, levelIndex) => {
      const y = levelHeight * (levelIndex + 1);
      const levelWidth = options.width / (level.length + 1);

      level.forEach((node, nodeIndex) => {
        positions.push({
          x: levelWidth * (nodeIndex + 1),
          y: y
        });
      });
    });

    return positions;
  }

  /**
   * 将节点分组
   * @private
   */
  _groupNodesByLevel(nodes) {
    const levels = [];
    const processed = new Set();

    // 重要性高的节点在第一层
    const highImportance = nodes.filter(n => n.importance === 'high');
    if (highImportance.length > 0) {
      levels.push(highImportance);
      highImportance.forEach(n => processed.add(n.id));
    }

    // 中等重要性节点
    const mediumImportance = nodes.filter(n => n.importance === 'medium' && !processed.has(n.id));
    if (mediumImportance.length > 0) {
      levels.push(mediumImportance);
      mediumImportance.forEach(n => processed.add(n.id));
    }

    // 其余节点
    const others = nodes.filter(n => !processed.has(n.id));
    if (others.length > 0) {
      levels.push(others);
    }

    return levels;
  }

  /**
   * 定位节点
   * @private
   */
  _positionNodes(nodes, layout, options) {
    return nodes.map((node, index) => ({
      ...node,
      x: layout[index] ? layout[index].x : Math.random() * options.width,
      y: layout[index] ? layout[index].y : Math.random() * options.height,
      fixed: node.importance === 'high' // 重要节点固定位置
    }));
  }

  /**
   * 生成图例
   * @private
   */
  _generateLegend(colors) {
    return [
      { type: 'individual', label: '个人', color: colors.individual },
      { type: 'organization', label: '组织', color: colors.organization },
      { type: 'object', label: '物品', color: colors.object },
      { type: 'concept', label: '概念', color: colors.concept }
    ];
  }

  /**
   * 生成样式
   * @private
   */
  _generateStyles(options) {
    return {
      node: {
        default: {
          r: options.nodeSize,
          fill: '#3498db',
          stroke: '#2c3e50',
          strokeWidth: 2
        },
        hover: {
          r: options.nodeSize * 1.2,
          stroke: '#e74c3c',
          strokeWidth: 3
        }
      },
      edge: {
        default: {
          stroke: '#95a5a6',
          strokeWidth: 2,
          opacity: 0.6
        },
        hover: {
          stroke: '#e74c3c',
          strokeWidth: 3,
          opacity: 1.0
        }
      },
      label: {
        fontSize: options.fontSize,
        fontFamily: 'Arial, sans-serif',
        fill: '#2c3e50'
      }
    };
  }

  /**
   * 生成节点ID
   * @private
   */
  _generateNodeId(player) {
    return `${player.type}_${player.name.replace(/\s/g, '_')}`;
  }

  /**
   * 计算节点大小
   * @private
   */
  _calculateNodeSize(player, options) {
    const baseSize = options.nodeSize;
    const importanceMultiplier = {
      high: 1.5,
      medium: 1.0,
      low: 0.7
    };

    return baseSize * (importanceMultiplier[player.importance] || 1.0);
  }

  /**
   * 获取节点组
   * @private
   */
  _getNodeGroup(type) {
    const groups = {
      individual: 0,
      organization: 1,
      object: 2,
      concept: 3
    };
    return groups[type] || 0;
  }

  /**
   * 获取关系标签
   * @private
   */
  _getRelationLabel(type) {
    const labels = {
      supervision: '监管',
      cooperation: '合作',
      competition: '竞争',
      influence: '影响',
      dependency: '依赖'
    };
    return labels[type] || '关系';
  }

  /**
   * 计算边宽度
   * @private
   */
  _calculateEdgeWidth(strength) {
    const widths = {
      '强': 4,
      '中': 2,
      '弱': 1
    };
    return widths[strength] || 2;
  }

  /**
   * 获取边颜色
   * @private
   */
  _getEdgeColor(type) {
    const colors = {
      supervision: '#e74c3c',    // 红色 - 监管
      cooperation: '#27ae60',    // 绿色 - 合作
      competition: '#f39c12',    // 橙色 - 竞争
      influence: '#3498db',      // 蓝色 - 影响
      dependency: '#9b59b6'      // 紫色 - 依赖
    };
    return colors[type] || '#95a5a6';
  }

  /**
   * 获取边样式
   * @private
   */
  _getEdgeStyle(strength) {
    const styles = {
      '强': 'solid',
      '中': 'solid',
      '弱': 'dashed'
    };
    return styles[strength] || 'solid';
  }

  /**
   * 渲染HTML格式
   * @private
   */
  _renderHTML(vizData) {
    return `
<!DOCTYPE html>
<html>
<head>
    <title>参与者网络可视化</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { display: flex; }
        .network { flex: 1; }
        .legend { width: 200px; padding: 20px; background: #f8f9fa; }
        .legend-item { display: flex; align-items: center; margin: 10px 0; }
        .legend-color { width: 20px; height: 20px; margin-right: 10px; }
        .node { cursor: pointer; }
        .edge { fill: none; }
        .label { font-size: 12px; text-anchor: middle; }
    </style>
</head>
<body>
    <h2>参与者网络可视化</h2>
    <div class="container">
        <div class="network">
            <svg width="${vizData.metadata.width}" height="${vizData.metadata.height}" id="network"></svg>
        </div>
        <div class="legend">
            <h3>图例</h3>
            ${vizData.legend.map(item => `
                <div class="legend-item">
                    <div class="legend-color" style="background: ${item.color}"></div>
                    <span>${item.label}</span>
                </div>
            `).join('')}
            <h3>统计信息</h3>
            <p>节点数量: ${vizData.metadata.nodeCount}</p>
            <p>边数量: ${vizData.metadata.edgeCount}</p>
        </div>
    </div>
    <script>
        // 网络数据
        const data = ${JSON.stringify(vizData, null, 2)};

        // 创建SVG
        const svg = d3.select("#network");
        const width = +svg.attr("width");
        const height = +svg.attr("height");

        // 添加连线
        const links = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(data.edges)
            .enter().append("line")
            .attr("class", "edge")
            .attr("x1", d => {
                const node = data.nodes.find(n => n.id === d.from);
                return node ? node.x : 0;
            })
            .attr("y1", d => {
                const node = data.nodes.find(n => n.id === d.from);
                return node ? node.y : 0;
            })
            .attr("x2", d => {
                const node = data.nodes.find(n => n.id === d.to);
                return node ? node.x : 0;
            })
            .attr("y2", d => {
                const node = data.nodes.find(n => n.id === d.to);
                return node ? node.y : 0;
            })
            .attr("stroke", d => d.color)
            .attr("stroke-width", d => d.width)
            .attr("stroke-dasharray", d => d.style === "dashed" ? "5,5" : "0");

        // 添加节点
        const nodes = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(data.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("cx", d => d.x)
            .attr("cy", d => d.y)
            .attr("r", d => d.size)
            .attr("fill", d => d.color)
            .attr("stroke", "#2c3e50")
            .attr("stroke-width", 2);

        // 添加标签
        const labels = svg.append("g")
            .attr("class", "labels")
            .selectAll("text")
            .data(data.nodes)
            .enter().append("text")
            .attr("class", "label")
            .attr("x", d => d.x)
            .attr("y", d => d.y - d.size - 5)
            .text(d => d.label);

        // 添加交互
        nodes.on("mouseover", function(event, d) {
            d3.select(this)
                .attr("stroke-width", 3)
                .attr("stroke", "#e74c3c");
        })
        .on("mouseout", function(event, d) {
            d3.select(this)
                .attr("stroke-width", 2)
                .attr("stroke", "#2c3e50");
        });
    </script>
</body>
</html>`;
  }
}

module.exports = Visualizer;