import datetime
import logging
import shlex
import subprocess

import dateutil.relativedelta

logger = logging.getLogger(__name__)

def round_to_month_str(timestamp):
    """Round the given timestamp to the month.
    """
    dt = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    return dt.strftime('%Y-%m')

def month_range_str(start, stop=datetime.date.today()):
    list = []

    d = start.replace(day=1)
    while d < stop:
        list.append(d.strftime('%Y-%m'))
        d = d + dateutil.relativedelta.relativedelta(months=1)

    return list

def get_domain(email):
    """Get a domain from the e-mail address.
    """
    split = email.split('@')
    if len(split) < 2:
        return ''

    domain = split[1]
    # FIXME Quick hack: foo.example.com -> example.com
    if (domain != 'users.noreply.github.com'
            and domain.endswith('.com')):
        split = domain.rsplit('.', 3)
        if len(split) > 2:
            domain = '.'.join(split[-2:])
    
    return domain

def count_lines(filename):
    # FIXME Implement natively
    command = ('find "{}" '
        + '-path "*/.git" -prune '
        + '-o -path "*/vendor" -prune '
        + '-o -type f -print0 '
        + '| xargs -0 wc -l').format(shlex.quote(filename))
    logger.debug('executing: %s', command)
    proc = subprocess.run(
        command, stdout=subprocess.PIPE, shell=True, encoding='utf-8')
    out = proc.stdout
    logger.debug('output: %s', out)
    if not out:
        return 0
    return int(out.rsplit('\n', 2)[-2].split()[0])