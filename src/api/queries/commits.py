import requests
from src.api.client import BaseGitHubClient

def get_graph_commits(client: BaseGitHubClient, username: str, start_date: str, end_date: str) -> int:
    client.increment_query_count('graph_commits')
    query = '''
    query($start_date: DateTime!, $end_date: DateTime!, $login: String!) {
        user(login: $login) {
            contributionsCollection(from: $start_date, to: $end_date) {
                contributionCalendar {
                    totalContributions
                }
            }
        }
    }'''
    variables = {'start_date': start_date, 'end_date': end_date, 'login': username}
    request = client.simple_request('graph_commits', query, variables)
    return int(request.json()['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions'])

def fetch_recursive_loc(client: BaseGitHubClient, owner: str, repo_name: str, cursor: str = None, addition_total: int = 0, deletion_total: int = 0, my_commits: int = 0) -> tuple:
    client.increment_query_count('recursive_loc')
    query = '''
    query ($repo_name: String!, $owner: String!, $cursor: String) {
        repository(name: $repo_name, owner: $owner) {
            defaultBranchRef {
                target {
                    ... on Commit {
                        history(first: 100, after: $cursor) {
                            totalCount
                            edges {
                                node {
                                    author {
                                        user {
                                            id
                                        }
                                    }
                                    deletions
                                    additions
                                }
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }
        }
    }'''
    variables = {'repo_name': repo_name, 'owner': owner, 'cursor': cursor}
    
    request = requests.post(
        'https://api.github.com/graphql', 
        json={'query': query, 'variables': variables}, 
        headers=client.config.headers
    )
    
    if request.status_code == 200:
        repo_data = request.json().get('data', {}).get('repository', {})
        if not repo_data or not repo_data.get('defaultBranchRef'):
            return addition_total, deletion_total, my_commits
        
        history = repo_data['defaultBranchRef']['target']['history']
        for node in history['edges']:
            author_user = node['node']['author']['user']
            if author_user and author_user.get('id') == client.owner_id:
                my_commits += 1
                addition_total += node['node']['additions']
                deletion_total += node['node']['deletions']

        if history['edges'] == [] or not history['pageInfo']['hasNextPage']:
            return addition_total, deletion_total, my_commits
        return fetch_recursive_loc(client, owner, repo_name, history['pageInfo']['endCursor'], addition_total, deletion_total, my_commits)
        
    elif request.status_code == 403:
        raise Exception("Too many requests in a short amount of time! You've hit the non-documented anti-abuse limit!")
        
    raise Exception(f"recursive_loc() has failed with a {request.status_code} {request.text} {client.query_count}")
