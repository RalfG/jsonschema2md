"""Convert JSON Schema to Markdown documentation."""


__author__ = "Ralf Gabriels"
__email__ = "ralfg@hotmail.be"
__license__ = "Apache-2.0"


try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

import io
import json
import re
from typing import Dict, Optional, Sequence

import click
import yaml

__version__ = version("jsonschema2md")


class Parser:
    """
    JSON Schema to Markdown parser.

    Examples
    --------
    >>> import jsonschema2md
    >>> parser = jsonschema2md.Parser()
    >>> md_lines = parser.parse_schema(json.load(input_json))
    """

    tab_size = 2

    def __init__(self, examples_as_yaml: bool = False, show_examples: str = "all"):
        """
        Setup JSON Schema to Markdown parser.

        Parameters
        ----------
        examples_as_yaml : bool, default False
            Parse examples in YAML-format instead of JSON.
        show_examples: str, default 'all'
            Parse examples for only objects, only properties or all. Valid options are
            `{"all", "object", "properties"}`.

        """
        self.examples_as_yaml = examples_as_yaml

        valid_show_examples_options = ["all", "object", "properties"]
        show_examples = show_examples.lower()
        if show_examples in valid_show_examples_options:
            self.show_examples = show_examples
        else:
            raise ValueError(
                f"`show_examples` option should be one of "
                f"`{valid_show_examples_options}`; `{show_examples}` was passed."
            )

    def _construct_description_line(self, obj: Dict, add_type: bool = False) -> Sequence[str]:
        """Construct description line of property, definition, or item."""
        description_line = []

        if "description" in obj:
            ending = "" if re.search(r"[.?!;]$", obj["description"]) else "."
            description_line.append(f"{obj['description']}{ending}")
        if add_type:
            if "type" in obj:
                description_line.append(f"Must be of type *{obj['type']}*.")
        if "minimum" in obj:
            description_line.append(f"Minimum: `{obj['minimum']}`.")
        if "exclusiveMinimum" in obj:
            description_line.append(f"Exclusive minimum: `{obj['exclusiveMinimum']}`.")
        if "maximum" in obj:
            description_line.append(f"Maximum: `{obj['maximum']}`.")
        if "exclusiveMaximum" in obj:
            description_line.append(f"Exclusive maximum: `{obj['exclusiveMaximum']}`.")
        if "minItems" in obj or "maxItems" in obj:
            length_description = "Length must be "
            if "minItems" in obj and "maxItems" not in obj:
                length_description += f"at least {obj['minItems']}."
            elif "maxItems" in obj and "minItems" not in obj:
                length_description += f"at most {obj['maxItems']}."
            elif obj["minItems"] == obj["maxItems"]:
                length_description += f"equal to {obj['minItems']}."
            else:
                length_description += f"between {obj['minItems']} and {obj['maxItems']} (inclusive)."
            description_line.append(length_description)
        if "enum" in obj:
            description_line.append(f"Must be one of: `{json.dumps(obj['enum'])}`.")
        if "additionalProperties" in obj:
            if obj["additionalProperties"]:
                description_line.append("Can contain additional properties.")
            else:
                description_line.append("Cannot contain additional properties.")
        if "$ref" in obj:
            description_line.append(f"Refer to *{obj['$ref']}*.")
        if "default" in obj:
            description_line.append(f"Default: `{json.dumps(obj['default'])}`.")

        # Only add start colon if items were added
        if description_line:
            description_line.insert(0, ":")

        return description_line

    def _construct_examples(self, obj: Dict, indent_level: int = 0, add_header: bool = True) -> Sequence[str]:
        def dump_json_with_line_head(obj, line_head, **kwargs):
            f = io.StringIO(json.dumps(obj, **kwargs))
            result = [line_head + line for line in f.readlines()]
            return "".join(result)

        def dump_yaml_with_line_head(obj, line_head, **kwargs):
            f = io.StringIO(yaml.dump(obj, **kwargs))
            result = [line_head + line for line in f.readlines()]
            return "".join(result).rstrip()

        example_lines = []
        if "examples" in obj:
            example_indentation = " " * self.tab_size * (indent_level + 1)
            if add_header:
                example_lines.append(f"\n{example_indentation}Examples:\n")
            for example in obj["examples"]:
                if self.examples_as_yaml:
                    lang = "yaml"
                    dump_fn = dump_yaml_with_line_head
                else:
                    lang = "json"
                    dump_fn = dump_json_with_line_head
                example_str = dump_fn(example, line_head=example_indentation, indent=4)
                example_lines.append(
                    f"{example_indentation}```{lang}\n" f"{example_str}\n" f"{example_indentation}```\n\n"
                )
        return example_lines

    def _parse_object(
        self,
        obj: Dict,
        name: Optional[str],
        name_monospace: bool = True,
        output_lines: Optional[str] = None,
        indent_level: int = 0,
    ) -> Sequence[str]:
        """Parse JSON object and its items, definitions, and properties recursively."""
        if not isinstance(obj, dict):
            raise TypeError(f"Non-object type found in properties list: `{name}: {obj}`.")

        if not output_lines:
            output_lines = []

        indentation = " " * self.tab_size * indent_level
        indentation_items = " " * self.tab_size * (indent_level + 1)

        # Construct full description line
        description_line_base = self._construct_description_line(obj)
        description_line = list(
            map(
                lambda line: line.replace("\n\n", "<br>" + indentation_items),
                description_line_base,
            )
        )

        # Add full line to output
        description_line = " ".join(description_line)
        if name is None:
            obj_type = f"*{obj['type']}*" if "type" in obj else ""
            name_formatted = ""
        else:
            obj_type = f" *({obj['type']})*" if "type" in obj else ""
            name_formatted = f"**`{name}`**" if name_monospace else f"**{name}**"
        output_lines.append(f"{indentation}- {name_formatted}{obj_type}{description_line}\n")

        # Recursively parse subschemas following schema composition keywords
        schema_composition_keyword_map = {
            "allOf": "All of",
            "anyOf": "Any of",
            "oneOf": "One of",
        }
        for key, label in schema_composition_keyword_map.items():
            if key in obj:
                output_lines.append(f"{indentation_items}- **{label}**\n")
                for child_obj in obj[key]:
                    output_lines = self._parse_object(
                        child_obj,
                        None,
                        name_monospace=False,
                        output_lines=output_lines,
                        indent_level=indent_level + 2,
                    )

        # Recursively add items and definitions
        for name in ["items", "definitions"]:
            if name in obj:
                output_lines = self._parse_object(
                    obj[name],
                    name.capitalize(),
                    name_monospace=False,
                    output_lines=output_lines,
                    indent_level=indent_level + 1,
                )

        # Recursively add additional child properties
        if "additionalProperties" in obj and isinstance(obj["additionalProperties"], dict):
            output_lines = self._parse_object(
                obj["additionalProperties"],
                "Additional Properties",
                name_monospace=False,
                output_lines=output_lines,
                indent_level=indent_level + 1,
            )

        # Recursively add child properties
        for name in ["properties", "patternProperties"]:
            if name in obj:
                for property_name, property_obj in obj[name].items():
                    output_lines = self._parse_object(
                        property_obj,
                        property_name,
                        output_lines=output_lines,
                        indent_level=indent_level + 1,
                    )

        # Add examples
        if self.show_examples in ["all", "properties"]:
            output_lines.extend(self._construct_examples(obj, indent_level=indent_level))

        return output_lines

    def parse_schema(self, schema_object: Dict) -> Sequence[str]:
        """Parse JSON Schema object to markdown text."""
        output_lines = []

        # Add title and description
        if "title" in schema_object:
            output_lines.append(f"# {schema_object['title']}\n\n")
        else:
            output_lines.append("# JSON Schema\n\n")
        if "description" in schema_object:
            output_lines.append(f"*{schema_object['description']}*\n\n")

        # Add items
        if "items" in schema_object:
            output_lines.append(f"## Items\n\n")
            output_lines.extend(self._parse_object(schema_object["items"], "Items", name_monospace=False))

        # Add additional properties
        if "additionalProperties" in schema_object and isinstance(
            schema_object["additionalProperties"], dict
        ):
            output_lines.append(f"## Additional Properties\n\n")
            output_lines.extend(
                self._parse_object(
                    schema_object["additionalProperties"],
                    "Additional Properties",
                    name_monospace=False,
                )
            )

        # Add pattern properties
        if "patternProperties" in schema_object:
            output_lines.append(f"## Pattern Properties\n\n")
            for obj_name, obj in schema_object["patternProperties"].items():
                output_lines.extend(self._parse_object(obj, obj_name))

        # Add properties and definitions
        for name in ["properties", "definitions"]:
            if name in schema_object:
                output_lines.append(f"## {name.capitalize()}\n\n")
                for obj_name, obj in schema_object[name].items():
                    output_lines.extend(self._parse_object(obj, obj_name))

        # Add examples
        if "examples" in schema_object and self.show_examples in ["all", "object"]:
            output_lines.append("## Examples\n\n")
            output_lines.extend(self._construct_examples(schema_object, indent_level=0, add_header=False))

        return output_lines


@click.command()
@click.version_option(version=__version__)
@click.argument("input-json", type=click.File("rt"), metavar="<input.json>")
@click.argument("output-markdown", type=click.File("wt"), metavar="<output.md>")
@click.option(
    "--examples-as-yaml",
    type=bool,
    default=False,
    help="Parse examples in YAML-format instead of JSON.",
)
@click.option(
    "--show-examples",
    type=click.Choice(["all", "properties", "object"], case_sensitive=False),
    default="all",
    help="Parse examples for only the main object, only properties, or all.",
)
def main(input_json, output_markdown, examples_as_yaml, show_examples):
    """Convert JSON Schema to Markdown documentation."""
    parser = Parser(examples_as_yaml=examples_as_yaml, show_examples=show_examples)
    output_md = parser.parse_schema(json.load(input_json))
    output_markdown.writelines(output_md)
    click.secho("✔ Successfully parsed schema!", bold=True, fg="green")


if __name__ == "__main__":
    main()
