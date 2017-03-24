add_library(
    flanders
    SHARED
    flanders.h
    naive.cpp
    helpers.h
    helpers.cpp
    btree.h
    btree.cpp
    helpers.h
    helpers.cpp
    intersect.h
    intersect.cpp
    distance.h
    distance.cpp
    )

install(TARGETS flanders LIBRARY DESTINATION "lib")
install(FILES flanders.h DESTINATION "include")
