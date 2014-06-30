#!/bin/bash
pushd ~/mdp/mdp
    rm nohup-gh.out
    rm nohup-gh.err
    git reset --hard
    git pull
	nohup ./github.py > nohup-gh.out 2> nohup-gh.err < /dev/null &
popd
