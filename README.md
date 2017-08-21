# Git Insights

Generates a report of Git repositories, including:

* The number of commits per month
* Top contributors by author/domain
* The number of lines of code month-by-month

## Prerequisites

* Python 3.5 or later
* `/bin/sh`, `find`, `wc` commands

## Quick Start

```
$ pip3 install --require requirements.txt
$ python3 git_insights.py <repo>
```

Notes:

* Using a virtual environment (venv) is recommended to isolate an
  environment.
* The repository specified as an argument must be a local.
* The repository should be newly cloned; this program will checkout
  revisions to count lines.

# License Notice

This product depends on GitPython 2.1.5, which is available under the
"3-clause BSD" license. For details, see
https://github.com/gitpython-developers/GitPython/.

This product depends on Jinja 2.9.6, which is available under the
"3-clause BSD" license. For details, see http://jinja.pocoo.org/.

This product depends on dateutil 2.6.1, which is available under the
"3-clause BSD" license. For details, see
https://github.com/dateutil/dateutil/.

This product depends on Bootstrap 3.3.7, which is available under the
MIT license. For details, see http://getbootstrap.com/.

This product depends on jQuery 1.12.4, which is available under the MIT
license. For details, see http://jquery.com/.

This product depends on Chart.js 2.6.0, which is available under the MIT
license. For details, see http://www.chartjs.org/.
