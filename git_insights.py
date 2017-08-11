import argparse
import collections
import datetime
import json
import operator

import git
import jinja2

import utils

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, git.objects.util.Actor):
            return obj.name + ' <' + obj.email + '>'
        return json.JSONEncoder.default(self, obj)

parser = argparse.ArgumentParser(
    description='Make reports from Git repositories.')
parser.add_argument(
    'repositories', metavar='repo', nargs='+',
    help='Git repositories')
args = parser.parse_args()

num_commits = 0
commits_by_author = collections.defaultdict(int)
commits_by_domain = collections.defaultdict(int)
commits_by_month = collections.defaultdict(int)

for r in args.repositories:
    repo = git.Repo(r)

    for commit in repo.iter_commits():
        # Skip a merge commit
        if len(commit.parents) > 1:
            continue

        num_commits += 1

        author = commit.author
        commits_by_author[author] += 1

        domain = utils.get_domain(author.email)
        if domain:
            commits_by_domain[domain] += 1
        
        commits_by_month[utils.round_to_month(commit.authored_date)] += 1

sorted_commits_by_author = sorted(
    commits_by_author.items(),
    key=operator.itemgetter(1), reverse=True)
sorted_commits_by_domain = sorted(
    commits_by_domain.items(),
    key=operator.itemgetter(1), reverse=True)
sorted_commits_by_month = sorted(
    commits_by_month.items(),
    key=operator.itemgetter(0))

top_n = 10
render_context = {
    'repositories': args.repositories,
    'top_n': top_n,
    'num_commits': num_commits,
    'num_authors': len(sorted_commits_by_author),
    'num_domains': len(sorted_commits_by_domain),
    'commits_by_month': sorted_commits_by_month,
    'commits_by_author': sorted_commits_by_author[:top_n],
    'commits_by_domain': sorted_commits_by_domain[:top_n],
}
env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
template = env.get_template('template.html')
print(template.render(render_context))
