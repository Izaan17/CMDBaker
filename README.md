# CMDBaker
Bake python scripts into your terminal making it easier to run your python scripts.
Only works on macOS.

# ⚠️ Important
CMDBaker now has a completely different code base. This means that if you are on older versions of CMDBaker it will no longer work.

### What do I do if I'm on an old version?
Simply rerun the original python script called main.py it will automatically re-bake itself.

# Setup
To set up CMDBaker just run the python file.
```zsh
pip install -r requirements.txt

python3 main.py
```

# Usage
![CMDBaker Usage](https://imgur.com/fck4GiU.gif)

```zsh
bake COMMAND_NAME PYTHON_SOURCE_FILE
```

# Created Command Showcase
![CMDBaker Tutorial](https://imgur.com/T57lKb8.gif)

# Flags
## List all baked commands
![CMDBaker Flags](https://imgur.com/B5xG78j.gif)

```zsh
bake -l
```

# View baked commands contents

![CMDBaker Flags](https://imgur.com/mvNlXKu.gif)

```zsh
bake -v COMMAND_NAME
```

#### Move to directory of python script
```zsh
bake -in COMMAND_NAME
```
