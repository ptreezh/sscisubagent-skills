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
          text: '质性研究方法',
          items: [
            { text: '扎根理论', link: '/methodologies/grounded-theory' },
            { text: '社会网络分析', link: '/methodologies/sna' },
            { text: '行动者网络理论', link: '/methodologies/ant' },
            { text: '布迪厄场域分析', link: '/methodologies/bourdieu' }
          ]
        },
        {
          text: '定量研究方法',
          items: [
            { text: 'QCA', link: '/methodologies/qca' },
            { text: 'DID', link: '/methodologies/did' },
            { text: '回归分析', link: '/methodologies/regression' },
            { text: '问卷设计', link: '/methodologies/survey' }
          ]
        },
        {
          text: '混合方法与社会理论',
          items: [
            { text: '混合方法', link: '/methodologies/mixed-methods' },
            { text: '数字马克思', link: '/methodologies/digital-marx' },
            { text: '数字涂尔干', link: '/methodologies/digital-durkheim' },
            { text: '数字韦伯', link: '/methodologies/digital-weber' }
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
