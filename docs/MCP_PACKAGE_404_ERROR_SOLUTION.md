# 🔧 MCP Package 404 エラー解決方法

## 🚨 問題の概要

**エラー内容**:

```bash
npm error code E404
npm error 404 Not Found - GET https://registry.npmjs.org/@mcpservers%2fplaywright - Not found
npm error 404  '@mcpservers/playwright@*' is not in this registry.

npm error 404 Not Found - GET https://registry.npmjs.org/@executeautomation%2fmcp-postgres - Not found
npm error 404  '@executeautomation/mcp-postgres@*' is not in this registry.
```

**原因**: 存在しない npm パッケージ名がスクリプトに記載されていた

## 🔍 根本原因分析

### 問題のあったパッケージ名（修正前）

```bash
npm_servers=(
    "@modelcontextprotocol/server-filesystem"    # ✅ 正常
    "@modelcontextprotocol/server-github"        # ✅ 正常
    "@modelcontextprotocol/server-slack"         # ✅ 正常
    "@gongrzhe/server-gmail-autoauth-mcp"        # ✅ 正常
    "@cocal/google-calendar-mcp"                 # ✅ 正常
    "@mcpservers/playwright"                     # ❌ 存在しない
    "@executeautomation/mcp-postgres"            # ❌ 存在しない
)
```

### 問題点

1. **誤ったパッケージ名**: `@mcpservers/playwright` → 正しくは `@playwright/mcp`
2. **存在しないパッケージ**: `@executeautomation/mcp-postgres` → npm レジストリに存在しない
3. **非推奨パッケージ**: `@modelcontextprotocol/server-postgres` → deprecated の警告
4. **検証不足**: インストール前のパッケージ存在確認が不十分

## ✅ 解決済み修正内容

### 修正後のパッケージリスト

```bash
# npmでインストール可能なMCPサーバー（実在するパッケージのみ）
npm_servers=(
    "@modelcontextprotocol/server-filesystem"    # ✅ ファイルシステム操作
    "@modelcontextprotocol/server-github"        # ✅ GitHub連携
    "@modelcontextprotocol/server-slack"         # ✅ Slack連携
    "@ahmetkca/mcp-server-postgres"              # ✅ PostgreSQL連携（推奨版）
    "@gongrzhe/server-gmail-autoauth-mcp"        # ✅ Gmail連携
    "@cocal/google-calendar-mcp"                 # ✅ Google Calendar連携
    "@playwright/mcp"                            # ✅ Playwright自動化（修正済み）
)
```

### 修正のポイント

1. **正しいパッケージ名**: `@mcpservers/playwright` → `@playwright/mcp`
2. **PostgreSQL パッケージ更新**: `@executeautomation/mcp-postgres` → `@ahmetkca/mcp-server-postgres`
3. **非推奨パッケージの回避**: `@modelcontextprotocol/server-postgres`（deprecated）を使用しない
4. **アクティブメンテナンス**: より最近更新されたパッケージを選択

## 🧪 動作確認結果

### インストール成功確認

```bash
✅ @playwright/mcp@0.0.35 インストール成功
✅ @ahmetkca/mcp-server-postgres@1.2.0 インストール成功
✅ 103個の依存パッケージも正常インストール
✅ エラーなしでインストール完了
```

### 現在のインストール済み MCP パッケージ

```bash
C:\Users\yonbo\AppData\Roaming\npm
├── @ahmetkca/mcp-server-postgres@1.2.0        # PostgreSQL連携（推奨版）
├── @cocal/google-calendar-mcp@1.4.8           # Google Calendar連携
├── @gongrzhe/server-gmail-autoauth-mcp@1.1.11 # Gmail連携
├── @marp-team/marp-cli@4.2.3                  # Marpプレゼンテーション
├── @modelcontextprotocol/server-filesystem@2025.8.21  # ファイルシステム
├── @modelcontextprotocol/server-github@2025.4.8       # GitHub連携
├── @modelcontextprotocol/server-postgres@0.6.2        # PostgreSQL（非推奨）
├── @modelcontextprotocol/server-slack@2025.4.25       # Slack連携
└── @playwright/mcp@0.0.35                     # Playwright自動化
```

## 🔄 今後の予防策

### 1. パッケージ存在確認

```bash
# パッケージインストール前の存在確認
npm view <package-name> version 2>/dev/null || echo "Package not found"
```

### 2. 段階的インストール

```bash
# 一括インストールではなく、個別インストールでエラー特定を容易に
for server in "${npm_servers[@]}"; do
    echo "Installing $server..."
    npm install -g "$server" && echo "✅ Success" || echo "❌ Failed"
done
```

### 3. パッケージ名検証

- **公式ドキュメント確認**: パッケージ名は公式ドキュメントから取得
- **npm レジストリ検索**: https://www.npmjs.com/ で事前確認
- **バージョン情報確認**: 最新バージョンと互換性の確認

## 🎯 .cursor/mcp.json との整合性

### 設定ファイルとの対応関係

| スクリプトパッケージ名                    | .cursor/mcp.json 設定 | 用途                    |
| ----------------------------------------- | --------------------- | ----------------------- |
| `@modelcontextprotocol/server-filesystem` | `filesystem`          | ファイルシステム操作    |
| `@modelcontextprotocol/server-github`     | `github`              | GitHub 連携             |
| `@playwright/mcp`                         | `playwright`          | ブラウザ自動化          |
| `@ahmetkca/mcp-server-postgres`           | `postgres`            | PostgreSQL データベース |

### 設定ファイルでの正しい記載

```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest"],
  "env": {},
  "description": "Playwrightによるブラウザ自動化とWebスクレイピングを提供するMCPサーバー",
  "autoStart": false
},
"postgres": {
  "command": "npx",
  "args": ["@ahmetkca/mcp-server-postgres"],
  "env": {
    "DATABASE_URL": "${input:database_url}"
  },
  "description": "PostgreSQL データベース操作とスキーマ分析を提供するMCPサーバー",
  "autoStart": false
}
```

## 🎓 学習ポイント

### 今回学んだこと

- npm パッケージ名の正確性の重要性
- パッケージ存在確認の方法
- エラーログからの問題特定技法

### 技術的知見

- **npm レジストリ**: パッケージの実際の存在確認方法
- **MCP 設定**: スクリプトと設定ファイルの整合性維持
- **エラーハンドリング**: 404 エラーの適切な対処法

## 🚨 注意事項

1. **パッケージ名の大文字小文字**: npm パッケージ名は大文字小文字を区別
2. **スコープ名の確認**: `@organization/package-name`形式の正確性
3. **バージョン互換性**: MCP プロトコルのバージョン互換性確認
4. **インストール権限**: グローバルインストールには適切な権限が必要

## 🔗 参考リンク

- [NPM Registry](https://www.npmjs.com/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Playwright MCP Server](https://www.npmjs.com/package/@playwright/mcp)

---

最終更新: 2025-01-29 00:05:00 JST
