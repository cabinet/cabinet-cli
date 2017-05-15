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

    def __init__(self, vault_name=None, account_id=None, password=None):
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

        self._ready = self._load_credentials(vault_name, account_id, password)

    def _load_credentials(self, vault_name=None, account_id=None, password=None):
        """
        It loads the vault name and account id from the configuration, then
        it overrides the configuration with the cli options (if entered).
        Finally, it prompts for the account password and opens the vault.

        Params:
        :param vault_name: The name of the vault
        :type: str
        :param account_id:
        :type: str

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

        is_open = False
        for i in range(3):
            try:
                if password is None:
                    self.password = getpass()
                else:
                    self.password = password

                is_open = self.open_vault(self.account_id, self.password,
                                          self.vault_name)
                break
            except Exception as e:
                msg = "There was an error opening the vault."
                if i < 2:
                    msg += " Wrong password? Try again or Ctrl+C to quit."
                else:
                    msg += " Exit."
                print(msg)

        return is_open

    def open_vault(self, account_id, password, vault_name):
        """
        Open the vault identified by the vault_name.

        Params:
        :param account_id:
        :type: str
        :param password:
        :type: str
        :param vault_name: The name of the vault
        :type: str

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
        :type: list of dicts.
        """
        return self.cab.get_by_tags(tags)

    def get_tags(self):
        """
        Get all the tags from the vault.
        """
        tags = self.cab.get_tags()
        print("Tags:", ','.join(tags))

    def get_all(self):
        """
        Get all the items from the vault without the 'content' (i.e: only name
        and tags).

        :returns: The list of items
        :type: list of dicts.
        """
        return self.cab.get_all()

    def get_item(self, name, print_all):
        """
        Get an item from the vault.

        :param name: The name of the item to recover.
        :type: str
        :param print_all: Print all the information related to the item.
        :type: bool

        :returns: The item with the specified name.
        :type: dict
        """
        if self._ready:
            item = self.cab.get(name)

            if not item:
                print('Item with name "{0}" not found!'.format(name))
                return

            if print_all:
                print("Name: {0}\nTags: {1}\nContent: {2}"
                      .format(name, item['tags'], item['content']))
            else:
                print(item['content'])

    def get_item_content(self, name):
        """
        Get the content of an item from the vault.

        :param name: The name of the item to recover.
        :type: str

        :returns: The item's content.
        :type: str
        """
        if self._ready:
            item = self.cab.get(name)

            if not item:
                print('Item with name "{0}" not found!'.format(name))
                return

            return item['content']

    def get_item_tags(self, name):
        """
        Get the tags of an item from the vault.

        :param name: The name of the item to recover.
        :type: str

        :returns: The item's tags.
        :type: list
        """
        if self._ready:
            item = self.cab.get(name)

            if not item:
                print('Item with name "{0}" not found!'.format(name))
                return

            return item['tags']

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

    def update(self, name, tags, content):
        if self._ready:
            self.cab.update(name, content, tags)

    def rename(self, name, new_name):
        if self._ready:
            self.cab.rename(name, new_name)

    def remove(self, name):
        if self._ready:
            self.cab.remove(name)

    def search(self, tags, show_tags):
        """
        Search for items with the given tags.

        :param tags: the tags to search for
        :type tags: list

        :param show_tags: whether we should show the tags or not
        :type show_tags: bool
        """
        if not self._ready:
            return

        item_list = self.get_by_tags(tags)
        for item in item_list:
            line = "{0} \ttags: {1}"

            tags = ", ".join(item['tags'])
            print(line.format(item['name'], tags))
