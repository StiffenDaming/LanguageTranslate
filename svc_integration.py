import os
import sys
import librosa
import numpy as np
import soundfile as sf
from scipy.io import wavfile
import torch


# 【关键修改】动态获取 so-vits-svc 路径
# =========================================================
if getattr(sys, 'frozen', False):
    # 如果是 PyInstaller 打包环境（虽然我们选了方案 B，但保留兼容）
    base_dir = sys._MEIPASS
else:
    # 开发环境/方案 B：获取脚本所在目录的上一级（或 exe 同级）
    # 尝试1：从 sys.argv[0] 获取 exe/脚本 路径
    try:
        app_path = os.path.abspath(sys.argv[0])
        base_dir = os.path.dirname(app_path)
    except:
        # 尝试2：从 __file__ 获取
        base_dir = os.path.dirname(os.path.abspath(__file__))

# 假设 so-vits-svc 文件夹在 exe/脚本 同级
SOVITS_ROOT = os.path.join(base_dir, "so-vits-svc")

# 校验路径
if not os.path.exists(SOVITS_ROOT):
    raise FileNotFoundError(f"找不到 so-vits-svc 文件夹！请确保它在程序同级目录下：{SOVITS_ROOT}")

# 切换目录并添加到路径
os.chdir(SOVITS_ROOT)
sys.path.insert(0, SOVITS_ROOT)
# =========================================================

# 现在导入 so-vits-svc 的模块
from inference.infer_tool import Svc

# --------------------------
# 1. 重采样模块（完全复用你的 resample.py 逻辑）
# --------------------------
def load_wav(wav_path):
    return librosa.load(wav_path, sr=None)

def trim_wav(wav, top_db=40):
    return librosa.effects.trim(wav, top_db=top_db)

def normalize_peak(wav, threshold=1.0):
    peak = np.abs(wav).max()
    if peak > threshold:
        wav = 0.98 * wav / peak
    return wav

def resample_wav(wav, sr, target_sr):
    return librosa.resample(wav, orig_sr=sr, target_sr=target_sr)

def save_wav_to_path(wav, save_path, sr):
    wavfile.write(
        save_path,
        sr,
        (wav * np.iinfo(np.int16).max).astype(np.int16)
    )

def resample_single(
    input_wav_path,
    output_wav_path,
    target_sr=44100,
    skip_loudnorm=False
):
    """单个音频文件的重采样预处理"""
    wav, sr = load_wav(input_wav_path)
    wav, _ = trim_wav(wav)
    wav = normalize_peak(wav)
    resampled_wav = resample_wav(wav, sr, target_sr)
    if not skip_loudnorm:
        resampled_wav /= np.max(np.abs(resampled_wav))
    os.makedirs(os.path.dirname(output_wav_path), exist_ok=True)
    save_wav_to_path(resampled_wav, output_wav_path, target_sr)
    print(f"[Resample] OK: {input_wav_path} -> {output_wav_path}")

# --------------------------
# 2. SVC 推理封装（核心！）
# --------------------------
class SvcIntegrator:
    def __init__(
        self,
        model_path,          # .pth 模型文件路径
        config_path,         # config.json 路径
        cluster_model_path="", # kmeans 模型路径（可选，没有则留空）
        device=None,         # 推理设备，默认自动选 cuda/cpu
        target_sr=44100      # 目标采样率，需与模型训练时一致
    ):
        self.target_sr = target_sr
        
        # 初始化模型
        print(f"[SVC] Loading model from {model_path}...")
        self.svc_model = Svc(
            net_g_path=model_path,
            config_path=config_path,
            cluster_model_path=cluster_model_path if cluster_model_path else "",
            device=device
        )
        print("[SVC] Model loaded successfully.")

    def convert_voice(
        self,
        input_audio_path,    # 输入音频路径（建议是经过 resample_single 处理后的）
        output_audio_path,   # 输出音频路径
        speaker_name,        # 目标说话人名称（在 config.json 的 spk 列表里）
        tran=0,              # 音调调整（半音数，+升调 -降调）
        slice_db=-40,        # 静音切片阈值（dB）
        cluster_infer_ratio=0, # 聚类推理比例（0-1，没有聚类模型则设为0）
        auto_predict_f0=False, # 自动预测音高（建议 False，用 tran 手动调）
        pad_seconds=0.5      # 切片前后填充秒数
    ):
        """
        执行声音转换（内部调用 slice_inference 处理长音频）
        """
        print(f"[SVC] Converting: {input_audio_path} -> Speaker: {speaker_name}")
        
        # 调用核心推理接口
        out_audio_np = self.svc_model.slice_inference(
            raw_audio_path=input_audio_path,
            spk=speaker_name,
            tran=tran,
            slice_db=slice_db,
            cluster_infer_ratio=cluster_infer_ratio,
            auto_predict_f0=auto_predict_f0,
            noice_scale=0.4,
            pad_seconds=pad_seconds,
            f0_predictor='pm', # 音高预测器：pm/crepe 等
            enhancer_adaptive_key=0,
            cr_threshold=0.05,
            k_step=100,
            use_spk_mix=False,
            second_encoding=False,
            loudness_envelope_adjustment=1
        )
        
        # 保存结果
        os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
        sf.write(output_audio_path, out_audio_np, self.target_sr)
        print(f"[SVC] Done: Saved to {output_audio_path}")

# --------------------------
# 3. 一键流程示例（如何调用）
# --------------------------
if __name__ == "__main__":
    # --- 配置路径（请修改为你自己的路径） ---
    MODEL_PATH = r"C:\Users\42969\so-vits-svc\logs\44k\G_28450.pth"
    CONFIG_PATH = r"C:\Users\42969\so-vits-svc\configs\config.json"
    CLUSTER_PATH = "" # 如果没有聚类模型，留空即可
    
    INPUT_RAW = r"F:\QtProject2\LanguageTranslate\audio\20260202180153.wav"     # 你的原始音频
    INPUT_RESAMPLED = r"F:\QtProject2\LanguageTranslate\temp\resampled.wav"# 重采样后的中间文件
    OUTPUT_FINAL = r"F:\QtProject2\LanguageTranslate\audio\svc\output_20260202180153.wav"   # 最终转换结果
    
    TARGET_SPEAKER = "myvoice"   # 换成你实际的说话人名称
    
    # --- 执行流程 ---
    # 1. 初始化模型（只需初始化一次）
    svc = SvcIntegrator(
        model_path=MODEL_PATH,
        config_path=CONFIG_PATH,
        cluster_model_path=CLUSTER_PATH,  # 直接传空字符串
        target_sr=44100
    )
    
    # 2. 先重采样预处理
    resample_single(
        input_wav_path=INPUT_RAW,
        output_wav_path=INPUT_RESAMPLED,
        target_sr=44100
    )
    
    # 3. 进行声音转换
    svc.convert_voice(
        input_audio_path=INPUT_RESAMPLED,
        output_audio_path=OUTPUT_FINAL,
        speaker_name=TARGET_SPEAKER,
        tran=0 # 如果音调不合适，修改这里，比如 +6 升6个半音
    )