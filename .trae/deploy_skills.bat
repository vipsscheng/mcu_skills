@echo off

rem 切换到脚本目录
cd /d "%~dp0"

rem 运行自动加载脚本并复制到全局目录
python auto_load_skills.py --global

rem 暂停以便查看结果
pause