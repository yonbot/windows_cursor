# 🌐 クロスプラットフォーム Python 環境セットアップ

## 🎯 概要

`setup_complete_environment.sh` スクリプトを Windows・Mac 両環境で動作するよう修正しました。環境を自動検出して適切なコマンドとパスを使用します。

## 🔍 実装した機能

### 1. 環境自動検出

```bash
# 環境検出とPythonコマンドの決定
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "📍 python3 コマンドを使用します"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "📍 python コマンドを使用します"
fi
```

### 2. OS 別処理分岐

```bash
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]] || command -v powershell &> /dev/null; then
    # Windows環境の処理
else
    # Unix系環境（Mac/Linux）の処理
fi
```

## 🔧 主な修正内容

### Python コマンド検出の改善

**修正前**:

```bash
if command -v python3 &> /dev/null; then
    python3 -m venv env  # Windows では python3 が存在しない
```

**修正後**:

```bash
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"  # Mac/Linux で優先
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"   # Windows で利用
fi

$PYTHON_CMD -m venv env  # 検出されたコマンドを使用
```

### 仮想環境削除の改善

**修正前**:

```bash
powershell -Command "Remove-Item -Recurse -Force env"  # 常に PowerShell
```

**修正後**:

```bash
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]] || command -v powershell &> /dev/null; then
    # Windows環境
    powershell -Command "Remove-Item -Recurse -Force env"
else
    # Unix系環境 (Mac/Linux)
    rm -rf env
fi
```

### パッケージインストールの統一

**Windows 環境**:

```bash
powershell -Command "
    env\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install jupyter notebook ipykernel pandas numpy matplotlib seaborn
    python -m ipykernel install --user --name=cursor_project --display-name='Cursor Project'
"
```

**Unix 系環境**:

```bash
source env/bin/activate
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install jupyter notebook ipykernel pandas numpy matplotlib seaborn
$PYTHON_CMD -m ipykernel install --user --name=cursor_project --display-name="Cursor Project"
deactivate
```

## 🌟 対応環境

### ✅ Windows 環境

- **Python コマンド**: `python` （`python3` は通常存在しない）
- **仮想環境パス**: `env\Scripts\Activate.ps1`
- **削除コマンド**: PowerShell の `Remove-Item`
- **検出方法**: `command -v powershell` で PowerShell 存在確認

### ✅ Mac/Linux 環境

- **Python コマンド**: `python3` 優先、`python` フォールバック
- **仮想環境パス**: `env/bin/activate`
- **削除コマンド**: `rm -rf`
- **検出方法**: `$OSTYPE` 変数による判定

## 🧪 動作確認結果

### Windows 環境

```bash
✅ python コマンドが検出される
✅ PowerShell による仮想環境操作が動作
✅ パッケージインストールが正常完了
✅ Jupyter カーネル登録が成功
```

### Mac 環境（予想される動作）

```bash
✅ python3 コマンドが優先的に検出される
✅ bash による仮想環境操作が動作
✅ パッケージインストールが正常完了
✅ Jupyter カーネル登録が成功
```

## 🎓 技術的なポイント

### 1. 環境検出の優先順位

1. **Python コマンド**: `python3` → `python` の順で検出
2. **OS 判定**: `$OSTYPE` 変数 + PowerShell 存在確認
3. **フォールバック**: 各環境で利用可能なコマンドを自動選択

### 2. PowerShell との連携

- bash 変数を PowerShell に直接渡せないため、PowerShell 内では `python` コマンドを直接使用
- 仮想環境アクティベート後は `python` コマンドが適切に動作

### 3. エラーハンドリング

- 存在しないディレクトリの削除エラーを回避
- コマンド存在確認による安全な実行
- 環境別の適切なエラーメッセージ

## 🚨 注意事項

1. **Windows 環境**: PowerShell の実行ポリシーが制限されている場合は事前設定が必要
2. **Mac 環境**: `python3` コマンドが優先されるため、Python 2.x との混在に注意
3. **パス区切り文字**: Windows (`\`) と Unix (`/`) の違いを適切に処理
4. **権限**: 仮想環境作成・削除に適切な権限が必要

## 🔗 関連ファイル

- `setup_complete_environment.sh`: メインのセットアップスクリプト
- `docs/DEACTIVATE_ERROR_SOLUTION.md`: deactivate エラーの解決方法
- `docs/ENSUREPIP_ERROR_SOLUTION.md`: ensurepip エラーの解決方法

---

最終更新: 2025-01-29 00:30:00 JST
