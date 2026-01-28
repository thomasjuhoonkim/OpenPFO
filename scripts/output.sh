#!/bin/sh

tar -vc --use-compress-program="pigz -p 32" -f output.tar.gz output