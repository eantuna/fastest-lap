add_subdirectory(./main)

if (${ENABLE_TESTS})
    add_subdirectory(./test)
endif()

add_subdirectory(./cli)