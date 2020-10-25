#!/bin/sh
tmux new-session -A -s paperbot-test 'python3 PrincessPaperplane/paperbot.py -test'
tmux detach -s paperbot-test

