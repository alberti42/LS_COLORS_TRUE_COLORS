# LS_COLORS

![Build](https://github.com/trapd00r/LS_COLORS/actions/workflows/build.yaml/badge.svg)

:information_source: This is a fork of [trapd00r/LS_COLORS](https://github.com/trapd00r/LS_COLORS). It adds the [`ansi_256_to_rgb.py`](https://github.com/alberti42/LS_COLORS_TRUE_COLORS/blob/master/ansi_256_to_rgb.py) script and a GitHub action that automatically generates `LS_COLORS_TRUE` from `LS_COLORS`. True colours (24bit encoding) may be preferred for modern terminal emulators that support 24bit colours.

If you use `zinit` as your plugin loader for `zsh`, you can load it with this instructions in your `.zshrc` file:

```zsh
# LS_COLORS theme - download the default profile
zinit wait for light-mode lucid \
    atclone'
      [[ -z ${commands[dircolors]} ]] && local P=${${(M)OSTYPE##darwin}:+g}
      ${P}sed -i  "/^DIR\s/c\DIR 38;2;104;114;255;1" LS_COLORS_TRUE   # adjusts the color of directories
      ${P}sed -i "/^LINK\s/c\LINK 1;36" LS_COLORS_TRUE   # adjusts the color of soft links (alternative -> TARGET)
      ${P}dircolors -b LS_COLORS >! src_colors.zsh
      ${P}dircolors -b LS_COLORS_TRUE >! src_true_colors.zsh
      # For BSD/macOS, include the following two lines
      echo -e "LSCOLORS=exfxcxdxbxegedabagacad\nexport LSCOLORS" >> src_colors.zsh
      echo -e "LSCOLORS=exfxcxdxbxegedabagacad\nexport LSCOLORS" >> src_true_colors.zsh
    ' \
    atinit'
      if [[ "$COLORTERM" == *truecolor* || "$COLORTERM" == *24bit* ]]; then
            # this terminal supports truecolor
            source src_true_colors.zsh
        else
            # Truecolor is not supported
            src_true_colors.zsh
        fi
    ' \
    atpull'%atclone' \
    git \
    id-as'LS_COLORS_TRUE_COLORS' \
    lucid \
    nocompile'!' \
    reset @alberti42/LS_COLORS_TRUE_COLORS
```

---

<!-- mdformat-toc start --slug=github --no-anchors --maxlevel=3 --minlevel=1 -->

- [LS_COLORS](#ls_colors)
  - [What does it look like?](#what-does-it-look-like)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
    - [Arch Linux](#arch-linux)
  - [Information for Developers](#information-for-developers)
  - [Legal](#legal)

<!-- mdformat-toc end -->

This is a collection of extension:color mappings, suitable to use as your
`LS_COLORS` environment variable. Most of them use the extended color map,
described in the ECMA-48 document; in other words, you'll need a terminal
with capabilities of displaying 256 colors.

As of this writing, around 300 different filetypes/extensions is supported.
That's indeed a lot of extensions, but there's a lot more! Your help is greatly
appreciated.

Fork this project on github, add the extensions you are missing, and send a pull
request.

Some guidelines:

For files that usually ends up next to each other, like html, css and js,
try to pick colors that fits in nicely together. Filetypes with multiple
possible extensions, like htm and html, should have the same color.

## What does it look like?

Here's a screenshot _(font and minor color shades, of course, depend on terminal and its configuration)_:

![Screenshot1](docs/static/LS_COLORS.png)

## Dependencies

You need GNU `dircolors` and a compatible directory listing tool, such as GNU
`ls`. Both are available in GNU coreutils.

## Installation

The repo contains two compiled scripts `lscolors.sh` & `lscolors.csh`, which you can download & source directly or point your plugin manager to pick up one of them.

To enable the colors, add the following line to your shell's start-up script:

For Bourne shell (e.g. `~/.bashrc` or `~/.zshrc`):

```
source ~/path/to/lscolors.sh
```

For C shell or [fish shell](https://fishshell.com/) (e.g. `~/.cshrc` or `~/.config/fish/config.fish`):

```
source ~/path/to/lscolors.csh
```

If you prefer to manually generate these files, an installation script is provided with this repository:

```console
$ mkdir /tmp/LS_COLORS && curl -L https://api.github.com/repos/trapd00r/LS_COLORS/tarball/master | tar xzf - --directory=/tmp/LS_COLORS --strip=1
$ ( cd /tmp/LS_COLORS && make install )
To enable the colors, add the following line to your shell's start-up script:

For Bourne shell (e.g. ~/.bashrc or ~/.zshrc):
  source "~/.local/share/lscolors.sh"

For C shell (e.g. ~/.cshrc):
  source "~/.local/share/lscolors.csh"
$
```

### Arch Linux

Arch Linux users can install the [`lscolors-git`][3] package from the AUR for easy
integration with bash, csh, or zsh.

## Information for Developers

There's a [library][1] I've written that lets you use various LS COLORS on
arbitrary files and directories. A simple implementation can be found [here][2].

Using this, you can do

```shell
find $HOME -maxdepth 1  | ls_color

mpc search artist Laleh | ls_color
```

... and so on.

## Legal

© Copyright 2014-2022 Magnus Woldrich.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the Perl Artistic License for more details.

This program is free software: you can redistribute it and/or modify it under
the terms of the Perl Artistic License as published by the Perl Foundation,
either version 1.0 of the License, or (at your option) any later version.

You should have received a copy of the Perl Artistic License along
with this program.  If not, see <http://www.perlfoundation.org/artistic_license_1_0>.

[1]: https://github.com/trapd00r/File-LsColor
[2]: https://github.com/trapd00r/File-LsColor/tree/master/bin
[3]: https://aur.archlinux.org/packages/lscolors-git
