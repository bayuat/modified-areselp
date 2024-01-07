function getfilelist(foldername)
fileList = dir(fullfile(foldername, '*.mat'));
fileList = {fileList.name};
fileList = strrep(fileList, '.mat', '');
[t]=table(transpose(fileList));
numvar=width(fileList);
newName=append('<< ',string(numvar));
t=renamevars(t,'Var1',newName);
%fileListtable(1,:)={'<<'};
tnew={'>>'};
%t(end,end)={'>>'};
t=[t;tnew];
writetable(t,'./IHARP/ARESELP/process_multiframe.txt');
end
