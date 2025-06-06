import matplotlib.pyplot as plt
import numpy as np
from NDH_Tools.loadmat import loadmat
from NDH_Tools.str_compare import str_compare
from NDH_Tools.polarstereo_fwd import polarstereo_fwd
from NDH_Tools.distance_vector import distance_vector
from NDH_Tools.find_nearest_xy import find_nearest_xy
from NDH_Tools.elevation_shift import elevation_shift
from NDH_Tools.find_nearest import find_nearest
from NDH_Tools.depth_shift import depth_shift

################################################################################################


def radar_load(fn,plot_flag=0,elevation1_or_depth2=1,alternative_data_opt=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function does the standard load, transformation, and plotting
    %     that is common in the CReSIS radar analysis workflow
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     fn -- the input filename or list of filenames to be read
    %     plot_flag -- 0 or 1, for whether or not you want a plot included, or 2 for the plotting code to be printed
    %     elevation1_or_depth2 -- there is a depth conversion that is built in, 1 if you want true elevation, 2 for depth in ice
    %                             0 will give you an empty object
    %     alternative_data_opt -- Some files (generated by Nick) contain more than one data type. This lets you switch them.
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     radar_data -- the simple product of loading the mat file (+ x and y coordinates and distance added)
    %     depth_data -- the depth or elevation product
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
  
     
    if isinstance(fn,list) == 0:
        fn = [fn]
        
    concat_list = ['Elevation','GPS_time','Latitude','Longitude','Surface','Bottom']
    
    ############## Here we loop through the radar data and concatenate the files
    for fn_ind,fn_temp in enumerate(fn):
        
        if fn_ind == 0:
            radar_data = loadmat(fn_temp);
            
            ############# Here we exit if the file didn't load properly
            if len(radar_data.keys()) == 0:
                depth_data = radar_data
                return radar_data,depth_data
            
            data2_exist = str_compare(radar_data.keys(),'Data2')
            if len(data2_exist[0]) > 0:
                alternative_data_exist = 1
            else:
                alternative_data_exist = 0
            
            xy = polarstereo_fwd(radar_data['Latitude'],radar_data['Longitude'])
            distance = distance_vector(xy['x'],xy['y'])
            radar_data['x'] = xy['x']
            radar_data['y'] = xy['y']
            radar_data['distance'] = distance
            radar_data['im_end'] = [0,len(distance)]
            radar_data['orig_ind'] = np.arange(0,len(distance))
            radar_data['filename'] = [fn_temp.split('/')[-1]]
            
        if fn_ind > 0:
            
            radar_data_temp = loadmat(fn_temp)            
            
            xy_temp = polarstereo_fwd(radar_data_temp['Latitude'],radar_data_temp['Longitude'])
            
            ########## Here we deal with potentially overlapping frames
            comp_dists = find_nearest_xy([xy_temp['x'],xy_temp['y']],[radar_data['x'][-1],radar_data['y'][-1]])
            if comp_dists['index'] != 0:                
                for cut_key in concat_list:
                    radar_data_temp[cut_key] = radar_data_temp[cut_key][comp_dists['index'][0]:]
                radar_data_temp['Data'] = radar_data_temp['Data'][:,comp_dists['index'][0]:]
                xy_temp['x'] = xy_temp['x'][comp_dists['index'][0]:]
                xy_temp['y'] = xy_temp['y'][comp_dists['index'][0]:]
            
            inc_dist = comp_dists['distance'][0]
            distance = distance_vector(xy_temp['x'],xy_temp['y'])
        
            if inc_dist < 0.01:
                inc_dist = 0.01
                
            ########## Here we do the data concatenation
            radar_data['x'] = np.concatenate([radar_data['x'],xy_temp['x']])
            radar_data['y'] = np.concatenate([radar_data['y'],xy_temp['y']])
            radar_data['distance'] = np.concatenate([radar_data['distance'],distance+np.max(radar_data['distance'])+inc_dist])
            radar_data['im_end'].append(len(radar_data['distance']))
            radar_data['orig_ind'] = np.concatenate([radar_data['orig_ind'],np.arange(comp_dists['index'][0],len(distance))])
            radar_data['filename'].append(fn_temp.split('/')[-1])
            
            radar_data['Data'] = np.concatenate([radar_data['Data'],radar_data_temp['Data']],axis=1)
            
            ############# Here we handle files with potentially alternative datatytpes:
            if alternative_data_exist == 1:
                radar_data['Data2'] = np.concatenate([radar_data['Data2'],radar_data_temp['Data2']],axis=1)
            
            for concat_keys in concat_list:
                radar_data[concat_keys] = np.concatenate([radar_data[concat_keys],radar_data_temp[concat_keys]])
            
    ############# Here we do the depth or elevation shift
    if elevation1_or_depth2 == 0:
        depth_data = 'No depth data requested'    
        
    elif elevation1_or_depth2 == 1:
        if np.all([alternative_data_exist == 1, alternative_data_opt == 1]):
            print('Loading Alternative Data Set')
            depth_data = elevation_shift(radar_data['Data2'],radar_data['Time'],radar_data['Surface'],radar_data['Elevation'],radar_data['Bottom'])
        else:
            depth_data = elevation_shift(radar_data['Data'],radar_data['Time'],radar_data['Surface'],radar_data['Elevation'],radar_data['Bottom'])
    elif elevation1_or_depth2 == 2:
        if np.all([alternative_data_exist == 1, alternative_data_opt == 1]):
            print('Loading Alternative Data Set')
            depth_data = depth_shift(radar_data['Data2'],radar_data['Time'],radar_data['Surface'],radar_data['Elevation'],radar_data['Bottom'])
        else:
            depth_data = depth_shift(radar_data['Data'],radar_data['Time'],radar_data['Surface'],radar_data['Elevation'],radar_data['Bottom'])
            

    ############# Here we either plot the data or deliver a plot string for future use
    if plot_flag == 1:

        if elevation1_or_depth2 == 0:
            bot_inds = find_nearest(radar_data['Time'],radar_data['Bottom'])
            bot_ind = np.nanmax(bot_inds['index'])+100

            fig = plt.figure(figsize=(15,7))
            imdata = plt.imshow(10*np.log10(radar_data['Data'][:bot_ind,:]),
                                origin='lower',aspect='auto',cmap='gray_r')
            ax = plt.gca()        
            ax.invert_yaxis()

        else:
            fig = plt.figure(figsize=(15,7))
            imdata = plt.imshow(10*np.log10(depth_data['new_data']),
                                extent=[radar_data['distance'][0]/1000,radar_data['distance'][-1]/1000,
                                        depth_data['depth_axis'][0],depth_data['depth_axis'][-1]],
                                origin='lower',aspect='auto',cmap='gray_r')
            
            if elevation1_or_depth2 == 2:
                plt.ylabel('Depth (m)')
            elif elevation1_or_depth2 == 1:
                plt.ylabel('Elevation w.r.t WGS84 (m)')
            plt.xlabel('Distance (km)')
            
            cbar = plt.colorbar(imdata)
            ax = plt.gca()
            ax.invert_yaxis()

    ############## This delivers the plot string of interest
    elif plot_flag == 2:

        if elevation1_or_depth2 == 0:
            print('''
fig = plt.figure(figsize=(15,7))
imdata = plt.imshow(10*np.log10(radar_data['Data']),
                    origin='lower',aspect='auto',cmap='gray_r')
                    
cbar = plt.colorbar(imdata)
ax = plt.gca() 
ax.invert_yaxis()
            ''')            
        else:
            print('''
fig = plt.figure(figsize=(15,7))
imdata = plt.imshow(10*np.log10(depth_data['new_data']),
                    extent=[radar_data['distance'][0]/1000,radar_data['distance'][-1]/1000,
                            depth_data['depth_axis'][0],depth_data['depth_axis'][-1]],
                    origin='lower',aspect='auto',cmap='gray_r')    
                    
cbar = plt.colorbar(imdata)
ax = plt.gca()
ax.invert_yaxis()
            ''')

    return radar_data,depth_data