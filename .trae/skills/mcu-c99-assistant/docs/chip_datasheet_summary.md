# 芯片手册摘要与Demo资料

本文档收集了主流单片机芯片的手册摘要、关键参数、应用场景和Demo资料，为开发者提供参考。

## 意法半导体 (STMicroelectronics)

### STM32F103C8T6

#### 手册摘要
- **核心架构**：ARM Cortex-M3 32位RISC处理器
- **最大主频**：72 MHz
- **运算性能**：1.25 DMIPS/MHz (Dhrystone 2.1)
- **存储容量**：64 KB Flash，20 KB SRAM
- **外设资源**：
  - 2个12位ADC（最多16个外部通道）
  - 1个高级控制定时器(TIM1)，3个通用定时器(TIM2-TIM4)，2个基本定时器(TIM6-TIM7)
  - 3个USART，2个SPI，2个I2C，1个CAN，1个USB
  - 7通道DMA控制器
- **工作电压**：2.0~3.6V
- **封装**：LQFP-48

#### 应用场景
- 嵌入式系统
- 工业控制
- 医疗设备
- 机器人
- 物联网设备
- 智能传感器
- 自动化控制系统

#### Demo资料
- **基础例程**：GPIO控制、中断处理、定时器应用、串口通信
- **项目示例**：舵机测试仪、OLED显示、ADC采集
- **开发环境**：Keil MDK，需要安装Keil.STM32F1xx_DFP.2.3.0.pack支持包
- **资源链接**：[STM32F103C8T6例程资源](https://gitcode.com/Universal-Tool/b033d)

### STM32F407VGT6

#### 手册摘要
- **核心架构**：ARM Cortex-M4 32位处理器，带FPU
- **最大主频**：168 MHz
- **运算性能**：210 DMIPS/1.25 DMIPS/MHz
- **存储容量**：1 MB Flash，192 + 4 KB SRAM
- **外设资源**：
  - 3个12位ADC（最多24个外部通道）
  - 1个高级控制定时器(TIM1)，3个通用定时器(TIM2-TIM4)，2个基本定时器(TIM6-TIM7)，2个高级定时器(TIM8-TIM11)
  - 4个USART，3个SPI，2个I2C，2个CAN，1个USB OTG
  - 16通道DMA控制器
- **工作电压**：2.0~3.6V
- **封装**：LQFP-100

#### 应用场景
- 工业自动化
- 电机控制
- 人机界面
- 医疗设备
- 物联网网关
- 高端嵌入式系统

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、PWM
- **高级例程**：FreeRTOS、FATFS、USB HID
- **开发环境**：Keil MDK、STM32CubeIDE

## 兆易创新 (GD32)

### GD32F103C8T6

#### 手册摘要
- **核心架构**：ARM Cortex-M3 32位RISC处理器
- **最大主频**：72 MHz
- **运算性能**：1.25 DMIPS/MHz
- **存储容量**：64 KB Flash，20 KB SRAM
- **外设资源**：
  - 2个12位ADC（最多16个外部通道）
  - 1个高级控制定时器(TIMER1)，3个通用定时器(TIMER2-TIMER4)，2个基本定时器(TIMER5-TIMER6)
  - 3个USART，2个SPI，2个I2C，1个CAN，1个USB
  - 7通道DMA控制器
- **工作电压**：2.0~3.6V
- **封装**：LQFP-48

#### 应用场景
- 工业控制
- 消费电子
- 物联网设备
- 替代STM32F103系列

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、PWM
- **开发环境**：Keil MDK、GD32CubeIDE

## 微芯科技 (Microchip)

### ATmega328P

#### 手册摘要
- **核心架构**：8位AVR RISC处理器
- **最大主频**：20 MHz
- **运算性能**：20 MIPS @ 20 MHz
- **存储容量**：32 KB Flash，2 KB SRAM，1 KB EEPROM
- **外设资源**：
  - 10位ADC（8通道）
  - 2个8位定时器/计数器，1个16位定时器/计数器
  - 1个USART，1个SPI，1个I2C
  - 6个PWM通道
- **工作电压**：1.8~5.5V
- **封装**：DIP-28, TQFP-32, QFN-32

#### 应用场景
- Arduino UNO
- 小型嵌入式项目
- 传感器节点
- 消费电子
- 教育实验

#### Demo资料
- **Arduino库**：丰富的Arduino库支持
- **基础例程**：GPIO、UART、SPI、I2C、ADC、PWM
- **开发环境**：Arduino IDE、Atmel Studio

### PIC16F877A

#### 手册摘要
- **核心架构**：8位PIC RISC处理器
- **最大主频**：20 MHz
- **运算性能**：5 MIPS @ 20 MHz
- **存储容量**：14 KB Flash，368 bytes SRAM，256 bytes EEPROM
- **外设资源**：
  - 10位ADC（8通道）
  - 3个定时器/计数器
  - 1个USART，1个SPI，1个I2C
  - 4个PWM通道
- **工作电压**：4.0~5.5V
- **封装**：DIP-40, TQFP-44

#### 应用场景
- 工业控制
- 自动化设备
- 仪器仪表
- 消费电子

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、PWM
- **开发环境**：MPLAB X IDE、XC8编译器

## 德州仪器 (TI)

### MSP430G2553

#### 手册摘要
- **核心架构**：16位RISC处理器
- **最大主频**：16 MHz
- **运算性能**：16 MIPS @ 16 MHz
- **存储容量**：16 KB Flash，512 bytes SRAM
- **外设资源**：
  - 10位ADC（8通道）
  - 2个16位定时器
  - 1个USART，1个SPI，1个I2C
- **工作电压**：1.8~3.6V
- **封装**：TSSOP-20, QFN-20

#### 应用场景
- 低功耗应用
- 便携医疗设备
- 传感器节点
- 电池供电设备

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、低功耗模式
- **开发环境**：Code Composer Studio、IAR Embedded Workbench

## 恩智浦 (NXP)

### LPC1768

#### 手册摘要
- **核心架构**：ARM Cortex-M3 32位处理器
- **最大主频**：100 MHz
- **运算性能**：1.25 DMIPS/MHz
- **存储容量**：512 KB Flash，64 KB SRAM
- **外设资源**：
  - 12位ADC（8通道）
  - 4个定时器，1个 watchdog 定时器
  - 4个UART，2个SPI，2个I2C，1个CAN
  - 2个I2S接口
- **工作电压**：2.0~3.6V
- **封装**：LQFP-100

#### 应用场景
- 工业控制
- 通信设备
- 人机界面
- 汽车电子

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、PWM
- **开发环境**：Keil MDK、LPCXpresso IDE

## 树莓派 (Raspberry Pi)

### RP2040

#### 手册摘要
- **核心架构**：双核心ARM Cortex-M0+ 32位处理器
- **最大主频**：133 MHz
- **存储容量**：264 KB SRAM
- **外设资源**：
  - 12位ADC（4通道）
  - 8个可编程I/O（PIO）状态机
  - 2个UART，2个SPI，2个I2C
  - 16个PWM通道
- **工作电压**：1.8~3.3V
- **封装**：QFN-56

#### 应用场景
- 树莓派Pico开发板
- 物联网设备
- 传感器节点
- 嵌入式控制系统
- 教育实验

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、PWM
- **SDK**：Raspberry Pi Pico SDK
- **开发环境**：C/C++、MicroPython

## 乐鑫 (Espressif)

### ESP32-C3

#### 手册摘要
- **核心架构**：RISC-V 32位处理器
- **最大主频**：160 MHz
- **存储容量**：400 KB SRAM，内置Flash
- **外设资源**：
  - 12位ADC（6通道）
  - 2个定时器
  - 1个UART，2个SPI，1个I2C
  - WiFi 802.11 b/g/n，蓝牙5.0
- **工作电压**：3.0~3.6V
- **封装**：QFN-32

#### 应用场景
- 物联网设备
- WiFi/蓝牙网关
- 智能家电
- 传感器网络

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、WiFi、蓝牙
- **SDK**：ESP-IDF
- **开发环境**：ESP-IDF、Arduino IDE

## 中微半导体 (CMS)

### CMS32F031C6T6

#### 手册摘要
- **核心架构**：ARM Cortex-M0 32位处理器
- **最大主频**：48 MHz
- **存储容量**：32 KB Flash，4 KB SRAM
- **外设资源**：
  - 12位ADC（10通道）
  - 3个定时器
  - 1个UART，1个SPI，1个I2C
- **工作电压**：2.4~3.6V
- **封装**：LQFP-48

#### 应用场景
- 消费电子
- 家电控制
- 传感器节点

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC
- **开发环境**：Keil MDK

## 华大半导体 (HC32)

### HC32F460KET6

#### 手册摘要
- **核心架构**：ARM Cortex-M4 32位处理器，带FPU
- **最大主频**：180 MHz
- **存储容量**：512 KB Flash，128 KB SRAM
- **外设资源**：
  - 12位ADC（24通道）
  - 8个定时器
  - 4个UART，3个SPI，2个I2C，2个CAN
  - 2个USB
- **工作电压**：2.7~3.6V
- **封装**：LQFP-64

#### 应用场景
- 工业控制
- 电机驱动
- 电力电子
- 通信设备

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、PWM
- **开发环境**：Keil MDK、HC32 IDE

## 灵动微电子 (MM32)

### MM32F103C8T6

#### 手册摘要
- **核心架构**：ARM Cortex-M3 32位处理器
- **最大主频**：72 MHz
- **存储容量**：64 KB Flash，20 KB SRAM
- **外设资源**：
  - 2个12位ADC（16通道）
  - 4个定时器
  - 3个UART，2个SPI，2个I2C，1个CAN
- **工作电压**：2.0~3.6V
- **封装**：LQFP-48

#### 应用场景
- 工业控制
- 消费电子
- 替代STM32F103系列

#### Demo资料
- **基础例程**：GPIO、UART、SPI、I2C、ADC、PWM
- **开发环境**：Keil MDK

## 总结

本文档收集了主流单片机芯片的手册摘要和Demo资料，为开发者提供参考。随着技术的不断发展，芯片型号和资料会不断更新，建议开发者参考各厂商的官方网站获取最新信息。

### 选型建议
1. **根据应用需求**：选择合适的性能、功耗和功能
2. **考虑开发资源**：选择有完善开发工具和技术支持的平台
3. **评估供应链**：选择供货稳定的型号
4. **参考社区支持**：选择有活跃社区和丰富资源的平台
5. **成本预算**：平衡性能和成本需求

通过本文档的参考，开发者可以快速了解不同芯片的特性和应用场景，选择最适合自己项目的单片机型号。