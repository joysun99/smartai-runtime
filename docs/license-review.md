# 再分发材料审查

状态：**待完成**。当前包的本地功能验证及许可文本清单不能替代公开二进制再分发审查。审查结果须按具体归档摘要记录，而不是仅按上游项目名称概括。

| 包 | 已有材料 | 发布前待核对 |
| --- | --- | --- |
| llama CPU/CUDA、Whisper CPU/CUDA | 包内上游许可证与 Debian 组件版权文件 | 具体构建选项、源代码/变更及第三方库义务；CUDA 包中的 NVIDIA 文件清单与版本对应再分发条款 |
| Kokoro 常驻 worker CPU/CUDA | 包内 sherpa-onnx、ONNX Runtime、eSpeak、Go 与第三方声明；包含正式 worker 和旧探针 | 静态 eSpeak GPL-3.0-or-later 的完整对应源码和构建配方、组合程序的许可兼容性；worker/探针源码的公开许可；CUDA 包中的 NVIDIA/ONNX Runtime 条款 |
| FFmpeg CPU | 包内 Debian 组件版权文件 | 实际启用的 GPL/LGPL/非自由构建选项、完整依赖闭包、相应源码与修改/构建方式 |
| Collector CPU | 官方归档摘要、上游 README；本仓库已保存[固定标签的 Apache 2.0 文本](../licenses/README.md) | 核对二进制中第三方模块的许可证与声明，并决定随 Release 提供材料的方式；当前包装归档无 `licenses/` 文件 |

参考上游：[GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.en.html)、[FFmpeg 法律说明](https://ffmpeg.org/legal.html)、[CUDA 12.8 EULA](https://docs.nvidia.com/cuda/archive/12.8.0/eula/index.html)、[OpenTelemetry Collector 发行仓库](https://github.com/open-telemetry/opentelemetry-collector-releases)。这些资料用于逐项核对，不代表已得出发布许可结论。审查完成后应列出所提供的源码、声明及每个归档的批准人、日期和摘要。
