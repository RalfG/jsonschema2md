# JSON Schema

*A representation of a person, company, organization, or place*

## Properties

- **`fruits`** *(array)*
  - **Items** *(string)*
- **`vegetables`** *(array)*
  - **Items**: Refer to *#/definitions/veggie*.
## Definitions

- **`veggie`** *(object)*
  - **`veggieName`** *(string)*: The name of the vegetable.
  - **`veggieLike`** *(boolean)*: Do I like this vegetable?

  Examples:
  ```json
  {
      "veggieName": "carrot",
      "veggieLike": true
  }
  ```
## Examples

  ```json
  {
      "fruits": [
          "apple",
          "orange"
      ],
      "vegetables": [
          {
              "veggieName": "cabbage",
              "veggieLike": true
          }
      ]
  }
  ```
