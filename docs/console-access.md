# 控制台访问与 API 设置

本文适用于 CLI `0.4.0-alpha.7` 及更新版本，当前建议 `0.4.0-alpha.9`；旧 alpha.6 尚无设置菜单和多 Key 管理。默认 API、管理、控制台分别监听 `127.0.0.1:18080/18081/18082`，推理服务不会因访问网页而自动下载或启动。

## Runtime 与 Models

资源中心将 **Runtime 运行包**、**Models 模型**分别展示。先刷新运行包目录，再预览并明确确认安装；关闭页面不取消 daemon 持有的任务。安装完成后，在“用已安装资源准备服务”中选择模型、对应引擎运行包，以及语音服务所需的 FFmpeg，再启动当前实例或保存自启配置。

正式目录没有 alpha/beta/rc 包。勾选“包含预发布运行包”后刷新，会显式查询配置目录同源的 `catalog-all.json`；不会升级已安装版本或改写既有计划。CLI 等效命令：

```bash
smartai resource refresh --include-prereleases
smartai resource status
```

自定义目录只有约定的 `catalog-v3.json`/`catalog-all.json` 文件名才提供切换入口；其他目录通过 CLI 配置完整目录 URL。旧 alpha.6 可先设置 `download.runtime_catalog` 为 `https://github.com/joysun99/smartai-runtime/releases/download/smartai-runtime-index/catalog-all.json`，等待下载完成后重启并刷新。空目录不再等同于“没有安装功能”。

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

`SMARTAI_API_KEY` 等选定环境变量仍可提供独立运维推理凭据；页面不显示其内容，也不管理该环境变量。主配置升级为 version 3：可读取 version 2，但修改配置或创建 Key 时原子写入 version 3；旧 CLI 会拒绝新配置，避免忽略 Key 存储。新 Key 文件各自使用 schema 1。不要手动降低配置版本并混用旧二进制。

## 开放局域网 API

默认仍为本机监听。先创建推理 Key，再在“设置”保存指定网卡 IP 或 `0.0.0.0:18080`。CLI 等效操作：

```bash
smartai console status
smartai console listen 0.0.0.0:18080
# 等待下载结束，再重启；保存的 enabled 服务会按配置恢复。
smartai daemon stop
smartai daemon start
```

监听修改在下次启动生效；页面分别显示当前地址、保存地址和重启提示。如当前监听受环境变量覆盖，界面单独提示；下次启动仍提供覆盖时优先使用该值。缺少有效 Key 时不能保存非回环监听；非回环启动也重新校验凭据。当前或已保存的非回环配置不能删除最后一个有效推理 Key；全部过期后可通过 CLI 创建新 Key，再启动。客户端使用 `http://<服务器IP>:18080/v1` 和 `Authorization: Bearer <推理Key>`，只按部署需要开放 API 端口，不开放管理或 worker 端口。

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

在运行 daemon 的同一用户、相同配置和数据目录执行 `smartai --json runtime check <完整ID>`。换用 root 会读取另一套默认登记，可能显示“资源未登记”。当报告为预期 glibc 2.38、实际 2.36 时，alpha.7 的相关 Linux CPU 二进制不能使用；请安装 alpha.8 新 CPU 包并在服务中选择新 ID，复用原模型。修复包通过实际 2.36 用户态检查，不要求用户替换系统 libc。

生命周期和结构化请求日志默认启用。例如：

```bash
smartai service logs asr --lines 50 --follow
smartai --json config show
```

第二条用于核对实际数据目录；日志位于其中的 `daemon/daemon.log` 和 `daemon/requests.jsonl`。默认不记录用户文本、原始音频或 Key。当前 `observability.log_level` 字段尚未控制日志过滤，设为 `debug` 不会额外开启原生引擎输出。


## 安装器的滚动备份

alpha.9 安装器默认以当前程序覆盖上版备份，只保留一份 `smartai.previous` / `smartai.previous.exe`，继续使用本次已经下载并校验的归档安装。同版本同摘要复装保留现有备份；运行中的程序、未知安装归属、损坏包以及备份链接/目录仍拒绝替换。

如本地 `install.sh` 提示“已有上版备份，未覆盖”，先更新脚本。以下仍安装 alpha.8，脚本和目标 CLI 版本可以分别选择：

```bash
curl -fL https://github.com/joysun99/smartai-runtime/releases/download/smartai-cli-index/install.sh -o install.sh
bash install.sh --version 0.4.0-alpha.8
```

Windows 使用同一索引入口的 `install.ps1`，旧固定 Release 的附件不替换。旧脚本失败退出时已删除临时归档，因此首次重试仍需下载一次；新脚本不会再因已有普通备份中断升级。
