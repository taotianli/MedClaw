<p align="center">
  <img src="assets/nanoclaw-logo.png" alt="MedClaw" width="400">
</p>

<p align="center">
  面向医学影像和基因组数据的AI驱动医学分析助手。基于安全的容器化代理构建，配备医疗研究和临床工作流程的专业工具。
</p>

<p align="center">
  <a href="README.md">English</a>&nbsp; • &nbsp;
  <a href="https://discord.gg/VDdww8qS42"><img src="https://img.shields.io/discord/1470188214710046894?label=Discord&logo=discord&v=2" alt="Discord" valign="middle"></a>
</p>

MedClaw 利用 Claude Code 提供医学影像（DICOM、NIfTI、显微镜）和基因组数据（VCF、FASTQ、BAM）的智能分析，支持临床工作流程和研究管道。

## 为什么选择 MedClaw

医学数据分析需要专业工具、安全处理敏感患者信息以及与临床工作流程的集成。MedClaw 提供：

- **安全隔离** - 患者数据保留在具有文件系统隔离的容器化环境中
- **医学影像支持** - DICOM、NIfTI、全切片成像和显微镜分析
- **基因组分析** - 变异检测、序列比对、基因表达分析
- **临床集成** - HL7/FHIR 支持、电子病历集成能力
- **研究工作流程** - 批处理、管道自动化、可重现分析
- **轻量级架构** - 小型代码库，便于理解和合规性审计

## 快速开始

```bash
git clone https://github.com/taotianli/MedClaw.git
cd MedClaw
claude
```

然后运行 `/setup`。Claude Code 会处理依赖项、医学工具安装、容器设置和服务配置。

> **注意：** 以 `/` 为前缀的命令（如 `/setup`）是 [Claude Code 技能](https://code.claude.com/docs/en/skills)。在 `claude` CLI 提示符中输入它们。

## 医学功能

### 医学影像
- **DICOM 处理** - 读取、分析和转换 DICOM 文件
- **NIfTI 分析** - 脑成像、fMRI、结构性 MRI 处理
- **全切片成像** - 数字病理学、组织学分析
- **图像分割** - 器官、肿瘤和组织分割
- **3D 重建** - CT/MRI 体积渲染和分析
- **图像配准** - 多模态图像对齐

### 基因组分析
- **变异分析** - VCF 解析、注释、过滤
- **序列比对** - BAM/SAM 文件处理、质量控制
- **基因表达** - RNA-seq 分析、差异表达
- **基因组组装** - 从头组装、支架构建
- **系统发育分析** - 进化树构建、进化分析
- **注释** - 基因预测、功能注释

### 临床工具
- **HL7/FHIR** - 医疗数据交换标准
- **电子病历集成** - 电子健康记录连接
- **临床决策支持** - 循证建议
- **报告生成** - 结构化临床报告
- **数据匿名化** - 符合 HIPAA 的去标识化

## 医学工具和库

MedClaw 包含预配置的医学分析工具：

**影像学：**
- pydicom - DICOM 文件处理
- nibabel - 神经影像数据 I/O
- SimpleITK - 图像分析和配准
- scikit-image - 图像处理算法
- OpenSlide - 全切片成像
- 3D Slicer 集成 - 高级可视化

**基因组学：**
- BioPython - 序列分析
- pysam - SAM/BAM 文件操作
- PyVCF - VCF 文件解析
- scikit-bio - 生物信息学算法
- GATK 集成 - 变异检测管道
- Samtools/BCFtools - 序列数据处理

**机器学习：**
- TensorFlow/PyTorch - 深度学习框架
- MONAI - 医学影像 AI 工具包
- DeepVariant - 基因组变异检测
- nnU-Net - 医学图像分割

**临床：**
- FHIR-py - FHIR 资源处理
- HL7apy - HL7 消息处理
- Presidio - 数据匿名化

## 使用示例

使用触发词（默认：`@MedClaw`）与您的医学助手对话：

```
@MedClaw 分析这个 DICOM 序列，识别 CT 扫描中的任何异常
@MedClaw 处理这些 VCF 文件，生成致病性突变的变异报告
@MedClaw 从这个 MRI 扫描中分割肿瘤区域并计算体积
@MedClaw 比对这些 RNA-seq 读段并进行差异表达分析
@MedClaw 将这个全切片图像转换为金字塔 TIFF 并提取组织区域
@MedClaw 每周一早上 8 点检查新的影像研究并生成质量控制报告
```

从主频道管理分析工作流程：
```
@MedClaw 列出所有计划的基因组管道任务
@MedClaw 暂停每周影像质控任务
@MedClaw 显示变异检测管道的状态
```

## 安全性与合规性

**HIPAA 注意事项：**
- 容器隔离保护患者数据
- 所有数据访问的审计日志
- 包含数据匿名化工具
- 加密存储建议
- 通过文件系统挂载进行访问控制

**最佳实践：**
- 审查代码库以满足合规性要求
- 配置适当的数据保留策略
- 对敏感数据使用加密卷
- 为频道实施适当的身份验证
- 定期安全审计

详细安全模型请参见 [docs/SECURITY.md](docs/SECURITY.md)。

## 定制化

MedClaw 设计为可针对您的特定医学工作流程进行定制：

- "添加对分析 PET/CT 融合图像的支持"
- "与我们医院的 PACS 系统集成"
- "创建自动肺结节检测管道"
- "添加对单细胞 RNA-seq 分析的支持"
- "以我们的模板格式生成结构化放射学报告"

或运行 `/customize` 进行引导式更改。

## 架构

```
频道 --> SQLite --> 轮询循环 --> 容器（Claude Agent SDK + 医学工具）--> 响应
```

单个 Node.js 进程，医学分析工具在隔离的容器中运行。只能访问挂载的医学数据目录。每组消息队列具有并发控制。

关键文件：
- `src/index.ts` - 编排器：状态、消息循环、代理调用
- `src/channels/registry.ts` - 频道注册表（自注册）
- `src/container-runner.ts` - 使用医学工具生成代理容器
- `container/medical-tools/` - 医学影像和基因组学工具配置
- `groups/*/CLAUDE.md` - 每组医学上下文和内存

## 支持的医学数据格式

**影像学：**
- DICOM (.dcm, .dicom)
- NIfTI (.nii, .nii.gz)
- NRRD (.nrrd)
- Analyze (.hdr, .img)
- TIFF/BigTIFF (.tif, .tiff)
- SVS、NDPI（全切片格式）

**基因组学：**
- FASTQ (.fastq, .fq, .fastq.gz)
- FASTA (.fasta, .fa, .fna)
- SAM/BAM/CRAM (.sam, .bam, .cram)
- VCF/BCF (.vcf, .vcf.gz, .bcf)
- GFF/GTF (.gff, .gtf)
- BED (.bed)

**临床：**
- HL7 v2 消息
- FHIR JSON/XML
- CDA 文档

## 系统要求

- macOS 或 Linux
- Node.js 20+
- [Claude Code](https://claude.ai/download)
- [Docker](https://docker.com/products/docker-desktop)（用于容器隔离）
- Python 3.9+（用于医学分析工具）
- 建议 16GB+ RAM 用于影像分析
- 建议使用 GPU 进行深度学习任务

## 贡献

**添加医学分析技能，而不是功能。**

贡献教 Claude Code 如何添加医学功能的技能：

- `/add-pacs-integration` - 连接到 PACS 系统
- `/add-pathology-viewer` - 全切片图像查看器
- `/add-variant-pipeline` - 自动变异检测
- `/add-dicom-router` - DICOM 网络和路由
- `/add-clinical-nlp` - 从临床笔记中提取信息

### RFS（技能请求）

我们希望看到的医学技能：

**影像分析**
- `/add-brain-segmentation` - 自动脑结构分割
- `/add-lung-nodule-detection` - CT 肺结节检测管道
- `/add-cardiac-analysis` - 心脏 MRI 分析工具

**基因组学**
- `/add-somatic-pipeline` - 癌症体细胞变异检测
- `/add-rna-seq-pipeline` - 完整的 RNA-seq 分析工作流程
- `/add-metagenomics` - 微生物组分析工具

**临床集成**
- `/add-ehr-connector` - 电子病历系统集成
- `/add-radiology-reporting` - 结构化报告生成
- `/add-clinical-trials` - 临床试验数据管理

## 常见问题

**这符合 HIPAA 吗？**

MedClaw 提供技术保障（容器隔离、审计日志、加密支持），但 HIPAA 合规性需要组织政策、商业伙伴协议和适当的实施。审查代码库并为您的用例实施适当的控制。

**我可以将其用于临床诊断吗？**

MedClaw 是一个研究和分析工具。任何临床使用都需要适当的验证、监管批准以及合格医疗专业人员的监督。始终遵循适用的法规和指南。

**数据隐私如何？**

所有分析都在隔离的容器中运行。除非您明确配置外部集成，否则患者数据永远不会离开您的系统。使用加密存储和适当的访问控制。

**我可以与我们医院的系统集成吗？**

可以。MedClaw 可以定制以与 PACS、电子病历、LIS 和其他临床系统集成。使用技能或自定义代码添加集成。

**如何处理大型影像数据集？**

为您的数据存储配置适当的挂载点，使用批处理工作流程，并考虑使用 GPU 加速进行深度学习任务。容器系统支持挂载网络存储和高性能文件系统。

## 社区

有问题？想法？[加入 Discord](https://discord.gg/VDdww8qS42)。

## 许可证

MIT

**免责声明：** MedClaw 仅供研究和教育目的。未经适当验证和监管批准，不得用于临床诊断或治疗决策。用户负责遵守适用的医疗法规，包括 HIPAA、GDPR 和当地法律。
