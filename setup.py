# import sys
# import cx_Freeze
# import os
# import ntk
# # build_exe_options =
#
# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"
#
# # python_dir = os.path.dirname(os.path.dirname(os.__file__))
# # os.environ['TCL_LIBRARY'] = os.path.join(python_dir,'tcl','tcl8.6')
# #
# # os.environ['TK_LIBRARY'] = os.path.join(python_dir, 'tcl''tk8.6')
#
#
# executables = [cx_Freeze.Executable("restora_lite.py", base=base, icon="favicon.ico")]
#
# cx_Freeze.setup(
#     name="Bhojon",
#     version="3.2",
#     description="Bhojon Restora Application",
#     options={"build_exe": {"packages":["os", "ntk", "requests", "sys", "license", "tkinter", "_help", "time"], "include_files":["favicon.ico", "application","fonts"]}},
#     executables=executables
# )
#


#############################################################
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os", "ntk", "requests", "sys", "license", "tkinter", "_help", "time"],  "include_files":["favicon.ico", "application","fonts"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Bhojon Desktop",
    version="3.5",
    description="Bhojon Restora Application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("restora_lite.py", base=base,icon="favicon.ico")],
)
#############################################################




# import cx_Freeze
# import sys


# base = None

# if sys.platform == 'win32':
#     base = "Win32GUI"

# executables = [cx_Freeze.Executable("restora_lite.py", base=base, icon="favicon.ico")]

# cx_Freeze.setup(
#     name = "Bhojon",
#     options = {"build_exe": {"packages":["os", "ntk", "requests", "sys", "license", "tkinter", "_help", "time"], "include_files":["favicon.ico"]}},
#     version = "0.01",
#     description = "Bhojon Restora Application",
#     executables = executables
#     )



# import sys
# from cx_Freeze import setup, Executable

# # Dependencies are automatically detected, but it might need fine tuning.
# # "packages": ["os"] is used as example only
# build_exe_options = {"packages": ["os","ntk", "requests", "sys", "license","tkinter", "_help", "time"], "include_files":["favicon.ico"]}

# # base="Win32GUI" should be used only for Windows GUI app
# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

# setup(
#     name="Bhojon",
#     version="2.1",
#     description="Bhojon Desktop Application!",
#     options={"build_exe": build_exe_options},
#     executables=[Executable("restora_lite.py", base=base)],
# )