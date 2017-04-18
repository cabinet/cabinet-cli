#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click

from sys import stdin
from utils import get_content_from_editor

from cabinet_wrapper import CabinetWrapper


@click.group()
@click.option('account', '-a', '--account',
              help='Specify an account to use')
@click.option('vault', '-v', '--vault',
              help='Specify a vault to use')
@click.pass_context
def cli(ctx, account, vault):
    """Cabinet's command line interface."""
    if ctx.obj is None:
        ctx.obj = {}

    if account or vault:
        click.echo(">> Credentials")
        click.echo("Account:", account)
        click.echo("Vault:", vault)
        ctx.obj['account'] = account
        ctx.obj['vault'] = vault


@cli.command()
@click.argument('name')
@click.option('tags', '-t', '--tag', multiple=True,
              help='Specify tags for the item')
@click.option('content', '-c', '--content',
              help='The item content')
@click.option('from_stdin', '-i', '--from-stdin', is_flag=True,
              help="Get the content from stdin")
@click.option('editor', '-e', '--use-editor', is_flag=True,
              help="Use the default editor for entering the content")
@click.pass_context
def add(ctx, name, tags, content, from_stdin, editor):
    """Add an item to cabinet"""
    click.echo('>> Add item')
    click.echo('Name: {0}'.format(name))
    click.echo('Content: {0}'.format(content))

    if not content:
        if from_stdin:
            content = ""
            for line in stdin:
                content = content + line
        elif editor:
            content = get_content_from_editor()
            print("Content from editor:")
            print(content)
        else:
            click.echo("Error: you need to specify the content")
            return

    if tags:
        click.echo('Tags: %s' % ', '.join(tags))

    account = ctx.obj.get('account')
    vault = ctx.obj.get('vault')
    cab = CabinetWrapper(account, vault)
    cab.add_item(name, tags, content)


@cli.command()
@click.argument('name')
@click.option('tags', '-t', '--tag', multiple=True,
              help='Specify tags for the item')
@click.option('content', '-c', '--content',
              help='The item content')
@click.option('from_stdin', '-i', '--from-stdin', is_flag=True,
              help="Get the content from stdin")
@click.option('editor', '-e', '--use-editor', is_flag=True,
              help="Use the default editor for entering the content")
@click.pass_context
def update(ctx, name, tags, content, from_stdin, editor):
    """Update an existing item"""
    click.echo('>> Edit item')
    click.echo('Name: {0}'.format(name))

    account = ctx.obj.get('account')
    vault = ctx.obj.get('vault')
    cab = CabinetWrapper(account, vault)

    if not content:
        if from_stdin:
            content = ""
            for line in stdin:
                content = content + line
        elif editor:
            current_content = cab.get_item_content(name)
            if current_content:
                content = get_content_from_editor(current_content)
                print("Content from editor:")
                print(content)
        else:
            click.echo("Error: you need to specify the content")
            return

    if content:
        if not tags:
            tags = cab.get_item_tags(name)
        click.echo('Tags: %s' % ', '.join(tags))

        cab.update(name, tags, content)


@cli.command()
@click.argument('name')
@click.argument('new_name')
@click.pass_context
def rename(ctx, name, new_name):
    """Rename an existing item"""
    click.echo('>> Rename item')
    click.echo('Name: {0}'.format(name))
    click.echo('New name: {0}'.format(new_name))

    account = ctx.obj.get('account')
    vault = ctx.obj.get('vault')
    cab = CabinetWrapper(account, vault)
    cab.rename(name, new_name)


@cli.command()
@click.argument('name')
@click.option('print_all', '-a', '--all', is_flag=True,
              help='Print the item with all its information (tags and name)')
@click.pass_context
def get(ctx, name, print_all):
    """Get an item from cabinet"""
    account = ctx.obj.get('account')
    vault = ctx.obj.get('vault')
    cab = CabinetWrapper(account, vault)
    cab.get_item(name, print_all)


@cli.command()
def rm():
    """[not implemented] Remove an item from cabinet"""
    click.echo('Sorry! not implemented yet.')


@cli.command()
@click.pass_context
def tags(ctx):
    """Get tags from cabinet"""
    account = ctx.obj.get('account')
    vault = ctx.obj.get('vault')
    cab = CabinetWrapper(account, vault)
    cab.get_tags()


@cli.command()
@click.option('tags', '-t', '--tag', multiple=True,
              help='Specify tags for the item')
@click.option('show_tags', '-s', '--show-tags', is_flag=True,
              help='Show items with tags.')
@click.pass_context
def search(ctx, tags, show_tags):
    """Item searching on cabinet"""
    if tags:
        click.echo('Tags: %s' % ', '.join(tags))

    account = ctx.obj.get('account')
    vault = ctx.obj.get('vault')
    cab = CabinetWrapper(account, vault)
    cab.search(tags, show_tags)


if __name__ == '__main__':
    cli()
