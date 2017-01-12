[![Build Status](https://travis-ci.org/bast/flanders.svg?branch=master)](https://travis-ci.org/bast/flanders/builds)
[![License](https://img.shields.io/badge/license-%20MPL--v2.0-blue.svg)](../master/LICENSE)

# Flanders: Fast 2D nearest neighbor search with an angle

```
                                                    `.-:://////:-.`
                                             `-/oyhddddmmddddddNmdmdhs/`
                                          -ohddddddddddddNddddddNddddmmds.
                                        `hmmmmmdddddddddddNddddmmddddmmddm.
                                       `hddddddmmddddddhyyysoossyhdmNmdddNs
                                       sddddddddmmho/:-------------:odmmmmo
                                      :mddddddddd+-------------------:hddd.
                                      dddddddddm+---------------------:ms.
                                     :mddddddddd-----------------------s/`
                                     yddddddddds------------------------:s
                                    `mddddddddm+-----://////+/:---://////y`
                                    -Nddddddddm/----+:`     `./+-+-`    `.+:
                                    /mddddddddN:---o`          -d-    -.   o-
                                    omddddddddN////y  -d/      `m.    y+   +:
                                    sdddhhNmmmN+/::o: `-`     `+so++//:. `:+`
           `---.                    ydd+::mdddm:----/+-.````-:+:------:+s/-
           o/::/+-                  sN:-oomdddm+------://+///:---------:s
   `.-.`   s-----+/`                oN:---smddds------------:+oyhhysssydhs:.
  -o/://+-`.o:----/o`               /mh:---hyyy/----------+hdmmmmdddddmmmddho.
  /+-----:+/-o:----:+`       `..    .mddyyydo-----:///::ohdmmdmmdmddNdmmdmmddd/
   :+/-----:+/y-----:+-`  .:+///+.   dddddddd----:mMMNNddddddmddmdddmmdmddmdddm:
   ``-/+:----::-------:/+++:----/+   +mdddddN----:MMMMMNmmmmmmmdddddddhhhhhys+/.
.////+//+o:--------------/-----/o`    sdddddm/----oNmdmNNNNMMMm//os--...``
y:-----:/+o------------------:o:       :ydddm+-----:oyyyysydMMm:::o+.
:o/:----------------+o:-----:s`          .::+o--------://++oooo+:--:s
  -:/+/:--------------s/----s.              -o------------------:/o+.
      `-/+o------------/---+d-             `+o------------------::h
          .s/---------:::ohhhs             y.-++:-----------------d:`
           dhys+///+oyhhhhyhm/            `s````:/++o+//:::://+++/-.s.
          /dddhhhhhhyyhhhddhym`           -s`````````..-:::/h/s-````.s`
         :dyyhddddddddddhyyyym           `ydy-`````````````s:.-o/````sy/-`
         yyyyyyyyyyyyyyyyyyyhs     `./+ooymhyhy/.`````````:o....++``:dmdhhhso:`
         dyyyyyyyyyyyyyyyyyym:`-/oyddhyyyyhddyyhhs+-``````hso++ohd++dyyddyyyyhhyo/`
         myyyyyyyyyyyyyyyyyyNhhhyyyyyyyyyyyyddyyyyyhdyso++ddhmhmddhhyyyyddyyyyyyyhdy+.
```


## Status

Experimental code.
Under heavy development.
Nothing is stable.


## Installation

```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
./setup
cd build
make
```


## References

- https://en.wikipedia.org/wiki/Nearest_neighbor_search
- https://en.wikipedia.org/wiki/K-d_tree
- http://www.slideshare.net/awebneck/the-post-office-problem
- http://www.cs.nyu.edu/~roweis/papers/Ahmed_msc_thesis.pdf
- http://dl.acm.org/citation.cfm?doid=361002.361007
