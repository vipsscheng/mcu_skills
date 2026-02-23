# Trae AI 技能系统

[English](./README_en.md) | 中文

## 项目概述

这是一个面向 Trae AI 的技能系统，提供了多种专业化技能，涵盖嵌入式开发、前端设计、PDF处理、浏览器自动化、代码审查、自我改进等多个领域。

---

## 核心原则（重要）

本技能系统的核心原则是**守门员机制**和**资源适应性**：

### 1. 守门员机制 ⚠️
所有外部技能（浏览器、PDF等）获取的信息，必须经过**清洗与重构**，确保转化为符合 C99 标准、非阻塞架构的单片机代码后，才能交付给用户。

### 2. 资源适应性 ⚠️
无论调用何种技能，最终方案必须符合目标芯片的【资源定级】：
- **微资源型**（STC89C51）：禁用动态内存，使用前后台架构
- **中资源型**（GD32F103）：支持简单状态机
- **高资源型**（GD32F407）：支持分层架构、RTOS

### 3. 纯非阻塞架构
严禁 `delay_ms()`，必须使用 SysTick 差值比对或定时器轮询。

---

## 技能列表

### 核心技能

| 技能名称 | 版本 | 描述 | 状态 |
|----------|------|------|------|
| **mcu-c99-assistant** | 1.0.3 | 单片机C99标准编程专家 | ✅ |
| **self-improving-unified** | 1.0.0 | 自我改进与学习技能 | ✅ |
| **nima-core** | 3.0.6 | NIMA认知架构 | ✅ |

### 辅助技能

| 技能名称 | 版本 | 描述 | 状态 |
|----------|------|------|------|
| **pdf** | 0.1.0 | PDF文档处理 | ✅ |
| **fast-browser-use** | 1.0.5 | 浏览器自动化 | ✅ |
| **frontend-design** | 1.0.0 | 嵌入式GUI设计 | ✅ |
| **clean-code-review** | 1.0.0 | 代码审查 | ✅ |
| **memory-manager** | 1.0.0 | 内存管理 | ✅ |
| **desktop-control** | 1.0.0 | 桌面控制 | ✅ |
| **skill-creator** | 0.1.0 | 技能创建 | ✅ |
| **essence-distiller** | 1.0.1 | 内容提炼 | ✅ |
| **free-ride** | 1.0.4 | Free Ride | ✅ |
| **superdesign** | 1.0.0 | 超级设计 | ✅ |

---

## mcu-c99-assistant - 单片机编程助手

**核心定位：单片机领域的总架构师与技术中枢**

### 主要功能

1. **项目搭建**：自动创建完整的项目结构
2. **代码编写**：符合C99标准、纯非阻塞架构
3. **调试支持**：基于"软硬协同立体排障思维"
4. **性能优化**：针对单片机资源进行定级
5. **技术咨询**：解答C99标准相关问题

### 支持的平台

#### 国产平台（25+家）

| 架构 | 品牌 | 系列 | 代表型号 |
|------|------|------|----------|
| 8051 | STC | STC89/12/15/8A | STC89C52RC、STC12C5A60S2、STC8A8K64S4A12 |
| ARM Cortex-M3 | 兆易创新 | GD32F103 | GD32F103C8T6、GD32F103RCT6 |
| ARM Cortex-M4 | 兆易创新 | GD32F4 | GD32F407VGT6、GD32F450RGT6 |
| ARM Cortex-M0+ | 华大半导体 | HC32F003 | HC32F003C4U6、HC32F003C6TA |
| ARM Cortex-M4 | 华大半导体 | HC32F460 | HC32F460KET6、HC32F460JET6 |
| ARM Cortex-M3 | 灵动微电子 | MM32F103 | MM32F103C8T6、MM32F103RCT6 |
| ARM Cortex-M0+ | 中微半导体 | CMS32F | CMS32F031C6T6、CMS32F051C8T6 |
| ARM Cortex-M3 | 士兰微 | SL32F | SL32F103C8T6、SL32F103RCT6 |
| ARM Cortex-M3 | 比亚迪半导体 | BY32F | BY32F103C8T6、BY32F103RCT6 |
| ARM Cortex-M3 | 华润微 | CR32F | CR32F103C8T6、CR32F103RCT6 |
| ARM Cortex-M3 | 国民技术 | N32 | N32G430C8T7、N32G431C8T7 |
| 8051 | 新唐科技 | N76E003 | N76E003、N76E885 |
| ARM Cortex-M0 | 上海贝岭 | BL702 | BL702、BL704 |
| 8051 | 南方科技 | STC | STC89C51、STC12C5A60S2 |
| MIPS | 北京君正 | X1000 | X1000、X1000E |
| RISC-V | 乐鑫 | ESP32-C | ESP32-C3、ESP32-C6 |
| RISC-V | 长江存储 | Xtacking | 存储控制器系列 |
| RISC-V | 合肥长鑫 | DDR | 内存控制器系列 |

#### 进口平台（15+家）

| 架构 | 品牌 | 系列 | 代表型号 |
|------|------|------|----------|
| ARM Cortex-M3 | ST | STM32F1 | STM32F103C8T6、STM32F103RCT6 |
| ARM Cortex-M4 | ST | STM32F4 | STM32F407VGT6、STM32F429IGT6 |
| ARM Cortex-M7 | ST | STM32F7 | STM32F767ZI、STM32F746ZG |
| ARM Cortex-M4 | ST | STM32L4 | STM32L476RG、STM32L496AG |
| ARM Cortex-M0+ | NXP | LPC8 | LPC812M101JDH20 |
| ARM Cortex-M3 | NXP | LPC17 | LPC1768FBD100、LPC1788FBD208 |
| ARM Cortex-M4 | NXP | K64 | MK64FN1M0VLQ12 |
| AVR | Microchip | ATmega | ATmega328P、ATmega2560 |
| PIC | Microchip | PIC16 | PIC16F877A、PIC16F18855 |
| PIC | Microchip | PIC32 | PIC32MX470F512H |
| MSP430 | TI | MSP430G | MSP430G2553、MSP430F5529 |
| C2000 | TI | TMS320F28 | TMS320F28035、TMS320F28335 |
| ARM Cortex-M4 | Infineon | XMC4000 | XMC4500、XMC4700 |
| ARM Cortex-M3 | Renesas | RX600 | RX63N、RX631 |
| RISC-V | Raspberry Pi | RP2040 | RP2040 |

### 技能调用策略

本技能会自动调用其他辅助技能，**并对结果负责（守门员机制）**：

| 辅助技能 | 用途 | 过滤规则 |
|----------|------|----------|
| PDF技能 | 查看芯片手册 | 提取寄存器地址→转化为宏定义 |
| 浏览器技能 | 搜索技术资料 | Arduino/C++→重写为C99 |
| GUI技能 | 嵌入式界面设计 | LVGL/OLED/串口屏，非Web前端 |
| 自我改进 | 记录学习经验 | 硬件经验库 |

### 最终交付标准

无论调用了多少个外部技能，最终交付必须满足：
1. ✅ 可编译：符合 ANSI C / C99 标准
2. ✅ 非阻塞：没有死循环延时
3. ✅ 资源匹配：不会让 2KB RAM 芯片跑 10KB 代码
4. ✅ 无幻觉：显式输出的文本块
5. ✅ 守门员验证：外部信息经过清洗重构

---

## 项目结构

```
skills/
├── mcu-c99-assistant/           # 单片机编程助手（主技能）
│   ├── docs/                    # 文档目录（30+篇）
│   ├── SKILL.md                 # 技能定义
│   └── _meta.json              # 元数据
│
├── self-improving-unified/       # 自我改进技能
├── nima-core-3.0.6/             # NIMA认知架构
├── pdf-0.1.0/                   # PDF处理
├── fast-browser-use-1.0.5/       # 浏览器自动化
├── frontend-design-1.0.0/       # 嵌入式GUI设计
├── clean-code-review-1.0.0/      # 代码审查
├── memory-manager-1.0.0/         # 内存管理
├── desktop-control-1.0.0/        # 桌面控制
├── skill-creator-0.1.0/         # 技能创建
├── essence-distiller-1.0.1/      # 内容提炼
├── free-ride-1.0.4/             # Free Ride
└── superdesign-1.0.0/           # 超级设计
```

---

## 快速开始

### 环境要求

- Python 3.6+
- Node.js（部分技能需要）
- Rust（fast-browser-use需要）

### 安装依赖

```bash
python skills_check_env.py
```

### 使用技能

技能会根据用户输入自动触发。例如：

- 提到"单片机"、"MCU"、"GPIO"等 → 触发 mcu-c99-assistant
- 提到"PDF"、"处理PDF" → 触发 pdf
- 提到"浏览器"、"网页" → 触发 fast-browser-use
- 提到"界面"、"OLED"、"LVGL" → 触发 frontend-design（嵌入式GUI）
- 提到"错误"、"bug"、"修复" → 触发 self-improving-unified

---

## 工具脚本

### skills_check_env.py
技能环境检测与安装脚本。

```bash
python skills_check_env.py
```

### install_skills.py
统一技能安装脚本。

```bash
python install_skills.py
```

---

## 文档

- [单片机型号收集](./skills/mcu-c99-assistant/docs/comprehensive_mcu_models.md)
- [芯片手册摘要](./skills/mcu-c99-assistant/docs/chip_datasheet_summary.md)
- [芯片官方手册链接](./skills/mcu-c99-assistant/docs/chip_datasheets.md)

---

## 更新日志

### 2026-02-24
- mcu-c99-assistant 强化核心原则（守门员机制、资源适应性）
- 前端设计技能重新定位为"嵌入式GUI设计"
- 添加自我改进统一技能 self-improving-unified
- 添加 skills_check_env.py 环境检测脚本
- 完善所有技能的 metadata 配置

---

## 许可证

本项目基于 MIT 许可证开源。

---

*本项目由 Trae AI 驱动*
