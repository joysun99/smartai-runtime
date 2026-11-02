# smartai-runtime

smartai CLI 和原生运行包的公开分发仓库。CLI 第一方源码暂不公开；运行包和适用的 worker / 第三方对应源码通过 GitHub Release 提供。模型权重从固定上游地址下载，不放入 runtime 包。

## 当前稳定版本

| 对象 | 版本 | 当前范围 | 下载 |
| --- | --- | --- | --- |
| smartai CLI | `1.0.3` | Linux/WSL amd64，含 Web Console | [CLI Release](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-v1.0.3) |
| runtimes | `1.0.1` | Linux/WSL amd64 CPU：LLM、ASR、TTS、FFmpeg、Vision | [runtime Release](https://github.com/joysun99/smartai-runtime/releases/tag/runtimes-v1.0.1) |

两类从 `1.0.1` 统一发布，旧版 Release 和附件已撤回；已安装的模型、运行包及配置不受远端撤回操作影响。当前优先完善 Linux/WSL CPU；Linux CUDA、Windows CPU、Windows CUDA 后续依次交付。当前没有 Windows/CUDA 下载；CLI 与 runtime 版本独立；稳定运行包继续1.0.1，另有下方Vision CPU RC供显式试用。

运行包最低 CLI 为 `1.0.1`；具体 CPU 指令、系统库和依赖要求见各包 manifest。Linux 使用 glibc 2.36 基线；已完成本机 Linux/WSL CPU 的精确包及固定模型验证，其他环境和广泛质量需分别验收。

## 新语音候选预发布

| 对象 | 版本 | 下载与说明 |
| --- | --- | --- |
| CLI | `1.1.0-rc.6` | [Release、独立安装与回退](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-v1.1.0-rc.6) |
| Fun-ASR-Nano / ZipVoice-Distill CPU runtimes | `1.0.3-rc.4` | [两包、模型准备与适用源码](https://github.com/joysun99/smartai-runtime/releases/tag/runtimes-v1.0.3-rc.4)；最低CLI rc.6 |

仅Linux/WSL amd64 CPU，glibc>=2.36、AVX2/FMA/F16C。默认稳定CLI1.0.3/runtime1.0.1和Whisper/Kokoro推荐保持；已有模型/runtime绑定不会自动改变。

```bash
curl -fL https://github.com/joysun99/smartai-runtime/releases/download/smartai-v1.1.0-rc.6/install.sh -o install-smartai-rc.sh
bash install-smartai-rc.sh --version 1.1.0-rc.6 --install-dir "$PWD/smartai-rc6/bin"
./smartai-rc6/bin/smartai --config "$PWD/smartai-rc6/config.yaml" --data-dir "$PWD/smartai-rc6/data" init
```

以下`smartai`指新版CLI，使用所需的专用配置/数据参数。新引擎采用[显式候选目录](https://github.com/joysun99/smartai-runtime/releases/download/smartai-runtime-index/catalog-speech.json)，包含旧普通运行包和原推荐；原catalog-all/catalog-v3保留旧CLI可读取的引擎，避免未知service破坏整个目录。

```bash
smartai runtime install smartai-funasr-nano-v2-ort1.28.2-1.0.3-rc.4-linux-amd64-cpu --catalog https://github.com/joysun99/smartai-runtime/releases/download/smartai-runtime-index/catalog-speech.json
smartai runtime install smartai-zipvoice-distill-v2-ort1.28.2-1.0.3-rc.4-linux-amd64-cpu --catalog https://github.com/joysun99/smartai-runtime/releases/download/smartai-runtime-index/catalog-speech.json
smartai model pull fun-asr-nano-2512-int8
```

Web资源中心使用新版CLI显式设置 `download.runtime_catalog` 为候选目录并重启该实例；自定义目录已含候选，无需另勾预发布。Nano当前支持auto/zh/en、JSON/text；ZipVoice为固定参考音色`zipvoice_reference`，完整七文件模型需离线导入，资源来源/摘要和方法见runtime Release，不提供虚构HF地址或任意上传克隆。语音服务还需固定FFmpeg CPU包，可沿用已安装1.0.1。1～3显式副本按Nano每副本4GiB/ZipVoice每副本2GiB保守准入，预算不是内存预留。

CLI同时新增可选Whisper large-v3 Q5_0、Qwen3.5-2B/4B候选和思考开关；Qwen3仍推荐，两档3.5默认关闭思考，思考可能耗尽token预算而无最终答案。新语音功能、安装、取消恢复和glibc2.36实际加载已本机验证；新模型准确率及新音频人工试听仍待进行。保持旧ASR/LLM/OCR质量限制和多平台/新输入/其它浏览器/托管CI等暂缓范围，不将技术成功当质量通过。

建议独立程序、配置和数据目录；并行运行需空闲端口。回退先停止新版实例并恢复原配置，不用旧程序回写新的配置version7或模型报告schema7。旧RC和附件继续保留，未转为正式版。

## 既有 CPU 预发布 RC（继续保留）

| 对象 | RC 版本 | 范围与下载 |
| --- | --- | --- |
| smartai CLI | `1.1.0-rc.3` | Linux/WSL amd64；[发布说明、安装与回退](https://github.com/joysun99/smartai-runtime/releases/tag/smartai-v1.1.0-rc.3) |
| Vision CPU runtime | `1.0.2-rc.3` | **仅Vision**；[运行包与适用源码](https://github.com/joysun99/smartai-runtime/releases/tag/runtimes-v1.0.2-rc.3)；其它四项CPU运行包继续1.0.1 |

RC 不替换最新正式版或默认推荐；默认安装/更新仍选择 CLI1.0.3，稳定 runtime 目录和推荐仍1.0.1。显式安装RC：

```bash
curl -fL https://github.com/joysun99/smartai-runtime/releases/download/smartai-v1.1.0-rc.3/install.sh -o install-smartai-rc.sh
bash install-smartai-rc.sh --version 1.1.0-rc.3 --install-dir "$PWD/smartai-rc/bin"
./smartai-rc/bin/smartai --config "$PWD/smartai-rc/config.yaml" --data-dir "$PWD/smartai-rc/data" init
```

建议独立prefix/config/data；如与稳定实例同时运行，启动前设置空闲端口。新Vision包在完整目录中显式选择：

```bash
./smartai-rc/bin/smartai --config "$PWD/smartai-rc/config.yaml" --data-dir "$PWD/smartai-rc/data" runtime install smartai-vision-v0.1.0-1.0.2-rc.3-linux-amd64-cpu --catalog https://github.com/joysun99/smartai-runtime/releases/download/smartai-runtime-index/catalog-all.json
```

RC新增基本调用CLI、已保存资源配置管理，以及每项Vision能力的线程/队列和1～3显式副本。默认2线程/1副本/2等待；副本独立加载同一模型，资源不足明确拒绝。OCR同行片段排序已修复，字形/空格等模型问题仍保留。新容量入口需CLI1.1.0-rc.3；旧CLI会拒绝version6中的新capacity字段。回退先停止RC实例，再恢复原稳定程序及原配置/数据，不用旧CLI回写新配置，不删除资产或事务。

本轮有完整本地回归、精确glibc2.36用户态四能力推理和CPU2/3副本证据；广泛质量仍部分。ASR/LLM/OCR已知限制随版说明，原人工判定不合并或继承。当前版本的多平台交付/验收、新真实输入、其它浏览器、托管CI和OS隔离继续暂缓。本次不发布SenseVoice原生包/FP32模型或扩展模型许可。

## 安装 CLI

在希望安装的目录获取最新脚本；默认安装脚本所在目录的最新稳定版，目前为 `1.0.3`：

```bash
mkdir -p "$HOME/smartai"
cd "$HOME/smartai"
curl -fL https://github.com/joysun99/smartai-runtime/releases/download/smartai-cli-index/install.sh -o install.sh
bash install.sh
./smartai daemon start
```

升级前先在原目录执行 `./smartai daemon stop`。可用 `bash install.sh --version 1.0.3` 指定版本，`--install-dir DIR` 指定目录，`-i` 交互确认，`--list-versions` 查看可用版本，`--release-url URL` 指定发布来源。安装器核对归档及二进制摘要，升级只保留紧邻上版备份；模型和运行数据独立保存。

CLI 1.0.3 修复 Vision 下载模型卸载后重装的 `revision_unavailable` / HTTP404：保留原计划和摘要，重新预览并确认即可，HF 来源无需更改。运行包和模型版本保持不变。

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
