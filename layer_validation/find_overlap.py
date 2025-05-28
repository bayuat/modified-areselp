import numpy as np

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

def find_overlapping_intervals(log_gps_time1, log_gps_time2, tolerance=1e-10):
    overlap_intervals1 = []
    overlap_intervals2 = []

    i, j = 0, 0
    start_i, start_j = None, None

    while i < len(log_gps_time1) and j < len(log_gps_time2):
        if abs(log_gps_time1[i] - log_gps_time2[j]) < tolerance:
            if start_i is None:
                start_i, start_j = i, j
            i += 1
            j += 1
        else:
            if start_i is not None:
                overlap_intervals1.append((start_i, i - 1))
                overlap_intervals2.append((start_j, j - 1))
                start_i, start_j = None, None
            if log_gps_time1[i] < log_gps_time2[j]:
                i += 1
            else:
                j += 1

    if start_i is not None:
        overlap_intervals1.append((start_i, i - 1))
        overlap_intervals2.append((start_j, j - 1))

    return overlap_intervals1, overlap_intervals2

def adjust_overlapping_intervals(overlap_idx1, overlap_idx2):
    overlap_start1, overlap_end1 = overlap_idx1[0][0], overlap_idx1[-1][1]
    overlap_start2, overlap_end2 = overlap_idx2[0][0], overlap_idx2[-1][1]
    
    min_overlap = min(overlap_end1 - overlap_start1, overlap_end2 - overlap_start2)
    
    overlap_end1 = overlap_start1 + min_overlap
    overlap_end2 = overlap_start2 + min_overlap
    
    return [(overlap_start1, overlap_end1)], [(overlap_start2, overlap_end2)]