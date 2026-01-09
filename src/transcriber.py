"""
Whisper文字起こしモジュール

faster-whisperを使用したリアルタイム音声認識
"""

import numpy as np
from faster_whisper import WhisperModel


class Transcriber:
    """音声データをテキストに変換"""

    def __init__(
        self,
        model_size: str = "small",
        language: str = "ja",
        device: str = "auto",
    ):
        """
        Args:
            model_size: Whisperモデルサイズ (tiny, base, small, medium, large)
            language: 認識言語 (ja, en, auto)
            device: 推論デバイス (auto, cpu, cuda)
        """
        self.language = language if language != "auto" else None
        self.model_size = model_size

        print(f"Whisperモデル読み込み中: {model_size}...")

        # Apple Silicon最適化: compute_type="int8"で高速化
        # device="auto"でMetal/CPUを自動選択
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type="int8",
        )

        print("モデル読み込み完了")

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        """
        音声データを文字起こし

        Args:
            audio: 音声データ (numpy配列, float32, -1.0〜1.0)
            sample_rate: サンプルレート

        Returns:
            文字起こしテキスト
        """
        if len(audio) == 0:
            return ""

        # 音声データを正規化
        audio = audio.astype(np.float32)
        if audio.max() > 1.0 or audio.min() < -1.0:
            audio = audio / max(abs(audio.max()), abs(audio.min()))

        # 無音検出（閾値以下はスキップ）
        if np.abs(audio).mean() < 0.001:
            return ""

        # 文字起こし実行
        segments, info = self.model.transcribe(
            audio,
            language=self.language,
            beam_size=5,
            vad_filter=True,  # Voice Activity Detection
            vad_parameters=dict(
                min_silence_duration_ms=500,
            ),
        )

        # セグメントを結合
        text = " ".join(segment.text.strip() for segment in segments)
        return text.strip()
