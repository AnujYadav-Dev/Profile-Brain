from dataclasses import dataclass

@dataclass
class GitHubStats:
    account_id: str = ''
    account_date: str = ''
    age_data: str = "Not specified"
    commit_count: int = 0
    star_count: int = 0
    repo_count: int = 0
    contrib_repo_count: int = 0
    follower_count: int = 0
    loc_added: int = 0
    loc_deleted: int = 0
    loc_total: int = 0

@dataclass
class CacheEntry:
    repo_hash: str
    total_commits: int
    my_commits: int
    loc_added: int
    loc_deleted: int

    def to_string(self) -> str:
        return f"{self.repo_hash} {self.total_commits} {self.my_commits} {self.loc_added} {self.loc_deleted}\n"

    @classmethod
    def from_string(cls, line: str) -> 'CacheEntry':
        parts = line.split()
        if len(parts) >= 5:
            return cls(parts[0], int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
        return cls(parts[0], 0, 0, 0, 0)
