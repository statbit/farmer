#!/bin/bash

cd $HOME/git/farmer
git stash
git pull upstream master
git stash pop
