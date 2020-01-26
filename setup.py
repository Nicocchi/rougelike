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
    name = "Rougelike",
    options = options,
    version = "0.1",
    description = 'Rougelike Demo',
    executables = executables
)