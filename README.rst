..
    This file is part of Python Client Library for WCPMS.
    Copyright (C) 2024 INPE.

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


=================================================
Web Crop Phenology Metrics Service
=================================================


.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
        :target: https://github.com/brazil-data-cube/wcpms.py/blob/master/LICENSE
        :alt: Software License


.. image:: https://readthedocs.org/projects/wcpms/badge/?version=latest
        :target: https://wcpms.readthedocs.io/en/latest/
        :alt: Documentation Status


.. image:: https://img.shields.io/badge/lifecycle-stable-green.svg
        :target: https://www.tidyverse.org/lifecycle/#stable
        :alt: Software Life Cycle


.. image:: https://img.shields.io/github/tag/brazil-data-cube/wcpms.py.svg
        :target: https://github.com/brazil-data-cube/wcpms.py/releases
        :alt: Release


.. image:: https://img.shields.io/pypi/v/wcpms
        :target: https://pypi.org/project/wcpms/
        :alt: Python Package Index


.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord


About
=====

With the increasing availability of Earth Observation (EO) data, the demand for validation using land surface phenology is so important that CEOS (Committee on Earth Observation Satellites) has launched a mission in the Land Product Validation subgroup. 


Phenology is the study of timing recurrent biological events. It is an important indicator of annual plant growth. A key requirement for calculating phenology metrics is the availability of time series with high observation frequency. One concept that facilitates the retrieval of time series from EO data products is data cubes. Data cubes are analysis-ready data (ARD) image collections that have been modeled and organized as multidimensional data cubes. 


Although there are many implementations for estimating crop phenology based on remote sensing data, such as CropPhenology, Digital Earth Australia (DEA) or TIMESAT, these implementations require package installation and programming skills from the analysts to use it. In this paper, we propose a web service to minimize these efforts. 


In this context, the Web Crop Phenology Metrics Service (WCPMS) is open-source web service for calculating phenological metrics based on the Earth Observation Data from the Brazil Data Cube (BDC). It will allow analysts to calculate the metrics from data cubes without downloading big EO datasets to their personal computers. The software will run on the server side, so it doesn’t require package installation. By giving a point or a region, it will retrieve the phenological metrics associated with spatial locations by calculating it using a time series.

WCPMS is based on four operations:

- ``list_collections``: returns in list form the unique identifier of each of the data cubes available in the BDC's SpatioTemporal Asset Catalogs (STAC).

- ``describe``: returns in dictionary format the information on each of the phenology metrics, such as code, name, description and method. 	

- ``phenometrics``: returns in dictionary form all the phenological metrics calculated for the given spatial location. 

- ``phenometrics_region``: returns in list form  dictionary with the phenological metrics calculated for each of the given spatial location based on selected region methodology (all, systematic grid or random grid).


Installation
============

See `INSTALL.rst <./INSTALL.rst>`_.


Using WLTS in the Command Line
==============================

See `CLI.rst <./CLI.rst>`_.


Documentation
=============


WIP


References
==========


WIP


License
=======


.. admonition::
    Copyright (C) 2024 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
