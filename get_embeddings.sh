#!/bin/bash

wget -O levy_deps.words.bz2 http://u.cs.biu.ac.il/~yogo/data/syntemb/deps.words.bz2
bzip2 -d levy_deps.words.bz2
#rm bzip2 -d levy_deps.words.bz2
