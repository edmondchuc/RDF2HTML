import rdflib
from markdown2 import Markdown

import re



def extract_property_name_from_uri(s):
    """
    Extract the property name of a URI.

    :param s: A URI.
    :type s: str
    :return: The property name, where each word is separated by whitespace and set to lowercase.
    :rtype: str
    """
    property_name = str(s)  # cast to str
    # split on '#' if it exists, then on '/' and grab the last token
    property_name = property_name.split('#')[-1].split('/')[-1]

    # split the property_name if it is in camelCase or PascalCase
    full_name = []
    previous = 0
    for i, letter in enumerate(property_name):
        if letter.isupper():
            full_name.append(property_name[previous:i].lower())
            previous = i
    full_name.append(property_name[previous:].lower())

    property_name = ' '.join(full_name)
    return property_name


def make_title(s):
    """
    Make the string a title (actually, we shouldn't rely on this)

    :param s:
    :return:
    """
    s = s.split(' ')
    formatted = []
    for word in s:
        formatted.append(word[0].upper() + word[1:])
    s = ' '.join(formatted)
    return s


def is_email(email):
    """
    Check if the email is a valid email.

    This is done by matching it to a static regular expression pattern.

    :param email: The email to be tested.
    :return: True if the email matches the static regular expression, else false.
    :rtype: bool
    """
    pattern = r"[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    return True if re.search(pattern, email) is not None else False


def is_url(url):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return True if re.search(pattern, url) is not None else False


def is_literal(s):
    markdowner = Markdown()
    return markdowner.convert(s)


# NOT USED
def serialize_data(s):
    if isinstance(s, rdflib.Literal):
        markdowner = Markdown()
        return markdowner.convert(s)
    elif isinstance(s, rdflib.URIRef):
        # check if it's a URI or an email
        if is_email(s):
            s = f'<a href="mailto:{s}">{s}</a>'
        elif is_url(s):
            s = f'<a href="{s}">{s}</a>'
    return s


s = serialize_data