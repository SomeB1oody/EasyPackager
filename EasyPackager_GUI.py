import wx
import os
import subprocess
import re
import time
from pyautogui import write

def is_valid_version(version):
    pattern = r'^\d+(\.\d+){1,2}$'
    return re.match(pattern, version) is not None

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

class EasyPackagerWX(wx.Frame):
    def __init__(self, *args, **kw):
        super(EasyPackagerWX, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 先查找是否有anaconda
        anaconda_command_line = is_anaconda_installed()
        if not anaconda_command_line:
            wx.MessageBox(
                "No Anaconda found. Please install Anaconda or Miniconda.",
                "Error", wx.OK | wx.ICON_ERROR)
            return

        self.vbox.Add(wx.StaticText(
            panel, label=f"Anaconda: {anaconda_command_line}" + is_anaconda_installed()),
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
            wx.ALL,border=5)
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

        # 执行按钮
        self.execute_button = wx.Button(panel, label="Execute")
        self.vbox.Add(self.execute_button, flag=wx.ALL, border=5)
        self.execute_button.Bind(wx.EVT_BUTTON, self.on_execute_button)

        # 设置面板的布局管理器
        panel.SetSizer(self.vbox)
        panel.Layout()

    def on_select_file(self, event):
        with wx.FileDialog(None, "Select a video", wildcard="所有文件 (*.*)|*.*",
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

        # 参数
        parameters = ""
        if self.one_file.GetValue():
            parameters += "-F "
        if not self.show_command_line.GetValue():
            parameters += "-w "

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
        write("pyinstaller " + parameters + py_name_with_ext + "\n")
        if if_create:
            write(f"conda deactivate env_for_{py_name}\n")

        write("Finsh packaging, you can exit right now!")


if __name__ == "__main__":
    app = wx.App()
    frame = EasyPackagerWX(None)
    frame.SetTitle('Easy Packager with GUI')
    frame.SetSize((600, 425))
    frame.Show()
    app.MainLoop()