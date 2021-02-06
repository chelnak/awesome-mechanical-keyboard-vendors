# :rocket: Awesome Mechanical Keyboard Vendors [![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)

A curated list of *awesome* independent mechanical keyboard vendors organised alphabetically by location.

## Contents

{% for key in data.keys() -%}
* [{{ key }}](#{{ key.replace(' ', '-') }})
{% endfor %}
{% for key in data.keys() -%}
## {{ key }}

{% for p in data[key] -%}
* [{{ p['name'] }}]({{ p['url'] }})
{% endfor %}
{% endfor -%}

## Contributing

Contributions welcome! Read the [contribution guidelines](CONTRIBUTING.md) first.
