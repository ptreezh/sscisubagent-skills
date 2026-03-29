---
name: website-deploy-expert
version: "5.0.0"
subagent-support: false
graceful-fallback: true
execution_modes:
  - cli
performance:
  time: "5-10 min"
  reliability: "high"
---

# SocienceAI 网站部署技能 (Website Deploy Expert)

一键构建并部署 VitePress 网站到 www.socienceAI.com。

## 架构概览

```
D:\socienceAI\agentskills\website\
├── docs\                    # VitePress 源文件
│   ├── index.md             # 首页
│   ├── methodologies\       # 60 个技能页面 (.md)
│   │   ├── index.md         # 技能列表索引
│   │   ├── grounded-theory.md
│   │   ├── swot-analysis.md
│   │   └── ... (60 files)
│   ├── guide\               # 使用指南
│   ├── blog\                # 博客
│   ├── about\               # 关于
│   └── .vitepress\
│       ├── config.mts       # 侧边栏配置
│       └── dist\            # 构建输出 (HTML)
├── package.json             # VitePress 依赖
└── build-state.json         # 构建状态追踪
```

## 部署目标

| 项目 | 值 |
|------|-----|
| 域名 | www.socienceAI.com |
| FTP 主机 | 103.99.40.226 |
| FTP 用户 | 3njf8mh28i222 |
| FTP 密码 | 4GrdQlUW38 |
| 远程目录 | /web |
| 网站根目录 | /web (不是 /) |
| 控制面板 | https://dedit1010n55-dedihosts-hk-control.topvps.top/vhost/ |
| 主机商 | 硅云 (vpsor.cn) |

## 完整部署流程

### 步骤 1：修改内容

编辑 `D:\socienceAI\agentskills\website\docs\` 下的 `.md` 文件。

添加新技能页面时需更新：
- `docs/.vitepress/config.mts` — 侧边栏导航
- `docs/methodologies/index.md` — 技能列表

或运行生成脚本批量更新：
```bash
python D:\socienceAI\scripts\generate-website-pages.py
```

### 步骤 2：构建

```bash
cd D:\socienceAI\agentskills\website
npm run build
```

输出目录：`docs\.vitepress\dist\`

### 步骤 3：部署到 FTP

```python
import os
from pathlib import Path
from ftplib import FTP

FTP_HOST = '103.99.40.226'
FTP_USER = '3njf8mh28i222'
FTP_PASS = '4GrdQlUW38'
LOCAL_DIR = Path(r'D:\socienceAI\agentskills\website\docs\.vitepress\dist')
REMOTE_DIR = '/web'

ftp = FTP()
ftp.connect(FTP_HOST, 21, timeout=30)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(REMOTE_DIR)

for root, dirs, files in os.walk(LOCAL_DIR):
    rel = Path(root).relative_to(LOCAL_DIR)
    rd = REMOTE_DIR if str(rel) == '.' else REMOTE_DIR + '/' + str(rel).replace('\\', '/')
    # Ensure directory exists
    if rd != REMOTE_DIR:
        parts = rd.strip('/').split('/')
        cur = ''
        for p in parts:
            cur += '/' + p
            try:
                ftp.cwd(cur)
            except:
                try:
                    ftp.mkd(cur)
                except:
                    pass
        ftp.cwd('/')
    # Upload files
    for f in files:
        lp = Path(root) / f
        rp = rd + '/' + f
        with open(str(lp), 'rb') as fh:
            ftp.storbinary('STOR ' + rp, fh)
        print(f'  OK {rp}')

ftp.quit()
print('Deploy complete!')
```

### 步骤 4：验证

```bash
# 检查首页
curl -sI http://www.socienceAI.com/ | head -3

# 检查方法论页
curl -sI http://www.socienceAI.com/methodologies/ | head -3

# 检查单个技能
curl -sI http://www.socienceAI.com/methodologies/grounded-theory.html | head -3
```

## 重要注意事项

1. **网站根目录是 `/web` 不是 `/`** — 上传到 `/` 不会影响线上网站
2. **不要删除** `/web/agents/`, `/web/web.zip` 等旧文件 — 它们属于其他页面
3. **`#VPContent` 不是断链** — VitePress SPA 内部锚点
4. **FTP 可能超时** — 大文件需重试
5. **不要关闭用户的 Edge 浏览器** — 会丢失 session

## 技能页面生成

批量生成所有技能的 VitePress 页面：

```bash
python D:\socienceAI\scripts\generate-website-pages.py
```

此脚本会：
- 从 `agentskills-index.json` 读取所有技能
- 生成 60+ 个 `.md` 页面到 `website/docs/methodologies/`
- 更新 `methodologies/index.md`
- 更新 `.vitepress/config.mts` 侧边栏
- 更新 `build-state.json`

## 快速命令

```bash
# 一键构建+部署
cd D:\socienceAI\agentskills\website && npm run build && python D:\socienceAI\agentskills\deploy-to-web.py
```
