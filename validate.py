import re

def is_valid_url(url):
    regex = re.compile(
        r'^https?://' # scheme
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain
        r'localhost|' # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # IP address
        r'(?::\d+)?' # port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(regex.match(url))

def is_valid_shortname(shortname):
    regex = re.compile(
        r'^[a-zA-Z0-9_-]{3,50}$'
    )
    return bool(regex.match(shortname))