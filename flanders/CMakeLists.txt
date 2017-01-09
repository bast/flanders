add_library(
    cpp_interface
    SHARED
    cpp_interface.h
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

install(TARGETS cpp_interface LIBRARY DESTINATION lib)
