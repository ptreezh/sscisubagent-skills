/**
 * TDD测试 - MobilizationAnalyzer类测试
 * 遵循AAA模式：Arrange-Act-Assert
 * 测试ANT动员环节的理论准确性
 */

const MobilizationAnalyzer = require('../../src/analyzers/MobilizationAnalyzer');
const { MobilizationEffect, TranslationPhase } = require('../../../shared/types/TranslationTypes');

describe('MobilizationAnalyzer', () => {
  let analyzer;

  beforeEach(() => {
    // Arrange - 准备测试环境
    analyzer = new MobilizationAnalyzer({
      validationEngine: new MockValidationEngine(),
      chineseAdapter: new MockChineseAdapter()
    });
  });

  describe('动员机制分析', () => {
    test('应该识别政策实施的动员机制', () => {
      // Arrange
      const mobilizationText = `
        通过建立跨部门协调机制，有效整合各方资源和力量。
        设立专门的项目管理办公室，负责日常协调工作。
        制定详细的实施计划和时间表，确保有序推进。
        通过定期评估和反馈机制，及时调整策略和方向。
        建立了信息共享平台，促进参与者之间的沟通交流。
        通过激励机制设计，提高参与者的积极性和主动性。
      `;

      // Act
      const mobilization = analyzer.analyzeMobilizationMechanisms(mobilizationText);

      // Assert
      expect(mobilization).toEqual(
        expect.objectContaining({
          mechanisms: expect.arrayContaining([
            expect.objectContaining({
              type: 'coordination_mechanism',
              description: expect.stringContaining('跨部门协调机制'),
              scope: expect.any(String),
              effectiveness: expect.any(Number),
              sustainability: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'management_structure',
              description: expect.stringContaining('项目管理办公室'),
              scope: expect.any(String),
              effectiveness: expect.any(Number),
              sustainability: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'planning_system',
              description: expect.stringContaining('实施计划'),
              scope: expect.any(String),
              effectiveness: expect.any(Number),
              sustainability: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'evaluation_feedback',
              description: expect.stringContaining('评估和反馈'),
              scope: expect.any(String),
              effectiveness: expect.any(Number),
              sustainability: expect.any(Number)
            })
          ]),
          mobilizationEffectiveness: expect.objectContaining({
            overallEffectiveness: expect.any(Number),
            mechanismIntegration: expect.any(Number),
            resourceOptimization: expect.any(Number),
            coordinationEfficiency: expect.any(Number)
          })
        })
      );
    });

    test('应该识别技术项目的动员过程', () => {
      // Arrange
      const techMobilizationText = `
        通过敏捷开发方法论，实现了快速的迭代开发和部署。
        建立了开源社区平台，促进了协作开发和知识共享。
        实施了持续集成/持续部署(CI/CD)流程，提高了开发效率。
        通过定期版本发布，保持了项目的新鲜性和吸引力。
        建立了用户反馈渠道，及时响应需求和问题。
        通过开发者大会和培训活动，加强了社区凝聚力。
      `;

      // Act
      const mobilization = analyzer.analyzeMobilizationMechanisms(techMobilizationText);

      // Assert
      expect(mobilization).toEqual(
        expect.objectContaining({
          mechanisms: expect.arrayContaining([
            expect.objectContaining({
              type: 'methodology_adoption',
              description: expect.stringContaining('敏捷开发'),
              scope: expect.stringContaining('开发'),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'community_platform',
              description: expect.stringContaining('开源社区'),
              scope: expect.stringContaining('协作开发'),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'automation_pipeline',
              description: expect.stringContaining('CI/CD'),
              scope: expect.stringContaining('部署'),
              effectiveness: expect.any(Number)
            })
          ]),
          technologyFeatures: expect.arrayContaining([
            expect.objectContaining({
              feature: expect.stringContaining('敏捷开发'),
              impact: expect.any(Number),
              adoptionLevel: expect.any(Number)
            }),
            expect.objectContaining({
              feature: expect.stringContaining('开源社区'),
              impact: expect.any(Number),
              adoptionLevel: expect.any(Number)
            })
          ])
        })
      );
    });
  });

  describe('网络稳定性评估', () => {
    test('应该评估复杂网络的稳定性', () => {
      // Arranged
      const networkData = {
        actors: [
          {
            id: 'actor1',
            name: '环保部门',
            type: 'government',
            commitment: 0.9,
            resources: { political: 0.8, economic: 0.7, cultural: 0.6 },
            networkPosition: 'central'
          },
          {
            id: 'actor2',
            name: '环保企业',
            type: 'enterprise',
            commitment: 0.7,
            resources: { economic: 0.8, technical: 0.7, social: 0.5 },
            networkPosition: 'important'
          },
          {
            id: 'actor3',
            name: '研究机构',
            type: 'academic',
            commitment: 0.6,
           : resources: { cultural: 0.9, intellectual: 0.8, social: 0.4 },
            networkPosition: 'specialized'
          },
          {
            id: 'actor4',
            name: '媒体机构',
            type: 'media',
            commitment: 0.5,
           : resources: { symbolic: 0.8, social: 0.7, economic: 0.4 },
            networkPosition: 'influential'
          }
        ],
        connections: [
          { from: 'actor1', to: 'actor2', strength: 0.8, type: 'formal' },
          { from: 'actor1', to: 'actor3', strength: 0.6, type: 'formal' },
          { from: 'actor2', to: 'actor3', strength: 0.5, type: 'technical' },
          { from: 'actor1', to: 'actor4', strength: 0.7, type: 'informational' },
          { from: 'actor2', to: 'actor4', strength: 0.6, type: 'informational' },
          { from: 'actor3', to: 'actor4', strength: 0.4, type: 'expertise' }
        ],
        sharedGoals: ['环境保护', '技术创新', '公共利益'],
        coordinationMechanisms: ['定期会议', '项目协调', '信息共享'],
        conflictResolution: ['协商解决', '仲裁机制', '第三方调解']
      };

      // Act
      const stability = analyzer.assessNetworkStability(networkData);

      // Assert
      expect(stability).toEqual(
        expect.objectContaining({
          stabilityLevel: expect.stringMatching(/high|medium|low/),
          stabilityFactors: expect.arrayContaining([
            expect.objectContaining({
              factor: 'network_cohesion',
              score: expect.any(Number),
              impact: expect.any(Number)
            }),
            expect.objectContaining({
              factor: 'resource_commitment',
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
            structuralStability: expect.any(Number),
            functionalStability: expect.any(Number),
            temporalStability: expect.any(Number)
          }),
          riskAssessment: expect.objectContaining({
            fragilityPoints: expect.arrayContaining([
              expect.objectContaining({
                point: expect.any(String),
                vulnerability: expect.stringMatching(/high|medium|low/),
                impact: expect.stringMatching(/critical|significant|moderate/)
              })
            ]),
            resilienceLevel: expect.stringMatching(/high|medium|low/),
            adaptationCapacity: expect.stringMatching(/high|medium|low/)
          })
        })
      );
    });

    test('应该评估动态网络的稳定性变化', () => {
      // Arrange
      const dynamicData = {
        baselineNetwork: {
          actors: 3,
          connections: 4,
          stabilityScore: 0.6
        },
        evolutionTrend: {
          direction: 'increasing',
          changeRate: 0.3,
          timePeriod: '6个月'
        },
        changes: [
          {
            change: 'new_actors_added',
            beforeCount: 3,
            afterCount: 5,
            stabilityImpact: 0.1
          },
          {
            change: 'connections_increased',
            beforeCount: 4,
            afterCount: 8,
            stabilityImpact: 0.2
          }
        ]
      };

      // Act
      const dynamicStability = analyzer.assessDynamicStability(dynamicData);

      // Assert
      expect(dynamicStability).toEqual(
        expect.objectContaining({
          evolutionAnalysis: expect.objectContaining({
            direction: expect.stringMatching(/increasing|decreasing|stable/),
            changeRate: expect.any(Number),
            changeNature: expect.any(String),
            evolutionaryFactors: expect.arrayContaining([
              expect.objectContaining({
                factor: expect.any(String),
                impact: expect.any(Number)
              })
            ])
          }),
          stabilityProjection: expect.objectContaining({
            projectedStability: expect.any(Number),
            confidenceLevel: expect.any(Number),
            timeframe: expect.any(String)
          }),
          changeImpacts: expect.arrayContaining([
            expect.objectContaining({
              changeType: expect.any(String),
              stabilityChange: expect.any(Number),
              adaptationRequired: expect.stringMatching(/high|medium|low/),
              riskLevel: expect.stringMatching(/high|medium|low/)
            })
          ])
        })
      );
    });
  });

  describe('黑箱形成分析', () => {
    test('应该识别技术标准的黑箱化过程', () => {
      // Arrange
      const blackBoxText = `
        通过复杂的技术标准和认证程序，普通用户无法理解技术细节。
        专业的术语和符号体系创造了专业壁垒。
        标准制定过程不透明，外部人员难以参与和影响。
        技术决策集中在少数专家手中，形成专家权威。
        成本效益分析使用复杂的模型和算法，结果难以验证。
        监管机制的复杂性使得合规要求难以理解和遵守。
      `;

      // Act
      const blackBoxAnalysis = analyzer.identifyBlackBoxFormation(blackBoxText);

      // Assert
      expect(blackBoxAnalysis).toEqual(
        expect.objectContaining({
          blackBoxes: expect.arrayContaining([
            expect.objectContaining({
              name: expect.stringContaining('技术标准'),
              complexity: expect.stringMatching(/high|medium|low/),
              opacity: expect.any(Number),
              controlLevel: expect.any(Number),
              actors: expect.arrayContaining([
                expect.objectContaining({
                  role: expect.stringContaining('专家'),
                  power: expect.any(Number)
                })
              ])
            })
          ]),
          blackBoxingMechanisms: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('术语体系'),
              effect: expect.stringContaining('专业壁垒'),
              scope: expect.any(String),
              permanence: expect.stringMatching(/permanent|temporary/conditional/)
            })
          ]),
          opacityFactors: expect.arrayContaining([
            expect.objectContaining({
              factor: expect.stringContaining('决策不透明'),
              impact: expect.any(Number)
            }),
            expect.objectContaining({
              factor: expect.stringContaining('复杂模型'),
              impact: expect.any(Number)
            })
          ]),
          controlConcentration: expect.objectContaining({
            controlDistribution: expect.any(Object),
            concentrationLevel: expect.any(Number),
            powerImbalance: expect.any(Number),
              'expert_authority_concentration: expect.any(Number)
          })
        })
      );
    });

    test('应该分析黑箱的权力效应', () => {
      // Arrange
      const powerEffectText = `
        黑箱化的技术标准赋予了制定者的话语权威。
        复杂的认证程序创造了技术优势和市场壁垒。
        专业化的要求使得新进入者难以竞争。
        不透明的标准制定过程保护了既得利益者。
        技术黑箱化使得监管变得困难，需要专业知识。
      `;

      // Act
      const powerEffects = analyzer.analyzeBlackBoxPowerEffects(powerEffectText);

      // return
      expect(powerEffects).toEqual(
        expect.objectContaining({
          discursivePower: expect.objectContaining({
            authorityLevel: expect.any(Number),
            legitimacySource: expect.any(String),
            persuasionPower: expect.any(Number),
            audienceControl: expect.any(Number)
          }),
          economicPower: expect.objectContaining({
            marketEntryBarrier: expect.any(Number),
            competitiveAdvantage: expect.any(Number),
            pricingPower: expect.any(Number),
            resourceControl: expect.any(Number)
          }),
          expertPower: expect.objectContaining({
            expertiseMonopoly: expect.any(Number),
            decisionInfluence: expect.any(Number),
            advisoryAuthority: expect.any(Number),
            cognitivePower: expect.any(Number)
          }),
          powerDistribution: expect.objectContaining({
            powerCentralization: expect.any(Number),
            powerSourceDistribution: expect.any(Object),
            powerAccessMechanisms: expect.arrayContaining([
              expect.any(String)
            ])
          })
        })
      );
    });

    test('应该分析黑箱的稳定性和开放性', () => {
      // Arrange
      const opennessText = `
        技术标准虽然复杂但可以通过培训和认证获得理解。
        标准文档公开透明，任何人都可以查阅和评论。
        认证过程有申诉渠道，允许质疑和改进。
        标准定期更新，能够适应技术发展需要。
        多方参与的标准制定过程确保了平衡性。
      `;

      // Act
      const opennessAnalysis = analyzer.analyzeBlackBoxOpenness(opennessText);

      // Assert
      expect(opennessAnalysis).toEqual(
        expect.objectContaining({
          opennessLevel: expect.stringMatching(/high|medium|low/),
          accessibilityFeatures: expect.arrayContaining([
            expect.objectContaining({
              feature: expect.stringContaining('培训认证'),
              effectiveness: expect.any(Number),
              accessibility: expect.any(Number)
            }),
            expect.objectContaining({
              feature: expect.stringContaining('标准文档'),
              effectiveness: expect.any(Number),
              accessibility: expect.any(Number)
            })
          ]),
          transparencyMechanisms: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('申诉渠道'),
              effectiveness: expect.any(Number),
              transparencyLevel: expect.any(Number)
            })
          ]),
          adaptabilityFeatures: expect.arrayContaining([
            expect.objectContaining({
              feature: expect.stringContaining('定期更新'),
              responsiveness: expect.any(Number),
              adaptability: expect.any(Number)
            })
          ]),
          openingRisks: expect.arrayContaining([
            expect.objectContaining({
              risk: expect.any(String),
              mitigation: expect.any(String),
              severity: expect.stringMatching(/high|medium|low/)
            })
          ])
        })
      );
    });
  });

  describe('动员效果评估', () => {
    test('应该评估动员过程的整体效果', () => {
      // Arrange
      const mobilizationData = {
        mechanisms: [
          {
            type: 'coordination',
            effectiveness: 0.8,
            sustainability: 0.7
          },
          {
            type: 'incentive',
            effectiveness: 0.9,
            sustainability: 0.6
          },
          {
            type: 'monitoring',
            effectiveness: 0.7,
            sustainability: 0.8
          }
        ],
        effects: [
          MobilizationEffect.NETWORK_STABILIZATION,
          MobilizationEffect.BLACK_BOX_FORMATION,
          MobilizationEffect.POWER_CONSOLIDATION,
          MobilizationEffect.LEGITIMACY_ESTABLISHMENT
        ],
        metrics: {
          participantEngagement: 0.85,
          goalAchievement: 0.8,
          timelineAdherence: 0.75,
          resourceUtilization: 0.8
        }
      };

      // Act
      const effectAssessment = analyzer.assessMobilizationEffectiveness(mobilizationData);

      // Assert
      expect(effectAssessment).toEqual(
        expect.objectContaining({
          overallEffectiveness: expect.any(Number),
          phaseCompletion: expect.objectContaining({
            problematization: expect.any(Number),
            interessement: expect.any(Number),
            enrollment: expect.any(Number),
            mobilization: expect.any(Number)
          }),
          effectAchievement: expect.objectContaining({
            networkStabilization: expect.any(Number),
            blackBoxFormation: expect.any(Number),
            powerConsolidation: expect.any(Number),
            legitimationEstablishment: expect.any(Number)
          }),
          mechanismEffectiveness: expect.objectContaining({
            coordinationEffectiveness: expect.any(Number),
            incentiveEffectiveness: expect.any(Number),
            monitoringEffectiveness: expect.any(Number),
            overallMechanismIntegration: expect.any(Number)
          }),
          keyMetrics: expect.objectContaining({
            engagementScore: expect.any(Number),
            achievementScore: expect.any(Number),
            adherenceScore: expect.any(Number),
            utilizationScore: expect.any(Number),
            satisfactionScore: expect.any(Number)
          })
        })
      );
    });

    test('应该分析动员过程的可持续性', () => {
      // Arrange
      const sustainabilityData = {
        mechanisms: [
          {
            type: 'formal_institutional',
            sustainability: 0.9,
            renewalCycle: 'annual'
          },
          {
            type: 'informal_network',
            sustainability: 0.6,
            renewalCycle: 'continuous'
          },
          {
            type: 'technical_infrastructure',
            sustainability: 0.8,
            renewalCycle: 'biennial'
          }
        ],
        maintenanceFactors: [
          {
            factor: 'continuous_monitoring',
            necessity: expect.stringMatching(/high|medium|low/),
              cost: expect.any(Number)
          },
          {
            factor: 'capacity_building',
            necessity: expect.stringMatching(/high|medium|low/),
              cost: expect.any(Number)
          },
          {
            factor: 'relationship_maintenance',
            necessity: expect.stringMatching(/high|medium|low/),
              cost: expect.any(Number)
          }
        ]
      };

      // Act
      const sustainabilityAssessment = analyzer.assessSustainability(sustainabilityData);

      // Assert
      expect(sustainabilityAssessment).toEqual(
        expect.objectContaining({
          sustainabilityScore: expect.any(Number),
          sustainabilityFactors: expect.objectContaining({
            institutional_sustainability: expect.any(Number),
            network_sustainability: expect.any(Number),
            resource_sustainability: expect(Number),
            environmental_sustainability: expect.any(Number)
          }),
          renewalCapability: expect.objectContaining({
            selfRenewal: expect.any(Number),
            externalDependence: expect.any(Number),
            adaptationCapacity: expect.any(Number),
            learningCapability: expect.any(Number)
          }),
          longTermViability: expect.objectContaining({
            projectedLifespan: expect.any(Number),
            scalabilityPotential: expect.any(Number),
            resilienceToChange: expect.any(Number)
          }),
          riskAssessment: expect.object({
            sustainabilityRisks: expect.arrayContaining([
              expect.objectContaining({
                risk: expect.any(String),
                probability: expect.any(Number),
                impact: expect.any(Number),
                mitigation: expect.any(Array)
              })
            ]),
            riskLevel: expect.stringMatching(/high|medium|low/)
          })
        })
      );
    });
  });

  describe('中文本土化适配测试', () => {
    test('应该识别中国特色的动员机制', () => {
      // Arrange
      const chineseMobilizationText = `
        通过行政层级体系，实现了自上而下的政策动员。
        利用党组织体系，充分发挥了政治优势和组织力量。
        通过单位制度，调动了组织资源和管理能力。
        利用关系网络，加强了跨部门协作效率。
        通过绩效考核制度，激励参与者的积极性。
        通过问责机制，确保了执行的有效性。
      `;

      // Act
      const chineseAnalysis = analyzer.analyzeChineseMobilizationPatterns(chineseMobilizationText);

      // Assert
      expect(chineseAnalysis).toEqual(
        expect.objectContaining({
          administrativeSystem: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('行政层级体系'),
              direction: expect.stringContaining('自上而下'),
              effectiveness: expect.any(Number)
            })
          ]),
          partyOrganization: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('党组织体系'),
              advantage: expect.stringContaining('政治优势'),
              effectiveness: expect.any(Number)
            })
          ]),
          danweiSystem: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('单位制度'),
              capability: expect.stringContaining('组织资源'),
              effectiveness: expect.any(Number)
            })
          ]),
          performanceSystem: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('绩效考核'),
              motivation: expect.stringContaining('激励参与者'),
              effectiveness: expect.any(Number)
            })
          ]),
          accountabilityMechanism: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('问责机制'),
              function: expect.stringContaining('确保执行'),
              effectiveness: expect.any(Number)
            })
          ])
        })
      );
    });
  });

    test('应该分析动员过程中的文化因素', () => {
      // Arrange
      const culturalText = `
        通过集体主义价值观，增强了团队凝聚力。
        利用层级思维，建立了清晰的指挥体系。
        通过关系导向，促进了内部协调。
        通过面子文化，提高了参与者的责任感。
        通过集体荣誉感，激发了团队的工作热情。
      `;

      // Act
      const culturalAnalysis = analyzer.analyzeCulturalFactors(culturalText);

      // Assert
      expect(culturalAnalysis).toEqual(
        expect.objectContaining({
          collectivistValues: expect.arrayContaining([
            expect.objectContaining({
              value: expect.stringContaining('集体主义'),
              impact: expect.stringContaining('团队凝聚力'),
              strength: expect.any(Number)
            })
          ]),
          hierarchicalStructure: expect.arrayContaining([
            expect.objectContaining({
              structure: expect.stringContaining('层级思维'),
              function: expect.stringContaining('指挥体系'),
              effectiveness: expect.any(Number)
            })
          ]),
          relationshipOrientation: expect.arrayContaining([
            expect.objectContaining({
              orientation: expect.stringContaining('关系导向'),
              impact: expect.stringContaining('内部协调'),
              effectiveness: expect.any(Number)
            })
          ]),
          culturalNorms: expect.arrayContaining([
            expect.objectContaining({
              norm: expect.stringContaining('面子文化'),
              function: expect.stringContaining('责任感'),
              strength: expect.any(Number)
            })
          ])
        })
      );
    });
  });
  });

  describe('错误处理和边界条件', () => {
    test('应该处理无效的动员数据', () => {
      // Arrange
      const invalidData = {
        mechanisms: null,
        effects: undefined,
        metrics: []
      };

      // Act
      const assessment = analyzer.assessMobilizationEffectiveness(invalidData);

      // Assert
      expect(assessment).toEqual(
        expect.objectContaining({
          status: 'error',
          errors: expect.arrayContaining([
            expect.stringContaining('invalid_data')
          ]),
          recommendations: expect.arrayContaining([
            expect.stringContaining('提供有效数据')
          ])
        })
      );
    });

    test('应该处理动员过程中的危机', () => {
      // Arrange
      const crisisText = `
        动员过程中出现了严重的资源不足问题。
        参与者之间产生了不可调和的利益冲突。
        外部环境发生了重大变化，导致计划失效。
        关键参与者突然退出，影响了网络稳定性。
        协调机制失灵，导致执行效率低下。
        评估指标设置不合理，无法准确反映实际情况。
      `;

      // Act
      const crisisAnalysis = analyzer.analyzeMobilizationCrisis(crisisText);

      // Assert
      expect(crisisAnalysis).toEqual(
        expect.objectContaining({
          crisisTypes: expect.arrayContaining([
            expect.objectContaining({
              type: 'resource_shortage',
              severity: expect.stringMatching(/critical|serious|minor/),
              impact: expect.stringMatching(/critical|significant|moderate/)
            }),
            expect.objectContaining({
              type: 'interest_conflict',
              severity: expect.stringMatching(/critical|serious|minor/),
              impact: expect.stringMatching(/critical|significant|moderate/)
            })
          ]),
          crisisImpact: expect.objectContaining({
            stabilityLevel: expect.stringMatching(/critical|impaired/compromised/),
            disruptionLevel: expect.stringMatching(/high|medium|low/),
            recoveryTimeframe: expect.any(String)
          }),
          responseStrategies: expect.arrayContaining([
            expect.objectContaining({
              strategy: expect.any(String),
              effectiveness: expect.stringMatching(/high|medium|low/),
              urgency: expect.stringMatching(/immediate|prompt|gradual/),
              resources: expect.arrayContaining([
                expect.any(String)
              ])
            })
          ]),
          learningPoints: expect.arrayContaining([
            expect.stringContaining('resourcePlanning'),
            expect.stringContaining('conflictResolution'),
            expect.stringContaining('mechanismImprovement')
          ])
        })
      );
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内处理复杂的动员分析', () => {
      // Arrange - 创建复杂的动员文本
      const complexText = `
        该动员过程采用了系统化的方法论，首先建立清晰的动员目标体系，
        确保所有参与者对目标有共同的理解和认同。通过多层次的沟通机制，
        及时传递重要信息和决策。其次，建立了完善的激励系统，包括物质激励和精神激励，
        根据参与者的不同需求和动机，设计个性化的激励方案。第三，构建了高效的协调机制，
        通过定期的协调会议和项目管理系统，确保各方步调一致。第四，建立了监督评估体系，
        通过设定明确的KPI指标和评估周期，持续跟踪进展和效果。最后，
        建立了反馈学习机制，根据实际效果调整动员策略和方法。
        整个动员过程涉及政府部门15个，企业32家，学术机构8家，媒体机构12个。
        动员周期为18个月，分为启动、发展、成熟、稳定四个阶段。
        投入总预算8000万元，其中人力资源4000万元，物质资源3000万元，其他1000万元。
        动员效果包括：网络稳定性提升65%，目标达成率85%，参与度达到90%。
        关键成功因素包括：政府支持力度大，激励机制设计合理，协调机制有效。
        主要挑战包括：利益协调复杂，资源整合困难，时间跨度长。
        后续建议：继续加强协调机制建设，优化激励机制设计，完善监督评估体系。
      `.repeat(3);

      // Act
      const startTime = Date.now();
      const mobilization = analyzer.analyzeMobilizationMechanisms(complexText);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(5000); // 5秒内完成
      expect(mobilization.mechanisms.length).toBeGreaterThan(0);
      expect(mobilization.mobilizationEffectiveness.overallEffectiveness).toBeGreaterThan(0);
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