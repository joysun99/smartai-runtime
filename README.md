# smartai-runtime

smartai CLI 和可选原生运行时的公开发布仓库。大归档放在 GitHub Release 附件；模型权重由 smartai 按独立模型目录下载。

## 已公开版本

| 对象 | 版本 | 平台与范围 | 发布附件 |
| --- | --- | --- | --- |
| smartai CLI | `0.4.0-alpha.6` | Linux/WSL、Windows amd64 | [CLI Release](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-v0.4.0-alpha.6) |
| runtimes | `1.0.0-alpha.7` | Linux/WSL CPU/CUDA、Windows amd64 CPU；LLM、ASR、TTS、FFmpeg | [runtimes Release](https://github.com/joysun99/smartai-runtime/releases/tag/runtimes-v1.0.0-alpha.7) |

两个版本均为预发布，需显式选择。CLI 安装器及版本列表位于 [smartai-cli-index](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-cli-index)；运行时完整版本列表和预发布目录位于 [smartai-runtime-index](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-runtime-index)。`catalog-all.json` 列出预发布运行时；`catalog-v3.json` 仅用于正式稳定版推荐，目前为空。runtime 组合声明最低 CLI `0.4.0-alpha.6`；Windows 应使用已修复在线安装目录提交问题的 `0.4.0-alpha.6`。

每个运行时归档附有 `SOURCE_MANIFEST.json` 和许可证材料；对应 Release 的 `SOURCES.md`、`source-origins.json` 标明第三方来源、锁定版本和 SHA-256。FFmpeg/LAME 原始源码及 Kokoro worker 源码另作附件。CLI 的使用条款、免责声明和 Go 依赖许可证位于二进制包的 `INSTALL.md`，第一方 CLI 源码未公开。

当前 CLI 的 8 个附件与 runtime 的 32 个附件已按发布端大小和摘要核对，并通过匿名 HTTPS 完整下载校验。Linux/WSL 与 Windows 原生 CPU 的安装、四种 runtime、固定模型及 LLM/ASR/TTS 用户流程已验证；WSL CUDA 逐项服务 API 也已通过；Windows CUDA、Vulkan、其他 Linux 发行版和广泛语言质量仍待验证。旧 `source-catalog.json` 是历史候选快照，**不是**在线安装目录；旧候选的许可状态见 [许可审查](docs/license-review.md)。

CLI alpha.6 的 Windows 同摘要候选已通过公网 runtime/模型下载及三服务 API、私有快捷方式和退出清理；公开后 Linux/Windows 安装器实际安装与版本检查通过。Linux 完整公网推理链路针对 alpha.5；验收使用既有宿主与代理，干净 OS、直连网络和 GPU 尚未据此验收。


runtime alpha.7 包含 11 个运行包，完整预发布目录共保留 19 个不可变版本。旧 CLI 的资源中心默认查询稳定目录（当前为空），如只看到模型卡片，显式设置后等待下载完成、重启 daemon，再刷新运行包目录：

```bash
smartai config set download.runtime_catalog https://github.com/joysun99/smartai-runtime/releases/download/smartai-runtime-index/catalog-all.json
```

本次 alpha.7 的公开 GitHub CLI/runtime 与 Hugging Face 三模型下载、WSL CUDA 逐项 LLM JSON/SSE、ASR、TTS 三格式、控制台会话 API 安装/TTS 启停、退出清理通过。测试使用现有宿主和代理，不代表干净 OS、直连网络、三项 GPU 同时负载或新的人工试听通过。CUDA 包随附锁定来源的运行库与许可证，不含显卡驱动；最低条件和实际验证范围以包清单为准。
