#!/usr/bin/env python3
"""
统一技能安装脚本
用于管理和安装所有技能的依赖和测试
"""
import os
import sys
import subprocess
import importlib
import json
from datetime import datetime

# 获取当前工作目录（优先使用）
current_dir = os.getcwd()

# 尝试找到技能目录
# 1. 首先尝试当前目录的skills子目录
SKILLS_DIR = os.path.join(current_dir, 'skills')
PERMISSIONS_FILE = os.path.join(current_dir, 'permissions.json')

# 2. 如果找不到，尝试.trae/skills目录
if not os.path.exists(SKILLS_DIR):
    trae_dir = os.path.join(current_dir, '.trae')
    if os.path.exists(trae_dir):
        SKILLS_DIR = os.path.join(trae_dir, 'skills')
        PERMISSIONS_FILE = os.path.join(trae_dir, 'permissions.json')

# 3. 如果还是找不到，尝试上级目录的.trae/skills
if not os.path.exists(SKILLS_DIR):
    parent_dir = os.path.dirname(current_dir)
    trae_dir = os.path.join(parent_dir, '.trae')
    if os.path.exists(trae_dir):
        SKILLS_DIR = os.path.join(trae_dir, 'skills')
        PERMISSIONS_FILE = os.path.join(trae_dir, 'permissions.json')

# 权限配置
PERMISSIONS = {
    'file_access': {
        'description': '文件访问权限',
        'required': True,
        'default': True
    },
    'network_access': {
        'description': '网络访问权限',
        'required': False,
        'default': False
    },
    'system_access': {
        'description': '系统访问权限',
        'required': False,
        'default': False
    }
}

# 技能配置
SKILL_CONFIGS = {
    'pdf-0.1.0': {
        'name': 'PDF技能',
        'dependencies': ['PyPDF2'],
        'test_file': 'CMS79FT73x用户手册_V1.5.3.pdf',
        'permissions': ['file_access']
    },
    'mcu-c99-assistant': {
        'name': 'MCU-C99助手',
        'dependencies': [],
        'test_file': None,
        'permissions': []
    }
}

# 加载权限配置
def load_permissions():
    if os.path.exists(PERMISSIONS_FILE):
        try:
            with open(PERMISSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载权限配置失败: {str(e)}")
            return {}
    return {}

# 保存权限配置
def save_permissions(permissions):
    try:
        with open(PERMISSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(permissions, f, indent=2, ensure_ascii=False)
        print("✓ 权限配置已保存")
        return True
    except Exception as e:
        print(f"保存权限配置失败: {str(e)}")
        return False

# 请求权限
def request_permissions():
    print("\n=== 权限授权 ===")
    print("请为技能授予必要的权限：")
    
    permissions = {}
    for perm_name, perm_info in PERMISSIONS.items():
        if perm_info['required']:
            print(f"✓ {perm_info['description']} (必需)")
            permissions[perm_name] = True
        else:
            response = input(f"是否授予 {perm_info['description']}? (y/n, 默认: {perm_info['default']}): ").lower()
            if response == 'y':
                permissions[perm_name] = True
            elif response == 'n':
                permissions[perm_name] = False
            else:
                permissions[perm_name] = perm_info['default']
                print(f"使用默认值: {perm_info['default']}")
    
    return permissions

# 检查权限
def check_permissions():
    print("检查权限配置...")
    
    # 加载现有权限
    existing_permissions = load_permissions()
    
    # 检查是否已有权限配置
    if existing_permissions:
        print("✓ 权限配置已存在")
        return existing_permissions
    
    # 请求新权限
    new_permissions = request_permissions()
    
    # 保存权限配置
    if save_permissions(new_permissions):
        return new_permissions
    else:
        return {}

# 验证技能权限
def verify_skill_permissions(skill_name):
    permissions = load_permissions()
    skill_perms = SKILL_CONFIGS.get(skill_name, {}).get('permissions', [])
    
    for perm in skill_perms:
        if perm not in permissions or not permissions[perm]:
            print(f"✗ {skill_name} 缺少必要的权限: {PERMISSIONS.get(perm, {}).get('description', perm)}")
            return False
    
    return True

# 检查Python环境
def check_python():
    print("检查Python环境...")
    if sys.version_info < (3, 6):
        print("错误：需要Python 3.6或更高版本")
        return False
    print(f"Python版本: {sys.version}")
    return True

# 安装依赖
def install_dependencies(skill_name, dependencies):
    print(f"安装 {skill_name} 依赖...")
    
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} 已安装")
        except ImportError:
            print(f"安装 {dep}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✓ {dep} 安装成功")
            else:
                print(f"✗ {dep} 安装失败: {result.stderr}")
                return False
    return True

# 测试PDF技能
def test_pdf_skill(skill_dir):
    print("测试PDF技能功能...")
    
    # 测试PyPDF2导入
    try:
        import PyPDF2
        print("✓ PyPDF2导入成功")
    except ImportError:
        print("✗ PyPDF2导入失败")
        return False
    
    # 测试PDF文件读取
    test_files = [
        "CMS79FT73x用户手册_V1.5.3.pdf",
        os.path.join(os.path.dirname(SKILLS_DIR), "CMS79FT73x用户手册_V1.5.3.pdf")
    ]
    test_file_found = False
    
    for test_file in test_files:
        if os.path.exists(test_file):
            test_file_found = True
            print(f"测试读取文件: {test_file}")
            try:
                with open(test_file, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    num_pages = len(reader.pages)
                    print(f"✓ 成功读取PDF文件，共 {num_pages} 页")
                    
                    # 测试文本提取
                    if num_pages > 0:
                        page = reader.pages[0]
                        text = page.extract_text()
                        if text:
                            print(f"✓ 成功提取文本，长度: {len(text)} 字符")
                            # 打印前100个字符作为预览
                            preview = text[:100].strip() + "..." if len(text) > 100 else text.strip()
                            print(f"  预览: {preview}")
                        else:
                            print("⚠ 文本提取为空")
            except Exception as e:
                print(f"✗ 读取PDF文件失败: {str(e)}")
            break
    
    if not test_file_found:
        print("⚠ 未找到测试PDF文件，跳过文件读取测试")
    
    return True

# 测试技能
def test_skill(skill_name, skill_dir):
    print(f"\n测试 {SKILL_CONFIGS.get(skill_name, {'name': skill_name})['name']}...")
    
    if skill_name == 'pdf-0.1.0':
        return test_pdf_skill(skill_dir)
    elif skill_name == 'mcu-c99-assistant':
        print("✓ MCU-C99助手技能无需特殊测试")
        return True
    else:
        print(f"⚠ 未找到 {skill_name} 的测试方法，跳过测试")
        return True

# 检查技能目录
def check_skill_directory():
    print("检查技能目录...")
    
    if not os.path.exists(SKILLS_DIR):
        print(f"错误：技能目录不存在: {SKILLS_DIR}")
        return False
    
    skill_dirs = [d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))]
    
    if not skill_dirs:
        print("错误：技能目录为空")
        return False
    
    print(f"找到 {len(skill_dirs)} 个技能:")
    for skill_dir in skill_dirs:
        print(f"- {skill_dir}")
    
    return skill_dirs

# 主安装函数
def main():
    print("=== 统一技能安装与测试 ===")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查Python环境
    if not check_python():
        return 1
    
    # 检查权限配置
    permissions = check_permissions()
    if not permissions:
        print("错误：权限配置失败")
        return 1
    
    # 检查技能目录
    skill_dirs = check_skill_directory()
    if not skill_dirs:
        return 1
    
    # 安装和测试每个技能
    results = {}
    
    for skill_name in skill_dirs:
        print(f"\n=== 处理技能: {skill_name} ===")
        
        skill_dir = os.path.join(SKILLS_DIR, skill_name)
        config = SKILL_CONFIGS.get(skill_name, {'dependencies': [], 'permissions': []})
        
        # 验证技能权限
        if not verify_skill_permissions(skill_name):
            results[skill_name] = '权限不足'
            continue
        
        # 安装依赖
        if not install_dependencies(skill_name, config['dependencies']):
            results[skill_name] = '安装失败'
            continue
        
        # 测试技能
        if not test_skill(skill_name, skill_dir):
            results[skill_name] = '测试失败'
            continue
        
        results[skill_name] = '成功'
    
    # 生成安装报告
    print("\n=== 安装报告 ===")
    print("技能安装结果:")
    
    all_success = True
    for skill_name, result in results.items():
        status = "✓" if result == "成功" else "✗"
        print(f"{status} {skill_name}: {result}")
        if result != "成功":
            all_success = False
    
    print("\n=== 安装完成 ===")
    if all_success:
        print("所有技能安装和测试成功！")
    else:
        print("部分技能安装或测试失败，请查看详细信息")
    
    print("\n使用说明:")
    print("- PDF技能: 使用PDF技能读取文件：[文件路径]")
    print("- MCU-C99助手: 直接询问单片机编程相关问题")
    
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())