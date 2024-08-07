# Sbot Format

Sublime Text plugin to do simple formatting of common source code files. Doesn't replace the existing file,
shows the content in a new view.

Built for ST4 on Windows and Linux.

- Prettify json, turns C/C++ style comments into valid json elements, and removes trailing commas.
- Prettify xml.
- Prettify C family (C/C++/C#) files using [AStyle](https://astyle.sourceforge.net/) (which must be installed and in your path). Note: I started with the python astyle module but didn't care for it.
- Prettify lua - uses main code from [LuaFormat](https://github.com/floydawong/LuaFormat) (MIT license). Gets a bit confused sometimes.


## Commands

| Command                  | Type     | Description                   | Args             |
| :--------                | :------- | :-------                      | :--------        |
| sbot_format_json         | Context  | Format json content           |                  |
| sbot_format_xml          | Context  | Format xml content            |                  |
| sbot_format_cx_src       | Context  | Format C/C++/C# content       |                  |
| sbot_format_lua          | Context  | Format lua content            |                  |

## Settings

| Setting            | Description         | Options                                     |
| :--------          | :-------            | :------                                     |
| tab_size           | Spaces per tab      | Currently applies to all file types         |
