#
# This file is part of WCPMS.
# Copyright (C) 2024 INPE.
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
ARG BASE_IMAGE=python:3.11
FROM ${BASE_IMAGE}

ARG GIT_COMMIT=unknown

# Image metadata
LABEL "org.repo.maintainer"="Brazil Data Cube <brazildatacube@inpe.br>"
LABEL "org.repo.title"="Docker image for WCPMS Server"
LABEL "org.repo.description"="Docker image for Web Crop Phenology Metrics Service (WCPMS) for Brazil Data Cube."
LABEL "org.repo.git_commit"="${GIT_COMMIT}"
LABEL "org.repo.licenses"="GPLv3"

# Build arguments
ARG BDC_WCPMS_VERSION="1.0.0"
ARG BDC_WCPMS_INSTALL_PATH="/opt/wcpms/${BDC_WCPMS_VERSION}"

COPY . ${BDC_WCPMS_INSTALL_PATH}
WORKDIR ${BDC_WCPMS_INSTALL_PATH}

RUN apt-get update -y \
    && apt-get install -y libpq-dev build-essential git vim \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --upgrade wheel

RUN pip install -e .[all] --no-cache
RUN pip install flask --no-cache

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
