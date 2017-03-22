# Cabinet CLI

An CLI for Cabinet.

## Installation

Get dependencies:

```
pip install -r requirements.txt
```

You can also install the cli as a local command inside the virtualenv thanks to the `setup.py` configuration.

```
pip install --editable .
```

You will have a `cab` command to use.


## Configuration

By default, the cli will read the configuration file located on `~/.config/cabinet/cli.ini`. So far, it only the following parameters are configurable:

* `account` : The user's account.
* `vault` : The default vault name to be used if none is specified.

The configuration file (`cli.ini`) looks like:

```ini
[Credentials]
# The cabinet account
account=facu
# The default vault to be used if none is specified
vault=awesome-vault
```

## CLI Overview

This are the now implemented features on the cli, hopefully this is self explanatory.

```
➜ cab
Usage: cab [OPTIONS] COMMAND [ARGS]...

Options:
  -a, --account TEXT  Specify an account to use
  -v, --vault TEXT    Specify a vault to use
  --help              Show this message and exit.

Commands:
  add     Add an item to cabinet
  get     Get an item from cabinet
  rm      [not implemented] Remove an item from cabinet
  search  Item searching on cabinet

➜ cab add --help
Usage: cab add [OPTIONS] NAME

  Add an item to cabinet

Options:
  -t, --tag TEXT      Specify tags for the item
  -c, --content TEXT  The item content
  -i, --from-stdin    Get the content from stdin
  -e, --use-editor    Use the default editor for entering the content
  --help              Show this message and exit.

➜ cab get --help
Usage: cab get [OPTIONS] NAME

  Get an item from cabinet

Options:
  -a, --all  Print the item with all its information (tags and name)
  --help  Show this message and exit.

➜ cab search --help
Usage: cab search [OPTIONS]

  Item searching on cabinet

Options:
  -t, --tag TEXT   Specify tags for the item
  -s, --show-tags  Show items with tags.
  --help           Show this message and exit.
```
