import re

from maya import cmds


class NodeModel:
    suffix_patterns = {
        "mesh": "geo",
        "joint": "jnt",
        "camera": "cam",
        'locator': 'loc'
    }

    def rename(self, new_name):
        # 選択中のものを一覧で取得する
        selections = cmds.ls(sl=True)

        # 選択されていない場合はエラーとし、その旨を返しつつ、以降の処理を実行できないようにします。
        if not selections:
            message = "Please Select node"
            return message

        # 新しい名前が空文字の場合はエラーとし、その旨を返しつつ、以降の処理を実行できないようにします。
        if not new_name:
            message = "Node name cannot be empty"
            return message

        # 　名前が変わらない場合はエラーする
        if selections[0] == new_name:
            message = "Node name is not changed"
            return message

        # 英数字とアンダースコア以外はエラーとし、その旨を返しつつ、以降の処理を実行できないようにします。
        valid_name_pattern = re.compile(r'^\w+$')
        if not valid_name_pattern.match(new_name):
            message = "Node name must be alphanumeric and underscore"
            return message

        # new name が既に存在する場合はエラーする
        if cmds.objExists(new_name):
            message = "Node name already exists"
            return message

        # ノードタイプを取得する。シェイプがある場合には、そのタイプを取得する。
        shapes = cmds.listRelatives(selections[0], shapes=True)
        if shapes:
            node_type = cmds.nodeType(shapes[0])
        else:
            node_type = cmds.nodeType(selections[0])

        # ノードのタイプによってはサフィックスを付ける
        if node_type in self.suffix_patterns:
            new_name += "_" + self.suffix_patterns[node_type]

        # エラーチェックを全て通過したならば、リネームを実行する
        cmds.rename(selections[0], new_name)
        print("Renamed: " + selections[0] + " -> " + new_name)
