#!/usr/bin/env node

/**
 * SSCI Subagent Skills - Validation Script
 *
 * 验证技能和智能体的格式和完整性
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 验证SSCI Subagent Skills...\n');

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

// 验证SKILL.md文件
function validateSkillFile(skillPath) {
  const skillFile = path.join(skillPath, 'SKILL.md');

  if (!fs.existsSync(skillFile)) {
    log(`❌ 缺少SKILL.md: ${skillPath}`, 'red');
    return false;
  }

  let content = fs.readFileSync(skillFile, 'utf8');

  // 去除BOM字符（如果存在）
  if (content.charCodeAt(0) === 0xFEFF) {
    content = content.slice(1);
  }

  // 检查YAML frontmatter
  if (!content.startsWith('---')) {
    log(`❌ SKILL.md缺少YAML frontmatter: ${skillPath}`, 'red');
    return false;
  }

  // 提取YAML frontmatter
  const frontmatterEnd = content.indexOf('---', 3);
  if (frontmatterEnd === -1) {
    log(`❌ SKILL.md的YAML frontmatter格式错误: ${skillPath}`, 'red');
    return false;
  }

  const frontmatter = content.substring(3, frontmatterEnd);

  // 检查必需字段
  const requiredFields = ['name', 'description', 'version'];
  for (const field of requiredFields) {
    if (!frontmatter.includes(`${field}:`)) {
      log(`❌ SKILL.md缺少必需字段 ${field}: ${skillPath}`, 'red');
      return false;
    }
  }

  return true;
}

// 验证智能体文件
function validateAgentFile(agentPath) {
  if (!fs.existsSync(agentPath)) {
    log(`❌ 智能体文件不存在: ${agentPath}`, 'red');
    return false;
  }

  let content = fs.readFileSync(agentPath, 'utf8');

  // 去除BOM字符（如果存在）
  if (content.charCodeAt(0) === 0xFEFF) {
    content = content.slice(1);
  }

  // 检查YAML frontmatter
  if (!content.startsWith('---')) {
    log(`❌ 智能体文件缺少YAML frontmatter: ${agentPath}`, 'red');
    return false;
  }

  return true;
}

// 验证技能目录
function validateSkills() {
  log('📦 验证技能...', 'blue');

  const skillsDir = path.join(process.cwd(), 'skills');
  if (!fs.existsSync(skillsDir)) {
    log('❌ skills目录不存在', 'red');
    return;
  }

  const skillDirs = fs.readdirSync(skillsDir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  let validCount = 0;
  let invalidCount = 0;

  for (const skillName of skillDirs) {
    const skillPath = path.join(skillsDir, skillName);

    // 跳过隐藏目录和特殊目录
    if (skillName.startsWith('.') || skillName === '__pycache__') {
      continue;
    }

    if (validateSkillFile(skillPath)) {
      validCount++;
      log(`  ✅ ${skillName}`, 'green');
    } else {
      invalidCount++;
    }
  }

  log(`\n技能验证完成: ${validCount} 有效, ${invalidCount} 无效\n`, 'bright');
}

// 验证智能体
function validateAgents() {
  log('🤖 验证智能体...', 'blue');

  const agentsDir = path.join(process.cwd(), 'agents');
  if (!fs.existsSync(agentsDir)) {
    log('❌ agents目录不存在', 'red');
    return;
  }

  const agentFiles = fs.readdirSync(agentsDir)
    .filter(file => file.endsWith('.md'));

  let validCount = 0;
  let invalidCount = 0;

  for (const agentFile of agentFiles) {
    const agentPath = path.join(agentsDir, agentFile);

    // 跳过特殊文件
    if (agentFile.startsWith('.') || agentFile === 'README.md') {
      continue;
    }

    if (validateAgentFile(agentPath)) {
      validCount++;
      log(`  ✅ ${agentFile}`, 'green');
    } else {
      invalidCount++;
    }
  }

  log(`\n智能体验证完成: ${validCount} 有效, ${invalidCount} 无效\n`, 'bright');
}

// 验证package.json
function validatePackageJson() {
  log('📄 验证package.json...', 'blue');

  const packagePath = path.join(process.cwd(), 'package.json');
  if (!fs.existsSync(packagePath)) {
    log('❌ package.json不存在', 'red');
    return;
  }

  const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));

  // 检查必需字段
  const requiredFields = ['name', 'version', 'description', 'stigmergy'];
  for (const field of requiredFields) {
    if (!packageJson[field]) {
      log(`❌ package.json缺少必需字段: ${field}`, 'red');
      return;
    }
  }

  // 检查stigmergy配置
  if (!packageJson.stigmergy.skills || packageJson.stigmergy.skills.length === 0) {
    log('⚠️  stigmergy.skills为空', 'yellow');
  }

  if (!packageJson.stigmergy.agents || packageJson.stigmergy.agents.length === 0) {
    log('⚠️  stigmergy.agents为空', 'yellow');
  }

  log('✅ package.json格式正确\n', 'green');
}

// 主函数
function main() {
  try {
    // 验证package.json
    validatePackageJson();

    // 验证技能
    validateSkills();

    // 验证智能体
    validateAgents();

    log('✅ 验证完成！', 'green');

  } catch (error) {
    log(`\n❌ 验证失败: ${error.message}`, 'red');
    process.exit(1);
  }
}

// 执行主函数
main();