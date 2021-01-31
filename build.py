import yaml
import re
import requests
from jinja2 import Template


def valid_url_format(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def valid_url_response(url):
    response = requests.get(url=url)
    response.raise_for_status()
    return (response.status_code == 200)


def apply_rules(item):
    print(f'-> Testing {item["name"]}')
    r = []
    if not valid_url_format(item['url']):
        r.append(f'Invalid url format: {item["url"]}')
    if not valid_url_response(item['url']):
        r.append(f'Invalid url response: {item["url"]}')

    if len(r) > 0:
        return r


AWESOME_VENDORS_SOURCE = 'awesome_vendors.yml'
README_TEMPLATE = 'README.template.md'
README = 'README.md'

sorted_dict = {}
error_list = []

with open(AWESOME_VENDORS_SOURCE, 'r') as file:
    yml_dict = yaml.safe_load(file)

for loc in sorted(yml_dict.keys()):
    [error_list.append({'section': loc, 'issue': r})
     for vendor in yml_dict[loc] if (r := apply_rules(vendor))]
    sorted_dict[loc] = sorted(yml_dict[loc], key=lambda k: k['name'])

if len(error_list) > 0:
    print(error_list)
    raise Exception(f'{len(error_list)} error(s) found')

with open(README_TEMPLATE, 'r') as file:
    template_string = file.read()
template = Template(template_string)
rendered_template = template.render(data=sorted_dict)

with open(README, 'w') as readme:
    readme.write(rendered_template)
