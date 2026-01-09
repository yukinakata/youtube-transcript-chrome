"""
ログ出力・保存モジュール

ターミナルへのリアルタイム表示とファイル保存を担当
"""

import os
from datetime import datetime
from pathlib import Path


class TranscriptLogger:
    """文字起こし結果のログ管理"""

    def __init__(self, log_dir: str = "./logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # セッション開始時刻でファイル名を決定
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = self.log_dir / f"{timestamp}.txt"
        self.start_time = datetime.now()

        # ログファイルを作成
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"# 文字起こしログ - {timestamp}\n")
            f.write(f"# 開始時刻: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n\n")

        print(f"ログファイル: {self.log_file}")

    def _get_elapsed_time(self) -> str:
        """開始からの経過時間を取得"""
        elapsed = datetime.now() - self.start_time
        total_seconds = int(elapsed.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def log(self, text: str) -> None:
        """文字起こし結果を出力・保存"""
        if not text.strip():
            return

        timestamp = self._get_elapsed_time()
        formatted = f"[{timestamp}] {text}"

        # ターミナル出力
        print(formatted)

        # ファイル保存
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

    def close(self) -> None:
        """ログセッションを終了"""
        end_time = datetime.now()
        elapsed = self._get_elapsed_time()

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write("\n" + "-" * 50 + "\n")
            f.write(f"# 終了時刻: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 総時間: {elapsed}\n")

        print(f"\n文字起こし終了。ログ保存先: {self.log_file}")
