# 用户体验增强

## 配置向导

### 图形化配置向导

#### 功能概述

- **直观界面**：图形化界面，易于操作
- **自动检测**：自动检测系统环境和已安装的工具
- **路径配置**：可视化配置编译器和工具路径
- **串口管理**：自动检测和配置串口设置
- **平台选择**：支持多种国产单片机平台
- **优化设置**：提供编译优化级别选择
- **配置验证**：验证配置的有效性
- **一键保存**：快速保存配置到文件

#### 使用流程

1. **启动向导**：运行`config_wizard.py`脚本
2. **环境检测**：自动检测系统环境
3. **编译器配置**：选择或浏览编译器路径
4. **工具配置**：配置烧录工具路径
5. **串口配置**：选择默认串口和波特率
6. **构建配置**：选择默认平台和优化级别
7. **验证配置**：检查配置的有效性
8. **保存配置**：保存配置到`mcu_config.json`文件

### 命令行配置工具

#### 功能概述

- **快速配置**：命令行界面，快速配置
- **批处理支持**：支持批处理脚本
- **配置导出**：导出配置为JSON文件
- **配置导入**：从JSON文件导入配置
- **配置验证**：验证配置的有效性
- **帮助信息**：详细的帮助文档

#### 使用示例

```bash
# 启动配置工具
python config_cli.py

# 快速配置
python config_cli.py --platform stm32 --optimization O2

# 导出配置
python config_cli.py --export config.json

# 导入配置
python config_cli.py --import config.json

# 验证配置
python config_cli.py --validate
```

## 友好的错误提示

### 错误分类

| 错误类型 | 错误代码 | 错误消息 | 解决方案 |
|---------|---------|---------|----------|
| 配置错误 | CONFIG_ERROR | 配置文件不存在或格式错误 | 运行配置向导重新配置 |
| 编译器错误 | COMPILER_ERROR | 编译器未找到或版本不兼容 | 安装正确版本的编译器 |
| 工具错误 | TOOL_ERROR | 烧录工具未找到或配置错误 | 安装和配置烧录工具 |
| 串口错误 | SERIAL_ERROR | 串口未找到或无法访问 | 检查串口连接和权限 |
| 硬件错误 | HARDWARE_ERROR | 硬件连接错误或设备未响应 | 检查硬件连接和电源 |
| 编译错误 | BUILD_ERROR | 代码编译失败 | 检查代码语法和依赖 |
| 烧录错误 | FLASH_ERROR | 固件烧录失败 | 检查烧录工具和连接 |
| 运行错误 | RUN_ERROR | 程序运行出错 | 检查代码逻辑和硬件 |

### 错误提示机制

#### 智能错误分析

```python
def analyze_error(error_message):
    """分析错误信息并提供解决方案"""
    error_patterns = {
        "error: #29: expected an expression": {
            "type": "BUILD_ERROR",
            "message": "语法错误：缺少表达式",
            "solution": "检查代码语法，确保所有语句都有正确的表达式"
        },
        "error: #167: unknown type name": {
            "type": "BUILD_ERROR",
            "message": "类型错误：未知类型名称",
            "solution": "检查头文件包含，确保所有类型都已定义"
        },
        "error: #102: unknown identifier": {
            "type": "BUILD_ERROR",
            "message": "标识符错误：未知标识符",
            "solution": "检查变量和函数名是否正确拼写"
        },
        "error: failed to open port": {
            "type": "SERIAL_ERROR",
            "message": "串口错误：无法打开串口",
            "solution": "检查串口连接和权限，确保串口未被其他程序占用"
        },
        "error: device not found": {
            "type": "HARDWARE_ERROR",
            "message": "硬件错误：设备未找到",
            "solution": "检查硬件连接和电源，确保设备已正确连接"
        }
    }
    
    for pattern, info in error_patterns.items():
        if pattern in error_message:
            return info
    
    return {
        "type": "UNKNOWN_ERROR",
        "message": "未知错误",
        "solution": "请检查错误信息并参考相关文档"
    }
```

#### 错误提示界面

```python
def show_error_message(error_info):
    """显示友好的错误提示"""
    print(f"\n[错误] {error_info['message']}")
    print(f"[类型] {error_info['type']}")
    print(f"[解决方案] {error_info['solution']}")
    print("\n[建议操作]")
    print("1. 检查相关配置")
    print("2. 参考文档中的故障排除部分")
    print("3. 运行环境检测脚本验证环境")
```

### 交互式错误处理

#### 错误恢复建议

```python
def suggest_recovery(error_type):
    """根据错误类型提供恢复建议"""
    recovery_suggestions = {
        "CONFIG_ERROR": [
            "运行配置向导: python config_wizard.py",
            "检查配置文件权限",
            "恢复默认配置: python config_cli.py --reset"
        ],
        "COMPILER_ERROR": [
            "安装编译器: 参考 docs/skill_integration.md",
            "配置编译器路径: python config_wizard.py",
            "检查编译器版本兼容性"
        ],
        "SERIAL_ERROR": [
            "检查串口连接",
            "重启设备",
            "检查串口驱动",
            "尝试其他串口"
        ],
        "HARDWARE_ERROR": [
            "检查硬件连接",
            "检查电源供应",
            "重置设备",
            "检查设备是否损坏"
        ],
        "BUILD_ERROR": [
            "检查代码语法",
            "检查头文件包含",
            "检查依赖项",
            "参考代码规范: docs/code_standards.md"
        ],
        "FLASH_ERROR": [
            "检查烧录工具配置",
            "检查设备连接",
            "重置设备",
            "尝试降低烧录速度"
        ],
        "RUN_ERROR": [
            "检查代码逻辑",
            "检查硬件连接",
            "使用调试工具排查",
            "参考调试指南: docs/debug_tools.md"
        ]
    }
    
    return recovery_suggestions.get(error_type, ["参考文档中的故障排除部分"])
```

## 用户界面改进

### 交互流程优化

#### 简化的命令流程

1. **项目初始化**：`python init_project.py <项目名称>`
2. **环境配置**：`python config_wizard.py`
3. **代码编译**：`make`
4. **固件烧录**：`python flash.py <平台> <固件文件>`
5. **项目测试**：`python test_project.py`
6. **问题排查**：`python troubleshoot.py`

#### 交互式菜单

```python
def show_main_menu():
    """显示主菜单"""
    print("\n=== MCU开发工具菜单 ===")
    print("1. 项目初始化")
    print("2. 环境配置")
    print("3. 代码编译")
    print("4. 固件烧录")
    print("5. 项目测试")
    print("6. 问题排查")
    print("7. 环境检测")
    print("8. 退出")
    
    choice = input("请选择操作 (1-8): ")
    return choice

def main_menu():
    """主菜单处理"""
    while True:
        choice = show_main_menu()
        
        if choice == "1":
            project_name = input("请输入项目名称: ")
            subprocess.run(["python", "init_project.py", project_name])
        elif choice == "2":
            subprocess.run(["python", "config_wizard.py"])
        elif choice == "3":
            subprocess.run(["make"])
        elif choice == "4":
            platform = input("请输入平台 (stm32/gd32/hc32/mm32/c51): ")
            firmware = input("请输入固件文件路径: ")
            subprocess.run(["python", "flash.py", platform, firmware])
        elif choice == "5":
            subprocess.run(["python", "test_project.py"])
        elif choice == "6":
            subprocess.run(["python", "troubleshoot.py"])
        elif choice == "7":
            subprocess.run(["python", "env_check.py"])
        elif choice == "8":
            print("退出...")
            break
        else:
            print("无效选择，请重新输入")
```

### 进度反馈

#### 编译进度

```python
def compile_with_progress():
    """带进度反馈的编译"""
    print("开始编译...")
    
    # 模拟编译过程
    steps = [
        "检查依赖",
        "预处理代码",
        "编译源代码",
        "链接目标文件",
        "生成固件文件",
        "验证固件文件"
    ]
    
    for i, step in enumerate(steps):
        print(f"[{i+1}/{len(steps)}] {step}...")
        # 模拟处理时间
        time.sleep(0.5)
    
    print("编译完成！")
```

#### 烧录进度

```python
def flash_with_progress(firmware, platform):
    """带进度反馈的烧录"""
    print(f"烧录 {firmware} 到 {platform} 平台...")
    
    # 模拟烧录过程
    steps = [
        "连接设备",
        "擦除闪存",
        "写入固件",
        "验证固件",
        "重置设备",
        "完成烧录"
    ]
    
    for i, step in enumerate(steps):
        print(f"[{i+1}/{len(steps)}] {step}...")
        # 模拟处理时间
        time.sleep(0.8)
    
    print("烧录完成！")
```

## 智能助手集成

### 命令自动补全

```python
def setup_autocomplete():
    """设置命令自动补全"""
    import readline
    
    # 命令补全列表
    commands = [
        "init_project", "config_wizard", "flash", "test_project",
        "troubleshoot", "env_check", "make", "make clean"
    ]
    
    # 平台补全列表
    platforms = ["stm32", "gd32", "hc32", "mm32", "c51"]
    
    def complete(text, state):
        """补全函数"""
        # 分割输入行
        line = readline.get_line_buffer().split()
        
        # 根据命令位置提供补全
        if len(line) == 1:
            # 补全命令
            matches = [c for c in commands if c.startswith(text)]
        elif len(line) == 2 and line[0] == "flash":
            # 补全平台
            matches = [p for p in platforms if p.startswith(text)]
        else:
            matches = []
        
        return matches[state] if state < len(matches) else None
    
    # 设置补全函数
    readline.set_completer(complete)
    readline.parse_and_bind('tab: complete')
```

### 上下文感知帮助

```python
def get_context_help(command):
    """根据命令提供上下文帮助"""
    help_texts = {
        "init_project": "初始化新项目，用法: init_project <项目名称>",
        "config_wizard": "配置开发环境，图形化界面",
        "flash": "烧录固件到设备，用法: flash <平台> <固件文件>",
        "test_project": "测试项目功能",
        "troubleshoot": "排查项目问题",
        "env_check": "检测开发环境",
        "make": "编译项目",
        "make clean": "清理编译产物"
    }
    
    return help_texts.get(command, "未知命令")

def show_help():
    """显示帮助信息"""
    print("\n=== 帮助信息 ===")
    print("可用命令:")
    for command, help_text in {
        "init_project": "初始化新项目",
        "config_wizard": "配置开发环境",
        "flash": "烧录固件",
        "test_project": "测试项目",
        "troubleshoot": "排查问题",
        "env_check": "检测环境",
        "make": "编译项目",
        "make clean": "清理产物"
    }.items():
        print(f"  {command}: {help_text}")
    print("\n输入 'help <命令>' 获取详细帮助")
```

## 常见问题自动检测

### 问题检测脚本

```python
def detect_common_issues():
    """检测常见问题"""
    print("检测常见问题...")
    
    issues = []
    
    # 检查编译器
    try:
        result = subprocess.run(["arm-none-eabi-gcc", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            issues.append({
                "type": "COMPILER_ERROR",
                "message": "ARM编译器未安装或未在PATH中",
                "solution": "安装ARM编译器并添加到PATH"
            })
    except Exception:
        issues.append({
            "type": "COMPILER_ERROR",
            "message": "ARM编译器未安装",
            "solution": "安装ARM编译器"
        })
    
    # 检查烧录工具
    try:
        result = subprocess.run(["openocd", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            issues.append({
                "type": "TOOL_ERROR",
                "message": "OpenOCD未安装或未在PATH中",
                "solution": "安装OpenOCD并添加到PATH"
            })
    except Exception:
        issues.append({
            "type": "TOOL_ERROR",
            "message": "OpenOCD未安装",
            "solution": "安装OpenOCD"
        })
    
    # 检查串口
    try:
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            issues.append({
                "type": "SERIAL_ERROR",
                "message": "未发现串口设备",
                "solution": "连接串口设备"
            })
    except ImportError:
        issues.append({
            "type": "DEPENDENCY_ERROR",
            "message": "pyserial未安装",
            "solution": "pip install pyserial"
        })
    
    # 检查配置文件
    if not os.path.exists("mcu_config.json"):
        issues.append({
            "type": "CONFIG_ERROR",
            "message": "配置文件不存在",
            "solution": "运行配置向导生成配置文件"
        })
    
    return issues

def main():
    """主函数"""
    issues = detect_common_issues()
    
    if issues:
        print("\n发现以下问题:")
        for i, issue in enumerate(issues):
            print(f"\n{i+1}. [{issue['type']}] {issue['message']}")
            print(f"   解决方案: {issue['solution']}")
        
        print("\n建议运行环境检测脚本获取详细信息:")
        print("   python env_check.py")
    else:
        print("\n未发现常见问题，环境正常！")
```

## 个性化设置

### 用户偏好配置

```json
{
  "preferences": {
    "editor": "vscode",
    "theme": "dark",
    "font_size": 12,
    "auto_save": true,
    "show_line_numbers": true
  },
  "build": {
    "default_platform": "stm32",
    "optimization": "O2",
    "generate_hex": true,
    "generate_bin": true
  },
  "flash": {
    "default_port": "COM3",
    "default_baudrate": 115200,
    "verify_after_flash": true,
    "reset_after_flash": true
  },
  "debug": {
    "enable_debug": true,
    "debug_level": "info",
    "log_file": "debug.log"
  }
}
```

### 快捷命令配置

```json
{
  "shortcuts": {
    "build": "make",
    "clean": "make clean",
    "flash": "python flash.py stm32 app.hex",
    "test": "python test_project.py",
    "config": "python config_wizard.py",
    "check": "python env_check.py"
  }
}
```

## 最佳实践

1. **简化操作**：提供简化的命令和脚本，减少用户操作步骤
2. **友好提示**：提供清晰、详细的错误提示和解决方案
3. **自动检测**：自动检测环境问题并提供修复建议
4. **进度反馈**：提供操作进度反馈，增强用户体验
5. **个性化设置**：允许用户自定义配置，适应不同需求
6. **智能补全**：提供命令自动补全，减少输入错误
7. **上下文帮助**：根据当前操作提供相关帮助信息
8. **错误恢复**：提供错误恢复建议，帮助用户快速解决问题
9. **一致性**：保持界面和操作的一致性，减少学习成本
10. **文档完善**：提供详细的文档和使用指南

## 示例使用场景

### 场景1：新项目创建

1. **用户**：运行 `python init_project.py my_project`
2. **系统**：创建项目结构，显示创建进度
3. **用户**：运行 `python config_wizard.py`
4. **系统**：启动图形化配置向导，自动检测环境
5. **用户**：配置编译器和工具路径
6. **系统**：验证配置，保存到配置文件
7. **用户**：运行 `make`
8. **系统**：编译项目，显示编译进度
9. **用户**：运行 `python flash.py stm32 app.hex`
10. **系统**：烧录固件，显示烧录进度
11. **用户**：运行 `python test_project.py`
12. **系统**：测试项目功能，显示测试结果

### 场景2：问题排查

1. **用户**：编译失败，收到错误提示
2. **系统**：分析错误信息，提供解决方案
3. **用户**：运行 `python troubleshoot.py`
4. **系统**：检测常见问题，提供修复建议
5. **用户**：按照建议修复问题
6. **系统**：验证修复结果，确认问题解决

### 场景3：环境配置

1. **用户**：运行 `python env_check.py`
2. **系统**：检测环境，显示检测结果
3. **用户**：运行 `python config_wizard.py`
4. **系统**：启动配置向导，根据检测结果提供建议
5. **用户**：调整配置参数
6. **系统**：验证配置，保存到配置文件
7. **用户**：运行 `make` 测试配置
8. **系统**：编译成功，确认环境配置正确