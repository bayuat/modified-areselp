from find_and_follow_layer import find_layers
import numpy as np

def calculate_continuous_layers(stitched_mask, num_masks, min_span):
    layers = find_layers(stitched_mask)
    max_width = stitched_mask.shape[1]
    
    continuous_layers_count = np.zeros(num_masks - 1)
    
    for layer in layers:
        columns = [c for r, c in layer]
        span = max(columns) - min(columns)
        
        for n in range(2, num_masks + 1):
            if span >= (min_span * (n - 1)):
                continuous_layers_count[n - 2] += 1
    
    return continuous_layers_count