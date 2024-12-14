# Bake

Bake python scripts into your terminal making it easier to run your python scripts.
Only works on macOS.

# ⚠️ Important

Bake now has a completely different code base. This means any older versions of Bake will no longer work.

### What do I do if I'm on an old version?

Simply rerun the original python script called main.py it will automatically re-bake itself.

```zsh
python3 main.py
```

# Setup

To set up Bake just run the python file.

```zsh
pip install -r requirements.txt

python3 main.py
```

# Usage

![Bake Usage](https://imgur.com/fck4GiU.gif)

```zsh
bake COMMAND_NAME PYTHON_SOURCE_FILE
```

# Created Command Showcase

![Bake Tutorial](https://imgur.com/T57lKb8.gif)

# Flags

## List all baked commands

![Bake Flags](https://imgur.com/B5xG78j.gif)

```zsh
bake -l
```

# View baked commands contents

```zsh
bake -vc COMMAND_NAME
```

#### Move to directory of python script

```zsh
bake -in COMMAND_NAME
```
