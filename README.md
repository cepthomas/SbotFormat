# What It Is
Sublime Text plugin to do simple formatting of common source code files. Doesn't replace the file, shows in a new view.

- Prettify json, handles comments and trailing commas.
- Prettify xmliew.
- Prettify C family (C/C++/C#) files using AStyle (must be in your path).

Built for Windows and ST4. Other OSes and ST versions will require some hacking.

## Commands
| Command                  | Implementation | Description |
|:--------                 |:-------        |:-------     |
| sbot_format_json         | Context        | Format json content - makes C/C++ comments into valid json elements and removes any trailing commas |
| sbot_format_xml          | Context        | Format xml content |
| sbot_format_cx_src       | Context        | Format C/C++/C# content |

## Settings
| Setting                  | Description |
|:--------                 |:-------     |
| sel_all                  | Option for selection defaults: if true and no user selection, assumes the whole document (like ST) |

