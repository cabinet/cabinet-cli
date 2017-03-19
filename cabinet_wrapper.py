#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from sys import exit
from getpass import getpass

from utils import get_configs

from cabinet import Cabinet


class CabinetWrapper:
    """
    A wrapper to easely use the cabinet library.

    TODO: In the future we should try moving this all to the library.
    """

    def __init__(self, vault_name=None, account_id=None):
        """
        Initialize the cabinet instance using the given vault/account or from
        the configuration file if you don't specify them.

        This will prompt for the account password to open the vault.

        :param vault_name: The name of the vault
        :type: str

        :param account_id:
        :type: str
        """
        join = os.path.join
        self.base_path = join(os.path.expanduser('~'), '.config', 'cabinet')
        self.config_file = join(self.base_path, 'cli.ini')
        self.secrets_path = join(self.base_path, 'secrets')
        self.vault_path = join(self.base_path, 'vaults')

        self._ready = self._load_credentials(vault_name, account_id)

    def _load_credentials(self, vault_name=None, account_id=None):
        """
        It loads the vault name and account id from the configuration, then
        it overrides the configuration with the cli options (if entered).
        Finally, it prompts for the account password and opens the vault.

        Params:
        :param vault_name: The name of the vault
        :type: String
        :param account_id:
        :type: String

        TODO: Move the print and die to utils
        """
        config = get_configs(self.config_file)

        if vault_name:
            self.vault_name = vault_name
        elif config.get('vault_name'):
            self.vault_name = config.get('vault_name')
        else:
            print('Vault not specified')
            exit()

        if account_id:
            self.account_id = account_id
        elif config.get('account_id'):
            self.account_id = config.get('account_id')
        else:
            print('Account not specified')
            exit()

        self.password = getpass()
        return self.open_vault(self.account_id, self.password, self.vault_name)

    def open_vault(self, account_id, password, vault_name):
        """
        Open the vault identified by the vault_name.

        Params:
        :param account_id:
        :type: String
        :param password:
        :type: String
        :param vault_name: The name of the vault
        :type: String

        TODO: Implement account_id/password/vault validation and opening
        """

        self.cab = Cabinet(account_id, password, self.secrets_path)
        self.cab.open(vault_name, self.vault_path)

        # TODO: Add open check. For this, the vault should verify keys
        return True

    def get_by_tags(self, tags):
        """
        Get all the items from the vault without the 'content' (i.e: only name
        and tags) that matches all the given tags.

        :returns: The list of items
        :type: List of Dictionaries.
        """
        return self.cab.get_by_tags(tags)

    def get_all(self):
        """
        Get all the items from the vault without the 'content' (i.e: only name
        and tags).

        :returns: The list of items
        :type: List of Dictionaries.
        """
        return self.cab.get_all()

    def get_item(self, name):
        """
        Get an item from the vault.

        :param name: The name of the item to recover.
        :type: String

        :returns: The item with the specified name.
        :type: Dictionary
        """
        if self._ready:
            item = self.cab.get(name)
            if item:
                print(item)
            else:
                print('Item with name "{0}" not found!'.format(name))

    def add_item(self, name, tags, content):
        """
        Add an item to the vault.

        :param item: The item's name
        :type: str

        :param tags: The item's tags
        :type: list

        :param content: The item's contents
        :type: any
        """
        if self._ready:
            item = {
                'name': name,
                'tags': tags,
                'content': content
            }
            self.cab.add(item)

    def search(self, tags, show_tags):
        """
        Search for items with the given tags.

        :param tags: the tags to search for
        :type tags: list

        :param show_tags: whether we should show the tags or not
        :type show_tags: bool
        """
        if self._ready:
            item_list = self.get_by_tags(tags)
            print("The following items were found:")
            tag_tpl = " tagged with {1}" if show_tags else ''
            for item in item_list:
                print(('\t-"{0}"' + tag_tpl).format(item['name'],
                                                    item['tags']))
