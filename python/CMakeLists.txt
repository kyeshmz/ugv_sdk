# setup.py points pybind11_DIR at the pip-installed pybind11 for wheel builds.
if(pybind11_DIR)
    find_package(pybind11 CONFIG REQUIRED)
else()
    add_subdirectory(pybind11)
endif()
add_subdirectory(ugv_sdk_py)