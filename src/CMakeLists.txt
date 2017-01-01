include_directories(${PROJECT_SOURCE_DIR}/api)

add_library(
    cpp_interface
    SHARED
    foo.cpp
    cpp_interface.h
    )

install(TARGETS cpp_interface LIBRARY DESTINATION lib)
