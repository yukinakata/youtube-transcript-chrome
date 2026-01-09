"""
音声キャプチャモジュール

BlackHole経由でシステム音声を取得
"""

import numpy as np
import sounddevice as sd
from typing import Callable, Optional


# 設定定数
SAMPLE_RATE = 16000  # Whisper推奨サンプルレート
CHANNELS = 1  # モノラル
CHUNK_DURATION = 5.0  # 精度重視: 5秒バッファ


class AudioCapture:
    """BlackHoleからの音声キャプチャ"""

    def __init__(
        self,
        device_name: str = "BlackHole",
        sample_rate: int = SAMPLE_RATE,
        chunk_duration: float = CHUNK_DURATION,
    ):
        """
        Args:
            device_name: 入力デバイス名（部分一致）
            sample_rate: サンプルレート
            chunk_duration: チャンクの長さ（秒）
        """
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_samples = int(sample_rate * chunk_duration)

        # BlackHoleデバイスを検索
        self.device_id = self._find_device(device_name)
        if self.device_id is None:
            available = self.list_devices()
            raise RuntimeError(
                f"'{device_name}' が見つかりません。\n"
                f"利用可能なデバイス:\n{available}\n\n"
                "BlackHoleをインストールしてください: brew install blackhole-2ch"
            )

        # バッファ
        self.buffer = np.array([], dtype=np.float32)
        self.callback: Optional[Callable[[np.ndarray], None]] = None
        self.stream: Optional[sd.InputStream] = None

    def _find_device(self, name: str) -> Optional[int]:
        """デバイス名からIDを検索"""
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if name.lower() in device["name"].lower() and device["max_input_channels"] > 0:
                print(f"入力デバイス: {device['name']}")
                return i
        return None

    @staticmethod
    def list_devices() -> str:
        """利用可能な入力デバイス一覧を取得"""
        devices = sd.query_devices()
        lines = []
        for i, device in enumerate(devices):
            if device["max_input_channels"] > 0:
                lines.append(f"  [{i}] {device['name']}")
        return "\n".join(lines) if lines else "  (なし)"

    def _audio_callback(self, indata, frames, time, status):
        """sounddeviceコールバック"""
        if status:
            print(f"音声警告: {status}")

        # バッファに追加
        audio = indata[:, 0].astype(np.float32)
        self.buffer = np.append(self.buffer, audio)

        # チャンクサイズに達したらコールバック
        while len(self.buffer) >= self.chunk_samples:
            chunk = self.buffer[: self.chunk_samples]
            self.buffer = self.buffer[self.chunk_samples :]

            if self.callback:
                self.callback(chunk)

    def start(self, callback: Callable[[np.ndarray], None]) -> None:
        """
        音声キャプチャを開始

        Args:
            callback: チャンクごとに呼ばれるコールバック関数
        """
        self.callback = callback
        self.buffer = np.array([], dtype=np.float32)

        self.stream = sd.InputStream(
            device=self.device_id,
            samplerate=self.sample_rate,
            channels=CHANNELS,
            dtype=np.float32,
            callback=self._audio_callback,
            blocksize=int(self.sample_rate * 0.1),  # 100ms単位で取得
        )
        self.stream.start()
        print(f"音声キャプチャ開始 ({self.chunk_duration}秒バッファ)")

    def stop(self) -> None:
        """音声キャプチャを停止"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        print("音声キャプチャ停止")
