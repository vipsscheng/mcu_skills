# 烧录工具配置

## 1. 烧录工具概述

### 1.1 常用烧录工具

| 烧录工具 | 适用范围 | 特点 |
|---------|---------|------|
| STC-ISP | STC 系列微控制器 | 专用烧录工具，通过串口烧录 |
| ST-Link | STM32 系列微控制器 | 官方烧录工具，支持 SWD/JTAG 接口 |
| J-Link | ARM Cortex 系列微控制器 | 高速烧录，支持多种接口 |
| CMSIS-DAP | ARM Cortex 系列微控制器 | 开源烧录协议，支持多种开发板 |
| AVRDUDE | AVR 系列微控制器 | 命令行烧录工具，支持多种编程器 |
| esptool.py | ESP8266/ESP32 | 专用烧录工具，通过串口烧录 |
| OpenOCD | 多种微控制器 | 开源烧录和调试工具 |
| st-flash | STM32 系列微控制器 | 命令行烧录工具 |

### 1.2 烧录接口

1. **串口**：最常用的烧录接口，通过 UART 协议烧录
2. **JTAG**：标准调试和烧录接口，支持 4/5/6 线模式
3. **SWD**：Serial Wire Debug，2 线接口，占用引脚少
4. **ICP**：In-Circuit Programming，在线编程
5. **ISP**：In-System Programming，在系统编程
6. **IAP**：In-Application Programming，应用内编程

## 2. STC-ISP 烧录工具

### 2.1 安装与配置

#### 安装 STC-ISP
1. 从 [STC官网](http://www.stcmcudata.com/STCISP/) 下载 STC-ISP 烧录工具
2. 解压到本地目录
3. 运行 `STC-ISP.exe`

#### 配置 STC-ISP
1. **选择单片机型号**：在 "单片机型号" 下拉菜单中选择目标 STC 微控制器型号
2. **选择串口**：在 "串口号" 下拉菜单中选择连接到目标板的串口
3. **设置波特率**：选择合适的波特率（如 115200）
4. **选择烧录文件**：点击 "打开程序文件" 按钮，选择要烧录的 hex 文件
5. **配置选项**：根据需要配置其他选项，如时钟选择、看门狗等

### 2.2 烧录流程

1. 连接目标板到计算机
2. 打开 STC-ISP 工具
3. 配置上述参数
4. 点击 "Download/下载" 按钮
5. 给目标板上电（或按复位按钮）
6. 等待烧录完成

### 2.3 常见问题

#### 无法连接到设备
- 检查串口连接是否正确
- 确认目标板已上电
- 检查串口驱动是否安装
- 尝试更换串口线

#### 烧录失败
- 确认选择了正确的单片机型号
- 尝试降低波特率
- 检查 hex 文件是否正确
- 确认目标板供电稳定

## 3. ST-Link 烧录工具

### 3.1 安装与配置

#### 安装 ST-Link 驱动
1. 从 [ST官网](https://www.st.com/en/development-tools/st-link-v2.html) 下载 ST-Link 驱动
2. 运行安装程序，按照提示完成安装
3. 安装完成后，连接 ST-Link 到计算机

#### 配置 ST-Link
1. 打开 STM32CubeProgrammer 工具
2. 选择 "ST-Link" 连接方式
3. 点击 "Connect" 按钮
4. 连接成功后，即可进行烧录操作

### 3.2 命令行烧录

#### 使用 st-flash 工具
```bash
# 烧录二进制文件
st-flash write project.bin 0x08000000

# 读取闪存内容
st-flash read output.bin 0x08000000 0x10000

# 擦除闪存
st-flash erase

# 烧录十六进制文件
st-flash --format ihex write project.hex
```

#### 使用 STM32CubeProgrammer 命令行
```bash
# 连接目标设备
STM32_Programmer_CLI -c port=SWD

# 烧录二进制文件
STM32_Programmer_CLI -c port=SWD -w project.bin 0x08000000

# 读取闪存内容
STM32_Programmer_CLI -c port=SWD -r output.bin 0x08000000 0x10000

# 擦除闪存
STM32_Programmer_CLI -c port=SWD -e all
```

### 3.3 IDE 集成烧录

#### Keil MDK 烧录配置
1. 打开项目选项
2. 在 "Debug" 选项卡中选择 "ST-Link Debugger"
3. 点击 "Settings" 按钮
4. 配置接口类型、速度等参数
5. 在 "Utilities" 选项卡中选择 "Use Target Driver for Flash Programming"
6. 选择 "ST-Link Debugger"
7. 点击 "Settings" 按钮，配置烧录选项
8. 点击 "OK" 保存配置

#### STM32CubeIDE 烧录配置
1. 打开项目配置
2. 在 "Run/Debug Configuration" 中选择 "STM32 Cortex-M C/C++ Application"
3. 配置烧录选项
4. 点击 "Run" 按钮开始烧录

## 4. J-Link 烧录工具

### 4.1 安装与配置

#### 安装 J-Link 驱动
1. 从 [Segger官网](https://www.segger.com/downloads/jlink/) 下载 J-Link 驱动
2. 运行安装程序，按照提示完成安装
3. 安装完成后，连接 J-Link 到计算机

#### 配置 J-Link
1. 打开 J-Link Commander 工具
2. 输入目标设备型号：`device STM32F401RE`
3. 选择接口：`interface SWD`
4. 设置速度：`speed 4000`
5. 连接目标设备：`connect`

### 4.2 命令行烧录

#### 使用 J-Link Commander
```bash
# 连接目标设备
JLinkExe -device STM32F401RE -if SWD -speed 4000 -autoconnect 1

# 烧录程序
> loadfile project.elf

# 重置设备
> r

# 运行程序
> g
```

#### 使用 J-Flash
1. 打开 J-Flash 工具
2. 选择目标设备型号
3. 选择烧录文件
4. 点击 "Program" 按钮开始烧录

### 4.3 IDE 集成烧录

#### Keil MDK 烧录配置
1. 打开项目选项
2. 在 "Debug" 选项卡中选择 "J-Link/J-Trace Cortex"
3. 点击 "Settings" 按钮
4. 配置接口类型、速度等参数
5. 在 "Utilities" 选项卡中选择 "Use Target Driver for Flash Programming"
6. 选择 "J-Link/J-Trace Cortex"
7. 点击 "Settings" 按钮，配置烧录选项
8. 点击 "OK" 保存配置

#### IAR Embedded Workbench 烧录配置
1. 打开项目选项
2. 在 "Debugger" 选项卡中选择 "J-Link/J-Trace"
3. 点击 "Setup" 按钮
4. 配置接口类型、速度等参数
5. 在 "Download" 选项卡中配置烧录选项
6. 点击 "OK" 保存配置

## 5. OpenOCD 烧录工具

### 5.1 安装与配置

#### 安装 OpenOCD
1. 从 [OpenOCD官网](https://openocd.org/) 下载 OpenOCD
2. 解压到本地目录
3. 将 OpenOCD 的 `bin` 目录添加到系统环境变量 `PATH`

#### 配置 OpenOCD
1. 创建配置文件（如 `stm32f4.cfg`）
2. 配置调试接口和目标设备

### 5.2 命令行烧录

#### 基本烧录命令
```bash
# 启动 OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg

# 在另一个终端中运行 telnet
 telnet localhost 4444

# 烧录程序
> program project.elf verify reset exit

# 擦除闪存
> erase

# 读取闪存
> dump_image output.bin 0x08000000 0x10000
```

#### 使用 GDB 烧录
```bash
# 启动 OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg

# 在另一个终端中运行 GDB
arm-none-eabi-gdb project.elf
> target remote :3333
> load
> reset
> quit
```

### 5.3 配置文件示例

#### STM32F4 配置文件
```cfg
# stm32f4.cfg

# 接口配置
source [find interface/stlink.cfg]

# 目标配置
source [find target/stm32f4x.cfg]

# 重置配置
reset_config srst_only
```

#### 自定义配置文件
```cfg
# custom.cfg

# 接口配置
interface stlink
stlink_vid_pid 0x0483 0x3748
stlink_device_desc "ST-Link/V2"

# 目标配置
target arm cortex_m

# 内存布局
flash bank stm32f4x 0x08000000 0x100000 0 0 0

# 重置配置
reset_config srst_only
```

## 6. 不同微控制器系列的烧录配置

### 6.1 STC 系列

#### 烧录工具
- **STC-ISP**：官方烧录工具
- **串口烧录**：通过串口进行烧录

#### 烧录流程
1. 连接目标板到计算机
2. 打开 STC-ISP 工具
3. 选择目标单片机型号
4. 选择串口号和波特率
5. 选择要烧录的 hex 文件
6. 点击 "Download/下载" 按钮
7. 给目标板上电（或按复位按钮）
8. 等待烧录完成

#### 示例配置
```
# STC-ISP 配置
- 单片机型号: STC89C52RC
- 串口号: COM3
- 波特率: 115200
- 程序文件: project.hex
- 时钟选择: 11.0592MHz
- 看门狗: 禁用
- 掉电检测: 禁用
- 低电压复位: 禁用
```

### 6.2 GD32 系列

#### 烧录工具
- **J-Link**：高速烧录
- **ST-Link**：兼容烧录
- **OpenOCD**：开源烧录

#### 烧录流程
1. 连接调试器到目标板
2. 打开烧录工具
3. 选择目标设备型号
4. 选择要烧录的文件
5. 开始烧录
6. 等待烧录完成

#### 命令行烧录示例
```bash
# 使用 J-Link 烧录
JLinkExe -device GD32F450IG -if SWD -speed 4000 -autoconnect 1
> loadfile project.elf
> r
> g

# 使用 OpenOCD 烧录
openocd -f interface/jlink.cfg -f target/gd32f4x.cfg
# 在 telnet 中执行
> program project.elf verify reset exit
```

### 6.3 HC32 系列

#### 烧录工具
- **J-Link**：高速烧录
- **CMSIS-DAP**：开源烧录

#### 烧录流程
1. 连接调试器到目标板
2. 打开烧录工具
3. 选择目标设备型号
4. 选择要烧录的文件
5. 开始烧录
6. 等待烧录完成

#### 命令行烧录示例
```bash
# 使用 J-Link 烧录
JLinkExe -device HC32F460 -if SWD -speed 4000 -autoconnect 1
> loadfile project.elf
> r
> g

# 使用 OpenOCD 烧录
openocd -f interface/jlink.cfg -f target/hc32f460.cfg
# 在 telnet 中执行
> program project.elf verify reset exit
```

### 6.4 MM32 系列

#### 烧录工具
- **J-Link**：高速烧录
- **ST-Link**：兼容烧录

#### 烧录流程
1. 连接调试器到目标板
2. 打开烧录工具
3. 选择目标设备型号
4. 选择要烧录的文件
5. 开始烧录
6. 等待烧录完成

#### 命令行烧录示例
```bash
# 使用 J-Link 烧录
JLinkExe -device MM32F103 -if SWD -speed 4000 -autoconnect 1
> loadfile project.elf
> r
> g

# 使用 st-flash 烧录
st-flash write project.bin 0x08000000
```

## 7. 烧录文件格式

### 7.1 常见烧录文件格式

| 文件格式 | 扩展名 | 特点 |
|---------|--------|------|
| Intel HEX | .hex | 文本格式，包含地址信息，适合串口烧录 |
| Binary | .bin | 二进制格式，直接存储数据，适合快速烧录 |
| ELF | .elf | 可执行链接格式，包含调试信息，适合调试 |
| Motorola S-record | .srec | 文本格式，包含地址信息，适合某些烧录工具 |

### 7.2 文件格式转换

#### HEX 转 BIN
```bash
# 使用 objcopy 转换
arm-none-eabi-objcopy -O binary project.hex project.bin

# 使用 IntelHex 库转换（Python）
pip install intelhex
python -c "from intelhex import IntelHex; ih = IntelHex('project.hex'); ih.tofile('project.bin', 'bin')"
```

#### ELF 转 HEX
```bash
# 使用 objcopy 转换
arm-none-eabi-objcopy -O ihex project.elf project.hex
```

#### ELF 转 BIN
```bash
# 使用 objcopy 转换
arm-none-eabi-objcopy -O binary project.elf project.bin
```

## 8. 烧录流程最佳实践

### 8.1 烧录前准备

1. **检查硬件连接**：确保烧录器与目标板连接正确
2. **确认目标板供电**：确保目标板供电稳定
3. **验证烧录文件**：确保烧录文件正确，无损坏
4. **备份原有程序**：如果需要，备份目标板上的原有程序
5. **关闭目标板上的其他设备**：避免干扰烧录过程

### 8.2 烧录过程

1. **选择合适的烧录工具**：根据目标微控制器选择合适的烧录工具
2. **配置烧录参数**：正确配置烧录工具的参数
3. **开始烧录**：启动烧录过程
4. **监控烧录进度**：观察烧录过程，确保无错误
5. **验证烧录结果**：烧录完成后，验证程序是否正确运行

### 8.3 烧录后验证

1. **复位设备**：烧录完成后，复位目标设备
2. **运行程序**：启动程序，观察是否正常运行
3. **测试功能**：测试程序的主要功能
4. **检查日志**：查看程序运行日志，确认无错误
5. **记录烧录信息**：记录烧录时间、版本等信息

## 9. 远程烧录

### 9.1 网络烧录

#### 使用 OpenOCD 远程烧录
```bash
# 在目标设备所在网络启动 OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg -c "bindto 0.0.0.0"

# 从远程计算机连接
arm-none-eabi-gdb project.elf
> target remote <target-ip>:3333
> load
> reset
> quit
```

#### 使用 J-Link GDB Server 远程烧录
```bash
# 在目标设备所在网络启动 J-Link GDB Server
JLinkGDBServer -device STM32F401RE -if SWD -speed 4000 -port 2331 -select usb

# 从远程计算机连接
arm-none-eabi-gdb project.elf
> target remote <target-ip>:2331
> load
> reset
> quit
```

### 9.2 IAP 烧录

#### IAP 原理
IAP（In-Application Programming）是一种在应用程序运行过程中更新固件的方法，通常通过串口、网络等方式接收新固件并写入闪存。

#### IAP 实现示例
```c
// IAP 主函数
int main(void) {
    // 初始化系统
    SystemInit();
    
    // 检查是否需要更新固件
    if (need_firmware_update()) {
        // 进入 IAP 模式
        iap_mode();
    } else {
        // 进入应用模式
        app_mode();
    }
}

// IAP 模式
void iap_mode(void) {
    // 初始化通信接口（如串口）
    uart_init();
    
    // 接收固件数据
    uint8_t firmware_buffer[FIRMWARE_SIZE];
    receive_firmware(firmware_buffer, FIRMWARE_SIZE);
    
    // 擦除闪存
    erase_flash(APP_START_ADDRESS, APP_SIZE);
    
    // 写入固件
    write_flash(APP_START_ADDRESS, firmware_buffer, FIRMWARE_SIZE);
    
    // 跳转到应用程序
    jump_to_app();
}

// 跳转到应用程序
void jump_to_app(void) {
    typedef void (*app_func)(void);
    app_func jump_to_application;
    
    // 设置应用程序入口地址
    jump_to_application = (app_func)(*(uint32_t*)(APP_START_ADDRESS + 4));
    
    // 设置栈指针
    __set_MSP(*(uint32_t*)APP_START_ADDRESS);
    
    // 跳转到应用程序
    jump_to_application();
}
```

## 10. 烧录工具自动化

### 10.1 脚本化烧录

#### 批处理脚本（Windows）
```batch
@echo off

REM 烧录脚本
set ST_LINK=st-flash
set FIRMWARE=project.bin
set ADDRESS=0x08000000

echo 正在烧录固件...
%ST_LINK% write %FIRMWARE% %ADDRESS%
echo 烧录完成！
pause
```

#### Shell 脚本（Linux/macOS）
```bash
#!/bin/bash

# 烧录脚本
ST_LINK=st-flash
FIRMWARE=project.bin
ADDRESS=0x08000000

echo "正在烧录固件..."
$ST_LINK write $FIRMWARE $ADDRESS
echo "烧录完成！"
```

### 10.2 CI/CD 集成

#### GitHub Actions 示例
```yaml
name: Build and Flash

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup ARM toolchain
      uses: fiam/arm-none-eabi-gcc@v1
      with:
        release: '10.3-2021.10'
    
    - name: Build firmware
      run: |
        make
    
    - name: Flash firmware
      if: github.ref == 'refs/heads/main'
      run: |
        # 安装 st-flash
        sudo apt-get install -y stlink-tools
        # 烧录固件
        st-flash write build/project.bin 0x08000000
```

#### GitLab CI 示例
```yaml
build_and_flash:
  stage: deploy
  image: ubuntu:latest
  script:
    - apt-get update && apt-get install -y build-essential arm-none-eabi-gcc make stlink-tools
    - make
    - st-flash write build/project.bin 0x08000000
  only:
    - main
```

## 11. 常见烧录问题和解决方案

### 11.1 烧录器无法连接

#### 问题原因
- 硬件连接问题
- 烧录器驱动未安装
- 目标设备未上电
- 接口配置错误

#### 解决方案
- 检查硬件连接
- 安装正确的驱动
- 确保目标设备已上电
- 检查接口配置

### 11.2 烧录失败

#### 问题原因
- 烧录文件错误
- 目标设备存储空间不足
- 闪存保护已启用
- 供电不稳定

#### 解决方案
- 检查烧录文件是否正确
- 确认目标设备存储空间足够
- 禁用闪存保护
- 确保供电稳定

### 11.3 烧录后程序无法运行

#### 问题原因
- 烧录文件错误
- 地址配置错误
- 程序存在bug
- 硬件问题

#### 解决方案
- 检查烧录文件是否正确
- 确认烧录地址配置正确
- 调试程序，查找bug
- 检查硬件是否正常

### 11.4 烧录速度慢

#### 问题原因
- 波特率设置过低
- 烧录文件过大
- 接口速度设置不当
- 烧录工具性能限制

#### 解决方案
- 提高波特率（串口烧录）
- 优化程序大小
- 提高接口速度（JTAG/SWD）
- 使用更高速的烧录工具

### 11.5 闪存擦除失败

#### 问题原因
- 闪存保护已启用
- 目标设备锁定
- 硬件问题
- 烧录工具不兼容

#### 解决方案
- 禁用闪存保护
- 解锁目标设备
- 检查硬件是否正常
- 使用兼容的烧录工具

## 12. 烧录工具维护

### 12.1 烧录器固件更新

#### ST-Link 固件更新
1. 从 [ST官网](https://www.st.com/en/development-tools/st-link-v2.html) 下载 ST-Link 固件更新工具
2. 运行固件更新工具
3. 连接 ST-Link 到计算机
4. 按照提示完成固件更新

#### J-Link 固件更新
1. 打开 J-Link Configurator 工具
2. 连接 J-Link 到计算机
3. 点击 "Update Firmware" 按钮
4. 按照提示完成固件更新

### 12.2 烧录器校准

#### 串口烧录校准
1. 确保串口线质量良好
2. 选择合适的波特率
3. 确保目标设备串口接收电路正常
4. 测试串口通信是否稳定

#### JTAG/SWD 校准
1. 确保 JTAG/SWD 连接线质量良好
2. 检查目标设备 JTAG/SWD 接口电路
3. 调整烧录工具的接口速度
4. 测试连接是否稳定

### 12.3 烧录工具故障排除

#### 烧录器不被识别
- 检查 USB 连接
- 重新安装驱动
- 尝试不同的 USB 端口
- 检查烧录器是否损坏

#### 烧录过程中断
- 检查供电是否稳定
- 确保连接电缆牢固
- 减少烧录文件大小
- 降低烧录速度

## 13. 总结

烧录工具配置是嵌入式系统开发中的重要环节，正确配置和使用烧录工具可以确保程序顺利烧录到目标设备中。本文档介绍了常用的烧录工具、不同微控制器系列的烧录配置、烧录流程和最佳实践以及常见问题和解决方案。

关键烧录技巧包括：

1. **选择合适的烧录工具**：根据目标微控制器选择合适的烧录工具。
2. **正确配置烧录参数**：确保烧录工具的参数配置正确。
3. **遵循烧录流程**：按照正确的流程进行烧录操作。
4. **验证烧录结果**：烧录完成后，验证程序是否正确运行。
5. **解决常见问题**：了解并解决常见的烧录问题。

通过正确使用烧录工具，可以确保程序顺利烧录到目标设备中，提高开发效率，减少问题发生。