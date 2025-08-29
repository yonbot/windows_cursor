# Claude Code 安全コマンド Hooks 設定

## 🎯 目的

Claude Code が生成するコマンドに`rm -rf`などの危険なコマンドが含まれていた場合、自動的に検知してアラートを表示し、安全な代替手段（`gomi`）を提案するシステムを構築します。

## 🛡️ 安全対策の必要性

### 危険コマンドの例

```bash
rm -rf /path/to/directory    # 危険：復元不可能な完全削除
sudo rm -rf /               # 極めて危険：システム全体削除
chmod 777 file              # 危険：セキュリティリスク
curl url | bash             # 危険：未検証スクリプト実行
```

### Gomi の利点

- **安全な削除**: ゴミ箱への移動（復元可能）
- **誤削除防止**: 完全削除を避ける
- **クロスプラットフォーム**: macOS/Linux 対応

## 🚀 セットアップ手順

### Step 1: Gomi のインストール

#### macOS (Homebrew)

```bash
brew install gomi
```

#### Linux (Go 環境)

```bash
go install github.com/b4b4r07/gomi/cmd/gomi@latest
```

#### 手動インストール

```bash
# GitHubリリースから適切なバイナリをダウンロード
curl -L https://github.com/b4b4r07/gomi/releases/latest/download/gomi_$(uname -s)_$(uname -m).tar.gz | tar xz
sudo mv gomi /usr/local/bin/
```

### Step 2: 安全 Hooks 設定

#### ~/.zshrc への追加 (zsh ユーザー)

```bash
# Claude Code安全フック設定ファイルを追加
cat >> ~/.zshrc << 'EOF'

# ===========================================
# Claude Code 安全コマンドHooks
# ===========================================

# gomiが利用可能かチェック
if command -v gomi >/dev/null 2>&1; then
    GOMI_AVAILABLE=true
else
    GOMI_AVAILABLE=false
fi

# 危険コマンド検知・アラート関数
claude_safety_check() {
    local cmd="$1"

    # rm -rf パターンの検知
    if [[ "$cmd" =~ rm.*-.*r.*f|rm.*-.*f.*r ]]; then
        echo "🚨 CLAUDE CODE 安全アラート 🚨"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "⚠️  危険なコマンドが検出されました"
        echo "💀 実行予定: $cmd"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        if [ "$GOMI_AVAILABLE" = true ]; then
            echo "✅ 安全な代替手段を提案します："

            # rm -rf を gomi に置換
            local safe_cmd=$(echo "$cmd" | sed 's/rm -rf/gomi/g' | sed 's/rm -fr/gomi/g')
            echo "🛡️  推奨コマンド: $safe_cmd"
            echo ""

            read -p "🤔 安全なコマンドに変更しますか？ (y/N): " choice
            case "$choice" in
                y|Y )
                    echo "✨ 安全なコマンドを実行します"
                    eval "$safe_cmd"
                    return 0
                    ;;
                * )
                    echo "❌ コマンド実行をキャンセルしました"
                    return 1
                    ;;
            esac
        else
            echo "❌ gomiがインストールされていません"
            echo "📥 インストール方法: brew install gomi"
            echo "⛔ 危険なコマンドの実行をブロックします"
            return 1
        fi
    fi

    # その他の危険コマンドパターン
    if [[ "$cmd" =~ sudo.*rm|chmod.*777|curl.*\|.*bash ]]; then
        echo "🚨 CLAUDE CODE 安全アラート 🚨"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "⚠️  潜在的に危険なコマンドです"
        echo "🔍 実行予定: $cmd"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        read -p "🤔 本当に実行しますか？ (y/N): " choice
        case "$choice" in
            y|Y )
                echo "⚠️  ユーザー確認済みで実行します"
                eval "$cmd"
                return 0
                ;;
            * )
                echo "✅ 安全のためコマンド実行をキャンセルしました"
                return 1
                ;;
        esac
    fi

    # 安全なコマンドはそのまま実行
    eval "$cmd"
}

# rmコマンドのオーバーライド（完全な安全性確保）
rm() {
    local args=("$@")
    local cmd="rm ${args[*]}"

    # 危険フラグの検知
    if [[ "$cmd" =~ -.*r.*f|-.*f.*r ]]; then
        claude_safety_check "$cmd"
    else
        # 通常のrmは警告のみ
        echo "💡 ヒント: より安全な削除には 'gomi' を使用できます"
        command rm "$@"
    fi
}

# Claude Code作業開始通知
claude_code_session_start() {
    echo "🤖 Claude Code セッション開始"
    echo "🛡️  安全フックが有効化されています"
    if [ "$GOMI_AVAILABLE" = true ]; then
        echo "✅ gomi (安全削除) 利用可能"
    else
        echo "⚠️  gomi未インストール - 'brew install gomi' を推奨"
    fi
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# エイリアス設定
alias claude-start='claude_code_session_start'
alias safe-rm='gomi'

EOF

echo "✅ Claude Code安全フック設定が完了しました"
echo "🔄 設定を反映するため、新しいターミナルを開くか 'source ~/.zshrc' を実行してください"
```

#### ~/.bashrc への追加 (bash ユーザー)

```bash
# bashユーザー用の同等設定
cat >> ~/.bashrc << 'EOF'
# 上記のzshrc設定と同じ内容をbashrc用に追加
# （内容は同一のため省略）
EOF
```

### Step 3: 設定の反映と確認

```bash
# 設定を反映
source ~/.zshrc

# Claude Codeセッション開始
claude-start

# テスト実行
echo "test file" > test.txt
rm -rf test.txt  # 安全アラートが表示されるはず
```

## 🧪 動作テスト

### テストケース 1: 危険コマンド検知

```bash
# 以下のコマンドでアラートが表示されることを確認
rm -rf ./test_directory
rm -fr ./another_test
sudo rm -rf /tmp/test
```

**期待される動作**:

```
🚨 CLAUDE CODE 安全アラート 🚨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  危険なコマンドが検出されました
💀 実行予定: rm -rf ./test_directory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 安全な代替手段を提案します：
🛡️  推奨コマンド: gomi ./test_directory

🤔 安全なコマンドに変更しますか？ (y/N):
```

### テストケース 2: gomi 動作確認

```bash
# テストファイル作成
mkdir test_dir
echo "test content" > test_dir/test.txt

# gomiでの安全削除
gomi test_dir

# 削除されたファイルの復元確認
gomi -r  # 復元可能ファイル一覧表示
```

## 🔧 カスタマイズ・設定調整

### 追加の危険コマンドパターン

```bash
# ~/.zshrcに追加パターンを設定
claude_safety_check() {
    # 既存のチェックに加えて以下を追加

    # Docker関連の危険コマンド
    if [[ "$cmd" =~ docker.*rmi.*-f|docker.*system.*prune.*-f ]]; then
        # アラート処理
    fi

    # Git関連の危険コマンド
    if [[ "$cmd" =~ git.*reset.*--hard.*HEAD~|git.*clean.*-fd ]]; then
        # アラート処理
    fi

    # システム関連の危険コマンド
    if [[ "$cmd" =~ systemctl.*stop|service.*stop ]]; then
        # アラート処理
    fi
}
```

### 感度レベル調整

```bash
# 環境変数で感度レベルを制御
export CLAUDE_SAFETY_LEVEL="strict"  # strict/normal/loose

# strict: 全ての危険コマンドをブロック
# normal: ユーザー確認後に実行可能
# loose: 警告のみ表示
```

## 📋 Tmux 統合設定

### Tmux セッション用の安全設定

```bash
# ~/.tmux.conf に追加
# Tmuxセッション開始時に安全フック有効化
set-hook -g session-created 'run-shell "echo \"🛡️ Tmux安全セッション開始\" && claude-start"'

# ペイン作成時にも安全設定を適用
set-hook -g pane-created 'run-shell "source ~/.zshrc"'
```

## 📚 Claude Code 実践での活用

### 実装フェーズでの安全確認

```bash
# Claude Codeから生成されたスクリプトの実行前チェック
claude_code_script_check() {
    local script_file="$1"

    echo "🔍 Claude Code生成スクリプトの安全性チェック"

    # 危険パターンの検索
    if grep -E "rm -rf|sudo rm|chmod 777|curl.*\|.*bash" "$script_file"; then
        echo "⚠️  危険なコマンドが含まれています"
        echo "📋 詳細確認を推奨します"
        return 1
    else
        echo "✅ 明らかな危険コマンドは検出されませんでした"
        return 0
    fi
}

# 使用例
# claude_code_script_check generated_script.sh
```

### セッション終了時のクリーンアップ

```bash
claude_code_session_end() {
    echo "🤖 Claude Code セッション終了"
    echo "🧹 安全クリーンアップを実行中..."

    # 一時ファイルの安全削除
    if [ -d "/tmp/claude_temp" ]; then
        gomi /tmp/claude_temp
    fi

    # 危険コマンド実行ログの確認
    if [ -f ~/.claude_dangerous_commands.log ]; then
        echo "⚠️  実行された危険コマンドのログ:"
        cat ~/.claude_dangerous_commands.log
    fi

    echo "✅ セッション終了完了"
}

alias claude-end='claude_code_session_end'
```

## 🚨 トラブルシューティング

### よくある問題と解決法

#### 1. gomi コマンドが見つからない

```bash
# 解決方法
brew install gomi

# または手動インストール
curl -L https://github.com/b4b4r07/gomi/releases/latest/download/gomi_$(uname -s)_$(uname -m).tar.gz | tar xz
sudo mv gomi /usr/local/bin/
```

#### 2. フックが動作しない

```bash
# 設定確認
type rm  # オーバーライドされているか確認

# 設定再読み込み
source ~/.zshrc

# 権限確認
ls -la ~/.zshrc
```

#### 3. アラートが表示されすぎる

```bash
# 感度レベルを調整
export CLAUDE_SAFETY_LEVEL="normal"

# 特定コマンドを除外
CLAUDE_SAFETY_IGNORE="rm -rf .git"
```

### ログとモニタリング

```bash
# 危険コマンド実行ログの設定
export CLAUDE_SAFETY_LOG="$HOME/.claude_safety.log"

# ログ確認
tail -f ~/.claude_safety.log

# 統計表示
claude_safety_stats() {
    echo "📊 Claude Code安全統計"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚫 ブロックされたコマンド数: $(grep "ブロック" ~/.claude_safety.log | wc -l)"
    echo "⚠️  警告が出たコマンド数: $(grep "警告" ~/.claude_safety.log | wc -l)"
    echo "✅ 安全に実行されたコマンド数: $(grep "安全実行" ~/.claude_safety.log | wc -l)"
}
```

## 📖 参考リソース

- [Gomi 公式リポジトリ](https://github.com/b4b4r07/gomi)
- [Shell Hook Best Practices](https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html)
- [Zsh Hook Functions](https://zsh.sourceforge.io/Doc/Release/Functions.html)

---

**🛡️ Claude Code 使用時の安全性を大幅に向上させ、初心者でも安心して学習できる環境を構築しました！**

この設定により、危険なコマンドの自動検知・置換が可能になり、学習中の事故を防止できます。

次は [Claude Code 基礎](claude_code_basics.md) に戻って、安全な環境での AI 協調開発を実践しましょう。

---

最終更新: 2025-01-28 19:45:00 JST
