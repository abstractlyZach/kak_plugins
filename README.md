[![Tests](https://github.com/abstractlyZach/kak_plugins/workflows/Tests/badge.svg)](https://github.com/abstractlyZach/kak_plugins/actions?workflow=Tests)
[![PyPI](https://img.shields.io/pypi/v/kak-plugins.svg)](https://pypi.org/project/kak-plugins/)
[![Codecov](https://codecov.io/gh/abstractlyZach/kak_plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/abstractlyZach/kak_plugins)


# Zach's Overengineered Kakoune Plugins
They say that for any given job, if [Python](https://www.python.org/) isn't the best tool for the job, then it's the second-best tool for the job.

[Kakoune](http://kakoune.org/) has a lot of amazing plugins and user-modes, and they're usually not written in Python.

So, since I must be working with the second-best tool for the job, I thought I would go the whole 9 yards and overengineer the h*ck out of it 😉. In true [abstractlyZach](https://www.github.com/abstractlyZach) fashion, this project includes:
- reimplementations of awesome scripts that could be one-liners in `bash` with, like, 5 pipes
- [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)
- readability as a priority
- [composition over inheritance](https://realpython.com/inheritance-composition-python/)
- rigorous testing
- helpful command-line menus
- milliseconds of extra run-time! Python is an interpreted language!
- intense CI practices
- linting and autoformatting
- lots of documentation
- [minimal use of Mocks](https://www.youtube.com/watch?v=rk-f3B-eMkI), maximal use of better test doubles like Fakes and Stubs
- robust error-handling
- fine-grained logging options

Also, I was pretty excited about [kakoune.cr](https://github.com/alexherbo2/kakoune.cr), but I was super fuzzy on how to actually use it. Hopefully these plugins will serve as living documentation on some good ways to leverage this tool.

## Installation
### as a user
I recommend using [pipx](https://pipxproject.github.io/pipx/installation/) for installation. It allows you to install python packages on your machine in separate virtual environments without having to manage the virtual environments yourself. `pip` also works if you prefer that.
```
pipx install kak-plugins
```

### as a developer
We use [poetry](https://python-poetry.org/) to do package and dependency management. For bonus points, install it using `pipx` instead of their recommended method.
```
pipx install poetry

git clone https://github.com/abstractlyZach/kak_plugins.git
cd kak_plugins

poetry install
```

## Dependencies
* [Kakoune](http://kakoune.org/), of course 😄
* [kakoune.cr](https://github.com/alexherbo2/kakoune.cr)
    * enables us to retrieve info from Kakoune
    * provides an interface to control Kakoune
* A clipboard command-line utility. I use these:
    * `pbcopy` for OSX
    * [xclip](https://github.com/astrand/xclip) for Linux
    * [wl-clipboard](https://github.com/bugaevc/wl-clipboard) for Wayland (if you don't know what this is and you use Linux, you'll probably use `xclip`)


## Setup
There are some environment varibles you will need to define in order to use these plugins. You would probably define these in your `~/.bashrc`, `zshrc`, or `~/.profile`. I define mine [here](https://github.com/abstractlyZach/dotfiles/blob/master/common/.profile)
```
# program that reads stdin and writes to your system clipboard
export CLIPBOARD="pbcopy"
```

# Plugins

## github-permalink
Create a permalink to a file on GitHub with lines pre-selected. [Example](https://github.com/abstractlyZach/kak_plugins/blob/main/src/kak_plugins/github_permalink.py#L26-L53). The selected line or range of lines matches your current selection in Kakoune and will be copied to your clipboard program.
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
