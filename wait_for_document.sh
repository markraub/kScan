#!/bin/sh
dir1="My Documents"
echo We out here trying to transfer some shit son
while inotifywait -qqre modify $dir1; do
	scp $dir1/* $USER@shell.csh.rit.edu:~/.scan
done
