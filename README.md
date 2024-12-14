# Bake

Bake is a tool for baking Python scripts into your terminal, making it easier to run your Python scripts as terminal commands. **Currently supports macOS only**.


## ⚠️ Important Notice

**Bake has undergone a complete rewrite**. Older versions of Bake will no longer function with this new codebase.

### What should I do if I'm using an old version?

To migrate to the latest version, simply follow the installation instructions [installer script](#installation--setup).

```zsh
python3 main.py
```


## Installation & Setup

To get started with the latest version of Bake, follow these steps:

### Step 1: Download the Bake Installer

In order for Bake to function correctly, you need to download and install the `bake` installer. This will allow you to set up Bake as a global command in your terminal.

You can find the `bake` installer in the [Bake Installer GitHub repository](https://github.com/Izaan17/BakeInstaller).

### Step 2: Run Bake

Once installed, you can run Bake with:

```zsh
bake -v
```


## Usage

### General Command

Bake allows you to turn your Python scripts into terminal commands. Use the following command to bake a new Python script:

```zsh
bake COMMAND_NAME PYTHON_SOURCE_FILE
```

- **COMMAND_NAME**: The name you want to assign to the baked command.
- **PYTHON_SOURCE_FILE**: The Python script you want to bake into a command.

### Example:

```zsh
bake myscript myscript.py
```

This will bake the `myscript.py` Python script and assign it the command `myscript`.


## Created Command Showcase

![Bake Tutorial](https://imgur.com/T57lKb8.gif)


## Available Flags

Bake provides several flags to manage and customize your baked commands. Here are some of the key options:

### List All Baked Commands

To list all currently baked commands, use the `-l` flag:

```zsh
bake -l
```

### View a Baked Command’s Contents

To view the contents of a specific baked command, use the `-vc` flag:

```zsh
bake -vc COMMAND_NAME
```

### Move to Directory of a Baked Command

To navigate to the directory where a specific baked command is located, use the `-in` flag:

```zsh
bake -in COMMAND_NAME
```

### Edit or Delete a Baked Command

You can also edit or delete existing baked commands using the `-e` and `-d` flags, respectively:

```zsh
bake -e COMMAND_NAME  # Edit a baked command
bake -d COMMAND_NAME   # Delete a baked command
```

### Edit Script Directly

You can also edit the contents of the target script by using the `-es` flag:
```zsh
bake -es COMMAND_NAME # Edit the script contents with the respective application
```

### View Current Version of Bake

To check which version of Bake you're using, run:

```zsh
bake -v
```


## Updating Bake

Bake will notify you if there is a new version available. To update Bake, use the following command:

```zsh
bake -u
```

You can also force an update with:

```zsh
bake -fu
```

This will pull the latest version from the Git repository and update your Bake installation.


## Conclusion

With Bake, managing and running your Python scripts as terminal commands has never been easier. Install and update Bake as needed, and enjoy a streamlined development process.

Don't forget to download the Bake installer from the [GitHub repository](https://github.com/Izaan17/BakeInstaller) to ensure everything works properly.