# ======================================================================== #
# Copyright 2019-2020 The Collaborators                                    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
# ======================================================================== #

cmake_policy(SET CMP0104 NEW)
cmake_policy(SET CMP0048 NEW)

project(cudaParticleAdvection
  VERSION 0.0.1
	DESCRIPTION "cuda Particle Advection with hardware accelerated tet query"
	LANGUAGES C CXX CUDA
)

cmake_minimum_required(VERSION 3.12)

# ------------------------------------------------------------------
# set dependencies (TBB, Optix and CUDA compiler)
# ------------------------------------------------------------------

set(OptiX_INSTALL_DIR "c:/ProgramData/NVIDIA Corporation/OptiX SDK 7.0.0")
set(OptiX_INCLUDE "${OptiX_INSTALL_DIR}/include")
set(TBB_ROOT_PATH "E:/libs/oneapi-tbb-2021.5.0")

if (WIN32)
  set(CUDA_HOST_COMPILER "C:/Program Files/Microsoft Visual Studio/2022/Professional/VC/Tools/MSVC/14.32.31326/bin/Hostx64/x64/cl.exe")
endif()

# ------------------------------------------------------------------
# first, include gdt project to do some general configuration stuff
# (build modes, glut, optix, etc)
# ------------------------------------------------------------------
set(owl_dir ${PROJECT_SOURCE_DIR}/owl/)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${owl_dir}/owl/common/cmake/")
include(configure_owl)

#set CUDA_HOST_COMPILER C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe

set(CompilerFlags
        CMAKE_CXX_FLAGS
        CMAKE_CXX_FLAGS_DEBUG
        CMAKE_CXX_FLAGS_RELEASE
        CMAKE_C_FLAGS
        CMAKE_C_FLAGS_DEBUG
        CMAKE_C_FLAGS_RELEASE
        )
foreach(CompilerFlag ${CompilerFlags})
  string(REPLACE "/MD" "/MT" ${CompilerFlag} "${${CompilerFlag}}")
endforeach()

# ------------------------------------------------------------------
# import owl: 
# ------------------------------------------------------------------
include_directories(${OWL_INCLUDES})
add_subdirectory(${owl_dir} EXCLUDE_FROM_ALL)

# -------------------------------------------------------
# the project itself
# -------------------------------------------------------

include_directories(${PROJECT_SOURCE_DIR})

cuda_compile_and_embed(ptxCode
  optix/optixQueryKernel.cu
)

add_library(optixTetQueries STATIC
  optix/internalTypes.h
  optix/OptixQuery.h
  optix/OptixTetQuery.cpp
  optix/OptixTriQuery.cpp
  ${ptxCode}
  )
target_link_libraries(optixTetQueries
  ${OWL_LIBRARIES}
  )

cuda_add_executable(cudaParticleAdvection
  cuda/common.h
  cuda/utils.cpp
  cuda/particles.cu
  cuda/HostTetMesh.h
  cuda/DeviceTetMesh.cuh
  query/ConvexQuery.h
  query/ConvexQuery.cu
  query/RTQuery.h
  query/RTQuery.cu
  cuda/cudaParticleAdvection.cu
  )

target_link_libraries(cudaParticleAdvection
  optixTetQueries
  )



