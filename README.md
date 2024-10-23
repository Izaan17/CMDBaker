# CMDBaker
Bake python scripts into your terminal making it easier to run your python scripts.
Only works on macOS.

# Setup
To set up CMDBaker just run the python file.
```zsh
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
