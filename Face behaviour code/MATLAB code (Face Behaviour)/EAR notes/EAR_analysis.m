% EAR analysis from extracted EAR notes
% Jonathan Dulce
% Last edited: 5 Nov 2021
clc; clear all; close all;
load('EAR_notes.mat');% EAR analysis
%% Fixing outliers

% remove NAN
EARstillness = EARstillness(~isnan(EARstillness));
EARsleepyEyes = EARsleepyEyes(~isnan(EARsleepyEyes));

% combine
EARcombined = [EARsleepyEyes EARstillness];

%% sort notes
EARstillness = sort(EARstillness);
EARsleepyEyes = sort(EARsleepyEyes);
EARcombined = sort(EARcombined);

%% find statistics

stillness_mean = mean(EARstillness);
stillness_median = median(EARstillness);
stillness_iqr = iqr(EARstillness);
stillness_quantiles = quantile(EARstillness, [0.25, 0.50, 0.75]);
stillness_max = stillness_quantiles(3)+1.5*stillness_iqr;
stillness_min = stillness_quantiles(3)-1.5*stillness_iqr;
stillness_80 = quantile(EARstillness, 0.2);
stillness_std = std(EARstillness);

sleepyEyes_mean = mean(EARsleepyEyes);
sleepyEyes_median = median(EARsleepyEyes);
sleepyEyes_iqr = iqr(EARsleepyEyes);
sleepyEyes_quantiles = quantile(EARsleepyEyes, [0.25, 0.50, 0.75]);
sleepyEyes_max = sleepyEyes_quantiles(3)+1.5*sleepyEyes_iqr;
sleepyEyes_min = sleepyEyes_quantiles(3)-1.5*sleepyEyes_iqr;
sleepyEyes_80 = quantile(EARsleepyEyes, 0.2);
sleepyEyes_std = std(EARsleepyEyes);


combined_mean = mean(EARcombined);
combined_median = median(EARcombined);
combined_iqr = iqr(EARcombined);
combined_quantiles = quantile(EARcombined, [0.25, 0.50, 0.75]);
combined_max = combined_quantiles(3)+1.5*combined_iqr;
combined_min = combined_quantiles(3)-1.5*combined_iqr;
combined_80 = quantile(EARcombined, 0.135);
combined_std = std(EARcombined);

%% plot

% sorted data
figure(1);
scatter(1:1:length(EARstillness), EARstillness);
title("Eye Aspect Ratio (EAR) - ""Stillness""");
xlabel("Frame Sample");
ylabel("EAR");
figure(2);
scatter(1:1:length(EARsleepyEyes), EARsleepyEyes);
title("Eye Aspect Ratio (EAR) - ""Sleepy Eyes""");
xlabel("Frame Sample");
ylabel("EAR");
figure(3);
scatter(1:1:length(EARcombined), EARcombined);
title("Eye Aspect Ratio (EAR) - ""Combined""");
xlabel("Frame Sample");
ylabel("EAR");

% histograms
figure(4);
histogram(EARstillness);
title("Eye Aspect Ratio (EAR) - ""Stillness""");
ylabel("Number of Frame Samples");
xlabel("EAR");
figure(5);
histogram(EARsleepyEyes);
title("Eye Aspect Ratio (EAR) - ""Sleepy Eyes""");
ylabel("Number of Frame Samples");
xlabel("EAR");
figure(6);
histogram(EARcombined);
title("Eye Aspect Ratio (EAR) - ""Combined""");
ylabel("Number of Frame Samples");
xlabel("EAR");

% boxplots
figure(7);
boxplot(EARstillness);
title("Eye Aspect Ratio (EAR) - ""Stillness""");
figure(8);
boxplot(EARsleepyEyes);
title("Eye Aspect Ratio (EAR) - ""Sleepy Eyes""");
figure(9);
boxplot(EARcombined);
title("Eye Aspect Ratio (EAR) - ""Combined""");


