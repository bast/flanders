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

add_executable(
    test.x
    test.cpp
    )

target_link_libraries(
    test.x
    flanders
    )

install(TARGETS flanders LIBRARY DESTINATION lib)
