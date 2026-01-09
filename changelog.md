# changelog.md - 変更履歴

すべての重要な変更はこのファイルに記録されます。

フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) に基づいています。

---

## [Unreleased]

### 計画中
- 基本的な音声キャプチャ機能
- Whisperによるリアルタイム文字起こし
- ターミナル出力
- ログファイル保存

---

## [0.0.1] - 2025-01-09

### Added（追加）
- プロジェクト初期化
- CLAUDE.md（目標・設計・制約）
- architecture.md（システムアーキテクチャ）
- changelog.md（このファイル）
- project-status.md（進捗状況）

### 決定事項
- Chrome拡張 → ローカルPythonアプリに方針変更
- Whisper smallモデル採用
- ターミナルベースのUI
- ログ形式: タイムスタンプ付きテキスト

---

## バージョニング規則

```
MAJOR.MINOR.PATCH

MAJOR: 互換性のない変更
MINOR: 後方互換性のある機能追加
PATCH: 後方互換性のあるバグ修正
```

## 変更タイプ

- **Added**: 新機能
- **Changed**: 既存機能の変更
- **Deprecated**: 将来削除予定の機能
- **Removed**: 削除された機能
- **Fixed**: バグ修正
- **Security**: セキュリティ関連
