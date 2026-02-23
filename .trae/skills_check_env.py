#!/usr/bin/env python3
"""
技能环境自动检测与安装脚本
支持检测所有技能依赖并自动安装
"""
import os
import sys
import subprocess
import platform
import json
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPT_DIR / "skills"

SYSTEM = platform.system().lower()
if SYSTEM == "windows":
    SYSTEM = "win32"

ALL_SKILL_DEPENDENCIES = {
    "nima-core-3.0.6": {
        "name": "NIMA核心",
        "requires": {
            "bins": ["python3", "node", "npm"],
            "pip_packages": ["pip", "setuptools", "wheel"]
        },
        "os": ["linux", "darwin", "win32"],
        "install": {
            "pip": ["-r requirements.txt", "-r requirements-scalability.txt"],
            "npm": []
        }
    },
    "fast-browser-use-1.0.5": {
        "name": "浏览器自动化",
        "requires": {
            "bins": ["cargo", "rustc"],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {
            "pip": [],
            "npm": []
        }
    },
    "memory-manager-1.0.0": {
        "name": "内存管理器",
        "requires": {
            "bins": ["bash", "sh"],
            "pip_packages": []
        },
        "os": ["linux", "darwin"],
        "install": {"pip": [], "npm": []}
    },
    "skill-creator-0.1.0": {
        "name": "技能创建器",
        "requires": {
            "bins": ["python3"],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    },
    "free-ride-1.0.4": {
        "name": "Free Ride",
        "requires": {
            "bins": ["python3"],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    },
    "self-improving-unified-1.0.0": {
        "name": "自我改进统一",
        "requires": {
            "bins": ["bash", "sh"],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    },
    "mcu-c99-assistant": {
        "name": "MCU C99助手",
        "requires": {
            "bins": [],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    },
    "pdf-0.1.0": {
        "name": "PDF处理",
        "requires": {
            "bins": [],
            "pip_packages": ["PyPDF2", "pdfplumber", "reportlab"]
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": ["PyPDF2", "pdfplumber", "reportlab"], "npm": []}
    },
    "frontend-design-1.0.0": {
        "name": "前端设计",
        "requires": {
            "bins": [],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    },
    "superdesign-1.0.0": {
        "name": "超级设计",
        "requires": {
            "bins": [],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    },
    "clean-code-review-1.0.0": {
        "name": "代码审查",
        "requires": {
            "bins": [],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    },
    "desktop-control-1.0.0": {
        "name": "桌面控制",
        "requires": {
            "bins": ["python3"],
            "pip_packages": ["pip"]
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    },
    "essence-distiller-1.0.1": {
        "name": "内容提炼",
        "requires": {
            "bins": [],
            "pip_packages": []
        },
        "os": ["linux", "darwin", "win32"],
        "install": {"pip": [], "npm": []}
    }
}

WINGET_PACKAGES = {
    "rust": {"id": "Rustlang.Rust.MSVC", "name": "Rust (MSVC)"},
    "git": {"id": "Git.Git", "name": "Git"},
    "python3": {"id": "Python.Python.3.13", "name": "Python 3.13"},
    "node": {"id": "OpenJS.NodeJS.LTS", "name": "Node.js LTS"},
}

def get_command_path(cmd):
    """获取命令路径"""
    if SYSTEM == "win32":
        try:
            result = subprocess.run(
                ["where", cmd], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip().split("\n")[0]
        except:
            pass
    else:
        try:
            result = subprocess.run(
                ["which", cmd], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
    return None

def check_command(cmd):
    """检查命令是否存在"""
    return get_command_path(cmd) is not None

def check_python_package(package):
    """检查Python包是否已安装"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except:
        return False

def check_winget():
    """检查winget是否可用"""
    try:
        result = subprocess.run(
            ["winget", "--version"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except:
        return False

def install_with_winget(package_id):
    """使用winget安装软件"""
    print(f"  尝试使用 winget 安装 {package_id}...")
    try:
        result = subprocess.run(
            ["winget", "install", package_id, "--silent", "--accept-package-agreements", "--accept-source-agreements"],
            capture_output=True, text=True, timeout=300
        )
        return result.returncode == 0
    except Exception as e:
        print(f"  安装失败: {e}")
        return False

def install_pip_package(package):
    """安装Python包"""
    print(f"  安装 Python 包: {package}")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "--quiet"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print(f"  ✓ {package} 安装成功")
            return True
        else:
            print(f"  ✗ {package} 安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ {package} 安装失败: {e}")
        return False

def check_skill(skill_name, config):
    """检查单个技能的依赖"""
    print(f"\n检查技能: {skill_name} ({config.get('name', '')})")
    
    results = {
        "os_compatible": SYSTEM in config.get("os", []),
        "bins": [],
        "pip_packages": [],
        "status": "ok"
    }
    
    if not results["os_compatible"]:
        print(f"  ⚠️ 操作系统不兼容: 需要 {config.get('os', [])}，当前 {SYSTEM}")
        results["status"] = "os_incompatible"
        return results
    
    for bin_cmd in config.get("requires", {}).get("bins", []):
        if check_command(bin_cmd):
            print(f"  ✓ {bin_cmd}")
        else:
            print(f"  ✗ {bin_cmd} (缺失)")
            results["bins"].append(bin_cmd)
    
    for pkg in config.get("requires", {}).get("pip_packages", []):
        if check_python_package(pkg):
            print(f"  ✓ Python包: {pkg}")
        else:
            print(f"  ✗ Python包: {pkg} (缺失)")
            results["pip_packages"].append(pkg)
    
    if results["bins"] or results["pip_packages"]:
        results["status"] = "missing_deps"
    
    return results

def install_skill_deps(skill_name, config, results):
    """安装技能缺失的依赖"""
    print(f"\n安装 {skill_name} 的缺失依赖...")
    
    winget_available = check_winget()
    
    for bin_cmd in results.get("bins", []):
        if bin_cmd in WINGET_PACKAGES:
            pkg_info = WINGET_PACKAGES[bin_cmd]
            print(f"  尝试安装: {pkg_info['name']}")
            if install_with_winget(pkg_info['id']):
                print(f"  ✓ {pkg_info['name']} 安装成功")
            else:
                print(f"  ✗ {pkg_info['name']} 安装失败")
        else:
            print(f"  ⚠️ 没有找到 {bin_cmd} 的自动安装方法，请手动安装")
    
    for pkg in results.get("pip_packages", []):
        install_pip_package(pkg)

def main():
    print("=" * 60)
    print("技能环境自动检测与安装")
    print("=" * 60)
    print(f"操作系统: {SYSTEM}")
    print(f"Python版本: {sys.version_info.major}.{sys.version_info.minor}")
    print(f"技能数量: {len(ALL_SKILL_DEPENDENCIES)}")
    
    results = {}
    missing_deps_skills = {}
    
    print("\n" + "=" * 60)
    print("开始检测技能依赖...")
    print("=" * 60)
    
    for skill_name, config in ALL_SKILL_DEPENDENCIES.items():
        results[skill_name] = check_skill(skill_name, config)
        if results[skill_name]["status"] == "missing_deps":
            missing_deps_skills[skill_name] = results[skill_name]
    
    print("\n" + "=" * 60)
    print("检测完成")
    print("=" * 60)
    
    total = len(results)
    ok_count = sum(1 for r in results.values() if r["status"] == "ok")
    missing_count = len(missing_deps_skills)
    incompatible_count = sum(1 for r in results.values() if r["status"] == "os_incompatible")
    
    print(f"\n总计: {total} 个技能")
    print(f"  ✓ 正常: {ok_count}")
    print(f"  ⚠️ 缺少依赖: {missing_count}")
    print(f"  ✗ 系统不兼容: {incompatible_count}")
    
    if missing_deps_skills:
        print("\n" + "=" * 60)
        print("开始自动安装缺失依赖...")
        print("=" * 60)
        
        for skill_name, result in missing_deps_skills.items():
            config = ALL_SKILL_DEPENDENCIES[skill_name]
            install_skill_deps(skill_name, config, result)
        
        print("\n" + "=" * 60)
        print("安装完成，请重启终端后重新检测")
        print("=" * 60)
    else:
        print("\n✓ 所有技能依赖已满足!")
    
    print("\n" + "=" * 60)
    print("技能依赖状态详情")
    print("=" * 60)
    
    for skill_name, result in results.items():
        config = ALL_SKILL_DEPENDENCIES[skill_name]
        status_icon = {
            "ok": "✓",
            "missing_deps": "⚠️",
            "os_incompatible": "✗"
        }.get(result["status"], "?")
        
        print(f"\n{status_icon} {skill_name}")
        print(f"   名称: {config.get('name', '')}")
        
        if result["bins"]:
            print(f"   缺失命令: {', '.join(result['bins'])}")
        if result["pip_packages"]:
            print(f"   缺失Python包: {', '.join(result['pip_packages'])}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
