% prepare workspace
clear all; close all; clc; format compact;

% intialize ros node
if(~robotics.ros.internal.Global.isNodeActive)
    rosinit('192.168.1.3'); % ip of the ROS Master
end

apriltagSubscriber = rossubscriber('/tag_detection');

r = robotics.Rate(100);
reset(r);

apriltagMsg = apriltagSubscriber.LatestMessage;

while(1)
    tic
    pause(eps);
    
    apriltagMsg = apriltagSubscriber.LatestMessage;

    % fixed loop pause
    waitfor(r);
end
    