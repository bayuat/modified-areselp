import numpy as np

def find_layers(mask):
    layers = []
    visited = np.zeros_like(mask, dtype=bool)
    
    for col in range(mask.shape[1]):
        layer_indices = np.where(mask[:, col] == 1)[0]
        for row in layer_indices:
            if not visited[row, col]:
                layer = follow_layer(mask, visited, row, col)
                if layer:
                    layers.append(layer)
    return layers

def follow_layer(mask, visited, row, col):
    layer = []
    stack = [(row, col)]
    
    while stack:
        r, c = stack.pop()
        if visited[r, c]:
            continue
        visited[r, c] = True
        layer.append((r, c))
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < mask.shape[0] and 0 <= cc < mask.shape[1] and mask[rr, cc] == 1 and not visited[rr, cc]:
                    stack.append((rr, cc))
    
    if len(layer) > 1:
        return layer
    return None