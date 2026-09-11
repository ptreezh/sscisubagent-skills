/**
 * Qwen CLI Skill 进化引擎扩展
 * 
 * 在 Qwen CLI 内部运行，自动触发 skill 的进化机制
 * 
 * 安装位置：~/.qwen/extensions/skill-evolution/
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

module.exports = {
  name: 'skill-evolution',
  version: '1.0.0',
  description: 'Skill 自主进化引擎 - 在 CLI 内部自动触发 skill 的教训记录和案例积累',
  
  // 扩展初始化
  async init(context) {
    console.log('[SkillEvolution] 进化引擎初始化...');
    
    this.context = context;
    this.skillsPath = path.join(context.homeDir, '.qwen', 'skills');
    this.sessionCount = 0;
    
    // 加载所有 skill
    this.skills = await this.loadSkills();
    
    console.log(`[SkillEvolution] 已加载 ${this.skills.length} 个 skill`);
  },
  
  // 加载所有 skill
  async loadSkills() {
    const skills = [];
    
    if (!fs.existsSync(this.skillsPath)) {
      console.log('[SkillEvolution] Skills 目录不存在');
      return skills;
    }
    
    const skillDirs = fs.readdirSync(this.skillsPath);
    
    for (const dir of skillDirs) {
      const skillPath = path.join(this.skillsPath, dir);
      
      if (fs.statSync(skillPath).isDirectory()) {
        // 检查是否有 skill-hooks.yaml
        const hooksPath = path.join(skillPath, 'skill-hooks.yaml');
        
        if (fs.existsSync(hooksPath)) {
          const hooksConfig = yaml.load(fs.readFileSync(hooksPath, 'utf-8'));
          
          skills.push({
            name: dir,
            path: skillPath,
            config: hooksConfig,
            soulPath: path.join(skillPath, 'soul.md'),
            lessonPath: path.join(skillPath, 'lesson-memory.md'),
            casePath: path.join(skillPath, 'case-library')
          });
        }
      }
    }
    
    return skills;
  },
  
  // 会话启动时触发
  async onSessionStart(context) {
    console.log('[SkillEvolution] 会话启动...');
    
    this.sessionCount++;
    
    // 加载每个 skill 的状态
    for (const skill of this.skills) {
      await this.loadSkillState(skill);
    }
    
    // 检查是否需要定期进化
    if (this.sessionCount % 10 === 0) {
      await this.triggerPeriodicEvolution();
    }
  },
  
  // 加载 skill 状态
  async loadSkillState(skill) {
    // 读取 soul.md
    if (fs.existsSync(skill.soulPath)) {
      const soul = fs.readFileSync(skill.soulPath, 'utf-8');
      skill.soul = soul;
    }
    
    // 读取 lesson-memory.md
    if (fs.existsSync(skill.lessonPath)) {
      const lessons = fs.readFileSync(skill.lessonPath, 'utf-8');
      skill.lessons = lessons;
    }
    
    // 读取案例库
    if (fs.existsSync(skill.casePath)) {
      const cases = this.loadCases(skill.casePath);
      skill.cases = cases;
    }
  },
  
  // 加载案例
  loadCases(casePath) {
    const cases = [];
    const successfulCasesPath = path.join(casePath, 'successful-cases');
    
    if (fs.existsSync(successfulCasesPath)) {
      const caseFiles = fs.readdirSync(successfulCasesPath);
      
      for (const file of caseFiles) {
        if (file.endsWith('.md')) {
          const caseContent = fs.readFileSync(path.join(successfulCasesPath, file), 'utf-8');
          cases.push({
            file: file,
            content: caseContent
          });
        }
      }
    }
    
    return cases;
  },
  
  // 用户输入前触发（注入 skill 状态）
  async onPrePrompt(context) {
    const currentSkill = this.getCurrentSkill(context);
    
    if (currentSkill) {
      // 注入 skill 状态到系统提示词
      const injection = this.createSkillStateInjection(currentSkill);
      context.systemPrompt += injection;
      
      console.log(`[SkillEvolution] 已注入 ${currentSkill.name} 状态`);
    }
  },
  
  // 创建 skill 状态注入
  createSkillStateInjection(skill) {
    let injection = `\n\n# Skill Identity\n\n`;
    
    // 添加 soul.md 的关键信息
    if (skill.soul) {
      injection += `根据 ${skill.name} 的定义：\n`;
      injection += `- 角色：${this.extractValue(skill.soul, 'role') || '专家'}\n`;
      injection += `- 价值观：${this.extractValue(skill.soul, 'values') || '严谨、系统、深入'}\n`;
      injection += `- 工作方式：${this.extractValue(skill.soul, 'working_style') || '多阶段分析'}\n\n`;
    }
    
    // 添加历史教训
    if (skill.lessons) {
      injection += `## 历史教训\n\n`;
      const recentLessons = skill.lessons.split('\n').slice(0, 10).join('\n');
      injection += recentLessons + '\n\n';
    }
    
    // 添加成功案例
    if (skill.cases && skill.cases.length > 0) {
      injection += `## 成功案例\n\n`;
      for (const case_ of skill.cases.slice(0, 3)) {
        const title = this.extractValue(case_.content, '案例', true);
        injection += `- ${title}\n`;
      }
      injection += '\n';
    }
    
    return injection;
  },
  
  // 从 YAML/Markdown 中提取值
  extractValue(content, key, isMarkdown = false) {
    if (!content) return null;
    
    if (isMarkdown) {
      const regex = new RegExp(`#.*?${key}.*?:\\s*(.+)`, 'i');
      const match = content.match(regex);
      return match ? match[1].trim() : null;
    } else {
      const regex = new RegExp(`${key}:\\s*(.+)`, 'i');
      const match = content.match(regex);
      return match ? match[1].trim() : null;
    }
  },
  
  // 任务完成后触发
  async onTaskComplete(context, result) {
    console.log('[SkillEvolution] 任务完成，记录教训...');
    
    const currentSkill = this.getCurrentSkill(context);
    
    if (currentSkill) {
      // 记录教训
      await this.recordLesson(currentSkill, result);
      
      // 如果成功，添加到案例库
      if (result.success === true) {
        await this.addCase(currentSkill, result);
      }
    }
  },
  
  // 记录教训
  async recordLesson(skill, result) {
    const timestamp = new Date().toISOString();
    const lessonPath = skill.lessonPath;
    
    // 提取教训
    const lesson = this.extractLesson(result);
    
    // 追加到 lesson-memory.md
    const lessonEntry = `
### 教训 ${this.getLessonCount(skill) + 1}: ${lesson.title}

**发生时间**: ${timestamp}  
**严重性**: ${lesson.severity}

#### 情境描述
${lesson.context}

#### 错误表现
${lesson.error}

#### 根本原因
${lesson.rootCause}

#### 改进策略
${lesson.improvement}

---
`;
    
    if (fs.existsSync(lessonPath)) {
      fs.appendFileSync(lessonPath, lessonEntry, 'utf-8');
    } else {
      fs.writeFileSync(lessonPath, `# 教训记忆日志\n\n**技能**: ${skill.name}\n**创建时间**: ${timestamp}\n\n---\n\n${lessonEntry}`, 'utf-8');
    }
    
    console.log(`[SkillEvolution] 已记录教训到 ${skill.name}`);
  },
  
  // 提取教训
  extractLesson(result) {
    return {
      title: result.taskType || '任务教训',
      severity: result.success ? '⚠️ 中等' : '🔴 严重',
      context: result.context || '任务执行过程中',
      error: result.error || '无明显错误',
      rootCause: result.rootCause || '待分析',
      improvement: result.improvement || '待提炼'
    };
  },
  
  // 获取教训数量
  getLessonCount(skill) {
    if (!fs.existsSync(skill.lessonPath)) return 0;
    
    const content = fs.readFileSync(skill.lessonPath, 'utf-8');
    const matches = content.match(/### 教训 \d+/g);
    return matches ? matches.length : 0;
  },
  
  // 添加案例
  async addCase(skill, result) {
    const casePath = path.join(skill.casePath, 'successful-cases');
    
    if (!fs.existsSync(casePath)) {
      fs.mkdirSync(casePath, { recursive: true });
    }
    
    const timestamp = new Date().toISOString().split('T')[0];
    const caseId = this.getCaseCount(skill) + 1;
    const caseFile = path.join(casePath, `case-${String(caseId).padStart(3, '0')}-${timestamp}.md`);
    
    // 创建案例内容
    const caseContent = this.createCaseContent(result, caseId, timestamp);
    
    fs.writeFileSync(caseFile, caseContent, 'utf-8');
    
    console.log(`[SkillEvolution] 已添加案例到 ${skill.name}`);
  },
  
  // 获取案例数量
  getCaseCount(skill) {
    const casePath = path.join(skill.casePath, 'successful-cases');
    
    if (!fs.existsSync(casePath)) return 0;
    
    return fs.readdirSync(casePath).filter(f => f.endsWith('.md')).length;
  },
  
  // 创建案例内容
  createCaseContent(result, caseId, timestamp) {
    return `# 成功案例 ${String(caseId).padStart(3, '0')}: ${result.taskType || '未知任务'}

**分析日期**: ${timestamp}  
**使用方法**: 自动记录  
**质量评分**: ${result.score || 100}/100

---

## 案例背景

### 研究问题
${result.context || '待补充'}

### 数据类型
${result.dataType || '待补充'}

### 分析方法
${result.method || '待补充'}

---

## 关键成功因素

1. **因素 1**: 待补充
2. **因素 2**: 待补充
3. **因素 3**: 待补充

---

## 质量验证

- [x] 方法正确性验证
- [x] 结果可靠性验证
- [x] 可重复性验证

**验证评分**: ${result.score || 100}/100

---

**案例作者**: 自动生成  
**审核状态**: ⏳ 待审核  
**最后更新**: ${timestamp}
`;
  },
  
  // 获取当前 skill
  getCurrentSkill(context) {
    // 从上下文获取当前使用的 skill
    const skillName = context.skillName || context.currentSkill;
    
    if (skillName) {
      return this.skills.find(s => s.name === skillName);
    }
    
    // 默认返回第一个 skill
    return this.skills[0] || null;
  },
  
  // 触发定期进化
  async triggerPeriodicEvolution() {
    console.log('[SkillEvolution] 触发定期进化...');
    
    for (const skill of this.skills) {
      // 复习教训
      await this.reviewLessons(skill);
      
      // 提炼模式
      await this.extractPatterns(skill);
      
      // 更新 soul.md
      await this.updateSoul(skill);
    }
    
    console.log('[SkillEvolution] 定期进化完成');
  },
  
  // 复习教训
  async reviewLessons(skill) {
    console.log(`[SkillEvolution] 复习 ${skill.name} 的教训...`);
    // 实现教训复习逻辑
  },
  
  // 提炼模式
  async extractPatterns(skill) {
    console.log(`[SkillEvolution] 从 ${skill.name} 提炼模式...`);
    // 实现模式提炼逻辑
  },
  
  // 更新 soul.md
  async updateSoul(skill) {
    console.log(`[SkillEvolution] 更新 ${skill.name} 的 soul.md...`);
    // 实现 soul.md 更新逻辑
  }
};
