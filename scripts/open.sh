#!/usr/bin/env bash

if [[ -x "$(command -v open)" ]]; then
    open $1
else
    xdg-open $1
fi
