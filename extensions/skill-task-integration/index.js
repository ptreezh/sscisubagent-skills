/**
 * Qwen CLI Skill 任务集成扩展
 * 
 * 实现 skill 任务计划在 CLI 对话中的加载、显示和执行
 * 
 * 安装位置：~/.qwen/extensions/skill-task-integration/
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

module.exports = {
  name: 'skill-task-integration',
  version: '1.0.0',
  description: 'Skill 任务集成 - 在 CLI 对话中加载和执行 skill 任务计划',
  
  // 扩展初始化
  async init(context) {
    console.log('[SkillTaskIntegration] 任务集成扩展初始化...');
    
    this.context = context;
    this.skillsPath = path.join(context.homeDir, '.qwen', 'skills');
    this.activeTasks = new Map(); // 存储活动任务
    
    // 加载所有 skill 的任务
    this.skills = await this.loadSkills();
    
    console.log(`[SkillTaskIntegration] 已加载 ${this.skills.length} 个 skill 的任务`);
  },
  
  // 加载所有 skill 的任务
  async loadSkills() {
    const skills = [];
    
    if (!fs.existsSync(this.skillsPath)) {
      return skills;
    }
    
    const skillDirs = fs.readdirSync(this.skillsPath);
    
    for (const dir of skillDirs) {
      const skillPath = path.join(this.skillsPath, dir);
      
      if (fs.statSync(skillPath).isDirectory()) {
        const taskPlanPath = path.join(skillPath, 'task_plan.md');
        
        if (fs.existsSync(taskPlanPath)) {
          const taskPlan = fs.readFileSync(taskPlanPath, 'utf-8');
          const tasks = this.parseTaskPlan(taskPlan);
          
          skills.push({
            name: dir,
            path: skillPath,
            taskPlan: taskPlan,
            tasks: tasks
          });
        }
      }
    }
    
    return skills;
  },
  
  // 解析 task_plan.md
  parseTaskPlan(content) {
    const tasks = [];
    
    // 提取阶段
    const phaseRegex = /### Phase (\d+): (.+?)\n([\s\S]*?)(?=\n###|\Z)/g;
    let match;
    
    while ((match = phaseRegex.exec(content)) !== null) {
      const phaseNum = parseInt(match[1]);
      const phaseName = match[2].trim();
      const phaseContent = match[3];
      
      // 提取子任务
      const subtaskRegex = /- \[([ x])\] (.+)/g;
      const subtasks = [];
      let subtaskMatch;
      
      while ((subtaskMatch = subtaskRegex.exec(phaseContent)) !== null) {
        const completed = subtaskMatch[1] === 'x';
        const taskName = subtaskMatch[2].trim();
        
        subtasks.push({
          name: taskName,
          completed: completed
        });
      }
      
      // 提取状态
      const statusMatch = phaseContent.match(/\*\*状态\*\*: (.+)/);
      const status = statusMatch ? statusMatch[1].trim() : 'pending';
      
      tasks.push({
        phase: phaseNum,
        name: phaseName,
        status: status,
        subtasks: subtasks,
        completed: subtasks.every(t => t.completed)
      });
    }
    
    return tasks;
  },
  
  // CLI 命令：显示任务清单
  async onCommand(context, command, args) {
    if (command === 'task' || command === '任务') {
      const subcommand = args[0];
      
      if (subcommand === 'list' || subcommand === '列表' || !subcommand) {
        return this.showTaskList(context);
      } else if (subcommand === 'show' || subcommand === '显示') {
        const skillName = args[1];
        return this.showSkillTasks(context, skillName);
      } else if (subcommand === 'start' || subcommand === '开始') {
        const skillName = args[1];
        const phaseNum = parseInt(args[2]);
        return this.startTask(context, skillName, phaseNum);
      } else if (subcommand === 'complete' || subcommand === '完成') {
        const skillName = args[1];
        const phaseNum = parseInt(args[2]);
        return this.completeTask(context, skillName, phaseNum);
      } else if (subcommand === 'progress' || subcommand === '进度') {
        return this.showProgress(context);
      }
    }
    
    return null;
  },
  
  // 显示任务清单
  async showTaskList(context) {
    let output = '# 📋 任务清单\n\n';
    
    for (const skill of this.skills) {
      const completedCount = skill.tasks.filter(t => t.completed).length;
      const totalCount = skill.tasks.length;
      const progress = totalCount > 0 ? Math.round(completedCount / totalCount * 100) : 0;
      
      output += `## ${skill.name}\n\n`;
      output += `**进度**: ${completedCount}/${totalCount} (${progress}%)\n\n`;
      
      for (const task of skill.tasks) {
        const icon = task.completed ? '✅' : '⏳';
        output += `${icon} **Phase ${task.phase}**: ${task.name}\n`;
        
        for (const subtask of task.subtasks) {
          const subIcon = subtask.completed ? '✅' : '⬜';
          output += `  ${subIcon} ${subtask.name}\n`;
        }
        output += '\n';
      }
    }
    
    return output;
  },
  
  // 显示特定 skill 的任务
  async showSkillTasks(context, skillName) {
    const skill = this.skills.find(s => s.name === skillName);
    
    if (!skill) {
      return `❌ 未找到 skill: ${skillName}`;
    }
    
    let output = `# 📋 ${skill.name} 任务清单\n\n`;
    
    const completedCount = skill.tasks.filter(t => t.completed).length;
    const totalCount = skill.tasks.length;
    const progress = totalCount > 0 ? Math.round(completedCount / totalCount * 100) : 0;
    
    output += `**总进度**: ${completedCount}/${totalCount} (${progress}%)\n\n`;
    
    for (const task of skill.tasks) {
      const icon = task.completed ? '✅' : '⏳';
      output += `${icon} **Phase ${task.phase}**: ${task.name}\n`;
      output += `状态：${task.status}\n\n`;
      
      for (const subtask of task.subtasks) {
        const subIcon = subtask.completed ? '✅' : '⬜';
        output += `${subIcon} ${subtask.name}\n`;
      }
      output += '\n';
    }
    
    return output;
  },
  
  // 开始任务
  async startTask(context, skillName, phaseNum) {
    const skill = this.skills.find(s => s.name === skillName);
    
    if (!skill) {
      return `❌ 未找到 skill: ${skillName}`;
    }
    
    const task = skill.tasks.find(t => t.phase === phaseNum);
    
    if (!task) {
      return `❌ 未找到 Phase ${phaseNum}`;
    }
    
    // 更新状态
    task.status = 'in_progress';
    
    // 保存到活动任务
    this.activeTasks.set(skillName, task);
    
    return `✅ 已开始：**${skill.name}** - Phase ${phaseNum}: ${task.name}\n\n当前任务：${task.subtasks.find(s => !s.completed)?.name || '所有子任务已完成'}`;
  },
  
  // 完成任务
  async completeTask(context, skillName, phaseNum) {
    const skill = this.skills.find(s => s.name === skillName);
    
    if (!skill) {
      return `❌ 未找到 skill: ${skillName}`;
    }
    
    const task = skill.tasks.find(t => t.phase === phaseNum);
    
    if (!task) {
      return `❌ 未找到 Phase ${phaseNum}`;
    }
    
    // 标记所有子任务为完成
    task.subtasks.forEach(s => s.completed = true);
    task.completed = true;
    task.status = 'complete';
    
    // 更新 task_plan.md
    this.updateTaskPlan(skill, phaseNum);
    
    // 从活动任务移除
    this.activeTasks.delete(skillName);
    
    return `✅ 已完成：**${skill.name}** - Phase ${phaseNum}: ${task.name}`;
  },
  
  // 显示进度
  async showProgress(context) {
    let output = '# 📊 任务进度\n\n';
    
    const totalTasks = this.skills.reduce((sum, s) => sum + s.tasks.length, 0);
    const completedTasks = this.skills.reduce((sum, s) => sum + s.tasks.filter(t => t.completed).length, 0);
    const overallProgress = totalTasks > 0 ? Math.round(completedTasks / totalTasks * 100) : 0;
    
    output += `**总体进度**: ${completedTasks}/${totalTasks} (${overallProgress}%)\n\n`;
    
    // 活动任务
    if (this.activeTasks.size > 0) {
      output += '## 🔄 进行中的任务\n\n';
      
      for (const [skillName, task] of this.activeTasks) {
        output += `- **${skillName}**: Phase ${task.phase}: ${task.name}\n`;
      }
      output += '\n';
    }
    
    return output;
  },
  
  // 更新 task_plan.md
  async updateTaskPlan(skill, phaseNum) {
    const taskPlanPath = path.join(skill.path, 'task_plan.md');
    
    // 重新生成 task_plan.md
    let content = `# 任务计划\n\n`;
    content += `**最后更新**: ${new Date().toISOString()}\n\n`;
    
    for (const task of skill.tasks) {
      content += `### Phase ${task.phase}: ${task.name}\n`;
      
      for (const subtask of task.subtasks) {
        const checkbox = subtask.completed ? '[x]' : '[ ]';
        content += `- ${checkbox} ${subtask.name}\n`;
      }
      
      content += `**状态**: ${task.status}\n\n`;
    }
    
    fs.writeFileSync(taskPlanPath, content, 'utf-8');
  },
  
  // 会话启动时加载任务
  async onSessionStart(context) {
    // 重新加载技能任务
    this.skills = await this.loadSkills();
    
    // 显示活动任务
    if (this.activeTasks.size > 0) {
      let output = '## 🔄 继续之前的任务\n\n';
      
      for (const [skillName, task] of this.activeTasks) {
        const currentSubtask = task.subtasks.find(s => !s.completed);
        if (currentSubtask) {
          output += `- **${skillName}**: ${task.name}\n`;
          output += `  当前子任务：${currentSubtask.name}\n`;
        }
      }
      
      context.systemPrompt += '\n\n' + output;
    }
  },
  
  // 用户输入前注入任务状态
  async onPrePrompt(context) {
    // 如果有活动任务，注入到上下文
    if (this.activeTasks.size > 0) {
      const taskInfo = [];
      
      for (const [skillName, task] of this.activeTasks) {
        const currentSubtask = task.subtasks.find(s => !s.completed);
        if (currentSubtask) {
          taskInfo.push(`${skillName}: ${currentSubtask.name}`);
        }
      }
      
      context.systemPrompt += `\n\n当前活动任务：${taskInfo.join(', ')}`;
    }
  },
  
  // 任务完成后触发
  async onTaskComplete(context, result) {
    // 如果有活动任务，标记完成
    if (this.activeTasks.size > 0) {
      console.log('[SkillTaskIntegration] 任务完成，更新状态...');
      // 可以自动或手动标记完成
    }
  }
};
