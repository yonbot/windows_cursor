# 🔧 Ensurepip エラー (103) 解決方法

## 🚨 問題の概要

**エラー内容**:

```
Error: Command '['C:\workspace_cursor\windows_cursor\env\Scripts\python.exe', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 103.
```

**原因**: Windows 環境での仮想環境における pip 初期化の失敗

## ✅ 解決済み手順

### 1. 問題診断

```powershell
# システムPython環境の確認
python --version  # → Python 3.13.7 ✅
pip --version     # → pip 25.2 ✅

# 仮想環境の状態確認
Get-ChildItem env  # → 破損した仮想環境を確認
```

### 2. 仮想環境の完全再作成（実行済み）

```powershell
# 1. 古い仮想環境を削除
Remove-Item -Recurse -Force env

# 2. 新しい仮想環境を作成
python -m venv env

# 3. 仮想環境をアクティベート
env\Scripts\Activate.ps1

# 4. pipを最新版にアップグレード
python -m pip install --upgrade pip
```

### 3. 動作確認（完了）

```powershell
# 基本パッケージのインストールテスト
pip install jupyter notebook ipykernel
# → 成功: 大量のパッケージが正常にインストール完了 ✅
```

## 🎯 解決結果

✅ **仮想環境**: 正常に再作成完了  
✅ **pip**: バージョン 25.2 で正常動作  
✅ **Python**: 3.13.7 で正常動作  
✅ **パッケージインストール**: Jupyter 関連など多数のパッケージが正常にインストール

## 🔄 今後同じエラーが発生した場合の対処法

### 方法 1: 仮想環境の再作成（推奨）

```powershell
Remove-Item -Recurse -Force env
python -m venv env
env\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 方法 2: pip 修復のみ

```powershell
python -m pip install --force-reinstall --target env\Lib\site-packages pip
```

## 🎓 学習ポイント

### 今回学んだこと

- Windows 環境での ensurepip エラーの特徴
- 仮想環境の破損検出方法
- PowerShell での安全な仮想環境管理

### 予防策

- 定期的な仮想環境の再作成
- システム Python との分離を意識
- 重要なパッケージリストの保存（requirements.txt）

## 🚨 注意事項

1. **仮想環境の削除**: 必要なパッケージ設定は事前にバックアップ
2. **PowerShell 実行ポリシー**: 必要に応じて `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. **パッケージの再インストール**: requirements.txt があれば `pip install -r requirements.txt`

---

最終更新: 2025-01-28 23:45:00 JST

