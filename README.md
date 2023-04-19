# jsonschema2md

[![](https://flat.badgen.net/pypi/v/jsonschema2md?icon=pypi)](https://pypi.org/project/jsonschema2md)
[![](https://flat.badgen.net/github/release/ralfg/jsonschema2md)](https://github.com/ralfg/jsonschema2md/releases)
[![](https://flat.badgen.net/github/checks/ralfg/jsonschema2md/)](https://github.com/ralfg/jsonschema2md/actions)
[![](https://flat.badgen.net/codecov/c/github/ralfg/jsonschema2md)](https://codecov.io/gh/RalfG/jsonschema2md)
![](https://flat.badgen.net/github/last-commit/ralfg/jsonschema2md)
![](https://flat.badgen.net/github/license/ralfg/jsonschema2md)

_Convert JSON Schemas to simple, human-readable Markdown documentation._

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
>
> _JSON Schema for a person object._
>
> ## Properties
>
> - **`firstName`** _(string)_: The person's first name.
> - **`lastName`** _(string)_: The person's last name.

See the [examples](https://github.com/RalfG/jsonschema2md/tree/master/examples)
directory for more elaborate examples.

---

## Installation

Install with pip

```sh
pip install jsonschema2md
```

## Usage

### From the CLI

```sh
jsonschema2md [OPTIONS] <input.json> <output.md>
```

### From Python

```python
import json
import jsonschema2md

parser = jsonschema2md.Parser(
    examples_as_yaml=False,
    show_examples="all",
)
with open("./examples/food.json", "r") as json_file:
    md_lines = parser.parse_schema(json.load(json_file))
print(''.join(md_lines))
```

### Options

- `examples_as_yaml`: Parse examples in YAML-format instead of JSON. (`bool`, default:
  `False`)
- `show_examples`: Parse examples for only the main object, only properties, or all.
  (`str`, default `all`, options: `object`, `properties`, `all`)

## pre-commit hook

You can use the pre-commit hook with:

```yaml
repos:
  - repo: https://github.com/sbrunner/jsonschema2md2
    hooks:
      - id: jsonschema2md
        rev: <version> # Use the ref you want to point at
        files: schema.json
        args:
          - --pre-commit
          - schema.json
          - schema.md
```

## Contributing

Bugs, questions or suggestions? Feel free to post an issue in the
[issue tracker](https://github.com/sbrunner/jsonschema2md2/issues/) or to make a pull
request! See
[Contributing.md](https://github.com/sbrunner/jsonschema2md2/blob/master/CONTRIBUTING.md)
for more info.

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```

## Changelog

See [Changelog.md](https://github.com/RalfG/jsonschema2md/blob/master/CHANGELOG.md).
