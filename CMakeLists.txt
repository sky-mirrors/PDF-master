cmake_minimum_required(VERSION 3.21)
project(nebula-office-graduation)

if(EXISTS "${CMAKE_SOURCE_DIR}/core/CMakeLists.txt")
  add_subdirectory(core)
else()
  message(FATAL_ERROR "Expected subdirectory 'core' with CMakeLists.txt not found")
endif()
