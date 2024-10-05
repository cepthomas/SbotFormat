import sys
import os
import unittest
from unittest.mock import MagicMock

# Add path to code under test.
cut_path = os.path.join(os.path.dirname(__file__), '..')
if cut_path not in sys.path:
      sys.path.insert(0, cut_path)

# Now import the sublime emulation.
import emu_sublime
import emu_sublime_plugin
sys.modules["sublime"] = emu_sublime
sys.modules["sublime_plugin"] = emu_sublime_plugin

# Now import the code under test.
import sbot_format

import sbot_common as sc


#-----------------------------------------------------------------------------------
class TestFormat(unittest.TestCase):

    def setUp(self):
        mock_settings = {
            "tab_size": 4,
        }
        sublime.load_settings = MagicMock(return_value=mock_settings)

    def tearDown(self):
        pass

    def test_format_json(self):
        v = sublime.View(601)

        with open(r'SbotDev\test_files\messy.json', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sbot_format.SbotFormatJsonCommand(v)
            res = cmd._do_one(s)
            self.assertEqual(res[:50], '{\n    "MarkPitch": {\n        "Original": 0,\n      ')

            # Make it a bad file.
            s = s.replace('\"Original\"', '')
            res = cmd._do_one(s)
            self.assertEqual(res[:50], "Json Error: Expecting property name enclosed in do")

    def test_format_xml(self):
        v = sublime.View(602)

        with open(r'SbotDev\test_files\messy.xml', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sbot_format.SbotFormatXmlCommand(v)
            res = cmd._do_one(s, '    ')

            if 'Error:' in res:
                self.fail(res)
            else:
                self.assertEqual(res[100:150], 'nType="Anti-IgG (PEG)" TestSpec="08 ABSCR4 IgG" Du')

            # Make it a bad file.
            s = s.replace('ColumnType=', '')
            res = cmd._do_one(s, '    ')
            self.assertEqual(res, "Error: not well-formed (invalid token): line 6, column 4")
