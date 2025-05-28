from NDH_Tools.polarstereo_fwd import polarstereo_fwd
from NDH_Tools.distance_vector import distance_vector
from NDH_Tools.elevation_shift import elevation_shift
from scipy.interpolate import CubicSpline 
import numpy as np
import scipy

def load_and_process_radargram(file_name, layer_dir, radar_dir):
    layer_fn = layer_dir+file_name
    radar_fn = radar_dir+file_name

    layer_data = scipy.io.loadmat(layer_fn)
    radar_data = scipy.io.loadmat(radar_fn)

    xy = polarstereo_fwd(radar_data['Latitude'][0],radar_data['Longitude'][0])
    distance = distance_vector(xy['x'],xy['y'])
    elevationdata = elevation_shift(radar_data['Data'],radar_data['Time'],radar_data['Surface'][0],radar_data['Elevation'][0],radar_data['Bottom'][0])

    lay = np.copy(layer_data['imlayer'])
    lay = np.vstack((lay, np.zeros((radar_data['Data'].shape[0] -lay.shape[0], lay.shape[1]))))
    elev_layerdepthdata = elevation_shift(lay,radar_data['Time'],radar_data['Surface'][0],radar_data['Elevation'][0],radar_data['Bottom'][0])

    ybottom = layer_data['ybottom']
    def check_overlapping_layers(lay, ybottom):
        ybottom_min = np.min(ybottom)
        overlapping_layers = np.unique(lay[ybottom_min, :])
        return overlapping_layers[overlapping_layers > 0]

    overlapping_layers = check_overlapping_layers(lay, ybottom)

    data = elev_layerdepthdata
    slice_labels = data['new_data']
    label_values = np.unique(slice_labels)[1:] 
    num_labels = len(label_values)
    splines = []
    domains = []

    for label_num in label_values:
        label_skeleton = (slice_labels[:,:] == label_num).astype(int)
            
        row, col = label_skeleton.shape
        col_check = np.arange(0, col, 10)

        x, y = [], []
        for c in col_check:
            for r in range(row):
                if label_skeleton[r,c] == 1:
                    if c in x: continue 
                    x.append(c) 
                    y.append(r) 

        # create the cubic spline for the label
        if(len(x) > 1 and len(y) > 1):
            splines.append(CubicSpline(x,y))
            domains.append(x)
        x = []
        y = []
    exclusion_margin = 700
    exclusion_zone = range(np.min(ybottom), np.min(ybottom) + exclusion_margin)

    ground_truth_mask = np.zeros_like(elevationdata['new_data'])

    for i in range(len(domains)):
        if i not in overlapping_layers:
            x_dense = np.linspace(min(domains[i]), max(domains[i]), num=len(domains[i])*10)  
            y_dense = splines[i](x_dense)

            for x, y in zip(x_dense.astype(int), y_dense.astype(int)):
                if 0 <= x < ground_truth_mask.shape[1] and 0 <= y < ground_truth_mask.shape[0]:
                    if y not in exclusion_zone:
                        ground_truth_mask[y, x] = 1

    return radar_data, ground_truth_mask, elevationdata