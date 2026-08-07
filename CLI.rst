..
    This file is part of Python phenometrics package.
    Copyright (C) 2026 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


Running WCPMS Server in the Command Line
========================================

The ``wcpms_server`` package installs a command line tool named ``wcpms_server`` that allows 
users to generate phenological metrics from a local data cube.


If you want to know the wcpms version, use the option ``--version``::

    wcpms_server --version


Datacube WCPMS command
-----------------------------

The main command provided by the CLI is ``datacube-phenometrics``, which generates 
WCPMS for a given spatial extent and collection.

A minimal example is shown below::

    wcpms_server datacube-phenometrics \
      --collection S2-16D-2 \
      --data-dir ./S2_10D \
      --bbox "-46.6507,-23.9681,-46.2772,-23.5992" \
      --band B04 \
      --band B08 