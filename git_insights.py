import argparse
import collections
import datetime
import json
import operator
import sys

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
earliest_authored_date = sys.maxsize
commits_by_author = collections.defaultdict(int)
commits_by_domain = collections.defaultdict(int)
commits_by_month = collections.defaultdict(int)
first_commit_in_month = collections.OrderedDict()

for r in args.repositories:
    repo = git.Repo(r)

    first_commit_in_month[r] = {}
    repo.git.checkout('origin/HEAD')
    for commit in repo.iter_commits():
        # Skip a merge commit
        if len(commit.parents) > 1:
            continue

        num_commits += 1
        earliest_authored_date = min(commit.authored_date, earliest_authored_date)

        author = commit.author
        commits_by_author[author] += 1

        domain = utils.get_domain(author.email)
        if domain:
            commits_by_domain[domain] += 1
        
        authored_month_str = utils.round_to_month_str(commit.authored_date)
        commits_by_month[authored_month_str] += 1
        first_commit_in_month[r][authored_month_str] = commit.hexsha

sorted_commits_by_author = sorted(
    commits_by_author.items(),
    key=operator.itemgetter(1), reverse=True)
sorted_commits_by_domain = sorted(
    commits_by_domain.items(),
    key=operator.itemgetter(1), reverse=True)

date_labels = utils.month_range_str(
    datetime.date.fromtimestamp(earliest_authored_date))

sorted_commits_by_month = []
for d in date_labels:
    sorted_commits_by_month.append(commits_by_month[d])

# Create lines by month
lines_by_month = collections.OrderedDict()
for r in first_commit_in_month.keys():
    repo = git.Repo(r)
    lines_by_month[r] = []
    prev_lines = 0
    for d in date_labels:
        if d in first_commit_in_month[r]:
            repo.git.checkout(first_commit_in_month[r][d])
            lines = utils.count_lines(r)
        else:
            lines = prev_lines
        lines_by_month[r].append(lines)
        prev_lines = lines

top_n = 10
render_context = {
    'ctime': datetime.datetime.today().isoformat(' '),
    'repositories': args.repositories,
    'top_n': top_n,
    'num_commits': num_commits,
    'num_authors': len(sorted_commits_by_author),
    'num_domains': len(sorted_commits_by_domain),
    'date_labels': date_labels,
    'commits_by_month': sorted_commits_by_month,
    'commits_by_author': sorted_commits_by_author[:top_n],
    'commits_by_domain': sorted_commits_by_domain[:top_n],
    'lines_by_month': lines_by_month,
}
env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
template = env.get_template('template.html')
print(template.render(render_context))
