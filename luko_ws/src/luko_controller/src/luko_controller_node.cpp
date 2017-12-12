#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include <control_msgs/FollowJointTrajectoryAction.h>
#include <trajectory_msgs/JointTrajectory.h>
#include <mbed_interface/JointAngles.h>
#include <sensor_msgs/JointState.h>
#include <std_msgs/Header.h>

class RobotTrajectoryFollower
{
protected:

  ros::NodeHandle nh_;
  // NodeHandle instance must be created before this line. Otherwise strange error may occur.
  actionlib::SimpleActionServer<control_msgs::FollowJointTrajectoryAction> as_; 
  std::string action_name_;
  ros::Publisher pub_angles;
  ros::Publisher fake_joint_state; 
public:

  RobotTrajectoryFollower(std::string name) :
    as_(nh_, name, false),
    action_name_(name)
  {
    //Register callback functions:
    as_.registerGoalCallback(boost::bind(&RobotTrajectoryFollower::goalCB, this));
    as_.registerPreemptCallback(boost::bind(&RobotTrajectoryFollower::preemptCB, this));
    as_.start();
    pub_angles = nh_.advertise<mbed_interface::JointAngles>("/mbed/set_target_angle", 100);
    fake_joint_state = nh_.advertise<sensor_msgs::JointState>("/joint_states", 100);
  }

  ~RobotTrajectoryFollower(void)//Destructor
  {
  }

  void goalCB()
  {
    // accept the new goal
    ROS_INFO("New goal!");

    ros::Time start_time = ros::Time::now();

    trajectory_msgs::JointTrajectory msg = as_.acceptNewGoal()->trajectory;
 
    std::vector<trajectory_msgs::JointTrajectoryPoint> trajectory_points = msg.points; 

    std::vector<int>::size_type vectorSize = trajectory_points.size();  
                                                                                                             
    ROS_INFO("The size of the vector = %lu", vectorSize);

 
    for (unsigned i=0; i<vectorSize; i++)
    {   
        mbed_interface::JointAngles new_angles;
        sensor_msgs::JointState fake_state;
	        
        fake_state.header = std_msgs::Header();

        fake_state.name.push_back("cylinder_joint");
        fake_state.name.push_back("low_joint0");
        fake_state.name.push_back("low_joint1");
        fake_state.name.push_back("low_joint2");
        fake_state.name.push_back("up_joint0");
        fake_state.name.push_back("up_joint1");
        fake_state.name.push_back("up_joint2");
        fake_state.name.push_back("head_bearing_link");
        fake_state.name.push_back("head_to_lamp");

// joint_names: ['cylinder_joint', 'head_bearing_link', 'head_to_lamp', 'low_joint0', 'up_joint0'] output from rviz
// joint_names: ['cylinder_joint', 'low_joint0', 'up_joint0', 'head_bearing_link', 'head_to_lamp'] input to mbed 
        new_angles.joints.push_back(msg.points[i].positions[0]); 
        new_angles.joints.push_back(msg.points[i].positions[3]); 
        new_angles.joints.push_back(msg.points[i].positions[4]); 
        new_angles.joints.push_back(msg.points[i].positions[1]); 
        new_angles.joints.push_back(msg.points[i].positions[2]);
 
        fake_state.position.push_back(msg.points[i].positions[0]); 
        fake_state.position.push_back(msg.points[i].positions[3]); 
        fake_state.position.push_back(msg.points[i].positions[3]); 
        fake_state.position.push_back(-msg.points[i].positions[3]); 
        fake_state.position.push_back(msg.points[i].positions[4]);
        fake_state.position.push_back(msg.points[i].positions[4]); 
        fake_state.position.push_back(-msg.points[i].positions[4]); 
        fake_state.position.push_back(msg.points[i].positions[1]); 
        fake_state.position.push_back(msg.points[i].positions[2]); 

        pub_angles.publish(new_angles);
        if (i < vectorSize - 1){
            ros::Time current_time = ros::Time::now();
            ros::Duration sleep_duration = start_time + msg.points[i+1].time_from_start - current_time; 	
            float secs = sleep_duration.toSec();
            ROS_INFO("%f: sleep duration", secs);
            sleep_duration.sleep();
            //ros::Duration(0.15).sleep();
	}
        fake_state.header.stamp = ros::Time::now();
	fake_joint_state.publish(fake_state);
    }
 
  }

  void preemptCB()
  {
    ROS_INFO("%s: Preempted", action_name_.c_str());
    // set the action state to preempted
    as_.setPreempted();
  }
};


int main(int argc, char** argv)
{
  ros::init(argc, argv, "action_server");

  RobotTrajectoryFollower RobotTrajectoryFollower("/joint_trajectory_action");
  
  ROS_INFO("Launched action server");

  ros::spin();

  return 0;
}
