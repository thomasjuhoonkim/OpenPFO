#!/bin/sh

tar -vc --use-compress-program="pigz -p 4" -f output.tar.gz output