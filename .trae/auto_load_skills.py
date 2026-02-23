#!/usr/bin/env python3
"""
技能自动加载器 V4.0
支持自定义技能目录路径，可以扫描任意位置的技能
支持从GitHub仓库远程拉取技能
支持自动检查更新和静默模式
支持AI编程工具平台自动检测（Trae、Cursor、Copilot、Claude等）
用法: 
    python auto_load_skills.py                    # 默认扫描当前目录的 .trae/skills
    python auto_load_skills.py --path /path/to/skills  # 自定义技能目录
    python auto_load_skills.py -p ./my_skills          # 相对路径
    python auto_load_skills.py --global                # 复制到全局目录
    python auto_load_skills.py --pull                  # 从远程仓库拉取技能
    python auto_load_skills.py --pull --global         # 拉取并复制到全局目录
    python auto_load_skills.py --check-update          # 检查是否有更新
    python auto_load_skills.py --auto-update           # 自动检查并应用更新
    python auto_load_skills.py --silent                # 静默模式（无输出）
    python auto_load_skills.py --detect-platform       # 检测当前AI编程工具平台
"""
import os
import sys
import json
import glob
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import platform_detector
    HAS_PLATFORM_DETECTOR = True
except ImportError:
    HAS_PLATFORM_DETECTOR = False

REQUIRED_FILES = {
    'SKILL.md': '技能说明文件',
    '_meta.json': '技能元数据文件'
}

OPTIONAL_FILES = {
    'skill.json': '技能配置文件',
    'scripts/': '脚本目录',
    'references/': '参考文档目录',
    'assets/': '资源文件目录'
}

# 全局技能目录
GLOBAL_SKILLS_DIR = os.path.join(os.path.expanduser('~'), '.trae-cn', 'skills')

# 默认配置
DEFAULT_CONFIG = {
    "auto_update": {
        "enabled": True,
        "check_on_startup": True,
        "check_interval_hours": 24,
        "silent_mode": False,
        "auto_apply_updates": False,
        "last_check_timestamp": 0
    },
    "github": {
        "repo": "https://github.com/vipsscheng/mcu_skills.git",
        "branch": "main"
    }
}

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def is_silent_mode():
    """检查是否为静默模式"""
    return '--silent' in sys.argv or load_config()['auto_update']['silent_mode']

def print_silent(*args, **kwargs):
    """条件打印（非静默模式下才输出"""
    if not is_silent_mode():
        print(*args, **kwargs)

def should_check_update(config):
    """检查是否应该检查更新"""
    if config['auto_update']['enabled'] and config['auto_update']['check_on_startup']:
        last_check = config['auto_update']['last_check_timestamp']
        interval = config['auto_update']['check_interval_hours'] * 3600
        return (datetime.now().timestamp() - last_check) > interval
    return False

def check_for_updates(skills_dir, config):
    """检查是否有更新可用（不应用）"""
    print_silent(f"\n🔍 检查技能更新...")
    
    git_dir = os.path.join(skills_dir, '.git')
    if not os.path.exists(git_dir):
        print_silent("   ⚠️  不是Git仓库，无法检查更新")
        return False
    
    try:
        result = subprocess.run(
            ['git', 'fetch', 'origin'],
            cwd=skills_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_silent(f"   ❌ 获取远程更新失败")
            return False
        
        result = subprocess.run(
            ['git', 'rev-list', '--count', 'HEAD..origin/' + config['github']['branch']],
            cwd=skills_dir,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            count = int(result.stdout.strip())
            if count > 0:
                print_silent(f"   📡 发现 {count} 个新提交可用！")
                return True
            else:
                print_silent("   ✅ 已是最新版本")
                return False
        return False
    except Exception as e:
        print_silent(f"   ❌ 检查更新失败: {e}")
        return False

def get_skills_directory():
    """从命令行参数、环境变量或默认位置获取技能目录"""
    if len(sys.argv) >= 3 and sys.argv[1] in ['--path', '-p']:
        custom_path = sys.argv[2]
        if os.path.isabs(custom_path):
            return custom_path
        else:
            return os.path.abspath(custom_path)

    env_path = os.environ.get('TRAE_SKILLS_DIR')
    if env_path and os.path.exists(env_path):
        return env_path

    current_dir = os.getcwd()
    possible_paths = [
        os.path.join(current_dir, '.trae', 'skills'),
        os.path.join(current_dir, 'skills'),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    parent_dir = os.path.dirname(current_dir)
    for path in [
        os.path.join(parent_dir, '.trae', 'skills'),
        os.path.join(parent_dir, 'skills'),
    ]:
        if os.path.exists(path):
            return path

    return possible_paths[0]

def scan_skills(skills_dir):
    """扫描技能目录，返回所有有效技能列表"""
    print_silent(f"🔍 扫描技能目录: {skills_dir}")

    if not os.path.exists(skills_dir):
        print_silent(f"❌ 技能目录不存在: {skills_dir}")
        print_silent("\n用法:")
        print_silent("  python auto_load_skills.py                    # 默认扫描")
        print_silent("  python auto_load_skills.py --path /path/to/skills  # 指定目录")
        print_silent("  python auto_load_skills.py -p ./my_skills          # 相对路径")
        print_silent("  python auto_load_skills.py --global                # 复制到全局目录")
        print_silent("  python auto_load_skills.py --check-update          # 检查是否有更新")
        print_silent("  python auto_load_skills.py --auto-update           # 自动检查并应用更新")
        print_silent("  python auto_load_skills.py --silent                # 静默模式（无输出）")
        print_silent("\n环境变量:")
        print_silent("  set TRAE_SKILLS_DIR=C:\\path\\to\\skills")
        return []

    skill_dirs = [d for d in os.listdir(skills_dir)
                  if os.path.isdir(os.path.join(skills_dir, d)) and not d.startswith('.')]

    print_silent(f"   找到 {len(skill_dirs)} 个候选技能\n")

    skills = []
    for skill_dir in skill_dirs:
        skill_path = os.path.join(skills_dir, skill_dir)
        skill_info = validate_skill(skill_dir, skill_path)
        if skill_info:
            skills.append(skill_info)

    return skills

def validate_skill(skill_name, skill_path):
    """验证技能是否有效"""
    print_silent(f"📦 验证技能: {skill_name}")

    missing_files = []
    found_files = {}

    for filename, description in REQUIRED_FILES.items():
        file_path = os.path.join(skill_path, filename)
        if os.path.exists(file_path):
            found_files[filename] = file_path
        else:
            missing_files.append(f"{filename} ({description})")

    if missing_files:
        print_silent(f"   ⚠️  缺少必需文件: {', '.join(missing_files)}")
        return None

    try:
        with open(found_files['_meta.json'], 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception as e:
        print_silent(f"   ❌ _meta.json 解析失败: {e}")
        return None

    skill_info = {
        'name': skill_name,
        'path': skill_path,
        'meta': meta,
        'files': found_files,
        'platform_templates': {}
    }

    for filename, description in OPTIONAL_FILES.items():
        file_path = os.path.join(skill_path, filename)
        if os.path.exists(file_path):
            skill_info[filename.rstrip('/')] = file_path

    if HAS_PLATFORM_DETECTOR:
        available_templates = platform_detector.get_available_templates(skill_path)
        if available_templates:
            skill_info['platform_templates']['available'] = available_templates
            
            current_platform = platform_detector.detect_platform()
            if current_platform != 'unknown':
                template_path = platform_detector.get_platform_template_path(skill_path, current_platform)
                if template_path:
                    skill_info['platform_templates']['active'] = template_path
                    skill_info['platform_templates']['platform'] = current_platform
                    print_silent(f"   🎯 检测到平台: {platform_detector.get_platform_info(current_platform)['name']}")
                    print_silent(f"   📄 平台模板: {os.path.basename(template_path)}")

    print_silent(f"   ✅ 技能验证通过")
    return skill_info

def pull_from_github(skills_dir, config=None):
    """从GitHub仓库拉取技能"""
    if config is None:
        config = load_config()
    
    github_repo = config['github']['repo']
    github_branch = config['github']['branch']

    print_silent(f"\n📡 从GitHub仓库拉取技能")
    print_silent(f"   仓库: {github_repo}")
    print_silent(f"   分支: {github_branch}")

    # 确保技能目录存在
    if not os.path.exists(skills_dir):
        try:
            os.makedirs(skills_dir)
            print_silent(f"   ✅ 创建技能目录成功: {skills_dir}")
        except Exception as e:
            print_silent(f"   ❌ 创建技能目录失败: {e}")
            return False

    # 检查是否已经是git仓库
    git_dir = os.path.join(skills_dir, '.git')
    if os.path.exists(git_dir):
        # 更新现有仓库
        print_silent("   🔄 更新现有仓库")
        try:
            result = subprocess.run(
                ['git', 'pull', 'origin', github_branch],
                cwd=skills_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print_silent("   ✅ 仓库更新成功")
            else:
                print_silent(f"   ❌ 仓库更新失败: {result.stderr}")
                return False
        except Exception as e:
            print_silent(f"   ❌ 执行git命令失败: {e}")
            return False
    else:
        # 克隆新仓库
        print_silent("   📋 克隆新仓库")
        try:
            result = subprocess.run(
                ['git', 'clone', '-b', github_branch, github_repo, skills_dir],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print_silent("   ✅ 仓库克隆成功")
            else:
                print_silent(f"   ❌ 仓库克隆失败: {result.stderr}")
                return False
        except Exception as e:
            print_silent(f"   ❌ 执行git命令失败: {e}")
            return False

    return True

def copy_to_global(skills):
    """复制技能到全局目录"""
    if '--global' not in sys.argv:
        return False

    print_silent(f"\n📤 复制技能到全局目录: {GLOBAL_SKILLS_DIR}")

    if not os.path.exists(GLOBAL_SKILLS_DIR):
        try:
            os.makedirs(GLOBAL_SKILLS_DIR)
            print_silent(f"   ✅ 创建全局技能目录成功")
        except Exception as e:
            print_silent(f"   ❌ 创建全局技能目录失败: {e}")
            return False

    copied_count = 0
    for skill in skills:
        skill_name = skill['name']
        source_path = skill['path']
        dest_path = os.path.join(GLOBAL_SKILLS_DIR, skill_name)

        try:
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
                print_silent(f"   🔄 覆盖技能: {skill_name}")
            else:
                print_silent(f"   📋 复制技能: {skill_name}")

            shutil.copytree(source_path, dest_path)
            copied_count += 1
        except Exception as e:
            print_silent(f"   ❌ 复制技能失败 {skill_name}: {e}")

    print_silent(f"   ✅ 成功复制 {copied_count} 个技能到全局目录")
    return True

def generate_registry(skills, skills_dir):
    """生成技能注册表"""
    registry = {
        'version': '2.0.0',
        'generated_at': datetime.now().isoformat(),
        'skills_directory': skills_dir,
        'skills_count': len(skills),
        'skills': [],
        'platform': {}
    }

    if HAS_PLATFORM_DETECTOR:
        current_platform = platform_detector.detect_platform()
        registry['platform']['detected'] = current_platform
        registry['platform']['info'] = platform_detector.get_platform_info(current_platform)

    for skill in skills:
        skill_entry = {
            'name': skill['name'],
            'slug': skill['meta'].get('slug', skill['name']),
            'version': skill['meta'].get('version', '1.0.0'),
            'path': skill['path'],
            'owner': skill['meta'].get('ownerId', 'unknown'),
            'published_at': skill['meta'].get('publishedAt', 0),
            'platform_templates': skill.get('platform_templates', {})
        }

        registry['skills'].append(skill_entry)

    return registry

def save_registry(registry, skills_dir):
    """保存注册表到技能目录"""
    registry_file = os.path.join(skills_dir, 'skill_registry.json')
    try:
        with open(registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        print_silent(f"✅ 注册表已保存: {registry_file}")
        return True
    except Exception as e:
        print_silent(f"❌ 保存注册表失败: {e}")
        fallback_file = os.path.join(os.getcwd(), 'skill_registry.json')
        try:
            with open(fallback_file, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)
            print_silent(f"✅ 注册表已保存到: {fallback_file}")
            return True
        except Exception as e2:
            print_silent(f"❌ 备用保存也失败: {e2}")
            return False

def print_skill_list(registry):
    """打印技能列表"""
    print_silent("\n" + "="*60)
    print_silent("📋 已注册的技能列表")
    print_silent("="*60)

    for i, skill in enumerate(registry['skills'], 1):
        print_silent(f"{i}. {skill['name']}")
        print_silent(f"   版本: {skill['version']}")
        print_silent(f"   路径: {skill['path']}")
        print_silent()

def main():
    config = load_config()
    
    # 平台检测模式
    if '--detect-platform' in sys.argv:
        if HAS_PLATFORM_DETECTOR:
            return platform_detector.main()
        else:
            print("错误: platform_detector 模块不可用")
            return 1
    
    print_silent("🚀 技能自动加载器 V4.0")
    print_silent(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    skills_dir = get_skills_directory()
    
    # 检查更新模式
    if '--check-update' in sys.argv:
        has_update = check_for_updates(skills_dir, config)
        config['auto_update']['last_check_timestamp'] = datetime.now().timestamp()
        save_config(config)
        return 0 if not has_update else 1
    
    # 自动更新模式
    if '--auto-update' in sys.argv:
        has_update = check_for_updates(skills_dir, config)
        if has_update:
            if config['auto_update']['auto_apply_updates']:
                pull_from_github(skills_dir, config)
            else:
                print_silent("\n提示: 运行 'python auto_load_skills.py --pull' 来应用更新")
        config['auto_update']['last_check_timestamp'] = datetime.now().timestamp()
        save_config(config)
    
    # 从GitHub拉取技能（如果指定）
    if '--pull' in sys.argv:
        pull_from_github(skills_dir, config)
    
    # 启动时自动检查更新
    if '--check-update' not in sys.argv and '--auto-update' not in sys.argv and '--pull' not in sys.argv:
        if should_check_update(config):
            print_silent("\n⏰ 距上次检查已超过 {} 小时，正在检查更新...".format(config['auto_update']['check_interval_hours']))
            has_update = check_for_updates(skills_dir, config)
            config['auto_update']['last_check_timestamp'] = datetime.now().timestamp()
            save_config(config)
            if has_update and config['auto_update']['auto_apply_updates']:
                print_silent("\n🚀 自动应用更新...")
                pull_from_github(skills_dir, config)

    skills = scan_skills(skills_dir)

    if not skills:
        print_silent("❌ 没有找到有效的技能")
        return 1

    # 复制到全局目录（如果指定）
    if '--global' in sys.argv:
        copy_to_global(skills)

    registry = generate_registry(skills, skills_dir)
    save_registry(registry, skills_dir)
    print_skill_list(registry)

    print_silent(f"✅ 成功加载 {len(skills)} 个技能")
    print_silent(f"📁 技能目录: {skills_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
