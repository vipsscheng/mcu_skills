@echo off

rem 切换到脚本目录
cd /d "%~dp0"

echo 🚀 开始技能部署流程...
echo.

rem 1. 检查环境
echo 📋 检查环境...
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