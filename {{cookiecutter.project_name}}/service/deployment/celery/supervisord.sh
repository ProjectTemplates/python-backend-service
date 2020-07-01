#! /usr/bin/env bash
set -e

supervisord -n -c /opt/app/supervisord.conf
