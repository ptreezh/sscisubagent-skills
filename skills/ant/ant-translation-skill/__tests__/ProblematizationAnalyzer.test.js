/**
 * TDD测试 - ProblematizationAnalyzer类测试
 * 遵循AAA模式：Arrange-Act-Assert
 * 测试ANT问题化环节的理论准确性
 */

const ProblematizationAnalyzer = require('../../src/ProblematizationAnalyzer');
const { ProblematizationType, TranslationPhase } = require('../../../shared/types/TranslationTypes');

describe('ProblematizationAnalyzer', () => {
  let analyzer;

  beforeEach(() => {
    // Arrange - 准备测试环境
    analyzer = new ProblematizationAnalyzer();
  });

  describe('问题定义识别', () => {
    test('应该正确识别环境政策的问题化过程', () => {
      // Arrange
      const policyText = `
        面对日益严重的环境污染问题，必须采取有效措施进行治理。
        当前的环境监管体系存在漏洞，导致企业违规排污现象频发。
        传统治理方法效果有限，需要创新的治理模式来解决这一问题。
        必须建立一套完整的环保标准和监管机制，才能有效控制污染。
      `;

      // Act
      const problematization = analyzer.analyzeProblematization(policyText);

      // Assert
      expect(problematization).toEqual(
        expect.objectContaining({
          problems: expect.arrayContaining([
            expect.objectContaining({
              type: ProblematizationType.PROBLEM_DEFINITION,
              description: expect.stringContaining('环境污染问题'),
              severity: expect.stringMatching(/high|medium|low/),
              urgency: expect.any(Number)
            })
          ]),
          solutions: expect.arrayContaining([
            expect.objectContaining({
              type: ProblematizationType.SOLUTION_PROPOSAL,
              description: expect.stringContaining('治理模式'),
              feasibility: expect.any(Number)
            })
          ]),
          obligatoryPassagePoints: expect.arrayContaining([
            expect.objectContaining({
              description: expect.stringContaining('环保标准'),
              necessity: expect.stringMatching(/critical|important|optional/),
              controlLevel: expect.any(Number)
            })
          ]),
          controversyDefinition: expect.any(String)
        })
      );
    });

    test('应该识别技术采纳的问题化框架', () => {
      // Arrange
      const technologyText = `
        传统的人工操作效率低下，无法满足现代生产需求。
        现有技术系统存在安全隐患，需要升级改造。
        如果不采用新技术，企业将失去市场竞争力。
        引入自动化系统是解决生产效率问题的唯一途径。
        但是新技术的成本高昂，需要政府补贴支持。
      `;

      // Act
      const problematization = analyzer.analyzeProblematization(technologyText);

      // Assert
      expect(problematization).toEqual(
        expect.objectContaining({
          problems: expect.arrayContaining([
            expect.objectContaining({
              description: expect.stringContaining('效率低下'),
              stakeholders: expect.arrayContaining([
                '企业',
                '员工'
              ])
            })
          ]),
          solutions: expect.arrayContaining([
            expect.objectContaining({
              description: expect.stringContaining('自动化系统'),
              barriers: expect.arrayContaining([
                expect.stringContaining('成本高昂')
              ])
            })
          ]),
          controversyFrame: expect.objectContaining({
            mainConflict: expect.stringContaining('成本与效益'),
            opposingForces: expect.arrayContaining([
              expect.any(String),
              expect.any(String)
            ])
          })
        })
      );
    });

    test('应该识别复杂社会问题的多维性', () => {
      // Arrange
      const socialIssueText = `
        城市交通拥堵问题日益严重，影响了居民的生活质量。
        现有的公共交通系统覆盖不足，无法满足出行需求。
        私家车数量激增，道路基础设施建设滞后。
        交通拥堵不仅造成经济损失，还影响社会公平。
        解决方案需要综合考虑土地利用、公共交通、交通管理等多个方面。
      `;

      // Act
      const problematization = analyzer.analyzeProblematization(socialIssueText);

      // Assert
      expect(problematization).toEqual(
        expect.objectContaining({
          problemComplexity: expect.objectContaining({
            dimensions: expect.arrayContaining([
              '经济影响',
              '社会公平',
              '基础设施',
              '生活质量'
            ]),
            complexityLevel: expect.stringMatching(/low|medium|high/),
            interconnectedness: expect.any(Number)
          }),
          stakeholderAnalysis: expect.objectContaining({
            affectedGroups: expect.arrayContaining([
              expect.stringContaining('居民'),
              expect.stringContaining('企业'),
              expect.stringContaining('政府')
            ]),
            powerDistribution: expect.any(Object),
            interestAlignment: expect.any(Object)
          })
        })
      );
    });
  });

  describe('必经节点分析', () => {
    test('应该识别政策实施的关键节点', () => {
      // Arrange
      const implementationText = `
        要有效实施环保政策，必须通过环境审批这一关键环节。
        所有企业都必须获得环保许可证才能运营。
        环保部门具有最终审批权，任何不符合标准的项目都无法通过。
        市场监管部门配合执行违规处罚，确保政策权威性。
        财政部门提供专项资金支持，为政策实施提供保障。
      `;

      // Act
      const passagePoints = analyzer.identifyObligatoryPassagePoints(implementationText);

      // Assert
      expect(passagePoints).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            name: expect.stringContaining('环境审批'),
            type: 'regulatory_control',
            controlMechanism: expect.stringContaining('审批权'),
            bypassOptions: expect.any(Array),
            enforcementMechanism: expect.any(String)
          }),
          expect.objectContaining({
            name: expect.stringContaining('环保许可证'),
            type: 'certification_requirement',
            controlMechanism: expect.stringContaining('许可制度'),
            bypassOptions: expect.any(Array),
            enforcementMechanism: expect.any(String)
          })
        ])
      );
    });

    test('应该评估必经节点的控制强度', () => {
      // Arrange
      const controlText = `
        核心算法掌握在少数几家大公司手中，这是技术发展的瓶颈。
        数据访问权限受到严格控制，没有授权无法获取关键数据。
        行业标准由主要参与者制定，新进入者难以改变规则。
        专利技术形成了技术壁垒，绕过需要支付高昂成本。
      `;

      // Act
      const controlAnalysis = analyzer.analyzeControlStrength(controlText);

      // Assert
      expect(controlAnalysis).toEqual(
        expect.objectContaining({
          overallControlLevel: expect.any(Number),
          controlPoints: expect.arrayContaining([
            expect.objectContaining({
              name: expect.any(String),
              controlStrength: expect.any(Number),
              controlType: expect.stringMatching(/formal|informal|technical|legal/),
              vulnerability: expect.stringMatching(/high|medium|low/),
              bypassComplexity: expect.any(Number)
            })
          ]),
          networkControl: expect.objectContaining({
            centralizationLevel: expect.any(Number),
            distributionMechanism: expect.any(String),
            accessRestrictions: expect.arrayContaining([
              expect.any(String)
            ])
          })
        })
      );
    });
  });

  describe('争议框架分析', () => {
    test('应该识别政策争议的核心冲突', () => {
      // Arrange
      const controversyText = `
        关于是否应该提高环保标准，存在激烈争论。
        环保组织认为必须严格标准以保护公共利益。
        企业界担心标准过高会增加成本负担。
        政府部门在经济发展和环境保护之间难以平衡。
        专家学者对标准的科学性和可行性也有不同看法。
      `;

      // Act
      const controversy = analyzer.analyzeControversy(controversyText);

      // Assert
      expect(controversy).toEqual(
        expect.objectContaining({
          centralConflict: expect.stringContaining('环保标准'),
          opposingForces: expect.arrayContaining([
            expect.objectContaining({
              group: expect.stringContaining('环保组织'),
              position: expect.stringContaining('严格标准'),
              arguments: expect.arrayContaining([
                expect.stringContaining('保护公共利益')
              ]),
              powerLevel: expect.any(Number)
            }),
            expect.objectContaining({
              group: expect.stringContaining('企业界'),
              position: expect.stringContaining('成本负担'),
              arguments: expect.arrayContaining([
                expect.stringContaining('成本')
              ]),
              powerLevel: expect.any(Number)
            })
          ]),
          controversyDimensions: expect.arrayContaining([
            '经济影响',
            '环境影响',
            '政治可行性'
          ]),
          resolutionProspects: expect.objectContaining({
            potentialSolutions: expect.arrayContaining([
              expect.any(String)
            ]),
            compromisePossibilities: expect.any(Number),
            stalemateRisk: expect.stringMatching(/high|medium|low/)
          })
        })
      );
    });

    test('应该分析争议的话语框架', () => {
      // Arrange
      const discourseText = `
        一些人将人工智能定义为"革命性技术"，强调其创新价值。
        另一些人则将其描述为"就业威胁"，关注其社会风险。
        "技术进步"与"社会稳定"形成对立的话语框架。
        "创新驱动"的话语与"监管必要"的话语产生冲突。
        不同的价值主张使得争议难以通过技术手段解决。
      `;

      // Act
      const discourseAnalysis = analyzer.analyzeDiscourseFrames(discourseText);

      // Assert
      expect(discourseAnalysis).toEqual(
        expect.objectContaining({
          competingFrames: expect.arrayContaining([
            expect.objectContaining({
              frame: expect.stringContaining('革命性技术'),
              metaphors: expect.arrayContaining([
                expect.stringContaining('技术')
              ]),
              values: expect.arrayContaining([
                '创新'
              ]),
              targetAudience: expect.any(String)
            }),
            expect.objectContaining({
              frame: expect.stringContaining('就业威胁'),
              metaphors: expect.arrayContaining([
                expect.stringContaining('风险')
              ]),
              values: expect.arrayContaining([
                '稳定'
              ]),
              targetAudience: expect.any(String)
            })
          ]),
          frameConflict: expect.objectContaining({
            incompatibleFrames: expect.arrayContaining([
              expect.any(String),
              expect.any(String)
            ]),
            fundamentalDifferences: expect.arrayContaining([
              expect.any(String)
            ]),
            resolutionDifficulty: expect.stringMatching(/low|medium|high/)
          }),
          discursivePower: expect.objectContaining({
            dominantFrame: expect.any(String),
            frameDistribution: expect.objectContaining({
              revolution: expect.any(Number),
              threat: expect.any(Number),
              innovation: expect.any(Number),
              regulation: expect.any(Number)
            }),
            frameShiftPossibility: expect.any(Number)
          })
        })
      );
    });
  });

  describe('问题化效果评估', () => {
    test('应该评估问题化的成功程度', () => {
      // Arrange
      const effectText = `
        通过定义明确的污染标准和监管机制，成功将企业纳入治理体系。
        环保部门的权威得到确立，政策执行效果显著。
        争议各方基本接受了治理框架，对抗程度降低。
        解决方案获得了广泛的社会认可，支持率较高。
      `;

      // Act
      const effectAssessment = analyzer.assessProblematizationEffect(effectText);

      // Assert
      expect(effectAssessment).toEqual(
        expect.objectContaining({
          successLevel: expect.stringMatching(/high|medium|low/),
          legitimacyEstablishment: expect.objectContaining({
            institutionalLegitimacy: expect.any(Number),
            socialLegitimacy: expect.any(Number),
            expertLegitimacy: expect.any(Number)
          }),
          enrollmentEffectiveness: expect.objectContaining({
            stakeholderAlignment: expect.any(Number),
            oppositionReduction: expect.any(Number),
          }),
          mobilizationReadiness: expect.objectContaining({
            resourceMobilization: expect.any(Number),
            coordinationEstablished: expect.any(Number)
          })
        })
      );
    });

    test('应该识别问题化的失败因素', () => {
      // Arrange
      const failureText = `
        问题定义不够清晰，各方对问题本质存在分歧。
        解决方案的可行性评估不足，实际执行困难重重。
        必经节点设置不合理，导致绕行行为频发。
        争议处理不当，对抗情绪加剧。
      `;

      // Act
      const failureAnalysis = analyzer.analyzeProblematizationFailure(failureText);

      // Assert
      expect(failureAnalysis).toEqual(
        expect.objectContaining({
          failureFactors: expect.arrayContaining([
            expect.objectContaining({
              factor: expect.stringContaining('问题定义'),
              severity: expect.stringMatching(/high|medium|low/),
              impact: expect.stringMatching(/critical|significant|moderate/)
            }),
            expect.objectContaining({
              factor: expect.stringContaining('必经节点'),
              severity: expect.stringMatching(/high|medium|low/),
              impact: expect.stringMatching(/critical|significant|moderate/)
            })
          ]),
          learningPoints: expect.arrayContaining([
            expect.stringContaining('问题定义'),
            expect.stringContaining('可行性评估')
          ]),
          improvementRecommendations: expect.arrayContaining([
            expect.objectContaining({
              recommendation: expect.any(String),
              priority: expect.stringMatching(/high|medium|low/),
              implementationComplexity: expect.stringMatching(/low|medium|high/)
            })
          ])
        })
      );
    });
  });

  describe('错误处理和边界条件', () => {
    test('应该处理无明确问题化的文本', () => {
      // Arrange
      const neutralText = '今天的天气很好，适合外出游玩。';

      // Act
      const problematization = analyzer.analyzeProblematization(neutralText);

      // Assert
      expect(problematization).toEqual(
        expect.objectContaining({
          problems: [],
          solutions: [],
          obligatoryPassagePoints: [],
          hasProblematization: false,
          completenessScore: 0
        })
      );
    });

    test('应该处理矛盾的问题定义', () => {
      // Arrange
      const contradictoryText = `
        这个技术既能解决所有问题，又可能带来更大风险。
        这个方案是最优选择，但也可能产生新的挑战。
        政府干预是必要的，但政府干预会降低效率。
      `;

      // Act
      const consistencyCheck = analyzer.checkProblemConsistency(contradictoryText);

      // Assert
      expect(consistencyCheck).toEqual(
        expect.objectContaining({
          consistencyLevel: expect.stringMatching(/low|medium|high/),
          contradictions: expect.arrayContaining([
            expect.objectContaining({
              type: expect.stringMatching(/logical|value|means_end/),
              description: expect.any(String),
              severity: expect.stringMatching(/high|medium|low/)
            })
          ]),
          clarificationNeeded: expect.arrayContaining([
            expect.any(String)
          ])
        })
      );
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内处理复杂政策文本', () => {
      // Arrange - 创建复杂的政策文本
      const complexText = `
        面对日益严重的环境污染问题，必须采取系统性治理措施。
        当前环境监管体系存在结构性缺陷，跨部门协调困难重重。
        传统末端治理模式效果有限，需要向源头治理转变。
        必须建立全方位的环境治理体系，包括法律、经济、技术、教育等多个维度。
        要充分发挥市场机制的作用，同时加强政府监管力度。
        必须平衡环境保护与经济发展的关系，实现可持续发展。
        国际环境合作日益重要，需要积极参与全球治理。
      `.repeat(3);

      // Act
      const startTime = Date.now();
      const problematization = analyzer.analyzeProblematization(complexText);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(3000); // 3秒内完成
      expect(problematization.problems.length).toBeGreaterThan(0);
      expect(problematization.solutions.length).toBeGreaterThan(0);
    });
  });
});