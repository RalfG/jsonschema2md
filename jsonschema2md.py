"""Convert JSON Schema to Markdown documentation."""


__author__ = "Ralf Gabriels"
__email__ = "ralfg@hotmail.be"
__license__ = "Apache-2.0"


try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version
import json
import re
from typing import Dict, Optional, Sequence
import io

import click

__version__ = version('jsonschema2md')


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

    def _construct_description_line(
        self,
        obj: Dict,
        add_type: bool = False
    ) -> Sequence[str]:
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
        if "maximum" in obj:
            description_line.append(f"Maximum: `{obj['maximum']}`.")
        if "enum" in obj:
            description_line.append(f"Must be one of: `{obj['enum']}`.")
        if "additionalProperties" in obj:
            if obj["additionalProperties"]:
                description_line.append("Can contain additional properties.")
            else:
                description_line.append("Cannot contain additional properties.")
        if "$ref" in obj:
            description_line.append(f"Refer to *{obj['$ref']}*.")
        if "default" in obj:
            description_line.append(f"Default: `{obj['default']}`.")

        # Only add start colon if items were added
        if description_line:
            description_line.insert(0, ":")

        return description_line

    def _construct_examples(
        self,
        obj: Dict,
        indent_level: int = 0,
        add_header: bool = True
    ) -> Sequence[str]:
        def dump_json_with_line_head(obj, line_head, **kwargs):
            f = io.StringIO(json.dumps(obj, **kwargs))
            result = [line_head + line for line in f.readlines()]
            return ''.join(result)

        example_lines = []
        if "examples" in obj:
            example_indentation = " " * self.tab_size * (indent_level + 1)
            if add_header:
                example_lines.append(f'\n{example_indentation}Examples:\n')
            for example in obj["examples"]:
                example_str = dump_json_with_line_head(
                    example,
                    line_head=example_indentation,
                    indent=4
                )
                example_lines.append(
                    f"{example_indentation}```json\n{example_str}\n{example_indentation}```\n"
                )
        return example_lines

    def _parse_object(
        self,
        obj: Dict,
        name: str,
        name_monospace: bool = True,
        output_lines: Optional[str] = None,
        indent_level: int = 0,
    ) -> Sequence[str]:
        """Parse JSON object and its items, definitions, and properties recursively."""
        if not isinstance(obj, dict):
            raise TypeError(
                f"Non-object type found in properties list: `{name}: {obj}`."
            )

        if not output_lines:
            output_lines = []

        # Construct full description line
        description_line = self._construct_description_line(obj)

        # Add full line to output
        description_line = " ".join(description_line)
        indentation = " " * self.tab_size * indent_level
        obj_type = f" *({obj['type']})*" if "type" in obj else ""
        name_formatted = f"**`{name}`**" if name_monospace else f"**{name}**"
        output_lines.append(
            f"{indentation}- {name_formatted}{obj_type}{description_line}\n"
        )

        # Recursively add items and definitions:
        for name in ["Items", "Definitions"]:
            if name.lower() in obj:
                output_lines = self._parse_object(
                    obj[name.lower()],
                    name,
                    name_monospace=False,
                    output_lines=output_lines,
                    indent_level=indent_level + 1
                )

        # Recursively add child properties
        if "properties" in obj:
            for property_name, property_obj in obj["properties"].items():
                output_lines = self._parse_object(
                    property_obj,
                    property_name,
                    output_lines=output_lines,
                    indent_level=indent_level + 1,
                )

        # Add examples
        output_lines.extend(
            self._construct_examples(obj, indent_level=indent_level)
        )

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

        # Add properties and definitions
        for name in ["Properties", "Definitions"]:
            if name.lower() in schema_object:
                output_lines.append(f"## {name}\n\n")
                for obj_name, obj in schema_object[name.lower()].items():
                    output_lines.extend(self._parse_object(obj, obj_name))

        # Add examples
        if "examples" in schema_object:
            output_lines.append("## Examples\n\n")
            output_lines.extend(self._construct_examples(
                schema_object, indent_level=0, add_header=False
            ))

        return output_lines


@click.command()
@click.version_option(version=__version__)
@click.argument("input-json", type=click.File("rt"), metavar="<input.json>")
@click.argument("output-markdown", type=click.File("wt"), metavar="<output.md>")
def main(input_json, output_markdown):
    """Convert JSON Schema to Markdown documentation."""
    parser = Parser()
    output_md = parser.parse_schema(json.load(input_json))
    output_markdown.writelines(output_md)
    click.secho("✔ Successfully parsed schema!", bold=True, fg="green")


if __name__ == "__main__":
    main()
