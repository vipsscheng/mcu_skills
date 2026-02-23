#!/usr/bin/env python3
"""环境检测与安装脚本"""
import os
import sys
import subprocess
import platform

def check_python():
    """检查Python环境"""
    print("检查Python环境...")
    try:
        version = sys.version_info
        print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
        if version.major >= 3 and version.minor >= 6:
            print("✓ Python版本满足要求")
            return True
        else:
            print("✗ Python版本过低，需要3.6+")
            return False
    except Exception as e:
        print(f"✗ 检查Python环境失败: {e}")
        return False

def install_dependencies():
    """安装依赖"""
    print("\n安装依赖...")
    try:
        # 安装必要的Python包
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("✓ Pip升级成功")
        
        # 安装pyinstaller（如果需要编译成EXE）
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller安装成功")
        
        return True
    except Exception as e:
        print(f"✗ 安装依赖失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 环境检测与安装 ===")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"架构: {platform.machine()}")
    
    # 检查Python环境
    if not check_python():
        print("请安装Python 3.6或更高版本")
        return 1
    
    # 安装依赖
    if not install_dependencies():
        print("依赖安装失败")
        return 1
    
    print("\n✅ 环境检测与安装完成")
    return 0

if __name__ == "__main__":
    sys.exit(main())