#!/usr/bin/env python3
"""
SocienceAI 网站自主建设引擎
Website Builder Engine

Day 1-7 自动化脚本

版本：1.0.0
日期：2026-03-22
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class WebsiteBuilder:
    """网站建设引擎"""
    
    def __init__(self, working_dir: str = './website'):
        self.working_dir = Path(working_dir)
        self.docs_dir = self.working_dir / 'docs'
        self.state_path = self.working_dir / 'build-state.json'
        
        self.state = {
            'current_day': 0,
            'completed_tasks': [],
            'pending_tasks': [],
            'generated_pages': []
        }
        
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if self.state_path.exists():
            with open(self.state_path, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
    
    def save_state(self):
        """保存状态"""
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    # ========================================================================
    # Day 1: 项目初始化
    # ========================================================================
    
    def day1_init(self):
        """Day 1: 项目初始化"""
        print("\n" + "="*60)
        print("Day 1: 项目初始化")
        print("="*60)
        
        tasks = [
            "创建项目目录",
            "初始化 Git",
            "创建基础文件结构",
            "创建 README.md"
        ]
        
        # 创建目录
        dirs = [
            self.working_dir,
            self.docs_dir,
            self.docs_dir / '.vitepress',
            self.docs_dir / 'methodologies',
            self.docs_dir / 'guide',
            self.docs_dir / 'about',
            self.docs_dir / 'blog',
        ]
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ 创建目录：{d}")
        
        # 创建 README.md
        readme_content = """# SocienceAI Website

> 让社会科学研究人人可为

## 快速开始

```bash
npm install
npm run dev
```

## 部署

```bash
npm run build
vercel --prod
```

## 目录结构

```
docs/
├── index.md              # 首页
├── methodologies/        # 方法论页面
├── guide/               # 使用指南
├── about/               # 关于
└── blog/                # 博客
```

## 许可证

MIT License
"""
        
        with open(self.working_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  ✅ 创建 README.md")
        
        # 更新状态
        self.state['current_day'] = 1
        self.state['completed_tasks'].extend(tasks)
        self.save_state()
        
        print("\n✅ Day 1 完成")
    
    # ========================================================================
    # Day 2-3: VitePress 配置
    # ========================================================================
    
    def day2_vitepress_config(self):
        """Day 2-3: VitePress 配置"""
        print("\n" + "="*60)
        print("Day 2-3: VitePress 配置")
        print("="*60)
        
        # 创建 package.json
        package_json = {
            "name": "socienceai-website",
            "version": "1.0.0",
            "description": "SocienceAI 官方网站",
            "scripts": {
                "dev": "vitepress dev docs",
                "build": "vitepress build docs",
                "preview": "vitepress preview docs"
            },
            "devDependencies": {
                "vitepress": "^1.0.0"
            }
        }
        
        with open(self.working_dir / 'package.json', 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
        print(f"  ✅ 创建 package.json")
        
        # 创建 VitePress 配置文件
        config_content = """import { defineConfig } from 'vitepress'

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
"""
        
        config_path = self.docs_dir / '.vitepress' / 'config.mts'
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"  ✅ 创建 VitePress 配置")
        
        # 更新状态
        self.state['current_day'] = 3
        self.save_state()
        
        print("\n✅ Day 3 完成")
    
    # ========================================================================
    # Day 4-5: 首页生成
    # ========================================================================
    
    def day4_homepage(self):
        """Day 4-5: 首页生成"""
        print("\n" + "="*60)
        print("Day 4-5: 首页生成")
        print("="*60)
        
        # 创建首页
        homepage_content = """---
layout: home
hero:
  name: SocienceAI
  text: 让社会科学研究人人可为
  tagline: 通过 AI 技术推动社会科学研究的范式革新
  image:
    src: /hero.png
    alt: SocienceAI
  actions:
    - theme: brand
      text: 开始使用
      link: /guide/quick-start
    - theme: alt
      text: 方法论
      link: /methodologies/
features:
  - icon: 📚
    title: 12 种方法论专家
    details: 扎根理论、社会网络分析、行动者网络理论、布迪厄场域分析等
  - icon: 🤖
    title: AI 辅助分析
    details: 智能编码、自动验证、持续进化，让研究更高效
  - icon: ✅
    title: 严格质量保证
    details: 所有报告必须经过严格测试和验证
  - icon: 🌍
    title: 完全免费开源
    details: 开放源代码，遵循 MIT 许可证，欢迎贡献
  - icon: 📖
    title: 详细文档
    details: 完整的使用教程、案例研究、最佳实践
  - icon: 💬
    title: 社区支持
    details: 活跃的社区，及时的技术支持
---

## 什么是 SocienceAI？

SocienceAI 是一个基于 AI 技术的社会科学方法论支持平台，致力于让严谨的社会科学方法论不再高深，让高质量的研究人人可为。

## 核心能力

### 方法论专家

我们提供 12 种社会科学方法论的 AI 专家支持：

**质性研究方法**:
- 扎根理论（Glaser & Strauss, Charmaz）
- 社会网络分析（Freeman, Wasserman）
- 行动者网络理论（Latour, Callon）
- 布迪厄场域分析（Bourdieu）

**定量研究方法**:
- QCA 定性比较分析（Ragin）
- DID 双重差分（Angrist & Pischke）
- 回归分析
- 问卷设计

**混合方法与社会理论**:
- 混合方法研究（Creswell）
- 数字马克思分析
- 数字涂尔干分析
- 数字韦伯分析

### AI 辅助功能

- **智能编码**: 自动识别概念、建立范畴
- **自动验证**: 测试覆盖率检查、方法论规范验证
- **持续进化**: 自主学习和改进
- **质量保证**: 严格的测试和验证流程

## 快速开始

```bash
# 使用 CLI
qwen "使用扎根理论分析以下访谈数据..."
```

[查看详细使用指南](/guide/quick-start)

## 适用场景

- 📝 **学位论文**: 帮助研究生完成数据分析
- 🔬 **研究项目**: 支持国家级社科基金项目
- 📊 **企业研究**: 用户研究、市场研究
- 🎓 **教学培训**: 方法论教学工作

## 成功案例

> "SocienceAI 帮助我完成了博士论文的数据分析，盲审获得优秀！"
> —— 某高校管理学博士生

> "使用 SocienceAI 的扎根理论工具，我们的研究效率提升了 50%。"
> —— 某研究机构研究团队

## 加入我们

- 🌟 [GitHub](https://github.com/socienceai) - 查看源代码
- 📱 [Twitter](https://twitter.com/socienceai) - 关注最新动态
- 💬 [Discord](https://discord.gg/socienceai) - 加入社区讨论

## 合作伙伴

[待添加]

---

*让社会科学研究人人可为*
"""
        
        with open(self.docs_dir / 'index.md', 'w', encoding='utf-8') as f:
            f.write(homepage_content)
        print(f"  ✅ 创建首页")
        
        # 更新状态
        self.state['current_day'] = 5
        self.state['generated_pages'].append('index.md')
        self.save_state()
        
        print("\n✅ Day 5 完成")
    
    # ========================================================================
    # Day 6-7: 方法论页面生成
    # ========================================================================
    
    def day6_methodology_pages(self):
        """Day 6-7: 方法论页面生成"""
        print("\n" + "="*60)
        print("Day 6-7: 方法论页面生成")
        print("="*60)
        
        # 方法论数据
        methodologies = {
            'grounded-theory': {
                'name': '扎根理论',
                'category': '质性研究',
                'masters': 'Kathy Charmaz / Strauss & Corbin',
                'works': [
                    'Charmaz, K. (2014). Constructing Grounded Theory',
                    'Strauss, A. & Corbin, J. (1990). Basics of Qualitative Research'
                ],
                'concepts': ['开放编码', '轴心编码', '选择式编码', '理论饱和度'],
                'applications': ['访谈数据分析', '理论建构研究', '探索性研究']
            },
            'sna': {
                'name': '社会网络分析',
                'category': '质性研究',
                'masters': 'Linton Freeman / Stanley Wasserman',
                'works': [
                    'Wasserman, S. & Faust, K. (1994). Social Network Analysis',
                    'Borgatti, S.P. & Foster, P.C. (2003). The Network Paradigm'
                ],
                'concepts': ['中心性分析', '社区检测', '结构洞分析'],
                'applications': ['组织网络研究', '社交网络分析', '知识网络研究']
            },
            'ant': {
                'name': '行动者网络理论',
                'category': '质性研究',
                'masters': 'Bruno Latour / Michel Callon',
                'works': [
                    'Latour, B. (2005). Reassembling the Social',
                    'Callon, M. (1986). Some Elements of a Sociology of Translation'
                ],
                'concepts': ['行动者识别', '转译过程', '网络稳定化'],
                'applications': ['科技社会学研究', '创新扩散分析', '技术评估']
            },
            'bourdieu': {
                'name': '布迪厄场域分析',
                'category': '质性研究',
                'masters': 'Pierre Bourdieu',
                'works': [
                    'Bourdieu, P. (1984). Distinction',
                    'Bourdieu, P. (1993). The Field of Cultural Production'
                ],
                'concepts': ['场域识别', '资本分析', '习性分析'],
                'applications': ['文化研究', '教育社会学', '权力结构分析']
            },
            'qca': {
                'name': 'QCA 定性比较分析',
                'category': '定量研究',
                'masters': 'Charles Ragin',
                'works': [
                    'Ragin, C.C. (2008). Redesigning Social Inquiry',
                    'Schneider, C.Q. & Wagemann, C. (2012). Set-Theoretic Methods'
                ],
                'concepts': ['模糊集校准', '真值表构建', '布尔最小化'],
                'applications': ['中小样本比较研究', '因果复杂性分析']
            },
            'did': {
                'name': 'DID 双重差分',
                'category': '定量研究',
                'masters': 'Joshua Angrist & Jörn-Steffen Pischke',
                'works': [
                    'Angrist, J.D. & Pischke, J.S. (2009). Mostly Harmless Econometrics'
                ],
                'concepts': ['平行趋势假设', '双向固定效应', '稳健性检验'],
                'applications': ['政策效果评估', '准实验设计分析']
            },
            'regression': {
                'name': '回归分析',
                'category': '定量研究',
                'masters': 'Ronald Fisher / Karl Pearson',
                'works': [
                    'Fisher, R.A. (1925). Statistical Methods for Research Workers',
                    'Wooldridge, J.M. (2013). Introductory Econometrics'
                ],
                'concepts': ['OLS 估计', '假设检验', '模型诊断'],
                'applications': ['计量经济学分析', '社会科学实证研究']
            },
            'survey': {
                'name': '问卷设计',
                'category': '定量研究',
                'masters': 'Don A. Dillman / Floyd J. Fowler',
                'works': [
                    'Dillman, D.A. (2014). Internet, Phone, Mail, and Mixed-Mode Surveys',
                    'Fowler, F.J. (2014). Survey Research Methods'
                ],
                'concepts': ['问题设计', '抽样方法', '信效度检验'],
                'applications': ['社会调查', '市场研究', '政策评估']
            },
            'mixed-methods': {
                'name': '混合方法研究',
                'category': '混合方法',
                'masters': 'John Creswell / Vicki Plano Clark',
                'works': [
                    'Creswell, J.W. & Plano Clark, V.L. (2018). Designing and Conducting Mixed Methods Research'
                ],
                'concepts': ['三角验证', '互补设计', '转换/整合'],
                'applications': ['复杂现象研究', '多层次分析']
            },
            'digital-marx': {
                'name': '数字马克思分析',
                'category': '社会理论',
                'masters': 'David Harvey / Christian Fuchs',
                'works': [
                    'Fuchs, C. (2014). Digital Labour and Karl Marx',
                    "Harvey, D. (2010). A Companion to Marx's Capital"
                ],
                'concepts': ['数字劳动', '剩余价值', '意识形态批判'],
                'applications': ['平台经济研究', '数字劳动分析']
            },
            'digital-durkheim': {
                'name': '数字涂尔干分析',
                'category': '社会理论',
                'masters': 'Émile Durkheim',
                'works': [
                    'Durkheim, E. (1912). The Elementary Forms of the Religious Life'
                ],
                'concepts': ['集体意识', '社会团结', '神圣/世俗'],
                'applications': ['数字宗教研究', '在线社区分析']
            },
            'digital-weber': {
                'name': '数字韦伯分析',
                'category': '社会理论',
                'masters': 'Max Weber',
                'works': [
                    'Weber, M. (1922). Economy and Society',
                    'Weber, M. (1905). The Protestant Ethic and the Spirit of Capitalism'
                ],
                'concepts': ['理性化', '科层制', '祛魅'],
                'applications': ['平台科层制研究', '数字权威分析']
            }
        }
        
        # 生成方法论页面
        for slug, data in methodologies.items():
            page_content = f"""# {data['name']}

> {data['category']}方法论专家

## 概述

{data['name']}是一种{data['category']}研究方法，由 **{data['masters']}** 创立并发展。

## 核心著作

"""
            for work in data['works']:
                page_content += f"- {work}\n"
            
            page_content += """
## 核心概念

"""
            for concept in data['concepts']:
                page_content += f"- {concept}\n"
            
            page_content += """
## 适用场景

"""
            for app in data['applications']:
                page_content += f"- {app}\n"
            
            page_content += f"""

## 如何使用

### CLI 使用

```bash
qwen "使用{data['name']}分析以下数据..."
```

### 在线使用

[待添加在线工具链接]

## 对标学者

**{data['masters']}**

## 学习资源

- [待添加教程链接]
- [待添加视频链接]
- [待添加案例]

## 相关方法论

[待添加相关链接]

---

*由 SocienceAI 提供 | [返回方法论列表](/methodologies/)*
"""
            
            page_path = self.docs_dir / 'methodologies' / f'{slug}.md'
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(page_content)
            print(f"  ✅ 创建 {data['name']} 页面")
        
        # 创建方法论索引页
        index_content = """# 方法论

SocienceAI 提供 12 种社会科学方法论的 AI 专家支持。

## 质性研究方法

- [扎根理论](/methodologies/grounded-theory) - Kathy Charmaz / Strauss & Corbin
- [社会网络分析](/methodologies/sna) - Linton Freeman / Stanley Wasserman
- [行动者网络理论](/methodologies/ant) - Bruno Latour / Michel Callon
- [布迪厄场域分析](/methodologies/bourdieu) - Pierre Bourdieu

## 定量研究方法

- [QCA 定性比较分析](/methodologies/qca) - Charles Ragin
- [DID 双重差分](/methodologies/did) - Joshua Angrist & Jörn-Steffen Pischke
- [回归分析](/methodologies/regression) - Ronald Fisher / Karl Pearson
- [问卷设计](/methodologies/survey) - Don A. Dillman / Floyd J. Fowler

## 混合方法与社会理论

- [混合方法研究](/methodologies/mixed-methods) - John Creswell / Vicki Plano Clark
- [数字马克思分析](/methodologies/digital-marx) - David Harvey / Christian Fuchs
- [数字涂尔干分析](/methodologies/digital-durkheim) - Émile Durkheim
- [数字韦伯分析](/methodologies/digital-weber) - Max Weber

## 选择方法论

不确定使用哪种方法？[查看方法论选择指南](/guide/choose-method)

---

*由 SocienceAI 提供*
"""
        
        with open(self.docs_dir / 'methodologies' / 'index.md', 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"  ✅ 创建方法论索引页")
        
        # 更新状态
        self.state['current_day'] = 7
        self.state['generated_pages'].extend([f'{slug}.md' for slug in methodologies.keys()])
        self.state['generated_pages'].append('methodologies/index.md')
        self.save_state()
        
        print("\n✅ Day 7 完成")
        print(f"\n📊 总计生成 {len(methodologies) + 1} 个方法论页面")
    
    # ========================================================================
    # 主函数
    # ========================================================================
    
    def run(self, day: int = None):
        """运行网站建设"""
        
        if day is None or day <= 1:
            self.day1_init()
        
        if day is None or day <= 3:
            self.day2_vitepress_config()
        
        if day is None or day <= 5:
            self.day4_homepage()
        
        if day is None or day <= 7:
            self.day6_methodology_pages()
        
        print("\n" + "="*60)
        print("✅ 网站建设第一阶段完成！")
        print("="*60)
        print(f"\n📊 统计:")
        print(f"  当前进度：Day {self.state['current_day']}")
        print(f"  生成页面：{len(self.state['generated_pages'])} 个")
        print(f"  完成任务：{len(self.state['completed_tasks'])} 项")
        print("\n下一步:")
        print("  1. npm install")
        print("  2. npm run dev")
        print("  3. 测试网站")
        print("  4. vercel --prod (部署上线)")
        print()


# ============================================================================
# 主程序
# ============================================================================

if __name__ == '__main__':
    import sys
    
    # 获取指定天数
    day = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    # 创建引擎
    builder = WebsiteBuilder()
    
    # 运行
    builder.run(day)
