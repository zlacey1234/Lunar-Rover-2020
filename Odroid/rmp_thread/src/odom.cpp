#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <rmp_thread/OdomSimple.h>


class Odom{
    public:
    	double vx, vy, vth;

	void callback(const rmp_thread::OdomSimple::ConstPtr& data){
	    const double pi = 3.1415926535897;
	    vth = data->odom_info[2]*pi/180.0; 
	    vx = data->odom_info[0];
	    vy = data->odom_info[1];   
	}
};    

int main(int argc, char** argv){
  ros::init(argc, argv, "odometry_publisher");

  ros::NodeHandle n;
  ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
  
  Odom Odom_instance;
  ros::Subscriber odom_sub = n.subscribe("/segway/odometry", 1000, &Odom::callback, &Odom_instance);
  tf::TransformBroadcaster odom_broadcaster;

  double x = 0.0;
  double y = 0.0;
  double th = 0.0;
  
  double vx, vy, vth;	
 
  ros::Time current_time, last_time;
  current_time = ros::Time::now();
  last_time = ros::Time::now();

  ros::Rate r(22.0);//1.0 in this example, probably going to need to be higher

  while(n.ok()){

    ros::spinOnce();   // check for incoming messages
    current_time = ros::Time::now();

    vx = Odom_instance.vx;
    vy = Odom_instance.vy;
    vth = Odom_instance.vth;

    //compute odometry in a typlical way given the velocities of the the robot, updated by the callback
    double dt = (current_time - last_time).toSec();
    double delta_x = (vx * cos(th) - vy * sin(th)) * dt;
    double delta_y = (vx * sin(th) + vy * cos(th)) * dt;
    double delta_th = vth * dt;

    x += delta_x;
    y += delta_y;
    th += delta_th;

    //since all odometry is 6DOF we'll need a quaternion created from yaw
    geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(th);

    //first, we'll publish the transform over tf
    geometry_msgs::TransformStamped odom_trans;
    odom_trans.header.stamp = current_time;
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "base_link";

    odom_trans.transform.translation.x = x;
    odom_trans.transform.translation.y = y;
    odom_trans.transform.translation.z = 0.0;
    odom_trans.transform.rotation = odom_quat;

    //send the transform
    odom_broadcaster.sendTransform(odom_trans);

    //next, we'll publish the odometry message over ROS
    nav_msgs::Odometry odom;
    odom.header.stamp = current_time;
    odom.header.frame_id = "odom";

    //set the position
    odom.pose.pose.position.x = x;
    odom.pose.pose.position.y = y;
    odom.pose.pose.position.z = 0.0;
    odom.pose.pose.orientation = odom_quat;

    //set the velocity
    odom.child_frame_id = "base_link";
    odom.twist.twist.linear.x = vx;
    odom.twist.twist.linear.y = vy;
    odom.twist.twist.angular.z = vth;

    //publish the message
    odom_pub.publish(odom);
   

    last_time = current_time;
    r.sleep();
  }
}


    









