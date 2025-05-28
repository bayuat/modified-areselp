def generate_data_files(base_name, start_idx, end_idx):
    data_files = []
    for i in range(start_idx, end_idx + 1):
        file_name = f"{base_name}{i:03d}.mat"
        data_files.append(file_name)
    return data_files