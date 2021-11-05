%FYP: Drowsiness Detection 
%Data Analysis
%Harold Johnson    28805933
%2021

%Load Databases
load("Preprocessed_Database.mat");  % Processed files
load("Bed_System_Database.mat");    % Raw files

%% Database Information
%Data for Person 1 (Used initially to test for a single person)
%Load the raw data
% HR1 = table2array(Bed_System_Database.RawData{1,1}(:,3));
% PPG1 = table2array(Bed_System_Database.RawData{1,1}(:,1));
% pre1film0 = table2array(Bed_System_Database.RawData{1,1}(:,10));
% pre1film1 = table2array(Bed_System_Database.RawData{1,1}(:,12));
% pre1film2 = table2array(Bed_System_Database.RawData{1,1}(:,14));

%% Load processed data for comparison
% posfilm0 = table2array(Preprocessed_Database.FilteredData{1,1}(:,8));

%Normalise baseline to zero. (Rough approach)
% pre1film0 = pre1film0-mean(pre1film0);
% pre1film1 = pre1film1-mean(pre1film1);
% pre1film2 = pre1film2-mean(pre1film2);

%% Loop For Each Person
%Seperate matrix for each person
%Using the smallest value across most people in database
siglen = 400000;   % record 400,000 samples from each participant                 
people_ppg = zeros(siglen,1,40);    %Preallocate reference PPG matrix
people_bcg = zeros(siglen,3,40);    %Preallocate reference PPG matrix

%Parcipants included in testing
bcgval = [4:7,9:14,16:20,21:31,34,36:38,40];

for i=1:length(bcgval)
    %Obtain reference PPG signal for each participant
    people_ppg(:,1,i) = table2array(Preprocessed_Database.FilteredData{bcgval(i),1}(1:siglen,1));
    
    %Obtain BCG signal for each participant
    people_bcg(:,1:3,i) = [table2array(Bed_System_Database.RawData{bcgval(i),1}(1:siglen,10)),table2array(Bed_System_Database.RawData{bcgval(i),1}(1:siglen,12)),table2array(Bed_System_Database.RawData{bcgval(i),1}(1:siglen,14))];
end

%% Initial Conditions
%Used for real-time Arduino digital filtering
%First-Order Low-Pass Filter, For Processing the Raw BCG Signals
%Obtained from: https://www.youtube.com/watch?v=CPpOJsHuMsM
Fs = 1000;          %Sampling rate (Hz)
fc = 30;            %Cut-off frequency (Hz)
num = 2*pi*fc;      %numerator
den= [1 2*pi*fc];   %denominator
H = tf(num,den);    %First-order Low Pass Filter
Hd = c2d(H, 1/Fs);  

%produces a time domain result in the form below:
%y(n+1) = 0.8282y(n)+0.1718u(n);

%% TESTING SET-UP
w = 30000;  %Set window frame, sample length (1000 = 1 sec)
k = 10000;  %Set sliding frame,

%Set Parameters
maxlen = floor((siglen-w)/k);         %Set length of recordings (300,000-30,000)/k
ppgHR = zeros(maxlen,length(bcgval)); %Preallocate 
bcgHR0 = ppgHR;                       %Preallocate
bcgHR1 = ppgHR;                       %Preallocate
bcgHR2 = ppgHR;                       %Preallocate
noHr = ppgHR;   %number of beats (in siglen/fs seconds)

for j=1:length(bcgval)
    %Max length that can be run of the signal
    ppgLFHFratio = zeros(maxlen,j);
    LFHFratio = zeros(maxlen,j);
    
    for i=1:maxlen
        len = (1+(i-1)*k) : (w+(i-1)*k);
        
        %Calculate HR
        [noHr(i), ppgHR(i,j),ppgHRV] = ppgfun(len,Fs,people_ppg(len,1,j));
        [bcgHR0(i,j),bcgHRV0] = filmfun(len,Fs,people_bcg(len,1,j)); %Prefilm0
        %[bcgHR1(i,j),bcgHRV1] = filmfun(len,Fs,people_bcg(len,2,j)); %Prefilm1
        %[bcgHR2(i,j),bcgHRV2] = filmfun(len,Fs,people_bcg(len,3,j)); %Prefilm2

        %Calculate HRV Features via Spectral analysis of a sequence.
        [ppgpLF,ppgpHF,ppgLFHFratio(i,j),ppgVLF,ppgLF,ppgHF,pp1f,ppgY,ppgNFFT] = fft_val_fun(ppgHRV,Fs,'spline');
        [pLF,pHF,LFHFratio(i,j),VLF,LF,HF,f,Y,NFFT1] = fft_val_fun(bcgHRV0,Fs,'spline');
    end 
end
    
%% BLAND-ALTMAN PLOT
%     [m1,m2] = size(ppgHR);
%     [n1,n2] = size(bcgHR0);
%     ppgHR_full = reshape(ppgHR,[1,m1*m2]);    %Reshape to a row matrix
%     bcg0HR_full = reshape(bcgHR0,[1,n1*n2]);  %Reshape to a row matrix
%     bcg1HR_full = reshape(bcgHR1,[1,n1*n2]);
%     bcg2HR_full = reshape(bcgHR2,[1,n1*n2]);
 
%BlandAltmanPlot
%Obtained from Thrynae
%https://github.com/thrynae/BlandAltmanPlot
%     figure, h=BlandAltmanPlot(,bcg0HR_full',ppgHR_full');
%     title('Bland-Altman Plot','FontSize',16);
%     xlabel('Average HR (bpm)','FontSize',16);
%     ylabel({'Difference in HR (bpm)';'BCG - PPG'},'FontSize',16);
%     title('Bland-Altman Plot');
%     xlabel('Average HR (bpm)');
%     ylabel({'Difference in HR (bpm)';'BCG - PPG'});
%     ylim([-15 15]);
%     xlim([50 90]);
%     ax = gca;
%     ax.FontSize = 14; 

%Used for measuring the mean and loa for total and individual participants
%[mu,loa,CI]=BlandAltman_values((ppgHR_full+bcg0HR_full)/2,(ppgHR_full-bcg0HR_full),0.05)
%mean(abs(ppgHR_full-bcg0HR_full))

%% PPG Analysis for Comparison -----------------------------
function [noHR, ppgHR,ppgHRV] = ppgfun(len,Fs,ppg)
%[noHR, ppgHR,ppgHRV] = ppgfun(len,Fs,ppg)
%noHR is the number of HR beats obtained.
%ppgHR is the HR obtained for the refernce PPG signal
%ppgHRV is the HRV obtained for the refernce PPG signal
%len is the lenght of the signal. It is a column or row vector
%fs is the sampling frequency
%PPG is the vector of bcg signal data

%This process calculates the minpeakdistance for the findpeak function
peak_rng = length(ppg)/5;
minpeak = (max(ppg(peak_rng:end-peak_rng))-min(ppg(peak_rng:end-peak_rng)))/4;

%Findpeak is used to calculate the peaks and hence the peak-peak interval
[ppgpk,ppgpktime] = findpeaks(ppg,'MinPeakProminence',minpeak,'MinPeakDistance',500);
ppgpktime = ppgpktime+len(1);

%Number of HR detected is recorded.
noHR = length(ppgpktime);

%PPG Plot
%   figure(1), plot(len,ppg');
%   title('PPG Reference Signal');
%   ylabel('Amplitude');
%   xlabel('Time (s)');
%   set(gca,'XTick',0:5000:30000)
%   set(gca,'XTickLabel',0:5:30)
%
%   hold on
%   plot(ppgpktime,ppgpk,'rs');
%   hold off

%% Calculate Heart Rate 
% First and last peaks are excluded, sometimes results in obscure results
ppgHR = 60*(length(ppgpktime)-2)/((ppgpktime(end-1)-ppgpktime(2))/Fs);

%Calculate HRV (Root Mean Square oF Successive Differences)
%Calculates the time variations between peaks
%Currently set to calculate mean
%   ppgdiff = (diff(t*ppgpktime(2:end-1))/fs).^2;%Calculate difference and square
%   ppgHRV = sqrt(mean(ppgdiff));  %Sqrt(mean of interval squared) = RMSSD

%HRV is obtained by measuring the difference in peak-peak timing
ppgHRV = diff(ppgpktime(2:end-1))/Fs;
end
% ---------------------------------------------------------------

%% FILM BCG ANALYSIS FUNCTION
function [hfilmHR,hfilmHRV] = filmfun(len,fs,prefilm)
%% Calculate the Heart Rate and Heart Rate variability for BCG data
%[hfilmHR,hfilmHRV] = filmfun(len,fs,prefilm)
%hfilmHR is the HR obtained for the BCG signal via hilbert transform
%hfilmHRV is the HRV obtained for the BCG signal via hilbert transform
%len is the lenght of the signal. It is a column or row vector
%fs is the sampling frequency
%prefilm is the vector of bcg signal data

%Initialise
film = zeros(1,length(len));

%Apply First-Order Low Pass Filter
for i=2:length(len)
    %y(n+1) = 0.8282y(n)+0.1718u(n);
    film(i) = 0.8282*film(i-1)+0.1718*prefilm(i);
end

%Plot Figure
%   figure(2), plot(len,film);
%   title('BCG Sample Signal');
%   ylabel('Amplitude');
%   xlabel('Time (s)');
%   ylim([1.01 1.035]);
%   set(gca,'XTick',0:5000:30000)
%   set(gca,'XTickLabel',0:5:30)

%% (Hilbert Transform) (APPROACH 1)
%Imaginary component of the Hilbert Transform function is the actual
%hilbert transform
film_hilbert = hilbert(film); 
filmhilbert = imag(film_hilbert);

%This process calculates the minpeakdistance for the findpeak function
peak_rng = length(filmhilbert)/5;
minpeak = (max(filmhilbert(peak_rng:end-peak_rng))-min(filmhilbert(peak_rng:end-peak_rng)))/3;

%%Find peaks in the Hilbert transform
[hpk,hpktime] = findpeaks(filmhilbert,'MinPeakProminence',minpeak,'MinPeakDistance',500);

%Film Plot
%   figure(3), plot(len,filmhilbert); % Plot figure
%   title('BCG Sample Signal');
%   ylabel('Amplitude');
%   xlabel('Time (s)');
%   set(gca,'XTick',0:5000:30000)
%   set(gca,'XTickLabel',0:5:30)
%   ylim([-0.01 0.02]);

%% Calculate HR and HRV
%exclude first and last peaks (sometimes inaccurate)
%Calculate Heart Rate
hfilmHR = 60*(length(hpktime)-2)/((hpktime(end-1)-hpktime(2))/fs);     %BCG Heart Rate

%Calculate Heart Rate Variability
%filmdiff = (diff(t*pktime(2:end-1))/fs).^2; %Calculate difference and square
%filmHRV = sqrt(mean(filmdiff));             %Sqrt(mean of interval squared) = RMSSD
hfilmHRV = (diff(hpktime(2:end-1))/fs);


%% (Continuous Wavelet Transform) (APPROACH 2)(Incomplete)
%%Calculate Heart Rate 
%   sig = {film,1/fs};
%   film_cwt = cwtft(sig,'plot'); 
% 
%   cwt(film,Fs);
% 
%Find peaks in the Hilbert transform
%   [cpk,cpktime] = findpeaks(imag(film_cwt),'MinPeakDistance',500);
%   cpktime = cpktime+len(1);

%Calculate difference between peak times,
%Calculate Heart Rate
%   cfilmHR = 60*(length(cpktime)-2)/((cpktime(end-1)-cpktime(2))/fs);     %BCG Heart Rate
% 
%Calculate Heart Rate Variability
%   cfilmHRV = (diff(cpktime(2:end-1))/fs);

end


%% Performing HRV Feature Extraction via Spectral analysis of a sequence 
%Obtained from MarcusVollmer/HRV
%https://github.com/MarcusVollmer/HRV

function [pLF,pHF,LFHFratio,VLF,LF,HF,f,Y,NFFT] = fft_val_fun(RR,Fs,type)
%fft_val_fun Spectral analysis of a sequence.
%[pLF,pHF,LFHFratio,VLF,LF,HF,f,Y,NFFT] = fft_val_fun(RR,Fs,type)
%uses FFT to compute the spectral density function. 


    RR = RR(:);
    if nargin<2 || isempty(Fs)
        error('HRV.fft_val_fun: wrong number or types of arguments');
    end   
    if nargin<3
        type = 'spline';
    end
    switch type
        case 'none'
            RR_rsmp = RR;
        otherwise
            if sum(isnan(RR))==0 && length(RR)>1
                ANN = cumsum(RR)-RR(1);
                % use interp1 methods for resampling
                RR_rsmp = interp1(ANN,RR,0:1/Fs:ANN(end),type);
            else
                RR_rsmp = [];
            end
    end
    % FFT
    L = length(RR_rsmp); 
    if L==0 
        pLF = NaN;  pHF = NaN;  LFHFratio = NaN;
        VLF = NaN;  LF = NaN;   HF = NaN;
        f = NaN;    Y = NaN;    NFFT = NaN;
    else
        NFFT = 2^nextpow2(L);
        Y = fft(HRV.nanzscore(RR_rsmp),NFFT)/L;
        f = Fs/2*linspace(0,1,NFFT/2+1);  

        YY = 2*abs(Y(1:NFFT/2+1));
        YY = YY.^2;
        
        VLF = sum(YY(f<=.04));
        LF  = sum(YY(f<=.15))-VLF;  
        HF  = sum(YY(f<=.4))-VLF-LF;
        TP  = sum(YY(f<=.4));

        pLF = LF/(TP-VLF)*100;
        pHF = HF/(TP-VLF)*100;    
        LFHFratio = LF/HF; 
    end
end
