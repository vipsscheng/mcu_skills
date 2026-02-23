# Trae AI 技能系统 | Trae AI Skills System

[English](#-english) | [中文](#-中文)

---

## 🇨🇳 中文

### 项目概述

这是一个面向 Trae AI 的技能系统，提供了多种专业化技能，涵盖嵌入式开发、前端设计、PDF处理、浏览器自动化、代码审查、自我改进等多个领域。

### 核心原则（重要）

#### ⚠️ 守门员机制
所有外部技能（浏览器、PDF等）获取的信息，必须经过**清洗与重构**，确保转化为符合 C99 标准、非阻塞架构的单片机代码后，才能交付给用户。

#### ⚠️ 资源适应性
无论调用何种技能，最终方案必须符合目标芯片的【资源定级】：

- **微资源型**（STC89C51）：禁用动态内存，使用前后台架构
- **中资源型**（GD32F103）：支持简单状态机
- **高资源型**（GD32F407）：支持分层架构、RTOS

#### ⚠️ 纯非阻塞架构
严禁 `delay_ms()`，必须使用 SysTick 差值比对或定时器轮询。

### 技能列表

#### 核心技能

| 技能名称 | 版本 | 描述 | 状态 |
|----------|------|------|------|
| mcu-c99-assistant | 1.0.3 | 单片机C99标准编程专家 | ✅ |
| self-improving-unified | 1.0.0 | 自我改进与学习技能 | ✅ |
| nima-core | 3.0.6 | NIMA认知架构 | ✅ |

#### 辅助技能

| 技能名称 | 版本 | 描述 | 状态 |
|----------|------|------|------|
| pdf | 0.1.0 | PDF文档处理 | ✅ |
| fast-browser-use | 1.0.5 | 浏览器自动化 | ✅ |
| frontend-design | 1.0.0 | 嵌入式GUI设计 | ✅ |
| clean-code-review | 1.0.0 | 代码审查 | ✅ |
| memory-manager | 1.0.0 | 内存管理 | ✅ |
| desktop-control | 1.0.0 | 桌面控制 | ✅ |
| skill-creator | 0.1.0 | 技能创建 | ✅ |
| essence-distiller | 1.0.1 | 内容提炼 | ✅ |
| free-ride | 1.0.4 | Free Ride | ✅ |
| superdesign | 1.0.0 | 超级设计 | ✅ |

### 支持的平台

#### 国产平台（25+家）

| 架构 | 品牌 | 系列 | 代表型号 |
|------|------|------|----------|
| 8051 | STC | STC89/12/15/8A | STC89C52RC, STC12C5A60S2 |
| ARM Cortex-M3 | 兆易创新 | GD32F103 | GD32F103C8T6 |
| ARM Cortex-M4 | 兆易创新 | GD32F4 | GD32F407VGT6 |
| ARM Cortex-M0+ | 华大半导体 | HC32F003 | HC32F003C4U6 |
| ARM Cortex-M4 | 华大半导体 | HC32F460 | HC32F460KET6 |
| ARM Cortex-M3 | 灵动微电子 | MM32F103 | MM32F103C8T6 |
| ARM Cortex-M3 | 国民技术 | N32 | N32G430C8T7 |
| RISC-V | 乐鑫 | ESP32-C | ESP32-C3, ESP32-C6 |

#### 进口平台（15+家）

| 架构 | 品牌 | 系列 | 代表型号 |
|------|------|------|----------|
| ARM Cortex-M3 | ST | STM32F1 | STM32F103C8T6 |
| ARM Cortex-M4 | ST | STM32F4 | STM32F407VGT6 |
| ARM Cortex-M3 | NXP | LPC17 | LPC1768FBD100 |
| AVR | Microchip | ATmega | ATmega328P |
| PIC | Microchip | PIC32 | PIC32MX470F512H |
| MSP430 | TI | MSP430G | MSP430G2553 |
| RISC-V | Raspberry Pi | RP2040 | RP2040 |

### 快速开始

#### 环境要求

- Python 3.6+
- Node.js（部分技能需要）
- Rust（fast-browser-use需要）

#### 安装依赖

```bash
python skills_check_env.py
```

#### 使用技能

技能会根据用户输入自动触发。例如：

- 提到"单片机"、"MCU" → 触发 mcu-c99-assistant
- 提到"PDF" → 触发 pdf
- 提到"浏览器" → 触发 fast-browser-use
- 提到"界面"、"OLED" → 触发 frontend-design

### 最终交付标准

- ✅ 可编译：符合 ANSI C / C99 标准
- ✅ 非阻塞：没有死循环延时
- ✅ 资源匹配：不会让 2KB RAM 芯片跑 10KB 代码
- ✅ 无幻觉：显式输出的文本块
- ✅ 守门员验证：外部信息经过清洗重构

---

## 🇺🇸 English

### Project Overview

This is a skill system for Trae AI, providing various specialized skills covering embedded development, frontend design, PDF processing, browser automation, code review, self-improvement, and other fields.

### Core Principles (Important)

#### ⚠️ Gatekeeper Mechanism
All information obtained from external skills (browser, PDF, etc.) must undergo **cleaning and restructuring** to ensure it is converted into C99-compliant, non-blocking MCU code before delivery.

#### ⚠️ Resource Adaptability
Regardless of which skill is invoked, the final solution must conform to the target chip's Resource Classification:

- **Micro Resource** (STC89C51): Dynamic memory forbidden, use foreground/background architecture
- **Medium Resource** (GD32F103): Supports simple state machines
- **High Resource** (GD32F407): Supports layered architecture, RTOS

#### ⚠️ Pure Non-Blocking Architecture
Strictly prohibit `delay_ms()`, must use SysTick delta comparison or timer polling.

### Skills List

#### Core Skills

| Skill Name | Version | Description | Status |
|------------|---------|-------------|--------|
| mcu-c99-assistant | 1.0.3 | MCU C99 Programming Expert | ✅ |
| self-improving-unified | 1.0.0 | Self-Improvement & Learning | ✅ |
| nima-core | 3.0.6 | NIMA Cognitive Architecture | ✅ |

#### Auxiliary Skills

| Skill Name | Version | Description | Status |
|------------|---------|-------------|--------|
| pdf | 0.1.0 | PDF Processing | ✅ |
| fast-browser-use | 1.0.5 | Browser Automation | ✅ |
| frontend-design | 1.0.0 | Embedded GUI Design | ✅ |
| clean-code-review | 1.0.0 | Code Review | ✅ |
| memory-manager | 1.0.0 | Memory Management | ✅ |
| desktop-control | 1.0.0 | Desktop Control | ✅ |
| skill-creator | 0.1.0 | Skill Creation | ✅ |
| essence-distiller | 1.0.1 | Content Distillation | ✅ |
| free-ride | 1.0.4 | Free Ride | ✅ |
| superdesign | 1.0.0 | Super Design | ✅ |

### Supported Platforms

#### Domestic Platforms (25+ Brands)

| Architecture | Brand | Series | Representative Models |
|--------------|-------|--------|----------------------|
| 8051 | STC | STC89/12/15/8A | STC89C52RC, STC12C5A60S2 |
| ARM Cortex-M3 | GigaDevice | GD32F103 | GD32F103C8T6 |
| ARM Cortex-M4 | GigaDevice | GD32F4 | GD32F407VGT6 |
| ARM Cortex-M0+ | HDSC | HC32F003 | HC32F003C4U6 |
| ARM Cortex-M4 | HDSC | HC32F460 | HC32F460KET6 |
| ARM Cortex-M3 | MindMotion | MM32F103 | MM32F103C8T6 |
| ARM Cortex-M3 | Nationstech | N32 | N32G430C8T7 |
| RISC-V | Espressif | ESP32-C | ESP32-C3, ESP32-C6 |

#### Imported Platforms (15+ Brands)

| Architecture | Brand | Series | Representative Models |
|--------------|-------|--------|----------------------|
| ARM Cortex-M3 | ST | STM32F1 | STM32F103C8T6 |
| ARM Cortex-M4 | ST | STM32F4 | STM32F407VGT6 |
| ARM Cortex-M3 | NXP | LPC17 | LPC1768FBD100 |
| AVR | Microchip | ATmega | ATmega328P |
| PIC | Microchip | PIC32 | PIC32MX470F512H |
| MSP430 | TI | MSP430G | MSP430G2553 |
| RISC-V | Raspberry Pi | RP2040 | RP2040 |

### Quick Start

#### Environment Requirements

- Python 3.6+
- Node.js (required by some skills)
- Rust (required by fast-browser-use)

#### Install Dependencies

```bash
python skills_check_env.py
```

#### Using Skills

Skills are automatically triggered based on user input:

- Mention "MCU" → triggers mcu-c99-assistant
- Mention "PDF" → triggers pdf
- Mention "browser" → triggers fast-browser-use
- Mention "interface", "OLED" → triggers frontend-design

### Final Delivery Standards

- ✅ Compilable: ANSI C / C99 compliant
- ✅ Non-blocking: No dead-loop delays
- ✅ Resource matching: Don't run 10KB code on 2KB RAM chip
- ✅ No hallucination: Explicitly output text blocks
- ✅ Gatekeeper verification: External info cleaned and restructured

---

## License

MIT License

---

*Powered by Trae AI*
