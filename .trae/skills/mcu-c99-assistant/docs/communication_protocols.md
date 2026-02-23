# 通信协议实现

## 概述

通信协议是嵌入式系统中不同设备之间交换数据的规则和标准。本文档将介绍在嵌入式系统中常见的通信协议实现，包括串口通信、I2C、SPI、CAN、以太网等，以及它们在不同系列微控制器上的应用。

## 串口通信 (UART/USART)

### 基本原理
- **UART** (Universal Asynchronous Receiver Transmitter)：通用异步收发器
- **USART** (Universal Synchronous/Asynchronous Receiver Transmitter)：通用同步/异步收发器
- **波特率**：数据传输速率，常见值有9600、115200等
- **数据格式**：起始位、数据位、奇偶校验位、停止位

### STC系列微控制器实现

```c
#include "stc8.h"

// 串口初始化
void UART_Init(uint32_t baudrate)
{
    SCON = 0x50;  // 8位数据，可变波特率
    AUXR |= 0x40; // 定时器1作为波特率发生器
    AUXR &= 0xFE; // 定时器1为12T模式
    TMOD &= 0x0F; // 清除定时器1模式位
    TMOD |= 0x20; // 定时器1为模式2（8位自动重载）
    TL1 = TH1 = 256 - (11059200 / 12 / baudrate); // 计算波特率初值
    TR1 = 1;      // 启动定时器1
    ES = 1;       // 开启串口中断
    EA = 1;       // 开启总中断
}

// 串口发送函数
void UART_SendByte(uint8_t byte)
{
    SBUF = byte;
    while(!TI);
    TI = 0;
}

// 串口发送字符串
void UART_SendString(char *str)
{
    while(*str) {
        UART_SendByte(*str++);
    }
}

// 串口中断服务函数
void UART_ISR(void) interrupt 4
{
    if(RI) {
        RI = 0;
        // 处理接收的数据
        uint8_t data = SBUF;
        // 这里可以添加数据处理逻辑
    }
    if(TI) {
        TI = 0;
    }
}

// 主函数
void main(void)
{
    UART_Init(9600);
    UART_SendString("Hello, UART!\r\n");
    
    while(1) {
        // 主循环
    }
}
```

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// 串口初始化
void UART_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能USART0时钟
    rcu_periph_clock_enable(RCU_USART0);
    
    // 配置PA9为USART0_TX
    gpio_af_set(GPIOA, GPIO_AF_7, GPIO_PIN_9);
    // 配置PA10为USART0_RX
    gpio_af_set(GPIOA, GPIO_AF_7, GPIO_PIN_10);
    
    // 配置GPIO
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_9 | GPIO_PIN_10);
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    
    // 配置USART0
    usart_deinit(USART0);
    usart_baudrate_set(USART0, 115200);
    usart_word_length_set(USART0, USART_WL_8BIT);
    usart_stop_bit_set(USART0, USART_STB_1BIT);
    usart_parity_config(USART0, USART_PM_NONE);
    usart_hardware_flow_cts_config(USART0, USART_CTS_DISABLE);
    usart_hardware_flow_rts_config(USART0, USART_RTS_DISABLE);
    usart_receive_config(USART0, USART_RECEIVE_ENABLE);
    usart_transmit_config(USART0, USART_TRANSMIT_ENABLE);
    usart_enable(USART0);
}

// 串口发送函数
void UART_SendByte(uint8_t byte)
{
    usart_data_transmit(USART0, byte);
    while(RESET == usart_flag_get(USART0, USART_FLAG_TBE));
}

// 串口发送字符串
void UART_SendString(char *str)
{
    while(*str) {
        UART_SendByte(*str++);
    }
}

// 串口接收函数
uint8_t UART_ReceiveByte(void)
{
    while(RESET == usart_flag_get(USART0, USART_FLAG_RBNE));
    return (uint8_t)usart_data_receive(USART0);
}

// 主函数
int main(void)
{
    UART_Init();
    UART_SendString("Hello, USART!\r\n");
    
    while(1) {
        // 主循环
    }
}
```

## I2C通信

### 基本原理
- **I2C** (Inter-Integrated Circuit)：集成电路间总线
- **特点**：两线制（SCL时钟线和SDA数据线）、多主机支持、从机地址识别
- **通信速率**：标准模式(100kHz)、快速模式(400kHz)、高速模式(3.4MHz)

### STC系列微控制器实现

```c
#include "stc8.h"

#define SCL P3_2
#define SDA P3_3

// 延时函数
void I2C_Delay(void)
{
    uint8_t i = 10;
    while(i--);
}

// 初始化I2C
void I2C_Init(void)
{
    SCL = 1;
    SDA = 1;
}

// 启动I2C
void I2C_Start(void)
{
    SDA = 1;
    SCL = 1;
    I2C_Delay();
    SDA = 0;
    I2C_Delay();
    SCL = 0;
}

// 停止I2C
void I2C_Stop(void)
{
    SDA = 0;
    SCL = 1;
    I2C_Delay();
    SDA = 1;
    I2C_Delay();
}

// 发送应答
void I2C_SendAck(uint8_t ack)
{
    SDA = ack;
    SCL = 1;
    I2C_Delay();
    SCL = 0;
    I2C_Delay();
}

// 接收应答
uint8_t I2C_ReceiveAck(void)
{
    uint8_t ack;
    SDA = 1;
    SCL = 1;
    I2C_Delay();
    ack = SDA;
    SCL = 0;
    I2C_Delay();
    return ack;
}

// 发送字节
void I2C_SendByte(uint8_t byte)
{
    uint8_t i;
    for(i = 0; i < 8; i++) {
        SDA = (byte & 0x80) >> 7;
        SCL = 1;
        I2C_Delay();
        SCL = 0;
        I2C_Delay();
        byte <<= 1;
    }
}

// 接收字节
uint8_t I2C_ReceiveByte(void)
{
    uint8_t i, byte = 0;
    for(i = 0; i < 8; i++) {
        SCL = 1;
        I2C_Delay();
        byte <<= 1;
        byte |= SDA;
        SCL = 0;
        I2C_Delay();
    }
    return byte;
}

// 向从设备写入数据
void I2C_Write(uint8_t addr, uint8_t reg, uint8_t data)
{
    I2C_Start();
    I2C_SendByte(addr << 1);  // 写入模式
    I2C_ReceiveAck();
    I2C_SendByte(reg);
    I2C_ReceiveAck();
    I2C_SendByte(data);
    I2C_ReceiveAck();
    I2C_Stop();
}

// 从从设备读取数据
uint8_t I2C_Read(uint8_t addr, uint8_t reg)
{
    uint8_t data;
    I2C_Start();
    I2C_SendByte(addr << 1);  // 写入模式
    I2C_ReceiveAck();
    I2C_SendByte(reg);
    I2C_ReceiveAck();
    I2C_Start();
    I2C_SendByte((addr << 1) | 0x01);  // 读取模式
    I2C_ReceiveAck();
    data = I2C_ReceiveByte();
    I2C_SendAck(1);  // 发送非应答
    I2C_Stop();
    return data;
}
```

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// I2C初始化
void I2C_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOB);
    // 使能I2C0时钟
    rcu_periph_clock_enable(RCU_I2C0);
    
    // 配置PB6为I2C0_SCL
    gpio_af_set(GPIOB, GPIO_AF_4, GPIO_PIN_6);
    // 配置PB7为I2C0_SDA
    gpio_af_set(GPIOB, GPIO_AF_4, GPIO_PIN_7);
    
    // 配置GPIO
    gpio_mode_set(GPIOB, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_6 | GPIO_PIN_7);
    gpio_output_options_set(GPIOB, GPIO_OTYPE_OD, GPIO_OSPEED_50MHZ, GPIO_PIN_6 | GPIO_PIN_7);
    
    // 配置I2C0
    i2c_deinit(I2C0);
    i2c_clock_config(I2C0, 100000, I2C_DTCY_2);
    i2c_mode_addr_config(I2C0, I2C_I2CMODE_ENABLE, I2C_ADDFORMAT_7BITS, 0x00);
    i2c_enable(I2C0);
}

// 向从设备写入数据
void I2C_Write(uint8_t addr, uint8_t reg, uint8_t data)
{
    // 等待总线空闲
    while(i2c_flag_get(I2C0, I2C_FLAG_I2CBSY));
    
    // 发送起始信号
    i2c_start_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_SBSEND));
    
    // 发送设备地址
    i2c_master_addressing(I2C0, addr << 1, I2C_TRANSMITTER);
    while(!i2c_flag_get(I2C0, I2C_FLAG_ADDSEND));
    i2c_flag_clear(I2C0, I2C_FLAG_ADDSEND);
    
    // 发送寄存器地址
    i2c_data_transmit(I2C0, reg);
    while(!i2c_flag_get(I2C0, I2C_FLAG_TBE));
    
    // 发送数据
    i2c_data_transmit(I2C0, data);
    while(!i2c_flag_get(I2C0, I2C_FLAG_TBE));
    
    // 发送停止信号
    i2c_stop_on_bus(I2C0);
    while(i2c_flag_get(I2C0, I2C_FLAG_STPDET));
}

// 从从设备读取数据
uint8_t I2C_Read(uint8_t addr, uint8_t reg)
{
    uint8_t data;
    
    // 等待总线空闲
    while(i2c_flag_get(I2C0, I2C_FLAG_I2CBSY));
    
    // 发送起始信号
    i2c_start_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_SBSEND));
    
    // 发送设备地址（写入模式）
    i2c_master_addressing(I2C0, addr << 1, I2C_TRANSMITTER);
    while(!i2c_flag_get(I2C0, I2C_FLAG_ADDSEND));
    i2c_flag_clear(I2C0, I2C_FLAG_ADDSEND);
    
    // 发送寄存器地址
    i2c_data_transmit(I2C0, reg);
    while(!i2c_flag_get(I2C0, I2C_FLAG_TBE));
    
    // 重新发送起始信号
    i2c_start_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_SBSEND));
    
    // 发送设备地址（读取模式）
    i2c_master_addressing(I2C0, addr << 1, I2C_RECEIVER);
    while(!i2c_flag_get(I2C0, I2C_FLAG_ADDSEND));
    i2c_flag_clear(I2C0, I2C_FLAG_ADDSEND);
    
    // 接收数据
    while(!i2c_flag_get(I2C0, I2C_FLAG_RBNE));
    data = i2c_data_receive(I2C0);
    
    // 发送非应答
    i2c_ack_config(I2C0, I2C_ACK_DISABLE);
    
    // 发送停止信号
    i2c_stop_on_bus(I2C0);
    while(i2c_flag_get(I2C0, I2C_FLAG_STPDET));
    
    // 重新使能应答
    i2c_ack_config(I2C0, I2C_ACK_ENABLE);
    
    return data;
}
```

## SPI通信

### 基本原理
- **SPI** (Serial Peripheral Interface)：串行外设接口
- **特点**：四线制（SCLK时钟线、MOSI主出从入、MISO主入从出、SS片选线）、全双工通信
- **通信速率**：最高可达几MHz，取决于设备能力

### STC系列微控制器实现

```c
#include "stc8.h"

#define SCK P1_7
#define MOSI P1_5
#define MISO P1_6
#define SS P1_4

// 初始化SPI
void SPI_Init(void)
{
    // 配置GPIO
    SCK = 0;
    MOSI = 1;
    MISO = 1;
    SS = 1;
}

// SPI发送接收字节
uint8_t SPI_Transfer(uint8_t data)
{
    uint8_t i, rx_data = 0;
    
    for(i = 0; i < 8; i++) {
        // 发送一位
        MOSI = (data & 0x80) >> 7;
        data <<= 1;
        
        // 时钟上升沿
        SCK = 1;
        
        // 接收一位
        rx_data <<= 1;
        rx_data |= MISO;
        
        // 时钟下降沿
        SCK = 0;
    }
    
    return rx_data;
}

// 向SPI设备写入数据
void SPI_Write(uint8_t reg, uint8_t data)
{
    SS = 0;  // 使能片选
    SPI_Transfer(reg);  // 发送寄存器地址
    SPI_Transfer(data);  // 发送数据
    SS = 1;  // 禁用片选
}

// 从SPI设备读取数据
uint8_t SPI_Read(uint8_t reg)
{
    uint8_t data;
    SS = 0;  // 使能片选
    SPI_Transfer(reg | 0x80);  // 发送寄存器地址（读模式）
    data = SPI_Transfer(0xFF);  // 读取数据
    SS = 1;  // 禁用片选
    return data;
}
```

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// SPI初始化
void SPI_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能SPI0时钟
    rcu_periph_clock_enable(RCU_SPI0);
    
    // 配置PA5为SPI0_SCK
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_5);
    // 配置PA6为SPI0_MISO
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_6);
    // 配置PA7为SPI0_MOSI
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_7);
    // 配置PA4为SPI0_NSS
    gpio_mode_set(GPIOA, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, GPIO_PIN_4);
    
    // 配置GPIO
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7);
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_7);
    
    // 配置SPI0
    spi_deinit(SPI0);
    spi_init(SPI0, SPI_MODE_MASTER, SPI_TRANSMODE_FULLDUPLEX, SPI_FRAMESIZE_8BIT, SPI_NSS_SOFT, 128);
    spi_enable(SPI0);
    
    // 初始化解选
    GPIO_BOP(GPIOA) = GPIO_PIN_4;
}

// SPI发送接收字节
uint8_t SPI_Transfer(uint8_t data)
{
    // 等待发送缓冲区为空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_TBE));
    // 发送数据
    spi_data_transmit(SPI0, data);
    // 等待接收缓冲区非空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_RBNE));
    // 接收数据
    return spi_data_receive(SPI0);
}

// 向SPI设备写入数据
void SPI_Write(uint8_t reg, uint8_t data)
{
    // 使能片选
    GPIO_BC(GPIOA) = GPIO_PIN_4;
    // 发送寄存器地址
    SPI_Transfer(reg);
    // 发送数据
    SPI_Transfer(data);
    // 禁用片选
    GPIO_BOP(GPIOA) = GPIO_PIN_4;
}

// 从SPI设备读取数据
uint8_t SPI_Read(uint8_t reg)
{
    uint8_t data;
    // 使能片选
    GPIO_BC(GPIOA) = GPIO_PIN_4;
    // 发送寄存器地址（读模式）
    SPI_Transfer(reg | 0x80);
    // 读取数据
    data = SPI_Transfer(0xFF);
    // 禁用片选
    GPIO_BOP(GPIOA) = GPIO_PIN_4;
    return data;
}
```

## CAN通信

### 基本原理
- **CAN** (Controller Area Network)：控制器局域网
- **特点**：差分信号传输、抗干扰能力强、支持多节点通信
- **应用场景**：汽车电子、工业控制、机器人等

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// CAN初始化
void CAN_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能CAN0时钟
    rcu_periph_clock_enable(RCU_CAN0);
    
    // 配置PA11为CAN0_RX
    gpio_af_set(GPIOA, GPIO_AF_9, GPIO_PIN_11);
    // 配置PA12为CAN0_TX
    gpio_af_set(GPIOA, GPIO_AF_9, GPIO_PIN_12);
    
    // 配置GPIO
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_11 | GPIO_PIN_12);
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_12);
    
    // 复位CAN0
    can_deinit(CAN0);
    
    // 配置CAN0
    can_parameter_struct can_parameter;
    can_struct_para_init(CAN_INIT_STRUCT, &can_parameter);
    can_parameter.time_triggered = DISABLE;
    can_parameter.auto_bus_off_recovery = ENABLE;
    can_parameter.auto_wake_up = DISABLE;
    can_parameter.auto_retrans = ENABLE;
    can_parameter.rec_fifo_overwrite = DISABLE;
    can_parameter.trans_fifo_order = DISABLE;
    can_parameter.working_mode = CAN_NORMAL_MODE;
    can_parameter.resync_jump_width = CAN_BT_SJW_1TQ;
    can_parameter.time_segment_1 = CAN_BT_BS1_5TQ;
    can_parameter.time_segment_2 = CAN_BT_BS2_3TQ;
    can_parameter.prescaler = 6;  // 1Mbps (48MHz / (6 * (1+5+3)))
    can_init(CAN0, &can_parameter);
    
    // 配置过滤器
    can_filter_parameter_struct can_filter;
    can_struct_para_init(CAN_FILTER_STRUCT, &can_filter);
    can_filter.filter_number = 0;
    can_filter.filter_mode = CAN_FILTERMODE_MASK;
    can_filter.filter_bits = CAN_FILTERBITS_32BIT;
    can_filter.filter_list_high = 0x0000;
    can_filter.filter_list_low = 0x0000;
    can_filter.filter_mask_high = 0x0000;
    can_filter.filter_mask_low = 0x0000;
    can_filter.filter_fifo_number = CAN_FIFO0;
    can_filter.filter_enable = ENABLE;
    can_filter_init(&can_filter);
}

// 发送CAN消息
uint8_t CAN_SendMessage(uint32_t id, uint8_t *data, uint8_t length)
{
    can_trasnmit_message_struct tx_message;
    can_struct_para_init(CAN_TX_MESSAGE_STRUCT, &tx_message);
    
    tx_message.tx_sfid = id;
    tx_message.tx_efid = 0;
    tx_message.tx_ft = CAN_FT_DATA;
    tx_message.tx_ff = CAN_FF_STANDARD;
    tx_message.tx_dlen = length;
    memcpy(tx_message.tx_data, data, length);
    
    return can_message_transmit(CAN0, &tx_message);
}

// 接收CAN消息
uint8_t CAN_ReceiveMessage(uint32_t *id, uint8_t *data, uint8_t *length)
{
    can_receive_message_struct rx_message;
    can_struct_para_init(CAN_RX_MESSAGE_STRUCT, &rx_message);
    
    if(can_message_receive(CAN0, CAN_FIFO0, &rx_message) == SUCCESS) {
        *id = rx_message.rx_sfid;
        memcpy(data, rx_message.rx_data, rx_message.rx_dlen);
        *length = rx_message.rx_dlen;
        return SUCCESS;
    }
    return ERROR;
}
```

## 以太网通信

### 基本原理
- **以太网**：基于IEEE 802.3标准的局域网技术
- **特点**：传输速率高、距离远、支持多节点通信
- **应用场景**：需要高速数据传输的嵌入式系统

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"
#include "lwip/netif.h"
#include "lwip/tcpip.h"
#include "lwip/dhcp.h"

// 网络接口
static struct netif gnetif;

// 网络初始化
void Ethernet_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    rcu_periph_clock_enable(RCU_GPIOB);
    rcu_periph_clock_enable(RCU_GPIOC);
    rcu_periph_clock_enable(RCU_GPIOD);
    rcu_periph_clock_enable(RCU_GPIOG);
    
    // 使能ETH时钟
    rcu_periph_clock_enable(RCU_ETH);
    
    // 配置GPIO
    // PA0-ETH_CRS_DV, PA1-ETH_RX_CLK, PA2-ETH_RX_EN, PA3-ETH_RX_DATA0, PA4-ETH_RX_DATA1
    // PA7-ETH_TX_EN, PB13-ETH_TX_CLK, PC1-ETH_TX_DATA0, PC2-ETH_TX_DATA1
    gpio_af_set(GPIOA, GPIO_AF_11, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3 | GPIO_PIN_4 | GPIO_PIN_7);
    gpio_af_set(GPIOB, GPIO_AF_11, GPIO_PIN_13);
    gpio_af_set(GPIOC, GPIO_AF_11, GPIO_PIN_1 | GPIO_PIN_2);
    
    // 配置GPIO模式
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3 | GPIO_PIN_4);
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLDOWN, GPIO_PIN_7);
    gpio_mode_set(GPIOB, GPIO_MODE_AF, GPIO_PUPD_PULLDOWN, GPIO_PIN_13);
    gpio_mode_set(GPIOC, GPIO_MODE_AF, GPIO_PUPD_PULLDOWN, GPIO_PIN_1 | GPIO_PIN_2);
    
    // 配置GPIO输出速度
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_100MHZ, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3 | GPIO_PIN_4 | GPIO_PIN_7);
    gpio_output_options_set(GPIOB, GPIO_OTYPE_PP, GPIO_OSPEED_100MHZ, GPIO_PIN_13);
    gpio_output_options_set(GPIOC, GPIO_OTYPE_PP, GPIO_OSPEED_100MHZ, GPIO_PIN_1 | GPIO_PIN_2);
    
    // 初始化LwIP
    tcpip_init(NULL, NULL);
    
    // 添加网络接口
    ip4_addr_t ipaddr, netmask, gw;
    IP4_ADDR(&ipaddr, 192, 168, 1, 100);
    IP4_ADDR(&netmask, 255, 255, 255, 0);
    IP4_ADDR(&gw, 192, 168, 1, 1);
    netif_add(&gnetif, &ipaddr, &netmask, &gw, NULL, ethernetif_init, tcpip_input);
    
    // 设置默认网络接口
    netif_set_default(&gnetif);
    
    // 启用网络接口
    netif_set_up(&gnetif);
    
    // 启动DHCP客户端
    dhcp_start(&gnetif);
}

// TCP服务器示例
void TCP_Server_Example(void)
{
    struct netconn *conn, *newconn;
    err_t err, accept_err;
    
    // 创建TCP连接
    conn = netconn_new(NETCONN_TCP);
    if(conn != NULL) {
        // 绑定端口
        err = netconn_bind(conn, NULL, 80);
        if(err == ERR_OK) {
            // 监听连接
            netconn_listen(conn);
            
            while(1) {
                // 接受连接
                accept_err = netconn_accept(conn, &newconn);
                if(accept_err == ERR_OK) {
                    // 处理连接
                    struct netbuf *buf;
                    void *data;
                    u16_t len;
                    
                    while(netconn_recv(newconn, &buf) == ERR_OK) {
                        do {
                            netbuf_data(buf, &data, &len);
                            // 处理接收到的数据
                            netconn_write(newconn, data, len, NETCONN_COPY);
                        } while(netbuf_next(buf) >= 0);
                        netbuf_delete(buf);
                    }
                    netconn_close(newconn);
                    netconn_delete(newconn);
                }
            }
        }
    }
}
```

## 无线通信协议

### 1. Wi-Fi
- **特点**：高速率、远距离、广泛应用
- **接口**：通常通过SPI或UART与Wi-Fi模块通信
- **示例模块**：ESP8266、ESP32

### 2. Bluetooth
- **特点**：低功耗、短距离、易于配对
- **版本**：BLE (Bluetooth Low Energy)、经典蓝牙
- **应用场景**：可穿戴设备、智能家居

### 3. Zigbee
- **特点**：低功耗、自组网、可靠性高
- **应用场景**：物联网、工业控制

### 4. LoRa
- **特点**：低功耗、远距离、抗干扰能力强
- **应用场景**：远程监控、物联网

## 通信协议选择指南

| 协议 | 传输距离 | 速率 | 抗干扰能力 | 功耗 | 适用场景 |
|------|----------|------|------------|------|----------|
| UART | 短距离 | 低-中 | 中 | 低 | 点对点通信 |
| I2C | 短距离 | 低 | 中 | 低 | 板上设备通信 |
| SPI | 短距离 | 高 | 高 | 中 | 高速设备通信 |
| CAN | 中距离 | 中 | 高 | 中 | 汽车、工业控制 |
| 以太网 | 长距离 | 高 | 高 | 高 | 高速数据传输 |
| Wi-Fi | 中距离 | 高 | 中 | 高 | 互联网接入 |
| Bluetooth | 短距离 | 中 | 中 | 低 | 个人设备互联 |
| Zigbee | 中距离 | 低 | 高 | 低 | 物联网 |
| LoRa | 长距离 | 低 | 高 | 低 | 远程监控 |

## 常见问题与解决方案

### 1. 通信数据错误
- **症状**：接收到的数据与发送的数据不一致
- **解决方案**：检查波特率/时钟频率、检查连线、检查接地

### 2. 通信超时
- **症状**：设备无法建立通信连接
- **解决方案**：检查设备地址、检查硬件连接、检查电源

### 3. 通信干扰
- **症状**：通信不稳定，偶尔出现错误
- **解决方案**：使用屏蔽线缆、增加滤波电容、优化接地

### 4. 总线竞争
- **症状**：多主机通信时出现冲突
- **解决方案**：使用总线仲裁机制、合理设计通信协议

## 示例项目

### 1. 多传感器数据采集系统

**功能说明**：使用I2C和SPI接口采集多种传感器数据，并通过串口发送到上位机。

**硬件需求**：
- 微控制器开发板
- I2C温湿度传感器（如DHT11）
- SPI加速度传感器（如ADXL345）
- 串口模块

**软件设计**：
- 初始化I2C和SPI接口
- 定期采集传感器数据
- 通过串口发送数据

**实现代码**：

```c
#include "gd32f4xx.h"

// 主函数
int main(void)
{
    // 系统初始化
    SystemInit();
    
    // 初始化串口
    UART_Init();
    
    // 初始化I2C
    I2C_Init();
    
    // 初始化SPI
    SPI_Init();
    
    while(1) {
        // 从I2C传感器读取温湿度
        uint16_t temperature = I2C_Read_Temperature();
        uint16_t humidity = I2C_Read_Humidity();
        
        // 从SPI传感器读取加速度
        int16_t x = SPI_Read_AccelX();
        int16_t y = SPI_Read_AccelY();
        int16_t z = SPI_Read_AccelZ();
        
        // 通过串口发送数据
        char buffer[100];
        sprintf(buffer, "Temp: %d.%dC, Humidity: %d.%d%%, Accel: %d, %d, %d\r\n", 
                temperature / 10, temperature % 10, 
                humidity / 10, humidity % 10, 
                x, y, z);
        UART_SendString(buffer);
        
        // 延时
        delay_ms(1000);
    }
}
```

### 2. 基于CAN总线的多节点控制系统

**功能说明**：使用CAN总线实现多个节点之间的通信，控制LED和读取传感器数据。

**硬件需求**：
- 多个CAN节点（微控制器开发板）
- CAN收发器
- LED和传感器

**软件设计**：
- 初始化CAN总线
- 发送控制命令
- 接收传感器数据

**实现代码**：

```c
// 节点1（发送控制命令）
#include "gd32f4xx.h"

int main(void)
{
    // 系统初始化
    SystemInit();
    
    // 初始化CAN
    CAN_Init();
    
    // 初始化LED
    LED_Init();
    
    uint8_t data[2] = {0, 0};
    uint32_t count = 0;
    
    while(1) {
        // 每1秒发送一次控制命令
        data[0] = count % 256;
        data[1] = (count / 256) % 256;
        CAN_SendMessage(0x100, data, 2);
        
        // 翻转LED
        LED_Toggle();
        
        count++;
        delay_ms(1000);
    }
}

// 节点2（接收控制命令并发送传感器数据）
#include "gd32f4xx.h"

int main(void)
{
    // 系统初始化
    SystemInit();
    
    // 初始化CAN
    CAN_Init();
    
    // 初始化传感器
    Sensor_Init();
    
    uint32_t id;
    uint8_t data[8];
    uint8_t length;
    
    while(1) {
        // 接收CAN消息
        if(CAN_ReceiveMessage(&id, data, &length) == SUCCESS) {
            // 处理控制命令
            if(id == 0x100) {
                // 执行控制操作
                Process_Control_Command(data, length);
            }
        }
        
        // 每500ms发送一次传感器数据
        static uint32_t last_time = 0;
        if(Get_Tick() - last_time > 500) {
            last_time = Get_Tick();
            
            // 读取传感器数据
            uint16_t sensor_data = Read_Sensor();
            
            // 发送传感器数据
            uint8_t sensor_buf[2] = {sensor_data & 0xFF, (sensor_data >> 8) & 0xFF};
            CAN_SendMessage(0x200, sensor_buf, 2);
        }
    }
}
```

## 总结

通信协议是嵌入式系统中重要的组成部分，选择合适的通信协议对于系统的性能和可靠性至关重要。本文档介绍了常见的通信协议实现方法，包括串口通信、I2C、SPI、CAN、以太网等，以及它们在不同系列微控制器上的应用。

通过本章节的学习，您应该能够：
1. 了解常见通信协议的基本原理和特点
2. 在不同系列微控制器上实现各种通信协议
3. 根据应用需求选择合适的通信协议
4. 解决通信过程中遇到的常见问题
5. 设计基于通信协议的嵌入式系统应用