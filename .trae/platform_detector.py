#!/usr/bin/env python3
"""
AI编程工具平台检测器
自动检测当前使用的AI编程工具：Trae、Cursor、Copilot、Claude等
"""
import os
import sys
import json
from pathlib import Path

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

KNOWN_PLATFORMS = {
    'trae': {
        'name': 'Trae IDE',
        'env_vars': ['TRAE_IDE', 'TRAE_SKILLS_DIR'],
        'process_names': ['trae', 'trae-ide'],
        'template_suffix': 'trae'
    },
    'cursor': {
        'name': 'Cursor',
        'env_vars': ['CURSOR', 'CURSOR_HOME'],
        'process_names': ['cursor'],
        'template_suffix': 'cursorrules'
    },
    'copilot': {
        'name': 'GitHub Copilot',
        'env_vars': ['GITHUB_COPILOT', 'COPILOT'],
        'process_names': ['github-copilot'],
        'template_suffix': 'copilot-instructions'
    },
    'claude': {
        'name': 'Claude',
        'env_vars': ['CLAUDE', 'ANTHROPIC'],
        'process_names': ['claude'],
        'template_suffix': 'claude-knowledge'
    },
    'windsurf': {
        'name': 'Windsurf',
        'env_vars': ['WINDSURF'],
        'process_names': ['windsurf'],
        'template_suffix': 'windsurf'
    },
    'continue': {
        'name': 'Continue',
        'env_vars': ['CONTINUE'],
        'process_names': ['continue'],
        'template_suffix': 'continue'
    }
}

def detect_platform_from_env():
    """从环境变量检测平台"""
    for platform_id, platform_info in KNOWN_PLATFORMS.items():
        for env_var in platform_info['env_vars']:
            if env_var in os.environ:
                return platform_id
    return None

def detect_platform_from_process():
    """从进程检测平台"""
    if not HAS_PSUTIL:
        return None
    
    try:
        current_pid = os.getpid()
        parent = psutil.Process(current_pid)
        
        while parent:
            parent_name = parent.name().lower()
            for platform_id, platform_info in KNOWN_PLATFORMS.items():
                for proc_name in platform_info['process_names']:
                    if proc_name in parent_name:
                        return platform_id
            try:
                parent = parent.parent()
            except psutil.NoSuchProcess:
                break
    except Exception:
        pass
    return None

def detect_platform_from_config():
    """从配置文件检测平台"""
    config_path = Path(__file__).parent / 'config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if 'platform' in config:
                    platform_config = config['platform']
                    if 'forced_platform' in platform_config and platform_config['forced_platform']:
                        platform_id = platform_config['forced_platform']
                        if platform_id in KNOWN_PLATFORMS:
                            return platform_id
        except Exception:
            pass
    return None

def detect_platform():
    """综合检测平台"""
    platform = detect_platform_from_config()
    if platform:
        return platform
    
    platform = detect_platform_from_env()
    if platform:
        return platform
    
    platform = detect_platform_from_process()
    if platform:
        return platform
    
    return 'unknown'

def get_platform_info(platform_id):
    """获取平台信息"""
    return KNOWN_PLATFORMS.get(platform_id, {
        'name': 'Unknown Platform',
        'template_suffix': 'default'
    })

def get_platform_template_path(skill_dir, platform_id):
    """获取平台模板路径"""
    platform_info = get_platform_info(platform_id)
    template_suffix = platform_info['template_suffix']
    
    templates_dir = Path(skill_dir) / 'templates' / 'platforms'
    if not templates_dir.exists():
        return None
    
    for template_file in templates_dir.iterdir():
        if template_file.is_file() and template_suffix in template_file.name:
            return str(template_file)
    
    return None

def get_available_templates(skill_dir):
    """获取技能可用的所有平台模板"""
    templates_dir = Path(skill_dir) / 'templates' / 'platforms'
    if not templates_dir.exists():
        return []
    
    templates = []
    for template_file in templates_dir.iterdir():
        if template_file.is_file():
            templates.append(template_file.name)
    
    return templates

def main():
    """测试平台检测"""
    print("=" * 60)
    print("AI编程工具平台检测器")
    print("=" * 60)
    
    platform = detect_platform()
    platform_info = get_platform_info(platform)
    
    print(f"\n检测结果:")
    print(f"  平台ID: {platform}")
    print(f"  平台名称: {platform_info['name']}")
    
    if platform != 'unknown':
        print(f"\n环境变量检测:")
        for env_var in platform_info['env_vars']:
            if env_var in os.environ:
                print(f"  ✓ {env_var} = {os.environ[env_var]}")
            else:
                print(f"  ✗ {env_var}")
        
        if HAS_PSUTIL:
            print(f"\n进程检测:")
            try:
                current_pid = os.getpid()
                parent = psutil.Process(current_pid)
                print(f"  当前进程: {parent.name()} (PID: {current_pid})")
                while parent:
                    parent = parent.parent()
                    if parent:
                        print(f"  父进程: {parent.name()} (PID: {parent.pid})")
            except Exception as e:
                print(f"  进程检测失败: {e}")
        else:
            print(f"\n进程检测: (psutil 未安装，跳过)")
    
    print("\n" + "=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
