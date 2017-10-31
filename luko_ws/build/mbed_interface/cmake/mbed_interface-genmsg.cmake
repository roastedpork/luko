# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "mbed_interface: 1 messages, 0 services")

set(MSG_I_FLAGS "-Imbed_interface:/home/pi/luko/luko_ws/src/mbed_interface/msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(mbed_interface_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg" NAME_WE)
add_custom_target(_mbed_interface_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "mbed_interface" "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(mbed_interface
  "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mbed_interface
)

### Generating Services

### Generating Module File
_generate_module_cpp(mbed_interface
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mbed_interface
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(mbed_interface_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(mbed_interface_generate_messages mbed_interface_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg" NAME_WE)
add_dependencies(mbed_interface_generate_messages_cpp _mbed_interface_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mbed_interface_gencpp)
add_dependencies(mbed_interface_gencpp mbed_interface_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mbed_interface_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(mbed_interface
  "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mbed_interface
)

### Generating Services

### Generating Module File
_generate_module_eus(mbed_interface
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mbed_interface
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(mbed_interface_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(mbed_interface_generate_messages mbed_interface_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg" NAME_WE)
add_dependencies(mbed_interface_generate_messages_eus _mbed_interface_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mbed_interface_geneus)
add_dependencies(mbed_interface_geneus mbed_interface_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mbed_interface_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(mbed_interface
  "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mbed_interface
)

### Generating Services

### Generating Module File
_generate_module_lisp(mbed_interface
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mbed_interface
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(mbed_interface_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(mbed_interface_generate_messages mbed_interface_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg" NAME_WE)
add_dependencies(mbed_interface_generate_messages_lisp _mbed_interface_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mbed_interface_genlisp)
add_dependencies(mbed_interface_genlisp mbed_interface_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mbed_interface_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(mbed_interface
  "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mbed_interface
)

### Generating Services

### Generating Module File
_generate_module_nodejs(mbed_interface
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mbed_interface
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(mbed_interface_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(mbed_interface_generate_messages mbed_interface_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg" NAME_WE)
add_dependencies(mbed_interface_generate_messages_nodejs _mbed_interface_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mbed_interface_gennodejs)
add_dependencies(mbed_interface_gennodejs mbed_interface_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mbed_interface_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(mbed_interface
  "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mbed_interface
)

### Generating Services

### Generating Module File
_generate_module_py(mbed_interface
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mbed_interface
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(mbed_interface_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(mbed_interface_generate_messages mbed_interface_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/luko/luko_ws/src/mbed_interface/msg/JointAngles.msg" NAME_WE)
add_dependencies(mbed_interface_generate_messages_py _mbed_interface_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(mbed_interface_genpy)
add_dependencies(mbed_interface_genpy mbed_interface_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS mbed_interface_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mbed_interface)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/mbed_interface
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(mbed_interface_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mbed_interface)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/mbed_interface
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(mbed_interface_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mbed_interface)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/mbed_interface
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(mbed_interface_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mbed_interface)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/mbed_interface
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(mbed_interface_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mbed_interface)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mbed_interface\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/mbed_interface
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(mbed_interface_generate_messages_py std_msgs_generate_messages_py)
endif()
