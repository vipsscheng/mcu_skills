# 运行时问题诊断

## 概述
运行时问题是嵌入式系统开发中常见的挑战，它们可能在系统运行过程中突然出现，导致系统异常、崩溃或功能失效。本章节将介绍各种微控制器的运行时问题诊断方法，帮助开发者快速定位和解决运行时问题。

## 常见运行时问题类型

### 硬件相关问题
- **电源问题**：电压波动、电源噪声、电池电量不足
- **时钟问题**：时钟不稳定、晶振故障、时钟配置错误
- **外设问题**：传感器故障、执行器故障、通信接口故障
- **硬件连接问题**：接线松动、接触不良、短路

### 软件相关问题
- **内存问题**：内存溢出、内存泄漏、空指针访问
- **逻辑问题**：死循环、逻辑错误、状态机错误
- **时序问题**：竞争条件、同步问题、中断冲突
- **异常处理**：未处理的异常、异常嵌套

### 通信问题
- **通信协议错误**：协议实现错误、数据格式错误
- **通信超时**：网络延迟、设备无响应
- **数据传输错误**：数据丢失、数据损坏
- **地址冲突**：I2C地址冲突、网络地址冲突

## STC系列微控制器运行时问题诊断

### 常见运行时问题及解决方案

#### 程序死机
**症状**：程序停止响应，无法执行任何操作
**可能原因**：
- 死循环
- 堆栈溢出
- 中断冲突
- 硬件故障

**解决方案**：
- 使用看门狗定时器，在程序死机时自动复位
- 检查代码中的死循环，特别是在中断处理函数中
- 合理设置堆栈大小，避免堆栈溢出
- 检查中断优先级设置，避免中断冲突

```c
// 看门狗配置
void WDT_Init(void) {
    WDT_CONTR = 0x3F;  // 启动看门狗，溢出时间约18ms
}

// 喂狗
void WDT_Feed(void) {
    WDT_CONTR = 0x3F;  // 重新加载看门狗
}

// 在主循环中定期喂狗
void main(void) {
    WDT_Init();
    
    while(1) {
        // 主程序逻辑
        
        WDT_Feed();  // 定期喂狗
    }
}
```

#### 串口通信异常
**症状**：串口接收数据错误、通信中断
**可能原因**：
- 波特率不匹配
- 数据格式错误
- 硬件连接问题
- 中断处理错误

**解决方案**：
- 确认波特率设置正确
- 检查数据格式（数据位、停止位、校验位）
- 检查硬件连接，确保TX/RX连接正确
- 优化中断处理函数，避免处理时间过长

```c
// UART初始化
void UART_Init(uint32_t baudrate) {
    SCON = 0x50;  // 8位数据，可变波特率
    AUXR |= 0x40; // 定时器1作为波特率发生器
    TMOD &= 0x0F; // 清除定时器1模式位
    TMOD |= 0x20; // 定时器1为8位自动重装模式
    TH1 = 256 - (11059200 / 12 / baudrate);  // 计算波特率
    TL1 = TH1;
    TR1 = 1;      // 启动定时器1
    ES = 1;       // 开启UART中断
    EA = 1;        // 开启总中断
}

// UART中断处理函数
void UART_ISR(void) interrupt 4 {
    if (RI) {
        RI = 0;
        // 处理接收到的数据
        uint8_t data = SBUF;
        // 注意：中断处理函数应尽量简短
    }
    if (TI) {
        TI = 0;
    }
}
```

#### ADC采集错误
**症状**：ADC采集值异常、不稳定
**可能原因**：
- 参考电压不稳定
- 输入信号噪声过大
- ADC配置错误
- 采样时间不足

**解决方案**：
- 确保参考电压稳定
- 增加硬件滤波电路
- 正确配置ADC参数
- 增加采样时间，提高采样精度

```c
// ADC初始化
void ADC_Init(void) {
    P1M0 = 0x01;  // P1.0设置为ADC输入
    P1M1 = 0x01;
    
    ADC_CONTR = 0x80;  // 打开ADC电源
    delay_ms(10);  // 等待ADC稳定
}

// 读取ADC值（带滤波）
uint16_t ADC_ReadFiltered(void) {
    uint32_t sum = 0;
    for (uint8_t i = 0; i < 10; i++) {
        ADC_CONTR &= 0xF0;
        ADC_CONTR |= 0x00;  // 选择P1.0通道
        ADC_CONTR |= 0x40;  // 启动ADC转换
        while (!(ADC_CONTR & 0x20));  // 等待转换完成
        ADC_CONTR &= ~0x20;  // 清除转换完成标志
        sum += (ADC_RES << 8) | ADC_RESL;
    }
    return sum / 10;  // 返回平均值
}
```

## GD32系列微控制器运行时问题诊断

### 常见运行时问题及解决方案

#### 硬故障（HardFault）
**症状**：程序突然崩溃，进入HardFault中断
**可能原因**：
- 非法内存访问
- 未对齐的内存访问
- 除零操作
- 栈溢出

**解决方案**：
- 实现HardFault中断处理函数，获取故障信息
- 使用调试器查看堆栈和寄存器状态
- 检查内存访问操作，避免越界访问
- 合理设置栈大小

```c
// HardFault中断处理函数
void HardFault_Handler(void) {
    // 保存故障信息
    uint32_t r0, r1, r2, r3, r12, lr, pc, psr;
    
    __asm volatile (
        "MRS %0, r0\n"
        "MRS %1, r1\n"
        "MRS %2, r2\n"
        "MRS %3, r3\n"
        "MRS %4, r12\n"
        "MRS %5, lr\n"
        "MRS %6, pc\n"
        "MRS %7, psr\n"
        : "=r"(r0), "=r"(r1), "=r"(r2), "=r"(r3), "=r"(r12), "=r"(lr), "=r"(pc), "=r"(psr)
    );
    
    // 输出故障信息
    printf("HardFault: r0=0x%08x, r1=0x%08x, r2=0x%08x, r3=0x%08x\n", r0, r1, r2, r3);
    printf("r12=0x%08x, lr=0x%08x, pc=0x%08x, psr=0x%08x\n", r12, lr, pc, psr);
    
    // 可以在这里添加故障处理逻辑
    while(1);
}
```

#### 内存管理问题
**症状**：内存分配失败、内存泄漏
**可能原因**：
- 堆内存不足
- 内存碎片
- 未释放的内存
- 栈溢出

**解决方案**：
- 使用内存池管理内存分配
- 定期检查内存使用情况
- 确保所有分配的内存都被释放
- 合理设置栈大小

```c
// 内存使用情况检查
void Check_Memory_Usage(void) {
    extern uint8_t _heap_start;
    extern uint8_t _heap_end;
    uint32_t heap_size = &_heap_end - &_heap_start;
    uint32_t free_heap = heap_size - used_heap;
    
    printf("Heap size: %d bytes\n", heap_size);
    printf("Used heap: %d bytes\n", used_heap);
    printf("Free heap: %d bytes\n", free_heap);
    
    if (free_heap < 1024) {
        printf("Warning: Low memory!\n");
    }
}

// 安全的内存分配函数
void* Safe_Malloc(uint32_t size) {
    void* ptr = malloc(size);
    if (ptr) {
        used_heap += size;
        Check_Memory_Usage();
    } else {
        printf("Error: Memory allocation failed!\n");
    }
    return ptr;
}

// 安全的内存释放函数
void Safe_Free(void* ptr, uint32_t size) {
    if (ptr) {
        free(ptr);
        used_heap -= size;
        Check_Memory_Usage();
    }
}
```

#### 外设初始化失败
**症状**：外设无法正常工作、初始化函数返回错误
**可能原因**：
- 时钟未使能
- 引脚配置错误
- 外设寄存器配置错误
- 硬件故障

**解决方案**：
- 确保外设时钟已使能
- 检查引脚配置是否正确
- 验证外设寄存器配置
- 检查硬件连接

```c
// 检查外设初始化状态
uint8_t Check_Peripheral_Init(void) {
    // 检查GPIO初始化
    if (gpio_init_flag == 0) {
        printf("Error: GPIO initialization failed!\n");
        return 0;
    }
    
    // 检查UART初始化
    if (uart_init_flag == 0) {
        printf("Error: UART initialization failed!\n");
        return 0;
    }
    
    // 检查SPI初始化
    if (spi_init_flag == 0) {
        printf("Error: SPI initialization failed!\n");
        return 0;
    }
    
    return 1;  // 所有外设初始化成功
}

// 外设初始化函数
void Peripheral_Init(void) {
    // 使能时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    rcu_periph_clock_enable(RCU_USART0);
    rcu_periph_clock_enable(RCU_SPI0);
    
    // 初始化GPIO
    gpio_init_flag = GPIO_Init();
    
    // 初始化UART
    uart_init_flag = UART_Init();
    
    // 初始化SPI
    spi_init_flag = SPI_Init();
    
    // 检查初始化状态
    if (!Check_Peripheral_Init()) {
        printf("Peripheral initialization failed!\n");
        // 处理初始化失败
    }
}
```

## HC32系列微控制器运行时问题诊断

### 常见运行时问题及解决方案

#### 系统时钟异常
**症状**：系统运行速度异常、定时器不准
**可能原因**：
- 时钟源配置错误
- 晶振故障
- 时钟分频设置错误
- 电源不稳定

**解决方案**：
- 检查时钟源配置
- 验证晶振是否正常工作
- 确认时钟分频设置正确
- 确保电源稳定

```c
// 时钟配置检查
void Check_Clock_Config(void) {
    uint32_t sysclk = SystemCoreClock;
    uint32_t hclk = sysclk / ((SCB->CLOCKCONTROL & SCB_CLOCKCONTROL_HPRE_Msk) >> SCB_CLOCKCONTROL_HPRE_Pos);
    uint32_t pclk1 = hclk / ((SCB->CLOCKCONTROL & SCB_CLOCKCONTROL_PPRE1_Msk) >> SCB_CLOCKCONTROL_PPRE1_Pos);
    uint32_t pclk2 = hclk / ((SCB->CLOCKCONTROL & SCB_CLOCKCONTROL_PPRE2_Msk) >> SCB_CLOCKCONTROL_PPRE2_Pos);
    
    printf("System clock: %d Hz\n", sysclk);
    printf("HCLK: %d Hz\n", hclk);
    printf("PCLK1: %d Hz\n", pclk1);
    printf("PCLK2: %d Hz\n", pclk2);
    
    if (sysclk != EXPECTED_SYSCLK) {
        printf("Warning: System clock mismatch! Expected: %d Hz, Actual: %d Hz\n", EXPECTED_SYSCLK, sysclk);
    }
}

// 时钟初始化
void Clock_Init(void) {
    // 配置时钟源
    stc_clk_sysclk_cfg_t stcSysClkCfg;
    CLK_SysClkConfig(&stcSysClkCfg);
    
    // 更新系统时钟
    SystemCoreClockUpdate();
    
    // 检查时钟配置
    Check_Clock_Config();
}
```

#### 中断处理问题
**症状**：中断不触发、中断处理函数执行异常
**可能原因**：
- 中断未使能
- 中断优先级设置错误
- 中断标志未清除
- 中断处理函数执行时间过长

**解决方案**：
- 确保中断已使能
- 检查中断优先级设置
- 确保中断标志被正确清除
- 优化中断处理函数，减少执行时间

```c
// 中断配置检查
void Check_Interrupt_Config(void) {
    // 检查外部中断配置
    if (EXTI_GetIntStatus(EXTI_CH_0) == Reset) {
        printf("Warning: EXTI0 interrupt not enabled!\n");
    }
    
    // 检查定时器中断配置
    if (TIMER_GetIntStatus(TIMER0, TIMER_INT_UP) == Reset) {
        printf("Warning: TIMER0 update interrupt not enabled!\n");
    }
    
    // 检查UART中断配置
    if (USART_GetIntStatus(USART1, UsartRxInt) == Reset) {
        printf("Warning: USART1 receive interrupt not enabled!\n");
    }
}

// 外部中断处理函数
void EXTI0_IRQHandler(void) {
    if (EXTI_GetIntStatus(EXTI_CH_0)) {
        // 处理外部中断
        // 注意：中断处理函数应尽量简短
        
        // 清除中断标志
        EXTI_ClearIntStatus(EXTI_CH_0);
    }
}
```

#### I2C通信问题
**症状**：I2C通信失败、数据传输错误
**可能原因**：
- 总线锁定
- 地址冲突
- 时序错误
- 硬件连接问题

**解决方案**：
- 实现I2C总线恢复机制
- 确保设备地址唯一
- 正确配置I2C时序参数
- 检查硬件连接

```c
// I2C总线恢复
void I2C_Bus_Recovery(void) {
    // 发送9个时钟脉冲，释放总线
    for (uint8_t i = 0; i < 9; i++) {
        I2C_SCL_High();
        delay_us(1);
        I2C_SCL_Low();
        delay_us(1);
    }
    
    // 发送停止条件
    I2C_Stop();
    
    printf("I2C bus recovered!\n");
}

// I2C通信检查
uint8_t I2C_Check_Communication(uint8_t device_address) {
    // 发送起始条件
    if (!I2C_Start()) {
        printf("Error: I2C start failed!\n");
        I2C_Bus_Recovery();
        return 0;
    }
    
    // 发送设备地址
    if (!I2C_Send_Address(device_address, I2C_WRITE)) {
        printf("Error: I2C device not found! Address: 0x%02x\n", device_address);
        I2C_Stop();
        return 0;
    }
    
    // 发送停止条件
    I2C_Stop();
    
    return 1;  // 通信正常
}
```

## MM32系列微控制器运行时问题诊断

### 常见运行时问题及解决方案

#### 复位问题
**症状**：系统频繁复位、无法正常启动
**可能原因**：
- 看门狗复位
- 电源复位
- 软件复位
- 硬件复位

**解决方案**：
- 检查复位原因
- 确保看门狗正确配置
- 检查电源稳定性
- 检查硬件复位电路

```c
// 检查复位原因
void Check_Reset_Reason(void) {
    uint32_t reset_flags = RCC->CSR;
    
    if (reset_flags & RCC_CSR_LPWRRSTF) {
        printf("Reset reason: Low power reset\n");
    } else if (reset_flags & RCC_CSR_WDTRSTF) {
        printf("Reset reason: Watchdog reset\n");
    } else if (reset_flags & RCC_CSR_SFTRSTF) {
        printf("Reset reason: Software reset\n");
    } else if (reset_flags & RCC_CSR_PORRSTF) {
        printf("Reset reason: Power-on reset\n");
    } else if (reset_flags & RCC_CSR_PINRSTF) {
        printf("Reset reason: External pin reset\n");
    }
    
    // 清除复位标志
    RCC->CSR |= RCC_CSR_RMVF;
}

// 看门狗配置
void WDT_Init(void) {
    // 使能IWDT时钟
    RCC->CSR |= RCC_CSR_LSION;
    while (!(RCC->CSR & RCC_CSR_LSIRDY));
    
    // 配置IWDT
    IWDG->KR = 0x5555;  // 解锁
    IWDG->PR = 0x06;  // 预分频 32
    IWDG->RLR = 0xFFF;  // 重载值
    IWDG->KR = 0xAAAA;  // 重载
    IWDG->KR = 0xCCCC;  // 启动
}

// 喂狗
void WDT_Feed(void) {
    IWDG->KR = 0xAAAA;  // 重载
}
```

#### 定时器问题
**症状**：定时器不触发、定时不准确
**可能原因**：
- 定时器配置错误
- 时钟源问题
- 中断优先级问题
- 定时器溢出

**解决方案**：
- 检查定时器配置
- 确认时钟源正确
- 检查中断优先级设置
- 处理定时器溢出

```c
// 定时器配置检查
void Check_Timer_Config(void) {
    // 检查TIM2配置
    printf("TIM2 prescaler: %d\n", TIM2->PSC);
    printf("TIM2 autoreload: %d\n", TIM2->ARR);
    printf("TIM2 counter: %d\n", TIM2->CNT);
    
    // 检查TIM2中断配置
    if (!(TIM2->DIER & TIM_DIER_UIE)) {
        printf("Warning: TIM2 update interrupt not enabled!\n");
    }
    
    // 计算定时时间
    uint32_t timer_clock = SystemCoreClock / (TIM2->PSC + 1);
    float period = (float)(TIM2->ARR + 1) / timer_clock;
    printf("TIM2 period: %.6f seconds\n", period);
}

// 定时器初始化
void Timer_Init(void) {
    // 使能时钟
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;
    
    // 配置定时器
    TIM2->PSC = 8399;  // 预分频，84MHz / 8400 = 10kHz
    TIM2->ARR = 9999;  // 自动重载值，10kHz / 10000 = 1Hz
    TIM2->DIER |= TIM_DIER_UIE;  // 启用更新中断
    TIM2->CR1 |= TIM_CR1_CEN;  // 启动定时器
    
    // 配置中断
    NVIC_EnableIRQ(TIM2_IRQn);
    NVIC_SetPriority(TIM2_IRQn, 2);
    
    // 检查定时器配置
    Check_Timer_Config();
}

// 定时器中断处理函数
void TIM2_IRQHandler(void) {
    if (TIM2->SR & TIM_SR_UIF) {
        // 处理定时器中断
        
        // 清除中断标志
        TIM2->SR &= ~TIM_SR_UIF;
    }
}
```

#### SPI通信问题
**症状**：SPI通信失败、数据传输错误
**可能原因**：
- 时钟极性/相位配置错误
- 数据位长度错误
- 片选信号问题
- 硬件连接问题

**解决方案**：
- 检查SPI配置参数
- 确认时钟极性和相位设置正确
- 检查片选信号控制
- 检查硬件连接

```c
// SPI配置检查
void Check_SPI_Config(void) {
    // 检查SPI1配置
    printf("SPI1 mode: %d\n", (SPI1->CR1 & SPI_CR1_MSTR) ? 1 : 0);
    printf("SPI1 clock polarity: %d\n", (SPI1->CR1 & SPI_CR1_CPOL) ? 1 : 0);
    printf("SPI1 clock phase: %d\n", (SPI1->CR1 & SPI_CR1_CPHA) ? 1 : 0);
    printf("SPI1 data size: %d bits\n", 8 + ((SPI1->CR1 & SPI_CR1_DFF) ? 8 : 0));
    printf("SPI1 baud rate prescaler: %d\n", 2 << ((SPI1->CR1 & SPI_CR1_BR_Msk) >> SPI_CR1_BR_Pos));
    
    // 检查SPI1状态
    if (!(SPI1->CR1 & SPI_CR1_SPE)) {
        printf("Warning: SPI1 not enabled!\n");
    }
}

// SPI通信测试
uint8_t SPI_Test(void) {
    // 发送测试数据
    uint8_t test_data = 0xAA;
    uint8_t received_data;
    
    // 使能片选
    CS_LOW();
    
    // 发送数据
    while (!(SPI1->SR & SPI_SR_TXE));
    SPI1->DR = test_data;
    
    // 接收数据
    while (!(SPI1->SR & SPI_SR_RXNE));
    received_data = SPI1->DR;
    
    // 等待传输完成
    while (SPI1->SR & SPI_SR_BSY);
    
    // 禁用片选
    CS_HIGH();
    
    // 检查数据
    if (received_data == test_data) {
        printf("SPI test passed!\n");
        return 1;
    } else {
        printf("SPI test failed! Sent: 0x%02x, Received: 0x%02x\n", test_data, received_data);
        return 0;
    }
}
```

## 通用运行时问题诊断方法

### 日志记录
- **串口日志**：通过串口输出运行时信息
- **RAM日志**：在RAM中存储日志，适用于无串口的情况
- **Flash日志**：在Flash中存储关键日志，掉电不丢失
- **远程日志**：通过网络发送日志到远程服务器

```c
// 日志级别定义
typedef enum {
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_FATAL
} LogLevel_t;

// 日志输出函数
void Log(LogLevel_t level, const char* format, ...) {
    va_list args;
    va_start(args, format);
    
    // 根据日志级别输出前缀
    switch (level) {
        case LOG_LEVEL_DEBUG:
            printf("[DEBUG] ");
            break;
        case LOG_LEVEL_INFO:
            printf("[INFO] ");
            break;
        case LOG_LEVEL_WARNING:
            printf("[WARNING] ");
            break;
        case LOG_LEVEL_ERROR:
            printf("[ERROR] ");
            break;
        case LOG_LEVEL_FATAL:
            printf("[FATAL] ");
            break;
    }
    
    // 输出日志内容
    vprintf(format, args);
    printf("\n");
    
    va_end(args);
    
    // 对于错误和致命错误，可以添加额外处理
    if (level >= LOG_LEVEL_ERROR) {
        // 可以在这里添加错误处理逻辑
    }
}

// 使用示例
void main(void) {
    Log(LOG_LEVEL_INFO, "System started");
    
    // 初始化硬件
    if (Hardware_Init() != 0) {
        Log(LOG_LEVEL_ERROR, "Hardware initialization failed");
        return;
    }
    
    Log(LOG_LEVEL_INFO, "Hardware initialized successfully");
    
    while(1) {
        // 主循环
        Log(LOG_LEVEL_DEBUG, "Main loop running");
        delay_ms(1000);
    }
}
```

### 断点调试
- **硬件断点**：使用调试器设置硬件断点
- **软件断点**：在代码中插入断点指令
- **条件断点**：当满足特定条件时触发断点
- **数据断点**：当数据被修改时触发断点

### 实时监控
- **变量监控**：实时监控关键变量的值
- **寄存器监控**：监控CPU和外设寄存器
- **内存监控**：监控内存使用情况
- **执行时间监控**：监控函数执行时间

```c
// 执行时间监控
void Measure_Execution_Time(void (*func)(void), const char* func_name) {
    uint32_t start_time = Get_System_Tick();
    
    // 执行函数
    func();
    
    uint32_t end_time = Get_System_Tick();
    uint32_t execution_time = end_time - start_time;
    
    printf("Function %s execution time: %d ms\n", func_name, execution_time);
}

// 内存使用监控
void Monitor_Memory_Usage(void) {
    extern uint8_t _heap_start;
    extern uint8_t _heap_end;
    extern uint8_t _stack_start;
    
    uint32_t heap_size = &_heap_end - &_heap_start;
    uint32_t stack_size = (uint32_t)&_stack_start - (uint32_t)&_heap_end;
    uint32_t free_memory = heap_size - used_heap;
    
    printf("Memory usage:\n");
    printf("Heap size: %d bytes\n", heap_size);
    printf("Used heap: %d bytes\n", used_heap);
    printf("Free heap: %d bytes\n", free_memory);
    printf("Stack size: %d bytes\n", stack_size);
}
```

### 故障注入测试
- **内存故障注入**：模拟内存损坏
- **通信故障注入**：模拟通信错误
- **电源故障注入**：模拟电源波动
- **时钟故障注入**：模拟时钟异常

## 运行时问题诊断工具

### 调试器
- **JTAG/SWD调试器**：使用JTAG或SWD接口进行调试
- **串口调试器**：通过串口进行调试
- **网络调试器**：通过网络进行远程调试
- **逻辑分析仪**：分析数字信号时序

### 软件工具
- **实时操作系统**：提供任务监控和调试功能
- **内存分析工具**：分析内存使用情况
- **性能分析工具**：分析系统性能
- **代码覆盖率工具**：分析代码执行覆盖情况

### 自定义诊断工具
- **状态指示灯**：通过LED指示系统状态
- **按键调试**：通过按键触发调试功能
- **调试菜单**：通过串口或显示屏提供调试菜单
- **远程诊断**：通过网络进行远程诊断

```c
// 调试菜单
void Debug_Menu(void) {
    printf("Debug Menu:\n");
    printf("1. Show system status\n");
    printf("2. Test GPIO\n");
    printf("3. Test UART\n");
    printf("4. Test I2C\n");
    printf("5. Test SPI\n");
    printf("6. Show memory usage\n");
    printf("7. Show task status\n");
    printf("8. Exit\n");
    printf("Enter your choice: ");
    
    uint8_t choice = getchar();
    printf("\n");
    
    switch (choice) {
        case '1':
            Show_System_Status();
            break;
        case '2':
            Test_GPIO();
            break;
        case '3':
            Test_UART();
            break;
        case '4':
            Test_I2C();
            break;
        case '5':
            Test_SPI();
            break;
        case '6':
            Monitor_Memory_Usage();
            break;
        case '7':
            Show_Task_Status();
            break;
        case '8':
            return;
        default:
            printf("Invalid choice!\n");
            break;
    }
    
    Debug_Menu();  // 显示菜单
}

// 系统状态显示
void Show_System_Status(void) {
    printf("System Status:\n");
    printf("System clock: %d Hz\n", SystemCoreClock);
    printf("Uptime: %d seconds\n", Get_System_Tick() / 1000);
    printf("Temperature: %.2f C\n", Read_Temperature());
    printf("Humidity: %.2f %%\n", Read_Humidity());
    printf("Battery voltage: %.2f V\n", Read_Battery_Voltage());
    
    // 检查各外设状态
    printf("Peripheral status:\n");
    printf("GPIO: %s\n", Check_GPIO() ? "OK" : "ERROR");
    printf("UART: %s\n", Check_UART() ? "OK" : "ERROR");
    printf("I2C: %s\n", Check_I2C() ? "OK" : "ERROR");
    printf("SPI: %s\n", Check_SPI() ? "OK" : "ERROR");
    printf("Timer: %s\n", Check_Timer() ? "OK" : "ERROR");
}
```

## 常见运行时问题解决方案汇总

### 内存问题
| 问题类型 | 症状 | 解决方案 |
|---------|------|--------|
| 内存溢出 | 程序崩溃、数据 corruption | 增加内存大小、优化内存使用、使用内存池 |
| 内存泄漏 | 可用内存逐渐减少 | 确保所有分配的内存都被释放、使用内存跟踪工具 |
| 空指针访问 | 硬故障、程序崩溃 | 检查指针有效性、使用空指针检查 |
| 栈溢出 | 程序崩溃、行为异常 | 增加栈大小、减少栈使用、避免递归 |

### 通信问题
| 问题类型 | 症状 | 解决方案 |
|---------|------|--------|
| 通信超时 | 数据传输失败 | 增加超时时间、检查硬件连接、优化通信协议 |
| 数据错误 | 接收到错误数据 | 增加校验和、使用更可靠的通信协议、检查硬件连接 |
| 总线锁定 | 通信完全失败 | 实现总线恢复机制、检查设备地址冲突 |
| 通信冲突 | 数据混乱 | 使用适当的仲裁机制、避免同时通信 |

### 定时器问题
| 问题类型 | 症状 | 解决方案 |
|---------|------|--------|
| 定时不准确 | 时间偏差 | 校准时钟、使用更精确的时钟源 |
| 定时器不触发 | 功能失效 | 检查定时器配置、确保中断使能 |
| 定时器溢出 | 计数错误 | 处理溢出情况、使用适当的计数范围 |
| 中断冲突 | 定时器失效 | 合理设置中断优先级、优化中断处理函数 |

### 电源问题
| 问题类型 | 症状 | 解决方案 |
|---------|------|--------|
| 电压波动 | 系统不稳定 | 使用稳压电源、增加滤波电容 |
| 电池电量低 | 系统重启 | 实现低电压检测、及时提醒用户 |
| 电源噪声 | 数据错误 | 增加电源滤波、隔离噪声源 |
| 功耗过高 | 电池寿命短 | 优化代码、使用低功耗模式、减少不必要的操作 |

## 运行时问题预防措施

### 代码质量
- **代码审查**：定期进行代码审查，发现潜在问题
- **单元测试**：为关键功能编写单元测试
- **集成测试**：测试系统各组件的交互
- **静态分析**：使用静态分析工具检查代码

### 系统设计
- **容错设计**：设计具有容错能力的系统
- **冗余设计**：关键组件使用冗余设计
- **降级设计**：在故障时能够降级运行
- **自诊断**：系统能够自我诊断和报告问题

### 硬件设计
- **电源设计**：确保电源稳定可靠
- **信号完整性**：确保信号传输的完整性
- **电磁兼容**：设计符合电磁兼容要求
- **热设计**：确保系统散热良好

### 运行时监控
- **健康检查**：定期检查系统健康状态
- **性能监控**：监控系统性能指标
- **安全监控**：监控安全相关事件
- **异常监控**：监控系统异常情况

## 应用实例

### 系统启动诊断
```c
// 系统启动诊断
void System_Startup_Diagnostic(void) {
    printf("System Startup Diagnostic\n");
    printf("==============================\n");
    
    // 检查复位原因
    Check_Reset_Reason();
    
    // 检查时钟配置
    Check_Clock_Config();
    
    // 检查硬件初始化
    if (!Check_Hardware_Init()) {
        printf("Hardware initialization failed!\n");
        // 进入安全模式
        Safe_Mode();
    }
    
    // 检查内存使用
    Monitor_Memory_Usage();
    
    // 检查通信接口
    if (!Check_Communication()) {
        printf("Communication check failed!\n");
        // 处理通信故障
    }
    
    // 检查传感器
    if (!Check_Sensors()) {
        printf("Sensor check failed!\n");
        // 处理传感器故障
    }
    
    printf("Startup diagnostic completed successfully!\n");
    printf("==============================\n");
}

// 主函数
int main(void) {
    // 系统启动诊断
    System_Startup_Diagnostic();
    
    // 初始化系统
    System_Init();
    
    // 主循环
    while(1) {
        // 定期进行运行时诊断
        if (Get_System_Tick() % 60000 == 0) {  // 每分钟
            Runtime_Diagnostic();
        }
        
        // 主程序逻辑
        Main_Loop();
    }
}
```

### 运行时诊断
```c
// 运行时诊断
void Runtime_Diagnostic(void) {
    printf("Runtime Diagnostic\n");
    printf("==============================\n");
    
    // 检查系统状态
    Show_System_Status();
    
    // 检查内存使用
    Monitor_Memory_Usage();
    
    // 检查任务状态
    if (osKernelGetState() == osKernelRunning) {
        Show_Task_Status();
    }
    
    // 检查通信状态
    Check_Communication_Status();
    
    // 检查传感器状态
    Check_Sensor_Status();
    
    // 检查错误日志
    Check_Error_Log();
    
    printf("Runtime diagnostic completed!\n");
    printf("==============================\n");
}

// 错误处理
void Error_Handler(uint32_t error_code, const char* error_msg) {
    // 记录错误
    Log(LOG_LEVEL_ERROR, "Error %d: %s", error_code, error_msg);
    
    // 保存错误信息到Flash
    Save_Error_Log(error_code, error_msg);
    
    // 根据错误类型处理
    switch (error_code) {
        case ERROR_MEMORY:
            // 内存错误处理
            Handle_Memory_Error();
            break;
        case ERROR_COMMUNICATION:
            // 通信错误处理
            Handle_Communication_Error();
            break;
        case ERROR_SENSOR:
            // 传感器错误处理
            Handle_Sensor_Error();
            break;
        case ERROR_HARDWARE:
            // 硬件错误处理
            Handle_Hardware_Error();
            break;
        default:
            // 其他错误处理
            Handle_General_Error();
            break;
    }
}
```

### 远程诊断
```c
// 远程诊断服务器
void Remote_Diagnostic_Server(void) {
    // 初始化网络连接
    Network_Init();
    
    // 等待连接
    while(1) {
        // 接受客户端连接
        int client_socket = Network_Accept();
        if (client_socket >= 0) {
            // 处理客户端请求
            Handle_Remote_Request(client_socket);
            
            // 关闭连接
            Network_Close(client_socket);
        }
        
        delay_ms(100);
    }
}

// 处理远程请求
void Handle_Remote_Request(int socket) {
    // 接收请求
    char request[1024];
    int bytes_received = Network_Receive(socket, request, sizeof(request));
    if (bytes_received > 0) {
        request[bytes_received] = '\0';
        
        // 解析请求
        if (strcmp(request, "GET_STATUS") == 0) {
            // 发送系统状态
            char response[2048];
            sprintf(response, "System status:\n" 
                    "Uptime: %d seconds\n" 
                    "Temperature: %.2f C\n" 
                    "Humidity: %.2f %%\n" 
                    "Battery: %.2f V\n" 
                    "Free memory: %d bytes\n",
                    Get_System_Tick() / 1000,
                    Read_Temperature(),
                    Read_Humidity(),
                    Read_Battery_Voltage(),
                    Get_Free_Memory());
            Network_Send(socket, response, strlen(response));
        } else if (strcmp(request, "GET_ERROR_LOG") == 0) {
            // 发送错误日志
            char response[4096];
            Get_Error_Log(response, sizeof(response));
            Network_Send(socket, response, strlen(response));
        } else if (strcmp(request, "RESET") == 0) {
            // 重置系统
            Network_Send(socket, "System resetting...\n", 19);
            delay_ms(100);
            NVIC_SystemReset();
        } else {
            // 未知请求
            Network_Send(socket, "Unknown request\n", 17);
        }
    }
}
```

## 总结
运行时问题诊断是嵌入式系统开发中的重要环节，通过有效的诊断方法和工具，可以快速定位和解决系统运行过程中出现的问题。本章节提供了各种微控制器的运行时问题诊断方法，包括常见运行时问题的识别、分析和解决方案，以及诊断工具和预防措施。通过建立完善的运行时诊断系统，可以提高系统的可靠性和可维护性，减少系统故障的发生，确保系统稳定运行。