function processframe_rev(infilename1,outfilenamelayer)
%% Step 0: Data Input
[geoinfo,echogram] =readdata_rev(infilename1);
[~,imAmp, ysrf,ybtm] = preprocessing_rev(geoinfo,echogram);

%% Step 1: Produce the feature image
scales = 3:15;
wavelet = 'mexh';
bgSkip = 50;
peakim = peakimcwt(imAmp,scales,wavelet,ysrf,ybtm,bgSkip);
%peakim = peakimcwt_rev(imAmp,scales,wavelet,ysrf,ybtm,bgSkip);

%% Step 2: Pick Seed points
seedpt = selectseedpt_rev(peakim);

%% Step3: layer-tracing and post-processing
% DIST = 3; BLOCKSIZE = 5;
% define parameters: distance allowance, block size, slope angle difference
DIST = 7; BLOCKSIZE = 51; SMOOTHANGLE = 90;
if nargin < 3
  params = {DIST,BLOCKSIZE,SMOOTHANGLE}; 
end
tic;
[imLayer] = tracelayers(peakim,seedpt,params);
toc;
[labelLayer] = postprocesslayers(imLayer,DIST);

%%
% Output folder path
folderPath = './result-for-kdd/MARESELP_pht_v3/20120511_01_061-067/';
filename = split(outfilenamelayer,'.');
outfile = [filename{1},'.mat'];

% Full path to the output file
fullFilePath = fullfile(folderPath, outfile);
savelayersandraw_rev(imLayer,labelLayer,imAmp,ysrf,ybtm,fullFilePath)
end
