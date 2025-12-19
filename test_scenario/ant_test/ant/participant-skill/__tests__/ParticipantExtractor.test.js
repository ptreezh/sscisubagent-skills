/**
 * TDD测试 - ParticipantExtractor类测试
 * 遵循AAA模式：Arrange-Act-Assert
 */

const ParticipantExtractor = require('../../src/ParticipantExtractor');
const TextAnalyzer = require('../../src/TextAnalyzer');
const { ParticipantType, Participant } = require('../../../shared/types/Types');

describe('ParticipantExtractor', () => {
  let extractor;
  let mockTextAnalyzer;

  beforeEach(() => {
    // Arrange - 依赖注入，便于测试
    mockTextAnalyzer = new TextAnalyzer();
    extractor = new ParticipantExtractor(mockTextAnalyzer);
  });

  describe('参与者提取', () => {
    test('应该从政策文档中提取所有参与者', () => {
      // Arrange
      const text = '某市政府发布了环保新政策，要求华为公司、阿里巴巴等企业减少排放。张局长负责监督执行，李教授提供技术咨询。';

      // Act
      const result = extractor.extract(text);

      // Assert
      expect(result.participants).toHaveLength(6); // 预期6个参与者

      // 验证关键参与者
      const participantNames = result.participants.map(p => p.name);
      expect(participantNames).toContain('市政府');
      expect(participantNames).toContain('华为公司');
      expect(participantNames).toContain('张局长');

      // 验证参与者类型
      const government = result.participants.find(p => p.name === '市政府');
      expect(government.type).toBe(ParticipantType.ORGANIZATION);

      const individual = result.participants.find(p => p.name === '张局长');
      expect(individual.type).toBe(ParticipantType.INDIVIDUAL);
    });

    test('应该正确识别参与者重要性', () => {
      // Arrange
      const text = '中央政府发布了重要政策，环保部门作为主要执行机构，联合地方政府共同推进。企业被要求配合实施。';

      // Act
      const result = extractor.extract(text);

      // Assert
      const centralGov = result.participants.find(p => p.name === '中央政府');
      expect(centralGov.importance).toBe('high');

      const epd = result.participants.find(p => p.name === '环保部门');
      expect(epd.importance).toBe('high');

      const enterprise = result.participants.find(p => p.type === ParticipantType.ORGANIZATION && p.name.includes('企业'));
      expect(enterprise.importance).toBe('medium');
    });

    test('应该去重参与者', () => {
      // Arrange
      const text = '环保部门发布了政策。环保部门将监督执行。环保部门负责评估效果。';

      // Act
      const result = extractor.extract(text);

      // Assert
      const epdParticipants = result.participants.filter(p => p.name === '环保部门');
      expect(epdParticipants).toHaveLength(1); // 只有一个环保部门
    });
  });

  describe('角色识别', () => {
    test('应该识别政府角色', () => {
      // Arrange
      const text = '环保部门、教育部、发改委都参与了政策制定。';

      // Act
      const result = extractor.extract(text);

      // Assert
      const epd = result.participants.find(p => p.name === '环保部门');
      expect(epd.role).toContain('监管');

      const moe = result.participants.find(p => p.name === '教育部');
      expect(moe.role).toContain('教育');
    });

    test('应该识别企业角色', () => {
      // Arrange
      const text = '华为公司、腾讯公司作为技术提供方参与项目。';

      // Act
      const result = extractor.extract(text);

      // Assert
      const huawei = result.participants.find(p => p.name === '华为公司');
      expect(huawei.role).toContain('技术');
    });
  });

  describe('关系识别', () => {
    test('应该识别监管关系', () => {
      // Arrange
      const text = '环保部门监管企业的排放行为。';

      // Act
      const result = extractor.extractRelations(result.participants, text);

      // Assert
      expect(result.relations).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            type: 'supervision',
            fromId: expect.any(String),
            toId: expect.any(String)
          })
        ])
      );
    });

    test('应该识别合作关系', () => {
      // Arrange
      const text = '华为公司和阿里巴巴合作开发新技术。';

      // Act
      const result = extractor.extractRelations(result.participants, text);

      // Assert
      expect(result.relations).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            type: 'cooperation'
          })
        ])
      );
    });
  });

  describe('错误处理', () => {
    test('应该处理空文本', () => {
      // Arrange
      const emptyText = '';

      // Act
      const result = extractor.extract(emptyText);

      // Assert
      expect(result.participants).toHaveLength(0);
      expect(result.relations).toHaveLength(0);
    });

    test('应该处理null输入', () => {
      // Act & Assert
      expect(() => {
        extractor.extract(null);
      }).toThrow('输入文本不能为空');
    });

    test('应该处理无效的文本分析器', () => {
      // Arrange
      const invalidExtractor = new ParticipantExtractor(null);

      // Act & Assert
      expect(() => {
        invalidExtractor.extract('测试文本');
      }).toThrow('文本分析器不能为空');
    });
  });

  describe('集成测试', () => {
    test('完整的提取流程', () => {
      // Arrange
      const complexText = `
        北京市政府发布了智慧城市建设规划，要求在2025年前完成数字化转型。
        环保部门负责环境监测，交通部门负责交通优化。
        华为公司作为主要技术供应商，提供5G网络和云计算支持。
        清华大学的李教授担任项目顾问，张局长担任项目总指挥。
        企业被要求配合政府部门的工作，共同推进智慧城市建设。
      `;

      // Act
      const result = extractor.extract(complexText);

      // Assert
      // 验证参与者数量合理
      expect(result.participants.length).toBeGreaterThan(5);

      // 验证有不同类型的参与者
      const types = new Set(result.participants.map(p => p.type));
      expect(types.size).toBeGreaterThan(1);

      // 验证有关系识别
      expect(result.relations.length).toBeGreaterThan(0);

      // 验证生成了摘要
      expect(result.summary).toBeDefined();
      expect(result.summary.participantCount).toBe(result.participants.length);
    });
  });
});