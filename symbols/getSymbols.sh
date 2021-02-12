#!/bin/bash

checkParametersValid() {
    if [ "${exchange}" != 'nyse' ] && [ "${exchange}" != 'nasdaq' ] && [ "${exchange}" != 'amex' ]
    then
        echo 'valid exchanges: nyse | nasdaq | amex'
        exit 1
    fi
}

if [ -z "${exchange}" ]
then
    exchange=''

    # Loop through arguments and process them
    for arg in "$@"
    do
        case $arg in
            -e=*|--exchange=*)
            exchange="${arg#*=}"
            shift # Remove --exchange from processing
            ;;
            *)
            other_arguments+=("$1")
            shift # Remove generic argument from processing
            ;;
        esac
    done
fi    

checkParametersValid

curl "https://api.nasdaq.com/api/screener/stocks?tableonly=true&exchange=${exchange}&download=true" \
  -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36' \
  --compressed