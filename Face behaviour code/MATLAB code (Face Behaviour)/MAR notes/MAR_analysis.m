% MAR analysis from extracted MAR notes
% Jonathan Dulce
% Last edited: 5 Nov 2021
clc; clear all; close all;
load('MAR_notes.mat');
%% Fixing outliers

% remove NAN
MARstillness = MARstillness(~isnan(MARstillness));
MARtalking = MARtalking(~isnan(MARtalking));
MARyawning = MARyawning(~isnan(MARyawning));


% remove MAR>1
% MARstillness = MARstillness(MARstillness<1);
% MARtalking = MARtalking(MARtalking<1);
% MARyawning = MARyawning(MARyawning<1);

%% sort notes
% MARstillness = sort(MARstillness);
% MARtalking = sort(MARtalking);
% MARyawning = sort(MARyawning);

%% Calculate statistics
stillness_mean = mean(MARstillness);
stillness_median = median(MARstillness);
stillness_iqr = iqr(MARstillness);
stillness_quantiles = quantile(MARstillness, [0.25, 0.50, 0.75]);
stillness_max = stillness_quantiles(3)+1.5*stillness_iqr;
stillness_min = min(MARstillness);
stillness_std = std(MARstillness);

talking_mean = mean(MARtalking);
talking_median = median(MARtalking);
talking_iqr = iqr(MARtalking);
talking_quantiles = quantile(MARtalking, [0.25, 0.50, 0.75]);
talking_max = talking_quantiles(3)+1.5*talking_iqr;
talking_min = min(MARtalking);
talking_std = std(MARtalking);

yawning_mean = mean(MARyawning);
yawning_median = median(MARyawning);
yawning_iqr = iqr(MARyawning);
yawning_quantiles = quantile(MARyawning, [0.25, 0.50, 0.75]);
yawning_max = yawning_quantiles(3)+1.5*yawning_iqr;
yawning_min = min(MARyawning);
yawning_std = std(MARyawning);

%% Calculate accuracy
total_frames = length([MARyawning, MARstillness, MARtalking]);
still_th = 0.06;
talk_th = 0.23;
yawn_th = 1;

% closed accuracy
still_success = sum(([MARstillness < still_th, MARtalking> still_th, MARyawning>still_th])==1);
still_success_rate = still_success/total_frames;

% talking accuracy
talk_success = sum(([(MARstillness < still_th) | (MARstillness > talk_th) , ...
    (MARtalking > still_th) & (MARtalking < talk_th), ...
    (MARyawning < still_th) | (MARyawning > talk_th)])==1);
talk_success_rate = talk_success/total_frames;

% yawning accuracy
yawn_success = sum(([(MARstillness < talk_th) | (MARstillness > yawn_th) , ...
    (MARtalking < talk_th) | (MARtalking > yawn_th), ...
    (MARyawning > talk_th) & (MARyawning < yawn_th)])==1);
yawn_success_rate = yawn_success/total_frames;

%% MAR graphs

% raw data
figure(1)
scatter(1:1:length(MARstillness), MARstillness);
title("Mouth Aspect Ratio (MAR) - ""Stillness""");
xlabel("Frame Sample");
ylabel("MAR");
figure(2)
scatter(1:1:length(MARtalking),MARtalking);
title("Mouth Aspect Ratio (MAR) - ""Talking""");
xlabel("Frame Sample");
ylabel("MAR");
figure(3)
scatter(1:1:length(MARyawning),MARyawning);
title("Mouth Aspect Ratio (MAR) - ""Yawning""");
xlabel("Frame Sample");
ylabel("MAR");

% boxplots
figure(4)
boxplot(MARstillness, 'symbol', '');
title("Mouth Aspect Ratio (MAR) - ""Stillness""");
ylabel("MAR")
ylim([-0.1, 1.1]);
figure(5);
boxplot(MARtalking, 'symbol', '');
title("Mouth Aspect Ratio (MAR) - ""Talking/Laughing""");
ylabel("MAR")
ylim([-0.1, 1.1]);
figure(6);
boxplot(MARyawning, 'symbol', '');
title("Mouth Aspect Ratio (MAR) - ""Yawning""");
ylabel("MAR")
ylim([-0.1, 1.1]);

%% plot boxplots on one graph
g1 = repmat({'Stillness'},length(MARstillness),1);
g2 = repmat({'Talking/Laughing'},length(MARtalking),1);
g3 = repmat({'Yawning'},length(MARyawning),1);
g = [g1; g2; g3];

figure(7);
boxplot([MARstillness'; MARtalking'; MARyawning'],g,'symbol', '','Labels', {'Stillness', 'Talking/Laughing', 'Yawning'});
title("Mouth Aspect Ratio (MAR)");
ylabel("MAR")
ylim([-0.1, 1.1]);

%% histograms
% figure(7)
% histogram(MARstillness)
% title("MAR stillness")
% figure(8)
% histogram(MARtalking)
% title("MAR talking")
% figure(9)
% histogram(MARyawning)
% title("MAR yawning")