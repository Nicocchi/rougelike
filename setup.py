from cx_Freeze import setup, Executable

base = None    

executables = [Executable("engine.py", base=base)]

packages = ["idna", "os", "random", "tcod"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Twilight of The Pixie Goddes",
    options = options,
    version = "0.1",
    description = 'Twilight of The Pixie Goddes Pre-Alpha Demo v0.1',
    executables = executables
)