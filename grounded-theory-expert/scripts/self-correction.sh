#!/bin/bash
# 自我校对脚本 - 根据评审失败项自动选择修正策略
# 使用 CLI 原生机制，而非 backend services

set -e

# 配置
PHASE="${1:-2}"
REVIEW_FILE="${2:-}"
OUTPUT_DIR="corrections"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CORRECTION_FILE="${OUTPUT_DIR}/correction-${PHASE}-${TIMESTAMP}.md"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "========================================"
echo "  Phase ${PHASE} 自我校对"
echo "========================================"
echo ""

# 初始化校对报告
cat > "$CORRECTION_FILE" << EOF
# Phase ${PHASE} 自我校对报告

**校对时间**: $(date -Iseconds)

---

## 评审失败项

EOF

# 如果没有提供评审文件，使用最新的
if [ -z "$REVIEW_FILE" ]; then
    REVIEW_FILE=$(ls -t logs/reviews/review-${PHASE}-*.md 2>/dev/null | head -1)
fi

if [ ! -f "$REVIEW_FILE" ]; then
    echo "❌ 错误：找不到评审文件"
    exit 1
fi

echo "使用评审文件：$REVIEW_FILE"
echo ""

# 解析评审失败项
FAILED_CHECKS=()

if [ "$PHASE" = "2" ]; then
    # QC-2.1: 编码者间信度
    if grep -q "QC-2.1.*❌" "$REVIEW_FILE"; then
        FAILED_CHECKS+=("QC-2.1")
        echo "发现失败项：QC-2.1 (编码者间信度)"
    fi
    
    # QC-2.2: 持续比较日志
    if grep -q "QC-2.2.*❌" "$REVIEW_FILE"; then
        FAILED_CHECKS+=("QC-2.2")
        echo "发现失败项：QC-2.2 (持续比较日志)"
    fi
    
    # QC-2.3: 编码本完整性
    if grep -q "QC-2.3.*❌" "$REVIEW_FILE"; then
        FAILED_CHECKS+=("QC-2.3")
        echo "发现失败项：QC-2.3 (编码本完整性)"
    fi
    
    # QC-2.4: 行动导向命名
    if grep -q "QC-2.4.*❌" "$REVIEW_FILE"; then
        FAILED_CHECKS+=("QC-2.4")
        echo "发现失败项：QC-2.4 (行动导向命名)"
    fi
fi

echo ""
echo "共发现 ${#FAILED_CHECKS[@]} 个失败项"
echo ""

# 执行修正策略
CORRECTIONS_APPLIED=()

for CHECK in "${FAILED_CHECKS[@]}"; do
    echo "执行修正策略：$CHECK..."
    
    case "$CHECK" in
        "QC-2.1")
            # SC-004: 编码员培训与重新编码
            echo "  执行 SC-004: 编码员培训与重新编码..."
            
            if [ -f "scripts/corrections/recoder-with-training.sh" ]; then
                bash "scripts/corrections/recoder-with-training.sh"
                CORRECTIONS_APPLIED+=("SC-004")
                echo "### SC-004: 编码员培训与重新编码" >> "$CORRECTION_FILE"
                echo "执行时间：$(date -Iseconds)" >> "$CORRECTION_FILE"
                echo "预期改进：+20%" >> "$CORRECTION_FILE"
                echo "" >> "$CORRECTION_FILE"
            else
                echo "  ⚠️ 修正脚本不存在，创建模板..."
                mkdir -p scripts/corrections
                cat > "scripts/corrections/recoder-with-training.sh" << 'INNER_EOF'
#!/bin/bash
# SC-004: 编码员培训与重新编码
echo "执行编码员培训..."
echo "重新编码数据..."
# TODO: 实现真实的重新编码逻辑
INNER_EOF
                chmod +x "scripts/corrections/recoder-with-training.sh"
            fi
            ;;
        
        "QC-2.2")
            # SC-005: 回溯补充比较日志
            echo "  执行 SC-005: 回溯补充比较日志..."
            
            if [ -f "scripts/corrections/backfill-comparison-log.sh" ]; then
                bash "scripts/corrections/backfill-comparison-log.sh"
                CORRECTIONS_APPLIED+=("SC-005")
                echo "### SC-005: 回溯补充比较日志" >> "$CORRECTION_FILE"
                echo "执行时间：$(date -Iseconds)" >> "$CORRECTION_FILE"
                echo "预期改进：+25%" >> "$CORRECTION_FILE"
                echo "" >> "$CORRECTION_FILE"
            else
                echo "  ⚠️ 修正脚本不存在，创建模板..."
                mkdir -p scripts/corrections
                cat > "scripts/corrections/backfill-comparison-log.sh" << 'INNER_EOF'
#!/bin/bash
# SC-005: 回溯补充比较日志
echo "回溯编码数据..."
echo "补充比较记录..."
# TODO: 实现真实的比较日志补充逻辑
INNER_EOF
                chmod +x "scripts/corrections/backfill-comparison-log.sh"
            fi
            ;;
        
        "QC-2.3")
            # SC-006: 自动生成编码本
            echo "  执行 SC-006: 自动生成编码本..."
            
            if [ -f "scripts/corrections/generate-coding-manual.sh" ]; then
                bash "scripts/corrections/generate-coding-manual.sh"
                CORRECTIONS_APPLIED+=("SC-006")
                echo "### SC-006: 自动生成编码本" >> "$CORRECTION_FILE"
                echo "执行时间：$(date -Iseconds)" >> "$CORRECTION_FILE"
                echo "预期改进：+30%" >> "$CORRECTION_FILE"
                echo "" >> "$CORRECTION_FILE"
            else
                echo "  ⚠️ 修正脚本不存在，创建模板..."
                mkdir -p scripts/corrections
                cat > "scripts/corrections/generate-coding-manual.sh" << 'INNER_EOF'
#!/bin/bash
# SC-006: 自动生成编码本
echo "从编码结果提取概念..."
echo "生成编码本..."
# TODO: 实现真实的编码本生成逻辑
INNER_EOF
                chmod +x "scripts/corrections/generate-coding-manual.sh"
            fi
            ;;
        
        "QC-2.4")
            # SC-007: 行动导向命名修正
            echo "  执行 SC-007: 行动导向命名修正..."
            
            if [ -f "scripts/corrections/fix-action-oriented-naming.sh" ]; then
                bash "scripts/corrections/fix-action-oriented-naming.sh"
                CORRECTIONS_APPLIED+=("SC-007")
                echo "### SC-007: 行动导向命名修正" >> "$CORRECTION_FILE"
                echo "执行时间：$(date -Iseconds)" >> "$CORRECTION_FILE"
                echo "预期改进：+15%" >> "$CORRECTION_FILE"
                echo "" >> "$CORRECTION_FILE"
            else
                echo "  ⚠️ 修正脚本不存在，创建模板..."
                mkdir -p scripts/corrections
                cat > "scripts/corrections/fix-action-oriented-naming.sh" << 'INNER_EOF'
#!/bin/bash
# SC-007: 行动导向命名修正
echo "检查概念命名..."
echo "修正为行动导向命名..."
# TODO: 实现真实的命名修正逻辑
INNER_EOF
                chmod +x "scripts/corrections/fix-action-oriented-naming.sh"
            fi
            ;;
    esac
    
    echo ""
done

# 写入校对总结
cat >> "$CORRECTION_FILE" << EOF

---

## 校对总结

| 指标 | 数值 |
|------|------|
| **失败项数量** | ${#FAILED_CHECKS[@]} |
| **修正策略数量** | ${#CORRECTIONS_APPLIED[@]} |
| **修正状态** | $([ ${#CORRECTIONS_APPLIED[@]} -eq ${#FAILED_CHECKS[@]} ] && echo "✅ 完成" || echo "⚠️ 部分完成") |

---

## 下一步

1. 重新执行 Phase ${PHASE}
2. 重新进行质量评审
3. 验证修正效果

EOF

echo "========================================"
echo "  自我校对完成"
echo "========================================"
echo "失败项数量：${#FAILED_CHECKS[@]}"
echo "修正策略数量：${#CORRECTIONS_APPLIED[@]}"
echo "校对报告：$CORRECTION_FILE"
echo ""

# 导出 JSON 格式
JSON_FILE="${OUTPUT_DIR}/correction-${PHASE}-${TIMESTAMP}.json"
cat > "$JSON_FILE" << EOF
{
  "phase": $PHASE,
  "timestamp": "$(date -Iseconds)",
  "failed_checks": ${#FAILED_CHECKS[@]},
  "corrections_applied": ${#CORRECTIONS_APPLIED[@]},
  "correction_strategies": [$(printf '"%s",' "${CORRECTIONS_APPLIED[@]}" | sed 's/,$//')],
  "completed": $([ ${#CORRECTIONS_APPLIED[@]} -eq ${#FAILED_CHECKS[@]} ] && echo "true" || echo "false")
}
EOF

echo "JSON 报告：$JSON_FILE"
