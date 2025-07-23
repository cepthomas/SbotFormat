# SbotFormat

Sublime Text plugin to do simple formatting of common source code files. Doesn't replace the existing file,
shows the content in a new view.

- Prettify json, turns C/C++ style comments into valid json elements, and removes trailing commas.
- Prettify xml.
- Prettify C family (C/C++/C#) files using [AStyle](https://astyle.sourceforge.net/) (which must be installed and in your path). Note: I started with the python astyle module but didn't care for it.
- Prettify lua - uses main code from [LuaFormat](https://github.com/floydawong/LuaFormat) (MIT license). Gets a bit confused sometimes.

Built for ST4 on Windows. Linux and OSX should be ok but are minimally tested - PRs welcome.


## Commands and Menus

| Command                  | Description                   | Args             |
| :--------                | :-------                      | :--------        |
| sbot_format_json         | Format json content           |                  |
| sbot_format_xml          | Format xml content            |                  |
| sbot_format_cx_src       | Format C/C++/C# content       |                  |
| sbot_format_lua          | Format lua content            |                  |


There is no default `Context.sublime-menu` file in this plugin.
Add the commands you like to your own `User\Context.sublime-menu` file. Typical entries are:
``` json
{ "caption": "Format",
    "children":
    [
        { "caption": "Format C/C++/C#", "command": "sbot_format_cx_src" },
        { "caption": "Format json", "command": "sbot_format_json" },
        { "caption": "Format xml", "command": "sbot_format_xml" },
        { "caption": "Format lua", "command": "sbot_format_lua" },
    ]
}
```

## Settings

| Setting            | Description         | Options                                     |
| :--------          | :-------            | :------                                     |
| tab_size           | Spaces per tab      | Currently applies to all file types         |

## Notes

- `sbot_common.py` contains miscellaneous common components primarily for internal use by the sbot family.
  This includes a very simple logger primarily for user-facing information, syntax errors and the like.
  Log file is in `<ST_PACKAGES_DIR>\User\SbotFormat\SbotFormat.log`.
