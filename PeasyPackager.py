import subprocess
import os
from pyautogui import write
import time
from shutil import copy
import ctypes

def is_admin():
    try:
        # 尝试使用管理员权限运行某个API
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin(program_path):
    try:
        # 使用ShellExecuteW函数以管理员权限运行
        proc = subprocess.Popen([
            'powershell',
            '-Command',
            f'Start-Process "{program_path}" -Verb runAs'
        ], shell=True)
        proc.communicate()
        print("PowerShell started.")
    except Exception as e:
        print(f"Cannot run as admin: {e}")

def is_anaconda_installed():
    # 查看是否有 anaconda
    anaconda_command_line = ""
    anaconda_paths = [
        "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Anaconda (anaconda3)",
        "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Anaconda (Miniconda)",
    ]

    for path in anaconda_paths:
        if os.path.exists(path):
            if os.path.isfile(os.path.join(path, "Anaconda PowerShell Prompt.lnk")):
                anaconda_command_line = os.path.join(path, "Anaconda PowerShell Prompt.lnk")
                break
            elif os.path.isfile(os.path.join(path, "Anaconda Prompt.lnk")):
                anaconda_command_line = os.path.join(path, "Anaconda Prompt.lnk")
                break

    return anaconda_command_line

def main():
    notice_for_use = '''
    Welcome to PeasyPackager!
    There is something you must know before using this program:

    1. This program requires conda to be installed:
    Download Anaconda or Miniconda from https://www.anaconda.com/download/

    2. When using this program, make sure that the program's input window is in focus.

    3. It takes time to run the program (depending on the Internet connection and number of dependencies).

    4. Chill and enjoy!

    Do you understand?[q for quit, any key for continue]
    '''
    print(notice_for_use)
    quit_or_not = input()
    if quit_or_not.lower() == 'q':
        quit()

    if not is_admin():
        print("Please run this program with administrator privileges.")
        quit()

    anaconda_command_line = is_anaconda_installed()

    if not anaconda_command_line:
        print("No Anaconda found. Please install Anaconda or Miniconda.")
        quit()

    print(f"Anaconda found: {anaconda_command_line}")

    # 新建环境还是用base
    dependencies = ""
    while True:
        base_or_new_env = input("Use base environment or create new environment?[base/new] ")
        if base_or_new_env.lower() == 'base':
            if_create = False
            break
        elif base_or_new_env.lower() == 'new':
            if_create = True
            py_ver = input("Enter the Python version: ")
            dependencies = input("Enter the dependency's/dependencies' package name(separate by space): ")
            break
        else:
            print("Invalid input. Please enter 'base' or 'new'.")

    # 询问.py文件路径
    while True:
        py_path = input("Enter the path of .py file: ")
        if os.path.isfile(py_path):
            break
        print("File does not exist. Please enter a valid path.")

    # 拆解路径
    folder_path = os.path.dirname(py_path)
    py_name_with_ext = os.path.basename(py_path)
    py_name, _ = os.path.splitext(py_name_with_ext)

    # 是否显示command_line
    while True:
        show_command_line = input("If run the program while opening a command line window?[y/n] ")
        if show_command_line.lower() == 'y':
            show_command_line = True
            break
        elif show_command_line.lower() == 'n':
            show_command_line = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    show_command_line = "-w " if not show_command_line else ""

    # 是否one file
    while True:
        one_file = input("Do you want to generate a single executable file?[y/n] ")
        if one_file.lower() == 'y':
            one_file = True
            break
        elif one_file.lower() == 'n':
            one_file = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    one_file = "-F " if one_file else ""

    # 是否加图标
    while True:
        icon = input("Do you want to add an icon?[y/n] ")
        if icon.lower() == 'y':
            add_icon = True
            while True:
                icon_path = input("Enter the path of icon file: ")
                if os.path.isfile(icon_path) and icon_path.endswith('.ico'):
                    break
                print("File does not exist or is not an icon file. Please enter a valid path.")
            break
        elif icon.lower() == 'n':
            add_icon = False
            break

    if add_icon:
        if not folder_path == os.path.dirname(icon_path):
            copy(icon_path, folder_path + "\\" + os.path.basename(icon_path))

    add_icon = f"-i {os.path.basename(icon_path)} " if add_icon else ""

    # 是否多Python文件打包
    while True:
        multi_py = input("Do you want to package multiple Python files?[y/n] ")
        if multi_py.lower() == 'y':
            multi_py = True
            multi_py_path = []
            while True:
                py_path_ = input("Enter the path of .py file(Enter two newlines to finish): ")
                if os.path.isfile(py_path_) and py_path_.endswith('.py'):
                    multi_py_path.append(py_path_)
                else:
                    if py_path_ == "":
                        break
                    print("File does not exist or is not a .py file. Please enter a valid path.")
            break
        elif multi_py.lower() == 'n':
            multi_py = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    # 执行
    run_as_admin(anaconda_command_line)
    time.sleep(5)

    if if_create:
        write(f"conda create -n env_for_{py_name} python={py_ver}\n")
        write("y\n")
        write(f"conda activate env_for_{py_name}\n")
        write(f"pip install {dependencies}\n")
    write("cd " + folder_path + "\n")
    write("pip install pyinstaller\n")
    if not multi_py:
        write("pyinstaller " + one_file + show_command_line + add_icon + py_name_with_ext + "\n")
        if if_create:
            write(f"conda deactivate env_for_{py_name}\n")

        write("Finsh packaging, you can exit right now!")
    else:
        write("pyi-makespec " + one_file + show_command_line + add_icon + py_name_with_ext + "\n")

        # 修改.spec文件
        spec_file_path = folder_path + "\\" + py_name + ".spec"
        with open(spec_file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        for index, line in enumerate(content):
            if line.strip().startswith("a = Analysis("):
                temp_list = content[index + 1].strip().strip("[],")
                temp_list = eval(f"[{temp_list}]")
                temp_list.append(multi_py_path)
                content[index + 1] = "    " + temp_list + ","
                break

        with open(spec_file_path, 'w', encoding='utf-8') as file:
            file.writelines(content)

        write("pyinstaller " + py_name + ".spec" + "\n")

    if if_create:
        write(f"conda deactivate env_for_{py_name}\n")

    write("Finsh packaging, you can exit right now!")

if __name__ == "__main__":
    main()