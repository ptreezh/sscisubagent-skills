/**
 * TDD测试 - FieldBoundaryAnalyzer类测试
 * 遵循AAA模式：Arrange-Act-Assert
 * 测试布迪厄场域边界识别的理论准确性
 */

const FieldBoundaryAnalyzer = require('../../src/FieldBoundaryAnalyzer');
const { FieldType, BoundaryType } = require('../../../shared/types/FieldTypes');

describe('FieldBoundaryAnalyzer', () => {
  let analyzer;

  beforeEach(() => {
    // Arrange - 准备测试环境
    analyzer = new FieldBoundaryAnalyzer();
  });

  describe('场域边界识别', () => {
    test('应该正确识别学术场域的内部边界', () => {
      // Arrange
      const academicText = `
        大学内部存在明显的学科壁垒，文学院和理学院在研究方法和评价标准上有很大差异。
        教授和讲师在学术地位和资源获取方面存在明显区分。
        学术委员会掌握了重要的学术决策权，普通教师很难参与其中。
      `;

      // Act
      const boundaries = analyzer.identifyInternalBoundaries(academicText);

      // Assert
      expect(boundaries).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            type: BoundaryType.FORMAL,
            description: expect.stringContaining('学科壁垒'),
            strength: expect.any(Number),
            permeability: expect.any(Number)
          }),
          expect.objectContaining({
            type: BoundaryType.FORMAL,
            description: expect.stringContaining('职称界限'),
            strength: expect.any(Number)
          })
        ])
      );
    });

    test('应该正确识别场域的外部影响', () => {
      // Arrange
      const text = `
        该大学受到教育部的政策指导，需要按照国家标准进行学科建设。
        市场经济的影响使得大学需要考虑就业率和产业化要求。
        社会舆论对学校的声誉有重要影响。
        政府拨款是学校收入的主要来源之一。
      `;

      // Act
      const externalBoundaries = analyzer.identifyExternalBoundaries(text);

      // Assert
      expect(externalBoundaries).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            source: '政府',
            type: BoundaryType.FORMAL,
            influence: '政策指导',
            strength: expect.any(Number)
          }),
          expect.objectContaining({
            source: '市场',
            type: BoundaryType.INFORMAL,
            influence: '就业压力',
            strength: expect.any(Number)
          })
        ])
      );
    });

    test('应该识别边界的控制机制', () => {
      // Arrange
      const text = `
        进入这个专业需要通过严格的入学考试和资格审查。
        获得教职必须具有博士学位和相关研究成果。
        学术期刊的审稿制度控制着知识生产的标准。
        专业协会的会员资格是专业认可的必要条件。
      `;

      // Act
      const mechanisms = analyzer.identifyBoundaryMechanisms(text);

      // Assert
      expect(mechanisms).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            mechanism: '准入控制',
            type: '资格审查',
            effectiveness: expect.any(Number)
          }),
          expect.objectContaining({
            mechanism: '专业认证',
            type: '会员资格',
            effectiveness: expect.any(Number)
          })
        ])
      );
    });

    test('应该评估边界渗透性', () => {
      // Arrange
      const text = `
        跨学科研究越来越受到重视，但传统学科边界仍然很强。
        业界专家可以担任兼职教授，但学术界对产业界的影响有限。
        社会资金可以资助研究项目，但不能决定研究方向。
        国际合作打破了地域限制，但文化差异仍然存在。
      `;

      // Act
      const permeability = analyzer.assessBoundaryPermeability(text);

      // Assert
      expect(permeability).toEqual(
        expect.objectContaining({
          overallPermeability: expect.any(Number),
          specificBoundaries: expect.objectContaining({
            academic: expect.any(Number),
            geographic: expect.any(Number),
            institutional: expect.any(Number)
          }),
          permeabilityTrends: expect.arrayContaining([
            expect.objectContaining({
              trend: expect.any(String),
              direction: expect.any(String)
            })
          ])
        })
      );
    });
  });

  describe('场域自主性评估', () => {
    test('应该正确评估经济自主性', () => {
      // Arrange
      const text = `
        该研究所主要依靠政府资助，预算使用需要严格审批。
        同时也承接企业委托项目，这部分收入占比30%。
        自主创收能力有限，主要收入来源还是国家拨款。
        财务独立性较低，重大开支需要上级批准。
      `;

      // Act
      const economicAutonomy = analyzer.assessEconomicAutonomy(text);

      // Assert
      expect(economicAutonomy).toEqual(
        expect.objectContaining({
          score: expect.any(Number),
          independenceLevel: expect.stringMatching(/low|medium|high/),
          mainIncomeSources: expect.arrayContaining([
            '政府资助',
            '企业项目'
          ]),
          expenditureConstraints: expect.arrayContaining([
            '严格审批'
          ]),
          autonomyTrend: expect.any(String)
        })
      );
    });

    test('应该正确评估政治自主性', () => {
      // Arrange
      const text = `
        学校领导由上级主管部门任命，重要政策需要报批。
        学术委员会在学术事务上有较大自主权。
        行政部门的干预主要体现在资源配置方面。
        教学内容和科研方向基本自主决定。
      `;

      // Act
      const politicalAutonomy = analyzer.assessPoliticalAutonomy(text);

      // Assert
      expect(politicalAutonomy).toEqual(
        expect.objectContaining({
          score: expect.any(Number),
          governanceStructure: expect.objectContaining({
            externalControl: expect.any(Number),
            internalAutonomy: expect.any(Number)
          }),
          decisionMakingAutonomy: expect.any(Number),
          personnelControl: expect.any(Number)
        })
      );
    });

    test('应该正确评估文化自主性', () => {
      // Arrange
      const text = `
        该学科具有独特的理论体系和研究方法。
        国际学术标准对本学科有重要影响。
        传统学术价值观与现代理念并存。
        学科内部的评价标准相对独立。
      `;

      // Act
      const culturalAutonomy = analyzer.assessCulturalAutonomy(text);

      // Assert
      expect(culturalAutonomy).toEqual(
        expect.objectContaining({
          score: expect.any(Number),
          theoreticalIndependence: expect.any(Number),
          methodologicalAutonomy: expect.any(Number),
          evaluationStandards: expect.objectContaining({
            internal: expect.any(Number),
            external: expect.any(Number)
          })
        })
      );
    });
  });

  describe('合法性来源识别', () => {
    test('应该识别不同类型的合法性', () => {
      // Arrange
      const text = `
        教授的权威来自其学术成果和专业能力。
        领导的权威来自正式的职位任命。
        传统权威在该组织中仍然有重要影响。
        同行认可是学术地位的重要标志。
        法规制度为组织提供了正式合法性。
      `;

      // Act
      const legitimacySources = analyzer.identifyLegitimacySources(text);

      // Assert
      expect(legitimacySources).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            type: 'expertise',
            source: '学术成果',
            strength: expect.any(Number)
          }),
          expect.objectContaining({
            type: 'formal',
            source: '职位任命',
            strength: expect.any(Number)
          }),
          expect.objectContaining({
            type: 'traditional',
            source: '传统权威',
            strength: expect.any(Number)
          }),
          expect.objectContaining({
            type: 'peer',
            source: '同行认可',
            strength: expect.any(Number)
          })
        ])
      );
    });
  });

  describe('边界变化趋势分析', () => {
    test('应该识别边界变化趋势', () => {
      // Arrange
      const text = `
        近年来，学科边界越来越模糊，跨学科合作增多。
        政府的行政干预有所减少，给予更多自主空间。
        市场力量对学术的影响持续增强。
        国际化程度不断提高，与国外机构的合作加深。
        数字化正在改变传统的学术交流方式。
      `;

      // Act
      const trends = analyzer.analyzeBoundaryTrends(text);

      // Assert
      expect(trends).toEqual(
        expect.objectContaining({
          trends: expect.arrayContaining([
            expect.objectContaining({
              dimension: '学科边界',
              trend: '开放',
              rate: expect.any(Number),
              drivers: expect.arrayContaining([
                '跨学科合作'
              ])
            }),
            expect.objectContaining({
              dimension: '政府干预',
              trend: '减弱',
              rate: expect.any(Number),
              drivers: expect.arrayContaining([
                '放权改革'
              ])
            })
          ]),
          overallDirection: expect.stringMatching(/opening|closing|stabilizing/),
          predictedFuture: expect.any(String)
        })
      );
    });
  });

  describe('错误处理和边界条件', () => {
    test('应该处理空文本输入', () => {
      // Arrange
      const emptyText = '';

      // Act
      const result = analyzer.identifyInternalBoundaries(emptyText);

      // Assert
      expect(result).toEqual([]);
    });

    test('应该处理非学术文本', () => {
      // Arrange
      const nonAcademicText = '今天的天气很好，适合出去游玩。';

      // Act
      const boundaries = analyzer.identifyInternalBoundaries(nonAcademicText);

      // Assert
      expect(boundaries.length).toBe(0);
    });

    test('应该处理模糊的边界描述', () => {
      // Arrange
      const vagueText = '各部门之间存在一些区别，但具体界限不清楚。';

      // Act
      const boundaries = analyzer.identifyInternalBoundaries(vagueText);

      // Assert
      expect(boundaries.length).toBeGreaterThanOrEqual(0);
      if (boundaries.length > 0) {
        expect(boundaries[0].strength).toBeLessThan(0.7); // 模糊描述的强度应该较低
      }
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内处理长文本', () => {
      // Arrange - 创建较长的学术文本
      const longText = `
        大学内部存在复杂的学术权力结构。学术委员会掌握着重要的学术决策权，
        包括职称评定、项目审批、学术标准制定等。教授群体在学术事务中享有较高的话语权，
        但在行政事务中的影响力有限。青年教师在学术资源分配中处于不利地位，
        需要通过积累学术资本来提升地位。学科之间存在明显的壁垒，
        跨学科研究面临制度性障碍。外部市场力量的影响日益增强，
        大学需要在学术追求和市场压力之间寻找平衡。
      `.repeat(5);

      // Act
      const startTime = Date.now();
      const boundaries = analyzer.identifyInternalBoundaries(longText);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(1000); // 1秒内完成
      expect(boundaries.length).toBeGreaterThan(0);
    });
  });
});