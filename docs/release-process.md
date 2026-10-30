# 候选运行时发布流程

> 本文记录旧 `source-catalog.json` 候选的流程；这些候选仍未发布。当前已公开版本以仓库 [README](../README.md) 为准。新版本以独立 CLI / runtimes Release 和各自版本索引发布，不能把本文的旧候选摘要当作新附件。

当前仓库只保存固定候选身份；8 个归档尚未成为公开 Release 附件。`source-catalog.json` 记录五个引擎/FFmpeg 包、两个 Kokoro 常驻 worker 包和一个 Collector 包的固定摘要。TTS 候选具备正式 worker 入口；探针专用包不进入在线推荐。归档来源目录由发布者显式指定，不属于公开仓库内容。

## 布局与准备

计划使用一个固定标签的 GitHub Release：8 个 `.tar.gz` 附件、`catalog.json`、`SHA256SUMS`、`release-inventory.json`。目录 schema 2 的 `archive_url` 指向固定标签的附件 URL，不使用会变化的 `latest`。模型文件不会进入附件。GitHub 普通 Git 拒绝超过 100 MiB 的文件，而本批最大归档约 1.85 GB；Release 单附件须小于 2 GiB，所以归档只放 Release 附件。仓库保留清单、校验脚本与审查记录，不使用 Git LFS。

准备元数据时，设置 `SMARTAI_RELEASE_TAG`、`SMARTAI_M0_ARCHIVES`、`SMARTAI_TTS_ARCHIVES`、`SMARTAI_CUDA_ARCHIVES`、`SMARTAI_COLLECTOR_ARCHIVES`。CUDA 候选从独立目录读取，避免误用已废弃的旧 CUDA 归档：

```bash
python3 scripts/prepare-release.py \
  --tag "$SMARTAI_RELEASE_TAG" \
  --m0-dir "$SMARTAI_M0_ARCHIVES" \
  --tts-dir "$SMARTAI_TTS_ARCHIVES" \
  --cuda-dir "$SMARTAI_CUDA_ARCHIVES" \
  --collector-dir "$SMARTAI_COLLECTOR_ARCHIVES" \
  --output ".staging/$SMARTAI_RELEASE_TAG"
```

脚本对源候选清单、每个归档的大小与 SHA-256、包内清单和文件/链接身份做独立检查。成功后只在忽略的 `.staging/` 写三个发布元数据文件，不复制多 GiB 归档；归档原文件保持原样。另生成只供本地上传使用、不得作为附件发布的 `upload-sources.json`。已有输出目录会被拒绝。

## 发布准入

1. 逐包完成 [许可审查](license-review.md)，补齐对应源码、构建配方、声明和 NVIDIA 许可条件。Collector 包没有随附许可证文本，需随同分发补足。审查完成前不上传归档。
2. 发布者须具备仓库写入权限，并通过 GitHub CLI 或 Web UI 创建草稿 Release。命令行工具可安装在用户目录，无需 sudo；登录凭据不得写入本仓库。
3. 以固定标签创建草稿并上传完全相同的 8 个归档与三个元数据文件。发布前从 GitHub API 读取每个附件 `size` 与 `digest`，和本地 `SHA256SUMS` 比对；任何失败均不发布该 Release。
4. 发布后在独立机器/网络完整下载并重新计算摘要，再使用干净 smartai 数据目录从实际 HTTPS `catalog.json` 安装、校验及执行必要的服务检查。记录平台、CLI 提交、结果与限制。随后才在 README 标记为可下载，并让 smartai 文档指向该 feed。

变更归档字节时新建标签。删除旧 Release 前核对其是否仍被 smartai 内嵌目录或用户安装计划引用；清理构建副本不影响已发布的固定链接。


## 当前两类发布的规则

CLI 与 runtime 组合分别测试、编译、打包、发布和清理；一个 runtime 组合可只覆盖指定平台和后端，不要求为其他平台重新编号。alpha.8 runtime 仅更新 Linux amd64 CPU，CUDA/Windows 沿用 alpha.7。每个附件和完整 runtime ID 不可变，历史发现目录由远端既有索引合并，不能从发布者本地保留的产物推断。

发布前核对固定源码、精确归档、平台/后端实际能力与模型结果及第三方材料。采用 glibc 2.36 sysroot 的 CPU 包，还必须具有精确归档在实际 2.36 用户态下通过的记录；仅在较新宿主成功或修改清单版本不满足门槛。对应 GCC 源码、Debian 补丁和源描述文件作为独立附件，原始名称、字节和摘要均保留。

固定版本先上传草稿，核对远端大小/摘要后公开，再匿名 HTTPS 完整下载每个附件。全部通过才更新 CLI 安装索引、runtime 版本列表及完整/稳定目录。源码或验证结果不齐全时拒绝隐式重建或跳过检查；中断后重试同版也不能覆盖已公开附件。清理本地可重建产物不删除远端版本、来源锁或审核原件。

新包使用对应源码提交时间统一归档和安装文件日期，保证重复打包一致；独立 CLI/runtime 标签可能对应不同提交，因此不要求两类对象时间相同。
