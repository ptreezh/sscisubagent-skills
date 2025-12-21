import json
import tempfile
import os
from pathlib import Path

# 创建测试数据
stats_data = {
    "variable1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "variable2": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    "group": ["A", "A", "B", "B", "A", "B", "A", "B", "A", "B"]
}

# 创建临时输入文件
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
    json.dump(stats_data, f, ensure_ascii=False, indent=2)
    input_file = f.name

output_file = input_file.replace('.json', '_output.json')

print(f"Input file: {input_file}")
print(f"Output file: {output_file}")

# 执行分析
try:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(input_file))  # 切换到脚本目录
    
    # 直接调用函数而不是使用subprocess
    from advanced_statistical_analysis import main
    import sys
    import advanced_statistical_analysis
    
    # 保存原始的sys.argv
    original_argv = sys.argv
    
    # 设置参数
    sys.argv = [
        'advanced_statistical_analysis.py',
        '--input', input_file,
        '--output', output_file,
        '--analysis', 'descriptive',
        '--x-column', 'variable1'
    ]
    
    # 执行主函数
    advanced_statistical_analysis.main()
    
    # 恢复原始的sys.argv
    sys.argv = original_argv
    
    print("Analysis completed successfully")
    
    # 检查输出文件
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
            print(f"Output summary: {result['summary']}")
            print(f"Using advanced: {result['details'].get('using_advanced', 'N/A')}")
    else:
        print("Output file was not created")
        
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()

# 清理
if os.path.exists(input_file):
    os.unlink(input_file)
if os.path.exists(output_file):
    os.unlink(output_file)