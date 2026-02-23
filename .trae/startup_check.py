#!/usr/bin/env python3
"""
编辑器启动时自动检查技能更新
静默模式运行，适合编辑器启动时调用
"""
import os
import sys
import subprocess

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    auto_load_script = os.path.join(script_dir, 'auto_load_skills.py')
    
    if not os.path.exists(auto_load_script):
        return 1
    
    try:
        result = subprocess.run(
            [sys.executable, auto_load_script, '--auto-update', '--silent'],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode
    except Exception:
        return 1

if __name__ == "__main__":
    sys.exit(main())
