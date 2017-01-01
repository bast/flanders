include_directories(${PROJECT_SOURCE_DIR}/api)

add_library(
    flanders
    SHARED
    foo.cpp
    flanders.h
    )

install(TARGETS flanders LIBRARY DESTINATION lib)
