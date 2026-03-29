import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'SocienceAI',
  description: '让社会科学研究人人可为',
  lastUpdated: true,
  
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],
  
  themeConfig: {
    logo: '/logo.png',
    
    nav: [
      { text: '首页', link: '/' },
      { text: '方法论', link: '/methodologies/' },
      { text: '使用指南', link: '/guide/' },
      { text: '关于', link: '/about/' },
      { text: '博客', link: '/blog/' }
    ],
    
    sidebar: {
      '/methodologies/': [
        {
          text: '质性研究方法 (14)',
          items: [
            { text: '主题分析专家', link: '/methodologies/thematic-analysis' },
            { text: '会话分析专家', link: '/methodologies/conversation-analysis' },
            { text: '修辞分析专家', link: '/methodologies/rhetoric-analysis' },
            { text: '内容分析专家', link: '/methodologies/content-analysis' },
            { text: '叙事分析专家', link: '/methodologies/narrative-analysis' },
            { text: '扎根理论专家', link: '/methodologies/grounded-theory' },
            { text: '案例研究专家', link: '/methodologies/case-study' },
            { text: '民族志专家', link: '/methodologies/ethnography' },
            { text: '现象学研究专家', link: '/methodologies/phenomenology' },
            { text: '符号学分析专家', link: '/methodologies/semiotics-analysis' },
            { text: '视觉分析专家', link: '/methodologies/visual-analysis' },
            { text: '话语分析专家', link: '/methodologies/discourse-analysis' },
            { text: '诠释现象学分析专家', link: '/methodologies/ipa-analysis' },
            { text: '问卷设计专家', link: '/methodologies/survey-design' }
          ]
        },
        {
          text: '定量研究方法 (9)',
          items: [
            { text: '二手数据分析专家', link: '/methodologies/secondary-analysis' },
            { text: '元分析专家', link: '/methodologies/meta-analysis' },
            { text: '回归分析专家', link: '/methodologies/regression-analysis' },
            { text: '因子分析专家', link: '/methodologies/factor-analysis' },
            { text: '多层模型专家', link: '/methodologies/multilevel-modeling' },
            { text: '数据分析专家', link: '/methodologies/data-analysis' },
            { text: '文献计量分析专家', link: '/methodologies/bibliometric-analysis' },
            { text: '纵向数据分析专家', link: '/methodologies/longitudinal-analysis' },
            { text: '结构方程模型专家', link: '/methodologies/sem-analysis' }
          ]
        },
        {
          text: '混合方法研究 (2)',
          items: [
            { text: '混合方法研究专家', link: '/methodologies/mixed-methods' },
            { text: '行动研究专家', link: '/methodologies/action-research' }
          ]
        },
        {
          text: '实验研究方法 (1)',
          items: [
            { text: 'RCT实验设计专家', link: '/methodologies/rct-experimental-design' }
          ]
        },
        {
          text: '计算研究方法 (3)',
          items: [
            { text: 'NLP文本挖掘专家', link: '/methodologies/nlp-text-mining' },
            { text: '机器学习研究专家', link: '/methodologies/machine-learning-research' },
            { text: '社会序列分析专家', link: '/methodologies/social-sequence-analysis' }
          ]
        },
        {
          text: '网络分析方法 (2)',
          items: [
            { text: '社会网络分析专家', link: '/methodologies/social-network-analysis' },
            { text: '行动者网络理论专家', link: '/methodologies/actor-network-analysis' }
          ]
        },
        {
          text: '场域分析方法 (1)',
          items: [
            { text: '布迪厄场域分析专家', link: '/methodologies/bourdieu-field-analysis' }
          ]
        },
        {
          text: '理论分析方法 (3)',
          items: [
            { text: '数字涂尔干专家', link: '/methodologies/digital-durkheim' },
            { text: '数字韦伯专家', link: '/methodologies/digital-weber' },
            { text: '数字马克思主义专家', link: '/methodologies/digital-marx' }
          ]
        },
        {
          text: '复杂系统方法 (2)',
          items: [
            { text: '复杂适应系统仿真专家', link: '/methodologies/cas-simulation' },
            { text: '系统动力学专家', link: '/methodologies/system-dynamics' }
          ]
        },
        {
          text: '实证分析方法 (2)',
          items: [
            { text: '双重差分分析专家', link: '/methodologies/did-analysis' },
            { text: '定性比较分析专家', link: '/methodologies/qca-analysis' }
          ]
        },
        {
          text: '战略分析方法 (8)',
          items: [
            { text: 'PEST/PESTEL环境分析专家', link: '/methodologies/pest-analysis' },
            { text: 'SWOT战略分析专家', link: '/methodologies/swot-analysis' },
            { text: '价值主张设计专家', link: '/methodologies/value-proposition' },
            { text: '平衡计分卡专家', link: '/methodologies/balanced-scorecard' },
            { text: '波特五力模型专家', link: '/methodologies/porter-five-forces' },
            { text: '精益创业专家', link: '/methodologies/lean-startup' },
            { text: '蓝海战略专家', link: '/methodologies/blue-ocean-strategy' },
            { text: '设计思维专家', link: '/methodologies/design-thinking' }
          ]
        },
        {
          text: '市场营销方法 (2)',
          items: [
            { text: '品牌资产评估专家', link: '/methodologies/brand-equity' },
            { text: '消费者行为分析专家', link: '/methodologies/consumer-behavior' }
          ]
        },
        {
          text: '组织管理方法 (4)',
          items: [
            { text: 'OKR目标管理专家', link: '/methodologies/okr' },
            { text: '变革管理专家', link: '/methodologies/change-management' },
            { text: '敏捷项目管理专家', link: '/methodologies/agile-pm' },
            { text: '组织诊断专家', link: '/methodologies/organizational-diagnosis' }
          ]
        },
        {
          text: '商业分析方法 (2)',
          items: [
            { text: '商业模式专家', link: '/methodologies/business-model' },
            { text: '商业生态系统专家', link: '/methodologies/business-ecosystem' }
          ]
        },
        {
          text: '媒介研究方法 (2)',
          items: [
            { text: '互联网研究专家', link: '/methodologies/internet-research' },
            { text: '媒介分析专家', link: '/methodologies/media-analysis' }
          ]
        },
        {
          text: '历史分析方法 (2)',
          items: [
            { text: '历史分析专家', link: '/methodologies/historical-analysis' },
            { text: '文档分析专家', link: '/methodologies/document-analysis' }
          ]
        },
        {
          text: 'Meta技能 (1)',
          items: [
            { text: '技能升级专家', link: '/methodologies/skill-upgrade' }
          ]
        }
      ],
      '/guide/': [
        {
          text: '快速开始',
          items: [
            { text: '安装', link: '/guide/installation' },
            { text: '快速开始', link: '/guide/quick-start' },
            { text: '使用示例', link: '/guide/examples' }
          ]
        }
      ]
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/socienceai' },
      { icon: 'twitter', link: 'https://twitter.com/socienceai' }
    ],
    
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 SocienceAI'
    }
  }
})
