%% ORIGINAL VERSION
% function seedpt = selectseedpt_rev(peakim)
% a = peakim(peakim > 0); % only care about positive peaks
% [x,y] = find(peakim > 0);
% indices = sub2ind(size(peakim),x,y);
% val = peakim(indices); 
% seedpt = [val,x,y];
% seedpt = flipud(sortrows(seedpt));
% 
% pd = fitdist(a,'lognormal');
% thresh = exp(pd.mu + pd.sigma.^2 /2); %threshold to filter out seed pts
% 
% seedpt(seedpt(:,1) < thresh,:) = []; %change here
% seedpt(:,1) = [];
% end

%%
% OPTIONS 1
% uses Otsu's method to binarize the peak image, then removes small objects (i.e., noise) from the binary image 
% using the bwareaopen function. We then use the bwconncomp function to label connected components in the binary image, 
% and sort them in descending order of peak value. We then convert the resulting props structure to a matrix of [peak value, x, y] triplets, 
% and fit a log-normal distribution to the peak values. Finally, we use logical indexing to filter out peaks with value less than the threshold, 
% and return a matrix of [x, y] coordinates for the remaining peaks. This implementation is more robust to noise and can handle images with multiple disconnected peaks.

% function seedpt = selectseedpt_rev(peakim)
% % Binarize the peak image using Otsu's method
% bw = imbinarize(peakim, 'adaptive', 'Sensitivity', 0.5);
% 
% % Remove small objects (i.e., noise) from the binary image
% bw = bwareaopen(bw, 10);
% 
% % Label connected components in the binary image
% cc = bwconncomp(bw);
% 
% % Get the pixel values and locations of each connected component
% props = regionprops(cc, peakim, 'PixelValues', 'PixelIdxList');
% 
% % Convert the props structure to a matrix of [peak value, x, y] triplets
% num_peaks = length(props);
% seedpt = zeros(num_peaks, 3);
% for i = 1:num_peaks
%     [x, y] = ind2sub(size(peakim), props(i).PixelIdxList);
%     peak_vals = props(i).PixelValues;
%     peak_val = max(peak_vals);
%     seedpt(i, :) = [peak_val, x(1), y(1)];
% end
% 
% % Sort the components in descending order of peak value
% [~, idx] = sort(seedpt(:, 1), 'descend');
% seedpt = seedpt(idx, :);
% 
% % Fit a log-normal distribution to the peak values
% pd = fitdist(log(seedpt(:, 1)), 'lognormal');
% 
% % Filter out peaks with value less than threshold
% thresh = exp(pd.mu + pd.sigma.^2 / 2);
% keep_idx = seedpt(:, 1) >= thresh;
% seedpt = seedpt(keep_idx, 2:3);
% end

%% 
%OPTIONS 2: 
% function seedpt = selectseedpt_rev(peakim)
% bw = imbinarize(peakim, 'adaptive', 'Sensitivity', 0.5);
% 
% % Remove small objects (i.e., noise) using erosion
% se = strel('disk', 1);
% bw = imerode(imdilate(bw, se),se);
% 
% % Label connected components in the binary image
% cc = bwconncomp(bw);
% props = regionprops(cc, peakim, 'PixelValues', 'PixelIdxList');
% 
% % Convert the props structure to a matrix of [peak value, x, y] triplets
% num_peaks = length(props);
% seedpt = zeros(num_peaks, 3);
% for i = 1:num_peaks
%     [x, y] = ind2sub(size(peakim), props(i).PixelIdxList);
%     peak_vals = props(i).PixelValues;
%     peak_val = max(peak_vals);
%     seedpt(i, :) = [peak_val, x(1), y(1)];
% end
% 
% % Sort the components in descending order of peak value using median filtering
% max_filter_size = 3;
% peak_vals = seedpt(:, 1);
% peak_vals_filt = medfilt1(peak_vals, max_filter_size);
% [~, idx] = sort(peak_vals_filt, 'descend');
% seedpt = seedpt(idx, :);
% 
% % Filter out peaks with value less than threshold using Gaussian distribution
% peak_vals = seedpt(:, 1);
% thresh = mean(peak_vals) - 2*std(peak_vals);
% keep_idx = peak_vals > thresh;
% seedpt = seedpt(keep_idx, 2:3);
% end

%%
%OPTION 3:
function seedpt = selectseedpt_rev(peakim)
bw = imbinarize(peakim, 'adaptive', 'Sensitivity', 0.5);

% Remove small objects (i.e., noise) using erosion
se = strel('disk', 1);
bw = imerode(imdilate(bw, se),se);

% Label connected components in the binary image
cc = bwconncomp(bw);
props = regionprops(cc, peakim, 'PixelValues', 'PixelIdxList');

% Convert the props structure to a matrix of [peak value, x, y] triplets
num_peaks = length(props);
seedpt = zeros(num_peaks, 3);
for i = 1:num_peaks
    [x, y] = ind2sub(size(peakim), props(i).PixelIdxList);
    peak_vals = props(i).PixelValues;
    peak_val = max(peak_vals);
    seedpt(i, :) = [peak_val, x(1), y(1)];
end

% Sort the components in descending order of peak value
[~, idx] = sort(seedpt(:, 1), 'descend');
seedpt = seedpt(idx, :);

% Filter out peaks with value less than threshold using Gaussian distribution
peak_vals = seedpt(:, 1);
thresh = mean(peak_vals) - 2*std(peak_vals);
keep_idx = peak_vals > thresh;
seedpt = seedpt(keep_idx, 2:3);
end

%%
% %OPTION 4: fast non-maximum suppression
% function seedpt = selectseedpt_rev(peakim, neighborhood_size)
% % Set default value for neighborhood_size if not provided
% if nargin < 2
%     neighborhood_size = 3;
% end
% 
% % Apply non-maximum suppression to the peak image
% se = strel('rectangle', [neighborhood_size, neighborhood_size]);
% maxim = imdilate(peakim, se);
% seedpt = (peakim == maxim) & (peakim > 0);
% 
% % Get the coordinates of the remaining peaks
% [y, x] = find(seedpt);
% 
% % Sort the peaks in descending order of peak value
% peak_vals = peakim(seedpt);
% [~, idx] = sort(peak_vals, 'descend');
% x = x(idx);
% y = y(idx);
% 
% seedpt = [x, y];
% end

%%
%OPTION 5: Hessian-based blob detection and non-maximum suppression

% function seedpt = selectseedpt_rev(peakim, sigma, threshold, neighborhood_size)
% % Set default value for sigma if not provided
% if nargin < 2
%     sigma = 2;
% end
% 
% % Set default value for threshold if not provided
% if nargin < 3
%     threshold = 0.01;
% end
% 
% % Set default value for neighborhood_size if not provided
% if nargin < 4
%     neighborhood_size = 3;
% end
% 
% % Apply Hessian-based blob detection to the peak image
% [h, w] = size(peakim);
% hessian_response = zeros(h, w);
% for i = 1:h
%     for j = 1:w
%         H = hessian2D(peakim, i, j, sigma);
%         R = det(H) - threshold * trace(H)^2;
%         hessian_response(i, j) = R;
%     end
% end
% 
% % Apply non-maximum suppression to the hessian response
% se = strel('rectangle', [neighborhood_size, neighborhood_size]);
% maxim = imdilate(hessian_response, se);
% suppressed_response = (hessian_response == maxim) & (hessian_response > 0);
% 
% % Get the coordinates of the remaining peaks
% [y, x] = find(suppressed_response);
% 
% % Sort the peaks in descending order of response value
% response_vals = hessian_response(suppressed_response);
% [~, idx] = sort(response_vals, 'descend');
% x = x(idx);
% y = y(idx);
% 
% seedpt = [x, y];
% 
% % Fit a log-normal distribution to the peak values
% pd = fitdist(log(response_vals), 'lognormal');
% 
% % Filter out peaks with value less than threshold
% thresh = exp(pd.mu + pd.sigma.^2 / 2);
% keep_idx = response_vals >= thresh;
% seedpt = seedpt(keep_idx, :);
% end
% 
% % Function to compute the Hessian matrix at a given pixel in an image
% function H = hessian2D(I, x, y, sigma)
% dx = sigma * (1 + floor(sigma * 3));
% [x1, x2] = meshgrid(x-dx:x+dx, x-dx:x+dx);
% [y1, y2] = meshgrid(y-dx:y+dx, y-dx:y+dx);
% Gxx = imgaussfilt(I(x1, y1), sigma) + imgaussfilt(I(x2, y2), sigma) - 2 * imgaussfilt(I(x, y1), sigma) - 2 * ...
%     imgaussfilt(I(x1, y), sigma) + 4 * imgaussfilt(I(x, y), sigma);
% Gxy = imgaussfilt(I(x1, y1), sigma) - imgaussfilt(I(x1, y2), sigma) - ...
%     imgaussfilt(I(x2, y1), sigma) + imgaussfilt(I(x2, y2), sigma);
% Gyy = imgaussfilt(I(x1, y1), sigma) + imgaussfilt(I(x1, y2), sigma) - 2 * ...
%     imgaussfilt(I(x1, y), sigma) - 2 * imgaussfilt(I(x2, y), sigma) + 4 * imgaussfilt(I(x, y), sigma);
% H = [Gxx, Gxy; Gxy, Gyy];
% end



