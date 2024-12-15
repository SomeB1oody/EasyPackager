# EasyPeasyPackager
*Easy way to package your python file*
*简单的python文件打包器*

---
# 1.Intro
**EasyPeasyPackager** is a lightweight Python file packaging tool that uses wxPython as the frontend, conda environment as the base, and pyinstaller as the backend.
**EasyPeasyPackager**是一个以wxPython为前端，基于conda环境，以pyinstaller为后端的轻量化python文件打包程序。

Each program comes with both a non-GUI and a GUI version. The non-GUI version offers the simplest operations and code, making it easier to understand. The GUI version supports more complex operations, providing a more advanced and user-friendly experience.
每个程序都提供了 GUI 和非 GUI 版本。非 GUI 版本提供最简单的操作和代码，更易于理解；而 GUI 版本支持更复杂的操作，提供更高级且用户友好的体验。

Due to my limited capabilities, the code may have some imperfections. I warmly welcome everyone to share their suggestions and contribute to the project. For more details, please see the Contribution. Thank you for your understanding!
由于个人能力有限，代码可能存在一些不足，热烈欢迎大家分享建议并为项目做出贡献。详细信息请参考贡献。感谢您的理解！

---


# 2.Function 功能
**EasyPackager** allows users to choose between compiling in the conda base environment or creating a new virtual environment (requiring users to specify the necessary dependencies). Additionally, the program provides options to enable "single executable output only" (-F) and "open the command line during execution" (-w).
**EasyPackager**支持用户选择在conda的base环境抑或是创建一个新虚拟环境（需要用户输入所需的依赖项）来编译。同时，程序也开放了“是否只输出单个可执行文件”（-F）和“是否在运行同时打开命令行”（-w）的选项。

**PeasyPackager** is now available. PeasyPackager is an advanced version of EasyPackager, offering support for adding icons(.ico) to programs and packaging multiple Python files into a single executable.
**PeasyPackager**现已推出！ PeasyPackager是EasyPackager的高级版本，支持向程序添加图标(.ico)以及将多个 Python 文件打包到单个可执行文件中。


For a detailed user guide, please refer to the User Guide.
如需要详细的用户指南，请移步至用户指南。

---
# 3.Required environment 要求环境

- Python version should be at least 3.10.
  Python版本至少要3.10
  
- Must [install conda](https://www.anaconda.com/download)
  必须[安装conda](https://www.anaconda.com/download)。
  
-  **The program must be run as an administrator**; otherwise, there may be permission issues when installing dependencies with pip.
   **程序必须以管理员身份运行**，否则可能在pip安装依赖项时可能会有权限问题。

---
# 4. User Guide

Please read **Required environment** first, make sure your environment satisfies all requirements.
请你先阅读**要求环境**，确认你的环境满足所有要求

## 4.0. Install conda
- Enter your email (anaconda doesn't require to create a account to download).
  输入你的邮箱(anaconda不要求创建新账号才能下载)
![enter_email](https://github.com/user-attachments/assets/1a2f3cdf-4a80-4142-a80e-b1c994f1c316)

- Download
  下载
![download](https://github.com/user-attachments/assets/afecab61-bdff-448e-afe5-041a180697ac)

A brief digression: If you want to use conda to manage your dependencies, download Anaconda is a good choice (It even has a GUI fot you to manage dependencies); If you just use conda to package your python file, scroll down, you can see "Miniconda Installers". It's better to install miniconda because it's lightweight (but has no GUI).
题外话：如果你想用conda来管理依赖项，下载Anaconda是很不错的（它甚至还有图形界面来管理依赖项）；如果你只是想下载conda来打包你的python文件，那就在这个网页下滑，你会看到“Miniconda installer”，这会是你更好的选择，因为它更轻量（但是没有图形界面）。

- Then install (You can choose a custom installation path or proceed with the default installation.)
  然后安装(你可以选择路径安装，也可以就按照默认安装)

- After installation, make sure to check the Windows Start menu for **Anaconda Prompt** or **Anaconda Powershell Prompt**. If you see either of them, the installation was successful.
  安装好后请务必检查Windows的开始菜单上有没有**Anaconda Prompt**或者**Anaconda Powershell Prompt**。如果有，那就是对的。
  
![Start_menu](https://github.com/user-attachments/assets/bf126aa6-7033-4a8d-b0a4-3c24055928fd)

## 4.1 Use EasyPackager
### 1. Open EasyPackager as an admin.
Now Let me explain the meaning of each option.
现在我来解释每个选项的意思

![EP](https://github.com/user-attachments/assets/3d2c35a6-e2b6-426b-baae-c4f511a2b696)

**Base environment** vs. **create new environment** **Base环境**和**创建新环境**的对比
 
 Executable files packaged in the base environment tend to be quite large. This is because PyInstaller includes all the libraries and modules from your environment during packaging, including many that you may not even need! These unnecessary libraries not only bloat the size of the executable but can also make it run slower, laggy, and overly cumbersome. Therefore, this method of packaging is not recommended. It is highly recommended to use the second approach — creating a new environment for packaging.
 Base环境下打包产生的可执行文件都比较大，这是因为 Pyinstaller 打包的时候会把你环境中的库和模块全部打包进去，这就会使一些你根本用不着的库和模块也被打包进去了！而且这些库被打包之后不仅会使可执行文件变大，还会使其运行变卡变慢、变得十分臃肿。因此，不建议这样的打包方式。十分地建议用第二种方式进行打包 —— 创建新环境。

### 2. Select a python file
Click "Select file" button, choose a python file.
![Select_file](https://github.com/user-attachments/assets/a1596597-ecb8-41c4-b40f-8517f304a45b)

### 3. What to do next if I choose create a new environment? 在选择了创建新环境后该干什么？
![new_env](https://github.com/user-attachments/assets/e7d0d7cd-0ba2-411e-af7c-5ca07931c95c)

 After creating a new environment, you will notice that two input fields are enabled.
 在创建完新环境后你会发现有两处输入框被启用了。
 
 In the **Enter the Python version** field, you need to specify the Python version required for your program, such as `3.10`.
 在**Enter the Python version**处，你需要填写你的程序所需的python版本号，例如3.10。

In the second field, **Enter the dependency's/dependencies' package name (separate by space)**, you need to enter the package names (not module names) of the dependencies required by your program. For example, if your program imports `cv2` and `numpy`, you should enter `opencv-python numpy` (`cv2` is a module name, while `opencv-python` is the package name). If no additional dependencies are needed, you can leave this field blank.
 在第二处**Enter the dependency's/dependencies' package name(separate by space):** 中你需要填写你的程序所需要的依赖项的包名（不是模块名），比如你的程序导入了`cv2`和`numpy`，那么你就应该添上`opencv-python numpy`  (`cv2`是模块名，`opencv-python`是包名)，如果没有需要额外安装的依赖项就不填。

### 4.What does those check boxes mean? 底部的单选框该怎么选？

The first check box, `Generates a single executable file`, determines whether the output will consist of a single `.exe` file. If not enable, the generated files will include the `.exe` file along with additional `.dll` dynamic link files. In this case, the program will only run if both the executable file and the dynamic link files are present. If enable, only a single `.exe` file will be generated, which can be executed directly without requiring any additional dynamic link files. It is highly recommended to select this option.
第一个单选框`Generates a single executable file`是指生成文件是不是只生成一个`.exe`文件，如果不选，生成的文件除了`.exe`还有其他`.dll`的动态链文件，只有动态链文件和可执行文件同时在时这个程序才能执行；如果勾选上，那么生成的文件中就会只有一个`.exe`文件，直接点击就可执行，不需要其他动态链，强烈建议勾选上。

The second check box, `Runs the program while opening a command line window`, means that when the generated executable file is opened, it will display a command line window. If your program does not have a GUI (such as `wx` or `Qt`) and includes interactive elements with the user (such as `input()`), it must be enabled.
第二个单选框`Runs the program while opening a command line window`是指生成的可执行文件打开后会显示命令行，如果你的程序没有GUI（比如`wx`或`Qt`），而且有与用户交互的部分（比如`input()`），就必须打开
![GUI_cmd](https://github.com/user-attachments/assets/4bc788b8-12c9-4d77-a350-dec603035672)

This is an example program that shows GUI and commmand line. Black part is command line, white part is GUI.
这个示例程序展现了GUI和命令行。黑色的部分就是命令行，白色的部分就是GUI。

### 5. What should I pay attention to at runtime? 运行时应该注意什么？

After clicking `Execute`, the program will automatically open **Anaconda Prompt** or **Anaconda Powershell Prompt**. You need to wait for a few seconds, and the program will input the commands automatically. Make sure to keep the command prompt window in focus and at the forefront during the process. You can exit when you see `Finsh packaging, you can exit right now!` on command line.
点击`Execute`后程序会自动打开**Anaconda Prompt** 或 **Anaconda Powershell Prompt**，你需要等几秒，程序便会自动输入命令。注意在运行过程中一定要把命令行放在最上层并在焦点上。当你看到`Finsh packaging, you can exit right now!`时即可退出![[runtime.png]]

### 6. Where is executable file? 可执行文件在哪里？
At this point, navigate to the location of your Python file, and you will see several new folders and files. The executable file will be located in the folder named `dist`.
此时打开你的python文件位置，你就会看到多了几个文件夹和文件，可执行文件就在叫做`dist`的文件夹中。
![folder](https://github.com/user-attachments/assets/6f04a9f9-a178-40ee-a0f2-1fb439199ddb)

---

## 5. Contribution 贡献

Contributions are welcome! Follow these steps:
欢迎贡献！请按照以下步骤操作：
 - 1. Fork project.
   Fork 项目。
 - 2. Create branch:
   创建分支：
 ```bash
 git checkout -b feature-name
```
- 3. Submit changes:
  提交更改：
```bash
git commit -m "Explain changes"
```
- 4. Push branch:
  推送分支：
```bash
git push orgin feature-name
```
- 5. Submit Pull Request.
  提交拉取请求。

---
## 6. License 证书

This project uses [MIT LICENSE](LICENSE).
本项目使用[MIT LICENSE](LICENSE)。

---
## 7. Contact information 联系方式

- Email: stanyin64@gmail.com
- GitHub: [@SomeB1ooody](https://github.com/SomeB1oody)
