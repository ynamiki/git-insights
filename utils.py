import datetime

def round_to_month(timestamp):
    """Round the given timestamp to the month.
    """
    dt = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    return dt.strftime('%Y-%m')

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
