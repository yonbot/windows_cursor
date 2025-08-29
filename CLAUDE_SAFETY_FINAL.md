# 🛡️ Claude Code 安全システム - 最終構成

## 📋 概要

Claude Code の安全性を確保するための 2 つのアプローチ：

1. **シェル関数による自動変換**（推奨・動作確認済み）
2. **フック機能**（現在動作しない可能性あり）

## ✅ 実装済みの構成

### 1. シェル関数による rm → gomi 自動変換

**ファイル**: `claude_safety_unified.sh`

```bash
# セットアップ
./claude_safety_unified.sh

# 有効化
source ~/.zshrc
```

**動作**:

- `rm -rf` → 自動的に `gomi` に変換
- 削除ファイルは復元可能
- Claude Code が実行しても安全

### 2. フック設定（参考）

**ファイル構成**:

```
.claude/
├── settings.json          # フック設定
└── hooks/
    └── bash-safety-check.py  # 危険コマンド検知スクリプト
```

**settings.json**:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/.claude/hooks/bash-safety-check.py",
            "block_on_exit_codes": [2]
          }
        ]
      }
    ]
  }
}
```

## 🔧 推奨設定

1. **シェル関数を使用**（確実に動作）

   ```bash
   ./claude_safety_unified.sh
   source ~/.zshrc
   ```

2. **フック設定は補助的に維持**
   - 将来のアップデートで動作する可能性
   - 現在は動作しない場合が多い

## 📝 メンテナンス

### 削除されたファイル（重複・不要）:

- `bash-validator.py`
- `bash-pre-execute.sh`
- `check-dangerous-command.sh`
- `hook-wrapper.sh`
- `simple-test.sh`
- `write-test.sh`

### 保持されたファイル:

- `claude_safety_unified.sh` - メインセットアップスクリプト
- `.claude/hooks/bash-safety-check.py` - フック用スクリプト
- `.claude/settings.json` - フック設定

## 🚀 使い方

```bash
# 危険なコマンドを実行しても...
rm -rf important_directory

# 実際には gomi が動作
🔄 rm -rf → gomi (復元可能な削除)

# 復元可能
gomi restore
```

---

最終更新: 2025-07-25 18:25:00 JST
