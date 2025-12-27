/**
 * 科大讯飞星火大模型集成技能
 * 遵循agentskills.io规范和渐进式披露原则
 */

class SparkIntegrationSkill {
    constructor(config = {}) {
        this.skillId = "spark-integration";
        this.name = "科大讯飞星火大模型集成";
        this.version = "1.0.0";
        this.description = "集成科大讯飞星火大模型进行智能分析";
        
        // 从环境变量或配置中加载API凭证
        this.appId = config.appId || process.env.SPARK_APP_ID;
        this.apiKey = config.apiKey || process.env.SPARK_API_KEY;
        this.apiSecret = config.apiSecret || process.env.SPARK_API_SECRET;
        
        // 默认模型
        this.defaultModel = config.model || "spark-max";
        
        // API基础URL
        this.baseUrl = config.baseUrl || "https://spark-api-open.xf-yun.com/v1/chat/completions";
        
        // 初始化完成标志
        this.isInitialized = !!(this.appId && this.apiKey && this.apiSecret);
    }

    /**
     * 基本信息 - 第一层级：最核心的功能说明
     */
    getBasicInfo() {
        return {
            skillId: this.skillId,
            name: this.name,
            version: this.version,
            description: this.description,
            isInitialized: this.isInitialized
        };
    }

    /**
     * 能力详情 - 第二层级：详细功能说明
     */
    getCapabilities() {
        if (!this.isInitialized) {
            throw new Error("技能未初始化，请先配置API凭证");
        }

        return {
            skillId: this.skillId,
            capabilities: [
                {
                    name: "文本分析",
                    description: "使用科大讯飞星火大模型进行文本分析",
                    methods: ["analyzeText"]
                },
                {
                    name: "智能对话",
                    description: "基于星火大模型的智能对话功能",
                    methods: ["chat", "converse"]
                },
                {
                    name: "内容生成",
                    description: "利用星火大模型生成高质量内容",
                    methods: ["generateContent"]
                }
            ]
        };
    }

    /**
     * 详细接口 - 第三层级：具体API接口
     */
    getAPIInterface() {
        if (!this.isInitialized) {
            throw new Error("技能未初始化，请先配置API凭证");
        }

        return {
            skillId: this.skillId,
            endpoints: [
                {
                    name: "analyzeText",
                    description: "文本分析功能",
                    parameters: {
                        text: "待分析的文本",
                        analysisType: "分析类型（可选）",
                        model: "指定模型（可选）"
                    }
                },
                {
                    name: "chat",
                    description: "智能对话功能",
                    parameters: {
                        message: "用户消息",
                        history: "对话历史（可选）",
                        model: "指定模型（可选）"
                    }
                },
                {
                    name: "generateContent",
                    description: "内容生成功能",
                    parameters: {
                        prompt: "生成提示",
                        contentType: "内容类型（可选）",
                        model: "指定模型（可选）"
                    }
                }
            ]
        };
    }

    /**
     * 完整文档 - 第四层级：完整的技术文档
     */
    getFullDocumentation() {
        if (!this.isInitialized) {
            throw new Error("技能未初始化，请先配置API凭证");
        }

        return {
            skillId: this.skillId,
            basicInfo: this.getBasicInfo(),
            capabilities: this.getCapabilities(),
            apiInterface: this.getAPIInterface(),
            usageGuide: {
                initialization: "new SparkIntegrationSkill({appId: '...', apiKey: '...', apiSecret: '...'})",
                example: {
                    code: "const skill = new SparkIntegrationSkill(config);\nconst result = await skill.analyzeText('分析这段文本');",
                    explanation: "初始化技能实例并调用文本分析功能"
                }
            },
            configuration: {
                required: ["appId", "apiKey", "apiSecret"],
                optional: ["model", "baseUrl"],
                environmentVars: ["SPARK_APP_ID", "SPARK_API_KEY", "SPARK_API_SECRET"]
            }
        };
    }

    /**
     * 文本分析功能
     */
    async analyzeText(text, options = {}) {
        if (!this.isInitialized) {
            throw new Error("技能未初始化，请先配置API凭证");
        }

        const model = options.model || this.defaultModel;
        const analysisType = options.analysisType || "general";

        // 根据分析类型构建提示词
        let prompt;
        switch (analysisType) {
            case "sentiment":
                prompt = `请分析以下文本的情感倾向：\n\n${text}`;
                break;
            case "summary":
                prompt = `请对以下文本进行摘要：\n\n${text}`;
                break;
            case "topic":
                prompt = `请识别以下文本的主题：\n\n${text}`;
                break;
            default:
                prompt = `请分析以下文本：\n\n${text}`;
        }

        return await this.callSparkAPI(prompt, model);
    }

    /**
     * 智能对话功能
     */
    async chat(message, options = {}) {
        if (!this.isInitialized) {
            throw new Error("技能未初始化，请先配置API凭证");
        }

        const model = options.model || this.defaultModel;
        const history = options.history || [];

        // 构建对话消息
        const messages = [
            ...history,
            { role: "user", content: message }
        ];

        // 构建提示词
        const prompt = messages.map(msg => `${msg.role}: ${msg.content}`).join("\n");

        return await this.callSparkAPI(prompt, model);
    }

    /**
     * 内容生成功能
     */
    async generateContent(prompt, options = {}) {
        if (!this.isInitialized) {
            throw new Error("技能未初始化，请先配置API凭证");
        }

        const model = options.model || this.defaultModel;
        const contentType = options.contentType || "general";

        // 根据内容类型调整提示词
        let finalPrompt = prompt;
        if (contentType === "article") {
            finalPrompt = `请写一篇关于"${prompt}"的文章`;
        } else if (contentType === "summary") {
            finalPrompt = `请总结关于"${prompt}"的关键点`;
        } else if (contentType === "outline") {
            finalPrompt = `请为"${prompt}"创建一个大纲`;
        }

        return await this.callSparkAPI(finalPrompt, model);
    }

    /**
     * 调用科大讯飞API的核心方法
     */
    async callSparkAPI(prompt, model = this.defaultModel) {
        // 这里我们集成之前创建的SparkAPI类
        // 为了简化，直接使用fetch API调用后端接口
        try {
            const response = await fetch('/backend/api/spark/call', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    model: model,
                    appId: this.appId,
                    apiKey: this.apiKey,
                    apiSecret: this.apiSecret
                })
            });

            if (!response.ok) {
                throw new Error(`API调用失败: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            return {
                success: true,
                result: data,
                model: model,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            console.error('调用科大讯飞API时出错:', error);
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * 模型列表查询
     */
    getAvailableModels() {
        return {
            skillId: this.skillId,
            models: [
                { name: "spark-max", description: "星火Max认知大模型" },
                { name: "spark-pro", description: "星火Pro认知大模型" },
                { name: "spark-standard", description: "星火Standard认知大模型" },
                { name: "spark-mini", description: "星火Mini认知大模型" },
                { name: "spark-vision", description: "星火多模态认知大模型" }
            ]
        };
    }

    /**
     * 健康检查
     */
    async healthCheck() {
        try {
            // 尝试进行一个简单的API调用
            const result = await this.callSparkAPI("健康检查", "spark-mini");
            return {
                skillId: this.skillId,
                status: result.success ? "healthy" : "unhealthy",
                message: result.success ? "API连接正常" : result.error,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                skillId: this.skillId,
                status: "unhealthy",
                message: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }
}

// 导出技能类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SparkIntegrationSkill;
}

// 为了让技能可以被动态加载，暴露创建函数
if (typeof window !== 'undefined') {
    window.SparkIntegrationSkill = SparkIntegrationSkill;
}