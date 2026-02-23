# 串口通信

## 概述

串口通信是单片机与外部设备进行数据交换的重要方式，广泛应用于调试、数据传输、设备控制等场景。本文档将详细介绍国产单片机的串口通信实现方法，包括初始化配置、数据发送与接收、中断处理等。

## 基本概念

### 串口通信参数
- **波特率**：数据传输速率，单位为bps（比特每秒）
- **数据位**：每个字符的数据位数，通常为8位
- **停止位**：每个字符结束时的停止位数，通常为1位
- **奇偶校验**：用于检测数据传输错误的机制，包括奇校验、偶校验和无校验

### 串口工作模式
- **查询模式**：通过轮询方式检查串口状态
- **中断模式**：通过中断处理串口事件
- **DMA模式**：通过DMA控制器自动处理数据传输

## STC系列串口通信

### STC89C51串口通信

#### 寄存器说明
- **SCON**：串口控制寄存器
- **PCON**：电源控制寄存器（包含波特率倍增位）
- **TH1/TL1**：定时器1的高/低字节（用于波特率生成）
- **IE**：中断允许寄存器
- **IP**：中断优先级寄存器

#### 波特率计算

对于STC89C51，波特率计算公式为：
 	ext{波特率} = rac{f_{osc}}{12 	imes 32 	imes (256 - 	ext{TH1})} （当SMOD=0时）
 	ext{波特率} = rac{f_{osc}}{12 	imes 16 	imes (256 - 	ext{TH1})} （当SMOD=1时）

其中， f_{osc}  为晶振频率。

#### 示例：串口初始化与发送

```c
#include <reg51.h>

#define FOSC 11059200UL
#define BAUD 9600

void UART_Init() {
    // 设置波特率
    SCON = 0x50; // 8位数据，可变波特率
    PCON |= 0x80; // SMOD=1，波特率倍增
    TMOD &= 0x0F; // 清除定时器1模式位
    TMOD |= 0x20; // 定时器1工作在模式2
    TH1 = 256 - (FOSC / (16 * 12 * BAUD));
    TL1 = TH1; // 自动重装
    TR1 = 1; // 启动定时器1
    ES = 1; // 允许串口中断
    EA = 1; // 允许总中断
}

void UART_SendByte(unsigned char byte) {
    SBUF = byte;
    while(!TI); // 等待发送完成
    TI = 0; // 清除发送标志
}

void UART_SendString(unsigned char *str) {
    while(*str) {
        UART_SendByte(*str++);
    }
}

void UART_ISR() interrupt 4 {
    if(RI) {
        RI = 0; // 清除接收标志
        // 处理接收数据
        unsigned char recv_data = SBUF;
        // 可以在这里添加数据处理逻辑
    }
    if(TI) {
        TI = 0; // 清除发送标志
    }
}

void main() {
    UART_Init();
    UART_SendString("Hello, STC89C51!\r\n");
    
    while(1) {
        // 主循环
    }
}
```

### STC12C5A60S2串口通信

#### 寄存器说明
- **SCON**：串口控制寄存器
- **AUXR**：辅助寄存器（包含波特率控制位）
- **TH1/TL1**：定时器1的高/低字节
- **IE**：中断允许寄存器
- **IP**：中断优先级寄存器

#### 波特率计算

对于STC12C5A60S2，波特率计算公式为：
 	ext{波特率} = rac{f_{osc}}{16 	imes (256 - 	ext{TH1})} （当AUXR的BRTR位为1时）

#### 示例：串口初始化与中断接收

```c
#include <STC12C5A60S2.h>

#define FOSC 24000000UL
#define BAUD 115200

void UART_Init() {
    // 设置波特率
    SCON = 0x50; // 8位数据，可变波特率
    AUXR |= 0x40; // 定时器1工作在1T模式
    AUXR &= 0xFE; // 定时器1为16位自动重装
    TMOD &= 0x0F; // 清除定时器1模式位
    TH1 = 256 - (FOSC / (16 * BAUD));
    TL1 = TH1; // 自动重装
    TR1 = 1; // 启动定时器1
    ES = 1; // 允许串口中断
    EA = 1; // 允许总中断
}

void UART_SendByte(unsigned char byte) {
    SBUF = byte;
    while(!TI); // 等待发送完成
    TI = 0; // 清除发送标志
}

void UART_ISR() interrupt 4 {
    if(RI) {
        RI = 0; // 清除接收标志
        unsigned char recv_data = SBUF;
        // 回显接收到的数据
        UART_SendByte(recv_data);
    }
}

void main() {
    UART_Init();
    UART_SendString("Hello, STC12C5A60S2!\r\n");
    
    while(1) {
        // 主循环
    }
}
```

## GD32系列串口通信

### GD32F103串口通信

#### 寄存器说明
- **USARTx_CTL0**：串口控制寄存器0
- **USARTx_CTL1**：串口控制寄存器1
- **USARTx_BAUD**：波特率寄存器
- **USARTx_DATA**：数据寄存器
- **USARTx_STAT**：状态寄存器
- **USARTx_RT**：接收超时寄存器
- **USARTx_ADD**：地址寄存器

#### 波特率计算

对于GD32F103，波特率计算公式为：
 	ext{波特率} = rac{f_{PCLK}}{16 	imes 	ext{USART_BAUD}} 

其中， f_{PCLK}  为外设时钟频率。

#### 示例：串口初始化与DMA接收

```c
#include "gd32f10x.h"

#define BAUD 115200

void UART_Init(void) {
    // 使能USART0时钟
    rcu_periph_clock_enable(RCU_USART0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA9为USART0_TX
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    // 配置PA10为USART0_RX
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_10);
    
    // 配置USART0
    usart_deinit(USART0);
    usart_baudrate_set(USART0, BAUD);
    usart_word_length_set(USART0, USART_WL_8BIT);
    usart_stop_bit_set(USART0, USART_STB_1BIT);
    usart_parity_config(USART0, USART_PM_NONE);
    usart_hardware_flow_cts_config(USART0, USART_CTS_DISABLE);
    usart_hardware_flow_rts_config(USART0, USART_RTS_DISABLE);
    usart_receive_config(USART0, USART_RECEIVE_ENABLE);
    usart_transmit_config(USART0, USART_TRANSMIT_ENABLE);
    usart_enable(USART0);
}

void UART_SendByte(uint8_t byte) {
    usart_data_transmit(USART0, byte);
    while(RESET == usart_flag_get(USART0, USART_FLAG_TBE));
}

void UART_SendString(uint8_t *str) {
    while(*str) {
        UART_SendByte(*str++);
    }
}

uint8_t UART_ReceiveByte(void) {
    while(RESET == usart_flag_get(USART0, USART_FLAG_RBNE));
    return usart_data_receive(USART0);
}

int main(void) {
    UART_Init();
    UART_SendString("Hello, GD32F103!\r\n");
    
    while(1) {
        uint8_t data = UART_ReceiveByte();
        UART_SendByte(data);
    }
}
```

## HC32系列串口通信

### HC32F460串口通信

#### 寄存器说明
- **M0P_USARTx_CR1**：控制寄存器1
- **M0P_USARTx_CR2**：控制寄存器2
- **M0P_USARTx_BRR**：波特率寄存器
- **M0P_USARTx_DR**：数据寄存器
- **M0P_USARTx_SR**：状态寄存器
- **M0P_USARTx_GTOR**：接收超时寄存器
- **M0P_USARTx_PSC**：预分频寄存器

#### 示例：串口初始化与中断接收

```c
#include "hc32f460.h"

#define BAUD 115200

void UART_Init(void) {
    // 使能USART0时钟
    CLK_FcgPeriphClockCmd(CLK_FCG_USART0, ENABLE);
    // 使能GPIOA时钟
    CLK_FcgPeriphClockCmd(CLK_FCG_GPIOA, ENABLE);
    
    // 配置PA9为USART0_TX
    GPIO_SetFunc(GPIO_PORT_A, GPIO_PIN_9, GPIO_FUNC_3);
    // 配置PA10为USART0_RX
    GPIO_SetFunc(GPIO_PORT_A, GPIO_PIN_10, GPIO_FUNC_3);
    
    // 配置USART0
    USART_DeInit(M0P_USART0);
    USART_BaudRateSet(M0P_USART0, BAUD);
    USART_WordLengthSet(M0P_USART0, USART_WORDLEN_8BIT);
    USART_StopBitSet(M0P_USART0, USART_STOPBIT_1BIT);
    USART_ParityConfig(M0P_USART0, USART_PARITY_NONE);
    USART_DirectionConfig(M0P_USART0, USART_DIR_TX_RX);
    USART_FuncCmd(M0P_USART0, USART_FUNC_RX | USART_FUNC_TX, ENABLE);
    
    // 配置中断
    USART_IntCmd(M0P_USART0, USART_INT_RI, ENABLE);
    NVIC_ClearPendingIRQ(USART0_IRQn);
    NVIC_SetPriority(USART0_IRQn, 3);
    NVIC_EnableIRQ(USART0_IRQn);
}

void UART_SendByte(uint8_t byte) {
    USART_SendData(M0P_USART0, byte);
    while(USART_GetFlag(M0P_USART0, USART_FLAG_TC) == RESET);
}

void UART_SendString(uint8_t *str) {
    while(*str) {
        UART_SendByte(*str++);
    }
}

void USART0_IRQHandler(void) {
    if(USART_GetIntFlag(M0P_USART0, USART_INT_RI)) {
        uint8_t data = USART_ReceiveData(M0P_USART0);
        UART_SendByte(data); // 回显
        USART_ClearIntFlag(M0P_USART0, USART_INT_RI);
    }
}

int main(void) {
    UART_Init();
    UART_SendString("Hello, HC32F460!\r\n");
    
    while(1) {
        // 主循环
    }
}
```

## MM32系列串口通信

### MM32F103串口通信

#### 寄存器说明
- **USARTx_CR1**：控制寄存器1
- **USARTx_CR2**：控制寄存器2
- **USARTx_CR3**：控制寄存器3
- **USARTx_BRR**：波特率寄存器
- **USARTx_GTPR**：保护时间和预分频寄存器
- **USARTx_SR**：状态寄存器
- **USARTx_DR**：数据寄存器

#### 示例：串口初始化与发送接收

```c
#include "MM32F103.h"

#define BAUD 115200

void UART_Init(void) {
    // 使能USART1时钟
    RCC->APB2ENR |= RCC_APB2ENR_USART1EN;
    // 使能GPIOA时钟
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;
    
    // 配置PA9为USART1_TX
    GPIOA->CRH &= ~(0xF << 4);
    GPIOA->CRH |= (0xB << 4); // 复用推挽输出
    // 配置PA10为USART1_RX
    GPIOA->CRH &= ~(0xF << 8);
    GPIOA->CRH |= (0x4 << 8); // 浮空输入
    
    // 配置USART1
    USART1->BRR = SystemCoreClock / BAUD;
    USART1->CR1 |= USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;
}

void UART_SendByte(uint8_t byte) {
    while(!(USART1->SR & USART_SR_TXE));
    USART1->DR = byte;
    while(!(USART1->SR & USART_SR_TC));
}

void UART_SendString(uint8_t *str) {
    while(*str) {
        UART_SendByte(*str++);
    }
}

uint8_t UART_ReceiveByte(void) {
    while(!(USART1->SR & USART_SR_RXNE));
    return USART1->DR;
}

int main(void) {
    UART_Init();
    UART_SendString("Hello, MM32F103!\r\n");
    
    while(1) {
        uint8_t data = UART_ReceiveByte();
        UART_SendByte(data);
    }
}
```

## 通用串口操作函数

### 环形缓冲区实现

```c
#define BUFFER_SIZE 256

typedef struct {
    uint8_t buffer[BUFFER_SIZE];
    uint16_t head;
    uint16_t tail;
    uint16_t count;
} RingBuffer;

void RingBuffer_Init(RingBuffer *rb) {
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
}

uint8_t RingBuffer_Put(RingBuffer *rb, uint8_t data) {
    if(rb->count >= BUFFER_SIZE) {
        return 0; // 缓冲区满
    }
    rb->buffer[rb->head] = data;
    rb->head = (rb->head + 1) % BUFFER_SIZE;
    rb->count++;
    return 1;
}

uint8_t RingBuffer_Get(RingBuffer *rb, uint8_t *data) {
    if(rb->count == 0) {
        return 0; // 缓冲区空
    }
    *data = rb->buffer[rb->tail];
    rb->tail = (rb->tail + 1) % BUFFER_SIZE;
    rb->count--;
    return 1;
}

uint16_t RingBuffer_Count(RingBuffer *rb) {
    return rb->count;
}
```

### 串口命令解析

```c
#define MAX_COMMAND_LENGTH 64

typedef struct {
    uint8_t buffer[MAX_COMMAND_LENGTH];
    uint16_t length;
} CommandBuffer;

void CommandBuffer_Init(CommandBuffer *cb) {
    cb->length = 0;
}

void CommandBuffer_Add(CommandBuffer *cb, uint8_t data) {
    if(cb->length < MAX_COMMAND_LENGTH - 1) {
        cb->buffer[cb->length++] = data;
        cb->buffer[cb->length] = '\0';
    }
}

void CommandBuffer_Reset(CommandBuffer *cb) {
    cb->length = 0;
    cb->buffer[0] = '\0';
}

void ProcessCommand(uint8_t *command) {
    // 简单的命令处理示例
    if(strcmp((char *)command, "help") == 0) {
        UART_SendString("Available commands:\r\n");
        UART_SendString("help - Show this help\r\n");
        UART_SendString("status - Show system status\r\n");
        UART_SendString("reset - Reset system\r\n");
    } else if(strcmp((char *)command, "status") == 0) {
        UART_SendString("System status: OK\r\n");
    } else if(strcmp((char *)command, "reset") == 0) {
        UART_SendString("Resetting system...\r\n");
        // 执行复位操作
    } else {
        UART_SendString("Unknown command: ");
        UART_SendString(command);
        UART_SendString("\r\n");
    }
}
```

## 常见问题与解决方案

### 问题1：串口通信乱码
- **原因**：波特率设置不正确，或者时钟频率配置错误
- **解决方案**：检查波特率计算是否正确，确认时钟频率设置

### 问题2：串口接收数据丢失
- **原因**：接收缓冲区溢出，或者中断处理不及时
- **解决方案**：使用环形缓冲区，优化中断处理代码

### 问题3：串口发送数据不完整
- **原因**：发送缓冲区未满就继续发送，或者硬件问题
- **解决方案**：确保发送完成后再发送下一个字节，检查硬件连接

### 问题4：中断不触发
- **原因**：中断未使能，或者优先级设置错误
- **解决方案**：检查中断使能位，确认中断优先级配置

## 最佳实践

1. **波特率选择**：根据通信距离和干扰情况选择合适的波特率，一般短距离通信使用9600或115200bps
2. **缓冲区设计**：使用环形缓冲区提高数据处理效率，避免数据丢失
3. **错误处理**：添加奇偶校验或其他错误检测机制，提高通信可靠性
4. **中断优化**：中断处理函数应尽量简短，避免在中断中执行耗时操作
5. **电源管理**：在不需要通信时，可以关闭串口时钟以降低功耗
6. **抗干扰**：使用屏蔽线缆，增加地线，远离干扰源

## 示例项目

### 项目：串口调试助手

#### 功能描述
- 实现串口数据的发送和接收
- 支持命令解析和执行
- 提供系统状态查询

#### 代码实现

```c
#include "gd32f10x.h"
#include <string.h>

#define BAUD 115200

RingBuffer rx_buffer;
CommandBuffer cmd_buffer;

void UART_Init(void) {
    // 使能USART0时钟
    rcu_periph_clock_enable(RCU_USART0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA9为USART0_TX
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    // 配置PA10为USART0_RX
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_10);
    
    // 配置USART0
    usart_deinit(USART0);
    usart_baudrate_set(USART0, BAUD);
    usart_word_length_set(USART0, USART_WL_8BIT);
    usart_stop_bit_set(USART0, USART_STB_1BIT);
    usart_parity_config(USART0, USART_PM_NONE);
    usart_hardware_flow_cts_config(USART0, USART_CTS_DISABLE);
    usart_hardware_flow_rts_config(USART0, USART_RTS_DISABLE);
    usart_receive_config(USART0, USART_RECEIVE_ENABLE);
    usart_transmit_config(USART0, USART_TRANSMIT_ENABLE);
    
    // 配置中断
    nvic_irq_enable(USART0_IRQn, 0, 0);
    usart_interrupt_enable(USART0, USART_INT_RBNE);
    
    usart_enable(USART0);
}

void UART_SendByte(uint8_t byte) {
    usart_data_transmit(USART0, byte);
    while(RESET == usart_flag_get(USART0, USART_FLAG_TBE));
}

void UART_SendString(uint8_t *str) {
    while(*str) {
        UART_SendByte(*str++);
    }
}

void USART0_IRQHandler(void) {
    if(RESET != usart_flag_get(USART0, USART_FLAG_RBNE)) {
        uint8_t data = usart_data_receive(USART0);
        RingBuffer_Put(&rx_buffer, data);
    }
}

void ProcessSerialData(void) {
    uint8_t data;
    while(RingBuffer_Get(&rx_buffer, &data)) {
        if(data == '\r' || data == '\n') {
            // 命令结束，处理命令
            if(cmd_buffer.length > 0) {
                ProcessCommand(cmd_buffer.buffer);
                CommandBuffer_Reset(&cmd_buffer);
            }
        } else {
            // 添加到命令缓冲区
            CommandBuffer_Add(&cmd_buffer, data);
        }
    }
}

int main(void) {
    RingBuffer_Init(&rx_buffer);
    CommandBuffer_Init(&cmd_buffer);
    UART_Init();
    
    UART_SendString("Serial Debug Assistant\r\n");
    UART_SendString("Type 'help' for available commands\r\n");
    
    while(1) {
        ProcessSerialData();
        // 其他任务
    }
}
```

### 项目：Modbus RTU通信

#### 功能描述
- 实现Modbus RTU协议的基本功能
- 支持读取和写入保持寄存器
- 提供错误检测和处理

#### 代码实现

```c
#include "gd32f10x.h"

#define BAUD 9600
#define SLAVE_ADDRESS 0x01

uint16_t holding_registers[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

void UART_Init(void) {
    // 使能USART0时钟
    rcu_periph_clock_enable(RCU_USART0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA9为USART0_TX
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    // 配置PA10为USART0_RX
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_10);
    
    // 配置USART0
    usart_deinit(USART0);
    usart_baudrate_set(USART0, BAUD);
    usart_word_length_set(USART0, USART_WL_8BIT);
    usart_stop_bit_set(USART0, USART_STB_1BIT);
    usart_parity_config(USART0, USART_PM_NONE);
    usart_hardware_flow_cts_config(USART0, USART_CTS_DISABLE);
    usart_hardware_flow_rts_config(USART0, USART_RTS_DISABLE);
    usart_receive_config(USART0, USART_RECEIVE_ENABLE);
    usart_transmit_config(USART0, USART_TRANSMIT_ENABLE);
    usart_enable(USART0);
}

uint16_t CalculateCRC(uint8_t *data, uint8_t length) {
    uint16_t crc = 0xFFFF;
    uint8_t i, j;
    
    for(i = 0; i < length; i++) {
        crc ^= data[i];
        for(j = 0; j < 8; j++) {
            if(crc & 0x0001) {
                crc >>= 1;
                crc ^= 0xA001;
            } else {
                crc >>= 1;
            }
        }
    }
    
    return crc;
}

void ProcessModbusRequest(uint8_t *request, uint8_t length) {
    if(length < 8) return; // 最小Modbus RTU帧长度
    
    // 检查从站地址
    if(request[0] != SLAVE_ADDRESS) return;
    
    // 检查CRC
    uint16_t received_crc = (request[length-1] << 8) | request[length-2];
    uint16_t calculated_crc = CalculateCRC(request, length-2);
    if(received_crc != calculated_crc) return;
    
    uint8_t function_code = request[1];
    uint16_t start_address = (request[2] << 8) | request[3];
    uint16_t quantity = (request[4] << 8) | request[5];
    
    switch(function_code) {
        case 0x03: // 读取保持寄存器
            if(start_address + quantity <= 10) {
                uint8_t response[5 + quantity*2];
                response[0] = SLAVE_ADDRESS;
                response[1] = 0x03;
                response[2] = quantity * 2;
                
                for(uint8_t i = 0; i < quantity; i++) {
                    response[3 + i*2] = holding_registers[start_address + i] >> 8;
                    response[4 + i*2] = holding_registers[start_address + i] & 0xFF;
                }
                
                uint16_t crc = CalculateCRC(response, 3 + quantity*2);
                response[3 + quantity*2] = crc & 0xFF;
                response[4 + quantity*2] = crc >> 8;
                
                for(uint8_t i = 0; i < 5 + quantity*2; i++) {
                    UART_SendByte(response[i]);
                }
            } else {
                // 地址超出范围
                uint8_t response[5];
                response[0] = SLAVE_ADDRESS;
                response[1] = 0x83;
                response[2] = 0x02;
                uint16_t crc = CalculateCRC(response, 3);
                response[3] = crc & 0xFF;
                response[4] = crc >> 8;
                
                for(uint8_t i = 0; i < 5; i++) {
                    UART_SendByte(response[i]);
                }
            }
            break;
            
        case 0x06: // 写入单个保持寄存器
            if(start_address < 10) {
                uint16_t value = (request[4] << 8) | request[5];
                holding_registers[start_address] = value;
                
                // 发送确认
                for(uint8_t i = 0; i < length; i++) {
                    UART_SendByte(request[i]);
                }
            } else {
                // 地址超出范围
                uint8_t response[5];
                response[0] = SLAVE_ADDRESS;
                response[1] = 0x86;
                response[2] = 0x02;
                uint16_t crc = CalculateCRC(response, 3);
                response[3] = crc & 0xFF;
                response[4] = crc >> 8;
                
                for(uint8_t i = 0; i < 5; i++) {
                    UART_SendByte(response[i]);
                }
            }
            break;
    }
}

int main(void) {
    UART_Init();
    
    uint8_t buffer[256];
    uint8_t index = 0;
    
    while(1) {
        if(RESET != usart_flag_get(USART0, USART_FLAG_RBNE)) {
            buffer[index++] = usart_data_receive(USART0);
            // 简单的帧检测，这里仅作为示例
            if(index >= 8) {
                ProcessModbusRequest(buffer, index);
                index = 0;
            }
        }
    }
}
```

## 总结

串口通信是单片机开发中非常重要的通信方式，本文档提供了STC、GD32、HC32、MM32等国产单片机的串口通信实现方法，包括初始化配置、数据发送与接收、中断处理、缓冲区设计等内容。

在实际开发中，应根据具体的单片机型号和应用场景选择合适的串口配置方案，同时注意波特率设置、缓冲区设计和错误处理，以确保通信的可靠性和稳定性。

通过本文档的学习，开发者可以掌握国产单片机的串口通信技术，为嵌入式系统开发打下坚实的基础。