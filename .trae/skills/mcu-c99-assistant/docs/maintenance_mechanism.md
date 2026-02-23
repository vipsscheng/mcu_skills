# 维护机制

## 版本控制

### Git版本控制

#### 初始化仓库

1. **创建Git仓库**：在技能目录中初始化Git仓库
   ```bash
   cd "E:\Desktop\znt\.trae\skills\mcu-c99-assistant"
   git init
   git add .
   git commit -m "初始化技能仓库"
   ```

2. **配置远程仓库**：连接到GitHub或其他Git托管服务
   ```bash
   git remote add origin https://github.com/username/mcu-c99-assistant.git
   git push -u origin master
   ```

3. **分支管理**：建立合理的分支结构
   - `master`：稳定版本
   - `develop`：开发版本
   - `feature/*`：功能分支
   - `bugfix/*`：bug修复分支

### 版本号规范

#### 语义化版本号

采用语义化版本号格式：`MAJOR.MINOR.PATCH`

- **MAJOR**：不兼容的API变更
- **MINOR**：向后兼容的功能添加
- **PATCH**：向后兼容的bug修复

#### 版本号管理

1. **版本号更新**：在`_meta.json`中更新版本号
   ```json
   {
     "version": "1.0.1",
     "publishedAt": 1700000000000
   }
   ```

2. **版本标签**：使用Git标签标记版本
   ```bash
   git tag -a v1.0.1 -m "版本 1.0.1"
   git push --tags
   ```

3. **版本日志**：维护版本变更日志
   - 创建`CHANGELOG.md`文件
   - 记录每个版本的变更内容

### 配置文件管理

#### 配置文件版本控制

- **跟踪配置文件**：将配置文件纳入版本控制
- **忽略敏感信息**：使用`.gitignore`忽略包含敏感信息的文件
- **配置模板**：提供配置文件模板，避免直接提交敏感信息

#### .gitignore配置

```gitignore
# 编译产物
*.o
*.exe
*.hex
*.bin

# 临时文件
*.tmp
*.log

# 编辑器文件
.vscode/
.idea/
*.swp
*.swo

# 配置文件（如果包含敏感信息）
mcu_config.json

# 环境文件
.env

# 构建目录
dist/
build/
```

## 更新检查功能

### 版本检查机制

#### 本地版本检查

1. **读取当前版本**：从`_meta.json`读取当前版本
2. **检查更新**：定期检查远程仓库的最新版本
3. **版本比较**：比较本地版本和远程版本
4. **更新提示**：当发现新版本时提示用户

#### 远程版本检查

1. **GitHub API**：使用GitHub API获取最新版本
2. **版本比较**：比较本地版本和远程版本
3. **更新通知**：发送更新通知给用户

### 更新检查脚本

#### 版本检查脚本

```python
#!/usr/bin/env python3
"""版本检查脚本"""
import os
import json
import requests
import semver

def get_local_version(skill_dir):
    """获取本地版本"""
    meta_path = os.path.join(skill_dir, "_meta.json")
    if not os.path.exists(meta_path):
        return None
    
    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        return meta.get("version")
    except Exception as e:
        print(f"读取本地版本失败: {e}")
        return None

def get_remote_version(repo_url):
    """获取远程版本"""
    try:
        # 从GitHub API获取最新版本
        api_url = repo_url.replace("github.com", "api.github.com/repos").rstrip(".git") + "/releases/latest"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            tag_name = data.get("tag_name")
            if tag_name.startswith("v"):
                return tag_name[1:]
            return tag_name
        return None
    except Exception as e:
        print(f"获取远程版本失败: {e}")
        return None

def check_update(skill_dir, repo_url):
    """检查更新"""
    local_version = get_local_version(skill_dir)
    if not local_version:
        print("无法获取本地版本")
        return False
    
    remote_version = get_remote_version(repo_url)
    if not remote_version:
        print("无法获取远程版本")
        return False
    
    print(f"本地版本: {local_version}")
    print(f"远程版本: {remote_version}")
    
    try:
        if semver.compare(remote_version, local_version) > 0:
            print("发现新版本！")
            print(f"建议更新到版本 {remote_version}")
            return True
        else:
            print("当前已是最新版本")
            return False
    except Exception as e:
        print(f"版本比较失败: {e}")
        return False

def main():
    """主函数"""
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    repo_url = "https://github.com/username/mcu-c99-assistant.git"
    
    print("检查技能更新...")
    has_update = check_update(skill_dir, repo_url)
    
    if has_update:
        print("\n更新建议:")
        print("1. 手动更新: git pull origin master")
        print("2. 重新部署: 运行 deploy_skills.bat")

if __name__ == "__main__":
    main()
```

#### 自动更新脚本

```python
#!/usr/bin/env python3
"""自动更新脚本"""
import os
import subprocess
import sys

def update_skill(skill_dir, repo_url):
    """更新技能"""
    print(f"更新技能: {skill_dir}")
    
    # 切换到技能目录
    os.chdir(skill_dir)
    
    try:
        # 拉取最新代码
        print("拉取最新代码...")
        subprocess.run(["git", "pull", "origin", "master"], check=True)
        print("✅ 代码更新成功")
        
        # 检查是否需要重新部署
        print("检查是否需要重新部署...")
        return True
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return False

def main():
    """主函数"""
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    repo_url = "https://github.com/username/mcu-c99-assistant.git"
    
    print("开始自动更新技能...")
    success = update_skill(skill_dir, repo_url)
    
    if success:
        print("\n🎉 技能更新完成！")
        print("建议重新运行部署脚本以更新全局技能")
    else:
        print("\n❌ 技能更新失败，请手动更新")

if __name__ == "__main__":
    main()
```

### 更新通知机制

#### 邮件通知

1. **配置邮件服务**：设置SMTP服务器和邮箱
2. **通知模板**：创建更新通知邮件模板
3. **发送通知**：当发现新版本时发送邮件通知

#### 本地通知

1. **系统通知**：使用系统通知机制发送更新提示
2. **日志记录**：记录更新检查结果到日志文件
3. **UI通知**：在Trae IDE中显示更新通知

## 维护流程

### 日常维护

1. **代码检查**：定期检查代码质量和安全性
2. **依赖更新**：更新依赖包到最新版本
3. **文档更新**：更新文档以反映最新功能
4. **测试验证**：运行测试确保功能正常

### 版本发布流程

1. **代码冻结**：在发布前冻结代码
2. **测试**：运行全面测试
3. **版本号更新**：更新版本号
4. **变更日志**：更新变更日志
5. **标签创建**：创建版本标签
6. **发布**：推送代码和标签到远程仓库
7. **部署**：部署新版本

### 回滚机制

1. **版本备份**：备份每个版本的代码
2. **回滚计划**：制定回滚计划
3. **回滚测试**：测试回滚流程
4. **回滚执行**：当出现问题时执行回滚

## 监控与日志

### 运行监控

1. **技能使用统计**：记录技能的使用情况
2. **错误监控**：监控技能执行过程中的错误
3. **性能监控**：监控技能的性能指标

### 日志管理

1. **日志配置**：配置日志级别和格式
2. **日志存储**：存储日志到文件
3. **日志分析**：分析日志以发现问题
4. **日志轮转**：定期轮转日志文件

### 监控脚本

```python
#!/usr/bin/env python3
"""技能监控脚本"""
import os
import json
import time
from datetime import datetime

def log_usage(skill_name, action, duration):
    """记录技能使用情况"""
    log_file = "skill_usage.log"
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "skill": skill_name,
        "action": action,
        "duration": duration,
        "status": "success"
    }
    
    with open(log_file, 'a', encoding='utf-8') as f:
        json.dump(log_entry, f)
        f.write('\n')

def log_error(skill_name, error_message):
    """记录错误"""
    error_file = "skill_errors.log"
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "skill": skill_name,
        "error": error_message
    }
    
    with open(error_file, 'a', encoding='utf-8') as f:
        json.dump(error_entry, f)
        f.write('\n')

def analyze_logs():
    """分析日志"""
    usage_log = "skill_usage.log"
    error_log = "skill_errors.log"
    
    # 分析使用情况
    if os.path.exists(usage_log):
        with open(usage_log, 'r', encoding='utf-8') as f:
            usage_entries = [json.loads(line) for line in f if line.strip()]
        
        total_usage = len(usage_entries)
        success_count = len([e for e in usage_entries if e.get("status") == "success"])
        avg_duration = sum(e.get("duration", 0) for e in usage_entries) / total_usage if total_usage > 0 else 0
        
        print(f"使用统计:")
        print(f"总使用次数: {total_usage}")
        print(f"成功次数: {success_count}")
        print(f"平均执行时间: {avg_duration:.2f} 秒")
    
    # 分析错误情况
    if os.path.exists(error_log):
        with open(error_log, 'r', encoding='utf-8') as f:
            error_entries = [json.loads(line) for line in f if line.strip()]
        
        error_count = len(error_entries)
        error_types = {}
        for entry in error_entries:
            error = entry.get("error", "Unknown")
            error_types[error] = error_types.get(error, 0) + 1
        
        print(f"\n错误统计:")
        print(f"总错误次数: {error_count}")
        print("错误类型:")
        for error, count in error_types.items():
            print(f"  - {error}: {count} 次")

def main():
    """主函数"""
    print("分析技能监控日志...")
    analyze_logs()

if __name__ == "__main__":
    main()
```

## 安全维护

### 安全检查

1. **代码安全**：定期检查代码中的安全漏洞
2. **依赖安全**：检查依赖包的安全漏洞
3. **配置安全**：检查配置文件中的敏感信息
4. **网络安全**：检查网络请求的安全性

### 安全更新

1. **漏洞修复**：及时修复发现的安全漏洞
2. **依赖更新**：更新存在安全问题的依赖包
3. **安全补丁**：发布安全补丁
4. **安全通知**：向用户发送安全通知

### 安全最佳实践

1. **最小权限**：使用最小权限原则
2. **输入验证**：验证所有用户输入
3. **加密存储**：加密存储敏感信息
4. **安全日志**：记录安全相关事件
5. **定期审计**：定期进行安全审计

## 文档维护

### 文档更新

1. **内容更新**：更新文档以反映最新功能
2. **格式统一**：保持文档格式的一致性
3. **链接检查**：检查文档中的链接是否有效
4. **示例更新**：更新文档中的示例代码

### 文档版本控制

1. **文档版本**：为每个版本维护对应的文档
2. **文档标签**：使用Git标签标记文档版本
3. **文档差异**：记录文档的变更历史

### 文档生成

1. **自动生成**：使用工具自动生成API文档
2. **文档模板**：使用统一的文档模板
3. **文档部署**：将文档部署到合适的平台

## 最佳实践

1. **定期更新**：定期更新技能和依赖
2. **版本控制**：使用Git进行版本管理
3. **自动化**：自动化测试和部署流程
4. **监控**：监控技能的使用和性能
5. **安全**：定期进行安全检查
6. **文档**：保持文档的更新和完整
7. **回滚**：准备回滚计划以应对问题
8. **沟通**：及时向用户通知更新和问题

## 示例维护流程

### 每周维护

1. **代码检查**：检查代码质量和安全性
2. **依赖更新**：更新依赖包
3. **文档更新**：更新文档
4. **测试**：运行测试
5. **监控分析**：分析监控数据

### 版本发布

1. **代码冻结**：在发布前冻结代码
2. **全面测试**：运行所有测试
3. **版本号更新**：更新版本号
4. **变更日志**：更新变更日志
5. **标签创建**：创建版本标签
6. **推送**：推送代码和标签
7. **部署**：部署新版本
8. **通知**：通知用户更新

### 问题处理

1. **问题识别**：识别和确认问题
2. **问题分析**：分析问题原因
3. **解决方案**：制定解决方案
4. **修复实施**：实施修复
5. **测试验证**：验证修复效果
6. **发布**：发布修复版本
7. **通知**：通知用户修复情况