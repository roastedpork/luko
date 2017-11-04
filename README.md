# luco

The repository is split into two main folders, `luko_ws` for the ROS workspace, and `mbed` for all the motor controller code.


## How to Develop with ROS 

To initialise ROS, ROSCore must be running as a proccess, each node will run on another process.

To run ROSCore type `roscore`.

To run each node, type `rosrun <package_name> <script or binary>`.

To list all packages, type `rosrun <tab>`

Running C++ files, you will first need to compile the source file, >>>>> TBD: Follow online tutorial to configure CMakefile.txt to utilise catkin_make

Custom message types need to be compiled via catkin_make

To launch all ROS packages, use `roslaunch`, this has not been implemented yet so don't do it.


## Creating a custom ROS package

From the luko_ws/src directory, type  `catkin_create_pkg <cusotm package name> <dependencies>` 
