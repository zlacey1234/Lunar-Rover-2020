clear;
close all;
clc;

%% Comment one of these out

% Zachary Lacey Microsoft Surface
%pathToNavigationLogs = 'C:\Users\zlace\OneDrive\Documents\AMAV\Lunar-Rover-2020\development\data_analysis\Navigation';

%Zachary Lacey Dell Laptop
pathToNavigationLogs = 'D:\Lunar-Rover-2020\development\data_analysis\Apriltag'

%%
cd(pathToNavigationLogs)
%%
[file1,path1] = uigetfile('*.log');

[file2,path2] = uigetfile('*.log');

[file3,path3] = uigetfile('*.log');

[file4,path4] = uigetfile('*.log');

[file5,path5] = uigetfile('*.log');

[file6,path6] = uigetfile('*.log');

[file7,path7] = uigetfile('*.log');

[file8,path8] = uigetfile('*.log');


file1
filepath1 = [path1 file1];
data1 = csvread(filepath1);

file2
filepath2 = [path2 file2];
data2 = csvread(filepath2);

file3
filepath3 = [path3 file3];
data3 = csvread(filepath3);

file4
filepath4 = [path4 file4];
data4 = csvread(filepath4);

file5
filepath5 = [path5 file5];
data5 = csvread(filepath5);

file6
filepath6 = [path6 file6];
data6 = csvread(filepath6);

file7
filepath7 = [path7 file7];
data7 = csvread(filepath7);

file8
filepath8 = [path8 file8];
data8 = csvread(filepath8);

%%      [ID         Size         Time        X           Y          Z     ];

Data1 = [data1(:,1) data1(:,2) data1(:,3) data1(:,4) data1(:,5) data1(:,6)];
Data2 = [data2(:,1) data2(:,2) data2(:,3) data2(:,4) data2(:,5) data2(:,6)];
Data3 = [data3(:,1) data3(:,2) data3(:,3) data3(:,4) data3(:,5) data3(:,6)];
Data4 = [data4(:,1) data4(:,2) data4(:,3) data4(:,4) data4(:,5) data4(:,6)];
Data5 = [data5(:,1) data5(:,2) data5(:,3) data5(:,4) data5(:,5) data5(:,6)];
Data6 = [data6(:,1) data6(:,2) data6(:,3) data6(:,4) data6(:,5) data6(:,6)];
Data7 = [data7(:,1) data7(:,2) data7(:,3) data7(:,4) data7(:,5) data7(:,6)];
Data8 = [data8(:,1) data8(:,2) data8(:,3) data8(:,4) data8(:,5) data8(:,6)];

%%

numel(Data1(:,1));
Data2Array = Data2(1:numel(Data1(:,1)),:);
Data3Array = Data3(1:numel(Data1(:,1)),:);

DataError1_2X = Data1(:,4) - Data2Array(:,4);
DataError1_2Z = Data1(:,6) - Data2Array(:,6);

DataError1_2 = sqrt(DataError1_2X.^2 + DataError1_2Z.^2)

DataError3_2X = Data2Array(:,4) - Data3Array(:,4);
DataError3_2Z = Data2Array(:,6) - Data3Array(:,6);

DataError3_2 = sqrt(DataError3_2X.^2 + DataError3_2Z.^2)

DataError1_3X = Data1(:,4) - Data3Array(:,4);
DataError1_3Z = Data1(:,6) - Data3Array(:,6);

DataError1_3 = sqrt(DataError1_3X.^2 + DataError1_3Z.^2)

% figure(1)
% subplot(2,1,1)
% hold on
% plot(Data1(:,3),Data3Array(:,4),'LineWidth', 1)
% plot(Data1(:,3),Data2Array(:,4),'LineWidth', 1)
% plot(Data1(:,3),Data1(:,4),'LineWidth', 1)
% title('Position X vs Time for Apriltags, 70 cm Away')
% axis([0 30 -0.3 0.2])
% xlabel('Time (seconds)');
% ylabel('Position X (meters)');
% legend('Tag ID: 0','Tag ID: 1', 'Tag ID: 2');
% grid on 
% set(gca, 'FontSize',20);
% hold off 
% 
% subplot(2,1,2)
% hold on
% plot(Data1(:,3),Data3Array(:,6),'LineWidth', 1)
% plot(Data1(:,3),Data2Array(:,6),'LineWidth', 1)
% plot(Data1(:,3),Data1(:,6),'LineWidth', 1)
% title('Position Z vs Time for Apriltags, 70 cm Away')
% axis([0 30 0.2 0.22])
% xlabel('Time (seconds)');
% ylabel('Position Z (meters)');
% legend('Tag ID: 0','Tag ID: 1', 'Tag ID: 2');
% grid on 
% set(gca, 'FontSize',20);
% hold off  


Actual = ones(numel(Data1(:,1)))*(8.5)*2.54/100;
figure(2)
hold on
plot(Data1(:,3),DataError1_2,'LineWidth', 1)
plot(Data1(:,3),DataError3_2,'LineWidth', 1)
plot(Data1(:,3),Actual, '--m', 'LineWidth', 2)
title('Distance Between the Apriltags Centroids vs Time')
xlabel('Time (seconds)');
ylabel('Distance (meters)');
legend('Distance Error Between Tag ID: 1 and Tag ID: 2','Distance Error Between Tag ID: 0 and Tag ID: 1','Actual Measured Distance Error');
axis([0 30 0.21 0.22])
grid on 
set(gca, 'FontSize',20);
hold off  

% plot(Data1(:,3),DataError1_3)
% figure(1)
% subplot(3,1,1)
% hold on 
% plot(Data1(:,3), Data1(:,4))
% plot(Data2(:,3), Data2(:,4))
% plot(Data3(:,3), Data3(:,4))
% plot(Data4(:,3), Data4(:,4))
% plot(Data5(:,3), Data5(:,4))
% plot(Data6(:,3), Data6(:,4))
% plot(Data7(:,3), Data7(:,4))
% plot(Data8(:,3), Data8(:,4))
% hold off 
% 
% subplot(3,1,2)
% hold on 
% plot(Data1(:,3), Data1(:,5))
% plot(Data2(:,3), Data2(:,5))
% plot(Data3(:,3), Data3(:,5))
% plot(Data4(:,3), Data4(:,5))
% plot(Data5(:,3), Data5(:,5))
% plot(Data6(:,3), Data6(:,5))
% plot(Data7(:,3), Data7(:,5))
% plot(Data8(:,3), Data8(:,5))
% hold off 
% 
% subplot(3,1,3)
% hold on 
% plot(Data1(:,3), Data1(:,6))
% plot(Data2(:,3), Data2(:,6))
% plot(Data3(:,3), Data3(:,6))
% plot(Data4(:,3), Data4(:,6))
% plot(Data5(:,3), Data5(:,6))
% plot(Data6(:,3), Data6(:,6))
% plot(Data7(:,3), Data7(:,6))
% plot(Data8(:,3), Data8(:,6))
% hold off 
% 
% figure(2)
% hold on 
% plot(Data1(:,3), Data1(:,4))
% plot(Data2(:,3), Data2(:,4))
% plot(Data3(:,3), Data3(:,4))
% plot(Data4(:,3), Data4(:,4))
% plot(Data5(:,3), Data5(:,4))
% plot(Data6(:,3), Data6(:,4))
% hold off 
% 
% figure(3)
% hold on
% plot(Data1(:,4), Data1(:,6))
% plot(Data2(:,4), Data2(:,6))
% plot(Data3(:,4), Data3(:,6))
% plot(Data4(:,4), Data4(:,6))
% plot(Data5(:,4), Data5(:,6))
% plot(Data6(:,4), Data6(:,6))