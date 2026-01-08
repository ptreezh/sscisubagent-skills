#!/usr/bin/env node

/**
 * SSCI Subagent Skills - Post-install Script
 *
 * 该脚本在npm install后自动执行，用于：
 * 1. 检测stigmergy是否已安装
 * 2. 自动同步技能到stigmergy
 * 3. 部署到所有可用的CLI工具
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🚀 SSCI Subagent Skills - 安装后配置\n');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 检查stigmergy是否已安装
function checkStigmergy() {
  try {
    execSync('stigmergy --version', { stdio: 'pipe' });
    log('✅ Stigmergy已安装', 'green');
    return true;
  } catch (error) {
    log('⚠️  Stigmergy未安装', 'yellow');
    log('💡 请先安装Stigmergy: npm install -g stigmergy-cli', 'blue');
    return false;
  }
}

// 同步技能到stigmergy
function syncSkills() {
  try {
    log('\n📦 正在同步技能到Stigmergy...', 'blue');

    // 读取package.json中的stigmergy配置
    const packagePath = path.join(process.cwd(), 'package.json');
    const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    const stigmergyConfig = packageJson.stigmergy;

    if (!stigmergyConfig || !stigmergyConfig.skills || stigmergyConfig.skills.length === 0) {
      log('⚠️  未找到技能配置', 'yellow');
      return;
    }

    log(`找到 ${stigmergyConfig.skills.length} 个技能`, 'bright');

    // 执行stigmergy skill sync
    try {
      execSync('stigmergy skill sync', { stdio: 'inherit' });
      log('✅ 技能同步成功', 'green');
    } catch (error) {
      log('⚠️  技能同步失败，请手动执行: stigmergy skill sync', 'yellow');
    }

  } catch (error) {
    log(`❌ 同步失败: ${error.message}`, 'red');
  }
}

// 部署到CLI工具
function deployToCLIs() {
  try {
    log('\n🔧 正在部署到CLI工具...', 'blue');

    // 执行stigmergy deploy
    try {
      execSync('stigmergy deploy', { stdio: 'inherit' });
      log('✅ 部署成功', 'green');
    } catch (error) {
      log('⚠️  部署失败，请手动执行: stigmergy deploy', 'yellow');
    }

  } catch (error) {
    log(`❌ 部署失败: ${error.message}`, 'red');
  }
}

// 显示安装完成信息
function showCompletionMessage() {
  log('\n' + '='.repeat(50), 'bright');
  log('🎉 SSCI Subagent Skills 安装完成！', 'green');
  log('='.repeat(50), 'bright');
  log('\n📚 可用的技能:', 'blue');
  log('  • ant - 行动者网络理论分析', 'reset');
  log('  • field-analysis - 布迪厄场域分析', 'reset');
  log('  • grounded-theory-expert - 扎根理论专家', 'reset');
  log('  • network-computation - 社会网络计算', 'reset');
  log('  • mathematical-statistics - 数理统计分析', 'reset');
  log('  • validity-reliability - 信度效度分析', 'reset');
  log('  • conflict-resolution - 冲突解决', 'reset');
  log('\n🤖 可用的智能体:', 'blue');
  log('  • ant-expert - 行动者网络理论专家', 'reset');
  log('  • field-analysis-expert - 场域分析专家', 'reset');
  log('  • grounded-theory-expert - 扎根理论专家', 'reset');
  log('  • literature-expert - 文献管理专家', 'reset');
  log('  • sna-expert - 社会网络分析专家', 'reset');
  log('\n📖 使用方法:', 'blue');
  log('  在支持的CLI中直接使用自然语言触发技能', 'reset');
  log('  例如: "分析这个文本的场域结构"', 'reset');
  log('\n🔧 手动命令:', 'blue');
  log('  stigmergy skill sync     # 同步技能', 'reset');
  log('  stigmergy skill list     # 列出所有技能', 'reset');
  log('  stigmergy deploy         # 部署到CLI', 'reset');
  log('\n📚 更多信息: https://github.com/ptreezh/sscisubagent-skills', 'bright');
  log('='.repeat(50) + '\n', 'bright');
}

// 主函数
function main() {
  try {
    // 检查stigmergy
    const hasStigmergy = checkStigmergy();

    if (hasStigmergy) {
      // 同步技能
      syncSkills();

      // 部署到CLI
      deployToCLIs();
    }

    // 显示完成信息
    showCompletionMessage();

  } catch (error) {
    log(`\n❌ 安装后配置失败: ${error.message}`, 'red');
    process.exit(1);
  }
}

// 执行主函数
main();