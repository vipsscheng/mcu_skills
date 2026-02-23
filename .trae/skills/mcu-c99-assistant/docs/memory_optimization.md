# 内存使用优化

## 1. 内存使用分析工具

### 1.1 编译器内置工具

#### GCC
```bash
# 生成内存使用报告
arm-none-eabi-size your_program.elf

# 生成详细的内存映射文件
arm-none-eabi-nm --size-sort -t d your_program.elf

# 使用objdump查看内存布局
arm-none-eabi-objdump -t your_program.elf
```

#### Keil MDK
```
# 使用 scatter file 控制内存分配
# 在项目选项中查看内存使用情况
# 使用 RTX 内存调试工具
```

#### IAR Embedded Workbench
```
# 使用 Memory window 查看内存使用
# 生成内存使用报告
# 使用 C-SPY 调试器分析内存
```

### 1.2 第三方工具

#### Valgrind (适用于支持的平台)
```bash
valgrind --tool=memcheck --leak-check=full ./your_program
```

#### 自定义内存跟踪工具
```c
// 简单的内存跟踪实现
#define MEMORY_TRACE_ENABLE 1

#if MEMORY_TRACE_ENABLE
#define MALLOC(size) custom_malloc(size, __FILE__, __LINE__)
#define FREE(ptr) custom_free(ptr, __FILE__, __LINE__)

void* custom_malloc(size_t size, const char* file, int line) {
    void* ptr = malloc(size);
    printf("Malloc %zu bytes at %p from %s:%d\n", size, ptr, file, line);
    return ptr;
}

void custom_free(void* ptr, const char* file, int line) {
    printf("Free at %p from %s:%d\n", ptr, file, line);
    free(ptr);
}
#endif
```

## 2. 内存管理策略

### 2.1 静态内存分配

#### 优势
- 编译时确定内存大小
- 无运行时开销
- 避免内存碎片

#### 示例
```c
// 静态数组
static uint8_t buffer[1024];

// 静态结构体
static struct {
    uint16_t data;
    uint8_t flag;
} sensor_data;
```

### 2.2 动态内存分配

#### 注意事项
- 避免频繁分配和释放
- 设置内存分配失败处理
- 监控内存使用情况

#### 示例
```c
// 安全的动态内存分配
void* safe_malloc(size_t size) {
    void* ptr = malloc(size);
    if (ptr == NULL) {
        // 内存分配失败处理
        error_handler(ERROR_MEMORY_ALLOCATION);
    }
    return ptr;
}

// 内存池实现
#define MEM_POOL_SIZE 4096
#define BLOCK_SIZE 32

static uint8_t memory_pool[MEM_POOL_SIZE];
static uint8_t memory_map[MEM_POOL_SIZE / BLOCK_SIZE];

void* pool_malloc(size_t size) {
    // 简单的内存池分配实现
    // ...
}

void pool_free(void* ptr) {
    // 内存池释放实现
    // ...
}
```

## 3. 不同微控制器系列的内存优化

### 3.1 STC 系列

#### 内存特点
- 内部RAM较小（通常为128B-1024B）
- 无外部RAM扩展能力
- 代码存储在Flash中

#### 优化策略
```c
// 使用xdata存储大数组（STC12系列及以上）
__xdata uint8_t large_buffer[1024];

// 常量数据存储在code区
__code const uint8_t lookup_table[] = {
    0x00, 0x01, 0x02, 0x03
};

// 位操作节省内存
__bit flag;

// 结构体优化
struct {
    uint8_t state : 2;
    uint8_t error : 1;
    uint8_t reserved : 5;
} status;
```

### 3.2 GD32 系列

#### 内存特点
- 内部RAM较大（8KB-256KB）
- 支持外部RAM扩展
- 具有多种内存区域（SRAM、CCM等）

#### 优化策略
```c
// 使用DMA减少CPU内存访问
#define BUFFER_SIZE 1024
uint8_t dma_buffer[BUFFER_SIZE] __attribute__((section(".sram1")));

// 放置常量到FLASH
const uint8_t large_lookup_table[] __attribute__((section(".rodata"))) = {
    // 大量常量数据
};

// 使用内存对齐
uint32_t aligned_buffer[256] __attribute__((aligned(4)));

// 堆大小配置（在链接脚本中）
// HEAP_SIZE = 0x1000; // 4KB堆
```

### 3.3 HC32 系列

#### 内存特点
- 内部RAM大小适中（8KB-128KB）
- 支持内存保护单元(MPU)
- 具有多种内存访问模式

#### 优化策略
```c
// 使用MPU保护关键内存区域
void mpu_config(void) {
    // 配置MPU保护代码和数据区域
    // ...
}

// 零拷贝技术
void zero_copy_transfer(void) {
    // 直接操作硬件缓冲区
    // ...
}

// 内存分配对齐
#define ALIGNMENT 4
void* aligned_malloc(size_t size) {
    void* ptr = malloc(size + ALIGNMENT - 1);
    return (void*)(((uintptr_t)ptr + ALIGNMENT - 1) & ~(ALIGNMENT - 1));
}
```

### 3.4 MM32 系列

#### 内存特点
- 内部RAM大小（4KB-128KB）
- 支持多种低功耗模式下的内存保持
- 具有特殊功能寄存器(SFR)区域

#### 优化策略
```c
// 低功耗模式下的内存管理
void low_power_memory_config(void) {
    // 配置需要在低功耗模式下保持的内存区域
    // ...
}

// 使用分散加载文件控制内存分配
// scatter.sct 文件示例
/*
LR_IROM1 0x08000000 0x00100000 {
    ER_IROM1 0x08000000 0x00100000 {
        *.o (RESET, +First)
        *(InRoot$$Sections)
        .ANY (+RO)
        .ANY (+XO)
    }
    
    RW_IRAM1 0x20000000 0x00020000 {
        .ANY (+RW +ZI)
    }
}
*/
```

## 4. 内存使用优化技巧

### 4.1 数据类型优化

#### 选择合适的数据类型
```c
// 避免使用过大的数据类型
// 不好的做法
uint32_t counter; // 只需要计数到255

// 好的做法
uint8_t counter; // 足够存储0-255

// 使用位域节省内存
typedef struct {
    uint8_t flag1 : 1;
    uint8_t flag2 : 1;
    uint8_t mode : 2;
    uint8_t status : 4;
} ControlFlags; // 总共只占1字节
```

### 4.2 字符串优化

#### 字符串存储
```c
// 不好的做法
char message[] = "Hello, World!";

// 好的做法（存储在ROM中）
const char message[] = "Hello, World!";

// 字符串常量池
#define MSG_ERROR "Error"
#define MSG_SUCCESS "Success"
```

#### 字符串处理
```c
// 使用静态缓冲区
#define MAX_STRING_LENGTH 64
static char buffer[MAX_STRING_LENGTH];

// 避免动态字符串操作
int string_copy(char* dest, const char* src, size_t max_len) {
    // 安全的字符串复制
    size_t i;
    for (i = 0; i < max_len - 1 && src[i]; i++) {
        dest[i] = src[i];
    }
    dest[i] = '\0';
    return i;
}
```

### 4.3 数组和缓冲区优化

#### 缓冲区大小估算
```c
// 根据实际需求设置缓冲区大小
#define UART_BUFFER_SIZE 64 // 足够处理典型的UART数据

// 环形缓冲区实现
typedef struct {
    uint8_t buffer[UART_BUFFER_SIZE];
    uint8_t head;
    uint8_t tail;
} RingBuffer;

// 缓冲区管理
void ring_buffer_init(RingBuffer* rb) {
    rb->head = 0;
    rb->tail = 0;
}

int ring_buffer_push(RingBuffer* rb, uint8_t data) {
    uint8_t next = (rb->head + 1) % UART_BUFFER_SIZE;
    if (next != rb->tail) {
        rb->buffer[rb->head] = data;
        rb->head = next;
        return 1;
    }
    return 0; // 缓冲区满
}
```

### 4.4 函数优化

#### 减少栈使用
```c
// 不好的做法
void process_data(void) {
    uint8_t large_buffer[1024]; // 占用大量栈空间
    // ...
}

// 好的做法
static uint8_t large_buffer[1024]; // 使用静态存储
void process_data(void) {
    // 使用large_buffer
    // ...
}
```

#### 函数参数传递
```c
// 不好的做法（传递大结构体）
void process_struct(struct BigStruct s) {
    // ...
}

// 好的做法（传递指针）
void process_struct(const struct BigStruct* s) {
    // ...
}
```

## 5. 内存碎片管理

### 5.1 内存碎片产生原因
- 频繁的内存分配和释放
- 分配不同大小的内存块
- 长时间运行的系统

### 5.2 内存碎片解决方案

#### 内存池
```c
// 固定大小内存池
#define BLOCK_SIZES 5
#define BLOCK_SIZE_0 16
#define BLOCK_SIZE_1 32
#define BLOCK_SIZE_2 64
#define BLOCK_SIZE_3 128
#define BLOCK_SIZE_4 256

static uint8_t pool_0[10 * BLOCK_SIZE_0];
static uint8_t pool_1[10 * BLOCK_SIZE_1];
static uint8_t pool_2[5 * BLOCK_SIZE_2];
static uint8_t pool_3[3 * BLOCK_SIZE_3];
static uint8_t pool_4[2 * BLOCK_SIZE_4];

static uint8_t pool_0_used[10];
static uint8_t pool_1_used[10];
static uint8_t pool_2_used[5];
static uint8_t pool_3_used[3];
static uint8_t pool_4_used[2];

void* pool_alloc(size_t size) {
    // 根据大小选择合适的内存池
    if (size <= BLOCK_SIZE_0) {
        // 从pool_0分配
    } else if (size <= BLOCK_SIZE_1) {
        // 从pool_1分配
    }
    // ...
}
```

#### 内存分配策略
```c
// 首次适应算法
void* first_fit_alloc(size_t size) {
    // 查找第一个足够大的空闲块
    // ...
}

// 最佳适应算法
void* best_fit_alloc(size_t size) {
    // 查找大小最接近的空闲块
    // ...
}
```

## 6. 内存使用监控

### 6.1 运行时内存监控

#### 堆使用监控
```c
// 堆使用统计
typedef struct {
    size_t total_heap;
    size_t used_heap;
    size_t free_heap;
    size_t max_used_heap;
} HeapStats;

HeapStats heap_stats;

void update_heap_stats(void) {
    // 更新堆使用统计
    // ...
}

void print_heap_stats(void) {
    printf("Heap: Total=%zu, Used=%zu, Free=%zu, MaxUsed=%zu\n",
           heap_stats.total_heap,
           heap_stats.used_heap,
           heap_stats.free_heap,
           heap_stats.max_used_heap);
}
```

#### 栈使用监控
```c
// 栈使用监控
#define STACK_SIZE 1024
static uint8_t stack[STACK_SIZE];
static uint32_t stack_watermark;

void init_stack_monitor(void) {
    // 初始化栈监控
    memset(stack, 0xAA, STACK_SIZE);
    stack_watermark = STACK_SIZE;
}

void check_stack_usage(void) {
    // 检查栈使用情况
    uint32_t i;
    for (i = 0; i < STACK_SIZE; i++) {
        if (stack[i] != 0xAA) {
            break;
        }
    }
    stack_watermark = i;
    printf("Stack usage: %lu bytes\n", STACK_SIZE - stack_watermark);
}
```

### 6.2 内存使用分析工具

#### 编译时分析
```bash
# 使用size工具分析
arm-none-eabi-size your_program.elf

# 输出示例
#   text    data     bss     dec     hex filename
#  12345     678    9012   22035    5613 your_program.elf
```

#### 运行时分析
```c
// 内存使用报告
void generate_memory_report(void) {
    // 生成内存使用报告
    printf("=== Memory Usage Report ===\n");
    print_heap_stats();
    check_stack_usage();
    // 其他内存使用信息
    printf("=========================\n");
}
```

## 7. 内存优化最佳实践

### 7.1 代码层面优化

1. **使用适当的数据类型**
   - 选择最小足够的数据类型
   - 使用位域存储多个布尔值
   - 避免使用浮点数（如无必要）

2. **合理使用内存区域**
   - 将常量存储在ROM中
   - 将频繁访问的数据放在快速RAM中
   - 使用分散加载文件优化内存布局

3. **优化字符串处理**
   - 使用静态字符串
   - 避免动态字符串操作
   - 使用字符串常量池

4. **优化数组和缓冲区**
   - 合理设置缓冲区大小
   - 使用环形缓冲区
   - 避免过大的局部数组

5. **函数优化**
   - 减少函数参数传递
   - 避免递归（如无必要）
   - 使用内联函数减少函数调用开销

### 7.2 系统层面优化

1. **内存分配策略**
   - 使用静态内存分配
   - 实现内存池管理
   - 避免频繁的动态内存分配

2. **内存碎片管理**
   - 使用固定大小的内存块
   - 实现内存分配算法
   - 定期整理内存碎片

3. **内存监控**
   - 实现运行时内存监控
   - 定期生成内存使用报告
   - 设置内存使用阈值告警

4. **链接器优化**
   - 使用链接脚本控制内存布局
   - 启用链接时优化(LTO)
   - 移除未使用的代码和数据

## 8. 应用示例

### 8.1 低内存系统优化

#### STC89C52 内存优化示例
```c
// 内存优化配置
#define SMALL_MEMORY_SYSTEM 1

#if SMALL_MEMORY_SYSTEM
// 使用xdata存储大数组
__xdata uint8_t uart_buffer[128];

// 位操作
__bit uart_rx_flag;
__bit uart_tx_flag;

// 紧凑结构体
typedef struct {
    uint8_t state : 2;
    uint8_t error : 1;
    uint8_t reserved : 5;
} SystemStatus;

// 常量存储在code区
__code const uint8_t lookup_table[] = {
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05
};

// 函数优化
void process_data(void) {
    static uint8_t local_buffer[64]; // 使用静态存储
    // 处理数据
}
#endif
```

### 8.2 中等内存系统优化

#### GD32F450 内存优化示例
```c
// 内存区域配置
#define SRAM1_BASE 0x20000000
#define SRAM1_SIZE 0x00040000 // 256KB

// 放置关键数据到快速RAM
uint8_t dma_buffer[1024] __attribute__((section(".sram1")));

// 内存池实现
#define MEM_POOL_SIZE 16384
static uint8_t memory_pool[MEM_POOL_SIZE];
static uint32_t pool_free_index = 0;

void* pool_alloc(size_t size) {
    if (pool_free_index + size <= MEM_POOL_SIZE) {
        void* ptr = &memory_pool[pool_free_index];
        pool_free_index += size;
        return ptr;
    }
    return NULL;
}

// 内存使用监控
void monitor_memory_usage(void) {
    static size_t max_heap_usage = 0;
    size_t current_heap_usage = pool_free_index;
    
    if (current_heap_usage > max_heap_usage) {
        max_heap_usage = current_heap_usage;
    }
    
    printf("Memory usage: %zu/%zu bytes (max: %zu)\n", 
           current_heap_usage, MEM_POOL_SIZE, max_heap_usage);
}
```

### 8.3 内存分配失败处理

#### 安全的内存分配示例
```c
// 内存分配失败处理
void* safe_malloc(size_t size) {
    void* ptr = malloc(size);
    if (ptr == NULL) {
        // 内存分配失败处理
        printf("Memory allocation failed for size %zu\n", size);
        
        // 尝试释放不必要的内存
        free_unused_resources();
        
        // 再次尝试分配
        ptr = malloc(size);
        if (ptr == NULL) {
            // 仍然失败，执行错误处理
            error_handler(ERROR_OUT_OF_MEMORY);
        }
    }
    return ptr;
}

// 释放不必要的资源
void free_unused_resources(void) {
    // 释放临时缓冲区
    // 清理缓存
    // 其他资源释放
}
```

## 9. 内存优化检查清单

### 9.1 代码检查
- [ ] 使用了适当的数据类型
- [ ] 常量存储在ROM中
- [ ] 避免了过大的局部变量
- [ ] 函数参数传递优化
- [ ] 字符串处理优化

### 9.2 内存分配检查
- [ ] 使用静态内存分配
- [ ] 实现了内存池管理
- [ ] 避免频繁的动态内存分配
- [ ] 内存分配失败处理
- [ ] 内存碎片管理

### 9.3 内存监控检查
- [ ] 实现了运行时内存监控
- [ ] 定期生成内存使用报告
- [ ] 设置了内存使用阈值告警
- [ ] 分析了内存使用热点

### 9.4 系统配置检查
- [ ] 链接脚本优化
- [ ] 内存布局合理
- [ ] 启用了链接时优化
- [ ] 移除了未使用的代码和数据

## 10. 总结

内存使用优化是嵌入式系统开发中的重要环节，特别是对于资源受限的微控制器。通过合理的内存管理策略、优化的代码设计和有效的监控工具，可以显著提高系统的稳定性和性能。

关键优化策略包括：

1. **选择合适的数据类型**：使用最小足够的数据类型，减少内存占用。
2. **合理使用内存区域**：将数据放在适当的内存区域，提高访问效率。
3. **优化内存分配**：优先使用静态内存分配，实现内存池管理。
4. **监控内存使用**：定期检查内存使用情况，及时发现问题。
5. **系统级优化**：通过链接脚本和编译选项优化内存布局。

通过综合应用这些优化策略，可以在有限的内存资源下实现更复杂的功能，提高系统的可靠性和性能。