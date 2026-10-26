# smartai-runtime 协作约定

本仓库保存 smartai 原生运行时的固定候选身份、发布工具与分发记录。模型权重和用户数据不属于本仓库。

- 每个候选保留不可变的 ID、归档大小、归档 SHA-256 和包内 `runtime.json` SHA-256。重新打包必须使用新身份或明确记录替换原因，不能让既有下载链接悄悄指向不同字节。
- 大归档使用 GitHub Release 附件；不要把归档提交到普通 Git 或 Git LFS。不要提交代理、Token、OpenObserve 凭据或私有模型。
- `source-catalog.json` 是源项目的候选快照，不是在线安装 feed。只在附件全部上传、摘要复核及独立 HTTP 下载验证后发布相应 `catalog.json`，并更新 README 状态。
- 发布前核对每个包的再分发材料。许可文件存在不等于完成源码/构建选项、NVIDIA 再分发条件和第三方声明审查。未通过时保持候选状态。
- 写明已验证的平台及范围；不要把 WSL 的 CPU/CUDA 结果扩写为 Windows、Vulkan 或其他 Linux 环境已通过。Git 操作仅针对本仓库，保留用户现有修改。
