/**
 * TDD测试 - CapitalMapper类测试
 * 遵循AAA模式：Arrange-Act-Assert
 * 测试布迪厄资本理论映射的准确性
 */

const CapitalMapper = require('../../src/CapitalMapper');
const { CapitalType, CapitalForm } = require('../../../shared/types/CapitalTypes');

describe('CapitalMapper', () => {
  let mapper;

  beforeEach(() => {
    // Arrange - 准备测试环境
    mapper = new CapitalMapper();
  });

  describe('资本类型识别', () => {
    test('应该正确识别文化资本', () => {
      // Arrange
      const actorData = {
        education: ['清华大学博士', '哈佛大学博士后'],
        publications: ['SCI论文20篇', '专著2部'],
        academicAwards: ['国家自然科学奖', '长江学者'],
        languages: ['英语流利', '法语基础'],
        culturalKnowledge: ['古典音乐', '书法艺术'],
        teachingExperience: '15年'
      };

      // Act
      const culturalCapital = mapper.identifyCulturalCapital(actorData);

      // Assert
      expect(culturalCapital).toEqual(
        expect.objectContaining({
          embodiedCapital: expect.objectContaining({
            languageSkills: expect.any(Number),
            culturalTaste: expect.any(Number),
            educationalCredentials: expect.any(Number)
          }),
          objectifiedCapital: expect.objectContaining({
            publications: expect.any(Number),
            culturalAssets: expect.any(Number),
            intellectualProducts: expect.any(Number)
          }),
          institutionalizedCapital: expect.objectContaining({
            academicDegrees: expect.any(Number),
            professionalTitles: expect.any(Number),
            awardsRecognition: expect.any(Number)
          }),
          totalCulturalCapital: expect.any(Number)
        })
      );
    });

    test('应该正确识别社会资本', () => {
      // Arrange
      const networkData = {
        professionalNetworks: ['中国化学会', '国际物理学会'],
        alumniNetworks: ['清华大学校友会', '哈佛校友会'],
        institutionalAffiliations: ['中科院院士', '国家重点实验室主任'],
        personalRelationships: ['与多位部长有良好关系', '业界影响力大'],
        familyBackground: '学术世家',
        mentorshipRelations: ['师从著名科学家'],
        collaborativeProjects: 25
      };

      // Act
      const socialCapital = mapper.identifySocialCapital(networkData);

      // Assert
      expect(socialCapital).toEqual(
        expect.objectContaining({
          networkSize: expect.any(Number),
          networkDiversity: expect.any(Number),
          connectionStrength: expect.any(Number),
          resourceAccess: expect.any(Number),
          prestigeNetworks: expect.arrayContaining([
            expect.objectContaining({
              name: expect.any(String),
              type: expect.any(String),
              strength: expect.any(Number)
            })
          ]),
          guanxiCapital: expect.objectContaining({
            politicalConnections: expect.any(Number),
            businessConnections: expect.any(Number),
            academicConnections: expect.any(Number)
          })
        })
      );
    });

    test('应该正确识别经济资本', () => {
      // Arrange
      const economicData = {
        income: {
          salary: '年薪50万',
          consultingFees: '年咨询收入100万',
          bookRoyalties: '年稿费20万',
          stockOptions: '上市公司股权价值200万'
        },
        assets: {
          realEstate: '北京房产两套',
          investments: '股票基金组合',
          businessEquity: '科技创业公司股份'
        },
          fundingAccess: {
          researchGrants: '累计获得科研经费5000万',
          ventureCapital: '创业投资1000万',
          governmentSupport: '政府扶持资金300万'
        }
      };

      // Act
      const economicCapital = mapper.identifyEconomicCapital(economicData);

      // Assert
      expect(economicCapital).toEqual(
        expect.objectContaining({
          totalIncome: expect.any(Number),
          assetValue: expect.any(Number),
          fundingCapacity: expect.any(Number),
          economicMobility: expect.any(Number),
          incomeStability: expect.stringMatching(/high|medium|low/),
          riskProfile: expect.stringMatching(/conservative|moderate|aggressive/),
          capitalLiquidity: expect.any(Number)
        })
      );
    });

    test('应该正确识别象征资本', () => {
      // Arrange
      const symbolicData = {
        reputation: {
          academicReputation: '国际知名学者',
          publicRecognition: '频繁媒体曝光',
          peerRespect: '同行高度认可',
          studentAdmiration: '学生心目中的名师'
        },
        titles: {
          academicTitles: ['教授', '博导', '院士'],
          honoraryTitles: ['人民代表', '政协委员'],
          editorialPositions: ['期刊主编', '学会理事']
        },
        influence: {
          policyInfluence: '参与国家政策制定',
          thoughtLeadership: '学术思想影响力',
          mediaInfluence: '公众意见领袖',
          industryInfluence: '产业发展顾问'
        },
        legitimacy: {
          expertiseLegitimacy: '专业权威',
          moralAuthority: '道德声望',
          traditionalAuthority: '继承的声望',
          charismaticAuthority: '个人魅力'
        }
      };

      // Act
      const symbolicCapital = mapper.identifySymbolicCapital(symbolicData);

      // Assert
      expect(symbolicCapital).toEqual(
        expect.objectContaining({
          reputationScore: expect.any(Number),
          influenceScope: expect.arrayContaining([
            'academic',
            'policy',
            'public',
            'industry'
          ]),
          legitimacySources: expect.arrayContaining([
            expect.objectContaining({
              type: expect.any(String),
              strength: expect.any(Number)
            })
          ]),
          symbolicPower: expect.any(Number),
          recognitionLevel: expect.stringMatching(/international|national|regional|local/)
        })
      );
    });
  });

  describe('中国特色资本识别', () => {
    test('应该识别政治资本', () => {
      // Arrange
      const politicalData = {
        partyPositions: ['党委书记', '党支部委员'],
        governmentRoles: ['政协委员', '专家顾问'],
        administrativeRanks: ['厅级干部', '享受政府特殊津贴'],
        policyInfluence: '参与国家重大科技政策制定',
        stateHonors: ['全国劳动模范', '国家科技进步奖'],
        leadershipRoles: ['重点实验室主任', '学科带头人']
      };

      // Act
      const politicalCapital = mapper.identifyPoliticalCapital(politicalData);

      // Assert
      expect(politicalCapital).toEqual(
        expect.objectContaining({
          partyInfluence: expect.any(Number),
          governmentConnections: expect.any(Number),
          policyMakingPower: expect.any(Number),
          administrativeAuthority: expect.any(Number),
          stateRecognition: expect.any(Number),
          leadershipPosition: expect.stringMatching(/high|medium|low/),
          politicalNetwork: expect.objectContaining({
            centralLevel: expect.any(Number),
            provincialLevel: expect.any(Number),
            localLevel: expect.any(Number)
          })
        })
      );
    });

    test('应该识别关系资本', () => {
      // Arrange
      const guanxiData = {
        familyBackground: '革命干部家庭',
        classmateNetworks: '大学同学在重要岗位',
        hometownConnections: '老乡关系网',
        mentorshipRelations: '师从权威学者',
        businessFriendships: '与企业家长期合作',
        officialFriendships: '与政府官员良好关系',
        professionalColleagues: '行业内广泛人脉'
      };

      // Act
      const guanxiCapital = mapper.identifyGuanxiCapital(guanxiData);

      // Assert
      expect(guanxiCapital).toEqual(
        expect.objectContaining({
          familyNetwork: expect.any(Number),
          educationalNetwork: expect.any(Number),
          regionalNetwork: expect.any(Number),
          professionalNetwork: expect.any(Number),
          businessNetwork: expect.any(Number),
          officialNetwork: expect.any(Number),
          networkQuality: expect.objectContaining({
            diversity: expect.any(Number),
            strength: expect.any(Number),
            accessibility: expect.any(Number)
          }),
          guanxiUtilization: expect.objectContaining({
            informationAccess: expect.any(Number),
            resourceMobilization: expect.any(Number),
            problemSolving: expect.any(Number)
          })
        })
      );
    });
  });

  describe('资本分布分析', () => {
    test('应该分析群体资本分布', () => {
      // Arrange
      const groupData = [
        {
          name: '张教授',
          cultural: 90,
          social: 70,
          economic: 60,
          symbolic: 85,
          political: 40
        },
        {
          name: '李研究员',
          cultural: 70,
          social: 50,
          economic: 80,
          symbolic: 60,
          political: 30
        },
        {
          name: '王副教授',
          cultural: 60,
          social: 65,
          economic: 50,
          symbolic: 55,
          political: 25
        }
      ];

      // Act
      const distribution = mapper.analyzeCapitalDistribution(groupData);

      // Assert
      expect(distribution).toEqual(
        expect.objectContaining({
          capitalInequality: expect.objectContaining({
            giniCoefficient: expect.any(Number),
            concentrationIndex: expect.any(Number),
            inequalityLevel: expect.stringMatching(/low|medium|high/)
          }),
          capitalComposition: expect.objectContaining({
            culturalCapitalShare: expect.any(Number),
            socialCapitalShare: expect.any(Number),
            economicCapitalShare: expect.any(Number),
            symbolicCapitalShare: expect.any(Number),
            politicalCapitalShare: expect.any(Number)
          }),
          dominantCapitalType: expect.any(String),
          capitalStratification: expect.objectContaining({
            elite: expect.any(Number),
            upper: expect.any(Number),
            middle: expect.any(Number),
            lower: expect.any(Number)
          })
        })
      );
    });

    test('应该识别资本精英', () => {
      // Arrange
      const actorsData = [
        {
          name: '学术权威',
          capitals: { cultural: 95, social: 80, economic: 70, symbolic: 90, political: 60 }
        },
        {
          name: '管理精英',
          capitals: { cultural: 70, social: 85, economic: 80, symbolic: 75, political: 85 }
        },
        {
          name: '普通学者',
          capitals: { cultural: 60, social: 50, economic: 40, symbolic: 45, political: 20 }
        }
      ];

      // Act
      const elites = mapper.identifyCapitalElites(actorsData);

      // Assert
      expect(elites).toEqual(
        expect.objectContaining({
          eliteGroup: expect.arrayContaining([
            expect.objectContaining({
              name: expect.any(String),
              eliteType: expect.stringMatching(/academic|administrative|economic|political/),
              eliteScore: expect.toBeGreaterThan(0.8),
              dominanceAreas: expect.arrayContaining([
                expect.any(String)
              ])
            })
          ]),
          eliteCharacteristics: expect.objectContaining({
            capitalAdvantage: expect.any(Number),
            networkAdvantage: expect.any(Number),
            influenceAdvantage: expect.any(Number)
          }),
          eliteReproduction: expect.objectContaining({
            successionMechanisms: expect.arrayContaining([
              expect.any(String)
            ]),
            accessBarriers: expect.arrayContaining([
              expect.any(String)
            ])
          })
        })
      );
    });
  });

  describe('资本转换分析', () => {
    test('应该分析资本转换效率', () => {
      // Arrange
      const conversionData = {
        historicalConversions: [
          { from: 'cultural', to: 'economic', success: true, efficiency: 0.7 },
          { from: 'social', to: 'cultural', success: true, efficiency: 0.6 },
          { from: 'economic', to: 'symbolic', success: true, efficiency: 0.8 },
          { from: 'cultural', to: 'political', success: false, efficiency: 0.3 }
        ]
      };

      // Act
      const conversionAnalysis = mapper.analyzeCapitalConversion(conversionData);

      // Assert
      expect(conversionAnalysis).toEqual(
        expect.objectContaining({
          conversionMatrix: expect.objectContaining({
            'cultural_to_economic': expect.any(Number),
            'social_to_cultural': expect.any(Number),
            'economic_to_symbolic': expect.any(Number),
            'cultural_to_political': expect.any(Number)
          }),
          overallEfficiency: expect.any(Number),
          optimalConversions: expect.arrayContaining([
            expect.objectContaining({
              from: expect.any(String),
              to: expect.any(String),
              efficiency: expect.any(Number)
            })
          ]),
          conversionBarriers: expect.arrayContaining([
            expect.objectContaining({
              conversionType: expect.any(String),
              barrier: expect.any(String),
              severity: expect.any(Number)
            })
          ])
        })
      );
    });

    test('应该识别资本转换策略', () => {
      // Arrange
      const actorStrategy = {
        currentCapitals: { cultural: 80, social: 60, economic: 50, symbolic: 70 },
        targetPosition: '学院院长',
        positionRequirements: {
          cultural: 70,
          social: 80,
          economic: 60,
          symbolic: 85,
          political: 70
        }
      };

      // Act
      const strategies = mapper.identifyConversionStrategies(actorStrategy);

      // Assert
      expect(strategies).toEqual(
        expect.objectContaining({
          capitalGaps: expect.objectContaining({
            cultural: expect.any(Number),
            social: expect.any(Number),
            economic: expect.any(Number),
            symbolic: expect.any(Number)
          }),
          conversionPaths: expect.arrayContaining([
            expect.objectContaining({
              from: expect.any(String),
              to: expect.any(String),
              path: expect.arrayContaining([expect.any(String)]),
              expectedEfficiency: expect.any(Number)
            })
          ]),
          investmentPriorities: expect.arrayContaining([
            expect.objectContaining({
              capitalType: expect.any(String),
              priority: expect.stringMatching(/high|medium|low/),
              expectedROI: expect.any(Number)
            })
          ])
        })
      );
    });
  });

  describe('错误处理和边界条件', () => {
    test('应该处理不完整的资本数据', () => {
      // Arrange
      const incompleteData = {
        education: ['清华大学博士'],
        publications: null,
        academicAwards: undefined,
        languages: [],
        culturalKnowledge: undefined
      };

      // Act
      const culturalCapital = mapper.identifyCulturalCapital(incompleteData);

      // Assert
      expect(culturalCapital).toEqual(
        expect.objectContaining({
          totalCulturalCapital: expect.any(Number),
          dataCompleteness: expect.toBeLessThan(1),
          missingFields: expect.arrayContaining([
            expect.stringContaining('publications'),
            expect.stringContaining('academicAwards')
          ])
        })
      );
    });

    test('应该处理极端资本值', () => {
      // Arrange
      const extremeData = {
        cultural: -10, // 负值
        social: 150,    // 超过最大值
        economic: 0,
        symbolic: 'invalid' // 无效值
      };

      // Act
      const normalizedCapital = mapper.normalizeCapitalValues(extremeData);

      // Assert
      expect(normalizedCapital).toEqual(
        expect.objectContaining({
          cultural: 0,      // 负值应该被修正为0
          social: 100,      // 超过最大值应该被修正为100
          economic: 0,
          symbolic: expect.any(Number) // 应该有默认值
        })
      );
    });

    test('应该处理矛盾的资本信息', () => {
      // Arrange
      const contradictoryData = {
        education: ['清华大学博士'],
        income: '年薪10万',
        assets: '资产价值10亿', // 与收入不匹配
        reputation: '无名小卒',
        titles: ['诺贝尔奖得主'] // 与声誉不匹配
      };

      // Act
      const consistencyCheck = mapper.checkDataConsistency(contradictoryData);

      // Assert
      expect(consistencyCheck).toEqual(
        expect.objectContaining({
          consistencyScore: expect.toBeLessThan(0.8),
          contradictions: expect.arrayContaining([
            expect.objectContaining({
              field: expect.any(String),
              conflict: expect.any(String),
              severity: expect.stringMatching(/low|medium|high/)
            })
          ]),
          recommendations: expect.arrayContaining([
            expect.stringContaining('验证')
          ])
        })
      );
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内处理大量资本数据', () => {
      // Arrange - 创建大量actor数据
      const largeDataset = [];
      for (let i = 0; i < 1000; i++) {
        largeDataset.push({
          name: `Actor${i}`,
          cultural: Math.random() * 100,
          social: Math.random() * 100,
          economic: Math.random() * 100,
          symbolic: Math.random() * 100,
          political: Math.random() * 100
        });
      }

      // Act
      const startTime = Date.now();
      const distribution = mapper.analyzeCapitalDistribution(largeDataset);
      const endTime = Date.now();

      // Assert
      expect(endTime - startTime).toBeLessThan(3000); // 3秒内完成
      expect(distribution).toBeDefined();
      expect(distribution.capitalInequality).toBeDefined();
    });
  });
});