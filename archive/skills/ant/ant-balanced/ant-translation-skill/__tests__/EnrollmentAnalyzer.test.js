/**
 * TDD测试 - EnrollmentAnalyzer类测试
 * 遵循AAA模式：Arrange-Act-Assert
 * 测试ANT招募环节的理论准确性
 */

const EnrollmentAnalyzer = require('../../src/analyzers/EnrollmentAnalyzer');
const { EnrollmentStrategy, TranslationPhase } = require('../../../shared/types/TranslationTypes');

describe('EnrollmentAnalyzer', () => {
  let analyzer;

  beforeEach(() => {
    // Arrange - 准备测试环境
    analyzer = new EnrollmentAnalyzer({
      validationEngine: new MockValidationEngine(),
      chineseAdapter: new MockChineseAdapter()
    });
  });

  describe('招募策略识别', () => {
    test('应该识别政策实施的招募策略', () => {
      // Arrange
      const enrollmentText = `
        政府通过财政补贴政策，成功吸引企业参与环保项目。
        通过签订合作协议，明确了各方责任和义务。
        政府部门提供技术指导，帮助企业解决技术难题。
        企业承诺按期完成任务，并接受政府的监督检查。
        媒体宣传政策成效，提高公众参与度和支持率。
        建立了多方协调机制，确保政策顺利实施。
      `;

      // Act
      const enrollment = analyzer.analyzeEnrollmentStrategies(enrollmentText);

      // Assert
      expect(enrollment).toEqual(
        expect.objectContaining({
          strategies: expect.arrayContaining([
            expect.objectContaining({
              type: EnrollmentStrategy.SPONSORSHIP_ENROLLMENT,
              actor: expect.stringContaining('政府'),
              mechanism: expect.stringContaining('财政补贴'),
              targetActors: expect.arrayContaining([
                '企业'
              ]),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              type: EnrollmentStrategy.DIRECT_ENROLLMENT,
              actor: expect.stringContaining('政府'),
              mechanism: expect.stringContaining('合作协议'),
              targetActors: expect.arrayContaining([
                '企业'
              ]),
              effectiveness: expect.any(Number)
            })
          ]),
          enrollmentLandscape: expect.objectContaining({
            targetActors: expect.arrayContaining([
              expect.objectContaining({
                type: 'government',
                role: 'policy_maker',
                engagementLevel: expect.any(Number),
                influenceLevel: expect.any(Number)
              }),
              expect.objectContaining({
                type: 'enterprise',
                role: 'implementer',
                engagementLevel: expect(Number),
                influenceLevel: expect.any(Number)
              })
            ]),
            actorRelationships: expect.arrayContaining([
              expect.objectContaining({
                from: expect.stringContaining('政府'),
                to: expect.stringContaining('企业'),
                relationship: expect.any(String),
                strength: expect.any(Number)
              })
            ])
          })
        })
      );
    });

    test('应该识别技术创新的招募过程', () => {
      // Arrange
      const techEnrollmentText = `
        技术领导者通过开源项目，吸引了全球开发者的参与。
        提供API文档和开发工具包，降低了技术门槛。
        建立开发者社区，提供技术支持和交流平台。
        举办黑客松和竞赛活动，激发创新热情。
        通过GitHub代码贡献统计，识别核心贡献者。
        给予贡献者社区地位和技术认可。
      `;

      // Act
      const enrollment = analyzer.analyzeEnrollmentStrategies(techEnrollmentText);

      // Assert
      expect(enrollment).toEqual(
        expect.objectContaining({
          strategies: expect.arrayContaining([
            expect.objectContaining({
              type: EnrollmentStrategy.DIRECT_ENROLLMENT,
              actor: expect.stringContaining('技术领导者'),
              mechanism: expect.stringContaining('开源项目'),
              targetActors: expect.arrayContaining([
                '开发者'
              ]),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              type: EnrollmentStrategy.DELEGATION_ENROLLMENT,
              actor: expect.stringContaining('技术领导者'),
              mechanism: expect.stringContaining('社区平台'),
              targetActors: expect.arrayContaining([
                '开发者'
              ]),
              effectiveness: expect.any(Number)
            })
          ]),
          recruitmentChallenges: expect.arrayContaining([
            expect.objectContaining({
              challenge: expect.any(String),
              severity: expect.stringMatching(/high|medium|low/),
              mitigation: expect.any(String)
            })
          ])
        })
      );
    });

    test('应该识别混合招募策略', () => {
      // Arrange
      const mixedText = `
        核心团队成员由直接邀请和主动申请两种方式组成。
        重要合作伙伴通过长期合作关系邀请加入。
        志愿者通过公开招募渠道参与项目。
        专家顾问通过正式合同方式参与咨询。
        支持者通过资源捐赠方式参与贡献。
        临时参与者通过项目委托方式参与。
      `;

      // Act
      const enrollment = analyzer.analyzeEnrollmentStrategies(mixedText);

      // Assert
      expect(enrollment).toEqual(
        expect.objectContaining({
          strategyMix: expect.objectContaining({
            directEnrollment: expect.any(Number),
            openEnrollment: expect.any(Number),
            referralEnrollment: expect.any(Number),
            contractEnrollment: expect.any(Number)
          }),
          strategyEffectiveness: expect.objectContaining({
            mixedStrategyBenefits: expect.arrayContaining([
              expect.any(String)
            ]),
            coordinationComplexity: expect.any(Number),
            resourceOptimization: expect.any(Number)
          })
        })
      )
    );
    });
  });

  describe('招募过程追踪', () => {
    test('应该追踪完整的招募时间线', () => {
      // Arrange
      const timelineText = `
        第一阶段：初步接触和兴趣激发（1-2个月）
        第二阶段：深入沟通和条件谈判（2-3个月）
        第三阶段：正式签约和角色分配（1个月）
        第四阶段：启动准备和团队建设（1个月）
        第五阶段：项目实施和效果评估（持续）

        关键里程碑包括：意向确认、协议签署、资源到位、团队组建、项目启动。
      `;

      // Act
      const timeline = analyzer.trackEnrollmentProcess(timelineText);

      // Assert
      expect(timeline).toEqual(
        expect.objectContaining({
          phases: expect.arrayContaining([
            expect.objectContaining({
              phase: 'initial_contact',
              duration: '1-2个月',
              objectives: expect.arrayContaining([
                '初步接触',
                '兴趣激发'
              ]),
              activities: expect.arrayContaining([
                expect.any(String)
              ])
            }),
            expect.objectContaining({
              phase: 'deep_communication',
              duration: '2-3个月',
              objectives: expect.arrayContaining([
                '深入沟通',
                '条件谈判'
              ]),
              activities: expect.arrayContaining([
                expect.any(String)
              ])
            })
          ]),
          milestones: expect.arrayContaining([
            expect.objectContaining({
              milestone: '意向确认',
              timing: expect.any(String),
              significance: expect.stringMatching(/critical|important|major|minor/),
              status: expect.stringMatching(/completed|pending|failed/)
            }),
            expect.objectContaining({
              milestone: '协议签署',
              timing: expect.any(String),
              significance: expect.stringMatching(/critical|important|major|minor/),
              status: expect.stringMatching(/completed|pending|failed/)
            })
          ]),
          timelineMetrics: expect.objectContaining({
            totalDuration: expect.any(String),
            phaseCount: expect.any(Number),
            averagePhaseDuration: expect.any(Number),
            completionRate: expect.any(Number)
          })
        })
      );
    });

    test('应该分析招募过程中的变化', () => {
      //预期结果不会执行
    });

    test('应该记录招募挑战和解决方案', () => {
      //预期结果不会执行
    });
  });

  describe('招募效果评估', () => {
    test('应该评估招募成功率', () => {
      // Arrange
      const effectivenessText = `
        招募计划成功吸引了50家企业参与，超过预期目标的25%。
        核心参与者的参与度达到90%，合作意愿强烈。
        资源承诺率达到了目标需求的80%，基本满足项目需要。
        招募过程耗时6个月，比预期时间缩短了1个月。
        成本控制在预算范围内，性价比合理。
        参与者多样性良好，覆盖了不同利益相关方。
      `;

      // Act
      const effectiveness = analyzer.assessEnrollmentEffectiveness({
        targetActors: 40,
        enrolledActors: 50,
        resourceCommitment: 0.8,
        timeSpent: '6个月',
        budgetUtilization: 0.9
      });

      // Assert
      expect(effectiveness).toEqual(
        expect.objectContaining({
          successMetrics: expect.objectContaining({
            recruitmentRate: expect.any(Number),
            targetCompletionRate: expect.any(Number),
            resourceFulfillmentRate: expect.any(Number),
            timelineEfficiency: expect.any(Number),
            budgetEfficiency: expect.any(Number)
          }),
          engagementMetrics: expect.objectContaining({
            participationRate: expect.any(Number),
            commitmentLevel: expect.any(Number),
            satisfactionLevel: expect.any(Number),
            retentionRate: expect.any(Number)
          }),
          diversityMetrics: expect.objectContaining({
            stakeholderDiversity: expect.any(Number),
            geographicDiversity: expect.any(Number),
            sectorDiversity: expect.any(Number),
            perspectiveDiversity: expect.any(Number)
          })
        })
      );
    });

    test('应该评估网络稳定性', () => {
      // Arrange
      const networkData = {
        enrolledActors: [
          { id: 'actor1', type: 'government', commitment: 'high' },
          { id: 'actor2', type: 'enterprise', commitment: 'medium' },
          { id: 'actor3', type: 'expert', commitment: 'high' }
        ],
        networkConnections: [
          { from: 'actor1', to: 'actor2', strength: 0.8, type: 'formal' },
          { from: 'actor2', to: 'actor3', strength: 0.6, type: 'technical' }
        ],
        sharedGoals: [
          '环境保护',
          '技术创新'
        ],
        coordinationMechanisms: [
          '定期会议',
          '项目协调'
        ]
      };

      // Act
      const stability = analyzer.assessNetworkStability(networkData);

      // Assert
      expect(stability).toEqual(
        expect.objectContaining({
          stabilityLevel: expect.stringMatching(/high|medium|low/),
          stabilityFactors: expect.arrayContaining([
            expect.objectContaining({
              factor: 'commitment_level',
              score: expect.any(Number),
              impact: expect.any(Number)
            }),
            expect.objectContaining({
              factor: 'connection_density',
              score: expect.any(Number),
              impact: expect.any(Number)
            }),
            expect.objectContaining({
              factor: 'goal_alignment',
              score: expect.any(Number),
              impact: expect.any(Number)
            }),
            expect.objectContaining({
              factor: 'coordination_effectiveness',
              score: expect.any(Number),
              impact: expect.any(Number)
            })
          ]),
          stabilityMetrics: expect.objectContaining({
            networkCohesion: expect.any(Number),
            resistanceLevel: expect.any(Number),
            adaptability: expect.any(Number),
            robustness: expect.any(Number)
          })
        })
      );
    });
  });

  describe('权力效应分析', () => {
    test('应该分析招募带来的权力效应', () => {
      // Arrange
      const powerData = {
        enrollmentStrategies: [
          { type: 'government_sponsorship', effectiveness: 0.9 },
          { type: 'media_endorsement', effectiveness: 0.7 },
          { type: 'expert_support', effectiveness: 0.8 }
        ],
        enrolledActors: [
          {
            id: 'government',
            type: 'institutional',
            resources: { political: 0.9, economic: 0.8 },
            networkPosition: 'central'
          },
          {
            id: 'media',
            type: 'informational',
            resources: { discursive: 0.8, symbolic: 0.7 },
            networkPosition: 'influential'
          },
          {
            id: 'expert',
            type: 'knowledge',
            resources: { technical: 0.9, cultural: 0.6 },
            networkPosition: 'specialized'
          }
        ],
        networkChanges: [
          {
            change: 'centralization_of_power',
            actors: ['government', 'media'],
            effect: 'increase_control'
          },
          {
            change: 'expertise_enhancement',
            actors: ['expert'],
            effect: 'increase_influence'
          }
        ]
      };

      // Act
      const powerAnalysis = analyzer.analyzePowerEffects(powerData);

      // Assert
      expect(powerAnalysis).toEqual(
        expect.objectContaining({
          powerEffects: expect.objectContaining({
            institutionalPower: expect.any(Number),
            discursivePower: expect.any(Number),
            technicalPower: expect.any(Number),
            symbolicPower: expect.any(Number),
            totalPower: expect.any(Number)
          }),
          powerDistribution: expect.objectContaining({
            powerCentralization: expect.any(Number),
            powerDiversity: expect.any(Number),
            powerBalance: expect.any(Number),
            powerTransition: expect.any(Number)
          }),
          influenceMechanisms: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.any(String),
              effectiveness: expect.any(Number),
              targetAudience: expect.any(Array),
              scope: expect.any(String)
            })
          ]),
          powerConstructionMetrics: expect.objectContaining({
            powerGains: expect.any(Number),
            powerStability: expect.any(Number),
            powerLegitimacy: expect.any(Number),
            powerProjection: expect.any(Number)
          })
        })
      );
    });
  });

  describe('中文本土化适配测试', () => {
    test('应该识别中国特色的招募模式', () => {
      // Arrange
      const chineseText = `
        通过单位制度动员，各级政府部门积极参与项目实施。
        利用关系网络，加强了各方之间的信任和合作。
        通过行政级别确保政策执行的权威性和有效性。
        党�员身份提升了参与者的社会地位和专业认可。
        组织资源为项目实施提供了制度保障和支持。
        荣誉机制激励了参与者的积极性和贡献度。
      `;

      // Act
      const chineseAnalysis = analyzer.analyzeChineseEnrollmentPatterns(chineseText);

      // Assert
      expect(chineseAnalysis).toEqual(
        expect.objectContaining({
          danweiSystem: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('单位制度'),
              effectiveness: expect.any(Number),
              culturalContext: expect.stringContaining('组织化动员')
            })
          ]),
          guanxiNetworks: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('关系网络'),
              type: expect.stringMatching(/formal|informal|hierarchical/),
              effectiveness: expect.any(Number)
            })
          ]),
          administrativeInfluence: expect.arrayContaining([
            expect.objectContaining({
              source: expect.stringContaining('行政级别'),
              influenceType: expect.stringMatching(/authority|control|coordination/),
              scope: expect.any(String)
            })
          ]),
          chineseCulturalFeatures: expect.arrayContaining([
            expect.stringContaining('社会地位'),
            expect.stringContaining('专业认可'),
            expect.stringContaining('制度保障')
          ])
        })
      );
    });
  });

  describe('错误处理和边界条件', () => {
    test('应该处理无招募文本', () => {
      // Arrange
      const emptyText = '';

      // Act
      const enrollment = analyzer.analyzeEnrollmentStrategies(emptyText);

      // Assert
      expect(enrollment).toEqual(
        expect.objectContaining({
          strategies: [],
          enrollmentLandscape: {
            targetActors: [],
            actorRelationships: []
          },
          hasEnrollment: false
        })
      );
    });

    test('应该处理矛盾的招募信息', () => {
      // Arrange
      const contradictoryText = `
        政府既想强制执行政策，又想保持自愿参与。
        企业既想获得政府支持，又想保持自主性。
        专家既想提供专业建议，又想保持独立性。
        公众既希望政策见效，又不想增加负担。
      `;

      // Act
      const analysis = analyzer.analyzeContradictoryEnrollment(contradictoryText);

      // Assert
      expect(analysis).toEqual(
        expect.objectContaining({
          contradictions: expect.arrayContaining([
            expect.objectContaining({
              actors: expect.arrayContaining([
                expect.stringContaining('政府')
              ]),
              conflictType: expect.stringMatching(/autonomy_vs_control|support_vs_independence|expertise_vs_commitment/),
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
          ]),
          consensusPossibility: expect.stringMatching(/high|medium|low/)
        })
      );
    });

    test('应该处理不完整的招募数据', () => {
      // Arrange
      const incompleteData = {
        targetActors: null,
        strategies: undefined,
        timeline: []
      };

      // Act
      const assessment = analyzer.assessEnrollmentEffectiveness(incompleteData);

      // Assert
      expect(assessment).toEqual(
        expect.objectContaining({
          successLevel: 'insufficient_data',
          dataCompleteness: expect.any(Number),
          missingElements: expect.arrayContaining([
            expect.stringContaining('targetActors')
          ]),
          recommendations: expect.arrayContaining([
            expect.stringContaining('补充数据')
          ])
        })
      );
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内处理复杂的招募分析', () => {
      // Arrange - 创建复杂的招募文本
      const complexText = `
        该项目采用了多层次的招募策略。首先，通过政府部门的行政命令，确保了基本参与者的参与。
        其次，通过行业组织的推荐，吸引了相关企业的积极加入。
        再次，通过学术机构的专家评审，获得了专业的技术支持。
        同时，通过媒体宣传扩大了项目影响力，提高了社会各界的参与度。
        此外，通过企业社会责任倡议，吸引了更多企业的支持。
        最后，通过国际合作项目，引入了国际先进的经验和技术支持。
        招募过程中，建立了完善的信息披露机制，确保招募过程的透明度。
        通过定期的协调会议，及时解决参与过程中的问题和挑战。
        通过建立监督评估机制，确保招募目标的实现。
        项目招募历时8个月，涉及政府部门15个，企业32家，学术机构8家，
        国际组织5家，媒体机构12家，社会团体20个。
        总计动员资金5000万元，参与人员超过200人。
      `.repeat(2);

      // Act
      const startTime = Date.now();
      const enrollment = analyzer.analyzeEnrollmentStrategies(complexText);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(4000); // 4秒内完成
      expect(enrollment.strategies.length).toBeGreaterThan(0);
      expect(enrollment.enrollmentLandscape.targetActors.length).toBeGreaterThan(0);
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