import os
import shutil
from lxml import etree

from src.core.config import logger, TEMPLATE_DIR
from src.core.models import GitHubStats
from src.render.svg_utils import justify_format

def svg_overwrite(filename: str, mode: str, stats: GitHubStats):
    if not os.path.exists(filename):
        template_file = os.path.join(TEMPLATE_DIR, f"{mode}.svg")
        if os.path.exists(template_file):
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            shutil.copy(template_file, filename)
            logger.info("Copied default template %s to %s", template_file, filename)
        else:
            logger.error("Template SVG file not found: '%s'. Also could not find default template at '%s'.", filename, template_file)
            return

    try:
        tree = etree.parse(filename)
    except OSError:
        logger.error("Failed to parse SVG file: '%s'. Ensure the file is a valid XML/SVG.", filename)
        return
        
    root = tree.getroot()
    justify_format(root, 'age_data', stats.age_data, 49)
    justify_format(root, 'commit_data', stats.commit_count, 22)
    justify_format(root, 'star_data', stats.star_count, 14)
    justify_format(root, 'repo_data', stats.repo_count, 6)
    justify_format(root, 'contrib_data', stats.contrib_repo_count)
    justify_format(root, 'follower_data', stats.follower_count, 10)
    justify_format(root, 'loc_data', stats.loc_total, 9)
    justify_format(root, 'loc_add', stats.loc_added)
    justify_format(root, 'loc_del', stats.loc_deleted, 7)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
