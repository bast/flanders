add_library(
    flanders
    SHARED
    flanders.h
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

# clang seems to need this
target_link_libraries(
    flanders
    stdc++
    )

install(TARGETS flanders LIBRARY DESTINATION "lib")
install(FILES flanders.h DESTINATION "include")
