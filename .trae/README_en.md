<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trae AI Skills System</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .lang-switch { display: flex; justify-content: center; gap: 10px; margin: 20px 0; }
        .lang-btn { padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: all 0.3s; }
        .lang-btn.active { background: #667eea; color: white; }
        .lang-btn:not(.active) { background: #e0e0e0; color: #333; }
        .lang-btn:hover { transform: scale(1.05); }
        .content { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .section { margin-bottom: 30px; }
        h2 { color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 20px; }
        h3 { color: #555; margin: 20px 0 15px; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #667eea; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: "Courier New", monospace; }
        pre { background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; overflow-x: auto; }
        pre code { background: none; padding: 0; }
        .zh, .en { display: none; }
        .zh.active, .en.active { display: block; }
        .note { background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px 15px; margin: 10px 0; }
        .warning { background: #f8d7da; border-left: 4px solid #dc3545; padding: 10px 15px; margin: 10px 0; }
        .success { background: #d4edda; border-left: 4px solid #28a745; padding: 10px 15px; margin: 10px 0; }
        ul, ol { margin-left: 30px; margin-bottom: 15px; }
        li { margin-bottom: 8px; }
        .footer { text-align: center; margin-top: 30px; color: #666; }
        a { color: #667eea; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Trae AI Skills System</h1>
        <p>Trae AI 技能系统</p>
        <div class="lang-switch">
            <button class="lang-btn" onclick="switchLang('zh')">中文</button>
            <button class="lang-btn active" onclick="switchLang('en')">English</button>
        </div>
    </div>

    <div class="content">
        <!-- Project Overview -->
        <div class="section">
            <h2>Project Overview | 项目概述</h2>
            <div class="zh">
                <p>这是一个面向 Trae AI 的技能系统，提供了多种专业化技能，涵盖嵌入式开发、前端设计、PDF处理、浏览器自动化、代码审查、自我改进等多个领域。</p>
            </div>
            <div class="en active">
                <p>This is a skill system for Trae AI, providing various specialized skills covering embedded development, frontend design, PDF processing, browser automation, code review, self-improvement, and other fields.</p>
            </div>
        </div>

        <!-- Core Principles -->
        <div class="section">
            <h2>Core Principles | 核心原则</h2>
            <div class="zh">
                <div class="note"><strong>⚠️ 守门员机制：</strong>所有外部技能（浏览器、PDF等）获取的信息，必须经过<strong>清洗与重构</strong>，确保转化为符合 C99 标准、非阻塞架构的单片机代码后，才能交付给用户。</div>
                <div class="note"><strong>⚠️ 资源适应性：</strong>无论调用何种技能，最终方案必须符合目标芯片的【资源定级】</div>
                <ul>
                    <li><strong>微资源型</strong>（STC89C51）：禁用动态内存，使用前后台架构</li>
                    <li><strong>中资源型</strong>（GD32F103）：支持简单状态机</li>
                    <li><strong>高资源型</strong>（GD32F407）：支持分层架构、RTOS</li>
                </ul>
                <div class="warning"><strong>⚠️ 纯非阻塞架构：</strong>严禁 delay_ms()，必须使用 SysTick 差值比对或定时器轮询。</div>
            </div>
            <div class="en active">
                <div class="note"><strong>⚠️ Gatekeeper Mechanism:</strong> All information obtained from external skills (browser, PDF, etc.) must undergo <strong>cleaning and restructuring</strong> to ensure it is converted into C99-compliant, non-blocking MCU code before delivery.</div>
                <div class="note"><strong>⚠️ Resource Adaptability:</strong> Regardless of which skill is invoked, the final solution must conform to the target chip's Resource Classification:</div>
                <ul>
                    <li><strong>Micro Resource</strong> (STC89C51): Dynamic memory forbidden, use foreground/background architecture</li>
                    <li><strong>Medium Resource</strong> (GD32F103): Supports simple state machines</li>
                    <li><strong>High Resource</strong> (GD32F407): Supports layered architecture, RTOS</li>
                </ul>
                <div class="warning"><strong>⚠️ Pure Non-Blocking:</strong> Strictly prohibit delay_ms(), must use SysTick delta comparison or timer polling.</div>
            </div>
        </div>

        <!-- Skills List -->
        <div class="section">
            <h2>Skills List | 技能列表</h2>
            <div class="zh">
                <h3>核心技能 | Core Skills</h3>
                <table>
                    <tr><th>技能名称</th><th>版本</th><th>描述</th><th>状态</th></tr>
                    <tr><td>mcu-c99-assistant</td><td>1.0.3</td><td>单片机C99标准编程专家</td><td>✅</td></tr>
                    <tr><td>self-improving-unified</td><td>1.0.0</td><td>自我改进与学习技能</td><td>✅</td></tr>
                    <tr><td>nima-core</td><td>3.0.6</td><td>NIMA认知架构</td><td>✅</td></tr>
                </table>
                <h3>辅助技能 | Auxiliary Skills</h3>
                <table>
                    <tr><th>技能名称</th><th>版本</th><th>描述</th><th>状态</th></tr>
                    <tr><td>pdf</td><td>0.1.0</td><td>PDF文档处理</td><td>✅</td></tr>
                    <tr><td>fast-browser-use</td><td>1.0.5</td><td>浏览器自动化</td><td>✅</td></tr>
                    <tr><td>frontend-design</td><td>1.0.0</td><td>嵌入式GUI设计</td><td>✅</td></tr>
                    <tr><td>clean-code-review</td><td>1.0.0</td><td>代码审查</td><td>✅</td></tr>
                    <tr><td>memory-manager</td><td>1.0.0</td><td>内存管理</td><td>✅</td></tr>
                    <tr><td>desktop-control</td><td>1.0.0</td><td>桌面控制</td><td>✅</td></tr>
                    <tr><td>skill-creator</td><td>0.1.0</td><td>技能创建</td><td>✅</td></tr>
                    <tr><td>essence-distiller</td><td>1.0.1</td><td>内容提炼</td><td>✅</td></tr>
                    <tr><td>free-ride</td><td>1.0.4</td><td>Free Ride</td><td>✅</td></tr>
                    <tr><td>superdesign</td><td>1.0.0</td><td>超级设计</td><td>✅</td></tr>
                </table>
            </div>
            <div class="en active">
                <h3>Core Skills | 核心技能</h3>
                <table>
                    <tr><th>Skill Name</th><th>Version</th><th>Description</th><th>Status</th></tr>
                    <tr><td>mcu-c99-assistant</td><td>1.0.3</td><td>MCU C99 Programming Expert</td><td>✅</td></tr>
                    <tr><td>self-improving-unified</td><td>1.0.0</td><td>Self-Improvement & Learning</td><td>✅</td></tr>
                    <tr><td>nima-core</td><td>3.0.6</td><td>NIMA Cognitive Architecture</td><td>✅</td></tr>
                </table>
                <h3>Auxiliary Skills | 辅助技能</h3>
                <table>
                    <tr><th>Skill Name</th><th>Version</th><th>Description</th><th>Status</th></tr>
                    <tr><td>pdf</td><td>0.1.0</td><td>PDF Processing</td><td>✅</td></tr>
                    <tr><td>fast-browser-use</td><td>1.0.5</td><td>Browser Automation</td><td>✅</td></tr>
                    <tr><td>frontend-design</td><td>1.0.0</td><td>Embedded GUI Design</td><td>✅</td></tr>
                    <tr><td>clean-code-review</td><td>1.0.0</td><td>Code Review</td><td>✅</td></tr>
                    <tr><td>memory-manager</td><td>1.0.0</td><td>Memory Management</td><td>✅</td></tr>
                    <tr><td>desktop-control</td><td>1.0.0</td><td>Desktop Control</td><td>✅</td></tr>
                    <tr><td>skill-creator</td><td>0.1.0</td><td>Skill Creation</td><td>✅</td></tr>
                    <tr><td>essence-distiller</td><td>1.0.1</td><td>Content Distillation</td><td>✅</td></tr>
                    <tr><td>free-ride</td><td>1.0.4</td><td>Free Ride</td><td>✅</td></tr>
                    <tr><td>superdesign</td><td>1.0.0</td><td>Super Design</td><td>✅</td></tr>
                </table>
            </div>
        </div>

        <!-- Supported Platforms -->
        <div class="section">
            <h2>Supported Platforms | 支持的平台</h2>
            <div class="zh">
                <h3>国产平台（25+家）</h3>
                <table>
                    <tr><th>架构</th><th>品牌</th><th>系列</th><th>代表型号</th></tr>
                    <tr><td>8051</td><td>STC</td><td>STC89/12/15/8A</td><td>STC89C52RC, STC12C5A60S2</td></tr>
                    <tr><td>ARM Cortex-M3</td><td>兆易创新</td><td>GD32F103</td><td>GD32F103C8T6</td></tr>
                    <tr><td>ARM Cortex-M4</td><td>兆易创新</td><td>GD32F4</td><td>GD32F407VGT6</td></tr>
                    <tr><td>ARM Cortex-M0+</td><td>华大半导体</td><td>HC32F003</td><td>HC32F003C4U6</td></tr>
                    <tr><td>ARM Cortex-M4</td><td>华大半导体</td><td>HC32F460</td><td>HC32F460KET6</td></tr>
                    <tr><td>ARM Cortex-M3</td><td>灵动微电子</td><td>MM32F103</td><td>MM32F103C8T6</td></tr>
                    <tr><td>ARM Cortex-M3</td><td>国民技术</td><td>N32</td><td>N32G430C8T7</td></tr>
                    <tr><td>RISC-V</td><td>乐鑫</td><td>ESP32-C</td><td>ESP32-C3, ESP32-C6</td></tr>
                </table>
                <h3>进口平台（15+家）</h3>
                <table>
                    <tr><th>架构</th><th>品牌</th><th>系列</th><th>代表型号</th></tr>
                    <tr><td>ARM Cortex-M3</td><td>ST</td><td>STM32F1</td><td>STM32F103C8T6</td></tr>
                    <tr><td>ARM Cortex-M4</td><td>ST</td><td>STM32F4</td><td>STM32F407VGT6</td></tr>
                    <tr><td>ARM Cortex-M3</td><td>NXP</td><td>LPC17</td><td>LPC1768FBD100</td></tr>
                    <tr><td>AVR</td><td>Microchip</td><td>ATmega</td><td>ATmega328P</td></tr>
                    <tr><td>PIC</td><td>Microchip</td><td>PIC32</td><td>PIC32MX470F512H</td></tr>
                    <tr><td>MSP430</td><td>TI</td><td>MSP430G</td><td>MSP430G2553</td></tr>
                    <tr><td>RISC-V</td><td>Raspberry Pi</td><td>RP2040</td><td>RP2040</td></tr>
                </table>
            </div>
            <div class="en active">
                <h3>Domestic Platforms | 国产平台</h3>
                <table>
                    <tr><th>Architecture</th><th>Brand</th><th>Series</th><th>Representative Models</th></tr>
                    <tr><td>8051</td><td>STC</td><td>STC89/12/15/8A</td><td>STC89C52RC, STC12C5A60S2</td></tr>
                    <tr><td>ARM Cortex-M3</td><td>GigaDevice</td><td>GD32F103</td><td>GD32F103C8T6</td></tr>
                    <tr><td>ARM Cortex-M4</td><td>GigaDevice</td><td>GD32F4</td><td>GD32F407VGT6</td></tr>
                    <tr><td>ARM Cortex-M0+</td><td>HDSC</td><td>HC32F003</td><td>HC32F003C4U6</td></tr>
                    <tr><td>ARM Cortex-M4</td><td>HDSC</td><td>HC32F460</td><td>HC32F460KET6</td></tr>
                    <tr><td>ARM Cortex-M3</td><td>MindMotion</td><td>MM32F103</td><td>MM32F103C8T6</td></tr>
                    <tr><td>ARM Cortex-M3</td><td>Nationstech</td><td>N32</td><td>N32G430C8T7</td></tr>
                    <tr><td>RISC-V</td><td>Espressif</td><td>ESP32-C</td><td>ESP32-C3, ESP32-C6</td></tr>
                </table>
                <h3>Imported Platforms | 进口平台</h3>
                <table>
                    <tr><th>Architecture</th><th>Brand</th><th>Series</th><th>Representative Models</th></tr>
                    <tr><td>ARM Cortex-M3</td><td>ST</td><td>STM32F1</td><td>STM32F103C8T6</td></tr>
                    <tr><td>ARM Cortex-M4</td><td>ST</td><td>STM32F4</td><td>STM32F407VGT6</td></tr>
                    <tr><td>ARM Cortex-M3</td><td>NXP</td><td>LPC17</td><td>LPC1768FBD100</td></tr>
                    <tr><td>AVR</td><td>Microchip</td><td>ATmega</td><td>ATmega328P</td></tr>
                    <tr><td>PIC</td><td>Microchip</td><td>PIC32</td><td>PIC32MX470F512H</td></tr>
                    <tr><td>MSP430</td><td>TI</td><td>MSP430G</td><td>MSP430G2553</td></tr>
                    <tr><td>RISC-V</td><td>Raspberry Pi</td><td>RP2040</td><td>RP2040</td></tr>
                </table>
            </div>
        </div>

        <!-- Quick Start -->
        <div class="section">
            <h2>Quick Start | 快速开始</h2>
            <div class="zh">
                <h3>环境要求</h3>
                <ul>
                    <li>Python 3.6+</li>
                    <li>Node.js（部分技能需要）</li>
                    <li>Rust（fast-browser-use需要）</li>
                </ul>
                <h3>安装依赖</h3>
                <pre><code>python skills_check_env.py</code></pre>
                <h3>使用技能</h3>
                <p>技能会根据用户输入自动触发。例如：</p>
                <ul>
                    <li>提到"单片机"、"MCU" → 触发 mcu-c99-assistant</li>
                    <li>提到"PDF" → 触发 pdf</li>
                    <li>提到"浏览器" → 触发 fast-browser-use</li>
                    <li>提到"界面"、"OLED" → 触发 frontend-design</li>
                </ul>
            </div>
            <div class="en active">
                <h3>Environment Requirements | 环境要求</h3>
                <ul>
                    <li>Python 3.6+</li>
                    <li>Node.js (required by some skills)</li>
                    <li>Rust (required by fast-browser-use)</li>
                </ul>
                <h3>Install Dependencies | 安装依赖</h3>
                <pre><code>python skills_check_env.py</code></pre>
                <h3>Using Skills | 使用技能</h3>
                <p>Skills are automatically triggered based on user input:</p>
                <ul>
                    <li>Mention "MCU" → triggers mcu-c99-assistant</li>
                    <li>Mention "PDF" → triggers pdf</li>
                    <li>Mention "browser" → triggers fast-browser-use</li>
                    <li>Mention "interface", "OLED" → triggers frontend-design</li>
                </ul>
            </div>
        </div>

        <!-- Final Delivery Standards -->
        <div class="section">
            <h2>Final Delivery Standards | 最终交付标准</h2>
            <div class="zh">
                <div class="success">✅ 可编译：符合 ANSI C / C99 标准</div>
                <div class="success">✅ 非阻塞：没有死循环延时</div>
                <div class="success">✅ 资源匹配：不会让 2KB RAM 芯片跑 10KB 代码</div>
                <div class="success">✅ 无幻觉：显式输出的文本块</div>
                <div class="success">✅ 守门员验证：外部信息经过清洗重构</div>
            </div>
            <div class="en active">
                <div class="success">✅ Compilable: ANSI C / C99 compliant</div>
                <div class="success">✅ Non-blocking: No dead-loop delays</div>
                <div class="success">✅ Resource matching: Don't run 10KB code on 2KB RAM chip</div>
                <div class="success">✅ No hallucination: Explicitly output text blocks</div>
                <div class="success">✅ Gatekeeper verification: External info cleaned and restructured</div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>© 2026 Trae AI Skills System | MIT License</p>
            <p>Powered by Trae AI</p>
        </div>
    </div>

    <script>
        function switchLang(lang) {
            document.querySelectorAll('.zh, .en').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            
            if (lang === 'zh') {
                document.querySelectorAll('.zh').forEach(el => el.classList.add('active'));
                document.querySelector('.lang-btn:nth-child(1)').classList.add('active');
                document.documentElement.lang = 'zh-CN';
            } else {
                document.querySelectorAll('.en').forEach(el => el.classList.add('active'));
                document.querySelector('.lang-btn:nth-child(2)').classList.add('active');
                document.documentElement.lang = 'en';
            }
        }
    </script>
</body>
</html>
