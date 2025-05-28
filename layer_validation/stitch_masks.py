import numpy as np

def apply_manual_vertical_shift(mask, shift):
    return np.roll(mask, shift, axis=0)

def stitch_masks(mask1, mask2, overlap_idx1, overlap_idx2, vertical_shift):    
    mask1_height, mask1_width = mask1.shape
    mask2_height, mask2_width = mask2.shape
    
    aligned_mask2 = apply_manual_vertical_shift(mask2, vertical_shift)
    
    overlap_start1 = overlap_idx1[0][0]
    overlap_end1 = overlap_idx1[-1][1] + 1
    overlap_start2 = overlap_idx2[0][0]
    overlap_end2 = overlap_idx2[-1][1] + 1
    
    overlap_width1 = overlap_end1 - overlap_start1
    overlap_width2 = overlap_end2 - overlap_start2 
    
    if overlap_width1 != overlap_width2:
        raise ValueError("Overlap widths do not match between the two masks")
    
    overlap_width = overlap_width1
    
    stitched_height = max(mask1_height, mask2_height)
    stitched_width = mask1_width + mask2_width - overlap_width
    
    stitched_mask = np.zeros((stitched_height, stitched_width))
    
    stitched_mask[:mask1_height, :mask1_width] = mask1
    stitched_mask[:mask2_height, mask1_width - overlap_width:] = aligned_mask2
    
    return stitched_mask