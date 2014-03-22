cmake_minimum_required(VERSION 2.8.12)

project(pykde5)

find_package(ECM 0.0.9 REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

find_package(Qt5 5.2.0 CONFIG REQUIRED Core Widgets DBus Gui)
include(KDEInstallDirs)
include(KDEFrameworkCompilerSettings)
include(KDECMakeSettings)


# Match what's used in the main macros
cmake_policy(SET CMP0002 OLD)
find_package(PythonLibrary)

include(PythonMacros)
include(FeatureSummary)
include(ECMSetupVersion)

find_package(KF5 CONFIG REQUIRED Auth ItemModels ItemViews Archive Plotting Solid CoreAddons Sonnet)

#option(PYKDEUIC4_ALTINSTALL "Enable parallel-installation of the PyKDE4 tools" FALSE)

#set_package_properties(KDE4 PROPERTIES DESCRIPTION "The KDE libraries"
#                       URL "http://www.kde.org" TYPE REQUIRED
#                       PURPOSE "Required to build PyKDE4")
set_package_properties(PythonLibrary PROPERTIES DESCRIPTION
                       "The Python Library" URL "http://www.python.org"
                       TYPE REQUIRED PURPOSE "Required to build PyKDE4")
set_package_properties(PythonInterp PROPERTIES
                       DESCRIPTION "The Python interpreter"
                       URL "http://www.python.org" TYPE REQUIRED
                       PURPOSE "Required to build PyKDE4")

find_package(SIP)
set_package_properties(SIP PROPERTIES DESCRIPTION "The SIP binding generator"
                       URL "http://riverbankcomputing.com" TYPE REQUIRED
                       PURPOSE "Required to build PyKDE4")

include(SIPMacros)

if(SIP_VERSION STRLESS "040f03")    # These version numbers also appear in ../CMakeLists.txt
    message(FATAL_ERROR "The version of SIP found is too old. 4.15.3 or later is needed.")
endif()

find_package(PyQt5)
set_package_properties(PyQt5 PROPERTIES DESCRIPTION "The PyQt bindings"
                       URL "http://riverbankcomputing.com" TYPE REQUIRED
                       PURPOSE "Required to build PyKDE5")

if(PYQT5_VERSION STRLESS "050101")  # These version numbers also appear in ../CMakeLists.txt
    message(FATAL_ERROR "The version of PyQt found is too old. 5.1.1 or later is required.")
endif()

set(SIP_INCLUDES ${PYQT5_SIP_DIR} sip)
set(SIP_CONCAT_PARTS 8)
if (WIN32)
    set(SIP_TAGS ALL WS_WIN ${PYQT5_VERSION_TAG})
else ()
    set(SIP_TAGS ALL WS_X11 ${PYQT5_VERSION_TAG})
endif ()
set(SIP_DISABLE_FEATURES VendorID PyQt_NoPrintRangeBug)

# Use an extra option when compiling on Python 3.
if (PYTHON_VERSION_MAJOR GREATER 2)
    if(PYQT5_VERSION STRGREATER "040904")
	    # Disable for newer PyQt
	    set(SIP_EXTRA_OPTIONS -P -g -x PyKDE_QVector)
    else ()
	    set(SIP_EXTRA_OPTIONS -g)
    endif()
else (PYTHON_VERSION_MAJOR GREATER 2)
    if(PYQT5_VERSION STRGREATER "040904")
	# Disable for newer PyQt
    	set(SIP_EXTRA_OPTIONS -P -g -x PyKDE_QVector -x Py_v3)
    else ()
	    set(SIP_EXTRA_OPTIONS -g -x Py_v3)
    endif()
endif ()

get_property(qt5core_include TARGET Qt5::Core PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
get_property(qt5gui_include TARGET Qt5::Gui PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
get_property(qt5widgets_include TARGET Qt5::Widgets PROPERTY INTERFACE_INCLUDE_DIRECTORIES)

get_property(solid_include TARGET KF5::Solid PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
# Soild is being difficult. Lets set it here explicitly.

include_directories(
    ${SIP_INCLUDE_DIR}
    ${qt5core_include}
    ${qt5gui_include}
    ${qt5widgets_include}
    ${solid_include}/solid
)

add_definitions(-D_REENTRANT -DSIP_PROTECTED_IS_PUBLIC -Dprotected=public)

###############################################################################
# Module definitions
###############################################################################

# kauth
#file(GLOB kauth_files_sip sip/kauth/*.sip)
#set(SIP_EXTRA_FILES_DEPEND ${kauth_files_sip})
#add_sip_python_module(PyKDE5.kauth sip/kauth/kauthmod.sip KF5::Auth)

# kitemmodels
file(GLOB kitemmodels_files_sip sip/kitemmodels/*.sip)
set(SIP_EXTRA_FILES_DEPEND ${kitemmodels_files_sip})
add_sip_python_module(PyKDE5.kitemmodels sip/kitemmodels/kitemmodelsmod.sip KF5::ItemModels)

# kitemviews
file(GLOB kitemviews_files_sip sip/kitemviews/*.sip)
set(SIP_EXTRA_FILES_DEPEND ${kitemviews_files_sip})
add_sip_python_module(PyKDE5.kitemviews sip/kitemviews/kitemviewsmod.sip KF5::ItemViews)

# karchive
file(GLOB karchive_files_sip sip/karchive/*.sip)
set(SIP_EXTRA_FILES_DEPEND ${karchive_files_sip})
add_sip_python_module(PyKDE5.karchive sip/karchive/karchivemod.sip KF5::Archive)

# kplotting
file(GLOB kplottin_files_sip sip/kplotting/*.sip)
set(SIP_EXTRA_FILES_DEPEND ${kplotting_files_sip})
add_sip_python_module(PyKDE5.kplotting sip/kplotting/kplottingmod.sip KF5::Plotting)

# solid
file(GLOB solid_files_sip sip/solid/*.sip)
set(SIP_EXTRA_FILES_DEPEND ${solid_files_sip})
add_sip_python_module(PyKDE5.solid sip/solid/solidmod.sip KF5::Solid)

## kcoreaddons
file(GLOB kcoreaddons_files_sip sip/kcoreaddons/*.sip)
set(SIP_EXTRA_FILES_DEPEND ${kcoreaddons_files_sip})
add_sip_python_module(PyKDE5.kcoreaddons sip/kcoreaddons/kcoreaddonsmod.sip KF5::CoreAddons)

# sonnet
#file(GLOB sonnet_files_sip sip/sonnet/*.sip)
#set(SIP_EXTRA_FILES_DEPEND ${sonnet_files_sip})
#add_sip_python_module(PyKDE5.sonnet sip/sonnet/sonnetmod.sip KF5::SonnetCore KF5::SonnetUi)


set(PYKDE_MODULES "kitemmodels kitemviews karchive kplotting solid kcoreaddons")

###############################################################################

python_install(__init__.py ${PYTHON_SITE_PACKAGES_INSTALL_DIR}/PyKDE5)

# Setup and install pykdeconfig.py

# Turn these into formatted strings.
set(_SIP_TAGS)
foreach (_TAG ${SIP_TAGS})
    set(_SIP_TAGS "${_SIP_TAGS} -t ${_TAG}")
endforeach (_TAG)

set(_SIP_X)
foreach (_X ${SIP_DISABLE_FEATURES})
    set(_SIP_X "${_SIP_X} -X ${_X}")
endforeach (_X ${SIP_DISABLE_FEATURES})

#get_filename_component(LIB_DIR ${KDE5_LIB_DIR} NAME)

set (SIP_FILES_INSTALL_DIR ${SHARE_INSTALL_PREFIX}/sip)

#set(SIP_CONFIGURATION "
#kde_version_parts = '${KDE_VERSION}'.split('.')
#kde_version_hex = int(kde_version_parts[0])*65536 + int(kde_version_parts[1])*256 + int(kde_version_parts[2])
#_pkg_config = {
#    'dist_name':            '',
#    'kde_version':          kde_version_hex,
#    'kde_version_extra':    '',
#    'kde_version_sfx':      '',
#    'kde_version_str':      '${KDE_VERSION}',
#    'kdebasedir':           '${CMAKE_INSTALL_PREFIX}',
#    'kdeincdir':            '${KDE5_INCLUDE_DIR}',
#    'kdelibdir':            '${KDE5_LIB_DIR}',
#    'konsolepart':          'False',
#    'libdir':               '${LIB_DIR}',
#    'pykde_kde_sip_flags':  '${_SIP_TAGS} ${_SIP_X} ${SIP_EXTRA_OPTIONS}',
#    'pykde_mod_dir':        '${PYTHON_SITE_PACKAGES_INSTALL_DIR}/PyKDE5',
#    'pykde_modules':        '${PYKDE_MODULES}',
#    'pykde_sip_dir':        '${SIP_FILES_INSTALL_DIR}/PyKDE5',
#    'pykde_version':        kde_version_hex,
#    'pykde_version_str':    '${KDE_VERSION}'
#}
#
#_default_macros = None")
#
#configure_file(pykdeconfig.py.in ${CMAKE_CURRENT_BINARY_DIR}/pykdeconfig.py)
#python_install(${CMAKE_CURRENT_BINARY_DIR}/pykdeconfig.py ${PYTHON_SITE_PACKAGES_INSTALL_DIR}/PyKDE5)

# Install the .sip files for anyone that wants to build bindings on top of PyKDE5.
# (Don't forget the / at the end of sip/.)
install(DIRECTORY sip/ DESTINATION ${SIP_FILES_INSTALL_DIR}/PyKDE5
    PATTERN "*~" EXCLUDE    # This sucks, why can't I just whitelist what I _do_ want?
    PATTERN ".svn" EXCLUDE
    PATTERN "*.in" EXCLUDE)

#add_subdirectory(tools)
#add_subdirectory(docs)
#add_subdirectory(examples)

feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)
