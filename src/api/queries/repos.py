from typing import List
from src.api.client import BaseGitHubClient

def get_graph_repos_stars(client: BaseGitHubClient, count_type: str, owner_affiliation: List[str], username: str, cursor: str = None) -> int:
    client.increment_query_count('graph_repos_stars')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                totalCount
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            stargazers {
                                totalCount
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': username, 'cursor': cursor}
    request = client.simple_request('graph_repos_stars', query, variables)
    data = request.json()['data']['user']['repositories']
    
    if count_type == 'repos':
        return data['totalCount']
    elif count_type == 'stars':
        return sum(node['node']['stargazers']['totalCount'] for node in data['edges'])
    return 0

def fetch_loc_query(client: BaseGitHubClient, owner_affiliation: List[str], username: str, cursor: str = None, edges: List = None) -> List:
    if edges is None:
        edges = []
    client.increment_query_count('loc_query')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 60, after: $cursor, ownerAffiliations: $owner_affiliation) {
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            defaultBranchRef {
                                target {
                                    ... on Commit {
                                        history {
                                            totalCount
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': username, 'cursor': cursor}
    request = client.simple_request('loc_query', query, variables)
    data = request.json()['data']['user']['repositories']
    
    edges.extend(data['edges'])
    if data['pageInfo']['hasNextPage']:
        return fetch_loc_query(client, owner_affiliation, username, data['pageInfo']['endCursor'], edges)
    
    return edges
