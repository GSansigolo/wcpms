#
# This file is part of phenometrics.
# Copyright (C) 2026 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Command line interface for the phenometrics client."""

import click
import os

from .wcpms_server import get_phenometrics as run_phenometrics

class Config:
    """A simple decorator class for command line options."""

    def __init__(self):
        """Initialization of Config decorator."""
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@click.version_option()
@pass_config
def cli(config, verbose):
    """wcpms on command line."""
    config.verbose = verbose


@cli.command()
@click.option('--collection',
              required=True,
              help='STAC / Dataset collection ID')
@click.option('--data-dir',
              type=click.Path(exists=True, file_okay=False, path_type=str),
              default='.',
              show_default=True,
              help='Directory containing input data')
@click.option("--bbox", 
              type=click.STRING, 
              required=True,
              help='Bounding box as "minx,miny,maxx,maxy"')
@click.option('--band',
              'bands',
              multiple=True,
              default=["B04", "B08"],
              show_default=True,
              help='Band name (repeatable). E.g. --band B04 --band B08')
@pass_config
def datacube_phenometrics(
    config: Config,
    collection,
    data_dir,
    bbox,
    bands,
):
    """
    Generate phenometrics from a local data cube.
    """
    
    # Parse the bounding box string into a list of floats
    try:
        bbox_list = [float(coord.strip()) for coord in bbox.split(',')]
        if len(bbox_list) != 4:
            raise ValueError
    except ValueError:
        raise click.UsageError(
            'Invalid --bbox format. Please use "minx,miny,maxx,maxy" with numerical values.'
        )

    if config.verbose:
        click.secho(f'Collection: {collection}', fg='cyan', bold=True)
        click.secho(f'Data Directory: {data_dir}', fg='cyan')
        click.secho(f'Bounding Box: {bbox_list}', fg='cyan')
        click.secho(f'Bands: {list(bands)}', fg='cyan')
        click.secho('Working on phenometrics extraction...', fg='cyan')

    result = run_phenometrics(
        collection=collection,
        data_dir=data_dir,
        bbox=bbox_list,
        bands=list(bands)
    )

    if config.verbose:
        click.secho('Finished!', fg='green', bold=True)

    return result