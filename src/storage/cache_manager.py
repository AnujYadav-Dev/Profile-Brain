import os
import hashlib
from typing import List, Tuple

from src.core.config import Config, logger
from src.core.models import CacheEntry
from src.api.client import BaseGitHubClient
from src.api.queries.commits import fetch_recursive_loc

class CacheManager:
    def __init__(self, config: Config, client: BaseGitHubClient):
        self.config = config
        self.client = client
        self.filename = os.path.join(self.config.cache_dir, hashlib.sha256(self.config.user_name.encode('utf-8')).hexdigest() + '.txt')
        self.comment_size = 7

    def _read_cache(self) -> List[str]:
        try:
            with open(self.filename, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            return []

    def _write_cache(self, comment_lines: List[str], entries: List[CacheEntry]):
        os.makedirs(self.config.cache_dir, exist_ok=True)
        with open(self.filename, 'w') as f:
            f.writelines(comment_lines)
            for entry in entries:
                f.write(entry.to_string())

    def force_close_file(self, comment_lines: List[str], entries: List[CacheEntry]):
        self._write_cache(comment_lines, entries)
        logger.error(f'There was an error while writing to the cache file. The file, {self.filename} has had the partial data saved and closed.')

    def flush_cache(self, edges: List[dict]):
        data = self._read_cache()
        comment_lines = data[:self.comment_size]
        if not comment_lines and self.comment_size > 0:
            comment_lines = ['This line is a comment block. Write whatever you want here.\n'] * self.comment_size
        
        entries = [CacheEntry(hashlib.sha256(node['node']['nameWithOwner'].encode('utf-8')).hexdigest(), 0, 0, 0, 0) for node in edges]
        self._write_cache(comment_lines, entries)

    def build_cache(self, edges: List[dict], force_cache: bool = False) -> tuple:
        cached = True
        data = self._read_cache()
        
        if not data:
            self.flush_cache(edges)
            data = self._read_cache()
            
        if len(data) - self.comment_size != len(edges) or force_cache:
            cached = False
            self.flush_cache(edges)
            data = self._read_cache()
            
        comment_lines = data[:self.comment_size]
        data_lines = data[self.comment_size:]
        
        entries = [CacheEntry.from_string(line) for line in data_lines]
        loc_add = 0
        loc_del = 0
        
        try:
            for index, edge in enumerate(edges):
                node = edge['node']
                name_with_owner = node['nameWithOwner']
                repo_hash = hashlib.sha256(name_with_owner.encode('utf-8')).hexdigest()
                
                if entries[index].repo_hash == repo_hash:
                    try:
                        history_count = node['defaultBranchRef']['target']['history']['totalCount']
                    except TypeError:
                        history_count = 0
                        
                    if entries[index].total_commits != history_count and history_count > 0:
                        owner, repo_name = name_with_owner.split('/')
                        add_tot, del_tot, my_coms = fetch_recursive_loc(self.client, owner, repo_name)
                        entries[index] = CacheEntry(repo_hash, history_count, my_coms, add_tot, del_tot)
                    elif history_count == 0:
                        entries[index] = CacheEntry(repo_hash, 0, 0, 0, 0)
                
                loc_add += entries[index].loc_added
                loc_del += entries[index].loc_deleted
        except Exception as e:
            self.force_close_file(comment_lines, entries)
            raise e
            
        self._write_cache(comment_lines, entries)
        return loc_add, loc_del, loc_add - loc_del, cached

    def commit_counter(self) -> int:
        data = self._read_cache()
        data_lines = data[self.comment_size:]
        entries = [CacheEntry.from_string(line) for line in data_lines]
        return sum(entry.my_commits for entry in entries)
