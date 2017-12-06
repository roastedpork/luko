#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

print "============ Starting tutorial setup"
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('luko_moveit_script',
        anonymous=True) #TODO: check naming

robot = moveit_commander.RobotCommander()

scene = moveit_commander.PlanningSceneInterface()

group = moveit_commander.MoveGroupCommander("arm_head") #TODO: check naming

display_trajectory_publisher = rospy.Publisher(
                                    '/move_group/display_planned_path',
                                    moveit_msgs.msg.DisplayTrajectory,
                                    queue_size=20)

print "============ Reference frame: %s" % group.get_planning_frame()

print "============ End effector: %s" % group.get_end_effector_link()

print "============ Robot Groups:"
print robot.get_group_names()

print "============ Printing robot state"
print robot.get_current_state()
print "============"

group.set_named_target("left")

group.go(wait=True)
