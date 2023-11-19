# Minecraft dictionary for fcitx5-pinyin / 用于 fcitx5 拼音输入法的 Minecraft 词典

## Upstream projects / 上游项目

### mw2fcitx
- Original name `fcitx5-pinyin-moegirl`. I am using the old [v1 branch](https://github.com/outloudvi/mw2fcitx/tree/v1).

### Minecraft Wiki
- All entries come from page titles of [中文 Minecraft Wiki](https://zh.minecraft.wiki/).
- Thanks to all contributors for releasing the content in a free license and providing the API to download!

## Installation / 安装

### AUR / [archlinuxcn] repo

- TODO.

### From Github Release

1. Download latest version of `minecraft-cn.dict` (for fcitx5-pinyin) from releases.
2. Copy it to `/usr/share/fcitx5/pinyin/dictionaries/` (for fcitx5-pinyin) or import it from fcitx5 config tool.

## Build Requirements

- libime (https://github.com/fcitx/libime/)

Python modules:

- opencc (https://pypi.org/project/OpenCC/)
- pypinyin (https://pypi.org/project/pypinyin/)

Manual Build & Installation:

Please read the `Makefile` to figure it out.

## License

### Code in this project

- Unlicense. This is the choice of mw2fcitx and I might change it in the future.

### Generated minecraft dictionary

- CC BY-NC-SA 3.0 according to <https://zh.minecraft.wiki/w/Minecraft_Wiki:著作权>

