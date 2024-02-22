#!/usr/bin/env bash

fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/web_static/web_static_20240205144518.tgz -i ~/.ssh/school -u ubuntu
