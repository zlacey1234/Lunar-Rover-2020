cmake_minimum_required(VERSION 2.8.3)
project(rmp_thread)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
  message_generation
  tf
)


## Generate messages in the 'msg' folder
 add_message_files(
   FILES
   OdomSimple.msg
 )


## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   geometry_msgs   std_msgs
 )

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES rmp_thread
   CATKIN_DEPENDS geometry_msgs roscpp rospy std_msgs message_runtime
#  DEPENDS system_lib
)

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

add_executable(odom_node src/odom.cpp)

target_link_libraries(odom_node ${catkin_LIBRARIES})



