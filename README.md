# smartai-runtime

smartai 的可选原生运行时候选仓库。当前记录 Linux/WSL amd64 的 8 个固定候选包（LLM、ASR、TTS 常驻 worker、FFmpeg 和 OpenTelemetry Collector）；模型权重不在运行时包中。

**状态：候选身份已登记，归档尚未在本仓库公开发布。** `source-catalog.json` 记录从 smartai 项目固定的归档大小、SHA-256、包内清单摘要和依赖信息。它是来源清单，不是可供 `smartai runtime install` 使用的在线 feed。只有 Release 附件全部上传、校验和许可证材料核对通过后，才会发布相应版本的 `catalog.json`。

发布布局、校验命令和准入条件见 [发布指南](docs/release-process.md)。发布记录必须区分预发布验证、GitHub 附件已上传和独立网络下载验证。

当前候选仅覆盖 Debian 13.7 / WSL2 上验证过的 Linux amd64 CPU/CUDA 组合，以及 Collector CPU。原生 Linux、Windows 和 Vulkan 需要各自构建与验证。CUDA 包依赖宿主驱动；发现 GPU 不代表能力检查通过。

源项目：smartai。仓库公开内容只保存运行时候选身份和发布资料。
