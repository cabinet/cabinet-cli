# Cabinet CLI

An CLI for Cabinet.

## Installation

```
pip install -r requiremen.txt
```

## Configuration

By default, the cli will read the configuration file located on `~/.config/cabinet/cli.ini`. So far, it only the following parameters are configurable:

* `account` : The users account.
* `default_vault` : The default vault name to be used if none is specified.

The configuration file (`cli.ini`) looks like:

```ini
[Credentials]
# The cabinet account
account=facu
# The default vault to be used if none is specified
default_vault=awesome-vault
```

## CLI Sections

The command containse two sections:

* `search` : For seeking for a stored item
* `item` : For adding and getting an specific item

```profile
usage: cabinet (sub-commands ...) [options ...] {arguments ...}

Cabinet's cli client for managing vaults.

commands:

  item
    Item Controller

  search
    Search Controller

optional arguments:
  -h, --help     show this help message and exit
  --debug        toggle debug output
  --quiet        suppress all output
  -v, --version  show program's version number and exit
```

### Searching

```profile
usage: cabinet (sub-commands ...) [options ...] {arguments ...}

Search Controller

commands:

  default
    Get all the items in the vault.

positional arguments:
  extra_arguments

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -a ACCOUNT, --account ACCOUNT
                        Use this account to authenticate
  -v VAULT, --vault VAULT
                        Use this vault
  -s, --show-tags       Show items with tags.
  -t TAG, --tag TAG     Filter by tag
  --tags TAGS           Filter by multiple tags
```

### Adding/Getting

```profile
usage: cabinet (sub-commands ...) [options ...] {arguments ...}

Item Controller

commands:

  add
    Add an item to the vault.

  get
    Get an item from the vault.

positional arguments:
  name                  The item name.

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -a ACCOUNT, --account ACCOUNT
                        Use this account to authenticate
  -v VAULT, --vault VAULT
                        Use this vault
  -t TAG, --tag TAG     Add a tag to the item
  --tags TAGS           Add multiple separated comma tags
  --content CONTENT     Add content to the item
```
