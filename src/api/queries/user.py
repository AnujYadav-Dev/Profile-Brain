from src.api.client import BaseGitHubClient

def get_user_info(client: BaseGitHubClient, username: str) -> tuple:
    client.increment_query_count('user_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            id
            createdAt
        }
    }'''
    request = client.simple_request('user_getter', query, {'login': username})
    data = request.json()['data']['user']
    client.owner_id = data['id']
    return {'id': data['id']}, data['createdAt']

def get_followers(client: BaseGitHubClient, username: str) -> int:
    client.increment_query_count('follower_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            followers {
                totalCount
            }
        }
    }'''
    request = client.simple_request('follower_getter', query, {'login': username})
    return int(request.json()['data']['user']['followers']['totalCount'])
