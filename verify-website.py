#!/usr/bin/env python3
"""
SocienceAI 网站验证工具

在上传前验证本地网站内容的完整性和正确性

用法:
    python verify-website.py [directory]
"""

import os
import sys
from pathlib import Path
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
import webbrowser


class WebsiteVerifier:
    """网站验证器"""
    
    def __init__(self, website_dir='./website'):
        self.website_dir = Path(website_dir)
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def verify_all(self):
        """执行完整验证"""
        print("\n" + "="*70)
        print("  SocienceAI 网站验证工具")
        print("="*70)
        
        # 1. 检查目录结构
        self._verify_directory()
        
        # 2. 检查文件完整性
        self._verify_files()
        
        # 3. 检查 HTML 文件
        self._verify_html()
        
        # 4. 检查链接
        self._verify_links()
        
        # 5. 检查相对路径
        self._verify_relative_paths()
        
        # 6. 检查样式
        self._verify_styles()
        
        # 打印报告
        self._print_report()
        
        # 返回是否通过
        return len(self.errors) == 0
    
    def _verify_directory(self):
        """检查目录结构"""
        print("\n📁 检查目录结构...")
        
        required_dirs = [
            self.website_dir,
            self.website_dir / 'docs',
            self.website_dir / 'docs' / 'methodologies',
            self.website_dir / 'docs' / 'about',
            self.website_dir / 'docs' / 'blog',
        ]
        
        for dir_path in required_dirs:
            if dir_path.exists():
                self.passed.append(f"目录存在：{dir_path}")
                print(f"  ✅ {dir_path}")
            else:
                error = f"目录缺失：{dir_path}"
                self.errors.append(error)
                print(f"  ❌ {error}")
    
    def _verify_files(self):
        """检查文件完整性"""
        print("\n📄 检查文件完整性...")
        
        required_files = [
            self.website_dir / 'docs' / 'index.html',
            self.website_dir / 'docs' / 'index.md',
        ]
        
        for file_path in required_files:
            if file_path.exists():
                self.passed.append(f"文件存在：{file_path}")
                print(f"  ✅ {file_path.name}")
            else:
                error = f"文件缺失：{file_path}"
                self.errors.append(error)
                print(f"  ❌ {error}")
        
        # 检查方法论文件
        methods_dir = self.website_dir / 'docs' / 'methodologies'
        if methods_dir.exists():
            method_files = list(methods_dir.glob('*.html'))
            print(f"  ✅ 方法论文件：{len(method_files)} 个")
            self.passed.append(f"方法论文件：{len(method_files)} 个")
    
    def _verify_html(self):
        """检查 HTML 文件"""
        print("\n🔍 检查 HTML 文件...")
        
        html_files = list(self.website_dir.rglob('*.html'))
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查 DOCTYPE
            if '<!DOCTYPE html>' in content:
                self.passed.append(f"HTML5 声明：{html_file.name}")
            else:
                warning = f"缺少 DOCTYPE: {html_file.name}"
                self.warnings.append(warning)
            
            # 检查 charset
            if 'charset="UTF-8"' in content or "charset='UTF-8'" in content:
                self.passed.append(f"UTF-8 编码：{html_file.name}")
            else:
                warning = f"缺少 UTF-8 声明：{html_file.name}"
                self.warnings.append(warning)
            
            # 检查基本结构
            if '<html' in content and '</html>' in content:
                self.passed.append(f"HTML 结构：{html_file.name}")
            else:
                error = f"HTML 结构不完整：{html_file.name}"
                self.errors.append(error)
                print(f"  ❌ {error}")
                continue
            
            if '<head>' in content and '</head>' in content:
                self.passed.append(f"HEAD 标签：{html_file.name}")
            else:
                error = f"缺少 HEAD 标签：{html_file.name}"
                self.errors.append(error)
                print(f"  ❌ {error}")
                continue
            
            if '<body>' in content and '</body>' in content:
                self.passed.append(f"BODY 标签：{html_file.name}")
            else:
                error = f"缺少 BODY 标签：{html_file.name}"
                self.errors.append(error)
                print(f"  ❌ {error}")
        
        print(f"  ✅ 检查了 {len(html_files)} 个 HTML 文件")
    
    def _verify_links(self):
        """检查链接"""
        print("\n🔗 检查内部链接...")
        
        html_files = list(self.website_dir.rglob('*.html'))
        link_pattern = re.compile(r'href=["\']([^"\']+)[\"\']')
        
        total_links = 0
        broken_links = 0
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            links = link_pattern.findall(content)
            
            for link in links:
                # 跳过外部链接和锚点
                if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
                    continue
                
                total_links += 1
                
                # 检查相对路径
                if link.startswith('/'):
                    # 绝对路径（相对于 docs）
                    target = self.website_dir / 'docs' / link.lstrip('/')
                else:
                    # 相对路径
                    target = html_file.parent / link
                
                # 检查文件是否存在
                if not target.exists():
                    # 尝试去掉锚点
                    target_no_anchor = Path(str(target).split('#')[0])
                    if not target_no_anchor.exists():
                        broken_links += 1
                        error = f"断链：{html_file.name} → {link}"
                        self.errors.append(error)
                        print(f"  ❌ {error}")
        
        if broken_links == 0:
            print(f"  ✅ 所有 {total_links} 个内部链接正常")
            self.passed.append(f"内部链接：{total_links} 个全部正常")
        else:
            print(f"  ⚠️ 发现 {broken_links} 个断链")
    
    def _verify_relative_paths(self):
        """检查相对路径"""
        print("\n📍 检查相对路径...")
        
        html_files = list(self.website_dir.rglob('*.html'))
        path_pattern = re.compile(r'(href|src)=["\']([^"\']+)[\"\']')
        
        absolute_paths = 0
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            matches = path_pattern.findall(content)
            
            for attr, path in matches:
                # 检查是否有绝对路径（本地文件系统路径）
                if '://' in path or path.startswith('C:') or path.startswith('D:'):
                    absolute_paths += 1
                    error = f"发现绝对路径：{html_file.name} → {path}"
                    self.errors.append(error)
                    print(f"  ❌ {error}")
        
        if absolute_paths == 0:
            print(f"  ✅ 所有路径都是相对路径")
            self.passed.append("所有路径都是相对路径")
        else:
            print(f"  ❌ 发现 {absolute_paths} 个绝对路径")
    
    def _verify_styles(self):
        """检查样式"""
        print("\n🎨 检查样式...")
        
        html_files = list(self.website_dir.rglob('*.html'))
        
        files_with_styles = 0
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有样式
            if '<style>' in content or '<link' in content and 'stylesheet' in content:
                files_with_styles += 1
        
        print(f"  ✅ {files_with_styles}/{len(html_files)} 个文件包含样式")
        self.passed.append(f"样式文件：{files_with_styles}/{len(html_files)}")
    
    def _print_report(self):
        """打印验证报告"""
        print("\n" + "="*70)
        print("  验证报告")
        print("="*70)
        
        print(f"\n✅ 通过：{len(self.passed)} 项")
        print(f"⚠️ 警告：{len(self.warnings)} 项")
        print(f"❌ 错误：{len(self.errors)} 项")
        
        if self.warnings:
            print("\n⚠️ 警告:")
            for warning in self.warnings[:5]:  # 只显示前 5 个
                print(f"  - {warning}")
        
        if self.errors:
            print("\n❌ 错误:")
            for error in self.errors[:10]:  # 只显示前 10 个
                print(f"  - {error}")
        
        print("\n" + "="*70)
        
        if len(self.errors) == 0:
            print("✅ 验证通过！可以安全上传")
        else:
            print("❌ 验证失败！请先修复错误")
        
        print("="*70 + "\n")
    
    def start_local_server(self, port=8080):
        """启动本地测试服务器"""
        print(f"\n🚀 启动本地测试服务器 http://localhost:{port}")
        
        os.chdir(self.website_dir / 'docs')
        
        server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
        
        print(f"服务器已启动，按 Ctrl+C 停止")
        print(f"访问：http://localhost:{port}")
        
        # 自动打开浏览器
        webbrowser.open(f'http://localhost:{port}')
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
            server.shutdown()


class BackupManager:
    """备份管理器"""
    
    def __init__(self, ftp_config):
        self.ftp_config = ftp_config
        self.backup_dir = Path('./backup')
    
    def create_backup(self):
        """创建线上内容备份"""
        print("\n" + "="*70)
        print("  创建线上内容备份")
        print("="*70)
        
        # 创建备份目录
        self.backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f'backup_{timestamp}'
        backup_path.mkdir()
        
        print(f"\n📁 备份目录：{backup_path}")
        
        # TODO: 从 FTP 下载文件到备份目录
        print("⚠️ 待实现：从 FTP 服务器下载备份")
        
        return backup_path
    
    def restore_backup(self, backup_path):
        """恢复备份"""
        print("\n" + "="*70)
        print("  恢复备份")
        print("="*70)
        
        print(f"\n📁 备份路径：{backup_path}")
        
        # TODO: 上传备份文件到 FTP 服务器
        print("⚠️ 待实现：上传备份到 FTP 服务器")


if __name__ == '__main__':
    import sys
    
    # 获取网站目录
    website_dir = sys.argv[1] if len(sys.argv) > 1 else './website'
    
    # 创建验证器
    verifier = WebsiteVerifier(website_dir)
    
    # 执行验证
    success = verifier.verify_all()
    
    if success:
        print("\n✅ 验证通过，可以继续上传")
        
        # 询问是否启动本地服务器
        response = input("\n是否启动本地测试服务器？(y/n): ")
        if response.lower() == 'y':
            verifier.start_local_server()
    else:
        print("\n❌ 验证失败，请先修复错误")
        sys.exit(1)
