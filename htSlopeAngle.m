function [ht_agtan,shift] = htSlopeAngle(im,gapfill,buffdist)%, N, K)

    if nargin < 3
        buffdist = ceil(size(im,1)/3);
    end
    if nargin < 2 || gapfill == 0
        gapfill = ceil(size(im,2) * 0.25);
    end
    ht_agtan = nan;shift = 0;
    
    % keep minlen not change
    minlen = ceil(size(im,2) * 0.25);
    
    ht_agtan_initial = slopestimate(im,gapfill,minlen);
    if isnan(ht_agtan_initial),return; end

    [newim, shift] = adjustslopeim(im,ht_agtan_initial,buffdist);
    
    if isnan(newim), ht_agtan = ht_agtan_initial; return; end
    ht_agtan = slopestimate(newim,gapfill,minlen); 
end
%%
function ht_agtan = slopestimate(im, gapfill,minlen)
    if nargin < 2
        gapfill = ceil(size(im,2) * 0.25);
        minlen = ceil(size(im,2) * 0.25);
    end
    ht_agtan = nan;
    [H, theta,rho] = hough(im);
    P = houghpeaks(H); % default is pick the largest peak in HT domain
    if isempty(P)
        return;
    else
    lines = houghlines(im,theta,rho, P, 'FillGap',gapfill,'MinLength',minlen);
    if isempty(lines)
        return;
    else
        ht_angle = 0;
        nline = 0;
        for k = 1:length(lines)
            xy = [lines(k).point1; lines(k).point2]; % column 1 is x, 2 is y
            if xy(2,1) - xy(1,1) == 0
                nline = nline - 1;
                continue;
            else
                angle = (xy(2,2)-xy(1,2))/(xy(2,1)-xy(1,1));
                ht_angle = ht_angle + angle;
                nline = nline + 1;
            end                                        
        end
        if nline < 1
            return;
        else
            ht_angle = ht_angle / nline;
            ht_agtan = ht_angle;
        end
    end
    end
end

%%
function [newim, shift] = adjustslopeim(im,ht_agtan,buffdist)

newim = nan; shift = 0; 
    ycen = ceil(size(im,1)/2);
    hfwin = floor(size(im,2)/2);

    x = -hfwin:hfwin;
    y = round(x * ht_agtan); 

    x = x + ceil(size(im,2)/2);
    y = y + ycen;

    if ~mod(size(im,2),2)
        x(1) = [];
        y(1) = [];
    end
    
    idx = find(y <= 0 | y > size(im,1));
    x(idx) = [];
    y(idx) = []; 
    
    nbuff = buffdist*2 + 1;
    if abs(ht_agtan) <= 1
    
        xx = repmat(x,nbuff,1);
        yy = zeros(size(xx));

        for i = -buffdist: buffdist
            yy(buffdist + 1 + i,:) = y + i;
        end
    else
        yy = repmat(y,nbuff,1);
        xx = zeros(size(x));
        for i = -buffdist: buffdist
            xx(buffdist + 1 + i,:) = x + i;
        end
    end

        xx = reshape(xx,[size(xx,1)*size(xx,2),1]);
        yy = reshape(yy,[size(yy,1)*size(yy,2),1]);
        
        idx = find(xx <=0 | xx > size(im,2) | yy <=0 | yy > size(im,1));
        if ~isempty(idx), xx(idx) = []; ...
        yy(idx) = []; end
        
        indices = sub2ind(size(im),yy,xx);
    newim = zeros(size(im));
    newim(indices) = im(indices); 
end