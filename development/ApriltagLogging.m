% prepare workspace
clear all; close all; clc; format compact;

% intialize ros node
%if(~robotics.ros.internal.Global.isNodeActive)
    rosinit('192.168.1.2'); % ip of the ROS Master
%end

timeLimit = 30; % seconds

apriltagSubscriber = rossubscriber('/tag_detections','apriltag_ros/AprilTagDetectionArray');

r = robotics.Rate(40);
reset(r);

apriltagMsg = apriltagSubscriber.LatestMessage;

%% Apriltag

% Apriltag Time
ApriltagTime = apriltagMsg.Header.Stamp.Sec;
ApriltagTimeNSec = apriltagMsg.Header.Stamp.Nsec;

ApriltagTimeLog = double(ApriltagTime) + double(ApriltagTimeNSec)*10^-9;

initialTime = ApriltagTimeLog;

% Apriltag ID
ApriltagID = apriltagMsg.Detections.Id;

% Apriltage size
ApriltagSize = apriltagMsg.Detections.Size;

dateString = datestr(now,'mmmm_dd_yyyy_HH_MM_SS_FFF')

ApriltagLog = ['/home/zachary/Lunar-Rover-2020/development/data_analysis/Apriltag' '/Apriltag_' dateString '.log'];


while(1)
    tic
    pause(eps);
    
    apriltagMsg = apriltagSubscriber.LatestMessage;
    
    %% Apriltag

    % Apriltag Time
    ApriltagTime = apriltagMsg.Header.Stamp.Sec;
    ApriltagTimeNSec = apriltagMsg.Header.Stamp.Nsec;

    ApriltagTimeLog = double(ApriltagTime) + double(ApriltagTimeNSec)*10^-9;
    
    ApriltagTimeLog = ApriltagTimeLog - initialTime
    
    % Apriltag ID
    ApriltagID = apriltagMsg.Detections.Id;

    % Apriltage size
    ApriltagSize = apriltagMsg.Detections.Size;

    ApriltagSeq = apriltagMsg.Header.Seq;
    apriltagPose = apriltagMsg.Detections.Pose;
    % Apriltag Position
    ApriltagPositionX = apriltagPose.Pose.Pose.Position.X;
    ApriltagPositionY = apriltagPose.Pose.Pose.Position.Y;
    ApriltagPositionZ = apriltagPose.Pose.Pose.Position.Z;

    ApriltagOrienationX = apriltagPose.Pose.Pose.Orientation.X;
    ApriltagOrienationY = apriltagPose.Pose.Pose.Orientation.Y;
    ApriltagOrienationZ = apriltagPose.Pose.Pose.Orientation.Z;
    ApriltagOrienationW = apriltagPose.Pose.Pose.Orientation.W;
    
    if (ApriltagTimeLog >= timeLimit)
        return;
    else
        ApriltagLog
        [pFile1, message] = fopen(ApriltagLog,'a');
    
%        fprintf(pFile1,'%6.6f,',ApriltagSeq);
        fprintf(pFile1,'%6.6f,',ApriltagID);
        fprintf(pFile1,'%6.6f,', ApriltagSize);
        fprintf(pFile1,'%6.6f,', ApriltagTimeLog);
        
        fprintf(pFile1,'%6.6f,', ApriltagPositionX);
        fprintf(pFile1,'%6.6f,', ApriltagPositionY);
        fprintf(pFile1,'%6.6f,', ApriltagPositionZ);
        
        fprintf(pFile1,'%6.6f,', ApriltagOrienationX);
        fprintf(pFile1,'%6.6f,', ApriltagOrienationY);
        fprintf(pFile1,'%6.6f,', ApriltagOrienationZ);
        fprintf(pFile1,'%6.6f\n', ApriltagOrienationW);
        
        fclose(pFile1);
    end
    % fixed loop pause
    waitfor(r);
end
    