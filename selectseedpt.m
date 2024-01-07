function seedpt = selectseedpt(peakim)
a = peakim(peakim > 0); % only care about positive peaks
[x,y] = find(peakim > 0);
indices = sub2ind(size(peakim),x,y);
val = peakim(indices); 
seedpt = [val,x,y];
seedpt = flipud(sortrows(seedpt));

pd = fitdist(a,'lognormal');
thresh = exp(pd.mu + pd.sigma.^2 /2); %threshold to filter out seed pts

seedpt(seedpt(:,1) < thresh,:) = []; %change here
seedpt(:,1) = [];
end
