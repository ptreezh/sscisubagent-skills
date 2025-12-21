---
name: processing-citations
description: 处理中文社会科学文献引用，包括GB/T 7714标准格式化、引用规范性检查、期刊格式适配和引用完整性验证。当需要格式化引用、检查引用规范或适配期刊特殊要求时使用此技能。
---

# 中文引用处理技能

专门处理中文社会科学文献引用的标准化和规范化工作，确保引用格式符合GB/T 7714-2015标准以及各类中文期刊的特殊要求。

## 核心能力

### 1. GB/T 7714标准格式化
- **标准格式识别**：自动识别文献类型并应用对应格式
- **字段完整性检查**：确保必要引用信息的完整性
- **标点符号规范**：严格按照标准使用标点符号
- **作者姓名格式**：中文作者姓名的标准格式处理
- **期刊信息规范**：期刊名称、卷期、页码的标准表示

### 2. 期刊特殊格式适配
- **CSSCI期刊格式**：中文社会科学引文索引期刊格式要求
- **北大核心期刊**：北京大学核心期刊目录期刊格式
- **高校学报格式**：各高校学报的特殊格式要求
- **专业学会期刊**：各专业学会期刊的格式规范
- **国际期刊中文引用**：英文期刊的中文引用格式

### 3. 引用规范性验证
- **格式一致性检查**：全文引用格式的一致性验证
- **信息准确性验证**：引用信息的准确性检查
- **重复引用检测**：重复引用的识别和处理
- **缺失信息补充**：自动补充缺失的引用信息
- **过时引用识别**：识别和标记过时的引用

## 处理流程

### 第一步：引用信息提取
```bash
# 从文档中提取引用信息
grep -n "\[[0-9]\+\]" document.md
# 提取参考文献列表
sed -n '/参考文献/,$p' document.md
```

### 第二步：文献类型识别
**期刊论文识别模式**：
- 正则表达式：`作者\.题名\[J\]\.刊名,年,卷\(期\):起止页码\.`
- 关键特征：包含[J]标识，有刊名、年份、卷期信息

**图书识别模式**：
- 正则表达式：`作者\.书名\[M\]\.出版地:出版社,出版年\.`
- 关键特征：包含[M]标识，有出版地和出版社信息

**学位论文识别模式**：
- 正则表达式：`作者\.题名\[D\]\.保存地:保存单位,年份\.`
- 关键特征：包含[D]标识，有保存单位和年份

### 第三步：格式标准化处理
**标准化处理脚本**：
```javascript
// 引用格式标准化处理
function standardizeCitation(citation) {
    // 1. 清理多余空格
    citation = citation.replace(/\s+/g, ' ').trim();
    
    // 2. 标准化标点符号
    citation = citation.replace(/，/g, ',');
    citation = citation.replace(/：/g, ':');
    citation = citation.replace(/；/g, ';');
    
    // 3. 检查作者姓名格式
    citation = formatAuthorNames(citation);
    
    // 4. 验证必要字段
    citation = validateRequiredFields(citation);
    
    return citation;
}
```

### 第四步：期刊格式适配
**CSSCI期刊格式适配**：
```javascript
// CSSCI期刊格式特殊处理
function adaptToCSSCI(journalName, citation) {
    const cssciRules = {
        '社会学研究': {
            'authorFormat': 'fullName',
            'titleFormat': 'quotes',
            'journalFormat': 'full'
        },
        '社会': {
            'authorFormat': 'lastNameFirst',
            'titleFormat': 'noQuotes',
            'journalFormat': 'abbreviated'
        }
    };
    
    const rules = cssciRules[journalName];
    if (rules) {
        return applyJournalRules(citation, rules);
    }
    return citation;
}
```

### 第五步：质量验证检查
**质量检查清单**：
```bash
# 检查引用格式完整性
echo "检查项目："
echo "1. 作者姓名格式是否正确"
echo "2. 文献类型标识是否准确"
echo "3. 标点符号使用是否规范"
echo "4. 必要信息是否完整"
echo "5. 格式是否全文一致"
```

## 工具集成

### Python处理脚本
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
from typing import Dict, List, Tuple

class CitationProcessor:
    def __init__(self):
        self.citation_patterns = {
            'journal': r'(.+?)\.(.+?)\[J\]\.(.+?),(\d+),(\d+)\((\d+)\):(\d+)-(\d+)\.',
            'book': r'(.+?)\.(.+?)\[M\]\.(.+?):(.+?),(\d+)\.',
            'thesis': r'(.+?)\.(.+?)\[D\]\.(.+?):(.+?),(\d+)\.'
        }
        
    def extract_citations(self, document: str) -> List[str]:
        """从文档中提取引用列表"""
        # 提取文内引用
        in_text_citations = re.findall(r'\[(\d+)\]', document)
        
        # 提取参考文献列表
        ref_section = re.search(r'参考文献[\s\S]*', document)
        if ref_section:
            references = re.findall(r'\d+\..+', ref_section.group())
            return references
        return []
    
    def validate_citation_format(self, citation: str) -> Dict[str, any]:
        """验证引用格式规范性"""
        result = {
            'is_valid': False,
            'citation_type': None,
            'errors': [],
            'suggestions': []
        }
        
        for citation_type, pattern in self.citation_patterns.items():
            match = re.match(pattern, citation)
            if match:
                result['is_valid'] = True
                result['citation_type'] = citation_type
                
                # 检查各字段格式
                self.check_author_format(match.group(1), result)
                self.check_title_format(match.group(2), result)
                self.check_punctuation(citation, result)
                
                break
        
        if not result['is_valid']:
            result['errors'].append('引用格式不符合GB/T 7714标准')
            result['suggestions'].append('请参考标准格式重新格式化')
        
        return result
    
    def check_author_format(self, authors: str, result: Dict):
        """检查作者姓名格式"""
        if len(authors) > 50:
            result['errors'].append('作者姓名过长')
        
        # 检查中文作者姓名格式
        chinese_pattern = r'^[\u4e00-\u9fa5]+(,[\u4e00-\u9fa5]+)*$'
        if not re.match(chinese_pattern, authors):
            result['errors'].append('中文作者姓名格式不正确')
            result['suggestions'].append('作者姓名应为中文，多个作者用逗号分隔')
    
    def generate_standard_citation(self, metadata: Dict) -> str:
        """生成标准格式的引用"""
        citation_type = metadata.get('type', 'journal')
        
        if citation_type == 'journal':
            return f"{metadata['author']}.{metadata['title']}[J].{metadata['journal']},{metadata['year']},{metadata['volume']}({metadata['issue']}):{metadata['pages']}."
        elif citation_type == 'book':
            return f"{metadata['author']}.{metadata['title']}[M].{metadata['location']}:{metadata['publisher']},{metadata['year']}."
        elif citation_type == 'thesis':
            return f"{metadata['author']}.{metadata['title']}[D].{metadata['location']}:{metadata['institution']},{metadata['year']}."
        
        return ""

# 使用示例
if __name__ == "__main__":
    processor = CitationProcessor()
    
    # 示例引用
    citation = "张三.数字鸿沟研究[J].社会学研究,2023,38(2):123-145."
    
    # 验证格式
    result = processor.validate_citation_format(citation)
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

### Node.js处理脚本
```javascript
#!/usr/bin/env node
import { readFile, writeFile } from 'fs/promises';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

class CitationFormatter {
    constructor() {
        this.gbT7714Rules = {
            journal: {
                pattern: /^(.+?)\.(.+?)\[J\]\.(.+?),(\d+),(\d+)\((\d+)\):(\d+)-(\d+)\.$/,
                format: '{author}.{title}[J].{journal},{year},{volume}({issue}):{pages}.'
            },
            book: {
                pattern: /^(.+?)\.(.+?)\[M\]\.(.+?):(.+?),(\d+)\.$/,
                format: '{author}.{title}[M].{location}:{publisher},{year}.'
            }
        };
    }
    
    async processDocument(filePath) {
        try {
            const content = await readFile(filePath, 'utf-8');
            const citations = this.extractCitations(content);
            const processedCitations = [];
            
            for (const citation of citations) {
                const validated = this.validateCitation(citation);
                if (validated.isValid) {
                    processedCitations.push(this.standardizeCitation(citation));
                } else {
                    console.warn(`引用格式有问题: ${citation}`);
                    console.warn(`错误信息: ${validated.errors.join(', ')}`);
                }
            }
            
            return {
                original: citations,
                processed: processedCitations,
                errors: citations.filter(c => !this.validateCitation(c).isValid)
            };
        } catch (error) {
            console.error('处理文档时出错:', error);
            throw error;
        }
    }
    
    extractCitations(content) {
        // 提取参考文献部分
        const refMatch = content.match(/参考文献[\s\S]*/);
        if (!refMatch) return [];
        
        const refSection = refMatch[0];
        const citations = refSection.match(/\d+\..+/g) || [];
        
        return citations.map(citation => citation.trim());
    }
    
    validateCitation(citation) {
        for (const [type, rule] of Object.entries(this.gbT7714Rules)) {
            if (rule.pattern.test(citation)) {
                return {
                    isValid: true,
                    type: type,
                    matches: citation.match(rule.pattern)
                };
            }
        }
        
        return {
            isValid: false,
            errors: ['不符合GB/T 7714标准格式']
        };
    }
    
    standardizeCitation(citation) {
        // 标准化处理：清理空格、统一标点等
        return citation
            .replace(/\s+/g, ' ')
            .replace(/，/g, ',')
            .replace(/：/g, ':')
            .replace(/；/g, ';')
            .trim();
    }
}

// CLI使用
const formatter = new CitationFormatter();

// 处理命令行参数
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log('使用方法: node process-citations.js <文档文件路径>');
    process.exit(1);
}

const filePath = args[0];
formatter.processDocument(filePath)
    .then(result => {
        console.log('处理结果:');
        console.log(`原始引用数量: ${result.original.length}`);
        console.log(`成功处理: ${result.processed.length}`);
        console.log(`格式错误: ${result.errors.length}`);
        
        if (result.errors.length > 0) {
            console.log('\n格式错误的引用:');
            result.errors.forEach(error => console.log(`- ${error}`));
        }
        
        console.log('\n处理后的引用:');
        result.processed.forEach(citation => console.log(citation));
    })
    .catch(error => {
        console.error('处理失败:', error);
        process.exit(1);
    });
```

## 质量保证

### 验证检查清单
- [ ] 所有引用都符合GB/T 7714-2015标准
- [ ] 作者姓名格式正确且完整
- [ ] 文献类型标识准确无误
- [ ] 标点符号使用规范统一
- [ ] 必要引用信息完整无缺
- [ ] 全文引用格式保持一致
- [ ] 期刊特殊要求得到满足
- [ ] 重复引用已适当处理
- [ ] 过时引用已标记提醒
- [ ] 引用与正文对应正确

### 错误处理机制
**常见错误类型**：
1. **作者姓名格式错误**：中文作者姓名应为全名，英文作者应姓前名后
2. **文献类型标识错误**：[J]、[M]、[D]等标识使用不当
3. **标点符号不规范**：中英文标点混用，标点位置错误
4. **信息缺失**：缺少必要的时间、页码、出版地等信息
5. **格式不一致**：同类文献的格式表示不统一

**自动修复策略**：
- 标点符号自动替换
- 常见格式模式自动识别
- 缺失信息提示补充
- 重复引用自动合并

---

**此引用处理技能专门为中文社会科学研究者设计，确保引用格式的标准化和规范化，提升学术写作的专业性和规范性。**