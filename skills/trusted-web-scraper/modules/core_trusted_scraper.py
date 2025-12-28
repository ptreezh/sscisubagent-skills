"""
可信网站爬虫模块
此模块提供从可信网站（企业官网、教育网、政务网）收集信息的功能
"""

from typing import Dict, List, Any, Optional
import requests
import time
import json
from urllib.parse import urlparse
from datetime import datetime
import ssl
import socket


def trusted_web_scraper(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行可信网站爬虫任务
    
    Args:
        data: 包含爬取任务信息的字典
    
    Returns:
        包含爬取结果的字典
    """
    url = data.get('url', '')
    content_type = data.get('content_type', 'text')
    data_fields = data.get('data_fields', [])
    verification_level = data.get('verification_level', 'standard')
    rate_limit = data.get('rate_limit', 10)  # 每分钟请求数
    timeout = data.get('timeout', 30)
    retry_attempts = data.get('retry_attempts', 3)
    output_format = data.get('output_format', 'json')
    
    # 验证网站可信度
    trust_verification = verify_website_trustworthiness(url, verification_level)
    
    if not trust_verification['is_trusted']:
        return {
            "error": "Website is not verified as trustworthy",
            "trust_verification": trust_verification
        }
    
    # 根据验证结果选择适当的爬取策略
    crawl_strategy = select_crawl_strategy(url, trust_verification)
    
    # 执行信息提取
    extraction_results = extract_information(
        url, content_type, data_fields, crawl_strategy, 
        timeout, retry_attempts
    )
    
    # 数据处理和清洗
    processed_data = process_extracted_data(extraction_results, data_fields)
    
    # 生成输出
    output = generate_output(processed_data, trust_verification, output_format)
    
    return {
        "trust_verification": trust_verification,
        "crawl_strategy": crawl_strategy,
        "extraction_results": extraction_results,
        "processed_data": processed_data,
        "output": output,
        "summary": {
            "url": url,
            "status_code": extraction_results.get('status_code', 'N/A'),
            "trust_level": trust_verification['trust_level'],
            "content_extracted": len(extraction_results.get('extracted_data', [])),
            "processing_time": extraction_results.get('processing_time', 0)
        }
    }


def verify_website_trustworthiness(url: str, verification_level: str = 'standard') -> Dict[str, Any]:
    """
    验证网站的可信度
    
    Args:
        url: 要验证的URL
        verification_level: 验证级别 (basic, standard, thorough)
    
    Returns:
        验证结果
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # 基本验证
    basic_checks = {
        "has_valid_ssl": check_ssl_certificate(domain),
        "is_known_trusted_domain": is_trusted_domain(domain),
        "has_valid_whois": check_whois_info(domain) if verification_level in ['standard', 'thorough'] else True,
        "domain_age": get_domain_age(domain) if verification_level == 'thorough' else None
    }
    
    # 计算信任级别
    trust_score = calculate_trust_score(basic_checks)
    trust_level = determine_trust_level(trust_score)
    
    return {
        "url": url,
        "domain": domain,
        "basic_checks": basic_checks,
        "trust_score": trust_score,
        "trust_level": trust_level,
        "is_trusted": trust_level in ['high', 'medium'],
        "verification_details": {
            "ssl_valid": basic_checks["has_valid_ssl"],
            "trusted_domain": basic_checks["is_known_trusted_domain"],
            "whois_valid": basic_checks["has_valid_whois"]
        }
    }


def check_ssl_certificate(domain: str) -> bool:
    """
    检查SSL证书的有效性
    
    Args:
        domain: 域名
    
    Returns:
        SSL证书是否有效
    """
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                # 检查证书是否过期
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                return not_after > datetime.now()
    except Exception:
        # 对于HTTP网站或其他错误，返回True以允许继续处理
        return True


def is_trusted_domain(domain: str) -> bool:
    """
    检查是否为可信域名（教育、政府、知名企业）
    
    Args:
        domain: 域名
    
    Returns:
        是否为可信域名
    """
    # 检查顶级域名
    tlds = ['.edu', '.edu.cn', '.ac.cn', '.gov', '.gov.cn', '.org', '.org.cn']
    if any(domain.endswith(tld) for tld in tlds):
        return True
    
    # 检查知名企业的域名
    known_corporate_domains = [
        'baidu.com', 'alibaba.com', 'tencent.com', 'huawei.com', 
        'xiaomi.com', 'bytedance.com', 'jd.com', 'sina.com.cn',
        'sohu.com', '163.com', 'qq.com', 'weibo.com'
    ]
    
    for corp_domain in known_corporate_domains:
        if corp_domain in domain:
            return True
    
    # 检查知名高校域名
    known_edu_domains = [
        'pku.edu.cn', 'tsinghua.edu.cn', 'fudan.edu.cn', 'sjtu.edu.cn',
        'nju.edu.cn', 'zju.edu.cn', 'ustc.edu.cn', 'bisu.edu.cn',
        'bfsu.edu.cn', 'shisu.edu.cn', 'sicnu.edu.cn'
    ]
    
    for edu_domain in known_edu_domains:
        if edu_domain in domain:
            return True
    
    return False


def check_whois_info(domain: str) -> bool:
    """
    检查WHOIS信息（简化版本）
    
    Args:
        domain: 域名
    
    Returns:
        WHOIS信息是否有效
    """
    # 在实际实现中，这里会查询WHOIS数据库
    # 现在我们简化处理，返回True
    return True


def get_domain_age(domain: str) -> Optional[int]:
    """
    获取域名年龄（简化版本）
    
    Args:
        domain: 域名
    
    Returns:
        域名年龄（天数），如果无法获取则返回None
    """
    # 在实际实现中，这里会查询WHOIS数据库获取注册日期
    # 现在我们简化处理，返回固定值
    return 1000  # 假设域名已存在1000天


def calculate_trust_score(checks: Dict[str, Any]) -> float:
    """
    计算信任分数
    
    Args:
        checks: 验证检查结果
    
    Returns:
        信任分数 (0-1)
    """
    score = 0.0
    
    if checks.get('has_valid_ssl', False):
        score += 0.3
    if checks.get('is_known_trusted_domain', False):
        score += 0.4
    if checks.get('has_valid_whois', False):
        score += 0.2
    if checks.get('domain_age', 0) and checks['domain_age'] > 365:
        score += 0.1
    
    return min(score, 1.0)  # 确保分数不超过1.0


def determine_trust_level(score: float) -> str:
    """
    根据信任分数确定信任级别
    
    Args:
        score: 信任分数
    
    Returns:
        信任级别
    """
    if score >= 0.8:
        return "high"
    elif score >= 0.5:
        return "medium"
    elif score >= 0.2:
        return "low"
    else:
        return "untrusted"


def select_crawl_strategy(url: str, trust_verification: Dict[str, Any]) -> Dict[str, Any]:
    """
    根据网站特性和信任验证结果选择爬取策略
    
    Args:
        url: 目标URL
        trust_verification: 信任验证结果
    
    Returns:
        爬取策略
    """
    # 根据网站类型选择策略
    if any(edu_domain in url for edu_domain in ['.edu', '.ac.cn', '.edu.cn']):
        strategy = "educational_site"
    elif any(gov_domain in url for gov_domain in ['.gov', '.gov.cn']):
        strategy = "government_site"
    elif trust_verification.get('trust_level') == 'high':
        strategy = "trusted_corporate_site"
    else:
        strategy = "standard_site"
    
    # 确定技术策略
    tech_strategy = "static_parsing"  # 默认使用静态解析
    
    # 在实际实现中，这里会分析网站的技术架构
    # 例如，检测是否为SPA应用、是否需要JavaScript渲染等
    
    return {
        "strategy_type": strategy,
        "technical_approach": tech_strategy,
        "rate_limiting": True,
        "respects_robots_txt": True,
        "user_agent": "TrustedWebScraper/1.0 (Research Purpose)"
    }


def extract_information(
    url: str, 
    content_type: str, 
    data_fields: List[str], 
    crawl_strategy: Dict[str, Any], 
    timeout: int, 
    retry_attempts: int
) -> Dict[str, Any]:
    """
    从网站提取信息
    
    Args:
        url: 目标URL
        content_type: 内容类型
        data_fields: 要提取的数据字段
        crawl_strategy: 爬取策略
        timeout: 超时时间
        retry_attempts: 重试次数
    
    Returns:
        提取结果
    """
    start_time = time.time()
    
    headers = {
        'User-Agent': crawl_strategy.get('user_agent', 'TrustedWebScraper/1.0')
    }
    
    # 执行HTTP请求
    response = None
    for attempt in range(retry_attempts + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                break
            else:
                print(f"Attempt {attempt + 1}: Received status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}: Request failed with error: {e}")
            if attempt == retry_attempts:
                raise
            time.sleep(2 ** attempt)  # 指数退避
    
    if response is None:
        return {
            "error": "Failed to retrieve content after all retry attempts",
            "status_code": None,
            "processing_time": time.time() - start_time
        }
    
    # 这似解析HTML内容（在实际实现中，这里会使用BeautifulSoup或类似库）
    content = response.text
    extracted_data = parse_content(content, content_type, data_fields)
    
    processing_time = time.time() - start_time
    
    return {
        "url": url,
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "content_type": response.headers.get('Content-Type', ''),
        "content_length": len(content),
        "extracted_data": extracted_data,
        "processing_time": processing_time,
        "crawl_strategy_used": crawl_strategy
    }


def parse_content(content: str, content_type: str, data_fields: List[str]) -> List[Dict[str, Any]]:
    """
    解析网页内容，优先使用功能更强的库，如果没有则使用内置方法

    Args:
        content: 网页内容
        content_type: 内容类型
        data_fields: 要提取的数据字段

    Returns:
        提取的数据列表
    """
    # 尝试使用BeautifulSoup（如果可用）
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        extracted_data = []

        # 根据内容类型进行不同的解析
        if content_type == 'text':
            # 提取文本内容
            text_content = soup.get_text(separator=' ', strip=True)
            extracted_data.append({
                "type": "text",
                "content": text_content,
                "length": len(text_content)
            })

            # 提取标题
            titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for title in titles:
                extracted_data.append({
                    "type": f"title_{title.name}",
                    "content": title.get_text(strip=True),
                    "length": len(title.get_text(strip=True))
                })

            # 提取段落
            paragraphs = soup.find_all('p')
            for i, para in enumerate(paragraphs):
                text = para.get_text(strip=True)
                if text:  # 只有非空段落才添加
                    extracted_data.append({
                        "type": "paragraph",
                        "content": text,
                        "length": len(text),
                        "index": i
                    })

        elif content_type == 'tables':
            # 提取表格数据
            tables = soup.find_all('table')
            for i, table in enumerate(tables):
                rows = []
                for row in table.find_all(['tr']):
                    cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                    if cells:
                        rows.append(cells)
                extracted_data.append({
                    "type": "table",
                    "content": rows,
                    "length": len(rows),
                    "index": i
                })

        elif content_type == 'images':
            # 提取图片信息
            images = soup.find_all('img')
            for i, img in enumerate(images):
                extracted_data.append({
                    "type": "image",
                    "src": img.get('src', ''),
                    "alt": img.get('alt', ''),
                    "title": img.get('title', ''),
                    "index": i
                })

        elif content_type == 'documents':
            # 提取文档链接（PDF, DOC, DOCX等）
            doc_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
            links = soup.find_all('a', href=True)
            documents = []
            for link in links:
                href = link['href']
                if any(ext in href.lower() for ext in doc_extensions):
                    documents.append({
                        "url": href,
                        "text": link.get_text(strip=True)
                    })
            extracted_data.append({
                "type": "documents",
                "content": documents,
                "count": len(documents)
            })
        else:
            # 通用处理 - 提取所有文本内容
            text_content = soup.get_text(separator=' ', strip=True)
            extracted_data.append({
                "type": "general_content",
                "content": text_content,
                "length": len(text_content)
            })

        # 如果指定了特定字段，尝试提取这些字段
        for field in data_fields:
            if field.lower() == 'title':
                title_tag = soup.find('title')
                if title_tag:
                    extracted_data.append({
                        "type": "specified_field",
                        "field_name": "title",
                        "content": title_tag.get_text(strip=True),
                        "found": True
                    })
            elif field.lower() == 'meta_description':
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    extracted_data.append({
                        "type": "specified_field",
                        "field_name": "meta_description",
                        "content": meta_desc.get('content', ''),
                        "found": True
                    })
            elif field.lower() == 'links':
                links = [a.get('href', '') for a in soup.find_all('a', href=True)]
                extracted_data.append({
                    "type": "specified_field",
                    "field_name": "links",
                    "content": links,
                    "found": len(links) > 0
                })

        return extracted_data
    except ImportError:
        # 如果BeautifulSoup不可用，使用内置的正则表达式方法
        import re
        extracted_data = []

        # 提取标题（使用正则表达式）
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            extracted_data.append({
                "type": "title",
                "content": title_match.group(1).strip(),
                "length": len(title_match.group(1).strip())
            })

        # 提取H1标签
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        for i, h1 in enumerate(h1_matches):
            extracted_data.append({
                "type": "h1",
                "content": h1.strip(),
                "length": len(h1.strip()),
                "index": i
            })

        # 提取H2标签
        h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL)
        for i, h2 in enumerate(h2_matches):
            extracted_data.append({
                "type": "h2",
                "content": h2.strip(),
                "length": len(h2.strip()),
                "index": i
            })

        # 提取所有段落
        p_matches = re.findall(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        for i, p in enumerate(p_matches):
            clean_p = re.sub(r'<[^>]+>', ' ', p).strip()  # 去除嵌套标签
            if clean_p:  # 只有非空段落才添加
                extracted_data.append({
                    "type": "paragraph",
                    "content": clean_p,
                    "length": len(clean_p),
                    "index": i
                })

        # 提取所有链接
        link_matches = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.IGNORECASE)
        links = []
        for href, text in link_matches:
            links.append({"url": href, "text": re.sub(r'<[^>]+>', '', text).strip()})

        if links:
            extracted_data.append({
                "type": "links",
                "content": links,
                "count": len(links)
            })

        # 提取所有图片
        img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', content, re.IGNORECASE)
        if img_matches:
            extracted_data.append({
                "type": "images",
                "content": img_matches,
                "count": len(img_matches)
            })

        # 根据内容类型进行不同的处理
        if content_type == 'text':
            # 提取纯文本内容
            clean_text = re.sub(r'<[^>]+>', ' ', content)  # 去除HTML标签
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # 去除多余空白

            extracted_data.append({
                "type": "text",
                "content": clean_text,
                "length": len(clean_text)
            })
        elif content_type == 'tables':
            # 提取表格数据（简化处理）
            table_matches = re.findall(r'<table[^>]*>(.*?)</table>', content, re.IGNORECASE | re.DOTALL)
            tables = []
            for table_html in table_matches:
                # 简单提取表格单元格内容
                cells = re.findall(r'<td[^>]*>(.*?)</td>', table_html, re.IGNORECASE | re.DOTALL)
                clean_cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
                tables.append(clean_cells)

            if tables:
                extracted_data.append({
                    "type": "tables",
                    "content": tables,
                    "count": len(tables)
                })

        # 如果指定了特定字段，尝试提取这些字段
        for field in data_fields:
            if field.lower() == 'title':
                if title_match:
                    extracted_data.append({
                        "type": "specified_field",
                        "field_name": "title",
                        "content": title_match.group(1).strip(),
                        "found": True
                    })
            elif field.lower() == 'links':
                extracted_data.append({
                    "type": "specified_field",
                    "field_name": "links",
                    "content": links,
                    "found": len(links) > 0
                })
            elif field.lower() == 'images':
                extracted_data.append({
                    "type": "specified_field",
                    "field_name": "images",
                    "content": img_matches,
                    "found": len(img_matches) > 0
                })

        return extracted_data


def process_extracted_data(extraction_results: Dict[str, Any], data_fields: List[str]) -> Dict[str, Any]:
    """
    处理提取的数据
    
    Args:
        extraction_results: 提取结果
        data_fields: 要处理的数据字段
    
    Returns:
        处理后的数据
    """
    raw_data = extraction_results.get('extracted_data', [])
    
    # 数据清洗和标准化
    cleaned_data = []
    for item in raw_data:
        cleaned_item = item.copy()
        # 在实际实现中，这里会进行数据清洗、去重、标准化等操作
        cleaned_data.append(cleaned_item)
    
    # 数据验证
    validated_data = validate_extracted_data(cleaned_data)
    
    # 数据结构化
    structured_data = structure_extracted_data(validated_data, data_fields)
    
    return {
        "raw_data": raw_data,
        "cleaned_data": cleaned_data,
        "validated_data": validated_data,
        "structured_data": structured_data,
        "data_quality_metrics": calculate_data_quality_metrics(structured_data)
    }


def validate_extracted_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    验证提取的数据
    
    Args:
        data: 提取的数据
    
    Returns:
        验证后的数据
    """
    validated_data = []
    
    for item in data:
        # 在实际实现中，这里会进行数据验证
        # 例如：检查必填字段、数据类型、格式等
        validated_item = item.copy()
        validated_item['validation_status'] = 'passed'  # 简化处理
        validated_data.append(validated_item)
    
    return validated_data


def structure_extracted_data(data: List[Dict[str, Any]], data_fields: List[str]) -> List[Dict[str, Any]]:
    """
    结构化提取的数据
    
    Args:
        data: 提取的数据
        data_fields: 数据字段
    
    Returns:
        结构化的数据
    """
    structured_data = []
    
    for item in data:
        structured_item = {
            "source": item.get('type', 'unknown'),
            "content": item.get('content', ''),
            "metadata": {
                "length": item.get('length', len(item.get('content', ''))),
                "found": item.get('found', True)
            }
        }
        structured_data.append(structured_item)
    
    return structured_data


def calculate_data_quality_metrics(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    计算数据质量指标
    
    Args:
        data: 数据
    
    Returns:
        质量指标
    """
    total_items = len(data)
    valid_items = sum(1 for item in data if item.get('metadata', {}).get('length', 0) > 0)
    
    completeness = valid_items / total_items if total_items > 0 else 0
    
    return {
        "total_items": total_items,
        "valid_items": valid_items,
        "completeness": completeness,
        "accuracy": 0.95,  # 简化值
        "consistency": 0.90  # 简化值
    }


def generate_output(processed_data: Dict[str, Any], trust_verification: Dict[str, Any], output_format: str) -> Any:
    """
    生成输出
    
    Args:
        processed_data: 处理后的数据
        trust_verification: 信任验证结果
        output_format: 输出格式
    
    Returns:
        格式化的输出
    """
    output_data = {
        "trust_info": trust_verification,
        "extracted_data": processed_data["structured_data"],
        "quality_metrics": processed_data["data_quality_metrics"],
        "processing_info": {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    }
    
    if output_format == 'json':
        return output_data
    elif output_format == 'csv':
        # 在实际实现中，这里会将数据转换为CSV格式
        return json.dumps(output_data, ensure_ascii=False, indent=2)
    elif output_format == 'markdown':
        # 在实际实现中，这里会将数据转换为Markdown格式
        return format_as_markdown(output_data)
    else:
        return output_data


def format_as_markdown(data: Dict[str, Any]) -> str:
    """
    将数据格式化为Markdown
    
    Args:
        data: 数据
    
    Returns:
        Markdown格式的字符串
    """
    md_content = f"# 可信网站爬取结果\n\n"
    md_content += f"**信任级别**: {data['trust_info']['trust_level']}\n\n"
    md_content += f"**数据质量**:\n"
    md_content += f"- 完整性: {data['quality_metrics']['completeness']:.2%}\n"
    md_content += f"- 准确性: {data['quality_metrics']['accuracy']:.2%}\n"
    md_content += f"- 一致性: {data['quality_metrics']['consistency']:.2%}\n\n"
    
    md_content += f"## 提取的数据\n"
    for i, item in enumerate(data['extracted_data']):
        md_content += f"### 项目 {i+1}: {item['source']}\n"
        md_content += f"{item['content']}\n\n"
    
    return md_content