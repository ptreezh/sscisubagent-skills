/**
 * 工具函数
 */

const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');

/**
 * 获取用户主目录
 */
function getHomeDir() {
  return process.env.HOME || process.env.USERPROFILE || os.homedir();
}

/**
 * 检测已安装的AI CLI工具
 */
async function detectCLIs() {
  const clis = {
    claude: { installed: false, version: null },
    qwen: { installed: false, version: null },
    iflow: { installed: false, version: null }
  };

  // 检测Claude CLI
  try {
    const claudeVersion = execSync('claude --version', {
      encoding: 'utf8',
      stdio: 'pipe'
    }).trim();
    clis.claude.installed = true;
    clis.claude.version = claudeVersion;
  } catch (error) {
    clis.claude.installed = false;
  }

  // 检测Qwen CLI
  try {
    const qwenVersion = execSync('qwen --version', {
      encoding: 'utf8',
      stdio: 'pipe'
    }).trim();
    clis.qwen.installed = true;
    clis.qwen.version = qwenVersion;
  } catch (error) {
    clis.qwen.installed = false;
  }

  // 检测iFlow CLI
  try {
    const iflowVersion = execSync('iflow --version', {
      encoding: 'utf8',
      stdio: 'pipe'
    }).trim();
    clis.iflow.installed = true;
    clis.iflow.version = iflowVersion;
  } catch (error) {
    clis.iflow.installed = false;
  }

  return clis;
}

/**
 * 验证部署状态
 */
async function validateDeployment(verbose = false) {
  const clis = await detectCLIs();
  const homeDir = getHomeDir();
  const results = {};

  // 加载配置
  const packagePath = path.resolve(__dirname, '..');
  const packageJson = require(path.join(packagePath, 'package.json'));
  const ssciConfig = packageJson.ssci;

  for (const [cliName, cliInfo] of Object.entries(clis)) {
    if (!cliInfo.installed) {
      results[cliName] = {
        valid: false,
        message: 'CLI工具未安装',
        details: []
      };
      continue;
    }

    const targetConfig = ssciConfig.cli_targets[cliName];
    if (!targetConfig) {
      results[cliName] = {
        valid: false,
        message: '不支持的CLI工具',
        details: []
      };
      continue;
    }

    const targetDir = path.join(homeDir, targetConfig.config_dir);
    const details = [];
    let valid = true;

    // 检查目录是否存在
    if (await fs.pathExists(targetDir)) {
      details.push(`配置目录存在: ${targetDir}`);

      // 检查智能体
      const agents = ssciConfig.agents;
      let agentCount = 0;
      for (const [agentName] of Object.entries(agents)) {
        const agentPath = path.join(targetDir, `${agentName}.md`);
        if (await fs.pathExists(agentPath)) {
          agentCount++;
          if (verbose) {
            details.push(`✓ 智能体: ${agentName}`);
          }
        } else if (verbose) {
          details.push(`✗ 缺失智能体: ${agentName}`);
        }
      }

      // 检查技能
      const skills = ssciConfig.skills;
      let skillCount = 0;
      for (const [category, skillList] of Object.entries(skills)) {
        const categoryDir = path.join(targetDir, category);
        if (await fs.pathExists(categoryDir)) {
          for (const skillPath of skillList) {
            const skillName = path.basename(skillPath);
            const skillFilePath = path.join(categoryDir, skillName);
            if (await fs.pathExists(skillFilePath)) {
              skillCount++;
              if (verbose) {
                details.push(`✓ 技能: ${category}/${skillName}`);
              }
            } else if (verbose) {
              details.push(`✗ 缺失技能: ${category}/${skillName}`);
            }
          }
        }
      }

      const totalExpectedAgents = Object.keys(agents).length;
      const totalExpectedSkills = Object.values(skills).flat().length;

      if (agentCount === totalExpectedAgents && skillCount === totalExpectedSkills) {
        results[cliName] = {
          valid: true,
          message: `完整部署 (${agentCount}个智能体, ${skillCount}个技能)`,
          details
        };
      } else {
        valid = false;
        results[cliName] = {
          valid: false,
          message: `部署不完整 (${agentCount}/${totalExpectedAgents}个智能体, ${skillCount}/${totalExpectedSkills}个技能)`,
          details
        };
      }

    } else {
      valid = false;
      results[cliName] = {
        valid: false,
        message: '技能包未部署',
        details: [`配置目录不存在: ${targetDir}`]
      };
    }
  }

  return results;
}

/**
 * 创建符号链接（如果需要）
 */
async function createSymlink(target, linkPath) {
  try {
    await fs.ensureDir(path.dirname(linkPath));

    // 如果链接已存在，先删除
    if (await fs.pathExists(linkPath)) {
      await fs.remove(linkPath);
    }

    await fs.symlink(target, linkPath);
    return true;
  } catch (error) {
    // 如果创建符号链接失败，尝试复制
    try {
      await fs.copy(target, linkPath);
      return false; // 使用复制而非链接
    } catch (copyError) {
      throw new Error(`无法创建链接或复制文件: ${copyError.message}`);
    }
  }
}

/**
 * 检查文件权限
 */
function checkFilePermissions(filePath) {
  try {
    fs.accessSync(filePath, fs.constants.R_OK | fs.constants.W_OK);
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * 获取文件大小（人类可读格式）
 */
function getHumanFileSize(filePath) {
  try {
    const stats = fs.statSync(filePath);
    const bytes = stats.size;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  } catch (error) {
    return 'Unknown';
  }
}

/**
 * 备份现有文件
 */
async function backupFile(filePath) {
  if (await fs.pathExists(filePath)) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = `${filePath}.backup.${timestamp}`;
    await fs.copy(filePath, backupPath);
    return backupPath;
  }
  return null;
}

module.exports = {
  getHomeDir,
  detectCLIs,
  validateDeployment,
  createSymlink,
  checkFilePermissions,
  getHumanFileSize,
  backupFile
};