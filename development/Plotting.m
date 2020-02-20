clear;
close all;
clc;

%% Toggle Flags
plotVIO = 1;
plotDesiredPose = 1;
plotVelocityCmd = 0;

pathToNavigationLogs = 'C:\Users\zlace\OneDrive\Documents\AMAV\Lunar-Rover-2020\development\data_analysis\Navigation';
cd(pathToNavigationLogs)

% VIO file SELECT This Only
[file1,path1] = uigetfile('*.log');

checkString = extractBetween(file1,1,3);
isVIO = strcmp(checkString{1,1}, 'VIO');

if ~isVIO
    disp('You must choose a VIO csv log');
    return
end

if plotVelocityCmd
    file2 = replaceBetween(file1,1,3,'VelCmd');
    path2 = path1;
end

if plotDesiredPose
    file3 = replaceBetween(file1,1,3,'DesiredPose');
    path3 = path1;
end

%% VIO 
if plotVIO
    file1
    filepath1 = [path1 file1];
    data1 = csvread(filepath1);
    
    % parse out
    TimeVIO = data1(:,1);
    TimeVIO = TimeVIO - TimeVIO(1);
    PositionXVIO = data1(:,2);
    PositionYVIO = data1(:,3);
    PositionZVIO = data1(:,4);
    PositionXVIOBodyFrame = -PositionYVIO;
    PositionYVIOBodyFrame = PositionXVIO;
    PositionZVIOBodyFrame = PositionZVIO;
    
    OrientationPhiVIO = data1(:,5);
    OrientationThetaVIO = data1(:,6);
    OrientationPsiVIO = data1(:,7);
    
    LinearVelocityXVIO = data1(:,8);
    LinearVelocityYVIO = data1(:,9);
    LinearVelocityZVIO = data1(:,10);
    AngularVelocityXVIO = data1(:,11);
    AngularVelocityYVIO = data1(:,12);
    AngularVelocityZVIO = data1(:,13);
end

if plotDesiredPose
    file3
    filepath3 = [path3 file3];
    data3 = csvread(filepath3);
    
    DesiredPositionX = data3(:,1);
    DesiredPositionY = data3(:,2);
    
    DesiredYaw = data3(:,3);
end

figure(1)
hold on
plot(TimeVIO, rad2deg(DesiredYaw))
plot(TimeVIO, OrientationPsiVIO)
title('Proportional Yaw Control Response on the Segway RMP 440 LE');
xlabel('Time (seconds)');
ylabel('Yaw (Degrees)');
legend('Desired Yaw', 'Intel Realsense Estimation')
grid on 
set(gca, 'FontSize',12);
hold off

figure(2)
subplot(2,1,1)
plot(TimeVIO, DesiredPositionX);
hold on
plot(TimeVIO, PositionXVIO);
hold off

subplot(2,1,2)
plot(TimeVIO, DesiredPositionY);
hold on
plot(TimeVIO, PositionYVIO);
hold off




