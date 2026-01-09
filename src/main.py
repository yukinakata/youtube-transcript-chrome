#!/usr/bin/env python3
"""
リアルタイム音声文字起こしアプリ

macOS + BlackHole + faster-whisper による
システム音声のリアルタイム文字起こし
"""

import signal
import sys
from pathlib import Path

# srcディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio_capture import AudioCapture
from src.transcriber import Transcriber
from src.logger import TranscriptLogger


class RealtimeTranscriber:
    """リアルタイム文字起こしアプリケーション"""

    def __init__(
        self,
        device_name: str = "BlackHole",
        model_size: str = "small",
        language: str = "ja",
    ):
        self.running = False

        # コンポーネント初期化
        print("=" * 50)
        print("リアルタイム文字起こし")
        print("=" * 50)

        self.logger = TranscriptLogger()
        self.transcriber = Transcriber(model_size=model_size, language=language)
        self.audio = AudioCapture(device_name=device_name)

    def _on_audio_chunk(self, audio_data):
        """音声チャンクを受信したときの処理"""
        text = self.transcriber.transcribe(audio_data)
        if text:
            self.logger.log(text)

    def start(self):
        """文字起こしを開始"""
        self.running = True

        # シグナルハンドラ設定
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        print("\n開始します。Ctrl+C で終了。")
        print("-" * 50)

        self.audio.start(self._on_audio_chunk)

        # メインループ
        try:
            while self.running:
                signal.pause()
        except Exception:
            pass

    def stop(self):
        """文字起こしを停止"""
        self.running = False
        self.audio.stop()
        self.logger.close()

    def _signal_handler(self, signum, frame):
        """シグナルハンドラ"""
        print("\n\n終了処理中...")
        self.stop()
        sys.exit(0)


def main():
    """エントリーポイント"""
    import argparse

    parser = argparse.ArgumentParser(
        description="リアルタイム音声文字起こし",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python src/main.py                    # デフォルト設定で実行
  python src/main.py --model medium     # mediumモデルを使用
  python src/main.py --lang en          # 英語モード
  python src/main.py --list-devices     # 利用可能なデバイス一覧
        """,
    )
    parser.add_argument(
        "--device",
        default="BlackHole",
        help="入力デバイス名 (デフォルト: BlackHole)",
    )
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisperモデルサイズ (デフォルト: small)",
    )
    parser.add_argument(
        "--lang",
        default="ja",
        help="認識言語 (デフォルト: ja)",
    )
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="利用可能な入力デバイス一覧を表示",
    )

    args = parser.parse_args()

    if args.list_devices:
        print("利用可能な入力デバイス:")
        print(AudioCapture.list_devices())
        return

    try:
        app = RealtimeTranscriber(
            device_name=args.device,
            model_size=args.model,
            language=args.lang,
        )
        app.start()
    except RuntimeError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n中断されました")
        sys.exit(0)


if __name__ == "__main__":
    main()
