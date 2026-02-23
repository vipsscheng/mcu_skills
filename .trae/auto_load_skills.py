#!/usr/bin/env python3
"""
技能自动加载器 V3.0
支持自定义技能目录路径，可以扫描任意位置的技能
支持从GitHub仓库远程拉取技能
用法: 
    python auto_load_skills.py                    # 默认扫描当前目录的 .trae/skills
    python auto_load_skills.py --path /path/to/skills  # 自定义技能目录
    python auto_load_skills.py -p ./my_skills          # 相对路径
    python auto_load_skills.py --global                # 复制到全局目录
    python auto_load_skills.py --pull                  # 从远程仓库拉取技能
    python auto_load_skills.py --pull --global         # 拉取并复制到全局目录
"""
import os
import sys
import json
import glob
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

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

# GitHub仓库配置
GITHUB_REPO = "https://github.com/vipsscheng/skills.git"
GITHUB_BRANCH = "main"

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
    print(f"🔍 扫描技能目录: {skills_dir}")

    if not os.path.exists(skills_dir):
        print(f"❌ 技能目录不存在: {skills_dir}")
        print("\n用法:")
        print("  python auto_load_skills.py                    # 默认扫描")
        print("  python auto_load_skills.py --path /path/to/skills  # 指定目录")
        print("  python auto_load_skills.py -p ./my_skills          # 相对路径")
        print("  python auto_load_skills.py --global                # 复制到全局目录")
        print("\n环境变量:")
        print("  set TRAE_SKILLS_DIR=C:\\path\\to\\skills")
        return []

    skill_dirs = [d for d in os.listdir(skills_dir)
                  if os.path.isdir(os.path.join(skills_dir, d)) and not d.startswith('.')]

    print(f"   找到 {len(skill_dirs)} 个候选技能\n")

    skills = []
    for skill_dir in skill_dirs:
        skill_path = os.path.join(skills_dir, skill_dir)
        skill_info = validate_skill(skill_dir, skill_path)
        if skill_info:
            skills.append(skill_info)

    return skills

def validate_skill(skill_name, skill_path):
    """验证技能是否有效"""
    print(f"📦 验证技能: {skill_name}")

    missing_files = []
    found_files = {}

    for filename, description in REQUIRED_FILES.items():
        file_path = os.path.join(skill_path, filename)
        if os.path.exists(file_path):
            found_files[filename] = file_path
        else:
            missing_files.append(f"{filename} ({description})")

    if missing_files:
        print(f"   ⚠️  缺少必需文件: {', '.join(missing_files)}")
        return None

    try:
        with open(found_files['_meta.json'], 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception as e:
        print(f"   ❌ _meta.json 解析失败: {e}")
        return None

    skill_info = {
        'name': skill_name,
        'path': skill_path,
        'meta': meta,
        'files': found_files
    }

    for filename, description in OPTIONAL_FILES.items():
        file_path = os.path.join(skill_path, filename)
        if os.path.exists(file_path):
            skill_info[filename.rstrip('/')] = file_path

    print(f"   ✅ 技能验证通过")
    return skill_info

def pull_from_github(skills_dir):
    """从GitHub仓库拉取技能"""
    if '--pull' not in sys.argv:
        return False

    print(f"\n📡 从GitHub仓库拉取技能")
    print(f"   仓库: {GITHUB_REPO}")
    print(f"   分支: {GITHUB_BRANCH}")

    # 确保技能目录存在
    if not os.path.exists(skills_dir):
        try:
            os.makedirs(skills_dir)
            print(f"   ✅ 创建技能目录成功: {skills_dir}")
        except Exception as e:
            print(f"   ❌ 创建技能目录失败: {e}")
            return False

    # 检查是否已经是git仓库
    git_dir = os.path.join(skills_dir, '.git')
    if os.path.exists(git_dir):
        # 更新现有仓库
        print("   🔄 更新现有仓库")
        try:
            result = subprocess.run(
                ['git', 'pull', 'origin', GITHUB_BRANCH],
                cwd=skills_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("   ✅ 仓库更新成功")
            else:
                print(f"   ❌ 仓库更新失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ 执行git命令失败: {e}")
            return False
    else:
        # 克隆新仓库
        print("   📋 克隆新仓库")
        try:
            result = subprocess.run(
                ['git', 'clone', '-b', GITHUB_BRANCH, GITHUB_REPO, skills_dir],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("   ✅ 仓库克隆成功")
            else:
                print(f"   ❌ 仓库克隆失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ 执行git命令失败: {e}")
            return False

    return True

def copy_to_global(skills):
    """复制技能到全局目录"""
    if '--global' not in sys.argv:
        return False

    print(f"\n📤 复制技能到全局目录: {GLOBAL_SKILLS_DIR}")

    if not os.path.exists(GLOBAL_SKILLS_DIR):
        try:
            os.makedirs(GLOBAL_SKILLS_DIR)
            print(f"   ✅ 创建全局技能目录成功")
        except Exception as e:
            print(f"   ❌ 创建全局技能目录失败: {e}")
            return False

    copied_count = 0
    for skill in skills:
        skill_name = skill['name']
        source_path = skill['path']
        dest_path = os.path.join(GLOBAL_SKILLS_DIR, skill_name)

        try:
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
                print(f"   🔄 覆盖技能: {skill_name}")
            else:
                print(f"   📋 复制技能: {skill_name}")

            shutil.copytree(source_path, dest_path)
            copied_count += 1
        except Exception as e:
            print(f"   ❌ 复制技能失败 {skill_name}: {e}")

    print(f"   ✅ 成功复制 {copied_count} 个技能到全局目录")
    return True

def generate_registry(skills, skills_dir):
    """生成技能注册表"""
    registry = {
        'version': '2.0.0',
        'generated_at': datetime.now().isoformat(),
        'skills_directory': skills_dir,
        'skills_count': len(skills),
        'skills': []
    }

    for skill in skills:
        skill_entry = {
            'name': skill['name'],
            'slug': skill['meta'].get('slug', skill['name']),
            'version': skill['meta'].get('version', '1.0.0'),
            'path': skill['path'],
            'owner': skill['meta'].get('ownerId', 'unknown'),
            'published_at': skill['meta'].get('publishedAt', 0)
        }

        registry['skills'].append(skill_entry)

    return registry

def save_registry(registry, skills_dir):
    """保存注册表到技能目录"""
    registry_file = os.path.join(skills_dir, 'skill_registry.json')
    try:
        with open(registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        print(f"✅ 注册表已保存: {registry_file}")
        return True
    except Exception as e:
        print(f"❌ 保存注册表失败: {e}")
        fallback_file = os.path.join(os.getcwd(), 'skill_registry.json')
        try:
            with open(fallback_file, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)
            print(f"✅ 注册表已保存到: {fallback_file}")
            return True
        except Exception as e2:
            print(f"❌ 备用保存也失败: {e2}")
            return False

def print_skill_list(registry):
    """打印技能列表"""
    print("\n" + "="*60)
    print("📋 已注册的技能列表")
    print("="*60)

    for i, skill in enumerate(registry['skills'], 1):
        print(f"{i}. {skill['name']}")
        print(f"   版本: {skill['version']}")
        print(f"   路径: {skill['path']}")
        print()

def main():
    print("🚀 技能自动加载器 V3.0")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    skills_dir = get_skills_directory()
    
    # 从GitHub拉取技能（如果指定）
    if '--pull' in sys.argv:
        pull_from_github(skills_dir)

    skills = scan_skills(skills_dir)

    if not skills:
        print("❌ 没有找到有效的技能")
        return 1

    # 复制到全局目录（如果指定）
    if '--global' in sys.argv:
        copy_to_global(skills)

    registry = generate_registry(skills, skills_dir)
    save_registry(registry, skills_dir)
    print_skill_list(registry)

    print(f"✅ 成功加载 {len(skills)} 个技能")
    print(f"📁 技能目录: {skills_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
