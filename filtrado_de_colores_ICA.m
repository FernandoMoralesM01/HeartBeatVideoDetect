clc;
clear;
a= csvread('colores3.csv');
spo= csvread('spo2.csv');
[dnoised,icasig,A,W,mrem,AIC]=deartifactingICA(a);
csvwrite('coloresICA.csv',dnoised);


%%
Signals = a';

spo = normalize(spo);
Signals(:,1) = normalize(Signals(:,1));
Signals(:,2) = normalize(Signals(:,2));
Signals(:,3) = normalize(Signals(:,3));



function norm = normalize(sgnl)
    norm = (sgnl - min(sgnl)) / (max(sgnl) - min(sgnl));
end