# 性能优化

## 文件大小优化

### 文档优化

#### 模块化拆分

- **拆分大型文档**：将大型文档拆分为多个小型模块文件
- **移除重复内容**：删除文档中的重复内容
- **优化图片资源**：压缩图片大小，使用适当的格式
- **减少空白字符**：移除多余的空白字符和空行

#### 文件格式优化

- **使用Markdown**：使用轻量级的Markdown格式
- **避免嵌套层级**：减少Markdown的嵌套层级
- **使用相对路径**：使用相对路径引用文件
- **压缩JSON文件**：移除JSON文件中的注释和多余空白

### 代码优化

#### 代码压缩

- **移除注释**：生产环境中移除不必要的注释
- **变量名简化**：使用简短的变量名
- **代码合并**：合并相关的代码文件
- **死代码移除**：移除未使用的代码

#### 资源优化

- **按需加载**：实现代码的按需加载
- **资源压缩**：压缩JavaScript和CSS文件
- **缓存策略**：实现合理的缓存策略

## 加载速度优化

### 技能加载优化

#### 并行加载

- **并行扫描**：并行扫描技能目录
- **异步解析**：异步解析技能元数据
- **延迟加载**：实现技能的延迟加载

#### 缓存机制

- **技能缓存**：缓存已加载的技能信息
- **元数据缓存**：缓存技能元数据
- **关键词缓存**：缓存关键词索引

### 关键词匹配优化

#### 索引优化

- **关键词索引**：创建关键词索引
- **前缀树**：使用前缀树存储关键词
- **哈希表**：使用哈希表快速查找关键词

#### 匹配算法

- **精确匹配**：优先进行精确匹配
- **前缀匹配**：支持前缀匹配
- **模糊匹配**：使用编辑距离进行模糊匹配
- **权重计算**：根据匹配程度计算权重

## 关键词优先级实现

### 优先级定义

#### 优先级等级

| 优先级 | 等级 | 权重 | 描述 |
|--------|------|------|------|
| 高 | 5 | 1.0 | 核心关键词，直接触发 |
| 中高 | 4 | 0.8 | 重要关键词，高概率触发 |
| 中 | 3 | 0.6 | 普通关键词，中等概率触发 |
| 中低 | 2 | 0.4 | 次要关键词，低概率触发 |
| 低 | 1 | 0.2 | 辅助关键词，仅辅助触发 |

#### 优先级配置

```json
{
  "keywords": [
    {
      "word": "单片机",
      "priority": 5,
      "category": "core"
    },
    {
      "word": "MCU",
      "priority": 5,
      "category": "core"
    },
    {
      "word": "嵌入式",
      "priority": 4,
      "category": "important"
    },
    {
      "word": "编程",
      "priority": 4,
      "category": "important"
    },
    {
      "word": "代码",
      "priority": 3,
      "category": "normal"
    }
  ]
}
```

### 优先级算法

#### 权重计算

```python
def calculate_weight(keyword, context):
    """计算关键词权重"""
    # 基础权重
    base_weight = get_priority_weight(keyword)
    
    # 上下文权重
    context_weight = calculate_context_weight(keyword, context)
    
    # 位置权重
    position_weight = calculate_position_weight(keyword, context)
    
    # 频率权重
    frequency_weight = calculate_frequency_weight(keyword, context)
    
    # 最终权重
    total_weight = base_weight * context_weight * position_weight * frequency_weight
    
    return total_weight

def get_priority_weight(keyword):
    """获取关键词基础权重"""
    priority_map = {
        "单片机": 1.0,
        "MCU": 1.0,
        "嵌入式": 0.8,
        "编程": 0.8,
        "代码": 0.6,
        # 更多关键词...
    }
    
    return priority_map.get(keyword, 0.4)

def calculate_context_weight(keyword, context):
    """计算上下文权重"""
    # 根据上下文相关性计算权重
    # 例如，在"单片机编程"中，"编程"的权重会更高
    context_terms = context.split()
    related_terms = ["单片机", "MCU", "嵌入式", "芯片", "硬件"]
    
    related_count = sum(1 for term in context_terms if term in related_terms)
    
    if related_count > 0:
        return 1.0 + (related_count * 0.2)
    else:
        return 0.8

def calculate_position_weight(keyword, context):
    """计算位置权重"""
    # 关键词在句子中的位置越靠前，权重越高
    position = context.find(keyword)
    if position == 0:
        return 1.2
    elif position < 10:
        return 1.1
    elif position < 50:
        return 1.0
    else:
        return 0.9

def calculate_frequency_weight(keyword, context):
    """计算频率权重"""
    # 关键词出现频率越高，权重越高
    frequency = context.count(keyword)
    if frequency >= 3:
        return 1.3
    elif frequency == 2:
        return 1.1
    else:
        return 1.0
```

#### 触发阈值

```python
def should_trigger(skill, context):
    """判断是否应该触发技能"""
    # 计算总权重
    total_weight = 0
    matched_keywords = []
    
    for keyword in skill.keywords:
        if keyword in context:
            weight = calculate_weight(keyword, context)
            total_weight += weight
            matched_keywords.append((keyword, weight))
    
    # 设置触发阈值
    threshold = 1.5
    
    # 检查是否达到阈值
    if total_weight >= threshold:
        # 排序匹配的关键词
        matched_keywords.sort(key=lambda x: x[1], reverse=True)
        
        # 记录匹配信息
        skill.last_match = {
            "weight": total_weight,
            "keywords": matched_keywords,
            "context": context,
            "timestamp": time.time()
        }
        
        return True
    else:
        return False
```

## 性能测试

### 加载性能测试

#### 测试方法

1. **准备测试环境**：设置不同大小的技能集合
2. **测量加载时间**：记录技能加载的时间
3. **分析内存使用**：测量技能加载的内存使用
4. **重复测试**：多次测试取平均值

#### 测试脚本

```python
def test_load_performance(skill_dirs):
    """测试技能加载性能"""
    import time
    import psutil
    import os
    
    # 记录开始时间和内存使用
    start_time = time.time()
    start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    
    # 加载技能
    skills = []
    for skill_dir in skill_dirs:
        skill = load_skill(skill_dir)
        skills.append(skill)
    
    # 记录结束时间和内存使用
    end_time = time.time()
    end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    
    # 计算结果
    load_time = end_time - start_time
    memory_used = end_memory - start_memory
    
    print(f"加载 {len(skills)} 个技能:")
    print(f"加载时间: {load_time:.2f} 秒")
    print(f"内存使用: {memory_used:.2f} MB")
    print(f"平均加载时间: {load_time / len(skills):.4f} 秒/技能")
    print(f"平均内存使用: {memory_used / len(skills):.4f} MB/技能")
    
    return load_time, memory_used
```

### 匹配性能测试

#### 测试方法

1. **准备测试数据**：准备不同长度和复杂度的测试文本
2. **测量匹配时间**：记录关键词匹配的时间
3. **分析准确率**：分析匹配的准确率
4. **重复测试**：多次测试取平均值

#### 测试脚本

```python
def test_match_performance(skill, test_texts):
    """测试关键词匹配性能"""
    import time
    
    # 记录开始时间
    start_time = time.time()
    
    # 执行匹配
    matches = []
    for text in test_texts:
        result = should_trigger(skill, text)
        matches.append(result)
    
    # 记录结束时间
    end_time = time.time()
    
    # 计算结果
    match_time = end_time - start_time
    match_count = sum(matches)
    
    print(f"测试 {len(test_texts)} 条文本:")
    print(f"匹配时间: {match_time:.4f} 秒")
    print(f"匹配率: {match_count / len(test_texts):.2f}")
    print(f"平均匹配时间: {match_time / len(test_texts):.6f} 秒/文本")
    
    return match_time, match_count / len(test_texts)
```

## 优化策略

### 缓存策略

#### 内存缓存

- **技能缓存**：缓存已加载的技能对象
- **关键词缓存**：缓存关键词索引
- **匹配结果缓存**：缓存近期的匹配结果

#### 磁盘缓存

- **技能元数据缓存**：缓存技能元数据到磁盘
- **关键词索引缓存**：缓存关键词索引到磁盘
- **配置缓存**：缓存配置信息到磁盘

### 并行处理

#### 多线程加载

- **技能扫描**：使用多线程扫描技能目录
- **元数据解析**：使用多线程解析技能元数据
- **关键词索引**：使用多线程构建关键词索引

#### 异步处理

- **异步加载**：使用异步IO加载技能
- **异步解析**：使用异步IO解析元数据
- **异步匹配**：使用异步IO进行关键词匹配

### 算法优化

#### 关键词匹配算法

- **前缀树**：使用前缀树存储关键词
- **布隆过滤器**：使用布隆过滤器快速判断关键词是否存在
- **Aho-Corasick算法**：使用Aho-Corasick算法进行多模式匹配

#### 权重计算优化

- **预计算权重**：预计算关键词的基础权重
- **缓存计算结果**：缓存权重计算结果
- **并行计算**：使用并行计算计算权重

## 最佳实践

1. **文件模块化**：将大型文件拆分为多个小型模块
2. **缓存机制**：实现合理的缓存策略
3. **并行处理**：使用多线程和异步处理提高性能
4. **算法优化**：选择合适的算法提高匹配速度
5. **资源管理**：合理管理内存和磁盘资源
6. **性能测试**：定期进行性能测试和优化
7. **按需加载**：实现技能的按需加载
8. **延迟初始化**：实现组件的延迟初始化
9. **压缩资源**：压缩文档和代码资源
10. **监控性能**：监控技能的加载和匹配性能

## 性能优化示例

### 示例1：关键词索引优化

```python
class KeywordIndex:
    """关键词索引类"""
    def __init__(self):
        self.trie = {}
        self.keywords = []
    
    def add_keyword(self, keyword, priority=3):
        """添加关键词"""
        self.keywords.append((keyword, priority))
        
        # 构建前缀树
        node = self.trie
        for char in keyword:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['_end'] = True
        node['_priority'] = priority
    
    def search(self, text):
        """搜索文本中的关键词"""
        matches = []
        
        for i in range(len(text)):
            node = self.trie
            j = i
            
            while j < len(text) and text[j] in node:
                node = node[text[j]]
                j += 1
                
                if '_end' in node:
                    keyword = text[i:j]
                    priority = node['_priority']
                    matches.append((keyword, priority, i))
        
        return matches
    
    def get_matches(self, text):
        """获取匹配的关键词及其权重"""
        matches = self.search(text)
        
        # 去重并计算权重
        unique_matches = {}
        for keyword, priority, position in matches:
            if keyword not in unique_matches or position < unique_matches[keyword][1]:
                # 计算权重
                weight = self.calculate_weight(keyword, priority, position, text)
                unique_matches[keyword] = (weight, position)
        
        # 按权重排序
        sorted_matches = sorted(unique_matches.items(), key=lambda x: x[1][0], reverse=True)
        
        return [(keyword, weight) for keyword, (weight, _) in sorted_matches]
    
    def calculate_weight(self, keyword, priority, position, text):
        """计算关键词权重"""
        # 基础权重
        base_weight = priority / 5.0
        
        # 位置权重
        position_weight = 1.0 - (position / len(text)) * 0.3
        
        # 长度权重
        length_weight = min(1.0, len(keyword) / 10.0 * 0.2 + 0.8)
        
        # 频率权重
        frequency = text.count(keyword)
        frequency_weight = 1.0 + (frequency - 1) * 0.1
        
        # 最终权重
        total_weight = base_weight * position_weight * length_weight * frequency_weight
        
        return total_weight
```

### 示例2：技能加载优化

```python
class SkillLoader:
    """技能加载器"""
    def __init__(self):
        self.skills = {}
        self.keyword_index = KeywordIndex()
        self.cache_file = ".skill_cache.json"
        
        # 尝试加载缓存
        self.load_cache()
    
    def load_skills(self, skill_dirs):
        """加载技能"""
        import concurrent.futures
        
        # 使用线程池并行加载技能
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_skill = {
                executor.submit(self.load_skill, skill_dir): skill_dir
                for skill_dir in skill_dirs
            }
            
            for future in concurrent.futures.as_completed(future_to_skill):
                skill = future.result()
                if skill:
                    self.skills[skill.slug] = skill
                    
                    # 添加关键词到索引
                    for keyword in skill.keywords:
                        self.keyword_index.add_keyword(keyword)
        
        # 保存缓存
        self.save_cache()
    
    def load_skill(self, skill_dir):
        """加载单个技能"""
        try:
            # 加载技能元数据
            meta_path = os.path.join(skill_dir, "_meta.json")
            if not os.path.exists(meta_path):
                return None
            
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            
            # 创建技能对象
            skill = Skill(
                slug=meta.get("slug"),
                name=meta.get("name"),
                version=meta.get("version"),
                keywords=meta.get("keywords", [])
            )
            
            return skill
        except Exception as e:
            print(f"加载技能失败 {skill_dir}: {e}")
            return None
    
    def save_cache(self):
        """保存缓存"""
        try:
            cache_data = {
                "skills": {
                    slug: {
                        "name": skill.name,
                        "version": skill.version,
                        "keywords": skill.keywords
                    }
                    for slug, skill in self.skills.items()
                },
                "timestamp": time.time()
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print(f"保存缓存失败: {e}")
    
    def load_cache(self):
        """加载缓存"""
        try:
            if not os.path.exists(self.cache_file):
                return
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # 检查缓存是否过期（24小时）
            if time.time() - cache_data.get("timestamp", 0) > 24 * 3600:
                return
            
            # 加载技能
            for slug, data in cache_data.get("skills", {}).items():
                skill = Skill(
                    slug=slug,
                    name=data.get("name"),
                    version=data.get("version"),
                    keywords=data.get("keywords", [])
                )
                self.skills[slug] = skill
                
                # 添加关键词到索引
                for keyword in skill.keywords:
                    self.keyword_index.add_keyword(keyword)
        except Exception as e:
            print(f"加载缓存失败: {e}")
    
    def match_skills(self, text):
        """匹配技能"""
        # 搜索关键词
        matches = self.keyword_index.get_matches(text)
        
        # 计算技能匹配度
        skill_scores = {}
        for skill_slug, skill in self.skills.items():
            score = 0
            for keyword, weight in matches:
                if keyword in skill.keywords:
                    score += weight
            
            if score > 0:
                skill_scores[skill_slug] = score
        
        # 按得分排序
        sorted_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_skills
```

## 性能监控

### 监控指标

- **加载时间**：技能加载的时间
- **内存使用**：技能加载的内存使用
- **匹配时间**：关键词匹配的时间
- **匹配准确率**：关键词匹配的准确率
- **触发率**：技能的触发率

### 监控工具

- **日志记录**：记录性能指标到日志文件
- **性能分析**：使用性能分析工具分析瓶颈
- **实时监控**：实时监控技能的性能

### 优化建议

1. **定期分析**：定期分析性能数据，找出瓶颈
2. **针对性优化**：根据性能数据进行针对性优化
3. **持续改进**：持续改进性能优化策略
4. **测试验证**：通过测试验证优化效果
5. **文档更新**：及时更新性能优化文档