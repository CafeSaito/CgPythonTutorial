# このps1ファイルのあるフォルダのパスを取得する
$root_dir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$env:PYTHONPATH = "$root_dir\scripts;$env:PYTHONPATH"

# mayaのインタープレターを使用してみましょう。
# -m unittest はPythonの標準ライブラリに含まれる unittest モジュールをスクリプトモードで実行することを意味します。
# discover はテストを自動的に検出するためのサブコマンドです。
# -s は--start-directory の略で、テストの検索を開始するディレクトリを指定します。
# -p は--pattern の略で、テストファイルのパターンを指定します。
& "C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe" -m unittest discover -s $root_dir\tests -p "test_*.py"
Pause