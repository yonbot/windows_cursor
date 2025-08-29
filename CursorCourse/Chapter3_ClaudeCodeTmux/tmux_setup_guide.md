# Tmux セットアップガイド

## 🎯 Tmux とは

**Tmux（Terminal Multiplexer）**は、一つのターミナルで複数のセッションを管理できるツールです。

### なぜ開発で Tmux が重要なのか？

1. **セッション永続化**: 作業を中断・再開できる
2. **マルチタスク**: 複数の作業を同時進行
3. **環境統一**: チーム開発での一貫した環境
4. **AI 協調開発**: 複数の AI ツールを効率的に切り替え

## 🛠️ インストール

### macOS

```bash
# Homebrew でインストール
brew install tmux

# バージョン確認
tmux -V
```

### Ubuntu/Debian

```bash
# APT でインストール
sudo apt update
sudo apt install tmux

# バージョン確認
tmux -V
```

### Windows (WSL)

```bash
# WSL 内で Ubuntu の手順に従う
sudo apt install tmux
```

## ⚙️ 基本設定

### ~/.tmux.conf 設定ファイル

```bash
# ホームディレクトリに設定ファイル作成
touch ~/.tmux.conf
```

### 推奨設定内容

```conf
# ~/.tmux.conf

# プレフィックスキーを Ctrl+b から Ctrl+a に変更（お好みで）
# set -g prefix C-a
# unbind C-b
# bind C-a send-prefix

# マウス操作を有効化
set -g mouse on

# 256色ターミナル対応
set -g default-terminal "screen-256color"

# ペイン分割のキーバインド
bind | split-window -h  # | で垂直分割
bind - split-window -v  # - で水平分割

# ペイン間移動をviライクに
bind h select-pane -L   # 左のペイン
bind j select-pane -D   # 下のペイン
bind k select-pane -U   # 上のペイン
bind l select-pane -R   # 右のペイン

# ウィンドウ番号を1から開始
set -g base-index 1
set -g pane-base-index 1

# ステータスバーの設定
set -g status-bg colour235
set -g status-fg colour136
set -g status-left '#[fg=colour166][#S] '
set -g status-right '#[fg=colour166]%Y-%m-%d %H:%M'

# アクティブペインの境界色
set -g pane-active-border-style fg=colour166

# 履歴を10000行まで保存
set -g history-limit 10000

# Escape キーの遅延をなくす
set -sg escape-time 0
```

### 設定を反映

```bash
# 設定ファイルを再読み込み
tmux source-file ~/.tmux.conf
```

## 🚀 開発用セッション構成

### AI 協調開発レイアウトの作成

```bash
# 開発専用セッション作成
tmux new-session -d -s dev-session

# ペイン分割（3ペイン構成）
tmux split-window -h                    # 垂直分割
tmux select-pane -t 0                   # 左ペインを選択
tmux split-window -v                    # 水平分割

# 各ペインに名前を設定
tmux select-pane -t 0 -T "Cursor/Editor"
tmux select-pane -t 1 -T "Claude Code"
tmux select-pane -t 2 -T "Dev Server"
```

### 理想的なレイアウト

```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│   Cursor/Editor     │   Claude Code       │
│   (要件定義・レビュー)   │   (実装)            │
│                     │                     │
├─────────────────────┴─────────────────────┤
│                                           │
│   Development Server                      │
│   (npm run dev / ログ監視)                 │
│                                           │
└───────────────────────────────────────────┘
```

## 📋 基本操作一覧

### セッション管理

```bash
# セッション作成
tmux new-session -s session-name

# セッション一覧
tmux list-sessions
tmux ls

# セッションに接続
tmux attach-session -t session-name
tmux a -t session-name

# セッション終了
tmux kill-session -t session-name

# 全セッション終了
tmux kill-server
```

### ペイン操作（デフォルト: Ctrl+b プレフィックス）

```bash
# ペイン分割
Ctrl+b %    # 垂直分割
Ctrl+b "    # 水平分割
Ctrl+b |    # 垂直分割（カスタム設定）
Ctrl+b -    # 水平分割（カスタム設定）

# ペイン移動
Ctrl+b o          # 次のペイン
Ctrl+b ←/→/↑/↓    # 方向キーで移動
Ctrl+b h/j/k/l    # viライク移動（カスタム設定）

# ペインサイズ調整
Ctrl+b Alt+←/→/↑/↓    # サイズ調整

# ペイン削除
Ctrl+b x    # 現在のペイン削除
```

### ウィンドウ操作

```bash
# 新しいウィンドウ作成
Ctrl+b c

# ウィンドウ切り替え
Ctrl+b n    # 次のウィンドウ
Ctrl+b p    # 前のウィンドウ
Ctrl+b 0-9  # 番号指定

# ウィンドウ一覧
Ctrl+b w

# ウィンドウ削除
Ctrl+b &
```

## 🔧 開発ワークフロー実践

### 1. 開発セッション開始

```bash
# プロジェクト専用セッション作成
tmux new-session -d -s translation-dev

# 開発用レイアウト構成
tmux split-window -h
tmux split-window -v

# セッションに接続
tmux attach-session -t translation-dev
```

### 2. 各ペインの役割設定

```bash
# ペイン 0: Cursor 作業
tmux select-pane -t 0
cursor .

# ペイン 1: Claude Code 実行
tmux select-pane -t 1
# Claude Code での実装作業

# ペイン 2: 開発サーバー
tmux select-pane -t 2
npm run dev
```

### 3. 作業の流れ

1. **ペイン 0**: Cursor で要件定義・レビュー
2. **ペイン 1**: Claude Code で実装
3. **ペイン 2**: 開発サーバーでリアルタイム確認
4. **切り替え**: `Ctrl+b o` で効率的に移動

## 💡 実践テクニック

### セッション復旧

```bash
# セッションが切れた場合の復旧
tmux list-sessions  # セッション確認
tmux attach -t translation-dev  # 再接続
```

### ログ管理

```bash
# ペイン内容をファイルに保存
tmux capture-pane -t 2 -p > server.log

# リアルタイムログ監視
tail -f .next/trace
```

### 複数プロジェクト管理

```bash
# プロジェクトごとにセッション作成
tmux new-session -d -s project-a
tmux new-session -d -s project-b
tmux new-session -d -s project-c

# セッション間の素早い切り替え
tmux switch-client -t project-a
```

## 🛡️ トラブルシューティング

### よくある問題と解決法

#### 1. セッションが見つからない

```bash
# セッション一覧確認
tmux ls

# セッションがない場合は再作成
tmux new-session -d -s dev-session
```

#### 2. ペインが反応しない

```bash
# ペインの状態確認
tmux list-panes

# 強制的にペイン削除・再作成
tmux kill-pane -t 1
tmux split-window -h
```

#### 3. 設定が反映されない

```bash
# 設定ファイル確認
cat ~/.tmux.conf

# 設定再読み込み
tmux source-file ~/.tmux.conf

# Tmux完全再起動
tmux kill-server
tmux new-session
```

#### 4. マウス操作ができない

```bash
# マウス設定確認
tmux show-options -g mouse

# マウス有効化
tmux set -g mouse on
```

## 📚 参考リソース

- [Tmux 公式 Wiki](https://github.com/tmux/tmux/wiki)
- [Tmux Cheat Sheet](https://tmuxcheatsheet.com/)
- [実用的な Tmux 設定例](https://github.com/gpakosz/.tmux)

---

**🚀 Tmux をマスターして、効率的な開発環境を構築しましょう！**

次は [Claude Code 基礎](claude_code_basics.md) に進んで、AI による実装技法を学習します。

---

最終更新: 2025-01-28 18:50:00 JST
