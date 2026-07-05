# resample_single.py
import argparse
import os
import librosa
import numpy as np
from scipy.io import wavfile

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

def process_single_file(input_path, output_path, target_sr=44100):
    """处理单个WAV文件，覆盖输出"""
    if not os.path.exists(input_path):
        print(f"[ERROR] File not found: {input_path}")
        return False
    
    try:
        print(f"[INFO] Loading: {input_path}")
        wav, sr = load_wav(input_path)
        
        print(f"[INFO] Trimming silence...")
        wav, _ = trim_wav(wav)
        
        print(f"[INFO] Normalizing peak...")
        wav = normalize_peak(wav)
        
        print(f"[INFO] Resampling from {sr}Hz to {target_sr}Hz...")
        resampled_wav = resample_wav(wav, sr, target_sr)
        
        # 响度归一化
        resampled_wav /= np.max(np.abs(resampled_wav))
        
        print(f"[INFO] Saving (overwriting): {output_path}")
        save_wav_to_path(resampled_wav, output_path, target_sr)
        
        print(f"[SUCCESS] Done!")
        return True
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Input WAV path")
    parser.add_argument("--output", type=str, required=True, help="Output WAV path (overwrite)")
    parser.add_argument("--sr", type=int, default=44100, help="Target sample rate")
    args = parser.parse_args()

    success = process_single_file(args.input, args.output, args.sr)
    exit(0 if success else 1)