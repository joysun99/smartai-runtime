# 再分发材料审查

状态：**待完成**。当前包的本地功能验证及许可文本清单不能替代公开二进制再分发审查。审查结果须按具体归档摘要记录，而不是仅按上游项目名称概括。

| 包 | 已有材料 | 发布前待核对 |
| --- | --- | --- |
| llama CPU/CUDA、Whisper CPU/CUDA | 包内上游许可证与 Debian 组件版权文件 | 具体构建选项、源代码/变更及第三方库义务；CUDA 包中的 NVIDIA 文件清单与版本对应再分发条款 |
| Kokoro 常驻 worker CPU/CUDA | 包内 sherpa-onnx、ONNX Runtime、eSpeak、Go 与第三方声明；包含正式 worker 和旧探针 | 静态 eSpeak GPL-3.0-or-later 的完整对应源码和构建配方、组合程序的许可兼容性；worker/探针源码的公开许可；CUDA 包中的 NVIDIA/ONNX Runtime 条款 |
| FFmpeg CPU | 包内 Debian 组件版权文件 | 实际启用的 GPL/LGPL/非自由构建选项、完整依赖闭包、相应源码与修改/构建方式 |
| Collector CPU | 官方归档摘要、上游 README、[固定标签的 Apache 2.0 文本](../licenses/README.md)、经摘要核对的官方 SPDX 2.3 SBOM | 核对二进制中第三方模块的许可证与声明文本，并决定随 Release 提供材料的方式；当前包装归档无 `licenses/` 文件 |

## Collector 官方 SBOM 核对

官方 v0.150.1 Release 为 `otelcol-contrib_0.150.1_linux_amd64.tar.gz` 提供[同名 SPDX 2.3 SBOM](https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.150.1/otelcol-contrib_0.150.1_linux_amd64.tar.gz.sbom.json)，SHA-256 为 `0cb68ab1ef984b9bd032abe230f73e7178adede4e7d5c6ff4714419585f21db9`。已核对 smartai 包内二进制的 Go 构建信息：1,019 个依赖全部与 SBOM 包名及版本匹配；SBOM 共列 1,022 个包，额外三项分别是主模块、Go 标准库和官方归档。四项 `licenseConcluded` 为 `NOASSERTION`，其中一项是第三方 Go 依赖；1,021 项 `licenseDeclared` 为 `NOASSERTION`。

这份 SBOM 提供依赖及部分许可证识别线索，不能代替逐项核对许可证、版权声明和再分发交付材料。完成审查前，Collector 归档仍为未发布候选。

参考上游：[GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.en.html)、[FFmpeg 法律说明](https://ffmpeg.org/legal.html)、[CUDA 12.8 EULA](https://docs.nvidia.com/cuda/archive/12.8.0/eula/index.html)、[OpenTelemetry Collector 发行仓库](https://github.com/open-telemetry/opentelemetry-collector-releases)。这些资料用于逐项核对，不代表已得出发布许可结论。审查完成后应列出所提供的源码、声明及每个归档的批准人、日期和摘要。
