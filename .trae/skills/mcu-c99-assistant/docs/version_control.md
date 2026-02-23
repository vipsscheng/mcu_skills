# 版本控制

## Git版本控制基础

### 初始化仓库

```bash
# 在现有目录初始化git仓库
git init

# 克隆远程仓库
git clone <repository-url>
```

### 基本Git命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `git add` | 添加文件到暂存区 | `git add .` |
| `git commit` | 提交更改 | `git commit -m "提交信息"` |
| `git push` | 推送到远程仓库 | `git push origin master` |
| `git pull` | 从远程仓库拉取 | `git pull origin master` |
| `git status` | 查看状态 | `git status` |
| `git log` | 查看提交历史 | `git log --oneline` |
| `git branch` | 管理分支 | `git branch feature/new` |
| `git checkout` | 切换分支 | `git checkout feature/new` |
| `git merge` | 合并分支 | `git merge feature/new` |

### 分支管理策略

#### Git Flow工作流

1. **master分支**：只包含稳定版本
2. **develop分支**：开发主分支
3. **feature分支**：功能开发分支
4. **release分支**：发布准备分支
5. **hotfix分支**：紧急修复分支

#### 分支命名规范

- `feature/功能名称`：新功能开发
- `bugfix/问题描述`：bug修复
- `hotfix/紧急修复`：紧急问题修复
- `release/版本号`：发布准备

### 提交信息规范

#### 提交信息结构

```
<类型>(<范围>): <描述>

<详细说明>

<尾部信息>
```

#### 提交类型

- `feat`：新功能
- `fix`：bug修复
- `docs`：文档更新
- `style`：代码风格调整
- `refactor`：代码重构
- `test`：测试相关
- `chore`：构建或依赖更新

#### 示例

```
feat(adc): 添加ADC采集功能

- 实现ADC初始化和读取
- 添加数据滤波算法
- 支持多通道采集

Signed-off-by: Your Name <your.email@example.com>
```

## 版本号管理

### 语义化版本规范

采用 `MAJOR.MINOR.PATCH` 格式：

- **MAJOR**：不兼容的API变更
- **MINOR**：向后兼容的功能添加
- **PATCH**：向后兼容的bug修复

### 版本标签

```bash
# 创建版本标签
git tag v1.0.0

# 推送标签到远程
git push origin v1.0.0
```

## 忽略文件配置

### .gitignore文件示例

```gitignore
# 编译产物
*.o
*.elf
*.hex
*.bin
*.map
*.lst

# 临时文件
*.tmp
*.log
*.bak

# 编辑器文件
.vscode/
.idea/
*.swp
*.swo

# 构建目录
build/
out/

# 依赖文件
*.d

# 环境配置
.env
local_config.h
```

## 远程仓库管理

### 添加远程仓库

```bash
git remote add origin <repository-url>
```

### 远程仓库操作

```bash
# 查看远程仓库
git remote -v

# 拉取远程更新
git pull origin master

# 推送到远程仓库
git push origin master

# 推送所有分支
git push --all origin
```

## 协作开发

### 代码审查

1. **创建Pull Request**：功能完成后，从特性分支向develop分支创建PR
2. **代码审查**：团队成员审查代码，提出修改建议
3. **合并代码**：审查通过后，合并到目标分支

### 解决冲突

```bash
# 拉取最新代码
git pull origin master

# 手动解决冲突
# 编辑冲突文件

# 标记冲突已解决
git add <冲突文件>

# 完成合并
git commit
```

## CI/CD集成

### 持续集成配置

#### GitHub Actions示例

```yaml
name: Build and Test

on:
  push:
    branches: [ master, develop ]
  pull_request:
    branches: [ master, develop ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up toolchain
      run: |
        sudo apt-get update
        sudo apt-get install -y gcc-arm-none-eabi
    - name: Build project
      run: make
    - name: Run tests
      run: make test
```

### 自动构建和部署

1. **自动构建**：代码提交后自动编译
2. **自动测试**：运行单元测试和集成测试
3. **自动部署**：通过IAP方式远程更新设备固件

## 版本控制最佳实践

1. **定期提交**：小步提交，频繁更新
2. **分支管理**：合理使用分支，避免分支混乱
3. **提交信息**：清晰、规范的提交信息
4. **代码审查**：严格的代码审查流程
5. **版本标签**：重要版本添加标签
6. **备份策略**：定期备份远程仓库
7. **忽略文件**：合理配置.gitignore文件
8. **文档同步**：版本更新时同步更新文档

## 常见问题处理

### 撤销更改

```bash
# 撤销工作区更改
git checkout -- <file>

# 撤销暂存区更改
git reset HEAD <file>

# 撤销最近一次提交
git reset --soft HEAD^  # 保留更改
git reset --hard HEAD^  # 丢弃更改
```

### 回滚版本

```bash
# 查看历史版本
git log --oneline

# 回滚到指定版本
git checkout <commit-hash>

# 创建新分支保存回滚状态
git checkout -b fix/rollback
```

### 子模块管理

```bash
# 添加子模块
git submodule add <repository-url> <path>

# 初始化子模块
git submodule init

# 更新子模块
git submodule update

# 克隆包含子模块的仓库
git clone --recursive <repository-url>
```

## 工具集成

### IDE集成

- **VS Code**：安装Git扩展，支持Git操作
- **Keil MDK**：集成Git版本控制
- **IAR Embedded Workbench**：支持Git操作

### 图形化工具

- **Git GUI**：Git官方图形界面工具
- **SourceTree**：免费的Git客户端
- **GitHub Desktop**：GitHub官方客户端
- **GitKraken**：功能强大的Git客户端

## 企业级版本控制

### GitLab配置

1. **私有仓库**：创建企业内部GitLab服务器
2. **权限管理**：设置不同角色的访问权限
3. **CI/CD管道**：配置自动化构建和测试
4. **代码质量**：集成代码质量分析工具

### 代码安全

1. **敏感信息保护**：避免提交密码、密钥等敏感信息
2. **代码扫描**：集成安全扫描工具
3. **访问控制**：设置合理的仓库访问权限
4. **审计日志**：记录所有Git操作

## 总结

版本控制是嵌入式软件开发的重要组成部分，合理使用Git可以：

1. **跟踪代码变更**：记录所有代码修改历史
2. **协作开发**：支持多人同时开发
3. **分支管理**：隔离不同功能和版本
4. **代码审查**：提高代码质量
5. **版本回滚**：快速恢复到之前的稳定版本
6. **CI/CD集成**：自动化构建和测试

通过遵循版本控制最佳实践，可以显著提高开发效率和代码质量，减少开发过程中的问题。