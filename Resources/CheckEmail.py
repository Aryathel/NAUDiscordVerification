import re  # Python Regex library
import dns.resolver  # Used to confirm that an email domain exists.

def check_email(email):
    # Simple Regex for syntax checking
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

    # Email syntax check
    match = re.match(regex, email)
    if match == None:
        return False

    try:
        # Get domain for DNS lookup
        splitAddress = email.split('@')
        domain = str(splitAddress[-1])

        # MX record lookup
        records = dns.resolver.query(domain, 'MX')
        mxRecord = records[0].exchange
        return True
    except:
        return False
