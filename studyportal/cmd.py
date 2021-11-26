import click
from .init import driveinit
from .scripts.load import load_resources
from .scripts.setup import setup_folder
from .scripts.sync import sync_drive
from .scripts.permissions import update_file_perms


@click.command()
@click.option(
    '-i', '--init', is_flag=True, help='Initialize Google Drive Service'
)
@click.option(
    '--load',
    is_flag=True,
    help='Add departments and courses to the database'
)
@click.option(
    '--setup',
    is_flag=True,
    help='Create "study" folder structure in the Drive and translate folder to structure.json'
)
@click.option(
    '--sync',
    is_flag=True,
    help='Sync studyportal database with files stored in Google Drive folder'
)
@click.option(
    '--perms',
    is_flag=True,
    help='Updates the permissions of the files in the drive'
)
def cli(init, load, setup, sync, perms):
    """Runs utility suite for managing studyportal"""
    click.echo('\nStudyportal-Utils: \n')
    click.echo('Utility suite for deployment and management of studyportal.')
    click.echo('Run with --help to view list of commands\n')
    if init:
        service = driveinit()
    if load:
        load_resources()
    elif setup:
        service = driveinit()
        setup_folder(service)
    elif sync:
        service = driveinit()
        sync_drive(service)
    elif perms:
        service = driveinit()
        update_file_perms(service)

