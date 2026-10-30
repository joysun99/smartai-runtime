# smartai-runtime

smartai CLI 和可选原生运行时的公开发布仓库。归档位于 GitHub Release；模型按独立目录下载，不放入 runtime 包。

## 当前版本

| 对象 | 版本 | 范围 | 附件 |
| --- | --- | --- | --- |
| smartai CLI | `0.4.0-alpha.10` | Linux/WSL、Windows amd64 | [CLI Release](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-v0.4.0-alpha.10) |
| runtimes | `1.0.0-alpha.8` | Linux amd64 CPU：LLM、Whisper ASR、Kokoro TTS、FFmpeg；glibc 2.36 基线 | [CPU runtime Release](https://github.com/joysun99/smartai-runtime/releases/tag/runtimes-v1.0.0-alpha.8) |
| runtimes | `1.0.0-alpha.7` | Linux/WSL CUDA、Windows amd64 CPU；旧 Linux CPU 包仍保留 | [runtime Release](https://github.com/joysun99/smartai-runtime/releases/tag/runtimes-v1.0.0-alpha.7) |

以上均为预发布，需显式选择。安装器和 CLI 版本位于 [smartai-cli-index](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-cli-index)；runtime 版本列表和目录位于 [smartai-runtime-index](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-runtime-index)。`catalog-all.json` 包含预发布与历史版本，`catalog-v3.json` 只用于稳定版推荐，当前为空。runtime 最低 CLI 为 `0.4.0-alpha.6`，建议使用最新 CLI。

## 安装与管理

下载最新版 `install.sh` 或 `install.ps1`，显式指定 CLI 版本 `0.4.0-alpha.10`。安装参数、私有 Windows daemon 快捷方式与授权说明见 [控制台访问指南](docs/console-access.md)和随包 `INSTALL.md`。CLI 第一方源码暂不公开，免费使用条款及免责声明、Go 第三方许可证随包提供。

启动后默认提供 Web Console。alpha.10 将 Runtime 按包发布版本、Models 按 ASR/LLM/TTS 分组，支持空闲资源确认卸载及历史任务折叠；设置页可切换 Hugging Face / hf-mirror，新计划立即生效、既有任务保持原来源。资源任务日志写 schema 3，请勿混用旧 CLI。勾选“包含预发布运行包”并刷新，预览后确认下载，完成后选择完整运行包、模型和 FFmpeg 显式启动服务。CLI 可使用：

```bash
smartai resource refresh --include-prereleases
```

已有固定版本不会自动升级；简写绑定也不会被目录刷新改写。旧 CLI 可显式配置完整目录：

```bash
smartai config set download.runtime_catalog https://github.com/joysun99/smartai-runtime/releases/download/smartai-runtime-index/catalog-all.json
```

默认 API 保持回环监听，设置页支持保存监听地址、多个推理 API Key 及有效期。控制台长期登录 Key 仅 CLI 可创建和删除。SSH 任意本地端口、明确 HTTPS URL 的 Nginx/Traefik 根路径和子路径部署见[访问指南](docs/console-access.md)。配置 version 3 可读取旧 v2，创建 Key 或变更配置后旧 CLI 会明确拒绝新配置。

## Linux CPU 的 glibc 兼容性

alpha.7 的部分 Linux CPU 依赖确实需要 glibc 2.38。glibc 2.36 主机请显式安装 alpha.8 的新 CPU 运行包，并在启动服务时选择这些完整 ID；无需替换系统 libc，也无需重新下载相同模型。对旧包反复“恢复”不能改变其二进制依赖。

alpha.8 从锁定 Debian 12/GCC 12 sysroot 构建源码组件，并选择同基线依赖。最终依赖闭包不得超过 glibc 2.36；清单保留实际最低符号要求。验收使用真实 glibc 2.36 用户态、既有宿主内核和 CPU，覆盖精确包能力、固定模型及三服务 API；这不等于另一台物理机、所有发行版或新增人工语音质量认证。CUDA/Windows runtime 的要求保持各自原清单，不据此降低。

## 发布材料与验证范围

每包附 `SOURCE_MANIFEST.json`、`licenses/`，Release 的 `SOURCES.md` 和 `source-origins.json` 记录来源、版本与摘要。FFmpeg/LAME、Kokoro worker 源码单独提供；CPU alpha.8 另附对应 GCC 原始源码、Debian 补丁和源描述文件。CLI 私有实现、模型权重和用户请求不包含在这些源码附件中。

公开附件通过匿名 HTTPS 完整下载与 SHA-256 后才更新发现索引，既有版本的 ID 和字节不可变。新包的归档时间使用对应源码 Git 提交时间，并保留安装后的程序及 NOTICE 时间；不是编译或安装发生时间。

已有验收包含 Linux/WSL CPU、Windows 原生 CPU 的固定模型与三服务流程，以及 WSL CUDA 逐项服务 API；CUDA 不包含宿主驱动。Windows CUDA、Vulkan、其他硬件、干净 OS、长期负载和广泛语言质量尚未据此验收。历史 `source-catalog.json` 是候选快照，不是在线安装 feed；旧候选许可状态见[许可审查](docs/license-review.md)。

alpha.8 的 CLI 8 个附件和 CPU runtime 18 个附件均已通过匿名 HTTPS 全量摘要校验，公开安装器已在 Linux/WSL 和 Windows 实际试装。完整 runtime 目录现为 23 项，稳定目录仍为空；公开安装不等于重复公网模型推理验收。

CLI alpha.9 的 Linux/Windows 安装器默认覆盖已有普通上版备份，仅保留紧邻上版；同版本复装不轮换备份，损坏包不改变现有程序及备份。新脚本已同步到 smartai-cli-index，也支持显式安装 alpha.8。请使用索引入口的新安装器，旧固定版本随附脚本保留原行为。

alpha.9 的 8 个发布附件均已通过匿名 HTTPS 与 SHA-256；公开新脚本在 Linux/Windows 已有备份时显式安装 alpha.8 的验证通过。旧脚本已删除的上次临时归档无法复用，首次换新脚本仍需下载一次。
