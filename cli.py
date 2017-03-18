#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This is the first cli prototype for the cabinet core.
#
# References;
#   argparse : https://docs.python.org/3/library/argparse.html
#   cement   : http://builtoncement.com/2.10/index.html
#
# TODO:
#   - Refactor the code to move each class, utils to its own module.

import argparse

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

from cabinet_wrapper import CabinetWrapper


VERSION = '0.0.1'
BANNER = """
Cabinet command line v{0}
GNU GENERAL PUBLIC LICENSE
""".format(VERSION)


# TODO: Move the types out of this file, to a type folder/file. ###############
def tags_type(value):
    """
    Parse the value to recover a list of tags.

    :param value: The value to parse
    :type: String

    :returns: A list of strings composed by spliting the value by ','.
    :type: List
    """
    try:
        return value.split(',')
    except:
        raise argparse.argumenttypeerror("Multiple tags should be separated by\
                                          comma")


def tuple_type(value):
    """
    Parse the value to recover a tuple

    :param value: The value to parse
    :type: String

    :returns: A tuple of two values composed by spliting the value by ','.
    :type: Tuple
    """
    try:
        key, value = value.split(',')
        return key, value
    except:
        raise argparse.argumenttypeerror("coordinates must be x,y,z")

###############################################################################
# TODO: Refactor this to avoid having this global var

COMMON_ARGS = [
    (['-a', '--account'],
        dict(help='Use this account to authenticate', action='store')),
    (['-v', '--vault'],
        dict(help='Use this vault', action='store'))
]

###############################################################################


class CabinetController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Cabinet's cli client for managing vaults."
        arguments = COMMON_ARGS + [
            (['--version'], dict(action='version', version=BANNER))
        ]

    @expose(hide=True)
    def default(self):
        """Without any parameter, the command will print the help"""
        app.args.print_help()


class ItemController(CementBaseController):
    class Meta:
        label = 'item'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = COMMON_ARGS + [
            (['name'],
             dict(help='The item name.', action='store')),
            (['-t', '--tag'],
             dict(help='Add a tag to the item', action='append')),
            (['--tags'],
             dict(help='Add multiple separated comma tags',
                  type=tags_type, action='store')),
            (['--content'],
             dict(help='Add content to the item',
                  type=tuple_type, action='append'))
        ]

    @expose(help='Get an item from the vault.')
    def get(self):
        """Get an item from the vault"""
        account_id = self.app.pargs.account
        vault_name = self.app.pargs.vault
        name = self.app.pargs.name
        if name:
            self.app.log.debug('Looking for item with name "{0}"'.format(name))
            cab = CabinetWrapper()
            if cab.load_credentials(vault_name, account_id):
                item = cab.get_item(name)
                if item:
                    print(item)
                else:
                    print('Item with name "{0}" not found!'.format(name))

    @expose(help="Add an item to the vault.")
    def add(self):
        """Add an item to the vault"""
        account_id = self.app.pargs.account
        vault_name = self.app.pargs.vault
        name = self.app.pargs.name
        tags = self.app.pargs.tags
        if not tags:
            tags = [] if not self.app.pargs.tag else self.app.pargs.tag
        content = [] if not self.app.pargs.content else self.app.pargs.content

        content_obj = {}
        for key, value in content:
            content_obj[key] = value

        if name:
            cab = CabinetWrapper()
            if cab.load_credentials(vault_name, account_id):
                cab.add_item({
                    'name': name,
                    'tags': tags,
                    'content': content_obj
                })
        else:
            print('Insufficient arguments!')


class SearchController(CementBaseController):
    """The command controller for searching within the vault values"""

    class Meta:
        label = 'search'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = COMMON_ARGS + [
            (['-s', '--show-tags'],
             dict(help='Show items with tags.', action='store_true')),
            (['-t', '--tag'],
             dict(help='Filter by tag', action='append')),
            (['--tags'],
             dict(help='Filter by multiple tags',
                  type=tags_type, action='store')),
            (['extra_arguments'],
             dict(action='store', nargs='*')),
        ]

    # TODO: Think where should go the item filter (In the cabinet or here?)
    @expose(help='Get all the items in the vault.')
    def default(self):
        """Print all the item names (and tags if apply) to stdout."""
        account_id = self.app.pargs.account
        vault_name = self.app.pargs.vault
        tags = self.app.pargs.tags
        if not tags:
            tags = [] if not self.app.pargs.tag else self.app.pargs.tag
        show_tags = self.app.pargs.show_tags

        cab = CabinetWrapper()
        cab.search(vault_name, account_id, tags, show_tags)


class MyApp(CementApp):
    class Meta:
        label = 'cabinet'
        base_controller = 'base'
        handlers = [CabinetController, ItemController, SearchController]


with MyApp() as app:
    app.run()
