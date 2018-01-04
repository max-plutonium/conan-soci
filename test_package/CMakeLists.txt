cmake_minimum_required(VERSION 3.1.2)
project(conan-soci-test CXX)

find_package(PostgreSQL REQUIRED)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include_directories(
    ${PostgreSQL_INCLUDE_DIRS})

add_executable(test-empty test-empty.cpp)
target_link_libraries(test-empty ${PostgreSQL_LIBRARIES} CONAN_PKG::SOCI CONAN_PKG::catch)
