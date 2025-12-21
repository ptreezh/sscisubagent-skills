/**
 * TDD测试 - InteressementAnalyzer类测试
 * 遵循AAA模式：Arrange-Act-Assert
 * 测试ANT兴趣化环节的理论准确性
 */

const InteressementAnalyzer = require('../../src/InteressementAnalyzer');
const { InteressementMechanism, TranslationPhase } = require('../../../shared/types/TranslationTypes');

describe('InteressementAnalyzer', () => {
  let analyzer;

  beforeEach(() => {
    // Arrange - 准备测试环境
    analyzer = new InteressementAnalyzer();
  });

  describe('利益对齐机制分析', () => {
    test('应该正确识别企业对环保政策的兴趣化策略', () => {
      // Arrange
      const enterpriseText = `
        通过提供环保技术补贴，政府成功吸引了企业参与治理。
        环保认证为企业带来了品牌价值和市场优势。
        绿色金融政策为企业提供了低成本的融资渠道。
        参与环保项目可以获得政府的政策支持和税收优惠。
        环保合规成为企业获得政府订单的必要条件。
      `;

      // Act
      const interessement = analyzer.analyzeInteressement(enterpriseText);

      // Assert
      expect(interessement).toEqual(
        expect.objectContaining({
          mechanisms: expect.arrayContaining([
            expect.objectContaining({
              type: InteressementMechanism.INCENTIVE_ALIGNMENT,
              device: expect.stringContaining('补贴'),
              targetedActors: expect.arrayContaining([
                '企业'
              ]),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              type: InteressementMechanism.PERSUASIVE_DEVICES,
              device: expect.stringContaining('环保认证'),
              targetedActors: expect.arrayContaining([
                '企业'
              ]),
              effectiveness: expect.any(Number)
            })
          ]),
          devices: expect.arrayContaining([
            expect.objectContaining({
              name: expect.any(String),
              type: expect.stringMatching(/economic|symbolic|technical|legal/),
              function: expect.any(String),
              targetGroup: expect.any(Array)
            })
          ]),
          interestAlignment: expect.objectContaining({
            alignmentLevel: expect.any(Number),
            keyAlignments: expect.arrayContaining([
              expect.objectContaining({
                actor: expect.stringContaining('企业'),
                interest: expect.any(String),
                alignmentMethod: expect.any(String),
                strength: expect.any(Number)
              })
            ]),
            misalignmentSources: expect.any(Array),
            alignmentStability: expect.stringMatching(/high|medium|low/)
          })
        })
      );
    });

    test('应该分析技术采纳中的兴趣化过程', () => {
      // Arrange
      const technologyText = `
        新技术通过展示生产效率提升的效果，吸引了制造商的兴趣。
        技术培训项目降低了员工的学习成本和适应阻力。
        专利保护为技术开发者提供了市场独占优势。
        开放平台策略吸引了更多开发者和合作伙伴。
        标准化接口降低了系统集成的技术门槛。
      `;

      // Act
      const interessement = analyzer.analyzeInteressement(technologyText);

      // Assert
      expect(interessement).toEqual(
        expect.objectContaining({
          interestAlignment: expect.objectContaining({
            actorGroups: expect.arrayContaining([
              expect.objectContaining({
                group: '制造商',
                primaryInterests: expect.arrayContaining([
                  '生产效率提升'
                ]),
                engagementLevel: expect.any(Number)
              }),
              expect.objectContaining({
                group: '开发者',
                primaryInterests: expect.arrayContaining([
                  '平台机会'
                ]),
                engagementLevel: expect.any(Number)
              })
            ])
          }),
          deviceEffectiveness: expect.objectContaining({
            economicDevices: expect.any(Number),
            symbolicDevices: expect.any(Number),
            technicalDevices: expect.any(Number),
            overallEffectiveness: expect.any(Number)
          })
        })
      );
    });
  });

  describe('替代方案消除分析', () => {
    test('应该识别政策实施中的替代方案消除', () => {
      // Arrange
      const eliminationText = `
        通过严格的环保标准，有效排除了传统高污染技术的使用空间。
        市场准入机制阻止了不达标企业的经营活动。
        政府采购政策仅支持符合环保标准的产品和服务。
        资格认证制度限制了不合规供应商的市场准入。
        技术标准强制淘汰了落后的生产工艺。
      `;

      // Act
      const elimination = analyzer.analyzeAlternativeElimination(eliminationText);

      // Assert
      expect(elimination).toEqual(
        expect.objectContaining({
          eliminatedAlternatives: expect.arrayContaining([
            expect.objectContaining({
              alternative: expect.stringContaining('高污染技术'),
              eliminationMethod: expect.stringContaining('环保标准'),
              effectiveness: expect.any(Number),
              persistence: expect.stringMatching(/permanent|temporary|partial/)
            }),
            expect.objectContaining({
              alternative: expect.stringContaining('不达标企业'),
              eliminationMethod: expect.stringContaining('市场准入'),
              effectiveness: expect.any(Number),
              persistence: expect.stringMatching(/permanent|temporary|partial/)
            })
          ]),
          eliminationMechanisms: expect.arrayContaining([
            expect.objectContaining({
              mechanism: expect.stringContaining('标准制定'),
              scope: expect.any(String),
              enforcement: expect.any(String),
              resistanceLevel: expect.stringMatching(/high|medium|low/)
            })
          ]),
          eliminationEffectiveness: expect.objectContaining({
            totalEliminated: expect.any(Number),
            permanentlyEliminated: expect.any(Number),
            temporarilyEliminated: expect.any(Number),
            residualThreats: expect.arrayContaining([
              expect.any(String)
            ])
          })
        })
      );
    });

    test('应该评估消除策略的系统性', () => {
      // Arrange
      const systemicText = `
        通过多层次的政策组合，形成了完整的替代方案消除体系。
        法律法规提供了制度保障，确保消除政策的权威性。
        经济激励调整了市场行为，引导参与者主动放弃替代方案。
        技术标准设置了客观门槛，使替代方案失去可行性。
        社会舆论创造了环境压力，增强消除政策的接受度。
      `;

      // Act
      const systematicAnalysis = analyzer.analyzeSystematicElimination(systemicText);

      // Assert
      expect(systematicAnalysis).toEqual(
        expect.objectContaining({
          eliminationStrategy: expect.objectContaining({
            approach: expect.stringMatching(/comprehensive|targeted|gradual/),
            coordinationLevel: expect.any(Number),
            mechanismIntegration: expect.any(Number)
          }),
          coverageAnalysis: expect.objectContaining({
            legalCoverage: expect.any(Number),
            economicCoverage: expect.any(Number),
            technicalCoverage: expect.any(Number),
            socialCoverage: expect.any(Number),
            overallCoverage: expect.any(Number)
          }),
          sustainabilityAssessment: expect.objectContaining({
            institutionalSustainability: expect.any(Number),
            economicSustainability: expect.any(Number),
            politicalSustainability: expect.any(Number),
            overallSustainability: expect.any(Number)
          })
        })
      );
    });
  });

  describe('说服装置分析', () => {
    test('应该识别和分析各种说服装置', () => {
      // Arrange
      const persuasionText = `
        统计数据图表直观展示了污染问题的严重程度，增强了政策说服力。
        成功案例展示证明了环保措施的可行性和效果。
        专家背书为政策提供了科学权威性支持。
        媒体报道扩大了政策影响，提高了公众认知度。
        激励机制设计巧妙地平衡了各方利益关系。
      `;

      // Act
      const persuasionAnalysis = analyzer.analyzePersuasiveDevices(persuasionText);

      // Assert
      expect(persuasionAnalysis).toEqual(
        expect.objectContaining({
          devices: expect.arrayContaining([
            expect.objectContaining({
              type: 'statistical_evidence',
              description: expect.stringContaining('统计数据图表'),
              targetAudience: expect.arrayContaining([
                '决策者',
                '专业人士'
              ]),
              persuasionMechanism: expect.stringContaining('理性说服'),
              credibility: expect.any(Number),
              emotionalAppeal: expect.any(Number)
            }),
            expect.objectContaining({
              type: 'case_demonstration',
              description: expect.stringContaining('成功案例'),
              targetAudience: expect.arrayContaining([
                '企业',
                '公众'
              ]),
              persuasionMechanism: expect.stringContaining('事实说服'),
              credibility: expect.any(Number),
              emotionalAppeal: expect.any(Number)
            })
          ]),
          deviceEffectiveness: expect.objectContaining({
            overallEffectiveness: expect.any(Number),
            credibilityScores: expect.objectContaining({
              statistical: expect.any(Number),
              testimonial: expect.any(Number),
              expert: expect.any(Number),
              media: expect.any(Number)
            }),
            emotionalImpact: expect.objectContaining({
              fearAppeal: expect.any(Number),
              hopeAppeal: expect.any(Number),
              authorityAppeal: expect.any(Number),
              socialProof: expect.any(Number)
            })
          })
        })
      );
    });
  });

  describe('利益重新定义分析', () => {
    test('应该识别利益概念的重新框架化', () => {
      // Arrange
      const reframingText = `
        通过成本效益分析，将环保支出重新定义为投资而非成本。
        将技术升级需求重新定义为创新机遇而非技术威胁。
        将监管要求重新定义为竞争优势而非合规负担。
        将社会责任重新定义为品牌价值而非额外成本。
        将绿色转型重新定义为发展机遇而非转型风险。
      `;

      // Act
      const reframingAnalysis = analyzer.analyzeInterestReframing(reframingText);

      // Assert
      expect(reframingAnalysis).toEqual(
        expect.objectContaining({
          reframingProcesses: expect.arrayContaining([
            expect.objectContaining({
              originalFrame: expect.stringContaining('成本'),
              reframedFrame: expect.stringContaining('投资'),
              reframingStrategy: expect.stringContaining('成本效益分析'),
              targetAudience: expect.arrayContaining([
                '企业管理者'
              ]),
              effectiveness: expect.any(Number)
            }),
            expect.objectContaining({
              originalFrame: expect.stringContaining('监管要求'),
              reframedFrame: expect.stringContaining('竞争优势'),
              reframingStrategy: expect.any(String),
              targetAudience: expect.arrayContaining([
                '企业'
              ]),
              effectiveness: expect.any(Number)
            })
          ]),
          reframingEffectiveness: expect.objectContaining({
            acceptanceIncrease: expect.any(Number),
            resistanceDecrease: expect.any(Number),
            engagementLevel: expect.any(Number),
            overallSuccess: expect.any(Number)
          }),
          cognitiveShift: expect.objectContaining({
            fromNegative: expect.arrayContaining([
              '负担',
              '威胁',
              '成本'
            ]),
            toPositive: expect.arrayContaining([
              '投资',
              '机遇',
              '价值'
            ]),
            shiftMagnitude: expect.any(Number)
          })
        })
      );
    });
  });

  describe('兴趣化效果评估', () => {
    test('应该评估兴趣化过程的成功程度', () => {
      // Arrange
      const successText = `
        各方利益相关者基本接受了政策方案，支持率达到85%。
        主要利益冲突得到有效化解，对抗情绪显著降低。
      替代方案被成功排除，各方只能沿着既定路径行动。
      政策实施过程中遇到的阻力很小，各方配合度很高。
      利益联盟稳固，网络稳定性达到预期水平。
      `;

      // Act
      const successAssessment = analyzer.assessInteressementSuccess(successText);

      // Assert
      expect(successAssessment).toEqual(
        expect.objectContaining({
          successLevel: expect.stringMatching(/high|medium|low/),
          alignmentMetrics: expect.objectContaining({
            stakeholderAlignment: expect.any(Number),
            interestCompatibility: expect.any(Number),
            commitmentLevel: expect.any(Number)
          }),
          resistanceManagement: expect.objectContaining({
            oppositionLevel: expect.any(Number),
            resistanceSources: expect.arrayContaining([
              expect.any(String)
            ]),
            neutralizationEffectiveness: expect.any(Number)
          }),
          enrollmentReadiness: expect.objectContaining({
            willingnessToAct: expect.any(Number),
            resourceCommitment: expect.any(Number),
            coordinationReadiness: expect.any(Number)
          })
        })
      );
    });

    test('应该识别兴趣化失败的原因', () => {
      // Arrange
      const failureText = `
        利益激励设计不当，未能有效调动各方积极性。
        说服装置缺乏说服力，无法改变现有认知框架。
        替代方案未被有效排除，仍有绕行空间存在。
        利益重新定义不成功，原有利益观念仍然占主导。
      `;

      // Act
      const failureAnalysis = analyzer.analyzeInteressementFailure(failureText);

      // Assert
      expect(failureAnalysis).toEqual(
        expect.objectContaining({
          failureFactors: expect.arrayContaining([
            expect.objectContaining({
              factor: expect.stringContaining('利益激励'),
              severity: expect.stringMatching(/high|medium|low/),
              description: expect.any(String)
            }),
            expect.objectContaining({
              factor: expect.stringContaining('说服装置'),
              severity: expect.stringMatching(/high|medium|low/),
              description: expect.any(String)
            })
          ]),
          improvementRecommendations: expect.arrayContaining([
            expect.objectContaining({
              recommendation: expect.any(String),
              priority: expect.stringMatching(/high|medium|low/),
              expectedImpact: expect.stringMatching(/high|medium|low/)
            })
          ]),
          recoveryStrategies: expect.arrayContaining([
            expect.objectContaining({
              strategy: expect.any(String),
              timeline: expect.any(String),
              resourceRequirements: expect.any(Array),
              successProbability: expect.any(Number)
            })
          ])
        })
      );
    });
  });

  describe'中文本土化适配测试', () => {
    test('应该识别中国特色的利益化策略', () => {
      // Arrange
      const chineseText = `
        通过政府背书，为企业提供了政策支持和信誉保障。
        利用关系网络，加强了各方之间的互信与合作。
        官员身份带来了社会地位和专业认可的双重收益。
        单位制度下的组织资源为政策实施提供了制度保障。
        行政级别确保了政策执行的权威性和有效性。
      `;

      // Act
      const chineseAdaptation = analyzer.analyzeChineseInteressement(chineseText);

      // Assert
      expect(chineseAdaptation).toEqual(
        expect.objectContaining({
          guanxiMechanisms: expect.arrayContaining([
            expect.objectContaining({
              type: 'relationship_network',
              description: expect.stringContaining('关系网络'),
              effectiveness: expect.any(Number),
              culturalContext: expect.stringContaining('关系社会')
            })
          ]),
          institutionalFeatures: expect.arrayContaining([
            expect.objectContaining({
              institution: expect.stringContaining('单位制度'),
              mechanism: expect.stringContaining('组织资源'),
              influenceLevel: expect.any(Number)
            })
          ]),
          administrativeInfluence: expect.arrayContaining([
            expect.objectContaining({
              level: expect.stringContaining('行政级别'),
              effect: expect.stringContaining('权威性'),
              scope: expect.any(String)
            })
          ])
        })
      );
    });
  });
});