# AI人工智能技能系统 | AI Skills System

[English](#-english) | [中文](#-中文)

---

## 中文

### 项目概述

这是一个 AI 的技能系统，提供了多种专业化技能，涵盖嵌入式开发、前端设计、PDF处理、浏览器自动化、代码审查、自我改进等多个领域。

### 核心原则（重要）

#### 门卫制度
技能获取的信息，必须经过清理和重构，确保转化为符合C99标准
#### 资源储备
双方征集技能，最终方案必须满足目标芯片的【资源定级】：

- **微资源型**（STC89C51）：禁止使用动态内存
- **中资源型**（GD32F103）：支持简单状态机
- **高资源型**（GD32F407）：支持分层架构和实时操作系统

#### 代码生成约束与规范 (主要是针对国产模型，强化Gmini与Claude)
- 代码生成的各种规范
- 阻止非架构要求
- C99标准合规
- 资源状况检查
- 无幻觉验证

#### 生成代码架构的优化
- 状态机架构
- 分层架构
- RTOS集成
- 功能模块化

#### 注释规则
- 功能注释
- 参数注释
- 返回值说明
- 关键注释
- 资源注释

### 最终交付标准
- 可编译：符合 ANSI C / C99 标准
- 符合注释：
- 资源匹配：不会让 2KB RAM 芯片跑 10KB 代码
- 无幻觉：显式输出的文本块
- 守门员验证：外部信息经过翻新重构

### 技能列表

#### 核心技能

| 技能名称 | 版本 | 描述 | 状态 |
|----------|------|------|------|
| mcu-c99 | 1.0.3 | 单片机C99标准编程专家 | OK |
| self-improving-unified | 1.0.0 | 自我改进与学习技能 | OK |
| nima-core | 3.0.6 | NIMA认知架构 | OK |

#### 辅助技能

| 技能名称 | 版本 | 描述 | 状态 |
|----------|------|------|------|
| pdf | 0.1.0 | PDF文档处理 | OK |
| fast-browser-use | 1.0.5 | 浏览器自动化 | OK |
| frontend-design | 1.0.0 | 嵌入式GUI设计 | OK |
| clean-code-review | 1.0.0 | 代码审查 | OK |
| memory-manager | 1.0.0 | 内存管理 | OK |
| desktop-control | 1.0.0 | 桌面控制 | OK |
| skill-creator | 0.1.0 | 技能创建 | OK |
| essence-distiller | 1.0.1 | 内容提炼 | OK |
| free-ride | 1.0.4 | Free Ride | OK |
| superdesign | 1.0.0 | 超级设计 | OK |

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
cd .trae
python skills_check_env.py
```

#### 使用技能

技能会根据用户输入自动触发。例如：

- 提到"单片机"、"MCU" -> 触发 mcu-c99-assistant
- 提到"PDF" -> 触发 pdf
- 提到"浏览器" -> 触发 fast-browser-use
- 提到"界面"、"OLED" -> 触发 frontend-design

### 推荐使用的 AI 模型

为获得最佳的单片机编程效果，推荐使用以下模型：

#### 首选模型（效果最好）

| 模型 | 说明 | 推荐方式 |
|------|------|----------|
| **Gemini 最新版** | 单片机编程效果优秀 | **API 密钥调用** |
| **Claude 最新版** | 单片机编程效果最佳 | **API 密钥调用** |

#### 重要说明

- **API 密钥调用 = 满血版**：只有通过 API 密钥调用的模型才能发挥完整能力
- **非 API 调用 = 残血版**：免费版、学生教育版、Pro 网页版等（非 API 调用）效果较差
- **国内调用注意事项**：
  - Gemini 和 Claude 在国内调用需要稳定的科学上网
  - 注意封号风险，建议使用稳定的网络环境
- **国产模型**：可以尝试使用，使用过程中有任何问题可以提交反馈，我会抓紧修复

---

## English

### Project Overview

This is an AI skill system that provides various specialized skills covering embedded development, frontend design, PDF processing, browser automation, code review, self-improvement, and other fields.

### Core Principles (Important)

#### Gatekeeper Mechanism
All information obtained from skills must be cleaned and restructured to ensure it is converted into C99-compliant standards.

#### Resource Reserve
Regardless of which skill is invoked, the final solution must conform to the target chip's Resource Classification:

- **Micro Resource** (STC89C51): Dynamic memory forbidden
- **Medium Resource** (GD32F103): Supports simple state machines
- **High Resource** (GD32F407): Supports layered architecture and real-time operating system

#### Code Generation Constraints and Standards (Mainly for Domestic Models, Enhanced for Gmini and Claude)
- Various code generation standards
- Block non-architecture requirements
- C99 standard compliance
- Resource status checks
- No-hallucination verification

#### Generated Code Architecture Optimization
- State machine architecture
- Layered architecture
- RTOS integration
- Functional modularity

#### Comment Rules
- Function comments
- Parameter comments
- Return value descriptions
- Key comments
- Resource comments

### Final Delivery Standards
- Compilable: Compliant with ANSI C / C99 standard
- Comment compliance
- Resource matching: Don't run 10KB code on 2KB RAM chip
- No hallucination: Explicitly output text blocks
- Gatekeeper verification: External info cleaned and restructured

### Skills List

#### Core Skills

| Skill Name | Version | Description | Status |
|------------|---------|-------------|--------|
| mcu-c99 | 1.0.3 | MCU C99 Programming Expert | OK |
| self-improving-unified | 1.0.0 | Self-Improvement and Learning | OK |
| nima-core | 3.0.6 | NIMA Cognitive Architecture | OK |

#### Auxiliary Skills

| Skill Name | Version | Description | Status |
|------------|---------|-------------|--------|
| pdf | 0.1.0 | PDF Processing | OK |
| fast-browser-use | 1.0.5 | Browser Automation | OK |
| frontend-design | 1.0.0 | Embedded GUI Design | OK |
| clean-code-review | 1.0.0 | Code Review | OK |
| memory-manager | 1.0.0 | Memory Management | OK |
| desktop-control | 1.0.0 | Desktop Control | OK |
| skill-creator | 0.1.0 | Skill Creation | OK |
| essence-distiller | 1.0.1 | Content Distillation | OK |
| free-ride | 1.0.4 | Free Ride | OK |
| superdesign | 1.0.0 | Super Design | OK |

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
cd .trae
python skills_check_env.py
```

#### Using Skills

Skills are automatically triggered based on user input:

- Mention "MCU" -> triggers mcu-c99-assistant
- Mention "PDF" -> triggers pdf
- Mention "browser" -> triggers fast-browser-use
- Mention "interface", "OLED" -> triggers frontend-design

### Recommended AI Models

For best MCU programming results, the following models are recommended:

#### Preferred Models (Best Performance)

| Model | Description | Recommended Usage |
|-------|-------------|-------------------|
| **Gemini Latest** | Excellent MCU programming performance | **API Key Call** |
| **Claude Latest** | Best MCU programming performance | **API Key Call** |

#### Important Notes

- **API Key Call = Full Version**: Only models called via API key can unleash full capabilities
- **Non-API Call = Crippled Version**: Free version, student/education version, Pro web version, etc. (non-API calls) have poor performance
- **China Access Notes**:
  - Gemini and Claude require stable VPN for access in China
  - Be aware of account suspension risk, recommend stable network environment
- **Domestic Models**: Can be tried, any issues encountered during use can be submitted for feedback, I will fix promptly

---

*Powered by AI*

## License

MIT License

---
