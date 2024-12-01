import subprocess
import os
from pyautogui import write
import time

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
    Welcome to EasyPeasyPackager!
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
    write("pyinstaller " + "-F " +("-w " if not show_command_line else "") + py_name_with_ext + "\n")
    if if_create:
        write(f"conda deactivate env_for_{py_name}\n")

    write("Finsh packaging, you can exit right now!")

if __name__ == "__main__":
    main()