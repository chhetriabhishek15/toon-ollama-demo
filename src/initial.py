"""Optional helper/experiment script from the project root.
This file was moved into src/ to keep the top-level tidy.
"""

from toon_format import encode, decode

sample_json = {
    "name": "Alice",
    "age": 30
}

print(encode(sample_json))

tabular_array_json = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

print(encode(tabular_array_json))

toon_string = """[2,]{id,name}:
  1,Alice
  2,Bob"""

decoded_data = decode(toon_string)
print(decoded_data)
