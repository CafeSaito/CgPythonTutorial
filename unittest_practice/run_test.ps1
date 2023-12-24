$root_dir = Split-Path $MyInvocation.MyCommand.Path

# Join-Pathはパスを結合する関数です。単純に文字列連結でもokです。eg) $scripts_dir = $root_dir + "\scripts"
$scripts_dir = Join-Path $root_dir "scripts"
$test_dir = Join-Path $root_dir "tests"

$env:PYTHONPATH = $scripts_dir

#-m unittest discoverはPythonの標準ライブラリであるunittestを使ってテストを発見し実行することを指示します。
#-sオプションはテストを検索するディレクトリを指定
& "C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe" -m unittest discover -s $test_dir
