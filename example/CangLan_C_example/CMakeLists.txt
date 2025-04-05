cmake_minimum_required(VERSION 3.25)
project(CangLan_C C)

set(CMAKE_C_STANDARD 90)

include_directories(.)

add_executable(CangLan_C
        CangLan.c
        CangLan.h
        CangLan_tool.c
        CangLan_tool.h
        main.c variable.h variable.c)
