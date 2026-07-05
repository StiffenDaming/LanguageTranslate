import argparse
import os
import sys
import traceback

# 确保能导入 svc_integration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from svc_integration import SvcIntegrator, resample_single

# 全局单例
_svc_instance = None

def get_svc_instance(model_path, config_path, cluster_path="", target_sr=44100):
    global _svc_instance
    if _svc_instance is None:
        print(f"[CLI] Initializing model...")
        _svc_instance = SvcIntegrator(
            model_path=model_path,
            config_path=config_path,
            cluster_model_path=cluster_path,
            target_sr=target_sr
        )
    return _svc_instance

def main():
    parser = argparse.ArgumentParser(
        description="So-VITS-SVC 声音转换 CLI 工具",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # 必须参数
    parser.add_argument("--input", "-i", required=True, help="输入原始音频路径 (.wav)")
    parser.add_argument("--output", "-o", required=True, help="输出转换后音频路径 (.wav)")
    parser.add_argument("--speaker", "-s", required=True, help="目标说话人名称 (在 config.json 中定义)")
    
    # =========================================================
    # 【关键修改】模型配置：默认从 exe/脚本 同级目录查找
    # =========================================================
    # 获取 exe 或脚本所在的目录
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的环境
        base_dir = sys._MEIPASS
    else:
        # 开发环境
        base_dir = SCRIPT_DIR

    # 默认路径：同级目录下的 model 文件夹和 config.json
    default_model = os.path.join(base_dir, "model", "G_28450.pth")
    default_config = os.path.join(base_dir, "config.json")
    
    parser.add_argument("--model", 
                        default=default_model,
                        help="模型文件路径 (.pth)")
    parser.add_argument("--config", 
                        default=default_config,
                        help="配置文件路径 (config.json)")
    parser.add_argument("--cluster", default="", help="聚类模型路径 (可选)")
    # =========================================================
    
    # 转换参数
    parser.add_argument("--tran", "-t", type=int, default=0, 
                        help="音调调整 (半音数, +升调 -降调, 默认: 0)")
    parser.add_argument("--slice-db", type=int, default=-40, 
                        help="静音切片阈值 (dB, 默认: -40)")
    parser.add_argument("--pad-seconds", type=float, default=0.5, 
                        help="切片前后填充秒数 (默认: 0.5)")
    
    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"[CLI] Error: 输入文件不存在: {args.input}", file=sys.stderr)
        return 1

    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    # 定义临时重采样文件路径
    temp_dir = os.path.dirname(os.path.abspath(args.output))
    resampled_path = os.path.join(temp_dir, f".temp_resampled_{os.getpid()}.wav")

    try:
        print(f"[CLI] Starting conversion...")
        print(f"[CLI] Input: {args.input}")
        print(f"[CLI] Output: {args.output}")
        print(f"[CLI] Speaker: {args.speaker}")
        print(f"[CLI] Model: {args.model}")
        print(f"[CLI] Config: {args.config}")

        # 1. 初始化模型
        svc = get_svc_instance(
            model_path=args.model,
            config_path=args.config,
            cluster_path=args.cluster
        )

        # 2. 重采样预处理
        print(f"[CLI] Step 1/2: Resampling...")
        resample_single(
            input_wav_path=args.input,
            output_wav_path=resampled_path,
            target_sr=44100
        )

        # 3. 声音转换
        print(f"[CLI] Step 2/2: Converting voice...")
        svc.convert_voice(
            input_audio_path=resampled_path,
            output_audio_path=args.output,
            speaker_name=args.speaker,
            tran=args.tran,
            slice_db=args.slice_db,
            pad_seconds=args.pad_seconds
        )

        print(f"[CLI] Success! Output saved to: {args.output}")
        return 0

    except Exception as e:
        print(f"[CLI] Error: {str(e)}", file=sys.stderr)
        print(f"[CLI] Traceback:\n{traceback.format_exc()}", file=sys.stderr)
        return 1
    finally:
        # 清理临时文件
        if os.path.exists(resampled_path):
            try:
                os.remove(resampled_path)
                print(f"[CLI] Cleaned up temp file: {resampled_path}")
            except Exception as e:
                print(f"[CLI] Warning: Failed to delete temp file: {e}", file=sys.stderr)

if __name__ == "__main__":
    sys.exit(main())