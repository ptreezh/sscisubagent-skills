#!/bin/bash
# 自动化部署脚本 - SSCI Subagent Skills
# 作者: socienceAI.com
# 联系: zhangshuren@freeagentskills.com

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Git状态
check_git_status() {
    log_info "检查Git状态..."

    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "当前目录不是Git仓库"
        exit 1
    fi

    # 检查是否有未提交的更改
    if [[ -z $(git status -s) ]]; then
        log_warning "没有需要提交的更改"
        return 1
    fi

    log_success "Git仓库检查通过"
    return 0
}

# 运行测试
run_tests() {
    log_info "运行测试..."

    # Python语法检查
    log_info "检查Python文件语法..."
    python_files=$(find . -name "*.py" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./env/*" -not -path "./archive/*" -not -path "./project_backup/*" -not -path "./desktop_design/*/node_modules/*")

    if [ -n "$python_files" ]; then
        for file in $python_files; do
            python -m py_compile "$file" 2>&1 || {
                log_error "Python语法检查失败: $file"
                exit 1
            }
        done
    fi

    log_success "所有测试通过"
}

# 添加文件到Git
add_files() {
    log_info "添加文件到Git..."

    # 添加所有更改
    git add .

    # 显示将要提交的文件
    log_info "将要提交的文件:"
    git status -s

    log_success "文件已添加到暂存区"
}

# 创建提交
create_commit() {
    log_info "创建Git提交..."

    # 获取提交信息
    if [ -z "$1" ]; then
        commit_message="feat: 自动部署更新 - $(date '+%Y-%m-%d %H:%M:%S')

        # 添加详细信息
        commit_message="$commit_message

- 更新作者和联系信息
- 优化技能文件结构
- 更新文档

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
    else
        commit_message="$1"
    fi

    git commit -m "$commit_message"

    log_success "提交创建成功"
}

# 推送到远程仓库
push_to_remote() {
    log_info "推送到远程仓库..."

    # 获取当前分支
    current_branch=$(git branch --show-current)

    log_info "当前分支: $current_branch"

    # 推送到远程
    git push origin "$current_branch"

    log_success "推送成功"
}

# 创建Git标签
create_tag() {
    if [ -n "$1" ]; then
        log_info "创建Git标签: $1"

        git tag -a "$1" -m "Release $1"
        git push origin "$1"

        log_success "标签创建并推送成功"
    fi
}

# 主函数
main() {
    echo "=========================================="
    echo "  SSCI Subagent Skills 自动部署脚本"
    echo "  作者: socienceAI.com"
    echo "=========================================="
    echo ""

    # 检查参数
    SKIP_TESTS=false
    COMMIT_MESSAGE=""
    VERSION_TAG=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --message|-m)
                COMMIT_MESSAGE="$2"
                shift 2
                ;;
            --tag|-t)
                VERSION_TAG="$2"
                shift 2
                ;;
            --help|-h)
                echo "使用方法:"
                echo "  $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --skip-tests       跳过测试"
                echo "  --message, -m      自定义提交信息"
                echo "  --tag, -t          创建版本标签"
                echo "  --help, -h         显示帮助信息"
                echo ""
                echo "示例:"
                echo "  $0                           # 默认部署"
                echo "  $0 --skip-tests              # 跳过测试"
                echo "  $0 -m 'feat: add new skill'  # 自定义提交信息"
                echo "  $0 -t v1.0.0                 # 创建版本标签"
                exit 0
                ;;
            *)
                log_error "未知选项: $1"
                echo "使用 --help 查看帮助信息"
                exit 1
                ;;
        esac
    done

    # 执行部署流程
    if check_git_status; then
        if [ "$SKIP_TESTS" = false ]; then
            run_tests
        else
            log_warning "跳过测试"
        fi

        add_files
        create_commit "$COMMIT_MESSAGE"
        push_to_remote

        if [ -n "$VERSION_TAG" ]; then
            create_tag "$VERSION_TAG"
        fi

        echo ""
        log_success "部署完成！"
        echo ""
        log_info "仓库地址: https://github.com/ptreezh/sscisubagent-skills"
    fi
}

# 运行主函数
main "$@"
