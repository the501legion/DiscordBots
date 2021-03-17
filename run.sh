#!/bin/sh
tmux kill-session -t paperbot-live
tmux new-session -d -s paperbot-live 'python3 PrincessPaperplane/paperbot.py'
