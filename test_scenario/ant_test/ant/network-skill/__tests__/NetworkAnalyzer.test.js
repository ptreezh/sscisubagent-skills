/**
 * TDD测试 - NetworkAnalyzer类测试
 * 遵循AAA模式：Arrange-Act-Assert
 */

const NetworkAnalyzer = require('../../src/NetworkAnalyzer');
const { ParticipantType, RelationType, Participant, Relation } = require('../../../shared/types/Types');

describe('NetworkAnalyzer', () => {
  let analyzer;
  let mockParticipants;
  let mockRelations;

  beforeEach(() => {
    // Arrange - 准备测试数据
    analyzer = new NetworkAnalyzer();

    // 创建测试参与者
    mockParticipants = [
      new Participant('环保部门', ParticipantType.ORGANIZATION, '监管部门', 'high'),
      new Participant('华为公司', ParticipantType.ORGANIZATION, '技术提供方', 'high'),
      new Participant('张局长', ParticipantType.INDIVIDUAL, '管理者', 'medium'),
      new Participant('地方政府', ParticipantType.ORGANIZATION, '执行机构', 'medium'),
      new Participant('AI技术', ParticipantType.CONCEPT, '技术方案', 'low')
    ];

    // 创建测试关系
    mockRelations = [
      new Relation('organization_环保部门', 'organization_华为公司', RelationType.SUPERVISION, '强', '环保部门监管华为公司'),
      new Relation('organization_环保部门', 'organization_地方政府', RelationType.SUPERVISION, '强', '环保部门指导地方政府'),
      new Relation('organization_华为公司', 'concept_AI技术', RelationType.DEPENDENCY, '中', '华为公司依赖AI技术'),
      new Relation('individual_张局长', 'organization_环保部门', RelationType.INFLUENCE, '强', '张局长影响环保部门')
    ];
  });

  describe('网络结构分析', () => {
    test('应该正确识别星型网络', () => {
      // Arrange - 已在上面的beforeEach中准备

      // Act
      const result = analyzer.analyze(mockParticipants, mockRelations);

      // Assert
      expect(result.networkStructure.type).toBe('星型网络');
      expect(result.networkStructure.centralPlayer).toBe('环保部门');
      expect(result.networkStructure.peripheryPlayers).toContain('华为公司');
      expect(result.networkStructure.peripheryPlayers).toContain('地方政府');
    });

    test('应该正确识别多中心网络', () => {
      // Arrange - 创建多中心网络
      const multiCenterParticipants = [
        new Participant('环保部门', ParticipantType.ORGANIZATION, '监管部门', 'high'),
        new Participant('科技部', ParticipantType.ORGANIZATION, '政策制定', 'high'),
        new Participant('教育部', ParticipantType.ORGANIZATION, '教育管理', 'high'),
        new Participant('企业A', ParticipantType.ORGANIZATION, '执行方', 'medium')
      ];

      const multiCenterRelations = [
        new Relation('organization_环保部门', 'organization_企业A', RelationType.SUPERVISION, '强'),
        new Relation('organization_科技部', 'organization_企业A', RelationType.COOPERATION, '强'),
        new Relation('organization_教育部', 'organization_企业A', RelationType.COOPERATION, '中')
      ];

      // Act
      const result = analyzer.analyze(multiCenterParticipants, multiCenterRelations);

      // Assert
      expect(result.networkStructure.type).toBe('多中心网络');
      expect(result.networkStructure.keyPlayers.length).toBeGreaterThan(1);
    });

    test('应该正确识别密集网络', () => {
      // Arrange - 创建密集网络
      const denseRelations = [
        ...mockRelations,
        new Relation('organization_地方政府', 'organization_华为公司', RelationType.COOPERATION, '中'),
        new Relation('individual_张局长', 'organization_华为公司', RelationType.INFLUENCE, '中'),
        new Relation('organization_地方政府', 'concept_AI技术', RelationType.DEPENDENCY, '弱')
      ];

      // Act
      const result = analyzer.analyze(mockParticipants, denseRelations);

      // Assert
      expect(result.networkOverview.networkDensity).toBeGreaterThan(0.5);
      expect(result.networkStructure.type).toBe('密集网络');
    });
  });

  describe('关键玩家识别', () => {
    test('应该识别网络中心节点', () => {
      // Arrange
      const participantsWithConnections = mockParticipants.map(p => {
        const connections = mockRelations
          .filter(r => r.fromId.includes(p.name) || r.toId.includes(p.name))
          .length;
        p.connections = connections;
        return p;
      });

      // Act
      const keyPlayers = analyzer.findKeyPlayers(participantsWithConnections, mockRelations);

      // Assert
      expect(keyPlayers).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            name: '环保部门',
            centralityScore: expect.any(Number)
          })
        ])
      );
    });

    test('应该计算正确的中介中心性', () => {
      // Arrange
      const testRelations = [
        new Relation('A', 'B', RelationType.COOPERATION, '强'),
        new Relation('B', 'C', RelationType.COOPERATION, '强'),
        new Relation('C', 'D', RelationType.COOPERATION, '强')
      ];

      // Act
      const betweenness = analyzer.calculateBetweennessCentrality(['A', 'B', 'C', 'D'], testRelations);

      // Assert
      expect(betweenness['B']).toBeGreaterThan(betweenness['A']);
      expect(betweenness['C']).toBeGreaterThan(betweenness['D']);
    });
  });

  describe('网络指标计算', () => {
    test('应该正确计算网络密度', () => {
      // Act
      const density = analyzer.calculateNetworkDensity(mockParticipants.length, mockRelations.length);

      // Assert
      expect(density).toBe(0.2); // 4个节点，理论上最大边数为6，实际边数为4，密度=4/6=0.67
    });

    test('应该计算聚集系数', () => {
      // Arrange
      const clusterRelations = [
        new Relation('A', 'B', RelationType.COOPERATION, '强'),
        new Relation('B', 'C', RelationType.COOPERATION, '强'),
        new Relation('A', 'C', RelationType.COOPERATION, '强'),
        new Relation('C', 'D', RelationType.COOPERATION, '弱')
      ];

      // Act
      const clustering = analyzer.calculateClusteringCoefficient(['A', 'B', 'C', 'D'], clusterRelations);

      // Assert
      expect(clustering['A']).toBeCloseTo(1.0, 1); // A、B、C形成完全连接
      expect(clustering['D']).toBe(0); // D只有一个连接
    });
  });

  describe('社区检测', () => {
    test('应该识别网络社区', () => {
      // Arrange - 创建两个明显分离的社区
      const communityParticipants = [
        new Participant('A', ParticipantType.ORGANIZATION),
        new Participant('B', ParticipantType.ORGANIZATION),
        new Participant('C', ParticipantType.ORGANIZATION),
        new Participant('D', ParticipantType.ORGANIZATION)
      ];

      const communityRelations = [
        new Relation('A', 'B', RelationType.COOPERATION, '强'),
        new Relation('B', 'C', RelationType.COOPERATION, '强'),
        new Relation('C', 'A', RelationType.COOPERATION, '强'),
        new Relation('D', 'A', RelationType.SUPERVISION, '弱') // D只连接到A
      ];

      // Act
      const communities = analyzer.detectCommunities(communityParticipants, communityRelations);

      // Assert
      expect(communities.length).toBe(2);
      expect(communities[0].members).toContain('A');
      expect(communities[0].members).toContain('B');
      expect(communities[0].members).toContain('C');
    });
  });

  describe('错误处理', () => {
    test('应该处理空输入', () => {
      // Act
      const result = analyzer.analyze([], []);

      // Assert
      expect(result.networkOverview.totalNodes).toBe(0);
      expect(result.networkOverview.totalEdges).toBe(0);
      expect(result.networkStructure.type).toBe('空网络');
    });

    test('应该处理无效的关系数据', () => {
      // Arrange
      const invalidRelations = [
        { fromId: 'A', toId: 'B' }, // 缺少type字段
        null,                       // null关系
        'invalid relation'          // 字符串关系
      ];

      // Act
      const result = analyzer.analyze(mockParticipants, invalidRelations);

      // Assert - 应该过滤掉无效关系，不崩溃
      expect(result.networkOverview.totalEdges).toBe(0);
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内分析大型网络', () => {
      // Arrange - 创建100个节点的大网络
      const largeNetwork = this._createLargeNetwork(50, 100);

      // Act
      const startTime = Date.now();
      const result = analyzer.analyze(largeNetwork.participants, largeNetwork.relations);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(2000); // 2秒内完成
      expect(result.networkOverview.totalNodes).toBe(50);
    });

    /**
     * 创建大型测试网络
     * @private
     */
    _createLargeNetwork(nodeCount, edgeCount) {
      const participants = [];
      const relations = [];

      // 创建参与者
      for (let i = 0; i < nodeCount; i++) {
        participants.push(
          new Participant(`Node${i}`, ParticipantType.ORGANIZATION, '测试节点', 'medium')
        );
      }

      // 创建关系
      for (let i = 0; i < edgeCount; i++) {
        const fromIndex = Math.floor(Math.random() * nodeCount);
        const toIndex = Math.floor(Math.random() * nodeCount);

        if (fromIndex !== toIndex) {
          relations.push(
            new Relation(
              `organization_Node${fromIndex}`,
              `organization_Node${toIndex}`,
              RelationType.COOPERATION,
              '中',
              `关系${i}`
            )
          );
        }
      }

      return { participants, relations };
    }
  });
});