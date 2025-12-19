/**
 * TDD测试 - InteressementAnalyzer类测试
 * 遵循AAA模式：Arrange-Act-Assert
 * 测试ANT兴趣化环节的理论准确性
 */

const InteressementAnalyzer = require('../../src/analyzers/InteressementAnalyzer');
const { InteressementStrategy, TranslationPhase } = require('../../../shared/types/TranslationTypes');

describe('InteressementAnalyzer', () => {
  let analyzer;

  beforeEach(() => {
    // Arrange - 准备测试环境
    analyzer = new InteressementAnalyzer({
      validationEngine: new MockValidationEngine(),
      chineseAdapter: new MockChineseAdapter()
    });
  });

  describe('利益对齐机制分析', () => {
    test('应该识别经济利益对齐策略', () => {
      // Arrange
      const economicText = `
        通过提供税收优惠政策，激励企业增加环保投入。
        政府设立专项基金，支持技术创新项目。
        企业获得财政补贴，降低绿色技术采用成本。
        银行提供绿色信贷，支持环保产业发展。
        投资者获得稳定回报，增强可持续投资信心。
        市场机制引导资源配置，实现经济效益与环境效益双赢。
      `;

      // Act
      const alignment = analyzer.analyzeAlignmentStrategies(economicText);

      // Assert
      expect(alignment).toEqual(
        expect.objectContaining({
          strategies: expect.arrayContaining([
            expect.objectContaining({
              type: InteressementStrategy.ECONOMIC_INCENTIVE,
              actor: expect.stringContaining('政府'),
              mechanism: expect.stringContaining('税收优惠'),
              targetActors: expect.arrayContaining([
                '企业'
              ]),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              type: InteressementStrategy.MATERIAL_BENEFIT,
              actor: expect.stringContaining('政府'),
              mechanism: expect.stringContaining('财政补贴'),
              targetActors: expect.arrayContaining([
                '企业'
              ]),
              effectiveness: expect.any(Number)
            })
          ]),
          alignmentLandscape: expect.objectContaining({
            targetActors: expect.arrayContaining([
              expect.objectContaining({
                type: 'enterprise',
                interests: expect.arrayContaining([
                  expect.stringContaining('经济')
                ]),
                alignmentLevel: expect.any(Number)
              })
            ]),
            interestConflicts: expect.arrayContaining([
              expect.objectContaining({
                conflict: expect.any(String),
                severity: expect.stringMatching(/high|medium|low/),
                resolution: expect.any(String)
              })
            ])
          })
        })
      );
    });

    test('应该识别技术利益对齐机制', () => {
      // Arrange
      const technicalText = `
        技术团队通过开源项目共享知识产权，促进技术创新。
        提供技术培训和知识转移，提升合作伙伴能力。
        建立技术标准体系，确保行业兼容性和互操作性。
        共同研发新技术，分担研发成本和风险。
        专利共享机制加速技术普及和应用。
        技术社区建设促进知识交流和协作创新。
      `;

      // Act
      const alignment = analyzer.analyzeAlignmentStrategies(technicalText);

      // Assert
      expect(alignment).toEqual(
        expect.objectContaining({
          strategies: expect.arrayContaining([
            expect.objectContaining({
              type: InteressementStrategy.TECHNOLOGY_SHARING,
              actor: expect.stringContaining('技术团队'),
              mechanism: expect.stringContaining('开源项目'),
              targetActors: expect.arrayContaining([
                '开发者'
              ]),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              type: InteressementStrategy.KNOWLEDGE_EXCHANGE,
              actor: expect.stringContaining('技术团队'),
              mechanism: expect.stringContaining('技术培训'),
              targetActors: expect.arrayContaining([
                '合作伙伴'
              ]),
              effectiveness: expect.any(Number)
            })
          ]),
          intellectualPropertyAlignment: expect.objectContaining({
            patentSharing: expect.any(Boolean),
            openSourceLicense: expect.any(Boolean),
            technologyTransfer: expect.any(Boolean),
            standardization: expect.any(Boolean)
          })
        })
      );
    });

    test('应该识别社会声誉利益对齐', () => {
      // Arrange
      const reputationText = `
        通过媒体宣传提升参与者的社会声誉和品牌形象。
        颁发荣誉证书和奖项，增强参与者的社会认可度。
        发布企业社会责任报告，展示环境保护贡献。
        举办行业峰会和论坛，提升参与者行业地位。
        建立最佳实践案例库，推广成功经验。
        公开表彰优秀参与者，树立行业标杆。
      `;

      // Act
      const alignment = analyzer.analyzeAlignmentStrategies(reputationText);

      // Assert
      expect(alignment).toEqual(
        expect.objectContaining({
          strategies: expect.arrayContaining([
            expect.objectContaining({
              type: InteressementStrategy.REPUTATION_BENEFIT,
              actor: expect.stringContaining('组织者'),
              mechanism: expect.stringContaining('媒体宣传'),
              targetActors: expect.arrayContaining([
                '参与者'
              ]),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              type: InteressementStrategy.SOCIAL_RECOGNITION,
              actor: expect.stringContaining('组织者'),
              mechanism: expect.stringContaining('荣誉证书'),
              targetActors: expect.arrayContaining([
                '优秀参与者'
              ]),
              effectiveness: expect.any(Number)
            })
          ]),
          reputationMechanisms: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('品牌形象'),
              impact: expect.stringMatching(/high|medium|low/),
              sustainability: expect.any(Number)
            }),
            expect.objectContaining({
              mechanism: expect.stringContaining('社会认可'),
              impact: expect.stringMatching(/high|medium|low/),
              sustainability: expect.any(Number)
            })
          ])
        })
      );
    });
  });

  describe('说服装置识别', () => {
    test('应该识别法律规范说服装置', () => {
      // Arrange
      const legalText = `
        通过制定法律法规，强制要求企业履行环保责任。
        建立环境标准体系，规范企业生产和运营行为。
        实施监管制度，确保法律法规得到有效执行。
        违法违规企业面临严厉处罚，形成有效威慑。
        环保部门拥有执法权，可以现场检查和取证。
        法律诉讼机制为受害者提供救济途径。
      `;

      // Act
      const devices = analyzer.identifyPersuasiveDevices(legalText);

      // Assert
      expect(devices).toEqual(
        expect.objectContaining({
          devices: expect.arrayContaining([
            expect.objectContaining({
              type: 'legal_regulation',
              name: expect.stringContaining('法律法规'),
              mechanism: expect.stringContaining('强制要求'),
              target: expect.stringContaining('企业'),
              effectiveness: expect.any(Number),
              enforcement: expect.objectContaining({
                mechanism: expect.stringContaining('监管制度'),
                authority: expect.stringContaining('环保部门'),
                penalty: expect.stringContaining('处罚')
              })
            }),
            expect.objectContaining({
              type: 'regulatory_standard',
              name: expect.stringContaining('环境标准'),
              mechanism: expect.stringContaining('规范行为'),
              target: expect.stringContaining('企业'),
              effectiveness: expect.any(Number)
            })
          ]),
          legalFramework: expect.objectContaining({
            compulsory: expect.any(Boolean),
            enforceable: expect.any(Boolean),
            penalties: expect.arrayContaining([
              expect.any(String)
            ])
          })
        })
      );
    });

    test('应该识别技术标准说服装置', () => {
      // Arrange
      const technicalText = `
        通过制定技术标准，确保产品和服务的兼容性。
        建立认证体系，验证技术方案的可行性和可靠性。
        发布技术指南，指导行业技术发展方向。
        标准化测试程序，确保技术评估的客观性。
        技术规范要求，提升行业整体技术水平。
        认证标识增强用户对技术产品的信任度。
      `;

      // Act
      const devices = analyzer.identifyPersuasiveDevices(technicalText);

      // Assert
      expect(devices).toEqual(
        expect.objectContaining({
          devices: expect.arrayContaining([
            expect.objectContaining({
              type: 'technical_standard',
              name: expect.stringContaining('技术标准'),
              mechanism: expect.stringContaining('兼容性'),
              target: expect.stringContaining('产品服务'),
              effectiveness: expect.any(Number),
              standardization: expect.objectContaining({
                compatibility: expect.any(Boolean),
                certification: expect.any(Boolean),
                qualityAssurance: expect.any(Boolean)
              })
            })
          ]),
          technicalFramework: expect.objectContaining({
            standardization: expect.any(Boolean),
            certification: expect.any(Boolean),
            qualityControl: expect.any(Boolean)
          })
        })
      );
    });

    test('应该识别道德伦理说服装置', () => {
      // Arrange
      const ethicalText = `
        通过强调环境保护的道德责任，唤起企业的伦理意识。
        倡导可持续发展理念，引导企业承担社会责任。
        强调代际公平原则，要求为子孙后代保护环境。
        宣传生态文明理念，提升全社会的环保意识。
        呼吁企业履行道德义务，主动采取环保措施。
        伦理约束机制规范企业行为，促进可持续发展。
      `;

      // Act
      const devices = analyzer.identifyPersuasiveDevices(ethicalText);

      // Assert
      expect(devices).toEqual(
        expect.objectContaining({
          devices: expect.arrayContaining([
            expect.objectContaining({
              type: 'ethical_appeal',
              name: expect.stringContaining('道德责任'),
              mechanism: expect.stringContaining('唤起伦理意识'),
              target: expect.stringContaining('企业'),
              effectiveness: expect.any(Number),
              ethicalBasis: expect.objectContaining({
                principle: expect.stringContaining('环境保护'),
                value: expect.stringContaining('可持续'),
                responsibility: expect.stringContaining('代际公平')
              })
            })
          ]),
          moralFramework: expect.objectContaining({
            ethicalPrinciples: expect.arrayContaining([
              expect.stringContaining('道德责任')
            ]),
            socialValues: expect.arrayContaining([
              expect.stringContaining('可持续发展')
            ]),
            moralObligations: expect.arrayContaining([
              expect.stringContaining('社会责任')
            ])
          })
        })
      );
    });
  });

  describe('替代方案消除', () => {
    test('应该识别技术替代方案消除', () => {
      // Arrange
      const eliminationText = `
        通过技术标准设定，排除了不达标的技术方案。
        专利保护阻止了竞争性技术的采用。
        技术兼容性要求限制了替代方案的选择。
        专有技术格式形成技术锁定效应。
        技术生态系统建设增加了转换成本。
        标准必要专利构筑了技术壁垒。
      `;

      // Act
      const elimination = analyzer.eliminateAlternatives(eliminationText);

      // Assert
      expect(elimination).toEqual(
        expect.objectContaining({
          eliminatedAlternatives: expect.arrayContaining([
            expect.objectContaining({
              alternative: expect.stringContaining('不达标技术'),
              eliminationMechanism: expect.stringContaining('技术标准'),
              effectiveness: expect.any(Number),
              impact: expect.stringMatching(/high|medium|low/)
            }),
            expect.objectContaining({
              alternative: expect.stringContaining('竞争性技术'),
              eliminationMechanism: expect.stringContaining('专利保护'),
              effectiveness: expect.any(Number),
              impact: expect.stringMatching(/high|medium|low/)
            })
          ]),
          eliminationStrategies: expect.objectContaining({
            technicalBarriers: expect.arrayContaining([
              expect.objectContaining({
                barrier: expect.stringContaining('技术锁定'),
                mechanism: expect.stringContaining('专有格式'),
                strength: expect.any(Number)
              })
            ]),
            economicBarriers: expect.arrayContaining([
              expect.objectContaining({
                barrier: expect.stringContaining('转换成本'),
                mechanism: expect.stringContaining('生态系统'),
                strength: expect.any(Number)
              })
            ])
          })
        })
      );
    });

    test('应该识别制度替代方案消除', () => {
      // Arrange
      const institutionalText = `
        通过行政规定确立了唯一的实施路径。
        政策排除了其他可能的解决方案。
        制度安排限制了行动选择的范围。
        程序要求排除了灵活处理的可能性。
        管理体制形成了固定的运作模式。
        决策机制集中化减少了替代选项。
      `;

      // Act
      const elimination = analyzer.eliminateAlternatives(institutionalText);

      // Assert
      expect(elimination).toEqual(
        expect.objectContaining({
          eliminatedAlternatives: expect.arrayContaining([
            expect.objectContaining({
              alternative: expect.stringContaining('其他方案'),
              eliminationMechanism: expect.stringContaining('行政规定'),
              effectiveness: expect.any(Number),
              impact: expect.stringMatching(/high|medium|low/)
            })
          ]),
          institutionalConstraints: expect.arrayContaining([
            expect.objectContaining({
              constraint: expect.stringContaining('程序要求'),
              flexibility: expect.stringMatching(/low|medium|high/),
              negotiability: expect.any(Boolean)
            })
          ])
        })
      );
    });
  });

  describe('兴趣化过程追踪', () => {
    test('应该追踪完整的兴趣化时间线', () => {
      // Arrange
      const timelineText = `
        第一阶段：利益识别和表达（1-2个月）
        第二阶段：对齐机制设计（2-3个月）
        第三阶段：说服装置部署（1-2个月）
        第四阶段：替代方案消除（1个月）
        第五阶段：兴趣固化确认（1个月）

        关键节点：利益明确、机制建立、装置生效、替代清除、兴趣锁定。
      `;

      // Act
      const timeline = analyzer.trackInteressementProcess(timelineText);

      // Assert
      expect(timeline).toEqual(
        expect.objectContaining({
          phases: expect.arrayContaining([
            expect.objectContaining({
              phase: 'interest_identification',
              duration: '1-2个月',
              objectives: expect.arrayContaining([
                '利益识别',
                '利益表达'
              ]),
              activities: expect.arrayContaining([
                expect.any(String)
              ])
            }),
            expect.objectContaining({
              phase: 'alignment_design',
              duration: '2-3个月',
              objectives: expect.arrayContaining([
                '对齐机制设计'
              ]),
              activities: expect.arrayContaining([
                expect.any(String)
              ])
            })
          ]),
          keyEvents: expect.arrayContaining([
            expect.objectContaining({
              event: '利益明确',
              timing: expect.any(String),
              significance: expect.stringMatching(/critical|important|major|minor/),
              status: expect.stringMatching(/completed|pending|failed/)
            })
          ]),
          processMetrics: expect.objectContaining({
            totalDuration: expect.any(String),
            phaseCount: expect.any(Number),
            completionRate: expect.any(Number),
            effectivenessScore: expect.any(Number)
          })
        })
      );
    });

    test('应该记录兴趣化挑战和解决方案', () => {
      // Arrange
      const challengeText = `
        面临利益冲突难以调和的挑战，通过利益补偿机制解决。
        参与者积极性不高，通过激励措施提升参与度。
        说服装置效果不佳，通过多管齐下增强说服力。
        替代方案依然存在，通过强化管制消除影响。
        利益关系不稳定，通过长期合同固化关系。
      `;

      // Act
      const challenges = analyzer.analyzeInteressementChallenges(challengeText);

      // Assert
      expect(challenges).toEqual(
        expect.objectContaining({
          challenges: expect.arrayContaining([
            expect.objectContaining({
              challenge: expect.stringContaining('利益冲突'),
              severity: expect.stringMatching(/high|medium|low/),
              solution: expect.stringContaining('利益补偿'),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              challenge: expect.stringContaining('积极性不高'),
              severity: expect.stringMatching(/high|medium|low/),
              solution: expect.stringContaining('激励措施'),
              effectiveness: expect.any(Number)
            })
          ]),
          resolutionStrategies: expect.arrayContaining([
            expect.objectContaining({
              strategy: expect.any(String),
              application: expect.stringMatching(/direct|indirect|combined/),
              successRate: expect.any(Number)
            })
          ])
        })
      );
    });
  });

  describe('兴趣化效果评估', () => {
    test('应该评估利益对齐效果', () => {
      // Arrange
      const effectivenessData = {
        targetActors: [
          { id: 'enterprise1', interests: ['经济利益', '技术发展'], alignment: 0.8 },
          { id: 'government1', interests: ['环境保护', '社会治理'], alignment: 0.9 }
        ],
        alignmentStrategies: [
          { type: 'economic_incentive', effectiveness: 0.85 },
          { type: 'technical_cooperation', effectiveness: 0.75 }
        ],
        eliminatedAlternatives: 5,
        remainingConflicts: 2
      };

      // Act
      const effectiveness = analyzer.assessInteressementEffectiveness(effectivenessData);

      // Assert
      expect(effectiveness).toEqual(
        expect.objectContaining({
          alignmentMetrics: expect.objectContaining({
            averageAlignmentLevel: expect.any(Number),
            alignmentDistribution: expect.objectContaining({
              high: expect.any(Number),
              medium: expect.any(Number),
              low: expect.any(Number)
            }),
            interestCoverage: expect.any(Number)
          }),
          strategyEffectiveness: expect.objectContaining({
            overallEffectiveness: expect.any(Number),
            strategySuccessRate: expect.any(Number),
            costEfficiency: expect.any(Number),
            timeEfficiency: expect.any(Number)
          }),
          eliminationEffectiveness: expect.objectContaining({
            alternativesEliminated: expect.any(Number),
            eliminationRate: expect.any(Number),
            residualThreats: expect.any(Number),
            eliminationCompleteness: expect.any(Number)
          })
        })
      );
    });

    test('应该评估网络稳定性增强', () => {
      // Arrange
      const networkData = {
        beforeInteressement: {
          actorCount: 8,
          connectionDensity: 0.3,
          conflictCount: 5
        },
        afterInteressement: {
          actorCount: 8,
          connectionDensity: 0.7,
          conflictCount: 2
        },
        alignmentMechanisms: [
          'economic_incentives',
          'technical_standards',
          'social_recognition'
        ]
      };

      // Act
      const stability = analyzer.assessNetworkStabilityEnhancement(networkData);

      // Assert
      expect(stability).toEqual(
        expect.objectContaining({
          stabilityImprovement: expect.objectContaining({
            connectionDensityIncrease: expect.any(Number),
            conflictReduction: expect.any(Number),
            networkCohesion: expect.any(Number),
            stabilityScore: expect.any(Number)
          }),
          contributingFactors: expect.arrayContaining([
            expect.objectContaining({
              factor: expect.any(String),
              contribution: expect.any(Number),
              sustainability: expect.any(String)
            })
          ]),
          resilienceMetrics: expect.objectContaining({
            shockResistance: expect.any(Number),
            adaptationCapacity: expect.any(Number),
            recoverySpeed: expect.any(Number)
          })
        })
      );
    });
  });

  describe('中文本土化适配测试', () => {
    test('应该识别中国特色的利益对齐机制', () => {
      // Arrange
      const chineseText = `
        通过政治动员激发参与者的责任意识和使命感。
        利用单位制度协调各方利益，实现整体利益最大化。
        借助关系网络促进沟通协调，增强利益共识。
        通过行政级别确保政策执行，维护利益格局稳定。
        发挥党组织作用，统一步调和思想认识。
        运用荣誉机制激励先进典型，树立学习榜样。
      `;

      // Act
      const chineseAnalysis = analyzer.analyzeChineseInteressementPatterns(chineseText);

      // Assert
      expect(chineseAnalysis).toEqual(
        expect.objectContaining({
          politicalMobilization: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('政治动员'),
              type: expect.stringMatching(/ideological|organizational|mass/),
              effectiveness: expect.any(Number),
              culturalContext: expect.stringContaining('责任意识')
            })
          ]),
          institutionalMechanisms: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('单位制度'),
              function: expect.stringContaining('利益协调'),
              governance: expect.stringMatching(/centralized|hierarchical|coordinated/),
              effectiveness: expect.any(Number)
            })
          ]),
          chineseCulturalFeatures: expect.arrayContaining([
            expect.stringContaining('关系网络'),
            expect.stringContaining('行政级别'),
            expect.stringContaining('党组织'),
            expect.stringContaining('荣誉机制')
          ])
        })
      );
    });
  });

  describe('错误处理和边界条件', () => {
    test('应该处理无兴趣化文本', () => {
      // Arrange
      const emptyText = '';

      // Act
      const interessement = analyzer.analyzeAlignmentStrategies(emptyText);

      // Assert
      expect(interessement).toEqual(
        expect.objectContaining({
          strategies: [],
          alignmentLandscape: {
            targetActors: [],
            interestConflicts: []
          },
          hasInteressement: false
        })
      );
    });

    test('应该处理矛盾的对齐信息', () => {
      // Arrange
      const contradictoryText = `
        政府既想通过经济激励引导企业，又想通过行政命令强制企业。
        企业既想要经济利益，又不想承担环保责任。
        公众既要求环境保护，又不愿意增加成本。
        技术既想开放共享，又想保持专有优势。
      `;

      // Act
      const analysis = analyzer.analyzeContradictoryInteressement(contradictoryText);

      // Assert
      expect(analysis).toEqual(
        expect.objectContaining({
          contradictions: expect.arrayContaining([
            expect.objectContaining({
              actors: expect.arrayContaining([
                expect.stringContaining('政府')
              ]),
              conflictType: expect.stringMatching(/incentive_vs_coercion|benefit_vs_responsibility|openness_vs_exclusivity/),
              severity: expect.stringMatching(/high|medium|low/)
            })
          ]),
          resolutionApproaches: expect.arrayContaining([
            expect.objectContaining({
              approach: expect.any(String),
              feasibility: expect.stringMatching(/high|medium|low/),
              recommendations: expect.arrayContaining([
                expect.any(String)
              ])
            })
          ])
        })
      );
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内处理复杂的兴趣化分析', () => {
      // Arrange - 创建复杂的兴趣化文本
      const complexText = `
        该项目设计了多层次的利益对齐机制。首先，通过经济激励措施，
        包括税收优惠、财政补贴、绿色信贷等，引导企业积极参与。
        其次，通过技术合作机制，共享知识产权，分担研发风险。
        再次，通过社会声誉激励，颁发环保奖项，提升企业形象。
        同时，通过法律规制手段，设定排放标准，强化环境监管。
        此外，通过道德伦理倡导，强调社会责任，唤起环保意识。
        最后，通过制度安排保障，建立长期合作机制，稳定利益预期。
        整个过程涉及政府、企业、公众、专家等多方利益相关者，
        通过复杂的利益网络构建，实现了各方利益的有效对齐。
        项目历时12个月，成功消除了15个替代方案，化解了8个利益冲突，
        建立了23个合作机制，参与各方的利益对齐度平均达到85%。
      `.repeat(2);

      // Act
      const startTime = Date.now();
      const interessement = analyzer.analyzeAlignmentStrategies(complexText);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(4000); // 4秒内完成
      expect(interessement.strategies.length).toBeGreaterThan(0);
      expect(interessement.alignmentLandscape.targetActors.length).toBeGreaterThan(0);
    });
  });
});

// Mock classes for testing
class MockValidationEngine {
  validateTheoryApplication() { return true; }
  validateCompleteness() { return { score: 0.9 }; }
  validateConsistency() { return { score: 0.85 }; }
  validateAccuracy() { return { score: 0.88 }; }
}

class MockChineseAdapter {
  adaptChineseContext() { return {}; }
  identifyChineseFeatures() { return {}; }
  mapConceptTerm() { return '中文术语'; }
}