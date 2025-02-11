import os
import json


def concat_text(file_to_concat, role, text):
    # Concats the transcribed text to the bottom of the current date's file

  with open(file_to_concat, 'r') as file:
    existing_data = json.load(file)
    existing_data.append({"role": role, "content": text})

    with open(file_to_concat, 'w') as edit_file:
      json.dump(existing_data, edit_file)
