/**
 * TDD测试 - TextAnalyzer类测试
 * 遵循AAA模式：Arrange-Act-Assert
 */

const TextAnalyzer = require('../../src/TextAnalyzer');
const { ParticipantType } = require('../../../shared/types/Types');

describe('TextAnalyzer', () => {
  let analyzer;

  beforeEach(() => {
    // Arrange - 准备测试环境
    analyzer = new TextAnalyzer();
  });

  describe('文本预处理', () => {
    test('应该正确清理和分词中文文本', () => {
      // Arrange
      const rawText = '  环保部门发布了新的政策要求。  ';

      // Act
      const result = analyzer.preprocess(rawText);

      // Assert
      expect(result).toContain('环保部门');
      expect(result).toContain('发布');
      expect(result).toContain('新政策');
      expect(result).not.toMatch(/^\s+|\s+$/g); // 不包含前后空格
    });

    test('应该处理空文本', () => {
      // Arrange
      const emptyText = '';

      // Act
      const result = analyzer.preprocess(emptyText);

      // Assert
      expect(result).toBe('');
    });
  });

  describe('参与者模式识别', () => {
    test('应该识别政府部门', () => {
      // Arrange
      const text = '环保部门、教育部和地方政府都参与了项目。';

      // Act
      const patterns = analyzer.extractParticipantPatterns(text);

      // Assert
      expect(patterns).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            text: '环保部门',
            type: ParticipantType.ORGANIZATION
          }),
          expect.objectContaining({
            text: '教育部',
            type: ParticipantType.ORGANIZATION
          }),
          expect.objectContaining({
            text: '地方政府',
            type: ParticipantType.ORGANIZATION
          })
        ])
      );
    });

    test('应该识别企业组织', () => {
      // Arrange
      const text = '华为公司、阿里巴巴和腾讯都支持这个项目。';

      // Act
      const patterns = analyzer.extractParticipantPatterns(text);

      // Assert
      expect(patterns).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            text: '华为公司',
            type: ParticipantType.ORGANIZATION
          })
        ])
      );
    });

    test('应该识别个人角色', () => {
      // Arrange
      const text = '张局长、李教授和王工程师参与了讨论。';

      // Act
      const patterns = analyzer.extractParticipantPatterns(text);

      // Assert
      expect(patterns).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            text: '张局长',
            type: ParticipantType.INDIVIDUAL
          }),
          expect.objectContaining({
            text: '李教授',
            type: ParticipantType.INDIVIDUAL
          })
        ])
      );
    });

    test('应该识别技术/物品概念', () => {
      // Arrange
      const text = '人工智能、大数据和云计算是关键技术。';

      // Act
      const patterns = analyzer.extractParticipantPatterns(text);

      // Assert
      expect(patterns).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            text: '人工智能',
            type: ParticipantType.CONCEPT
          }),
          expect.objectContaining({
            text: '大数据',
            type: ParticipantType.CONCEPT
          })
        ])
      );
    });
  });

  describe('边界条件测试', () => {
    test('应该处理超长文本', () => {
      // Arrange
      const longText = '环保部门' + '的重要工作。'.repeat(1000);

      // Act & Assert - 不应该崩溃或超时
      expect(() => {
        analyzer.extractParticipantPatterns(longText);
      }).not.toThrow();
    });

    test('应该处理特殊字符', () => {
      // Arrange
      const text = '环保@部门、教育部#和$地方政府都参与了项目。';

      // Act
      const patterns = analyzer.extractParticipantPatterns(text);

      // Assert
      expect(patterns.length).toBeGreaterThan(0);
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内完成分析', () => {
      // Arrange
      const text = '环保部门发布了新的环保政策，要求企业在2025年前减少碳排放。科技企业如华为、阿里巴巴都表示支持。地方政府将负责具体实施。张局长和李教授参与了政策制定。';

      // Act
      const startTime = Date.now();
      const result = analyzer.extractParticipantPatterns(text);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(1000); // 1秒内完成
      expect(result.length).toBeGreaterThan(0);
    });
  });
});