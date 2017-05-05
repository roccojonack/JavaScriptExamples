#! /bin/csh -f

git init
git remote add examples https://github.com/roccojonack/JavaScriptExamples.git

git config --global user.name  rocco
git config --global user.email rocco.jonack@gmail.com

git pull examples master

