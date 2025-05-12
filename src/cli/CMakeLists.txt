add_executable(f1_optimal_laptime
    f1_optimal_laptime.cpp
)

target_link_libraries(f1_optimal_laptime LINK_PRIVATE lion::lion)
target_link_libraries(f1_optimal_laptime LINK_PRIVATE fastestlapc)

target_compile_options(f1_optimal_laptime PRIVATE
    -Wno-error=unused-variable
)

set_target_properties(f1_optimal_laptime PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

add_executable(circuit_preprocessor
    circuit_preprocessor.cpp
)

target_link_libraries(circuit_preprocessor LINK_PRIVATE lion::lion)
target_link_libraries(circuit_preprocessor LINK_PRIVATE fastestlapc)

target_compile_options(circuit_preprocessor PRIVATE
    -Wno-error=unused-variable
)

set_target_properties(circuit_preprocessor PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)