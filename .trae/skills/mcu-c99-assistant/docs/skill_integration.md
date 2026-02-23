# 技能集成与环境检测

## 技能集成步骤

### 手动集成

1. **下载技能**：从GitHub或其他来源下载mcu-c99-assistant技能包
2. **放置技能**：将技能包解压到Trae技能目录
   - 全局目录：`C:\Users\用户名\.trae-cn\skills`
   - 项目目录：`项目根目录\.trae\skills`
3. **注册技能**：运行Trae IDE，技能会自动注册
4. **验证集成**：在Trae IDE中查看技能是否显示在技能列表中

### 自动集成

使用`auto_load_skills.py`脚本自动加载技能：

```bash
# 从指定路径加载技能
python auto_load_skills.py --path "E:\path\to\skills"

# 加载到全局目录
python auto_load_skills.py --path "E:\path\to\skills" --global

# 从环境变量指定的目录加载
set TRAE_SKILLS_DIR="E:\path\to\skills"
python auto_load_skills.py
```

## 环境检测机制

### 系统环境检测规范

- **Python环境**：检查Python版本是否满足要求（3.6+）
- **编译器环境**：检查ARM Cortex-M编译器、8051编译器等是否安装
- **构建工具**：检查Make、CMake等构建工具是否安装
- **烧录工具**：检查OpenOCD、ST-Link等烧录工具是否安装
- **串口设备**：检查串口设备是否存在
- **Trae目录**：检查全局和项目技能目录是否存在

### 环境检测流程

1. **系统信息收集**：收集操作系统和架构信息
2. **依赖检查**：检查必要的依赖是否安装
3. **工具检查**：检查编译和烧录工具是否可用
4. **目录检查**：检查必要的目录是否存在
5. **结果报告**：生成环境检测报告
6. **修复建议**：提供环境问题的修复建议

### 依赖管理

#### Python依赖

```bash
# 安装必要的Python依赖
pip install pyserial
pip install pyusb
pip install pywin32  # Windows系统
```

#### 编译器依赖

| 平台 | 编译器 | 下载地址 |
|------|--------|----------|
| ARM Cortex-M | arm-none-eabi-gcc | [ARM官网](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) |
| 8051 | SDCC | [SDCC官网](https://sdcc.sourceforge.net/) |
| 通用C | GCC | [MinGW](https://sourceforge.net/projects/mingw/) (Windows) / 系统自带 (Linux) |

#### 烧录工具依赖

| 工具 | 用途 | 下载地址 |
|------|------|----------|
| OpenOCD | 开源调试烧录工具 | [OpenOCD官网](https://openocd.org/) |
| ST-Link Utility | STM32烧录工具 | [ST官网](https://www.st.com/en/development-tools/stsw-link004.html) |
| STC-ISP | STC单片机烧录工具 | [STC官网](http://www.stcmcu.com/) |
| GD-Link Utility | GD32烧录工具 | [GD官网](https://www.gigadevice.com/) |

## 技能加载机制

### 自动加载流程

1. **启动检测**：Trae IDE启动时扫描技能目录
2. **技能发现**：查找包含SKILL.md和_meta.json的目录
3. **元数据解析**：读取_meta.json文件获取技能信息
4. **关键词提取**：从description字段和keywords数组提取触发关键词
5. **技能注册**：将技能注册到系统中
6. **触发配置**：根据关键词设置触发条件

### 手动加载流程

1. **技能放置**：将技能目录复制到技能目录
2. **刷新技能**：在Trae IDE中点击"刷新技能"按钮
3. **验证加载**：检查技能是否出现在技能列表中

## 环境配置向导

### 配置文件

```json
{
  "compilers": {
    "arm-none-eabi-gcc": "C:\\Program Files (x86)\\GNU Arm Embedded Toolchain\\10 2021.10\\bin\\arm-none-eabi-gcc.exe",
    "sdcc": "C:\\SDCC\\bin\\sdcc.exe",
    "gcc": "C:\\MinGW\\bin\\gcc.exe"
  },
  "tools": {
    "openocd": "C:\\OpenOCD\\bin\\openocd.exe",
    "st-flash": "C:\\ST-Link Utility\\ST-Link Utility\\ST-Link_CLI.exe"
  },
  "serial": {
    "default_port": "COM3",
    "default_baudrate": 115200
  },
  "build": {
    "default_platform": "stm32",
    "optimization": "O2"
  }
}
```

### 配置向导规范

- **界面设计**：提供直观的图形化界面
- **配置项**：包括编译器路径、工具路径、串口设置、构建配置等
- **自动检测**：自动检测已安装的工具和可用的串口
- **验证机制**：验证配置的有效性
- **保存机制**：将配置保存到配置文件
- **加载机制**：从配置文件加载现有配置

### 配置向导流程

1. **启动向导**：用户启动配置向导
2. **环境检测**：自动检测系统环境和已安装的工具
3. **配置输入**：用户输入或选择配置项
4. **配置验证**：验证配置的有效性
5. **保存配置**：将配置保存到配置文件
6. **应用配置**：应用配置到开发环境

## 技能集成测试

### 技能集成测试规范

- **结构测试**：测试技能目录结构是否完整
- **文件测试**：测试必要文件是否存在
- **元数据测试**：测试_meta.json文件是否有效
- **关键词测试**：测试关键词是否完整
- **加载测试**：测试技能是否能正常加载
- **功能测试**：测试技能功能是否正常

### 测试流程

1. **结构检查**：检查技能目录结构和必要文件
2. **元数据验证**：验证_meta.json文件的格式和内容
3. **关键词检查**：检查关键词的数量和质量
4. **加载测试**：测试技能的加载过程
5. **功能验证**：验证技能的功能是否正常
6. **结果报告**：生成测试结果报告

## 故障排除

### 技能加载失败

1. **检查文件结构**：确保技能目录包含SKILL.md和_meta.json文件
2. **检查文件格式**：确保_meta.json格式正确，无语法错误
3. **检查权限**：确保技能目录有读取权限
4. **检查路径**：确保技能放置在正确的目录中
5. **刷新技能**：在Trae IDE中点击"刷新技能"按钮

### 环境检测失败

1. **检查依赖**：确保所有必要的依赖都已安装
2. **检查路径**：确保编译器和工具的路径正确配置
3. **检查权限**：确保有执行编译器和工具的权限
4. **检查网络**：某些工具可能需要网络连接
5. **检查系统**：确保操作系统版本兼容

### 编译失败

1. **检查代码**：确保代码语法正确，符合C99标准
2. **检查配置**：确保Makefile配置正确
3. **检查依赖**：确保所有必要的头文件和库都已包含
4. **检查编译器**：确保编译器版本兼容
5. **检查错误信息**：根据错误信息定位问题

### 烧录失败

1. **检查连接**：确保调试器或串口连接正确
2. **检查驱动**：确保调试器驱动已安装
3. **检查设备**：确保目标设备电源正常
4. **检查固件**：确保固件文件格式正确
5. **检查工具**：确保烧录工具配置正确

## 最佳实践

1. **定期更新**：定期更新技能和依赖
2. **备份配置**：备份环境配置文件
3. **版本控制**：使用Git管理技能代码
4. **文档更新**：及时更新技能文档
5. **测试验证**：定期测试技能功能
6. **错误处理**：完善错误处理和日志记录
7. **用户反馈**：收集用户反馈，持续改进
8. **安全考虑**：确保技能安全，防止恶意代码