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


## Installation using pip

```shell
pip install git+https://github.com/bast/flanders.git
```


## Example

In this example we have 6 points (numbered 0 to 5) and two reference points
with a certain view vector and view angle. The first reference point finds
point 2. The second reference point does not find any neighbor within the view
angle and returns -1.

<img src="https://github.com/bast/flanders/raw/master/example/flanders.png" width="300">

```python
import flanders

points = [(60.4, 51.3), (173.9, 143.8), (132.9, 124.9), (19.5, 108.9), (196.5, 9.9), (143.3, 53.3)]

num_points = len(points)

context = flanders.new_context(num_points, points)

indices = flanders.search_neighbor(context,
                                   coordinates=[(119.2, 59.7), (155.2, 30.2)],
                                   view_vectors=[(0.0, 1.0), (-1.0, -1.0)],
                                   angles_deg=[90.0, 90.0])

assert indices == [2, -1]

flanders.free_context(context)
```

Instead of searching nearest neighbors of coordinates, you can also search by nearest neighbors of the points by their indices:

```python
indices = flanders.search_neighbor(context,
                                   ref_indices=range(num_points),
                                   view_vectors=[(1.0, 1.0) for _ in xrange(num_points)],
                                   angles_deg=[90.0 for _ in xrange(num_points)])

assert indices == [2, 2, -1, 2, 1, 2]
```

For debugging you can employ the naive slow implementation:

```python
indices = flanders.search_neighbor(context,
                                   coordinates=[(119.2, 59.7), (155.2, 30.2)],
                                   view_vectors=[(0.0, 1.0), (-1.0, -1.0)],
                                   angles_deg=[90.0, 90.0],
                                   naive=True)
```


## References

- https://en.wikipedia.org/wiki/Nearest_neighbor_search
- https://en.wikipedia.org/wiki/K-d_tree
- http://www.slideshare.net/awebneck/the-post-office-problem
- http://www.cs.nyu.edu/~roweis/papers/Ahmed_msc_thesis.pdf
- http://dl.acm.org/citation.cfm?doid=361002.361007
