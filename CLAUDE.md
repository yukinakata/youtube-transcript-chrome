# CLAUDE.md - YouTube/音声リアルタイム文字起こしアプリ

## 🎯 目標（Goal）

macOS上で動作するローカル音声文字起こしアプリケーションを構築する。
選択したウィンドウ/音声ソースからリアルタイムで音声をキャプチャし、Whisperを用いてテキストに変換、ターミナルに表示しながらログファイルとして保存する。

## 📐 設計（Design）

### コア機能
1. **音声キャプチャ**: BlackHole経由でシステム音声を取得
2. **リアルタイム文字起こし**: faster-whisper（Apple Silicon最適化）
3. **ターミナル出力**: タイムスタンプ付きでリアルタイム表示
4. **ログ保存**: 自動的に`./logs/`へタイムスタンプ付きファイル保存

### 技術スタック
- **言語**: Python 3.11+
- **音声処理**: sounddevice, numpy
- **文字起こし**: faster-whisper (small モデル)
- **仮想音声**: BlackHole 2ch
- **対応OS**: macOS (Apple Silicon)

### SKILLSレイヤー設計

```
┌─────────────────────────────────────────────────────────┐
│ 1. FOUNDATIONAL（思考の型）                              │
│    - 音声バッファリング → 文字起こし → 出力 の基本パターン │
│    - 3秒チャンク処理によるリアルタイム性確保              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. PARTNER / THIRD-PARTY（外部サービス吸収）            │
│    - Whisper: 音声認識エンジン                          │
│    - BlackHole: macOS仮想オーディオ                     │
│    - sounddevice: 音声入力ライブラリ                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. ENTERPRISE（勝ちパターン固定）                        │
│    - ログ形式の標準化                                   │
│    - ワークフロー最適化（起動→録音→保存→終了）          │
└─────────────────────────────────────────────────────────┘
```

## 🚧 制約（Constraints）

### 技術的制約
- macOS専用（BlackHole依存）
- Apple Silicon最適化（Intel Macでは動作未検証）
- Whisper smallモデル（500MB）のローカル保存が必要
- 初回起動時にモデルダウンロードが発生

### 運用制約
- BlackHoleの事前インストール・設定が必須
- 「Audio MIDI設定」での複数出力装置の構成が必要
- リアルタイム処理のため、3秒程度の遅延が発生

### スコープ外
- GUI（将来的な拡張として検討）
- 動画ファイルからの直接読み込み
- クラウドAPI連携
- Windows/Linux対応

## 📁 プロジェクト構造

```
youtube-transcript-chrome/
├── CLAUDE.md              # このファイル
├── architecture.md        # アーキテクチャ詳細
├── changelog.md           # 変更履歴
├── project-status.md      # 進捗状況
├── requirements.txt       # Python依存関係
├── src/
│   ├── __init__.py
│   ├── main.py           # エントリーポイント
│   ├── audio_capture.py  # 音声キャプチャ
│   ├── transcriber.py    # Whisper処理
│   └── logger.py         # ログ出力・保存
├── logs/                  # 文字起こしログ保存先
└── tests/
    └── test_*.py
```

## 🚀 クイックスタート

```bash
# 1. BlackHoleインストール
brew install blackhole-2ch

# 2. Audio MIDI設定で複数出力装置を構成

# 3. 依存関係インストール
pip install -r requirements.txt

# 4. 実行
python src/main.py
```
