import os
from typing import Tuple

def load_archive_data(cache_dir: str) -> Tuple[int, int, int, int, int]:
    archive_path = os.path.join(cache_dir, 'repository_archive.txt')
    if not os.path.exists(archive_path):
        return 0, 0, 0, 0, 0
        
    with open(archive_path, 'r') as f:
        data = f.readlines()
        
    old_data = data
    data = data[7:len(data)-3]
    added_loc, deleted_loc, added_commits = 0, 0, 0
    contributed_repos = len(data)
    
    for line in data:
        parts = line.split()
        if len(parts) >= 5:
            added_loc += int(parts[3])
            deleted_loc += int(parts[4])
            if parts[2].isdigit():
                added_commits += int(parts[2])
                
    added_commits += int(old_data[-1].split()[4][:-1])
    return added_loc, deleted_loc, added_loc - deleted_loc, added_commits, contributed_repos
