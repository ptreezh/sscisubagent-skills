#!/usr/bin/env python3
"""
Soul Agent Downloader - 按需下载机制
=======================================

支持从远程服务器按需下载分身资源包。

用法:
    python scripts/downloader.py --skill grounded-theory
    python scripts/downloader.py --download-all
    python scripts/downloader.py --check-updates

作者: SocienceAI Soul Agent System
版本: 1.0.0
"""

import os
import json
import hashlib
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
import concurrent.futures

# ============================================================================
# 配置
# ============================================================================

STORAGE_ROOT = Path.home() / ".stigmergy" / "soul-agents"
CACHE_DIR = Path.home() / ".cache" / "soul-agents"
MANIFEST_URL = "https://socienceai.com/soul-agents/manifest.json"
CDN_BASE_URL = "https://cdn.socienceai.com/soul-agents"

# ============================================================================
# 核心类
# ============================================================================


class SoulAgentDownloader:
    """分身资源下载器"""

    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> Dict:
        """加载资源清单"""
        try:
            response = requests.get(MANIFEST_URL, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️ 无法加载远程清单: {e}")
            return self._get_local_manifest()

    def _get_local_manifest(self) -> Dict:
        """获取本地清单"""
        local_file = self.cache_dir / "manifest.json"
        if local_file.exists():
            with open(local_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"agents": {}, "version": "1.0.0"}

    def _save_local_manifest(self, manifest: Dict):
        """保存本地清单"""
        local_file = self.cache_dir / "manifest.json"
        with open(local_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

    def get_agent_package_info(self, skill_id: str) -> Optional[Dict]:
        """获取分身包信息"""
        for category in [
            "qualitative_methods",
            "quantitative_methods",
            "mixed_methods",
            "social_theory",
            "business_methods",
        ]:
            if category in self.manifest.get("agents", {}):
                if skill_id in self.manifest["agents"][category]:
                    return self.manifest["agents"][category][skill_id]
        return None

    def download_agent_package(
        self, skill_id: str, progress_callback=None
    ) -> Optional[Path]:
        """
        下载分身资源包

        Args:
            skill_id: 分身ID
            progress_callback: 进度回调函数

        Returns:
            下载到的本地路径，或None（失败）
        """
        package_info = self.get_agent_package_info(skill_id)
        if not package_info:
            print(f"❌ 未找到分身: {skill_id}")
            return None

        # 检查本地缓存
        cache_file = self.cache_dir / f"{skill_id}.zip"
        if cache_file.exists():
            # 验证哈希
            if self._verify_file(cache_file, package_info.get("hash")):
                print(f"✅ 使用缓存: {cache_file}")
                return cache_file
            else:
                cache_file.unlink()  # 删除无效缓存

        # 下载
        url = f"{CDN_BASE_URL}/{skill_id}.zip"
        print(f"📥 正在下载: {package_info.get('name', skill_id)}")
        print(f"   大小: {package_info.get('size', 'N/A')}")

        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(cache_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)

            print(f"✅ 下载完成: {cache_file}")
            return cache_file

        except Exception as e:
            print(f"❌ 下载失败: {e}")
            if cache_file.exists():
                cache_file.unlink()
            return None

    def _verify_file(self, file_path: Path, expected_hash: str) -> bool:
        """验证文件哈希"""
        if not expected_hash or not file_path.exists():
            return True  # 无需验证

        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        actual_hash = sha256_hash.hexdigest()
        return actual_hash == expected_hash

    def install_from_cache(self, cache_file: Path, soul_id: str) -> bool:
        """
        从缓存安装分身

        Args:
            cache_file: 缓存文件路径
            soul_id: Soul ID

        Returns:
            是否安装成功
        """
        import zipfile

        target_dir = STORAGE_ROOT / soul_id

        try:
            print(f"📦 正在解压: {cache_file}")

            with zipfile.ZipFile(cache_file, "r") as zip_ref:
                zip_ref.extractall(target_dir)

            print(f"✅ 安装成功: {target_dir}")
            return True

        except Exception as e:
            print(f"❌ 安装失败: {e}")
            return False

    def download_and_install(
        self, skill_id: str, custom_name: str = None
    ) -> Optional[str]:
        """
        下载并安装分身

        Returns:
            Soul ID 或 None
        """
        # 先创建基础配置（无需等待下载）
        from create_engine import SoulAgentCreator

        creator = SoulAgentCreator()

        # 快速创建基础配置
        result = creator.create_soul_agent(skill_id, custom_name, verbose=False)
        soul_id = result["soul_id"]

        print(f"\n🦞 已创建基础分身配置")
        print(f"   Soul ID: {soul_id}")
        print(f"   位置: {result['path']}")

        # 后台下载完整资源
        print(f"\n📥 正在下载完整资源包...")
        cache_file = self.download_agent_package(skill_id)

        if cache_file:
            self.install_from_cache(cache_file, soul_id)
            print(f"\n✅ 分身完全安装完成!")
        else:
            print(f"\n⚠️ 基础分身已创建，完整资源下载失败")
            print(f"   分身可以正常使用，完整资源稍后可手动下载")

        return soul_id

    def download_all(
        self, parallel: bool = True, progress_callback=None
    ) -> Dict[str, Path]:
        """下载所有分身包"""
        manifest = self._get_local_manifest()
        results = {}

        skill_ids = []
        for category in [
            "qualitative_methods",
            "quantitative_methods",
            "mixed_methods",
            "social_theory",
            "business_methods",
        ]:
            if category in manifest.get("agents", {}):
                skill_ids.extend(manifest["agents"][category].keys())

        print(f"📥 开始下载 {len(skill_ids)} 个分身包...")

        if parallel:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(self.download_agent_package, sid): sid
                    for sid in skill_ids
                }

                for future in concurrent.futures.as_completed(futures):
                    skill_id = futures[future]
                    try:
                        result = future.result()
                        if result:
                            results[skill_id] = result
                    except Exception as e:
                        print(f"❌ {skill_id}: {e}")
        else:
            for skill_id in skill_ids:
                try:
                    result = self.download_agent_package(skill_id, progress_callback)
                    if result:
                        results[skill_id] = result
                except Exception as e:
                    print(f"❌ {skill_id}: {e}")

        return results

    def check_updates(self) -> Dict[str, Dict]:
        """检查更新"""
        local_manifest = self._get_local_manifest()
        remote_manifest = self._load_manifest()

        updates = {}

        for category in [
            "qualitative_methods",
            "quantitative_methods",
            "mixed_methods",
            "social_theory",
            "business_methods",
        ]:
            remote_agents = remote_manifest.get("agents", {}).get(category, {})
            local_agents = local_manifest.get("agents", {}).get(category, {})

            for skill_id, info in remote_agents.items():
                local_version = local_agents.get(skill_id, {}).get("version", "0")
                remote_version = info.get("version", "0")

                if remote_version > local_version:
                    updates[skill_id] = {
                        "name": info.get("name"),
                        "old_version": local_version,
                        "new_version": remote_version,
                        "changelog": info.get("changelog", ""),
                    }

        return updates


# ============================================================================
# 主程序
# ============================================================================


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Soul Agent Downloader")
    parser.add_argument("--skill", "-s", help="下载指定分身")
    parser.add_argument(
        "--download-all", "-a", action="store_true", help="下载所有分身"
    )
    parser.add_argument("--check-updates", "-u", action="store_true", help="检查更新")
    parser.add_argument("--parallel", "-p", action="store_true", help="并行下载")

    args = parser.parse_args()

    downloader = SoulAgentDownloader()

    if args.check_updates:
        print("\n🔍 检查更新中...")
        updates = downloader.check_updates()

        if updates:
            print(f"\n📦 发现 {len(updates)} 个可用更新:\n")
            for skill_id, info in updates.items():
                print(f"  • {info['name']} ({skill_id})")
                print(f"    {info['old_version']} → {info['new_version']}")
                if info["changelog"]:
                    print(f"    更新: {info['changelog']}")
                print()
        else:
            print("\n✅ 已是最新版本")
        return

    if args.skill:
        cache_file = downloader.download_agent_package(args.skill)
        if cache_file:
            print(f"\n✅ 下载完成: {cache_file}")
        return

    if args.download_all:
        results = downloader.download_all(parallel=args.parallel)
        print(
            f"\n✅ 下载完成: {len(results)}/{len(downloader._get_local_manifest().get('agents', {}))} 个分身"
        )
        return

    parser.print_help()


if __name__ == "__main__":
    main()
