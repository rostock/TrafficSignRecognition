#!/bin/bash

parent_path=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$parent_path" || exit

git clone https://github.com/cvat-ai/cvat
./start.sh
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
./stop.sh