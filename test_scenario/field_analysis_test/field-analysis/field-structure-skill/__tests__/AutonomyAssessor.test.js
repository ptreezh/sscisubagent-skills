/**
 * TDD测试 - AutonomyAssessor类测试
 * 遵循AAA模式：Arrange-Act-Assert
 * 测试布迪厄场域自主性评估的理论准确性
 */

const AutonomyAssessor = require('../../src/AutonomyAssessor');
const { FieldType, AutonomyLevel } = require('../../../shared/types/FieldTypes');

describe('AutonomyAssessor', () => {
  let assessor;

  beforeEach(() => {
    // Arrange - 准备测试环境
    assessor = new AutonomyAssessor();
  });

  describe('综合自主性评估', () => {
    test('应该正确评估高自主性场域', () => {
      // Arrange
      const fieldData = {
        economicData: {
          incomeSources: ['研究基金', '捐赠', '自主项目'],
          expenditureControl: '内部决策',
          budgetIndependence: '高'
        },
        politicalData: {
          governanceStructure: '学者自治',
          externalInfluence: '有限',
          appointmentProcess: '内部选举',
          decisionMaking: '集体决策'
        },
        culturalData: {
          theoreticalIndependence: '强',
          methodologicalAutonomy: '高',
          evaluationStandards: '同行评议',
          knowledgeProduction: '自主导向'
        }
      };

      // Act
      const autonomy = assessor.assessOverallAutonomy(fieldData);

      // Assert
      expect(autonomy).toEqual(
        expect.objectContaining({
          overallScore: expect.toBeGreaterThan(0.7),
          autonomyLevel: AutonomyLevel.HIGH,
          economicAutonomy: expect.objectContaining({
            score: expect.toBeGreaterThan(0.6)
          }),
          politicalAutonomy: expect.objectContaining({
            score: expect.toBeGreaterThan(0.6)
          }),
          culturalAutonomy: expect.objectContaining({
            score: expect.toBeGreaterThan(0.6)
          })
        })
      );
    });

    test('应该正确评估低自主性场域', () => {
      // Arrange
      const fieldData = {
        economicData: {
          incomeSources: ['政府拨款', '上级部门分配'],
          expenditureControl: '上级审批',
          budgetIndependence: '低'
        },
        politicalData: {
          governanceStructure: '行政任命',
          externalInfluence: '强',
          appointmentProcess: '上级指派',
          decisionMaking: '领导决定'
        },
        culturalData: {
          theoreticalIndependence: '弱',
          methodologicalAutonomy: '低',
          evaluationStandards: '行政评价',
          knowledgeProduction: '任务导向'
        }
      };

      // Act
      const autonomy = assessor.assessOverallAutonomy(fieldData);

      // Assert
      expect(autonomy).toEqual(
        expect.objectContaining({
          overallScore: expect.toBeLessThan(0.4),
          autonomyLevel: AutonomyLevel.LOW,
          externalPressures: expect.arrayContaining([
            expect.objectContaining({
              source: '政府',
              type: '行政控制',
              strength: expect.toBeGreaterThan(0.6)
            })
          ])
        })
      );
    });

    test('应该正确识别自主性变化趋势', () => {
      // Arrange
      const historicalData = [
        {
          year: 2020,
          economicAutonomy: 0.3,
          politicalAutonomy: 0.4,
          culturalAutonomy: 0.6
        },
        {
          year: 2021,
          economicAutonomy: 0.4,
          politicalAutonomy: 0.5,
          culturalAutonomy: 0.6
        },
        {
          year: 2022,
          economicAutonomy: 0.5,
          politicalAutonomy: 0.5,
          culturalAutonomy: 0.7
        }
      ];

      // Act
      const trends = assessor.analyzeAutonomyTrends(historicalData);

      // Assert
      expect(trends).toEqual(
        expect.objectContaining({
          overallTrend: 'increasing',
          keyChanges: expect.arrayContaining([
            expect.objectContaining({
              dimension: 'economicAutonomy',
              change: 'increasing',
              magnitude: expect.any(Number)
            })
          ]),
          futureProjection: expect.objectContaining({
            direction: expect.stringMatching(/increasing|decreasing|stable/),
            confidence: expect.any(Number)
          })
        })
      );
    });
  });

  describe('中文本土化自主性特征', () => {
    test('应该识别中国场域的特殊自主性特征', () => {
      // Arrange
      const chineseFieldData = {
        danweiCharacteristics: {
          institutionalEmbedding: '强',
          resourceAllocation: '上级分配',
          personnelManagement: '组织人事',
          decisionMaking: '集体领导'
        },
        guanxiInfluence: {
          informalNetworks: '强',
          personalRelationships: '重要',
          trustMechanisms: '人情关系',
          resourceMobilization: '关系网络'
        },
        administrativeLevel: {
          hierarchyRespect: '强',
          officialAuthority: '重要',
          bureaucraticLogic: '明显',
          complianceExpectation: '高'
        }
      };

      // Act
      const chineseFeatures = assessor.assessChineseAutonomyFeatures(chineseFieldData);

      // Assert
      expect(chineseFeatures).toEqual(
        expect.objectContaining({
          danweiSystemImpact: expect.any(Number),
          guanxiCapitalEffect: expect.any(Number),
          administrativeInfluence: expect.any(Number),
          specificConstraints: expect.arrayContaining([
            expect.stringContaining('单位制度'),
            expect.stringContaining('关系网络'),
            expect.stringContaining('行政级别')
          ]),
          uniqueAutonomySources: expect.arrayContaining([
            expect.stringContaining('专业权威'),
            expect.stringContaining('学术声望')
          ])
        })
      );
    });

    test('应该分析中国特色的权力关系', () => {
      // Arrange
      const powerRelationsText = `
        该大学实行党委领导下的校长负责制，重大事项需要党委常委会讨论决定。
        院长由上级主管部门任命，但在学术事务上有较大自主权。
        教授在学术评价中起主导作用，但重要决策需要党政联席会议通过。
        行业影响力是学校资源获取的重要途径，校友网络发挥重要作用。
      `;

      // Act
      const powerAnalysis = assessor.analyzeChinesePowerRelations(powerRelationsText);

      // Assert
      expect(powerAnalysis).toEqual(
        expect.objectContaining({
          formalAuthority: expect.objectContaining({
            partyLeadership: expect.any(Number),
            administrativeSystem: expect.any(Number),
          }),
          informalInfluence: expect.objectContaining({
            professionalAuthority: expect.any(Number),
            guanxiNetwork: expect.any(Number),
            alumniInfluence: expect.any(Number)
          }),
          powerBalance: expect.objectContaining({
            formalVsInformal: expect.any(Number),
            autonomyMargin: expect.any(Number)
          })
        })
      );
    });
  });

  describe('外部压力分析', () => {
    test('应该识别不同类型的外部压力', () => {
      // Arrange
      const externalInfluencesText = `
        教育部要求加强学科建设和人才培养质量评估。
        市场竞争迫使大学注重就业率和专业设置调整。
        社会舆论对大学治理透明度提出更高要求。
        国际排名压力影响着学校的资源配置策略。
        家长和学生的期望影响招生政策制定。
      `;

      // Act
      const pressures = assessor.identifyExternalPressures(externalInfluencesText);

      // Assert
      expect(pressures).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            source: '政府',
            type: '政策要求',
            pressure: expect.any(Number),
            area: '学科建设'
          }),
          expect.objectContaining({
            source: '市场',
            type: '竞争压力',
            pressure: expect.any(Number),
            area: '就业导向'
          }),
          expect.objectContaining({
            source: '社会',
            type: '舆论监督',
            pressure: expect.any(Number),
            area: '治理透明度'
          }),
          expect.objectContaining({
            source: '国际',
            type: '排名竞争',
            pressure: expect.any(Number),
            area: '资源配置'
          })
        ])
      );
    });

    test('应该评估外部压力对自主性的影响', () => {
      // Arrange
      const impactData = {
        externalPressures: [
          { source: '政府', strength: 0.8, area: '政策制定' },
          { source: '市场', strength: 0.6, area: '人才培养' },
          { source: '社会', strength: 0.4, area: '学术自由' }
        ],
        internalResistance: {
          institutionalDefenses: ['学术传统', '专业自主'],
          adaptiveStrategies: ['选择性执行', '内部缓冲'],
          negotiationCapacity: 0.7
        }
      };

      // Act
      const impact = assessor.assessExternalPressureImpact(impactData);

      // Assert
      expect(impact).toEqual(
        expect.objectContaining({
          overallImpact: expect.any(Number),
          autonomyErosion: expect.any(Number),
          adaptationStrategies: expect.arrayContaining([
            expect.stringContaining('选择性执行'),
            expect.stringContaining('内部缓冲')
          ]),
          resilienceCapacity: expect.any(Number),
          threatAreas: expect.arrayContaining([
            '政策制定'
          ])
        })
      );
    });
  });

  describe('内部合法性评估', () => {
    test('应该评估内部合法性来源', () => {
      // Arrange
      const legitimacyText = `
        教授的权威主要来自其学术成就和专业能力。
        传统上，资历和经验是权威的重要基础。
        同行的认可和尊重是学术地位的体现。
        学术委员会的决定具有程序正义性。
        长期形成的学术传统为组织提供了稳定性。
      `;

      // Act
      const legitimacy = assessor.assessInternalLegitimacy(legitimacyText);

      // Assert
      expect(legitimacy).toEqual(
        expect.objectContaining({
          overallLegitimacy: expect.any(Number),
          legitimacySources: expect.arrayContaining([
            expect.objectContaining({
              type: 'expertise',
              description: expect.stringContaining('学术成就'),
              strength: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'traditional',
              description: expect.stringContaining('资历经验'),
              strength: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'peer',
              description: expect.stringContaining('同行认可'),
              strength: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'procedural',
              description: expect.stringContaining('程序正义'),
              strength: expect.any(Number)
            })
          ]),
          legitimacyChallenges: expect.any(Array),
          legitimacyStability: expect.any(String)
        })
      );
    });
  });

  describe('错误处理和边界条件', () => {
    test('应该处理不完整的场域数据', () => {
      // Arrange
      const incompleteData = {
        economicData: null,
        politicalData: {},
        culturalData: undefined
      };

      // Act
      const autonomy = assessor.assessOverallAutonomy(incompleteData);

      // Assert
      expect(autonomy).toEqual(
        expect.objectContaining({
          overallScore: expect.any(Number),
          dataCompleteness: expect.toBeLessThan(1),
          warnings: expect.arrayContaining([
            expect.stringContaining('数据不完整')
          ])
        })
      );
    });

    test('应该处理矛盾的数据', () => {
      // Arrange
      const contradictoryData = {
        economicData: {
          incomeSources: ['政府拨款'],
          expenditureControl: '内部决策', // 矛盾
          budgetIndependence: '高'
        },
        politicalData: {
          governanceStructure: '学者自治',
          externalInfluence: '完全控制', // 矛盾
          appointmentProcess: '内部选举',
          decisionMaking: '领导决定' // 矛盾
        },
        culturalData: {}
      };

      // Act
      const autonomy = assessor.assessOverallAutonomy(contradictoryData);

      // Assert
      expect(autonomy).toEqual(
        expect.objectContaining({
          dataConsistency: expect.toBeLessThan(1),
          contradictions: expect.arrayContaining([
            expect.objectContaining({
              field: expect.any(String),
              conflict: expect.any(String)
            })
          ]),
          confidenceLevel: expect.toBeLessThan(0.8)
        })
      );
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内完成复杂自主性评估', () => {
      // Arrange - 创建复杂的场域数据
      const complexFieldData = {
        economicData: {
          incomeSources: ['政府拨款', '研究基金', '捐赠', '企业项目', '学费收入'],
          expenditureControl: '分级管理',
          budgetIndependence: '中等',
          financialConstraints: ['预算限制', '审计要求'],
          revenueStreams: 15
        },
        politicalData: {
          governanceStructure: '混合治理',
          externalInfluence: '多方面',
          appointmentProcess: '内外结合',
          decisionMaking: '分权决策',
          stakeholders: 25
        },
        culturalData: {
          theoreticalIndependence: '部分自主',
          methodologicalAutonomy: '相对自由',
          evaluationStandards: '多元化',
          knowledgeProduction: '问题导向',
          subfields: 8
        }
      };

      // Act
      const startTime = Date.now();
      const autonomy = assessor.assessOverallAutonomy(complexFieldData);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(1500); // 1.5秒内完成
      expect(autonomy).toBeDefined();
      expect(autonomy.overallScore).toBeGreaterThanOrEqual(0);
      expect(autonomy.overallScore).toBeLessThanOrEqual(1);
    });
  });
});