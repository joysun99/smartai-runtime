# smartai-runtime

smartai CLI 和原生运行包的公开分发仓库。CLI 第一方源码暂不公开；运行包和适用的 worker / 第三方对应源码通过 GitHub Release 提供。模型权重从固定上游地址下载，不放入 runtime 包。

## 当前版本

| 对象 | 版本 | 当前范围 | 下载 |
| --- | --- | --- | --- |
| smartai CLI | `1.0.2` | Linux/WSL amd64，含 Web Console | [CLI Release](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-v1.0.2) |
| runtimes | `1.0.1` | Linux/WSL amd64 CPU：LLM、ASR、TTS、FFmpeg、Vision | [runtime Release](https://github.com/joysun99/smartai-runtime/releases/tag/runtimes-v1.0.1) |

两类从 `1.0.1` 统一发布，旧版 Release 和附件已撤回；已安装的模型、运行包及配置不受远端撤回操作影响。当前优先完善 Linux/WSL CPU；Linux CUDA、Windows CPU、Windows CUDA 后续依次交付。当前没有 Windows/CUDA 下载；CLI 与 runtime 版本独立，runtime 继续使用 1.0.1。

运行包最低 CLI 为 `1.0.1`；具体 CPU 指令、系统库和依赖要求见各包 manifest。Linux 使用 glibc 2.36 基线；已完成本机 Linux/WSL CPU 的精确包及固定模型验证，其他环境和广泛质量需分别验收。

## 安装 CLI

在希望安装的目录获取最新脚本；默认安装脚本所在目录的最新稳定版，目前为 `1.0.2`：

```bash
mkdir -p "$HOME/smartai"
cd "$HOME/smartai"
curl -fL https://github.com/joysun99/smartai-runtime/releases/download/smartai-cli-index/install.sh -o install.sh
bash install.sh
./smartai daemon start
```

升级前先在原目录执行 `./smartai daemon stop`。可用 `bash install.sh --version 1.0.2` 指定版本，`--install-dir DIR` 指定目录，`-i` 交互确认，`--list-versions` 查看可用版本，`--release-url URL` 指定发布来源。安装器核对归档及二进制摘要，升级只保留紧邻上版备份；模型和运行数据独立保存。

CLI 1.0.2 修复旧 `demo-*` 完成任务导致的 daemon 启动失败。主配置可读 version 2/3/4/5，修改保存后升级为 6；旧 CLI 无法读取 version 6。首次从 1.0.1 升级须重新下载上方新版脚本，之后可使用 `./smartai update` 检测更新。

`install.ps1` 保留供后续 Windows 版本使用，当前稳定目录没有 Windows 程序条目。CLI 免费使用条款、免责声明和第三方 Go 通知随程序包提供。

## Web Console 和服务管理

启动 daemon 后，默认访问 `http://127.0.0.1:18082/`。服务器上可通过 SSH 转发访问，例如：

```bash
ssh -L 8888:127.0.0.1:18082 user@server
```

随后访问 `http://127.0.0.1:8888/`；本地映射端口可自行选择。HTTPS 反向代理支持根路径与子路径，需配置 `services.webconsole.public_url`，代理保留 Host、Origin 和路径前缀；详见[控制台访问说明](docs/console-access.md)。

- 资源中心：runtime 按发布版本、Models 按 ASR/LLM/TTS/VISION 折叠显示；显式预览并确认下载，空闲资源可卸载，历史任务默认折叠。
- 服务概览：默认只显示服务标题和状态，展开后选择已登记资源组合并启停；资源与连接也可折叠。Vision 四项能力独立管理。
- 服务配置：资源中心底部保存图标登记多组组合，最近保存为默认；自启开关独立控制下次启动，不改变当前实例。
- 设置：模型下载源、推理 API 监听地址和鉴权策略、多个 API Key 及有效期、支持的 API endpoints；控制台登录 Key 由 CLI 管理。
- CLI：`smartai update` 检测当前平台最新正式版，支持 `--include-prereleases` 和 `--json`，只查询、不替换程序；无需 GitHub 登录。`smartai console endpoints` 查看接口，`smartai daemon status` 显示有序的服务及 Vision 状态。推理 API 默认回环监听 `127.0.0.1:18080`。

## 安装运行包和模型

Web Console 资源中心刷新在线目录，选择 `1.0.1` 运行包和所需模型，预览后确认下载。下载不会自动启动推理；安装后保存完整资源组合，在服务概览中显式启动；自启开关只控制下次启动。也可使用：

```bash
./smartai runtime catalog --remote
./smartai runtime install whisper --backend cpu
./smartai model pull whisper-tiny-q5_1
```

1.0.1 CPU 组合包括 llama.cpp b11878、Whisper v1.9.5、Kokoro voices / sherpa 2.0.0 / ORT 1.28.2、FFmpeg 7.1.5、Vision v0.1.0。静态校验或入口检查通过不代表模型已加载，启动显示 ready 后才能推理。

可选模型包括 Whisper tiny/base/small、Qwen3-0.6B/4B、Kokoro v1.1 FP32/INT8 和三个 Vision 组合。Kokoro v1.1 提供女声 `zf_079`、男声 `zm_009`；旧 v1.0 停止新启用，新音频人工试听仍待确认。模型按固定快照、大小和摘要下载，已有安装不会被目录刷新静默升级。

## 下载索引与源码材料

- [smartai-cli-index](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-cli-index)：安装脚本、`cli-index.tsv`、CLI `versions.json`。
- [smartai-runtime-index](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-runtime-index)：稳定目录 `catalog-v3.json`、完整目录 `catalog-all.json`、runtime `versions.json`。
- 三个自有 Vision 小描述按 ID 和 SHA-256 固定在共享 runtime 索引，含 Vision 的 runtime Release 同时提供原件；权重及归属文件从固定上游下载。清理 runtime 版本不会删除共享描述。
- `retired-versions.json` 记录已撤回版本；已撤回版本号不能重新发布，旧附件不再下载。
- 每个 runtime Release 的 `SOURCES.md`、`source-origins.json`、包内 `licenses/` 和独立 worker / 对应源码附件提供适用来源与许可材料。CLI 保持私有不影响这些独立材料的提供。

**GitHub 自动显示的 `Source code (zip)` / `Source code (tar.gz)` 只是本公开仓库在标签处的快照，不包含 Release 的 Assets，也不是 CLI 安装包或私有源码，无需下载。** JSON 索引请直接下载相应 Assets；worker 及对应源码使用单独命名的附件。自动源码链接由 GitHub 生成，不能像上传附件一样单独删除。

仓库中的 `source-catalog.json` 保留早期候选快照，不能作为当前安装 feed。当前可下载版本以以上 Release 索引为准。
