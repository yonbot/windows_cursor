#!/usr/bin/env python3

import json
import sys
import re
from datetime import datetime

def log_event(event_type, command, action=""):
    """ログファイルに記録"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = os.path.expanduser("~/.claude_safety_hooks.log")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {event_type}: {command} {action}\n")

def check_dangerous_command(command):
    """危険なコマンドをチェック"""
    
    # rm -rf パターン
    if re.search(r'rm\s+(-\w*r\w*f|-\w*f\w*r)', command):
        print("""
🚨 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   危険なコマンドが検出されました！
🚨 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  コマンド: {}
💀 危険度: 高（完全削除・復元不可能）

✅ 代替案:
   1. gomiコマンドを使用（復元可能）: {}
   
   2. より慎重な削除:
      - まずlsで確認
      - 段階的に削除（rm -r without -f）

❌ このコマンドはブロックされました。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".format(command, re.sub(r'rm\s+-rf', 'gomi', command)), file=sys.stderr)
        return False
    
    # sudo rm パターン
    if re.search(r'sudo\s+rm\s+', command):
        print("""
🚨 システムレベルの削除コマンドが検出されました
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  コマンド: {}
🔒 権限: システム管理者

❌ セキュリティポリシーによりブロックされました。
""".format(command), file=sys.stderr)
        return False
    
    # curl/wget | bash/sh パターン
    if re.search(r'(curl|wget)\s+.*\|\s*(bash|sh)', command):
        print("""
🚨 未検証スクリプトの実行が検出されました
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  コマンド: {}
🔍 リスク: 未検証のコードを直接実行

✅ 推奨手順:
   1. まずスクリプトをダウンロード
   2. 内容を確認
   3. 安全性を検証後に実行

❌ このコマンドはブロックされました。
""".format(command), file=sys.stderr)
        return False
    
    # システムディレクトリへの削除操作
    if re.search(r'rm\s+.*(/\s|/bin|/etc|/usr|/var|/System|/Library)', command):
        print("""
🚨 システムディレクトリへの操作が検出されました
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ 絶対に実行してはいけません！
💀 コマンド: {}

❌ ブロックされました。
""".format(command), file=sys.stderr)
        return False
    
    # chmod 777 (警告のみ)
    if re.search(r'chmod\s+777', command):
        print("""
⚠️  セキュリティリスクのあるコマンド
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔓 コマンド: {}
🚨 リスク: 全ユーザーに全権限を付与

💡 推奨される代替案:
   - chmod 755 (実行可能ファイル)
   - chmod 644 (通常のファイル)
   - chmod 600 (機密ファイル)

⚠️  注意して実行してください。
""".format(command), file=sys.stderr)
        # 警告のみ（ブロックしない）
        return True
    
    return True

def main():
    # 標準入力からJSONを読み込む
    try:
        data = json.load(sys.stdin)
        
        # Bashコマンドを取得
        command = data.get('params', {}).get('command', '')
        
        # 危険なコマンドをチェック
        if not check_dangerous_command(command):
            # 危険なコマンドはブロック（exit code 2）
            sys.exit(2)
        
        # 安全なコマンドは通過
        sys.exit(0)
        
    except Exception as e:
        print(f"Error in safety check: {e}", file=sys.stderr)
        # エラーの場合は安全のため通過させる
        sys.exit(0)

if __name__ == "__main__":
    import os
    main()