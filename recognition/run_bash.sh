#!/bin/bash

parent_path=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$parent_path" || exit

datasets_path="$( cd -- "$( dirname -- "$parent_path" )" &> /dev/null && pwd )/datasets"

docker run -it --entrypoint "/bin/bash" -v "$datasets_path:/usr/src/datasets" -v "$parent_path:/usr/src/app" traffic-sign-recognition "$@"
