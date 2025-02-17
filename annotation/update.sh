#!/bin/bash

parent_path=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$parent_path" || exit

./stop.sh
# WORK IN PROGRESS; NOT FULLY TESTED YET!
cd cvat && git pull
cd cvat && CVAT_VERSION=latest docker compose pull
