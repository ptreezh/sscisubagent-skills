/**
 * 商业模式分析技能测试套件
 */

const BusinessModelAnalysisSkill = require('./skill.js');
const assert = require('assert');

class BusinessModelAnalysisSkillTest {
  constructor() {
    this.skill = new BusinessModelAnalysisSkill();
  }

  // 测试技能初始化
  testSkillInitialization() {
    console.log("运行测试: testSkillInitialization");
    assert.ok(this.skill, "技能实例应存在");
    assert.equal(this.skill.skillId, "business-model-analysis", "技能ID应匹配");
    assert.equal(this.skill.version, "1.0.0", "版本应匹配");
    console.log("✓ testSkillInitialization 通过");
  }

  // 测试输入验证
  testInputValidation() {
    console.log("运行测试: testInputValidation");
    
    // 测试缺少targetCompany
    try {
      this.skill.validateInputs({});
      assert.fail("应抛出异常，因为缺少targetCompany");
    } catch (error) {
      assert.ok(error.message.includes("targetCompany"), "应验证targetCompany参数");
    }
    
    // 测试缺少analysisType
    try {
      this.skill.validateInputs({ targetCompany: "比亚迪" });
      assert.fail("应抛出异常，因为缺少analysisType");
    } catch (error) {
      assert.ok(error.message.includes("analysisType"), "应验证analysisType参数");
    }
    
    // 测试无效的analysisType
    try {
      this.skill.validateInputs({ 
        targetCompany: "比亚迪",
        analysisType: "invalid-type"
      });
      assert.fail("应抛出异常，因为analysisType无效");
    } catch (error) {
      assert.ok(error.message.includes("无效的分析类型"), "应验证analysisType有效性");
    }
    
    // 测试有效输入
    const validInputs = {
      targetCompany: "比亚迪",
      analysisType: "comprehensive"
    };
    this.skill.validateInputs(validInputs); // 不应抛出异常
    
    console.log("✓ testInputValidation 通过");
  }

  // 测试执行方法
  async testExecuteMethod() {
    console.log("运行测试: testExecuteMethod");
    
    const inputs = {
      targetCompany: "比亚迪",
      analysisType: "business-model-canvas",
      industryContext: "新能源汽车"
    };
    
    const result = await this.skill.execute(inputs);
    
    assert.ok(result.success, "执行应成功");
    assert.ok(result.data, "应返回数据");
    assert.ok(result.data.businessModelCanvas, "应包含商业模式画布分析");
    
    console.log("✓ testExecuteMethod 通过");
  }

  // 测试不同分析类型
  async testDifferentAnalysisTypes() {
    console.log("运行测试: testDifferentAnalysisTypes");
    
    const analysisTypes = [
      'business-model-canvas',
      'competitive-analysis',
      'value-proposition',
      'revenue-streams',
      'comprehensive'
    ];
    
    for (const analysisType of analysisTypes) {
      const inputs = {
        targetCompany: "腾讯",
        analysisType: analysisType,
        industryContext: "互联网"
      };
      
      const result = await this.skill.execute(inputs);
      
      assert.ok(result.success, `执行${analysisType}分析应成功`);
      console.log(`✓ ${analysisType} 分析成功`);
    }
    
    console.log("✓ testDifferentAnalysisTypes 通过");
  }

  // 测试数据搜集模块
  async testDataCollection() {
    console.log("运行测试: testDataCollection");
    
    // 通过技能实例访问数据搜集功能
    const inputs = {
      targetCompany: "阿里巴巴",
      analysisType: "business-model-canvas",
      industryContext: "电商"
    };
    
    const result = await this.skill.execute(inputs);
    
    assert.ok(result.success, "执行应成功");
    assert.ok(result.data, "应返回数据");
    
    const companyData = result.data; // 从完整结果中获取公司数据
    
    console.log("✓ testDataCollection 通过");
  }

  // 测试商业模式画布分析
  async testBusinessModelCanvasAnalysis() {
    console.log("运行测试: testBusinessModelCanvasAnalysis");
    
    const inputs = {
      targetCompany: "宁德时代",
      analysisType: "business-model-canvas",
      industryContext: "电池"
    };
    
    const result = await this.skill.execute(inputs);
    
    assert.ok(result.success, "执行应成功");
    assert.ok(result.data.businessModelCanvas, "应返回商业模式画布");
    assert.ok(result.data.businessModelCanvas.valuePropositions, "应包含价值主张");
    assert.ok(result.data.businessModelCanvas.revenueStreams, "应包含收入流");
    assert.ok(result.data.businessModelCanvas.keyPartners, "应包含关键合作伙伴");
    
    console.log("✓ testBusinessModelCanvasAnalysis 通过");
  }

  // 测试竞争分析
  async testCompetitiveAnalysis() {
    console.log("运行测试: testCompetitiveAnalysis");
    
    const inputs = {
      targetCompany: "宁德时代",
      analysisType: "competitive-analysis",
      industryContext: "电池"
    };
    
    const result = await this.skill.execute(inputs);
    
    assert.ok(result.success, "执行应成功");
    assert.ok(result.data.competitiveAnalysis, "应返回竞争分析");
    assert.ok(Array.isArray(result.data.competitiveAnalysis.directCompetitors), "应包含直接竞争对手");
    assert.ok(result.data.competitiveAnalysis.competitivePosition, "应包含竞争定位");
    
    console.log("✓ testCompetitiveAnalysis 通过");
  }

  // 运行所有测试
  async runAllTests() {
    console.log("开始运行商业模式分析技能测试套件...\n");
    
    try {
      this.testSkillInitialization();
      this.testInputValidation();
      await this.testExecuteMethod();
      await this.testDifferentAnalysisTypes();
      await this.testDataCollection();
      await this.testBusinessModelCanvasAnalysis();
      await this.testCompetitiveAnalysis();
      
      console.log("\n✓ 所有测试通过！商业模式分析技能功能正常。");
    } catch (error) {
      console.log(`\n✗ 测试失败: ${error.message}`);
      console.log(error.stack);
      throw error;
    }
  }
}

// 运行测试
if (require.main === module) {
  const testSuite = new BusinessModelAnalysisSkillTest();
  testSuite.runAllTests().catch(error => {
    process.exit(1);
  });
}

module.exports = BusinessModelAnalysisSkillTest;