from NDH_Tools.loadmat import loadmat
from NDH_Tools.radar_load import radar_load
import numpy as np
import scipy


def load_and_process_radargram(file_name, layer_dir, radar_dir):
    layer_fn = layer_dir + file_name
    radar_fn = radar_dir + file_name

    groundtruth = loadmat(layer_fn)
    groundtruth_dists = groundtruth['layer_info'][()][2]
    groundtruth_layers = groundtruth['layer_info'][()][5].T
    radar_data, depth_data = radar_load(radar_fn, 0, 1)

    ground_truth_mask_nick = np.zeros_like(depth_data['new_data'])

    for i, layer in enumerate(groundtruth_layers):
        for idx, depth in enumerate(layer):
            if not np.isnan(depth):
                depth_idx = np.argmin(np.abs(depth_data['depth_axis'] - depth))
                dist_idx = np.argmin(np.abs(radar_data['distance'] - groundtruth_dists[idx]))
                if 0 <= depth_idx < ground_truth_mask_nick.shape[0] and 0 <= dist_idx < ground_truth_mask_nick.shape[1]:
                    ground_truth_mask_nick[depth_idx, dist_idx] = 1
    return radar_data, ground_truth_mask_nick, depth_data

def load_log_gps_time(file_path):
    radar_data = scipy.io.loadmat(file_path)
    gps_time = radar_data['GPS_time'][0]
    log_gps_time = np.log(gps_time)
    return log_gps_time

def load_lat_lon(file_path):    
    radar_data = scipy.io.loadmat(file_path)
    latitude = radar_data['Latitude'][0]  
    longitude = radar_data['Longitude'][0]  
    return latitude, longitude

def find_overlapping_columns(lat1, lon1, lat2, lon2, tolerance=0.00001):    
    lat_lon_set1 = set((round(lat, 3), round(lon, 3)) for lat, lon in zip(lat1, lon1))
    lat_lon_set2 = set((round(lat, 3), round(lon, 3)) for lat, lon in zip(lat2, lon2))    
    common_lat_lon = {(lat, lon) for lat, lon in lat_lon_set1 if any(abs(lat - x[0]) < tolerance and abs(lon - x[1]) < tolerance for x in lat_lon_set2)}
    
    if not common_lat_lon:
        return (None, None), (None, None)   
    
    common_indices1 = [i for i, (lat, lon) in enumerate(zip(lat1, lon1)) if (round(lat, 3), round(lon, 3)) in common_lat_lon]
    common_indices2 = [i for i, (lat, lon) in enumerate(zip(lat2, lon2)) if (round(lat, 3), round(lon, 3)) in common_lat_lon]
    
    start_idx1 = min(common_indices1)
    end_idx1 = max(common_indices1)
    start_idx2 = min(common_indices2)
    end_idx2 = max(common_indices2)
    
    return (start_idx1, end_idx1), (start_idx2, end_idx2)