import os
import json
from pathlib import Path

def match(f_val, cf_val):
    matched = True
    f_keys = list(f_val.keys())
    cf_keys = list(cf_val.keys())
    for f_value in f_keys:
        matched = matched and (f_val[f_value] == cf_val[cf_keys[f_keys.index(f_value)]])
    return matched


json_dir_path = os.path.join(os.path.dirname(__file__), "build/json")
png_dir_path = os.path.join(os.path.dirname(__file__), "build/images")
json_files = [file for file in os.listdir(json_dir_path) if file.endswith(".json")]
png_files = [file for file in os.listdir(png_dir_path) if file.endswith(".png")]

attributes = {}

for file in json_files:
    with open(os.path.join(json_dir_path, file), 'r') as f:
        attributes[file] = json.loads(f.read())

same_num = 0
files_to_delete = list()
checked_files = list();
for f in attributes.keys():
    for cf in attributes.keys():
        if (f != cf) and (f not in files_to_delete) and (cf not in checked_files):
            for f_value in (attributes[f])["attributes"]:
                for cf_value in (attributes[cf])["attributes"]:
                    same_num += match(f_value, cf_value)
            if same_num > 5:
                files_to_delete.append(cf)
            same_num = 0
            checked_files.append(f)

for file in files_to_delete:
    print("Deleted file: " + os.path.join(json_dir_path, file))
    os.remove(os.path.join(json_dir_path, file))
    print("Deleted image: " + os.path.join(png_dir_path, Path(file).stem) + ".png")
    os.remove(os.path.join(png_dir_path, Path(file).stem) + ".png")
