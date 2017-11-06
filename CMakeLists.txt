cmake_minimum_required(VERSION 3.9)

project(pykde5)

find_package(ECM 5.38.0 REQUIRED)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
include(FeatureSummary)


include(CppyyMacros)

###############################################################################
# Module definitions
###############################################################################

add_subdirectory(KF5.Akonadi)
add_subdirectory(KF5.KDcraw)

feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)
