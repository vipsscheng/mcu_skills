# Trae AI Skills System

[English](./README_en.md) | [中文](./README.md)

## Project Overview

This is a skill system for Trae AI, providing various specialized skills covering embedded development, frontend design, PDF processing, browser automation, code review, self-improvement, and other fields.

---

## Core Principles (Important)

The core principles of this skill system are **Gatekeeper Mechanism** and **Resource Adaptability**:

### 1. Gatekeeper Mechanism ⚠️
All information obtained from external skills (browser, PDF, etc.) must undergo **cleaning and restructuring** to ensure it is converted into C99-compliant, non-blocking MCU code before delivery to users.

### 2. Resource Adaptability ⚠️
Regardless of which skill is invoked, the final solution must conform to the target chip's **Resource Classification**:
- **Micro Resource** (STC89C51): Dynamic memory forbidden, use foreground/background architecture
- **Medium Resource** (GD32F103): Supports simple state machines
- **High Resource** (GD32F407): Supports layered architecture, RTOS

### 3. Pure Non-Blocking Architecture
Strictly prohibit `delay_ms()`, must use SysTick delta comparison or timer polling.

---

## Skills List

### Core Skills

| Skill Name | Version | Description | Status |
|------------|---------|-------------|--------|
| **mcu-c99-assistant** | 1.0.3 | MCU C99 Programming Expert | ✅ |
| **self-improving-unified** | 1.0.0 | Self-Improvement & Learning Skill | ✅ |
| **nima-core** | 3.0.6 | NIMA Cognitive Architecture | ✅ |

### Auxiliary Skills

| Skill Name | Version | Description | Status |
|------------|---------|-------------|--------|
| **pdf** | 0.1.0 | PDF Document Processing | ✅ |
| **fast-browser-use** | 1.0.5 | Browser Automation | ✅ |
| **frontend-design** | 1.0.0 | Embedded GUI Design | ✅ |
| **clean-code-review** | 1.0.0 | Code Review | ✅ |
| **memory-manager** | 1.0.0 | Memory Management | ✅ |
| **desktop-control** | 1.0.0 | Desktop Control | ✅ |
| **skill-creator** | 0.1.0 | Skill Creation | ✅ |
| **essence-distiller** | 1.0.1 | Content Distillation | ✅ |
| **free-ride** | 1.0.4 | Free Ride | ✅ |
| **superdesign** | 1.0.0 | Super Design | ✅ |

---

## mcu-c99-assistant - MCU Programming Assistant

**Core Positioning: Chief Architect and Technical Hub in the MCU Field**

### Main Features

1. **Project Setup**: Automatically create complete project structure
2. **Code Writing**: C99-compliant, pure non-blocking architecture
3. **Debugging Support**: Based on "Software-Hardware Collaborative Three-Dimensional Troubleshooting"
4. **Performance Optimization**: Resource profiling for MCU
5. **Technical Consulting**: Answer C99 standard related questions

### Supported Platforms

#### Domestic Platforms (25+ Brands)

| Architecture | Brand | Series | Representative Models |
|--------------|-------|--------|----------------------|
| 8051 | STC | STC89/12/15/8A | STC89C52RC, STC12C5A60S2, STC8A8K64S4A12 |
| ARM Cortex-M3 | GigaDevice | GD32F103 | GD32F103C8T6, GD32F103RCT6 |
| ARM Cortex-M4 | GigaDevice | GD32F4 | GD32F407VGT6, GD32F450RGT6 |
| ARM Cortex-M0+ | HDSC | HC32F003 | HC32F003C4U6, HC32F003C6TA |
| ARM Cortex-M4 | HDSC | HC32F460 | HC32F460KET6, HC32F460JET6 |
| ARM Cortex-M3 | MindMotion | MM32F103 | MM32F103C8T6, MM32F103RCT6 |
| ARM Cortex-M0+ | CMSemicon | CMS32F | CMS32F031C6T6, CMS32F051C8T6 |
| ARM Cortex-M3 | Silan Micro | SL32F | SL32F103C8T6, SL32F103RCT6 |
| ARM Cortex-M3 | BYD Semi | BY32F | BY32F103C8T6, BY32F103RCT6 |
| ARM Cortex-M3 | CR Micro | CR32F | CR32F103C8T6, CR32F103RCT6 |
| ARM Cortex-M3 | Nationstech | N32 | N32G430C8T7, N32G431C8T7 |
| 8051 | Nuvoton | N76E003 | N76E003, N76E885 |
| ARM Cortex-M0 | Belling | BL702 | BL702, BL704 |
| 8051 | Sonix | STC | STC89C51, STC12C5A60S2 |
| MIPS | Ingenic | X1000 | X1000, X1000E |
| RISC-V | Espressif | ESP32-C | ESP32-C3, ESP32-C6 |
| RISC-V | YMTC | Xtacking | Storage Controller Series |
| RISC-V | CXMT | DDR | Memory Controller Series |

#### Imported Platforms (15+ Brands)

| Architecture | Brand | Series | Representative Models |
|--------------|-------|--------|----------------------|
| ARM Cortex-M3 | ST | STM32F1 | STM32F103C8T6, STM32F103RCT6 |
| ARM Cortex-M4 | ST | STM32F4 | STM32F407VGT6, STM32F429IGT6 |
| ARM Cortex-M7 | ST | STM32F7 | STM32F767ZI, STM32F746ZG |
| ARM Cortex-M4 | ST | STM32L4 | STM32L476RG, STM32L496AG |
| ARM Cortex-M0+ | NXP | LPC8 | LPC812M101JDH20 |
| ARM Cortex-M3 | NXP | LPC17 | LPC1768FBD100, LPC1788FBD208 |
| ARM Cortex-M4 | NXP | K64 | MK64FN1M0VLQ12 |
| AVR | Microchip | ATmega | ATmega328P, ATmega2560 |
| PIC | Microchip | PIC16 | PIC16F877A, PIC16F18855 |
| PIC | Microchip | PIC32 | PIC32MX470F512H |
| MSP430 | TI | MSP430G | MSP430G2553, MSP430F5529 |
| C2000 | TI | TMS320F28 | TMS320F28035, TMS320F28335 |
| ARM Cortex-M4 | Infineon | XMC4000 | XMC4500, XMC4700 |
| ARM Cortex-M3 | Renesas | RX600 | RX63N, RX631 |
| RISC-V | Raspberry Pi | RP2040 | RP2040 |

### Skill Invocation Strategy

This skill automatically invokes other auxiliary skills, **taking responsibility for results (Gatekeeper Mechanism)**:

| Auxiliary Skill | Purpose | Filtering Rules |
|----------------|---------|-----------------|
| PDF Skill | View chip manuals | Extract register addresses → convert to macros |
| Browser Skill | Search technical resources | Arduino/C++ → rewrite to C99 |
| GUI Skill | Embedded interface design | LVGL/OLED/Serial HMI, not Web frontend |
| Self-Improvement | Record learning experience | Hardware experience database |

### Final Delivery Standards

Regardless of how many external skills are invoked, final delivery must meet:
1. ✅ Compilable: ANSI C / C99 compliant
2. ✅ Non-blocking: No dead-loop delays
3. ✅ Resource matching: Don't run 10KB code on 2KB RAM chip
4. ✅ No hallucination: Explicitly output text blocks
5. ✅ Gatekeeper verification: External info cleaned and restructured

---

## Project Structure

```
skills/
├── mcu-c99-assistant/           # MCU Programming Assistant (Main Skill)
│   ├── docs/                    # Documentation (30+ articles)
│   ├── SKILL.md                 # Skill Definition
│   └── _meta.json              # Metadata
│
├── self-improving-unified/       # Self-Improvement Skill
├── nima-core-3.0.6/             # NIMA Cognitive Architecture
├── pdf-0.1.0/                   # PDF Processing
├── fast-browser-use-1.0.5/       # Browser Automation
├── frontend-design-1.0.0/      # Embedded GUI Design
├── clean-code-review-1.0.0/     # Code Review
├── memory-manager-1.0.0/       # Memory Management
├── desktop-control-1.0.0/       # Desktop Control
├── skill-creator-0.1.0/        # Skill Creation
├── essence-distiller-1.0.1/    # Content Distillation
├── free-ride-1.0.4/            # Free Ride
└── superdesign-1.0.0/          # Super Design
```

---

## Quick Start

### Environment Requirements

- Python 3.6+
- Node.js (required by some skills)
- Rust (required by fast-browser-use)

### Install Dependencies

```bash
python skills_check_env.py
```

### Using Skills

Skills are automatically triggered based on user input. For example:

- Mention "MCU", "GPIO" → triggers mcu-c99-assistant
- Mention "PDF", "process PDF" → triggers pdf
- Mention "browser", "webpage" → triggers fast-browser-use
- Mention "interface", "OLED", "LVGL" → triggers frontend-design (Embedded GUI)
- Mention "error", "bug", "fix" → triggers self-improving-unified

---

## Utility Scripts

### skills_check_env.py
Skill environment detection and installation script.

```bash
python skills_check_env.py
```

### install_skills.py
Unified skill installation script.

```bash
python install_skills.py
```

---

## Documentation

- [Comprehensive MCU Models](./skills/mcu-c99-assistant/docs/comprehensive_mcu_models.md)
- [Chip Datasheet Summary](./skills/mcu-c99-assistant/docs/chip_datasheet_summary.md)
- [Chip Datasheet Links](./skills/mcu-c99-assistant/docs/chip_datasheets.md)

---

## Changelog

### 2026-02-24
- mcu-c99-assistant: Strengthened core principles (Gatekeeper Mechanism, Resource Adaptability)
- Frontend-design skill repositioned as "Embedded GUI Design"
- Added self-improving-unified skill
- Added skills_check_env.py environment detection script
- Improved metadata configuration for all skills

---

## License

This project is open source under the MIT license.

---

*Powered by Trae AI*
