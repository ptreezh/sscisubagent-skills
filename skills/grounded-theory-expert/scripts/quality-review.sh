#!/bin/bash
# 质量评审脚本 - 基于 Strauss & Corbin (1990), Charmaz (2006) 规范
# 使用 CLI 原生机制，而非 backend services

set -e

# 配置
PHASE="${1:-2}"  # 默认 Phase 2
OUTPUT_DIR="logs/reviews"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REVIEW_FILE="${OUTPUT_DIR}/review-${PHASE}-${TIMESTAMP}.md"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "========================================"
echo "  Phase ${PHASE} 质量评审"
echo "========================================"
echo ""

# 初始化评审报告
cat > "$REVIEW_FILE" << EOF
# Phase ${PHASE} 质量评审报告

**评审时间**: $(date -Iseconds)
**评审标准**: Strauss & Corbin (1990), Charmaz (2006)

---

## 评审结果

EOF

# 评审得分
TOTAL_SCORE=0
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Phase 2 开放编码评审标准
if [ "$PHASE" = "2" ]; then
    echo "评审 Phase 2: 开放性编码..."
    echo ""
    
    # QC-2.1: 编码者间信度
    echo "检查 QC-2.1: 编码者间信度..."
    if [ -f "results/coding_reliability.json" ]; then
        KAPPA=$(jq -r '.kappa' results/coding_reliability.json)
        if (( $(echo "$KAPPA >= 0.70" | bc -l) )); then
            echo "  ✅ 通过 (Kappa = $KAPPA)"
            echo "### QC-2.1: 编码者间信度 ✅ 通过" >> "$REVIEW_FILE"
            echo "Kappa = $KAPPA (> 0.70)" >> "$REVIEW_FILE"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            TOTAL_SCORE=$((TOTAL_SCORE + 25))
        else
            echo "  ❌ 失败 (Kappa = $KAPPA < 0.70)"
            echo "### QC-2.1: 编码者间信度 ❌ 失败" >> "$REVIEW_FILE"
            echo "Kappa = $KAPPA (< 0.70)" >> "$REVIEW_FILE"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
        fi
    else
        echo "  ❌ 失败 (文件不存在)"
        echo "### QC-2.1: 编码者间信度 ❌ 失败" >> "$REVIEW_FILE"
        echo "文件不存在：results/coding_reliability.json" >> "$REVIEW_FILE"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    # QC-2.2: 持续比较日志
    echo "检查 QC-2.2: 持续比较日志..."
    if [ -f "coding-results/constant_comparison_log.md" ]; then
        LOG_ENTRIES=$(grep -c "^## 比较记录" coding-results/constant_comparison_log.md || echo "0")
        if [ "$LOG_ENTRIES" -ge 20 ]; then
            echo "  ✅ 通过 (比较记录 = $LOG_ENTRIES)"
            echo "### QC-2.2: 持续比较日志 ✅ 通过" >> "$REVIEW_FILE"
            echo "比较记录 = $LOG_ENTRIES (≥ 20)" >> "$REVIEW_FILE"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            TOTAL_SCORE=$((TOTAL_SCORE + 25))
        else
            echo "  ❌ 失败 (比较记录 = $LOG_ENTRIES < 20)"
            echo "### QC-2.2: 持续比较日志 ❌ 失败" >> "$REVIEW_FILE"
            echo "比较记录 = $LOG_ENTRIES (< 20)" >> "$REVIEW_FILE"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
        fi
    else
        echo "  ❌ 失败 (文件不存在)"
        echo "### QC-2.2: 持续比较日志 ❌ 失败" >> "$REVIEW_FILE"
        echo "文件不存在：coding-results/constant_comparison_log.md" >> "$REVIEW_FILE"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    # QC-2.3: 编码本完整性
    echo "检查 QC-2.3: 编码本完整性..."
    if [ -f "coding-results/coding_manual.md" ]; then
        CONCEPT_COUNT=$(grep -c "^### 概念" coding-results/coding_manual.md || echo "0")
        if [ "$CONCEPT_COUNT" -ge 30 ]; then
            echo "  ✅ 通过 (概念数 = $CONCEPT_COUNT)"
            echo "### QC-2.3: 编码本完整性 ✅ 通过" >> "$REVIEW_FILE"
            echo "概念数 = $CONCEPT_COUNT (≥ 30)" >> "$REVIEW_FILE"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            TOTAL_SCORE=$((TOTAL_SCORE + 25))
        else
            echo "  ❌ 失败 (概念数 = $CONCEPT_COUNT < 30)"
            echo "### QC-2.3: 编码本完整性 ❌ 失败" >> "$REVIEW_FILE"
            echo "概念数 = $CONCEPT_COUNT (< 30)" >> "$REVIEW_FILE"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
        fi
    else
        echo "  ❌ 失败 (文件不存在)"
        echo "### QC-2.3: 编码本完整性 ❌ 失败" >> "$REVIEW_FILE"
        echo "文件不存在：coding-results/coding_manual.md" >> "$REVIEW_FILE"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    # QC-2.4: 行动导向命名
    echo "检查 QC-2.4: 行动导向命名..."
    if [ -f "coding-results/open_coding_results.json" ]; then
        ACTION_ORIENTED=$(jq -r '.action_oriented_percentage' coding-results/open_coding_results.json)
        if (( $(echo "$ACTION_ORIENTED >= 80" | bc -l) )); then
            echo "  ✅ 通过 (行动导向 = $ACTION_ORIENTED%)"
            echo "### QC-2.4: 行动导向命名 ✅ 通过" >> "$REVIEW_FILE"
            echo "行动导向 = $ACTION_ORIENTED% (≥ 80%)" >> "$REVIEW_FILE"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            TOTAL_SCORE=$((TOTAL_SCORE + 25))
        else
            echo "  ❌ 失败 (行动导向 = $ACTION_ORIENTED% < 80%)"
            echo "### QC-2.4: 行动导向命名 ❌ 失败" >> "$REVIEW_FILE"
            echo "行动导向 = $ACTION_ORIENTED% (< 80%)" >> "$REVIEW_FILE"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
        fi
    else
        echo "  ❌ 失败 (文件不存在)"
        echo "### QC-2.4: 行动导向命名 ❌ 失败" >> "$REVIEW_FILE"
        echo "文件不存在：coding-results/open_coding_results.json" >> "$REVIEW_FILE"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
fi

# 计算最终得分
if [ "$TOTAL_CHECKS" -gt 0 ]; then
    FINAL_SCORE=$((TOTAL_SCORE / TOTAL_CHECKS * 4))  # 归一化到 100
else
    FINAL_SCORE=0
fi

# 判断是否通过
if [ "$FINAL_SCORE" -ge 85 ]; then
    PASSED=true
    STATUS="✅ 通过"
else
    PASSED=false
    STATUS="❌ 失败"
fi

# 写入评审总结
cat >> "$REVIEW_FILE" << EOF

---

## 评审总结

| 指标 | 数值 |
|------|------|
| **总检查项** | $TOTAL_CHECKS |
| **通过** | $PASSED_CHECKS ✅ |
| **失败** | $FAILED_CHECKS ❌ |
| **通过率** | $(echo "scale=1; $PASSED_CHECKS * 100 / $TOTAL_CHECKS" | bc)% |
| **最终得分** | $FINAL_SCORE / 100 |
| **评审状态** | $STATUS |
| **收敛阈值** | 85 |
| **是否收敛** | $([ "$FINAL_SCORE" -ge 85 ] && echo "✅ 是" || echo "❌ 否") |

---

## 下一步

EOF

if [ "$PASSED" = true ]; then
    echo "✅ 评审通过，可以进入下一 Phase" >> "$REVIEW_FILE"
    echo "✅ 评审通过，可以进入下一 Phase"
else
    echo "❌ 评审失败，需要自我校对并重新迭代" >> "$REVIEW_FILE"
    echo "❌ 评审失败，需要自我校对并重新迭代"
    echo "" >> "$REVIEW_FILE"
    echo "### 需要修正的问题:" >> "$REVIEW_FILE"
    
    # 列出失败项
    if [ "$PHASE" = "2" ]; then
        [ ! -f "results/coding_reliability.json" ] || [ $(jq -r '.kappa' results/coding_reliability.json) \< 0.70 ] = true ] && echo "- [ ] QC-2.1: 编码者间信度" >> "$REVIEW_FILE"
        [ ! -f "coding-results/constant_comparison_log.md" ] || [ $(grep -c "^## 比较记录" coding-results/constant_comparison_log.md) -lt 20 ] && echo "- [ ] QC-2.2: 持续比较日志" >> "$REVIEW_FILE"
        [ ! -f "coding-results/coding_manual.md" ] || [ $(grep -c "^### 概念" coding-results/coding_manual.md) -lt 30 ] && echo "- [ ] QC-2.3: 编码本完整性" >> "$REVIEW_FILE"
        [ ! -f "coding-results/open_coding_results.json" ] || [ $(jq -r '.action_oriented_percentage' coding-results/open_coding_results.json) -lt 80 ] && echo "- [ ] QC-2.4: 行动导向命名" >> "$REVIEW_FILE"
    fi
fi

echo ""
echo "========================================"
echo "  评审完成"
echo "========================================"
echo "总检查项：$TOTAL_CHECKS"
echo "通过：$PASSED_CHECKS ✅"
echo "失败：$FAILED_CHECKS ❌"
echo "最终得分：$FINAL_SCORE / 100"
echo "评审状态：$STATUS"
echo "评审报告：$REVIEW_FILE"
echo ""

# 导出 JSON 格式
JSON_FILE="${OUTPUT_DIR}/review-${PHASE}-${TIMESTAMP}.json"
cat > "$JSON_FILE" << EOF
{
  "phase": $PHASE,
  "timestamp": "$(date -Iseconds)",
  "total_checks": $TOTAL_CHECKS,
  "passed_checks": $PASSED_CHECKS,
  "failed_checks": $FAILED_CHECKS,
  "pass_rate": $(echo "scale=2; $PASSED_CHECKS * 100 / $TOTAL_CHECKS" | bc),
  "final_score": $FINAL_SCORE,
  "passed": $PASSED,
  "convergence_threshold": 85,
  "converged": $([ "$FINAL_SCORE" -ge 85 ] && echo "true" || echo "false")
}
EOF

echo "JSON 报告：$JSON_FILE"

# 返回状态码
if [ "$PASSED" = true ]; then
    exit 0
else
    exit 1
fi
