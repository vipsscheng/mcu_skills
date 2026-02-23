# 技能自动部署指南

## 自动使用 auto_load_skills.py --global

### 批处理脚本方法

1. **创建批处理文件**：创建 `deploy_skills.bat` 文件

```batch
@echo off

rem 切换到脚本目录
cd /d "%~dp0"

rem 运行自动加载脚本并复制到全局目录
python auto_load_skills.py --global

rem 暂停以便查看结果
pause
```

2. **设置环境变量**：在系统环境变量中添加技能目录路径

```batch
rem 设置技能目录环境变量
setx TRAE_SKILLS_DIR "E:\path\to\skills"
```

3. **计划任务**：设置定期执行的计划任务

- 打开「任务计划程序」
- 创建新任务
- 设置触发器（如每天启动时）
- 操作设置为运行批处理文件
- 保存任务配置

### 开机自启动方法

1. **创建快捷方式**：创建 `deploy_skills.bat` 的快捷方式
2. **移动到启动目录**：将快捷方式移动到 `C:\Users\用户名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

## 编译成 EXE 可执行文件

### 使用 PyInstaller

1. **安装 PyInstaller**

```bash
pip install pyinstaller
```

2. **编译脚本**

```bash
# 切换到脚本目录
cd "E:\Desktop\znt\.trae"

# 编译成单文件可执行程序
pyinstaller --onefile auto_load_skills.py

# 编译成目录形式（包含依赖）
pyinstaller --onedir auto_load_skills.py
```

3. **配置编译选项**

```bash
# 编译时包含必要的依赖
pyinstaller --onefile --add-data "*.py;.", auto_load_skills.py

# 编译时设置图标
pyinstaller --onefile --icon=icon.ico auto_load_skills.py

# 编译时设置名称
pyinstaller --onefile --name=deploy_skills auto_load_skills.py
```

### 编译结果

- 单文件模式：生成 `dist\auto_load_skills.exe`
- 目录模式：生成 `dist\auto_load_skills` 目录

## 自动部署所需环境

### 环境检测与安装脚本

1. **创建环境检测脚本**：`check_env.py`

```python
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
```

2. **创建完整部署脚本**：`full_deploy.bat`

```batch
@echo off

rem 切换到脚本目录
cd /d "%~dp0"

echo 🚀 开始技能部署流程...
echo.

rem 1. 检查环境
python check_env.py
if %errorlevel% neq 0 (
    echo ❌ 环境检查失败
    pause
    exit /b 1
)
echo.

rem 2. 编译成EXE（可选）
echo 🔧 编译技能加载器...
pip install pyinstaller
pyinstaller --onefile auto_load_skills.py
if %errorlevel% neq 0 (
    echo ⚠️  编译失败，继续使用Python脚本
) else (
    echo ✅ 编译成功: dist\auto_load_skills.exe
)
echo.

rem 3. 自动加载技能到全局目录
echo 📤 加载技能到全局目录...
if exist "dist\auto_load_skills.exe" (
    "dist\auto_load_skills.exe" --global
) else (
    python auto_load_skills.py --global
)
echo.

rem 4. 设置环境变量
echo ⚙️ 设置环境变量...
setx TRAE_SKILLS_DIR "%~dp0skills"
echo ✅ 环境变量设置成功

echo.
echo 🎉 技能部署完成！
pause
```

## 部署方案

### 方案1：手动部署

1. **下载技能包**：从GitHub或其他来源下载技能包
2. **解压到技能目录**：将技能解压到 `E:\Desktop\znt\.trae\skills`
3. **运行部署脚本**：双击 `deploy_skills.bat`
4. **验证部署**：检查全局技能目录是否有技能文件

### 方案2：自动部署

1. **创建部署包**：包含所有必要文件
2. **设置计划任务**：定期运行部署脚本
3. **监控部署**：检查部署日志和技能状态

## 验证部署

### 检查技能加载

1. **查看全局技能目录**：`C:\Users\用户名\.trae-cn\skills`
2. **检查技能文件**：确认技能文件已复制
3. **验证技能注册**：检查 `skill_registry.json` 文件
4. **测试技能触发**：在Trae IDE中测试技能是否触发

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 权限不足 | 没有管理员权限 | 以管理员身份运行脚本 |
| 路径错误 | 技能目录路径不正确 | 检查 `TRAE_SKILLS_DIR` 环境变量 |
| 依赖缺失 | Python或依赖未安装 | 运行 `check_env.py` 安装依赖 |
| 编译失败 | PyInstaller未安装 | 先安装PyInstaller |
| 复制失败 | 目标目录权限不足 | 检查全局技能目录权限 |

## 最佳实践

1. **定期更新**：定期运行部署脚本更新技能
2. **版本控制**：使用Git管理技能代码
3. **备份配置**：备份技能配置和注册表
4. **监控日志**：记录部署过程和结果
5. **错误处理**：完善脚本的错误处理机制
6. **自动化**：设置自动部署和更新机制
7. **安全性**：确保技能来源安全可靠
8. **兼容性**：确保技能兼容不同版本的Trae IDE

## 示例部署流程

### 完整部署示例

1. **准备工作**
   - 安装Python 3.6+
   - 下载技能包到 `E:\Desktop\znt\.trae\skills`

2. **运行部署脚本**
   - 双击 `full_deploy.bat`
   - 等待部署完成

3. **验证部署结果**
   - 检查 `C:\Users\用户名\.trae-cn\skills` 目录
   - 在Trae IDE中测试技能触发

4. **设置自动更新**
   - 创建计划任务定期运行部署脚本
   - 监控部署状态

### 命令行部署示例

```bash
# 切换到脚本目录
cd "E:\Desktop\znt\.trae"

# 检查环境
python check_env.py

# 编译成EXE
pyinstaller --onefile auto_load_skills.py

# 加载技能到全局目录
python auto_load_skills.py --global

# 设置环境变量
setx TRAE_SKILLS_DIR "E:\Desktop\znt\.trae\skills"
```