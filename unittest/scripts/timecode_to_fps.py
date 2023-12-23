"""
これは、テスト用のサンプルです。
タイムコードをフレームレートに変換するスクリプトです。
フェイシャルキャプチャした情報を、mayaのタイムラインへ読み込む場合に必要になることがあります。
"""

import datetime


def timecode_to_fps(time_code, frame_rate):
    time_code_components = time_code.split(':')
    time_delta = datetime.timedelta(hours=int(time_code_components[0]),
                                    minutes=int(time_code_components[1]),
                                    seconds=int(time_code_components[2]) + float(time_code_components[3]) / 60.0)
    fps = time_delta.total_seconds() * frame_rate

    return fps
