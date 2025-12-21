#!/usr/bin/env node
/**
 * iFlow CLI适配�?- 将Claude Code格式的Subagent转换为iFlow CLI兼容格式
 * 
 * 功能说明�? * 1. 读取Claude Code标准的subagent配置文件
 * 2. 转换为iFlow CLI兼容的格�? * 3. 处理工具权限映射
 * 4. 生成适配后的配置文件
 * 5. 支持iFlow CLI的市场集�? */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class iFlowCLIAdapter {
    constructor() {
        this.sourceDir = path.join(__dirname, '../agents');
        this.outputDir = path.join(__dirname, '../iflow-compatible');
        this.toolMapping = {
            'read_file': 'file.read',
            'write_file': 'file.write',
            'list_directory': 'dir.list',
            'search_file_content': 'content.search',
            'run_shell_command': 'shell.execute',
            'web_search': 'web.search',
            'web_fetch': 'web.fetch',
            'read_file': 'file.read',
            'replace': 'file.replace',
            'write_file': 'file.write',
            'glob': 'file.glob',
            'multi_edit': 'file.multiEdit',
            'todo_write': 'todo.write',
            'todo_read': 'todo.read',
            'task': 'agent.task',
            'exit_plan_mode': 'agent.exitPlanMode',
            'save_memory': 'memory.save',
            'web_search': 'web.search',
            'web_fetch': 'web.fetch',
            'run_shell_command': 'shell.execute'
        };
    }

    /**
     * 转换单个subagent配置
     * @param {string} agentName - subagent名称
     * @param {Object} claudeConfig - Claude Code格式配置
     * @returns {Object} iFlow CLI兼容配置
     */
    convertSubagent(agentName, claudeConfig) {
        const iflowConfig = {
            name: agentName,
            displayName: this.extractDisplayName(claudeConfig.description),
            description: this.cleanDescription(claudeConfig.description),
            systemPrompt: this.convertSystemPrompt(claudeConfig),
            capabilities: this.extractCapabilities(claudeConfig),
            tools: this.mapTools(claudeConfig.tools || []),
            model: this.selectOptimalModel(claudeConfig.model || 'claude-3-5-sonnet-20241022'),
            category: this.determineCategory(claudeConfig.description),
            version: '1.0.0',
            author: '中文社科研究Subagent项目�?,
            tags: this.generateTags(claudeConfig.description),
            // iFlow CLI特有字段
            marketReady: true,
            installationType: 'agent',
            compatibility: {
                iflowVersion: '>=1.0.0',
                platforms: ['cli', 'web', 'vscode']
            },
            metadata: {
                language: 'zh-CN',
                domain: 'social-sciences',
                lastUpdated: new Date().toISOString(),
                downloadCount: 0,
                rating: 0
            }
        };

        return iflowConfig;
    }

    /**
     * 提取显示名称
     */
    extractDisplayName(description) {
        const match = description.match(/^(.+?)�?);
        return match ? match[1] : '中文社科研究专家';
    }

    /**
     * 清理描述文本
     */
    cleanDescription(description) {
        return description
            .replace(/，当需�?*时使用此专家�?/, '')
            .replace(/，包�?*$/g, '')
            .trim();
    }

    /**
     * 转换系统提示
     */
    convertSystemPrompt(claudeConfig) {
        let systemPrompt = '';

        // 添加基础信息
        systemPrompt += `你是${claudeConfig.name}�?{this.extractDisplayName(claudeConfig.description)}。\n\n`;

        // 添加专业领域
        if (claudeConfig['专业领域']) {
            systemPrompt += `## 专业领域\n${claudeConfig['专业领域']}\n\n`;
        }

        // 添加工作方法
        if (claudeConfig['工作方法']) {
            systemPrompt += `## 工作方法\n${claudeConfig['工作方法']}\n\n`;
        }

        // 添加质量检查清�?        if (claudeConfig['质量检查清�?]) {
            systemPrompt += `## 质量标准\n${claudeConfig['质量检查清�?]}\n\n`;
        }

        // 添加输出标准
        if (claudeConfig['输出标准']) {
            systemPrompt += `## 输出要求\n${claudeConfig['输出标准']}\n\n`;
        }

        // 添加iFlow CLI特定说明
        systemPrompt += `## iFlow CLI集成说明\n`;
        systemPrompt += `你运行在iFlow CLI环境中，可以访问以下工具：\n`;
        systemPrompt += `- 文件读写和处理\n`;
        systemPrompt += `- 网络搜索和内容获取\n`;
        systemPrompt += `- 命令行执行和脚本运行\n`;
        systemPrompt += `- 代码分析和处理\n`;
        systemPrompt += `- 任务管理和协作\n`;
        systemPrompt += `- 记忆管理和信息存储\n\n`;
        systemPrompt += `## 使用指南\n`;
        systemPrompt += `1. 仔细理解用户的需求和上下文\n`;
        systemPrompt += `2. 运用你的专业能力提供高质量的分析和建议\n`;
        systemPrompt += `3. 充分利用可用的工具来完成具体任务\n`;
        systemPrompt += `4. 保持与用户的良好互动和沟通\n`;
        systemPrompt += `5. 根据中文社科研究的特点提供本土化支持\n\n`;
        systemPrompt += `请根据用户需求，运用你的专业能力提供高质量的中文社会科学研究支持。\n`;

        return systemPrompt;
    }

    /**
     * 提取能力列表
     */
    extractCapabilities(claudeConfig) {
        const capabilities = [];

        // 从描述中提取能力
        const description = claudeConfig.description;
        
        if (description.includes('文献检�?)) capabilities.push('文献检�?);
        if (description.includes('引用格式')) capabilities.push('引用格式�?);
        if (description.includes('质量评估')) capabilities.push('文献质量评估');
        if (description.includes('趋势分析')) capabilities.push('研究趋势分析');
        if (description.includes('编码')) capabilities.push('质性编�?);
        if (description.includes('网络分析')) capabilities.push('社会网络分析');
        if (description.includes('场域')) capabilities.push('场域分析');
        if (description.includes('本土�?)) capabilities.push('中文本土�?);
        if (description.includes('行动�?)) capabilities.push('行动者网络分�?);
        if (description.includes('转译')) capabilities.push('转译过程分析');

        return capabilities.length > 0 ? capabilities : ['中文社会科学研究支持'];
    }

    /**
     * 映射工具权限
     */
    mapTools(claudeTools) {
        return claudeTools.map(tool => this.toolMapping[tool] || tool);
    }

    /**
     * 选择最优模�?     */
    selectOptimalModel(claudeModel) {
        // 根据任务复杂度选择iFlow CLI支持的模�?        const modelMapping = {
            'claude-3-5-sonnet-20241022': 'qwen-max',
            'claude-3-opus-20240229': 'qwen-max',
            'claude-3-sonnet-20240229': 'qwen-plus',
            'claude-3-haiku-20240307': 'qwen-turbo'
        };

        return modelMapping[claudeModel] || 'qwen-plus';
    }

    /**
     * 确定分类
     */
    determineCategory(description) {
        if (description.includes('文献')) return '文献管理';
        if (description.includes('编码') || description.includes('分析')) return '数据分析';
        if (description.includes('写作')) return '学术写作';
        if (description.includes('方法')) return '研究方法';
        if (description.includes('场域')) return '场域理论';
        if (description.includes('行动�?) || description.includes('网络')) return '网络分析';
        return '综合研究';
    }

    /**
     * 生成标签
     */
    generateTags(description) {
        const tags = [];
        
        if (description.includes('中文')) tags.push('中文');
        if (description.includes('社会科学')) tags.push('社会科学');
        if (description.includes('文献')) tags.push('文献管理');
        if (description.includes('分析')) tags.push('数据分析');
        if (description.includes('写作')) tags.push('学术写作');
        if (description.includes('研究')) tags.push('研究方法');
        if (description.includes('扎根理论')) tags.push('扎根理论');
        if (description.includes('社会网络')) tags.push('社会网络分析');
        if (description.includes('布迪�?)) tags.push('布迪厄理�?);
        if (description.includes('ANT')) tags.push('行动者网络理�?);

        return tags.length > 0 ? tags : ['中文社科研究'];
    }

    /**
     * 批量转换所有subagents
     */
    async convertAllSubagents() {
        try {
            // 确保输出目录存在
            await fs.mkdir(this.outputDir, { recursive: true });

            // 读取所有agent文件
            const agentFiles = await fs.readdir(this.sourceDir);
            const mdFiles = agentFiles.filter(file => file.endsWith('.md'));

            console.log(`发现 ${mdFiles.length} 个subagent文件`);

            const results = [];

            for (const file of mdFiles) {
                try {
                    const filePath = path.join(this.sourceDir, file);
                    const content = await fs.readFile(filePath, 'utf-8');
                    
                    // 解析Claude Code格式
                    const claudeConfig = this.parseClaudeConfig(content);
                    const agentName = file.replace('.md', '');
                    
                    // 转换为iFlow CLI格式
                    const iflowConfig = this.convertSubagent(agentName, claudeConfig);
                    
                    // 保存转换后的配置
                    const outputPath = path.join(this.outputDir, `${agentName}.json`);
                    await fs.writeFile(outputPath, JSON.stringify(iflowConfig, null, 2), 'utf-8');
                    
                    results.push({
                        agent: agentName,
                        status: 'success',
                        outputPath
                    });
                    
                    console.log(`�?转换成功: ${agentName}`);
                } catch (error) {
                    console.error(`�?转换失败: ${file}`, error.message);
                    results.push({
                        agent: file.replace('.md', ''),
                        status: 'failed',
                        error: error.message
                    });
                }
            }

            // 生成汇总报�?            await this.generateConversionReport(results);
            
            return results;
        } catch (error) {
            console.error('批量转换失败:', error);
            throw error;
        }
    }

    /**
     * 解析Claude Code配置
     */
    parseClaudeConfig(content) {
        const config = {};
        
        // 提取YAML前置内容
        const yamlMatch = content.match(/^---\n(.*?)\n---/s);
        if (yamlMatch) {
            const yamlContent = yamlMatch[1];
            const lines = yamlContent.split('\n');
            
            for (const line of lines) {
                const match = line.match(/^(\w+):\s*(.*)$/);
                if (match) {
                    config[match[1]] = match[2].replace(/^["']|["']$/g, '');
                }
            }
        }
        
        // 提取主要内容
        const mainContent = content.replace(/^---\n.*?\n---\n/s, '');
        config.content = mainContent;
        
        // 解析各个章节
        const sections = {
            '专业领域': /## 专业领域\s*\n([\s\S]*?)(?=\n##|\n#|$)/,
            '工作方法': /## 工作方法\s*\n([\s\S]*?)(?=\n##|\n#|$)/,
            '质量检查清�?: /## 质量检查清单\s*\n([\s\S]*?)(?=\n##|\n#|$)/,
            '输出标准': /## 输出标准\s*\n([\s\S]*?)(?=\n##|\n#|$)/,
            '使用场景示例': /## 使用场景示例\s*\n([\s\S]*?)(?=\n##|\n#|$)/
        };
        
        for (const [sectionName, pattern] of Object.entries(sections)) {
            const match = mainContent.match(pattern);
            if (match) {
                config[sectionName] = match[1].trim();
            }
        }
        
        return config;
    }

    /**
     * 生成转换报告
     */
    async generateConversionReport(results) {
        const report = {
            timestamp: new Date().toISOString(),
            adapter: 'iFlow CLI Adapter',
            version: '1.0.0',
            total: results.length,
            successful: results.filter(r => r.status === 'success').length,
            failed: results.filter(r => r.status === 'failed').length,
            details: results
        };

        const reportPath = path.join(this.outputDir, 'iflow-conversion-report.json');
        await fs.writeFile(reportPath, JSON.stringify(report, null, 2), 'utf-8');
        
        console.log(`\niFlow CLI转换完成！`);
        console.log(`总计: ${report.total} 个`);
        console.log(`成功: ${report.successful} 个`);
        console.log(`失败: ${report.failed} 个`);
        console.log(`详细报告: ${reportPath}`);
    }

    /**
     * 生成市场发布�?     */
    async generateMarketPackage() {
        try {
            const marketDir = path.join(this.outputDir, 'market-package');
            await fs.mkdir(marketDir, { recursive: true });

            // 读取所有转换后的配�?            const configFiles = await fs.readdir(this.outputDir);
            const jsonFiles = configFiles.filter(file => 
                file.endsWith('.json') && file !== 'iflow-conversion-report.json'
            );

            // 生成市场清单
            const manifest = {
                name: '中文社会科学研究Subagent集合',
                version: '1.0.0',
                description: '专为中文社会科学研究者设计的专业AI Subagent集合',
                author: '中文社科研究Subagent项目�?,
                homepage: 'https://github.com/your-repo/chinese-social-sciences-subagents',
                license: 'MIT',
                keywords: ['中文', '社会科学', '研究', 'AI', 'Subagent'],
                agents: []
            };

            // 复制agent文件并更新清�?            for (const file of jsonFiles) {
                const srcPath = path.join(this.outputDir, file);
                const destPath = path.join(marketDir, file);
                
                await fs.copyFile(srcPath, destPath);
                
                // 读取配置并添加到清单
                const config = JSON.parse(await fs.readFile(srcPath, 'utf-8'));
                manifest.agents.push({
                    name: config.name,
                    displayName: config.displayName,
                    description: config.description,
                    category: config.category,
                    version: config.version,
                    file: file
                });
            }

            // 保存市场清单
            const manifestPath = path.join(marketDir, 'manifest.json');
            await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2), 'utf-8');

            // 生成README
            const readme = this.generateMarketReadme(manifest);
            const readmePath = path.join(marketDir, 'README.md');
            await fs.writeFile(readmePath, readme, 'utf-8');

            console.log(`\n市场发布包已生成: ${marketDir}`);
            console.log(`包含 ${manifest.agents.length} 个agents`);
            
        } catch (error) {
            console.error('生成市场发布包失�?', error);
            throw error;
        }
    }

    /**
     * 生成市场README
     */
    generateMarketReadme(manifest) {
        let readme = `# ${manifest.name}\n\n`;
        readme += `${manifest.description}\n\n`;
        readme += `## 版本信息\n`;
        readme += `- 版本: ${manifest.version}\n`;
        readme += `- 作�? ${manifest.author}\n`;
        readme += `- 许可�? ${manifest.license}\n\n`;
        
        readme += `## 包含的Agents\n\n`;
        for (const agent of manifest.agents) {
            readme += `### ${agent.displayName}\n`;
            readme += `- **名称**: ${agent.name}\n`;
            readme += `- **分类**: ${agent.category}\n`;
            readme += `- **描述**: ${agent.description}\n`;
            readme += `- **版本**: ${agent.version}\n\n`;
        }
        
        readme += `## 安装方法\n\n`;
        readme += `1. 确保已安装iFlow CLI\n`;
        readme += `2. 使用以下命令安装:\n`;
        readme += `\`\`\`bash\n`;
        readme += `iflow market install ${manifest.name}\n`;
        readme += `\`\`\`\n\n`;
        
        readme += `## 使用方法\n\n`;
        readme += `安装完成后，可以通过以下方式使用:\n`;
        readme += `\`\`\`bash\n`;
        readme += `iflow agent list\n`;
        readme += `iflow agent use <agent-name>\n`;
        readme += `\`\`\`\n\n`;
        
        readme += `## 支持\n\n`;
        readme += `- 主页: ${manifest.homepage}\n`;
        readme += `- 问题反馈: ${manifest.homepage}/issues\n\n`;
        
        readme += `## 关键词\n\n`;
        readme += `${manifest.keywords.join(', ')}\n`;
        
        return readme;
    }

    /**
     * 安装转换后的subagents到iFlow CLI
     */
    async installToiFlowCLI() {
        try {
            const iflowConfigDir = path.join(process.env.HOME || process.env.USERPROFILE, '.iflow', 'agents');
            await fs.mkdir(iflowConfigDir, { recursive: true });

            const configFiles = await fs.readdir(this.outputDir);
            const jsonFiles = configFiles.filter(file => file.endsWith('.json') && file !== 'iflow-conversion-report.json');

            for (const file of jsonFiles) {
                const srcPath = path.join(this.outputDir, file);
                const destPath = path.join(iflowConfigDir, file);
                
                await fs.copyFile(srcPath, destPath);
                console.log(`�?安装: ${file}`);
            }

            console.log(`\n所有subagents已安装到iFlow CLI: ${iflowConfigDir}`);
            console.log('重启iFlow CLI即可使用�?);
        } catch (error) {
            console.error('安装失败:', error);
            throw error;
        }
    }
}

// CLI入口
async function main() {
    const adapter = new iFlowCLIAdapter();
    const args = process.argv.slice(2);

    try {
        if (args.includes('--install')) {
            console.log('开始转换并安装到iFlow CLI...');
            await adapter.convertAllSubagents();
            await adapter.installToiFlowCLI();
        } else if (args.includes('--convert')) {
            console.log('开始转换subagents...');
            await adapter.convertAllSubagents();
        } else if (args.includes('--market')) {
            console.log('开始转换并生成市场发布�?..');
            await adapter.convertAllSubagents();
            await adapter.generateMarketPackage();
        } else {
            console.log('iFlow CLI适配�?);
            console.log('');
            console.log('使用方法:');
            console.log('  node iflow-cli-adapter.js --convert   # 仅转换格�?);
            console.log('  node iflow-cli-adapter.js --install   # 转换并安装到iFlow CLI');
            console.log('  node iflow-cli-adapter.js --market    # 转换并生成市场发布包');
            console.log('');
            console.log('说明:');
            console.log('  - 转换结果保存�?./iflow-compatible/ 目录');
            console.log('  - 安装会将配置复制�?~/.iflow/agents/ 目录');
            console.log('  - 市场发布包保存在 ./iflow-compatible/market-package/ 目录');
        }
    } catch (error) {
        console.error('执行失败:', error);
        process.exit(1);
    }
}

// 如果直接运行此脚�?if (import.meta.url === `file://${process.argv[1]}`) {
    main();
}

export default iFlowCLIAdapter;
