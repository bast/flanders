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

target_include_directories(
    flanders
    PUBLIC
    ${PROJECT_BINARY_DIR}/include
    )

install(TARGETS flanders LIBRARY DESTINATION "lib")
install(FILES flanders.h DESTINATION "include")
install(FILES ${PROJECT_BINARY_DIR}/include/flanders_export.h DESTINATION "include")
