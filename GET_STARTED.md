# MedClaw 使用指南

## 🚀 立即开始

### 1. 构建容器（首次使用必须）

```bash
cd /home/taotl/Desktop/MedClaw
./container/build.sh
```

这将安装所有医学分析工具（约需 5-10 分钟）。

### 2. 配置环境

创建 `.env` 文件：

```bash
cp .env.example .env
nano .env
```

添加你的 API 密钥：

```bash
ANTHROPIC_API_KEY=your_api_key_here
ASSISTANT_NAME=MedClaw
```

### 3. 运行设置

```bash
claude
```

在 Claude Code 中运行：

```
/setup
```

## 📊 测试医学功能

### 测试 DICOM 处理

创建测试脚本：

```bash
mkdir -p test_data
cd test_data

# 下载示例 DICOM 文件（可选）
# wget https://www.rubomedical.com/dicom_files/chest.zip
# unzip chest.zip
```

在 Claude Code 中：

```
@MedClaw 我有一个 DICOM 文件在 test_data/scan.dcm，请分析它的元数据
```

### 测试基因组分析

```
@MedClaw 创建一个示例 VCF 文件并解析它
```

### 测试图像分割

```
@MedClaw 演示如何使用 SimpleITK 进行图像分割
```

## 🛠️ 常用命令

### 医学影像分析

```bash
# DICOM 分析
@MedClaw 读取 /path/to/dicom/file.dcm 并显示患者信息和影像参数

# NIfTI 分析
@MedClaw 加载 brain.nii.gz 并计算脑容量

# 图像分割
@MedClaw 对这个 CT 扫描进行阈值分割，阈值范围 100-400

# 体积计算
@MedClaw 从这个分割结果计算肿瘤体积
```

### 基因组数据分析

```bash
# VCF 解析
@MedClaw 解析 variants.vcf 并显示质量 > 30 的变异

# BAM 统计
@MedClaw 分析 aligned.bam 并显示比对统计信息

# 序列分析
@MedClaw 计算 genome.fasta 中所有序列的 GC 含量

# 变异过滤
@MedClaw 过滤 chr17:7571720-7590868 区域的变异（TP53 基因）
```

### 临床数据处理

```bash
# FHIR 资源
@MedClaw 创建一个 FHIR Patient 资源，姓名 John Doe，性别 male

# 数据匿名化
@MedClaw 匿名化这个 DICOM 文件中的患者信息

# 生命体征
@MedClaw 从这些 Observation 资源中提取生命体征
```

## 📁 项目结构

```
MedClaw/
├── container/
│   ├── medical-tools/          # 医学工具脚本
│   │   ├── dicom_utils.py      # DICOM 处理
│   │   ├── nifti_utils.py      # NIfTI 分析
│   │   ├── genomics_utils.py   # 基因组分析
│   │   ├── segmentation_utils.py # 图像分割
│   │   └── clinical_utils.py   # 临床数据
│   ├── Dockerfile              # 容器配置
│   └── build.sh                # 构建脚本
├── docs/
│   ├── QUICK_START.md          # 快速开始
│   ├── SETUP_GUIDE.md          # 安装指南
│   ├── MEDICAL_ANALYSIS_GUIDE.md # 分析指南
│   └── MEDICAL_DATA_FORMATS.md # 数据格式
├── src/                        # 源代码
├── groups/                     # 群组配置
├── README.md                   # 项目说明
└── .env                        # 环境配置
```

## 🔧 配置医学数据目录

编辑 `.env` 文件：

```bash
# 医学数据路径
MEDICAL_DATA_ROOT=/path/to/medical/data
DICOM_DATA_PATH=/path/to/dicom/studies
GENOMICS_DATA_PATH=/path/to/genomics/data
NIFTI_DATA_PATH=/path/to/nifti/data
```

## 💡 使用技巧

### 1. 批量处理

```
@MedClaw 分析 /data/dicom_studies/ 目录下的所有 DICOM 序列
```

### 2. 定时任务

```
@MedClaw 每天早上 8 点检查新的影像研究并生成质控报告
```

### 3. 数据转换

```
@MedClaw 将这个 DICOM 序列转换为 NIfTI 格式
```

### 4. 工作流自动化

```
@MedClaw 创建一个完整的 CT 肝脏分割工作流：
1. 读取 DICOM 序列
2. 转换为 Hounsfield 单位
3. 分割肝脏（阈值 40-60 HU）
4. 计算肝脏体积
5. 保存结果
```

## 📚 学习资源

### 文档

1. **快速开始**: `docs/QUICK_START.md`
   - 5 分钟快速上手

2. **医学分析指南**: `docs/MEDICAL_ANALYSIS_GUIDE.md`
   - DICOM 处理示例
   - NIfTI 分析示例
   - 基因组分析示例
   - 完整工作流

3. **数据格式**: `docs/MEDICAL_DATA_FORMATS.md`
   - 支持的文件格式
   - 格式转换方法
   - 最佳实践

4. **安装指南**: `docs/SETUP_GUIDE.md`
   - 详细安装步骤
   - 配置说明
   - 故障排除

### 示例代码

查看 `container/medical-tools/` 目录下的 Python 脚本：

```bash
# 查看 DICOM 工具
cat container/medical-tools/dicom_utils.py

# 查看基因组工具
cat container/medical-tools/genomics_utils.py

# 查看分割工具
cat container/medical-tools/segmentation_utils.py
```

## 🐛 故障排除

### 容器构建失败

```bash
# 清理 Docker 缓存
docker system prune -a

# 重新构建
cd container
./build.sh --no-cache
```

### 内存不足

增加 Docker 内存限制：

**macOS**: Docker Desktop → Settings → Resources → Memory: 16GB

**Linux**: 编辑 `/etc/docker/daemon.json`

### Python 包缺失

```bash
# 进入容器
docker run -it --rm medclaw-agent /bin/bash

# 安装包
pip install package-name

# 或重新构建容器
```

### 权限问题

```bash
# 修复医学数据目录权限
chmod -R 755 /path/to/medical/data
chown -R $USER:$USER /path/to/medical/data
```

## 🔒 安全最佳实践

1. **数据加密**: 使用加密卷存储敏感医学数据
2. **访问控制**: 配置适当的文件系统权限
3. **数据匿名化**: 处理前匿名化患者信息
4. **审计日志**: 启用数据访问日志
5. **合规性**: 遵循 HIPAA/GDPR 要求

## 📞 获取帮助

- **文档**: 查看 `docs/` 目录
- **调试**: 在 Claude Code 中运行 `/debug`
- **日志**: `docker logs medclaw-agent`
- **Discord**: https://discord.gg/VDdww8qS42
- **GitHub Issues**: https://github.com/taotianli/MedClaw/issues

## 🎯 下一步

1. ✅ 构建容器
2. ✅ 配置环境
3. ✅ 运行设置
4. 📊 测试医学功能
5. 📖 阅读文档
6. 🚀 开始分析你的医学数据

---

**提示**: 首次使用建议先阅读 `docs/QUICK_START.md` 和 `docs/MEDICAL_ANALYSIS_GUIDE.md`。

**注意**: MedClaw 仅供研究和教育用途。临床使用需要适当的验证和监管批准。
