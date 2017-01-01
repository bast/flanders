add_library(
    cpp_interface
    SHARED
    cpp_interface.h
    cpp_interface.cpp
    helpers.h
    helpers.cpp
    )

install(TARGETS cpp_interface LIBRARY DESTINATION lib)
