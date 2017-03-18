#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from sys import exit
from getpass import getpass
from configparser import ConfigParser

from cabinet import Cabinet


class CabinetWrapper:
    """
    A wrapper to easely use the cabinet library.

    TODO: In the future we should try moving this all to the library.
    """

    def __init__(self):
        join = os.path.join
        self.base_path = join(os.path.expanduser('~'), '.config', 'cabinet')
        self.config_file = join(self.base_path, 'cli.ini')
        self.secrets_path = join(self.base_path, 'secrets')
        self.vault_path = join(self.base_path, 'vaults')
        self.config = ConfigParser()
        self.config.read(self.config_file)

    def load_credentials(self, vault_name=None, account_id=None):
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

        if vault_name:
            self.vault_name = vault_name
        elif 'Credentials' in self.config and 'default_vault' in \
                                              self.config['Credentials']:
            self.vault_name = self.config['Credentials']['default_vault']
        else:
            print('Vault not specified')
            exit()

        if account_id:
            self.account_id = account_id
        elif 'Credentials' in self.config and 'account' in \
                                              self.config['Credentials']:
            self.account_id = self.config['Credentials']['account']
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

    def get_item(self, vault_name, account_id, name):
        """
        Get an item from the vault.

        :param name: The name of the item to recover.
        :type: String

        :returns: The item with the specified name.
        :type: Dictionary
        """
        if self.load_credentials(vault_name, account_id):
            item = self.cab.get_item(name)
            if item:
                print(item)
            else:
                print('Item with name "{0}" not found!'.format(name))

        return self.cab.get(name)

    def add_item(self, vault_name, account_id, name, tags, content):
        """
        Add an item to the vault.

        :param item: The item to be added.
        :type: Dictionary
        """
        if self.load_credentials(vault_name, account_id):
            item = {
                'name': name,
                'tags': tags,
                'content': content
            }
            self.cab.add(item)

    def search(self, vault_name, account_id, tags, show_tags):
        if self.load_credentials(vault_name, account_id):
            item_list = self.get_by_tags(tags)
            print("The following items were found:")
            tag_tpl = " tagged with {1}" if show_tags else ''
            for item in item_list:
                print(('\t-"{0}"' + tag_tpl).format(item['name'],
                                                    item['tags']))
