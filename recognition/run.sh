#!/bin/bash

parent_path=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$parent_path" || exit

docker run -v "/$parent_path/../datasets:/usr/src/datasets" -v "/$parent_path:/usr/src/app" traffic-sign-recognition "$@"
