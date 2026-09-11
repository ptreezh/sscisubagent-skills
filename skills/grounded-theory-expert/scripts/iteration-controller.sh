#!/bin/bash
# 迭代控制器 - 管理完整的迭代循环
# 使用 CLI 原生机制，而非 backend services

set -e

# 配置
PHASE="${1:-2}"
MAX_ITERATIONS="${2:-10}"
CONVERGENCE_THRESHOLD="${3:-85}"
MIN_IMPROVEMENT="${4:-5}"

OUTPUT_DIR="logs/iterations"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ITERATION_LOG="${OUTPUT_DIR}/iteration-log-${PHASE}-${TIMESTAMP}.md"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "========================================"
echo "  Phase ${PHASE} 迭代循环"
echo "========================================"
echo ""
echo "配置:"
echo "  最大迭代次数：$MAX_ITERATIONS"
echo "  收敛阈值：$CONVERGENCE_THRESHOLD%"
echo "  最小改进：$MIN_IMPROVEMENT%"
echo ""

# 初始化迭代日志
cat > "$ITERATION_LOG" << EOF
# Phase ${PHASE} 迭代日志

**开始时间**: $(date -Iseconds)
**配置**:
  - 最大迭代次数：$MAX_ITERATIONS
  - 收敛阈值：$CONVERGENCE_THRESHOLD%
  - 最小改进：$MIN_IMPROVEMENT%

---

## 迭代记录

EOF

# 迭代状态
PREV_SCORE=0
BEST_SCORE=0
CONVERGED=false
STAGNATION_COUNT=0
MAX_STAGNATION=3  # 连续 3 次改进<MIN_IMPROVEMENT 则提前停止

# 迭代循环
for ((ITERATION=1; ITERATION<=MAX_ITERATIONS; ITERATION++)); do
    echo ""
    echo "========================================"
    echo "  迭代 #$ITERATION"
    echo "========================================"
    echo ""
    
    # 1. 执行 Phase
    echo "1. 执行 Phase ${PHASE}..."
    if [ -f "scripts/execute-phase-${PHASE}.sh" ]; then
        bash "scripts/execute-phase-${PHASE}.sh" "$ITERATION"
    else
        echo "  ⚠️ Phase 执行脚本不存在，使用模拟执行..."
        sleep 2
    fi
    
    # 2. 自主反思
    echo ""
    echo "2. 自主反思..."
    if [ -f "scripts/self-reflect.sh" ]; then
        bash "scripts/self-reflect.sh" "$PHASE" "$ITERATION"
    else
        echo "  ⚠️ 反思脚本不存在，跳过..."
    fi
    
    # 3. 质量评审
    echo ""
    echo "3. 质量评审..."
    set +e  # 允许评审失败
    bash "scripts/quality-review.sh" "$PHASE"
    REVIEW_EXIT_CODE=$?
    set -e
    
    # 解析评审结果
    LATEST_REVIEW=$(ls -t logs/reviews/review-${PHASE}-*.md 2>/dev/null | head -1)
    if [ -f "$LATEST_REVIEW" ]; then
        CURRENT_SCORE=$(grep "最终得分" "$LATEST_REVIEW" | awk '{print $3}' | cut -d'/' -f1)
        [ -z "$CURRENT_SCORE" ] && CURRENT_SCORE=0
    else
        CURRENT_SCORE=0
    fi
    
    echo "  当前得分：$CURRENT_SCORE%"
    
    # 4. 检查是否收敛
    echo ""
    echo "4. 检查收敛..."
    
    if [ "$CURRENT_SCORE" -ge "$CONVERGENCE_THRESHOLD" ]; then
        echo "  ✅ 收敛！得分 $CURRENT_SCORE% ≥ $CONVERGENCE_THRESHOLD%"
        CONVERGED=true
        
        # 写入迭代日志
        cat >> "$ITERATION_LOG" << EOF

### 迭代 #$ITERATION

**状态**: ✅ 收敛
**得分**: $CURRENT_SCORE% / $CONVERGENCE_THRESHOLD%
**改进**: $((CURRENT_SCORE - PREV_SCORE))%

**结论**: Phase ${PHASE} 迭代收敛，符合方法论规范！

EOF
        break
    fi
    
    # 检查改进幅度
    IMPROVEMENT=$((CURRENT_SCORE - PREV_SCORE))
    
    if [ "$IMPROVEMENT" -lt "$MIN_IMPROVEMENT" ]; then
        STAGNATION_COUNT=$((STAGNATION_COUNT + 1))
        echo "  ⚠️ 改进放缓 ($IMPROVEMENT% < $MIN_IMPROVEMENT%)，停滞计数：$STAGNATION_COUNT"
        
        if [ "$STAGNATION_COUNT" -ge "$MAX_STAGNATION" ]; then
            echo "  ⚠️ 连续 $MAX_STAGNATION 次改进 < $MIN_IMPROVEMENT%，提前停止迭代"
            
            # 写入迭代日志
            cat >> "$ITERATION_LOG" << EOF

### 迭代 #$ITERATION

**状态**: ⚠️ 提前停止
**得分**: $CURRENT_SCORE% / $CONVERGENCE_THRESHOLD%
**改进**: $IMPROVEMENT%
**停滞计数**: $STAGNATION_COUNT

**结论**: 连续 $MAX_STAGNATION 次改进 < $MIN_IMPROVEMENT%，提前停止迭代。需要人工干预。

EOF
            break
        fi
    else
        STAGNATION_COUNT=0
        echo "  ✅ 改进 $IMPROVEMENT%"
    fi
    
    # 5. 自我校对（如果评审失败）
    if [ "$REVIEW_EXIT_CODE" -ne 0 ]; then
        echo ""
        echo "5. 自我校对..."
        bash "scripts/self-correction.sh" "$PHASE" "$LATEST_REVIEW"
    fi
    
    # 更新状态
    [ "$CURRENT_SCORE" -gt "$BEST_SCORE" ] && BEST_SCORE=$CURRENT_SCORE
    PREV_SCORE=$CURRENT_SCORE
    
    # 写入迭代日志
    cat >> "$ITERATION_LOG" << EOF

### 迭代 #$ITERATION

**状态**: 🔄 继续
**得分**: $CURRENT_SCORE% / $CONVERGENCE_THRESHOLD%
**改进**: $IMPROVEMENT%
**停滞计数**: $STAGNATION_COUNT

EOF
done

# 生成最终报告
echo ""
echo "========================================"
echo "  迭代循环完成"
echo "========================================"
echo ""

if [ "$CONVERGED" = true ]; then
    echo "✅ Phase ${PHASE} 收敛，最终得分：$BEST_SCORE%"
    FINAL_STATUS="✅ 收敛"
elif [ "$BEST_SCORE" -ge "$CONVERGENCE_THRESHOLD" ]; then
    echo "✅ Phase ${PHASE} 达到收敛标准，最终得分：$BEST_SCORE%"
    FINAL_STATUS="✅ 达到标准"
else
    echo "⚠️ Phase ${PHASE} 未收敛，最佳得分：$BEST_SCORE%"
    FINAL_STATUS="⚠️ 未收敛"
fi

# 写入最终报告
cat >> "$ITERATION_LOG" << EOF

---

## 最终报告

| 指标 | 数值 |
|------|------|
| **迭代次数** | $ITERATION |
| **最佳得分** | $BEST_SCORE% |
| **收敛阈值** | $CONVERGENCE_THRESHOLD% |
| **最终状态** | $FINAL_STATUS |
| **是否符合方法论规范** | $([ "$BEST_SCORE" -ge "$CONVERGENCE_THRESHOLD" ] && echo "✅ 是" || echo "❌ 否") |

---

## 下一步

EOF

if [ "$CONVERGED" = true ] || [ "$BEST_SCORE" -ge "$CONVERGENCE_THRESHOLD" ]; then
    echo "1. 进入 Phase $((PHASE + 1))" >> "$ITERATION_LOG"
    echo "✅ 可以进入下一 Phase"
else
    echo "1. 分析迭代失败原因" >> "$ITERATION_LOG"
    echo "2. 调整参数（增加最大迭代次数、优化修正策略）" >> "$ITERATION_LOG"
    echo "3. 重新执行迭代循环" >> "$ITERATION_LOG"
    echo "⚠️ 需要人工干预"
fi

echo ""
echo "迭代日志：$ITERATION_LOG"

# 导出 JSON 格式
JSON_FILE="${OUTPUT_DIR}/iteration-log-${PHASE}-${TIMESTAMP}.json"
cat > "$JSON_FILE" << EOF
{
  "phase": $PHASE,
  "start_timestamp": "$(date -Iseconds)",
  "iterations": $ITERATION,
  "best_score": $BEST_SCORE,
  "convergence_threshold": $CONVERGENCE_THRESHOLD,
  "converged": $([ "$BEST_SCORE" -ge "$CONVERGENCE_THRESHOLD" ] && echo "true" || echo "false"),
  "final_status": "$FINAL_STATUS",
  "meets_standards": $([ "$BEST_SCORE" -ge "$CONVERGENCE_THRESHOLD" ] && echo "true" || echo "false")
}
EOF

echo "JSON 报告：$JSON_FILE"

# 返回状态码
if [ "$BEST_SCORE" -ge "$CONVERGENCE_THRESHOLD" ]; then
    exit 0
else
    exit 1
fi
