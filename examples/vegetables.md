# JSON Schema

*Vegetable preferences*

## Properties

- **`fruits`** *(array)*
  - **Items** *(string)*
- **`vegetables`** *(array)*
  - **Items**: Refer to *#/definitions/veggie*.
## Definitions

- **`veggie`** *(object)*
  - **`veggieName`** *(string)*: The name of the vegetable.
  - **`veggieLike`** *(boolean)*: Do I like this vegetable?
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

