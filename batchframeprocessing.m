% function batchframeprocessing(datalist)
% [nums,inlist] = loadfilelist(datalist);
% for s = 1:length(nums)
%     segments = inlist(s,:);
%     filelist = cell(nums(s),1);
%     for j = 1:nums(s)
%         fname = segments{j};
%         filelist{j} = ['LAYERS-',fname];
%         processframe_rev(fname,filelist{j});
%     end
% end
function batchframeprocessing(datalist)
    [nums, inlist] = loadfilelist(datalist);
    for s = 1:length(nums)
        segments = inlist(s,:);
        filelist = cell(nums(s),1);
        for j = 1:nums(s)
            fname = segments{j};
            filelist{j} = ['LAYERS-', fname];
            try
                processframe_rev(fname, filelist{j});
            catch ME
                fprintf('An error occurred with file: %s\n', fname);
                fprintf('Error message: %s\n', ME.message);
                % Optionally, you can handle the error or log it here.
                % Continue to the next iteration.
            end
        end
    end
end
