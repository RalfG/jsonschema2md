# jsonschema2md

[![](https://flat.badgen.net/pypi/v/jsonschema2md?icon=pypi)](https://pypi.org/project/jsonschema2md)
[![](https://flat.badgen.net/github/release/ralfg/jsonschema2md)](https://github.com/ralfg/jsonschema2md/releases)
[![](https://flat.badgen.net/github/checks/ralfg/jsonschema2md/)](https://github.com/ralfg/jsonschema2md/actions)
[![](https://flat.badgen.net/codecov/c/github/ralfg/jsonschema2md)](https://codecov.io/gh/RalfG/jsonschema2md)
![](https://flat.badgen.net/github/last-commit/ralfg/jsonschema2md)
![](https://flat.badgen.net/github/license/ralfg/jsonschema2md)


*Convert JSON Schemas to simple, human-readable Markdown documentation.*

---

For example:
```json
{
    "$id": "https://example.com/person.schema.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Person",
    "description": "JSON Schema for a person object.",
    "type": "object",
    "properties": {
      "firstName": {
        "type": "string",
        "description": "The person's first name."
      },
      "lastName": {
        "type": "string",
        "description": "The person's last name."
      }
    }
  }
```

will be converted to:

> # Person
> *JSON Schema for a person object.*
> ## Properties
>
> - **`firstName`** *(string)*: The person's first name.
> - **`lastName`** *(string)*: The person's last name.

See the [examples](https://github.com/RalfG/jsonschema2md/tree/master/examples)
directory for more elaborate examples.

---

## Installation

Install with pip
```sh
$ pip install jsonschema2md
```


## Usage

### From the CLI

```sh
$ jsonschema2md <input.json> <output.md>
```


### From Python

```python
import jsonschema2md
parser = jsonschema2md.Parser()
md_lines = parser.parse_schema(json.load(input_json))
```


## Contributing

Bugs, questions or suggestions? Feel free to post an issue in the
[issue tracker](https://github.com/RalfG/jsonschema2md/issues/) or to make a pull
request! See
[Contributing.md](https://github.com/RalfG/jsonschema2md/blob/master/CONTRIBUTING.md)
for more info.


## Changelog

See [Changelog.md](https://github.com/RalfG/jsonschema2md/blob/master/CHANGELOG.md).
