# JSON Schema

_Vegetable preferences_

## Properties

- **`fruits`** _(array)_
  - **Items** _(string)_
- **`vegetables`** _(array)_
  - **Items**: Refer to _[#/definitions/veggie](#definitions/veggie)_.

## Definitions

- <a id="definitions/veggie"></a>**`veggie`** _(object)_
  - **`veggieName`** _(string, required)_: The name of the vegetable.
  - **`veggieLike`** _(boolean, required)_: Do I like this vegetable?
  - **`type_number`** _(array)_: The type and number of vegetable.
    - **Items**:
      - _string_: The type of the vegetable.
      - _number_: The number of vegetable.

## Examples

```json
{
  "fruits": ["apple", "orange"],
  "vegetables": [
    {
      "veggieName": "cabbage",
      "veggieLike": true
    }
  ]
}
```
