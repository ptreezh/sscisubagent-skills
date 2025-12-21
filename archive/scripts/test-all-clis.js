#!/usr/bin/env node

/**
 * SSCI技能包 - 多CLI测试脚本
 * 测试所有CLI工具的技能调用功能
 */

const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');

class CLITester {
  constructor() {
    this.testResults = {};
    this.rootDir = path.resolve(__dirname, '..');
    this.testDataDir = path.join(this.rootDir, 'test_data');
    this.testResults = {
      claude: { passed: 0, failed: 0, details: [] },
      qwen: { passed: 0, failed: 0, details: [] },
      gemini: { passed: 0, failed: 0, details: [] },
      iflow: { passed: 0, failed: 0, details: [] },
      codebuddy: { passed: 0, failed: 0, details: [] },
      codex: { passed: 0, failed: 0, details: [] },
      qodercli: { passed: 0, failed: 0, details: [] }
    };
  }

  async runAllTests() {
    console.log('🧪 开始多CLI功能测试\n');
    console.log('='.repeat(50));

    const testCases = [
      { cli: 'claude', test: 'testSkillRecognition', description: '技能识别测试' },
      { cli: 'qwen', test: 'testSkillRecognition', description: '技能识别测试' },
      { cli: 'gemini', test: 'testSkillRecognition', description: '技能识别测试' },
      { cli: 'iflow', test: 'testSkillRecognition', description: '技能识别测试' },
      { cli: 'codebuddy', test: 'testSkillRecognition', description: '技能识别测试' },
      { cli: 'codex', test: 'testSkillRecognition', description: '技能识别测试' },
      { cli: 'qodercli', test: 'testSkillRecognition', description: '技能识别测试' },
      { cli: 'claude', test: 'testAgentCalling', description: '智能体调用测试' },
      { cli: 'qwen', test: 'testAgentCalling', description: '智能体调用测试' },
      { cli: 'gemini', test: 'testAgentCalling', description: '智能体调用测试' },
      { cli: 'iflow', test: 'testAgentCalling', description: '智能体调用测试' }
    ];

    for (const testCase of testCases) {
      await this.runSingleTest(testCase);
    }

    this.generateTestReport();
  }

  async runSingleTest(testCase) {
    const { cli, test, description } = testCase;
    const cliConfig = this.testResults[cli];
    
    console.log(`\n🧪 测试 ${cli} - ${description}`);
    
    try {
      switch (test) {
        case 'testSkillRecognition':
          await this.testSkillRecognition(cli);
          cliConfig.passed++;
          break;
        case 'testAgentCalling':
          await this.testAgentCalling(cli);
          cliConfig.passed++;
          break;
        default:
          console.log(`❌ 未知测试类型: ${test}`);
      }
    } catch (error) {
      cliConfig.failed++;
      cliConfig.details.push(`${description}: ${error.message}`);
    }
  }

  async testSkillRecognition(cli) {
    const prompts = [
      '请帮我进行开放编码分析',
      '请计算网络中心性指标',
      '请帮我解决研究冲突',
      '请进行文献检索'
    ];

    let passed = 0;
    let failed = 0;

    for (const prompt of prompts) {
      try {
        const command = `${cli} -p "${prompt}"`;
        const result = execSync(command, { 
          encoding: 'utf8', 
          timeout: 30000 
        });
        
        // 检查结果中是否包含技能关键词
        const hasSkillKeywords = 
          result.includes('技能') || 
          result.includes('skill') ||
          result.includes('编码') ||
          result.includes('网络') ||
          result.includes('文献');
        
        if (hasSkillKeywords) {
          passed++;
          console.log(`  ✅ "${prompt}" - 技能识别成功`);
        } else {
          failed++;
          console.log(`  ❌ "${prompt}" - 技能识别失败`);
        }
      } catch (error) {
        failed++;
        console.log(`  ❌ "${prompt}" - 测试失败: ${error.message}`);
      }
    }

    this.testResults[cli].passed += passed;
    this.testResults[cli].failed += failed;
  }

  async testAgentCalling(cli) {
    const agentPrompts = [
      '请使用文献管理专家查找最新研究',
      '请使用扎根理论专家分析数据',
      '请使用sna-expert分析网络结构'
    ];

    let passed = 0;
    let failed = 0;

    for (const prompt of agentPrompts) {
      try {
        const command = `${cli} -p "${prompt}"`;
        const result = execSync(command, { 
          encoding: 'utf8', 
          timeout: 30000 
        });
        
        // 检查结果中是否包含智能体关键词
        const hasAgentKeywords = 
          result.includes('专家') ||
          result.includes('智能体') ||
          result.includes('agent');
        
        if (hasAgentKeywords) {
          passed++;
          console.log(`  ✅ "${prompt}" - 智能体调用成功`);
        } else {
          failed++;
          console.log(`  ❌ "${prompt}" - 智能体调用失败`);
        }
      } catch (error) {
        failed++;
        console.log(`  ❌ "${prompt}" - 测试失败: ${error.message}`);
      }
    }

    this.testResults[cli].passed += passed;
    this.testResults[cli].failed += failed;
  }

  generateTestReport() {
    console.log('\n' + '='.repeat(60));
    console.log('🧪 多CLI测试报告');
    console.log('='.repeat(60));

    const timestamp = new Date().toLocaleString('zh-CN');
    console.log(`测试时间: ${timestamp}`);

    let totalPassed = 0;
    let totalFailed = 0;

    console.log('\n📊 测试结果汇总:');
    Object.entries(this.testResults).forEach(([cli, results]) => {
      const statusIcon = results.passed > 0 ? '✅' : '❌';
      console.log(`  ${statusIcon} ${cli}:`);
      console.log(`    通过: ${results.passed}/${results.passed + results.failed}`);
      
      if (results.details.length > 0) {
        console.log('    失败原因:');
        results.details.forEach((detail, index) => {
          console.log(`      ${index + 1}. ${detail}`);
        });
      }
      
      totalPassed += results.passed;
      totalFailed += results.failed;
    });

    console.log('\n📈 总计:');
    console.log(`  通过测试: ${totalPassed}`);
    console.log(`  失败测试: ${totalFailed}`);
    console.log(`  成功率: ${((totalPassed / (totalPassed + totalFailed) * 100).toFixed(1)}%`);

    if (totalFailed > 0) {
      console.log('\n🔧 故障排除建议:');
      console.log('1. 检查CLI工具是否正确安装');
      console.log('2. 验证技能是否正确部署');
      console.log('3. 检查网络连接状态');
      console.log('4. 使用Stigmergy统一管理');
    }
  }
}

// 主程序
if (require.main === module) {
  const tester = new CLITester();
  tester.runAllTests().catch(console.error);
}

module.exports = CLITester;