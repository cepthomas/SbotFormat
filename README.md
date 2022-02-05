# What It Is
Sublime Text plugin to do simple formatting of common source code files.
- Prettify json and xml and show in a new view.
- Was also going to handle html but it's easier to use external or online formatter for this very occasional need.
- Also C family files using AStyle (must be in your path).

Built for Windows and ST4. Other OSes and ST versions will require some hacking.

## Commands
| Command                  | Description |
|:--------                 |:-------     |
| sbot_format_json         | Format json content - makes C/C++ comments into valid json elements and removes any trailing commas |
| sbot_format_xml          | Format xml content |
| sbot_format_cx_src       | Format C/C++/C# content |

## Settings
| Setting                  | Description |
|:--------                 |:-------     |
| sel_all                  | Option for selection defaults: if true and no user selection, assumes the whole document (like ST) |

