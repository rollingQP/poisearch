#! /bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
echo "运行文件夹:${SHELL_FOLDER}"
cd $SHELL_FOLDER
python3 gui.py
