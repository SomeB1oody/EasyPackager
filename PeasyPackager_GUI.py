import subprocess
import os
from pyautogui import write
import time
from shutil import copy
import re
import wx
import ctypes

def is_valid_version(version):
    pattern = r'^\d+(\.\d+){1,2}$'
    return re.match(pattern, version) is not None

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

class PeasyPackagerWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(PeasyPackagerWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.vbox.Add(wx.StaticText(
            panel, label=f"Anaconda: {is_anaconda_installed()}" + is_anaconda_installed()),
            flag=wx.ALL, border=5)

        # 新建还是base
        self.if_create = wx.RadioBox(
            panel, label="Use base environment or create new environment?", choices=[
                'base', 'new'
            ]
        )
        self.if_create.Bind(wx.EVT_RADIOBOX, self.on_if_create)
        self.vbox.Add(self.if_create, flag=wx.ALL, border=5)

        # 输入路径
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.file_button = wx.Button(panel, label="Select file")
        self.Bind(wx.EVT_BUTTON, self.on_select_file, self.file_button)
        self.hbox.Add(self.file_button, flag=wx.ALL, border=5)
        self.input_path_text = wx.StaticText(panel, label="Click \"Select file\" first")
        self.hbox.Add(self.input_path_text, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox, flag=wx.EXPAND)

        # 输入python版本
        self.vbox.Add(wx.StaticText(panel, label="Enter the Python version: "), flag=wx.ALL, border=5)
        self.py_ver = wx.TextCtrl(panel)
        self.py_ver.Enable(False)
        self.vbox.Add(self.py_ver, flag=wx.ALL, border=5)

        # 输入依赖项
        self.vbox.Add(wx.StaticText(
            panel, label="Enter the dependency's/dependencies' package name(separate by space): "),
            wx.ALL, border=5)
        self.dependencies = wx.TextCtrl(panel)
        self.dependencies.Enable(False)
        self.vbox.Add(self.dependencies, flag=wx.ALL, border=5)

        # 选择参数
        self.one_file = wx.CheckBox(panel, label="Generates a single executable file")
        self.vbox.Add(self.one_file, flag=wx.ALL, border=5)
        self.one_file.SetValue(True)

        self.show_command_line = wx.CheckBox(
            panel, label="Runs the program while opening a command line window"
        )
        self.vbox.Add(self.show_command_line, flag=wx.ALL, border=5)
        self.show_command_line.SetValue(True)

        self.icon = wx.CheckBox(panel, label="Add icon for the program")
        self.vbox.Add(self.icon, flag=wx.ALL, border=5)
        self.icon.Bind(wx.EVT_CHECKBOX, self.on_icon)
        self.icon.SetValue(False)

        self.multi_file = wx.CheckBox(panel, label="package multiple Python files")
        self.vbox.Add(self.multi_file, flag=wx.ALL, border=5)
        self.multi_file.SetValue(False)
        self.multi_file.Bind(wx.EVT_CHECKBOX, self.on_multi_file)

        # 加图标
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.icon_button = wx.Button(panel, label="Select file")
        self.icon_button.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.on_select_icon, self.icon_button)
        self.hbox2.Add(self.icon_button, flag=wx.ALL, border=5)
        self.icon_path_text = wx.StaticText(panel, label="Click \"Select file\" first")
        self.hbox2.Add(self.icon_path_text, flag=wx.ALL, border=5)
        self.vbox.Add(self.hbox2, flag=wx.EXPAND)

        # 多文件打包
        self.multi_py = wx.Button(panel, label="Select multiple Python files")
        self.vbox.Add(self.multi_py, flag=wx.ALL, border=5)
        self.multi_py.Bind(wx.EVT_BUTTON, self.on_multi_py)
        self.multi_py.Enable(False)

        # 执行按钮
        self.execute_button = wx.Button(panel, label="Execute")
        self.vbox.Add(self.execute_button, flag=wx.ALL, border=5)
        self.execute_button.Bind(wx.EVT_BUTTON, self.on_execute_button)

        # 设置面板的布局管理器
        panel.SetSizer(self.vbox)
        panel.Layout()

    def on_select_file(self, event):
        with wx.FileDialog(None, "Select a file", wildcard="*.py",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.input_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_file = dialog.GetPath()

    def on_if_create(self, event):
        if self.if_create.GetSelection() == 0:
            self.dependencies.Enable(False)
            self.py_ver.Enable(False)
        else:
            self.dependencies.Enable(True)
            self.py_ver.Enable(True)

    def on_icon(self, event):
        if self.icon.GetValue():
            self.icon_button.Enable(True)
        else:
            self.icon_button.Enable(False)

    def on_select_icon(self, event):
        with wx.FileDialog(None, "Select a icon", wildcard="*.ico",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.icon_path_text.SetLabel(f"{dialog.GetPath()}")
                self.selected_icon = dialog.GetPath()

    def on_multi_file(self, event):
        if self.multi_file.GetValue():
            self.multi_py.Enable(True)
        else:
            self.multi_py.Enable(False)

    def on_multi_py(self, event):
        with wx.FileDialog(None, "Select files", wildcard="*.py",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.paths = dialog.GetPaths()

    def on_execute_button(self, event):
        anaconda_command_line = is_anaconda_installed()
        if_create =True if self.if_create.GetSelection() == 1 else False
        py_path = self.selected_file

        if not py_path:
            wx.MessageBox("Please select a file first.","Error", wx.OK | wx.ICON_ERROR)
            return

        if if_create:
            py_ver = self.py_ver.GetValue()

            if not is_valid_version(py_ver):
                wx.MessageBox(
                    "Invalid Python version. Please enter a valid version.",
                    "Error", wx.OK | wx.ICON_ERROR)
                return

            dependencies = self.dependencies.GetValue()

        # 拆解路径
        folder_path = os.path.dirname(py_path)
        py_name_with_ext = os.path.basename(py_path)
        py_name, _ = os.path.splitext(py_name_with_ext)

        # 单文件
        one_file = "-F " if self.one_file.GetValue() else ""

        # 显示命令行
        show_command_line = "-w " if not self.show_command_line.GetValue() else ""

        # 加图标
        if self.icon.GetValue():
            icon_path = self.selected_icon
            if not folder_path == os.path.dirname(icon_path):
                copy(icon_path, folder_path + "\\" + os.path.basename(icon_path))

            add_icon = f"-i {os.path.basename(icon_path)}"
        else:
            add_icon = ""

        # 多文件
        if self.multi_file.GetValue():
            multi_py_path = self.paths

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

        if not self.multi_file.GetValue():
            write("pyinstaller " + one_file + show_command_line + add_icon + py_name_with_ext + "\n")

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
    app = wx.App()
    frame = PeasyPackagerWX(None)
    frame.SetTitle('Peasy Packager with GUI')
    frame.SetSize((600, 575))
    # 先查找是否有anaconda
    anaconda_command_line = is_anaconda_installed()
    if not anaconda_command_line:
        wx.MessageBox(
            "No Anaconda found. Please install Anaconda or Miniconda.", "Error", wx.OK | wx.ICON_ERROR
        )
        quit()

    # 确认有无管理员权限
    if not is_admin():
        wx.MessageBox(
            "Please run this program with administrator privileges.", "Error", wx.OK | wx.ICON_ERROR
        )
        quit()
    frame.Show()
    app.MainLoop()