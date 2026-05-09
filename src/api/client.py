import requests
from typing import Dict

from src.core.config import Config

class BaseGitHubClient:
    def __init__(self, config: Config):
        self.config = config
        self.query_count: Dict[str, int] = {
            'user_getter': 0, 
            'follower_getter': 0, 
            'graph_repos_stars': 0, 
            'recursive_loc': 0, 
            'graph_commits': 0, 
            'loc_query': 0
        }
        self.owner_id = None

    def increment_query_count(self, funct_id: str):
        self.query_count[funct_id] = self.query_count.get(funct_id, 0) + 1

    def simple_request(self, func_name: str, query: str, variables: dict) -> requests.Response:
        request = requests.post(
            'https://api.github.com/graphql', 
            json={'query': query, 'variables': variables}, 
            headers=self.config.headers
        )
        if request.status_code == 200:
            return request
        raise Exception(f"{func_name} has failed with a {request.status_code} {request.text} {self.query_count}")
