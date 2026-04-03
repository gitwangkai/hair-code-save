cmake_minimum_required(VERSION 3.0.2)
project(fw_upgrade)

# 设置默认编译选项
add_compile_options(-std=c++14)

# 定义通用宏
add_definitions(-DOS_UNIX)

# 包含头文件目录
include_directories(
  include
)

# 添加共享库
add_library(DEPS
    src/crc.cpp
    src/decryptfile.cpp
    src/can_interface_socketcan.cpp
    src/protocol.cpp
)

# 链接库
target_link_libraries(DEPS dl boost_system ssl crypto archive)

# 添加可执行文件
add_executable(fw_upgrade src/main.cpp)
target_link_libraries(fw_upgrade DEPS pthread)
