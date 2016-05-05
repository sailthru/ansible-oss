#!/usr/bin/env bash

# available env vars
# ANSIBLE_LIBRARY
# ANSIBLE_ACTION_PLUGINS
# ANSIBLE_CACHE_PLUGINS
# ANSIBLE_CALLBACK_PLUGINS
# ANSIBLE_CONNECTION_PLUGINS
# ANSIBLE_LOOKUP_PLUGINS
# ANSIBLE_INVENTORY_PLUGINS
# ANSIBLE_VARS_PLUGINS
# ANSIBLE_FILTER_PLUGINS
# ANSIBLE_TEST_PLUGINS
# ANSIBLE_STRATEGY_PLUGINS

ROOTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"

build_path() {
    P=$1

    for i in $( find ${P} -type d ); do 
        V=${V}:${i}
    done

    echo ${V} | cut -f 2- -d ":"
}

export ANSIBLE_ACTION_PLUGINS=$( build_path ${ROOTDIR}/tools/echelon )
export ANSIBLE_LIBRARY=$( build_path ${ROOTDIR}/modules )
export ANSIBLE_LOOKUP_PLUGINS=$( build_path ${ROOTDIR}/plugins/lookup_plugins )
