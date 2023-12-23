import unittest

from timecode_to_fps import timecode_to_fps


class TestTimeCodeToFps(unittest.TestCase):

    def test_time_code_to_fps(self):
        time_code = '00:00:01:00'
        frame_rate = 30
        fps = timecode_to_fps(time_code, frame_rate)
        self.assertEqual(30, fps)

        frame_rate = 60
        fps = timecode_to_fps(time_code, frame_rate)
        self.assertEqual(60, fps)

        frame_rate = ''
        self.assertRaises(TypeError, timecode_to_fps, time_code, frame_rate)
