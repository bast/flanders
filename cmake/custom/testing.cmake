# turn on testing
enable_testing()

# require python
find_package(PythonInterp REQUIRED)

# define test
add_test(python_test ${PYTHON_EXECUTABLE} ${PROJECT_SOURCE_DIR}/test.py)

# export environment variables needed by the test
set_property(
  TEST
    python_test
  PROPERTY ENVIRONMENT
    FLANDERS_BUILD_DIR=${PROJECT_BINARY_DIR}
#   ACCOUNT_LIBRARY_DIR=${PROJECT_BINARY_DIR}/lib
#   ACCOUNT_INCLUDE_DIR=${PROJECT_SOURCE_DIR}/account
  )
