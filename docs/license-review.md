# 再分发材料审查

状态：**待完成**。当前包的本地功能验证及许可文本清单不能替代公开二进制再分发审查。审查结果须按具体归档摘要记录，而不是仅按上游项目名称概括。

| 包 | 已有材料 | 发布前待核对 |
| --- | --- | --- |
| llama CPU/CUDA、Whisper CPU/CUDA | 包内上游许可证与 Debian 组件版权文件 | 具体构建选项、源代码/变更及第三方库义务；CUDA 包中的 NVIDIA 文件清单与版本对应再分发条款 |
| Kokoro 常驻 worker CPU/CUDA | 包内 sherpa-onnx、ONNX Runtime、eSpeak、Go 与第三方声明；包含正式 worker 和旧探针 | 静态 eSpeak GPL-3.0-or-later 的完整对应源码和构建配方、组合程序的许可兼容性；worker/探针源码的公开许可；CUDA 包中的 NVIDIA/ONNX Runtime 条款 |
| FFmpeg CPU | 包内 Debian 组件版权文件；已读取二进制报告的构建选项 | 完整依赖闭包、相应源码与修改/构建方式及逐项许可核对 |
| Collector CPU | 官方归档摘要、上游 README、[固定标签的 Apache 2.0 文本](../licenses/README.md)、经摘要核对的官方 SPDX 2.3 SBOM | 核对二进制中第三方模块的许可证与声明文本，并决定随 Release 提供材料的方式；当前包装归档无 `licenses/` 文件 |

## Kokoro 原生库对应源码勘误

两个 TTS 候选包的 `runtime.json` 将 eSpeak NG 静态依赖标为 `GPL-3.0-or-later`，并记录提交 `ed530aa113046142eb5115cf2fc9157854d0ffe1`。但 [sherpa-onnx v1.13.8 的 Piper 下载配方](https://github.com/k2-fsa/sherpa-onnx/blob/v1.13.8/cmake/piper-phonemize.cmake)引用的 [Piper 源码](https://github.com/csukuangfj/piper-phonemize/blob/f3ff95afc03640bc1399e113e83361192a2fafb4/CMakeLists.txt)默认指向另一个 eSpeak NG 提交 `7251208ee427ef87e94f39d0e99b15d287224ed6`，且允许使用外部构建树。无法仅凭这些资料证明两个上游 Linux 预编译库实际包含哪个提交。原有提交号应视为**未核实的来源声明**；在取得对应构建证明或自行重建、复验并提供完整源码材料前，两包继续保持未发布。

上游 [v2.0.0 移除 eSpeak 的迁移说明](https://github.com/k2-fsa/sherpa-onnx/issues/3731)提供未来替代路线，但当前 smartai 的 Kokoro 文本前端和试听尚未按新版重新验收。

## FFmpeg 构建选项初核

候选包中 `ffmpeg -version` 报告版本 `7.1.5-0+deb13u1`，构建选项包含 `--enable-gpl`、`--enable-libx264`、`--enable-libx265`、`--enable-libxvid` 和 `--enable-shared`；未出现 `--enable-nonfree`。这只是二进制自报的配置，不能代替对包内全部 Debian 库、具体源码与版权文件的核对，也不能由“未出现 nonfree”推断整包已经符合再分发条件。

## CUDA 运行库文件复核

先前的三个 CUDA 包合计包含 18 处 NVIDIA 运行库实文件，涉及 12 个不同文件；旧打包器曾对这些 `.so` 设置 RPATH，使包内字节与上游原件不同。当前源清单已换成新身份的候选包，所有 18 处文件均保留固定上游组件的原始字节；新包在 Linux/WSL amd64 上分别通过 LLM、ASR、TTS 的 CUDA 实际推理验证。旧包不得用作公开附件。

[CUDA 12.8 EULA](https://docs.nvidia.com/cuda/archive/12.8.0/eula/index.html) 的附件 A 列出相关 Linux 库名，其 Linux 再分发条款要求目标代码不被修改。[cuDNN 9.10.2 协议](https://docs.nvidia.com/deeplearning/cudnn/backend/v9.10.2/reference/eula.html)另行规定运行时 `.so` 的分发范围。保留原始字节只解决文件修改这一项；应用分发条件、声明交付及与其他组件的许可关系仍待审查。三个新 CUDA 归档继续保持未发布。

## Collector 官方 SBOM 核对

官方 v0.150.1 Release 为 `otelcol-contrib_0.150.1_linux_amd64.tar.gz` 提供[同名 SPDX 2.3 SBOM](https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.150.1/otelcol-contrib_0.150.1_linux_amd64.tar.gz.sbom.json)，SHA-256 为 `0cb68ab1ef984b9bd032abe230f73e7178adede4e7d5c6ff4714419585f21db9`。已核对 smartai 包内二进制的 Go 构建信息：1,019 个依赖全部与 SBOM 包名及版本匹配；SBOM 共列 1,022 个包，额外三项分别是主模块、Go 标准库和官方归档。四项 `licenseConcluded` 为 `NOASSERTION`，其中一项是第三方 Go 依赖；1,021 项 `licenseDeclared` 为 `NOASSERTION`。

这份 SBOM 提供依赖及部分许可证识别线索，不能代替逐项核对许可证、版权声明和再分发交付材料。完成审查前，Collector 归档仍为未发布候选。

参考上游：[GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.en.html)、[FFmpeg 法律说明](https://ffmpeg.org/legal.html)、[CUDA 12.8 EULA](https://docs.nvidia.com/cuda/archive/12.8.0/eula/index.html)、[OpenTelemetry Collector 发行仓库](https://github.com/open-telemetry/opentelemetry-collector-releases)。这些资料用于逐项核对，不代表已得出发布许可结论。审查完成后应列出所提供的源码、声明及每个归档的批准人、日期和摘要。
