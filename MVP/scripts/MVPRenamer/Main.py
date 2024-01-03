def run_main():
    from MVPRenamer.Model.NodeModel import NodeModel
    from MVPRenamer.Presenter.Presenter import Presenter
    from MVPRenamer.View.ConfirmView import ConfirmView
    from MVPRenamer.View.MainWindow import MainWindow

    # メインウィンドウを作成します。
    main_window = MainWindow()

    # 確認ダイアログを作成します。
    confirm_view = ConfirmView()

    # ノードモデルを作成します。
    node_model = NodeModel()

    # プレゼンターを作成します。
    presenter = Presenter(main_window, confirm_view, node_model)
    presenter.setup()


if __name__ == '__main__':
    import sys

    # ローカルで実行する場合のインポート処理。パスは適宜書き換えてください。
    sys.path.append(r'D:\cafegroup\CgPythonTutorial\MVP\scripts')
    try:
        import importlib

        importlib.reload(sys.modules['MVPRenamer.View.MainWindow'])
        importlib.reload(sys.modules['MVPRenamer.View.ConfirmView'])
        importlib.reload(sys.modules['MVPRenamer.Model.NodeModel'])
    except KeyError:
        pass

    run_main()
