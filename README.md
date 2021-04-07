[![Tests](https://github.com/abstractlyZach/kak_plugins/workflows/Tests/badge.svg)](https://github.com/abstractlyZach/kak_plugins/actions?workflow=Tests)
[![PyPI](https://img.shields.io/pypi/v/kak-plugins.svg)](https://pypi.org/project/kak-plugins/)
[![Codecov](https://codecov.io/gh/abstractlyZach/kak_plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/abstractlyZach/kak_plugins)


# kak_plugins
Zach's plugins for the [Kakoune](http://kakoune.org/) text editor.

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

## Logging
Logs are a good way of getting an idea of what's going on in the code. Logs will be written in a temporary directory in a file that has the name of the plugin. See here for rules on [where you can find logs on your system](https://docs.python.org/3/library/tempfile.html#tempfile.gettempdir)

# Plugins

## github-permalink
Create a permalink to a line or range of lines in a GitHub repo that matches your current selection in Kakoune. Then copy that permalink to your clipboard program.
1. open a file in Kakoune
1. make a selection
1. in normal mode, type `:$ github-permalink`
1. you now have a permalink to your kakoune selection. it should look something like this https://github.com/abstractlyZach/kak_plugins/blob/write-readme/README.md#L40

I like [binding this command](https://github.com/abstractlyZach/dotfiles/blob/master/kak/kakrc#L12) to hotkeys so I can hit 2 buttons and then paste the link into Slack or something.
