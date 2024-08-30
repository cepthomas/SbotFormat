import subprocess
import string
import re
import enum
import json
import xml
import xml.dom.minidom
import sublime
import sublime_plugin
from . import LuaFormat
from . import sbot_common as sc

# TODO Needs debugging.

FORMAT_SETTINGS_FILE = "SbotFormat.sublime-settings"

# Syntax defs.
SYNTAX_C = 'Packages/C++/C.sublime-syntax'
SYNTAX_CPP = 'Packages/C++/C++.sublime-syntax'
SYNTAX_CS = 'Packages/C#/C#.sublime-syntax'
SYNTAX_JSON = 'Packages/JSON/JSON.sublime-syntax'
SYNTAX_XML = 'Packages/XML/XML.sublime-syntax'
SYNTAX_LUA = 'Packages/Lua/Lua.sublime-syntax'


#-----------------------------------------------------------------------------------
def plugin_loaded():
    '''Called per plugin instance.'''
    sc.info(f'plugin_loaded() {__package__}')


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    '''Ditto.'''
    pass


#-----------------------------------------------------------------------------------
class FormatEvent(sublime_plugin.EventListener):
    ''' Process view events. '''

    def on_init(self, views):
        ''' First thing that happens when plugin/window created. Initialize everything. '''
        settings = sublime.load_settings(FORMAT_SETTINGS_FILE)


#-----------------------------------------------------------------------------------
class SbotFormatJsonCommand(sublime_plugin.TextCommand):
    ''' sbot_format_json'''

    def is_visible(self):
        # return self.view.settings().get('syntax') == SYNTAX_JSON
        return True

    def run(self, edit):
        sres = []
        err = False

        reg = sc.get_sel_regions(self.view)[0]
        s = self.view.substr(reg)
        s = self._do_one(s)
        sres.append(s)
        if s.startswith('Error'):
            err = True

        vnew = sc.create_new_view(self.view.window(), '\n'.join(sres))
        if not err:
            vnew.set_syntax_file(SYNTAX_JSON)

    def _do_one(self, s):
        ''' Clean and reformat the string. Returns the new string. '''

        class ScanState(enum.IntFlag):
            DEFAULT = enum.auto()   # Idle
            STRING = enum.auto()    # Process a quoted string
            LCOMMENT = enum.auto()  # Processing a single line comment
            BCOMMENT = enum.auto()  # Processing a block/multiline comment
            DONE = enum.auto()      # Finito

        # tabWidth = 4
        comment_count = 0
        sreg = []
        state = ScanState.DEFAULT
        current_comment = []
        current_char = -1
        next_char = -1
        escaped = False

        # Index is in cleaned version, value is in original.
        pos_map = []

        # Iterate the string.
        try:
            slen = len(s)
            i = 0
            while i < slen:
                current_char = s[i]
                next_char = s[i + 1] if i < slen - 1 else -1

                # Remove whitespace and transform comments into legal json.
                if state == ScanState.STRING:
                    sreg.append(current_char)
                    pos_map.append(i)
                    # Handle escaped chars.
                    if current_char == '\\':
                        escaped = True
                    elif current_char == '\"':
                        if not escaped:
                            state = ScanState.DEFAULT
                        escaped = False
                    else:
                        escaped = False

                elif state == ScanState.LCOMMENT:
                    # Handle line comments.
                    if current_char == '\n':
                        # End of comment.
                        scom = ''.join(current_comment)
                        stag = f'\"//{comment_count}\":\"{scom}\",'
                        comment_count += 1
                        sreg.append(stag)
                        pos_map.append(i)
                        state = ScanState.DEFAULT
                        current_comment.clear()
                    elif current_char == '\r':
                        # ignore
                        pass
                    else:
                        # Maybe escape.
                        if current_char == '\"' or current_char == '\\':
                            current_comment.append('\\')
                        current_comment.append(current_char)

                elif state == ScanState.BCOMMENT:
                    # Handle block comments.
                    if current_char == '*' and next_char == '/':
                        # End of comment.
                        scom = ''.join(current_comment)
                        stag = f'\"//{comment_count}\":\"{scom}\",'
                        comment_count += 1
                        sreg.append(stag)
                        pos_map.append(i)
                        state = ScanState.DEFAULT
                        current_comment.clear()
                        i += 1  # Skip next char.
                    elif current_char == '\n' or current_char == '\r':
                        # ignore
                        pass
                    else:
                        # Maybe escape.
                        if current_char == '\"' or current_char == '\\':
                            current_comment.append('\\')
                        current_comment.append(current_char)

                elif state == ScanState.DEFAULT:
                    # Check for start of a line comment.
                    if current_char == '/' and next_char == '/':
                        state = ScanState.LCOMMENT
                        current_comment.clear()
                        i += 1  # Skip next char.
                    # Check for start of a block comment.
                    elif current_char == '/' and next_char == '*':
                        state = ScanState.BCOMMENT
                        current_comment.clear()
                        i += 1  # Skip next char.
                    elif current_char == '\"':
                        sreg.append(current_char)
                        pos_map.append(i)
                        state = ScanState.STRING
                    # Skip ws.
                    elif current_char not in string.whitespace:
                        sreg.append(current_char)
                        pos_map.append(i)

                else:  # state == ScanState.DONE:
                    pass
                i += 1  # next

            # Prep for formatting.
            ret = ''.join(sreg)

            # Remove any trailing commas.
            ret = re.sub(',}', '}', ret)
            ret = re.sub(',]', ']', ret)

            # Run it through the formatter.
            ret = json.loads(ret)
            ret = json.dumps(ret, indent=4)

        except json.JSONDecodeError as je:
            # Get some context from the original string.
            context = []
            original_pos = pos_map[je.pos]
            start_pos = max(0, original_pos - 40)
            end_pos = min(len(s) - 1, original_pos + 40)
            context.append(f'Json Error: {je.msg} pos: {original_pos}')
            context.append(s[start_pos:original_pos])
            context.append('---------here----------')
            context.append(s[original_pos:end_pos])
            ret = '\n'.join(context)

        return ret


#-----------------------------------------------------------------------------------
class SbotFormatXmlCommand(sublime_plugin.TextCommand):
    ''' sbot_format_xml'''

    def is_visible(self):
        return self.view.settings().get('syntax') == SYNTAX_XML

    def run(self, edit):
        err = False

        settings = sublime.load_settings(FORMAT_SETTINGS_FILE)
        reg = sc.get_sel_regions(self.view)[0]
        s = self.view.substr(reg)
        s = self._do_one(s, ' ' * settings.get('tab_size'))
        if s.startswith('Error'):
            err = True

        vnew = sc.create_new_view(self.view.window(), s)
        if not err:
            vnew.set_syntax_file(SYNTAX_XML)

    def _do_one(self, s, sindent):
        ''' Clean and reformat the string. Returns the new string. '''

        def clean(node):
            for n in node.childNodes:
                if n.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                    if n.nodeValue:
                        n.nodeValue = n.nodeValue.strip()
                elif n.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                    clean(n)
        
        try:
            top = xml.dom.minidom.parseString(s)
            clean(top)
            top.normalize()
            ret = top.toprettyxml(indent=sindent)
        except Exception as e:
            ret = f"Error: {e}"

        return ret


#-----------------------------------------------------------------------------------
class SbotFormatCxSrcCommand(sublime_plugin.TextCommand):
    ''' sbot_format_cx_src '''

    def is_visible(self):
        syntax = self.view.settings().get('syntax')
        return syntax in [SYNTAX_C, SYNTAX_CPP, SYNTAX_CS]

    def run(self, edit):
        # Current syntax.
        syntax = self.view.settings().get('syntax')

        settings = sublime.load_settings(FORMAT_SETTINGS_FILE)
        reg = sc.get_sel_regions(self.view)[0]
        s = self.view.substr(reg)

        # Build the command. Uses --style=allman --indent=spaces=4 --indent-col1-comments --errors-to-stdout
        sindent = f"-s{settings.get('tab_size')}"
        p = ['astyle', '-A1', sindent, '-Y', '-X']
        if syntax == SYNTAX_CS: # else default of C
            p.append('--mode=cs')

        try:
            cp = subprocess.run(p, input=s, text=True, universal_newlines=True, capture_output=True, shell=True, check=True)
            sout = cp.stdout
        except Exception:
            sout = "Format Cx failed. Is astyle installed and in your path?"

        vnew = sc.create_new_view(self.view.window(), sout)
        vnew.set_syntax_file(syntax)


#-----------------------------------------------------------------------------------
class SbotFormatLuaCommand(sublime_plugin.TextCommand):
    ''' sbot_format_lua '''

    def is_visible(self):
        syntax = self.view.settings().get('syntax')
        return syntax == SYNTAX_LUA #and have_luafmt is True

    def run(self, edit):
        settings = sublime.load_settings(FORMAT_SETTINGS_FILE)
        r = sc.get_sel_regions(self.view)[0]
        self.view.unfold(r)

        # Get lines of view.
        lines = []
        for region in self.view.lines(r):
            cache = self.view.substr(region)
            if len(cache) == 0: cache = ' '
            lines.append(cache)

        sout = LuaFormat.lua_format(lines, settings)
        vnew = sc.create_new_view(self.view.window(), sout)
        vnew.set_syntax_file(SYNTAX_LUA)
