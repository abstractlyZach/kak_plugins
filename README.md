[![Tests](https://github.com/abstractlyZach/kak_plugins/workflows/Tests/badge.svg)](https://github.com/abstractlyZach/kak_plugins/actions?workflow=Tests)
[![PyPI](https://img.shields.io/pypi/v/kak-plugins.svg)](https://pypi.org/project/kak-plugins/)
[![Codecov](https://codecov.io/gh/abstractlyZach/kak_plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/abstractlyZach/kak_plugins)


# Zach's Overengineered Kakoune Plugins
I loved seeing the plugins that people write for [Kakoune](http://kakoune.org/), so I decided to write some on my own, but with extreme gusto. Sure, you could probaly accomplish the same results with a string of 7 shell commands, but where's the fun in that when you could have rigorous testing, fancy documentation, interactive menus and debugging, and powerful continuous integration?!

## Installation
I recommend using [pipx](https://pipxproject.github.io/pipx/installation/) for installation. It allows you to install python packages on your machine in separate virtual environments without having to manage the virtual environments yourself. `pip` also works if you prefer that.
```
pipx install kak_plugins
```

## Dependencies
* [Kakoune](http://kakoune.org/) of course
* [kakoune.cr](https://github.com/alexherbo2/kakoune.cr)
    * enables us to retrieve info from Kakoune
    * provides an interface to control Kakoune
* A clipboard command-line utility. I use these:
    * `pbcopy` for OSX
    * [xclip](https://github.com/astrand/xclip) for Linux
    * [wl-clipboard](https://github.com/bugaevc/wl-clipboard) for Wayland (if you don't know what this is and you use Linux, you'll probably use `xclip`)


## Setup
There are some environment varibles you will need to define in order to use these plugins. You would probably define these in your `~/.bashrc`, `zshrc`, or `~/.profile`. I define mine [here](https://github.com/abstractlyZach/dotfiles/blob/master/common/.profile]
```
# program that reads stdin and writes to your system clipboard
export CLIPBOARD="pbcopy"
```

# Plugins

## github-permalink
Create a permalink to a line or range of lines in a GitHub repo that matches your current selection in Kakoune. Then copy that permalink to your clipboard program.
```
github-permalink --help
```

### in kak
This method is great for using in your everyday editing

1. open a file in Kakoune
1. make a selection
1. in normal mode, use `:$ github-permalink`
1. you now have a permalink to your kakoune selection. it should look something like this https://github.com/abstractlyZach/kak_plugins/blob/write-readme/README.md#L40

I like [binding this command](https://github.com/abstractlyZach/dotfiles/blob/master/kak/kakrc#L12) to hotkeys so I can hit 2 buttons and then paste the link into Slack or something.

### in a terminal
This method is great for learning, development, and debugging

1. open a file in kakoune
1. make a selection
1. open a connected terminal. there are a couple of recommended methods
    * use `:>` in normal mode
    * [kcr-fzf-shell](https://github.com/alexherbo2/kakoune.cr/blob/master/share/kcr/commands/fzf/kcr-fzf-shell)
1. `github-permalink --help`
