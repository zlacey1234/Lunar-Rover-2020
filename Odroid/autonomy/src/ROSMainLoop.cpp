#include <ros/ros.h>
#include <iostream>
#include <vector>
#include <math.h>
#include <angles/angles.h>

// ROS Messages
#include <std_msgs/Float32.h>
#include <std_msgs/Int16.h>
#include <std_msgs/UInt8.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Twist.h>
#include <tf/transform_datatypes.h>
#include <apriltag_ros/AprilTagDetectionArray.h>

#include "Tag.h"

#include <signal.h>
#include <exception>

#define PI 3.14159265


using namespace std;

geometry_msgs::Pose currentLocation;

bool initialized = false;
bool startFlag = false;
bool tagsDetected = false;
double yaw_d = PI/2;
double timestamp;
double timeinitialized;
char yaw_position = '3';

Tag loc;

std_msgs::String msg;
geometry_msgs::Twist velocity;
// Should be changed
geometry_msgs::Twist desiredPose;

// Subscribers
ros::Subscriber rsOdometrySubscriber;
ros::Subscriber controlStartSubscriber;
ros::Subscriber aprilTagDetectionSubscriber;

// Publishers
ros::Publisher velocityCmdPublisher;
ros::Publisher desiredPosePublisher;

void sigintEventHandler(int sig);
void rsOdometryHandler(const nav_msgs::Odometry::ConstPtr& message);
void aprilTagDetectionHandler(const apriltag_ros::AprilTagDetectionArray::ConstPtr& tagInfo);
void startControlHandler(const std_msgs::Bool::ConstPtr& start);


int main(int argc, char **argv) {

    ros::init(argc, argv, "odometry", ros::init_options::NoSigintHandler);
    ros::NodeHandle mNH;

    // Register the SIGINT event handler so the node can properly shutdown
    signal(SIGINT, sigintEventHandler); 

    // subscribers
    controlStartSubscriber = mNH.subscribe(("/startControl"),10, startControlHandler);
    rsOdometrySubscriber = mNH.subscribe(("/camera/odom/sample"), 10, rsOdometryHandler);
    aprilTagDetectionSubscriber = mNH.subscribe(("/tag_detections"), 10, aprilTagDetectionHandler);

    // publishers
    velocityCmdPublisher = mNH.advertise<geometry_msgs::Twist>(("/cmd_vel"),10);
    desiredPosePublisher = mNH.advertise<geometry_msgs::Twist>(("/desiredPose"),10);

    ros::spin();

    return 0;
}

void startControlHandler(const std_msgs::Bool::ConstPtr& start){
    startFlag = start->data;
}

void sendDriveCommand(double linearVelocity, double angularVelocity) {
    velocity.linear.x = linearVelocity;
    velocity.angular.z = angularVelocity;
    velocityCmdPublisher.publish(velocity);
}

void sigintEventHandler(int sig) {
    ros::shutdown();
}

void rsOdometryHandler(const nav_msgs::Odometry::ConstPtr& message) {
    
    double time = (message->header.stamp.sec) + (message->header.stamp.nsec)*pow(10,-9);

    if (!initialized) {
        timeinitialized = time;
        time = time - timeinitialized; 
        printf("Initialized\n");
        initialized = true;
    }
    time = time - timeinitialized; 
    double time_satified;        
    // Get x and y location from pose
    currentLocation.position.x = message->pose.pose.position.x;
    currentLocation.position.y = message->pose.pose.position.y;

    tf::Quaternion q(message->pose.pose.orientation.x, 
                    message->pose.pose.orientation.y,
                    message->pose.pose.orientation.z,
                    message->pose.pose.orientation.w);

    tf::Matrix3x3 m(q);

    double roll, pitch, yaw;

    m.getRPY(roll, pitch, yaw);

    printf("Timestamp = %f \t Current Time = %f \tX = %f\t Yaw = %f\n",timestamp, time, currentLocation.position.x, yaw);


    /////////////////////////
    double x_d, y_d; 
    //double x_d_body, y_d_body, yaw_d_body;
    double x_error, y_error, error_dist, yaw_error;
    float Kp_x, Kp_yaw;
    double linear_x, twist_z; 
    double angleToleranceRad = 0.05;
    double outerAngleTolerance = 0.35;
    double waypointToleranceMeters = 0.02;
    double time_desired = 20.0;

    if(startFlag){
        Kp_x =  0.1;
        Kp_yaw = .25;
    
        x_d = 1.5;
        y_d = .10;

        x_error = x_d - currentLocation.position.x;
        y_error = y_d - currentLocation.position.y;

        
        // Testing Purposes


        if (tagsDetected) {
            printf("ID = %d\n",loc.getID());

            if (loc.getID() == 1) {
                velocity.linear.x  = 0;
                velocity.angular.z = 0;
            } else if (loc.getID() == 2) {
                yaw_d = atan2(loc.getPositionZ(), loc.getPositionX()) - PI/2;
                yaw_error = yaw_d;
                printf("YawCalculated  = %f,   Yaw Error = %f \t",  atan2(loc.getPositionZ(), loc.getPositionX())-PI/2, yaw_error);
            } 


        } else {
            switch(yaw_position) {
                case '1' :
                    yaw_d = -PI/2;

                    yaw_error = yaw_d - yaw;
                    if (abs(yaw_error) >= angleToleranceRad) {
                        timestamp = time;
                    } 
                    time_satified = time - timestamp;
                    if (time_satified >= time_desired) {
                        yaw_position = '2';
                    }
                    break;
                case '2' :
                    yaw_d = 0;

                    yaw_error = yaw_d - yaw;
                    if (abs(yaw_error) >= angleToleranceRad) {
                        timestamp = time;
                    } 
                    time_satified = time - timestamp;
                    if (time_satified >= time_desired) {
                        yaw_position = '3';
                    }
                    break;
                case '3' :
                    yaw_d = PI/2;

                    yaw_error = yaw_d - yaw;
                    if (abs(yaw_error) >= angleToleranceRad) {
                        timestamp = time;
                    } 
                    time_satified = time - timestamp;
                    if (time_satified >= time_desired) {
                        yaw_position = '3';
                    }
                    break;
                case '4' :
                    yaw_d = 0;

                    yaw_error = yaw_d - yaw;
                    if (abs(yaw_error) >= angleToleranceRad) {
                        timestamp = time;
                    } 
                    time_satified = time - timestamp;
                    if (time_satified >= time_desired) {
                        yaw_position = '1';
                    }
                    break;
                default :
                    printf("Invalid \n");
            } 
            printf("Yaw Position = %c \t Time satified = %f\n", yaw_position, time_satified);

        }

        if (abs(yaw_error) >= angleToleranceRad) {
            velocity.linear.x = 0;
            velocity.angular.z = -Kp_yaw*yaw_error;
        } else {
            velocity.linear.x  = 0;
            velocity.angular.z = 0;
        }

        /*
        
        yaw_d = atan2(y_error, x_error);

        yaw_error = yaw_d - yaw;

        error_dist = sqrt(pow(x_error,2) + pow(y_error,2));

        // package rosmessages
        if (abs(yaw_error) >= angleToleranceRad) {
            velocity.linear.x = 0;
            velocity.angular.z = -Kp_yaw*yaw_error;
        } else if ((abs(error_dist) >= waypointToleranceMeters) && (abs(yaw_error) <= outerAngleTolerance)) {
            velocity.linear.x  = Kp_x*error_dist;
            velocity.angular.z = 0;
        } else if (abs(error_dist) <= waypointToleranceMeters) {
            velocity.linear.x  = 0;
            velocity.angular.z = 0;
        } else {
            velocity.linear.x  = 0;
            velocity.angular.z = 0;
            printf("?????\n");
        }

        */
        desiredPose.linear.x = x_d;
        desiredPose.linear.y = y_d;
        desiredPose.angular.z = yaw_d;
    } else {
        desiredPose.linear.x = 0;
        desiredPose.linear.y = 0;
        desiredPose.angular.z = 0;

        velocity.linear.x  = 0;
        velocity.angular.z = 0;
    }

    velocityCmdPublisher.publish(velocity);
    desiredPosePublisher.publish(desiredPose);

    printf("Linear X = %f\t Yaw Rate = %f\t Yaw Desired = %f\n", velocity.linear.x, velocity.angular.z, yaw_d);

    printf("Start = %d\n", startFlag);

}

void aprilTagDetectionHandler(const apriltag_ros::AprilTagDetectionArray::ConstPtr& aprilTagInfo) {
    if (aprilTagInfo->detections.size() > 0) {
        vector<Tag> tags;

        for (int i = 0; i < aprilTagInfo->detections.size(); i++) {

            // Package up the ROS AprilTag data into our own type that does not rely on ROS.
            loc.setID( aprilTagInfo->detections[i].id[0] );

            // Pass the position of the AprilTag
            geometry_msgs::PoseWithCovarianceStamped tagPose = aprilTagInfo->detections[i].pose;
            loc.setPosition( make_tuple( tagPose.pose.pose.position.x,
                        tagPose.pose.pose.position.y,
                        tagPose.pose.pose.position.z ) );

            // Pass the orientation of the AprilTag
            loc.setOrientation( ::boost::math::quaternion<float>( tagPose.pose.pose.orientation.x,
                                        tagPose.pose.pose.orientation.y,
                                        tagPose.pose.pose.orientation.z,
                                        tagPose.pose.pose.orientation.w ) );
            tags.push_back(loc);

            //std::cout << loc << ' ';
            std::cout << tags.size() << ' ';
        }

        tagsDetected = true; 
    } else {
        tagsDetected = false; 
    }
}