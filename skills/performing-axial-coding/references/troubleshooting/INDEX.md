# 轴心编码故障排除快速指南

> **快速诊断**：根据症状快速定位问题和解决方案。

## 快速诊断表

| 症状 | 可能问题 | 快速解决 | 详细文档 |
|-----|---------|---------|---------|
| 范畴过于宽泛 | 聚类数量太少 | 增加n_categories参数 | `category-issues.md` - 问题1 |
| 概念归属不明确 | 范畴边界模糊 | 重新定义范畴边界 | `category-issues.md` - 问题2 |
| 关系论证不充分 | 数据支持不足 | 回到原始数据寻找证据 | `relationship-issues.md` - 问题1 |
| Paradigm不完整 | 缺少关键组件 | 系统检查六个组件 | `relationship-issues.md` - 问题2 |
| 工具输出不合理 | 参数设置不当 | 调整工具参数 | `technical-issues.md` - 问题1 |
| 范畴命名不当 | 缺乏理论敏感性 | 遵循命名原则 | `category-issues.md` - 问题3 |

---

## 三大问题类别

### 1. 范畴构建问题
**常见症状**：
- 范畴过于宽泛或过于狭窄
- 概念归属不明确
- 范畴命名不当

**快速诊断**：
```bash
python scripts/validate_categories.py --input categories.json
```

**详见**：`category-issues.md`

---

### 2. 关系识别问题
**常见症状**：
- 关系论证不充分
- Paradigm模型不完整
- 关系类型判断错误

**快速诊断**：
```bash
python scripts/construct_paradigm.py --input relationships.json --validate
```

**详见**：`relationship-issues.md`

---

### 3. 技术问题
**常见症状**：
- 工具运行报错
- 输出格式问题
- 工具输出不合理

**快速诊断**：检查输入文件格式、依赖安装

**详见**：`technical-issues.md`

---

## 紧急救援（5分钟快速修复）

### 问题：范畴过于宽泛
```bash
# 快速修复：增加聚类数量
python scripts/identify_categories.py \
  --input codes.json \
  --output categories_v2.json \
  --n_categories 8  # 从5增加到8
```

### 问题：关系证据不足
```bash
# 快速修复：降低强度阈值，查看更多关系
python scripts/build_relationships.py \
  --input categories.json \
  --output relationships.json \
  --min_strength 0.3  # 从0.5降低到0.3
```

### 问题：Paradigm不完整
```bash
# 快速修复：使用自动补全
python scripts/construct_paradigm.py \
  --input relationships.json \
  --output paradigm.json \
  --auto_complete  # 自动补充缺失组件
```

---

## 预防性最佳实践

### 1. 定期备份
```bash
cp categories.json categories_backup_$(date +%Y%m%d).json
```

### 2. 版本控制
- categories_v1.json（工具初步输出）
- categories_v2.json（人工精炼后）
- categories_final.json（最终版本）

### 3. 撰写备忘录
记录每次重要决策和理由

### 4. 定期验证
每完成一个阶段，运行验证工具

---

## 学习路径

**快速修复**：根据诊断表直接跳转到相应章节

**系统学习**：
1. `category-issues.md`（范畴问题）
2. `relationship-issues.md`（关系问题）
3. `technical-issues.md`（技术问题）

**预防学习**：先阅读各子文档，了解常见问题

---

## 寻求帮助

如果以上方案都无法解决：
1. 查阅理论文献（Strauss & Corbin, 1998）
2. 咨询导师或同行
3. 回到原始数据重新分析
4. 考虑收集更多数据

---

*文档大小：约500字 | 阅读时间：2分钟*
