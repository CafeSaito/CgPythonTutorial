# このスクリプトのディレクトリを取得
$root_dir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$script_dir = "$root_dir\scripts"
$test_dir = "$root_dir\tests"

# テストスクリプトのディレクトリまで移動します。

# 環境変数を設定
$env:PYTHONPATH = "$script_dir;$env:PYTHONPATH"

cd "$root_dir\tests"
# mayapy2024を指定してテストを実行
& "C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe" -m unittest
