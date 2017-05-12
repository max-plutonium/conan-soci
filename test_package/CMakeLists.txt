cmake_minimum_required(VERSION 3.1.2)
project(conan-soci-test CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(test-empty test-empty.cpp)
target_link_libraries(test-empty CONAN_PKG::SOCI CONAN_PKG::catch)
