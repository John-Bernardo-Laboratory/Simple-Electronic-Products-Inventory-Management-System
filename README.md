# Simple Electronic Products Inventory Management System

## Overview

This project is a Python-based application for managing electronic products in an inventory. It uses Tkinter for the GUI and SQLite for database operations.

## Installation Instructions

### 1. Install Python

1. Download Python from the official website: [Python Downloads](https://www.python.org/downloads/)
2. Run the installer and make sure to check the box for "Add Python to PATH" before clicking "Install Now."
3. Verify the installation by opening a command prompt or terminal and typing:
   
   ```bash
   python --version
   ```
   
### 2. Install Visual Studio Code (VSCode)

1. **Download VSCode**: 
   - Go to [VSCode Downloads](https://code.visualstudio.com/Download) and download the installer for your operating system.

2. **Run the Installer**: 
   - Follow the on-screen instructions to complete the installation.

3. **Launch VSCode**: 
   - Open VSCode from your application menu or desktop shortcut.

### 3. Set Up VSCode for Python Development

1. **Install Python Extension for VSCode**:
   - Open VSCode.
   - Press `Ctrl+Shift+X` to open the Extensions view.
   - Search for "Python" in the search bar.
   - Click on the extension named **Python** by Microsoft and click **Install**.

2. **Install Code Runner Extension** (Optional but useful for running code snippets):
   - Open VSCode.
   - Press `Ctrl+Shift+X` to open the Extensions view.
   - Search for "Code Runner" in the search bar.
   - Click on the extension named **Code Runner** by Jun Han and click **Install**.
   - This extension allows you to quickly run code snippets by pressing `Ctrl+Alt+N` or using the Run icon in the top right of the editor.

3. **Install the Libraries**:
   - Open a terminal or command prompt.
   - Run the following command to install the libraries:

     ```bash
     pip install pillow ttkthemes
     ```
4. **Open Your Project Folder**:
   - Click on `File` > `Open Folder...`.
   - Navigate to and select the folder containing your project files.

5. **Test the Program**:
   - In VSCode, open the main Python script (e.g., `GUI.py`).
   - To run the script, you can either press `F5` to start debugging or use `Ctrl+Alt+N` if you have Code Runner installed.
   - Ensure the program runs correctly and performs as expected.

## Creating a Standalone Executable

To package your application as a standalone executable, follow these steps:

1. **Install PyInstaller**:
   - Open a terminal or command prompt.
   - Install PyInstaller using pip:

     ```bash
     pip install pyinstaller
     ```

2. **Create the Executable**:
   - In the VSCode terminal, run the following command to generate an executable file for Windows:

     ```bash
     pyinstaller --onefile --icon=icon.ico --add-data "icon.ico;." --add-data "logo.png;." --add-data "database.db;." --noconsole GUI.py
     ```

   - **Explanation of Flags**:
     - `--onefile`: Bundles everything into a single executable file.
     - `--icon=icon.ico`: Specifies the icon for the executable.
     - `--add-data "icon.ico;."`: Includes additional files (`icon.ico` in this case) with the executable.
     - `--add-data "logo.png;."`: Includes the `logo.png` file.
     - `--add-data "database.db;."`: Includes the `database.db` file.
     - `--noconsole`: Hides the console window when running the GUI application.
     - `GUI.py`: The main script file for your application.

3. **Locate the Executable**:
   - After running the PyInstaller command, you can find the standalone executable in the `dist` directory within your project folder.
   - To ensure the software runs properly, copy the `icon.ico`, `logo.png`, and `database.db` files into the `dist` directory. These files are needed for the application to function correctly.

4. **Distribute Your Application**:
   - You can now distribute the executable file to others, who will be able to run the application without needing to install Python or the required libraries.
