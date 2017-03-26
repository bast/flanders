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


## Installation using pip

```shell
pip install git+https://github.com/bast/flanders.git
```


## Example

![alt text](https://github.com/bast/flanders/raw/master/example/flanders.png "example points")

```python
from flanders import new_context, free_context, search_neighbor
import numpy as np

x_coordinates = [60.4, 173.9, 132.9, 19.5, 196.5, 143.3]
y_coordinates = [51.3, 143.8, 124.9, 108.9, 9.9, 53.3]

num_points = len(x_coordinates)

context = new_context(num_points, np.array(x_coordinates), np.array(y_coordinates))

x = [119.2, 155.2]
y = [59.7, 30.2]
vx = [0.0, -1.0]
vy = [1.0, -1.0]
angles_deg = [90.0, 90.0]

indices_fast = search_neighbor(context,
                               x=x,
                               y=y,
                               vx=vx,
                               vy=vy,
                               angles_deg=angles_deg)

assert indices_fast == [2, -1]

free_context(context)
```


## References

- https://en.wikipedia.org/wiki/Nearest_neighbor_search
- https://en.wikipedia.org/wiki/K-d_tree
- http://www.slideshare.net/awebneck/the-post-office-problem
- http://www.cs.nyu.edu/~roweis/papers/Ahmed_msc_thesis.pdf
- http://dl.acm.org/citation.cfm?doid=361002.361007
