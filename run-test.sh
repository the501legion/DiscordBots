#!/bin/sh
whoami
tmux kill-session -t paperbot-test
tmux new-session -d -s paperbot-test 'python3 PrincessPaperplane/paperbot.py -test'
