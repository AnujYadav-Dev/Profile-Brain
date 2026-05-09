import datetime
import os

from src.core.config import get_config, logger
from src.core.models import GitHubStats
from src.core.utils import daily_readme, perf_counter, formatter

from src.api.client import BaseGitHubClient
from src.api.queries.user import get_user_info, get_followers
from src.api.queries.repos import get_graph_repos_stars, fetch_loc_query

from src.storage.cache_manager import CacheManager
from src.storage.archive import load_archive_data

from src.render.builder import svg_overwrite

class WorkflowOrchestrator:
    def __init__(self):
        self.config = get_config()
        self.github_client = BaseGitHubClient(self.config)
        self.cache_manager = CacheManager(self.config, self.github_client)
        self.stats = GitHubStats()
        self.total_time = 0.0
        
    def _fetch_user_data(self):
        (user_info, acc_date), user_time = perf_counter(get_user_info, self.github_client, self.config.user_name)
        self.stats.account_id = user_info['id']
        self.stats.account_date = acc_date
        self.total_time += user_time
        formatter('account data', user_time)
        
        if self.config.birth_date:
            birth_year, birth_month, birth_day = map(int, self.config.birth_date.split('-'))
            age_data, age_time = perf_counter(daily_readme, datetime.datetime(birth_year, birth_month, birth_day))
        else:
            age_data = "Not specified"
            age_time = 0.0
            
        self.stats.age_data = age_data
        self.total_time += age_time
        formatter('age calculation', age_time)
        
        follower_data, follower_time = perf_counter(get_followers, self.github_client, self.config.user_name)
        self.stats.follower_count = follower_data
        self.total_time += follower_time
        
    def _process_loc_and_cache(self):
        edges, loc_query_time = perf_counter(fetch_loc_query, self.github_client, ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'], self.config.user_name)
        loc_data, cache_time = perf_counter(self.cache_manager.build_cache, edges)
        
        self.stats.loc_added = loc_data[0]
        self.stats.loc_deleted = loc_data[1]
        self.stats.loc_total = loc_data[2]
        is_cached = loc_data[3]
        
        loc_time = loc_query_time + cache_time
        self.total_time += loc_time
        formatter('LOC (cached)', loc_time) if is_cached else formatter('LOC (no cache)', loc_time)
        
        commit_data, commit_time = perf_counter(self.cache_manager.commit_counter)
        self.stats.commit_count = commit_data
        self.total_time += commit_time

    def _fetch_repository_stats(self):
        star_data, star_time = perf_counter(get_graph_repos_stars, self.github_client, 'stars', ['OWNER'], self.config.user_name)
        self.stats.star_count = star_data
        self.total_time += star_time
        
        repo_data, repo_time = perf_counter(get_graph_repos_stars, self.github_client, 'repos', ['OWNER'], self.config.user_name)
        self.stats.repo_count = repo_data
        self.total_time += repo_time
        
        contrib_data, contrib_time = perf_counter(get_graph_repos_stars, self.github_client, 'repos', ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'], self.config.user_name)
        self.stats.contrib_repo_count = contrib_data
        self.total_time += contrib_time

    def _apply_archives(self):
        archive_path = os.path.join(self.config.cache_dir, 'repository_archive.txt')
        if os.path.exists(archive_path):
            archived_data = load_archive_data(self.config.cache_dir)
            self.stats.loc_added += archived_data[0]
            self.stats.loc_deleted += archived_data[1]
            self.stats.loc_total += archived_data[2]
            self.stats.commit_count += archived_data[3]
            self.stats.contrib_repo_count += archived_data[4]

    def _render_svg(self):
        svg_overwrite(self.config.dark_svg_path, 'dark_mode', self.stats)
        svg_overwrite(self.config.light_svg_path, 'light_mode', self.stats)

    def run(self):
        author_string = f"{self.config.user_name}, {datetime.datetime.now().year}"
        logger.info(f"Starting execution for {author_string}")
        logger.info('Calculation times:')
        
        self._fetch_user_data()
        self._process_loc_and_cache()
        self._fetch_repository_stats()
        self._apply_archives()
        self._render_svg()

        logger.info(f'Total function time: {self.total_time:.4f} s')
        
        total_calls = sum(self.github_client.query_count.values())
        logger.info(f'Total GitHub GraphQL API calls: {total_calls:3d}')
        for funct_name, count in self.github_client.query_count.items():
            logger.info('{:<28} {:>6}'.format('   ' + funct_name + ':', count))
