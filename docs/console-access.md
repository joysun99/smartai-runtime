# 控制台访问与 API 设置

本文适用于 CLI `1.0.3`（包含 1.0.2 功能）；运行包继续使用 `1.0.1`。默认 API、管理、控制台分别监听 `127.0.0.1:18080/18081/18082`，推理服务不会因访问网页而自动下载或启动。

## Runtime 与 Models

资源中心将 **Runtime 运行包**、**Models 模型**分别展示。先刷新运行包目录，再预览并明确确认安装；关闭页面不取消 daemon 持有的任务。安装完成后，在“用已安装资源准备服务”中选择模型、对应引擎运行包，以及语音服务所需的 FFmpeg，点击卡片底部保存图标登记组合，最近保存的一组成为默认；可保留多组，自启开关独立控制下次启动。到“服务概览”展开服务，默认选中默认组合，也可选其他组合后启停。概览服务与资源信息默认折叠，刷新保留展开状态和选择。

正式目录没有 alpha/beta/rc 包。勾选“包含预发布运行包”后刷新，会显式查询配置目录同源的 `catalog-all.json`；不会升级已安装版本或改写既有计划。CLI 等效命令：

```bash
smartai resource refresh --include-prereleases
smartai resource status
```

自定义目录只有约定的 `catalog-v3.json`/`catalog-all.json` 文件名才提供切换入口；其他目录通过 CLI 配置完整目录 URL。旧 alpha.6 可先设置 `download.runtime_catalog` 为 `https://github.com/joysun99/smartai-runtime/releases/download/smartai-runtime-index/catalog-all.json`，等待下载完成后重启并刷新。空目录不再等同于“没有安装功能”。

## 资源分组、任务与卸载

本节及下面的模型来源设置从 CLI `0.4.0-alpha.10` 起提供。

资源中心将 Runtime 按**运行包发布版本**分组，例如 `1.0.1` 下展示 llama、whisper、kokoro、ffmpeg，后端和引擎版本在卡片内单独标明。已安装版本即使未刷新在线目录，也从登记时固定摘要的清单读取版本；缺少可信版本信息的旧本地包单列。Models 按 ASR、LLM、TTS、Vision 分组；模型分类和 Runtime 版本组均可折叠。

“后台任务”默认展示执行中和排队任务；完成、失败、取消及中断任务收进“历史任务”，点击展开查看或显式恢复。刷新不会收起已展开的历史或重置服务选择。

已安装且未占用的资源可点击“卸载”；引用模式显示“移除登记”，保留外部原件。启动中、运行中、停止中的服务及安装任务会阻止卸载；共享 FFmpeg 被任一 ASR/TTS 服务使用时同样受保护。最终操作仍通过跨进程使用租约和原有删除事务检查，不能强制绕过。卸载保留缓存、固定版本绑定及服务配置；如配置仍指向已卸载资源，需重新安装原版或明确选择其他资源。

## 模型下载来源

在“设置 → 模型下载来源”选择 **Hugging Face** 或 **hf-mirror**，点击“保存模型来源”。保存后，新建的模型安装计划立即生效，无需重启；计划确认页显示实际来源。选择内置来源会同时清除原来保存的自定义 `download.endpoint`，其他下载配置不变。CLI 也可分别配置 `download.source` 和 `download.endpoint`，然后重启 daemon 读取变更。

已有计划、排队和执行中任务继续使用各自固定的来源和快照，重启恢复也不改源；失败不会自动切换。页面同时展示保存值和实际地址，如 `HF_ENDPOINT` / `SMARTAI_HF_ENDPOINT` 覆盖了保存值，会明确提示；移除环境覆盖后需重启 daemon。模型来源设置不影响 Runtime 的 GitHub 目录或下载源，也不扩大凭据允许域名。

资源任务日志 `resource-tasks/tasks.json` 从 schema 1/2 读取并写入 schema 3，新增固定模型来源；旧版 CLI 不识别该格式，不应混用或手动降低版本。旧任务仅在原下载计划能证明来源时恢复该来源，否则要求通过 CLI 指定原 endpoint 恢复，或重新预览并确认新计划，避免按当前默认值改投来源。资产索引仍为 schema 3，主配置版本见下文。

## SSH 任意本地端口

在客户端选择空闲端口；服务器仍监听回环地址：

```bash
LOCAL_PORT=19082
ssh -fNT -o ExitOnForwardFailure=yes \
  -L "127.0.0.1:${LOCAL_PORT}:127.0.0.1:18082" user@server
```

浏览器打开 `http://127.0.0.1:19082/`。本地端口可替换，不必等于服务器端口；也支持 `localhost` 和 IPv6 回环 Host。仍校验同源请求，不能通过任意域名或伪造转发头取得控制权。旧 alpha.6 需临时使用与服务器相同的本地端口，或升级后再使用不同端口。

## 两类 Key 与有效期

| 类型 | 默认有效期 | 管理入口 | 权限 |
| --- | --- | --- | --- |
| 推理 API Key | 90 天 | 设置页面、`console api-key` | 推理 API；不能登录控制台 |
| 控制台登录 Key | 365 天 | 仅 `console key` | 控制台管理；不能调用推理 API |

每类最多 64 个 Key。可选 1～3650 天，`--days 0` 表示永不过期。Key 以 SHA-256 摘要保存在数据目录 `auth/inference-keys.json` 或 `auth/console-keys.json`，完整值仅在创建结果中显示一次，不写入配置、列表或日志。重启后 Key 继续有效；网页会话最长 12 小时且不超过登录 Key 到期时间，daemon 重启需重新登录。到期或撤销立即阻止新请求；已鉴权推理不强制中断。首次创建推理 Key 后，即使全部删除也不会恢复匿名访问。

```bash
smartai console api-key create --name my-app --days 90
smartai console api-key list
smartai console api-key delete <推理Key的ID>
smartai console key create --name admin --days 365
smartai console key list
smartai console key delete <登录Key的ID>
```

命令在 daemon 运行和停止时都可使用；运行时走受保护的本机管理接口，停止时与 daemon 共用目录锁。登录 Key 的删除会使其网页会话同时失效；网页只显示无凭据元信息，没有创建或删除登录 Key 的接口。创建过登录 Key 后，本机/SSH 网页也要求登录，原先自动发放的本机会话失效；全部登录 Key 被撤销后通过 CLI 新建即可恢复访问。

`SMARTAI_API_KEY` 等选定环境变量仍可提供独立运维推理凭据；页面不显示其内容，也不管理该环境变量。CLI 1.0.2 主配置写 version 6，可读取 version 2/3/4/5，首次修改原子升级；旧 CLI 拒绝 version 6。新 Key 文件各自使用 schema 1。不要手动降低配置版本并混用旧二进制。

## 开放局域网 API

默认仍为本机监听。可直接在“设置”保存指定网卡 IP 或 `0.0.0.0:18080`，不受是否启用鉴权或有无 Key 影响。CLI 等效操作：

```bash
smartai console status
smartai console listen 0.0.0.0:18080
# 等待下载结束，再重启；保存的 enabled 服务会按配置恢复。
smartai daemon stop
smartai daemon start
```

监听地址与鉴权开关在下次启动生效，页面分别显示当前及保存值；环境覆盖仍按原优先级处理。保持鉴权时，非回环启动仍需有效 Key；尚无 Key 可先保存地址，页面提示重启前创建 Key。也可通过“停用 API KEY”或 `smartai console auth disable` 显式允许匿名推理；Key 保留，控制台和管理鉴权独立。重新启用校验前先创建有效 Key。

受保护的当前或保存非回环配置不能删除最后一个有效 Key。客户端启用鉴权时使用 `Authorization: Bearer <推理Key>`；显式停用时无需此头。设置的 endpoints 清单默认折叠，CLI 可用 `smartai console endpoints` 查看。推理端口与控制台转发端口不同。

## Nginx / Traefik HTTPS 代理

控制台本身保持回环监听。先创建登录 Key，再配置唯一外部 URL（须为 HTTPS、以 `/` 结尾），支持独立域名根路径和子路径及自定义端口：

```bash
smartai console key create --name admin --days 365
smartai config set services.webconsole.public_url https://console.example.com/smartai/
# 等待下载结束后，停止并重新启动 daemon。
```

代理必须保留原始 Host（含非默认端口）、Origin、路径前缀及 Cookie。smartai 根据明确配置的 URL 判断来源，不信任 `Forwarded`、`X-Forwarded-Host`、`X-Forwarded-Proto` 或 `X-Forwarded-Prefix` 来扩大访问权限。配置代理后，直接本机访问也必须登录，代理改写 Host 不能绕过登录。外部 Cookie 为 HttpOnly、Secure、SameSite=Strict，路径限制在配置前缀中。

Nginx：将以下内容放入已配置证书的 HTTPS `server` 块。`proxy_pass` 不附 URI，保留原路径；使用 `$http_host` 保留非默认端口。配置语义见 [Nginx 官方代理文档](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass)。

```nginx
location /smartai/ {
    proxy_pass http://127.0.0.1:18082;
    proxy_http_version 1.1;
    proxy_set_header Host $http_host;
    proxy_set_header Connection "";
    proxy_buffering off;
    proxy_read_timeout 420s;
    client_max_body_size 33m;
}
```

根路径部署将外部 URL 改为 `https://console.example.com/`，对应 `location /`。不要删除子路径前缀，也不需要改写 Cookie Path。

Traefik：以下为文件 provider 动态配置，假定 `websecure` 已配置 TLS，且代理运行在能访问宿主回环地址的网络环境；容器的 `127.0.0.1` 是容器自身。保留 `passHostHeader`，不使用 `StripPrefix`。参见 [Traefik 官方服务配置](https://doc.traefik.io/traefik/reference/routing-configuration/http/load-balancing/service/)。

```yaml
http:
  routers:
    smartai:
      rule: Host(`console.example.com`) && (Path(`/smartai`) || PathPrefix(`/smartai/`))
      entryPoints: [websecure]
      tls: {}
      service: smartai
  services:
    smartai:
      loadBalancer:
        passHostHeader: true
        servers:
          - url: http://127.0.0.1:18082
```

同一控制台当前只配置一个外部 URL。代理部署、证书和防火墙由部署方配置；本仓库的受控 HTTP 测试不等于用户真实 Nginx/Traefik 部署已验收。


## glibc 检查与日志

在运行 daemon 的同一用户、相同配置和数据目录执行 `smartai --json runtime check <完整ID>`。换用 root 会读取另一套默认登记，可能显示“资源未登记”。当前 runtime 1.0.1 Linux CPU 包采用 glibc 2.36 基线，具体要求以清单为准；历史较高基线包不能通过改清单绕过检查，应显式安装适合本机的新包并选择新 ID。

生命周期和结构化请求日志默认启用。例如：

```bash
smartai service logs asr --lines 50 --follow
smartai --json config show
```

第二条用于核对实际数据目录；日志位于其中的 `daemon/daemon.log` 和 `daemon/requests.jsonl`。默认不记录用户文本、原始音频或 Key。当前 `observability.log_level` 字段尚未控制日志过滤，设为 `debug` 不会额外开启原生引擎输出。


## 安装器的滚动备份

alpha.9 安装器默认以当前程序覆盖上版备份，只保留一份 `smartai.previous` / `smartai.previous.exe`，继续使用本次已经下载并校验的归档安装。同版本同摘要复装保留现有备份；运行中的程序、未知安装归属、损坏包以及备份链接/目录仍拒绝替换。

如本地 `install.sh` 提示“已有上版备份，未覆盖”，先更新脚本。更新脚本后指定 CLI 1.0.3：

```bash
curl -fL https://github.com/joysun99/smartai-runtime/releases/download/smartai-cli-index/install.sh -o install.sh
bash install.sh --version 1.0.3
```

Windows 使用同一索引入口的 `install.ps1`，旧固定 Release 的附件不替换。旧脚本失败退出时已删除临时归档，因此首次重试仍需下载一次；新脚本不会再因已有普通备份中断升级。


## 检测 CLI 更新

```bash
smartai update
smartai update --include-prereleases
smartai --json update
smartai update --no-proxy --timeout 30s
```

只查询当前平台的 CLI 索引，默认正式版，可用 `--release-url URL` 选择其他发布源。沿用下载代理，支持 `--proxy`；不需要 GitHub 登录，也不使用 HF Token。发现新版时显示对应安装脚本和指定版本安装方式，不下载程序包或启停服务。成功检测返回 0，JSON 中 `update_available` 表示是否有新版，开发版本无法比较时为 null；网络或索引错误返回非零，不自动换源。CLI 1.0.1 没有此命令，需先用新版安装脚本升级一次。


## Vision 模型卸载后重装报 HTTP404

CLI 1.0.2 的下载恢复路径遗漏了 Vision 多来源组合，卸载后重新预览 PP-OCRv5、AuraFace 等模型可能返回 `revision_unavailable`。升级到 CLI 1.0.3 后，重新预览并确认安装即可；保留现有 Hugging Face / hf-mirror 设置、固定下载计划和删除记录，无需清理数据或换成 main。恢复仍核对原完整文件身份和 SHA-256，runtime 1.0.1 无需重装。
