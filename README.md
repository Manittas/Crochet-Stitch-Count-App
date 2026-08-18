<h1 align="center">Crochet Stitch Count - v0.1</h1>

A lightweight desktop application for tracking crochet stitch counts across multiple rows.

The application was developed in **Python** using **Tkinter**, with a modular architecture separating application logic, data persistence, UI rendering, and utility functionality.

---

# Future Improvements

with future releases, the improvements are aiming to include:

- Voice activated count.
- UI redesign/refinement.
- Additional Piece object with a row counter.
- Project object containing Pieces and Rows.

---

## Features for version v0.1

### Stitch Counting

- Increment the stitch count of the current row. Can be done both by pressing the `Add` button or the `e` key.
- Decrement the stitch count when applicable. Can be done both by pressing the `Sub` button or the `q` key. Rows cannot be decremented below the value 0.
- Reset the current stitch count of a row to 0. Can be done by pressing the `r` key.
- Manually set the stitch count to a specific value. Can be done by pressing the `Set` button, which will show an input box. In that input box, the desired value can be added as long as it is a non negative number. The stitch count will be updated with this value once the user clicks the `ENTER` key. To close the input box, simply click the `Set` button again.
- Display the current stitch count directly in the main window and automatically update the UI when the current row changes.

### Row Management

- Create new crochet rows. Can be done both by pressing the `New` button or the `n` key. This will show a "New Row" popup requiring the user to set a unique name for the row. If no unique name is given, it automatically generate unique names for rows in the same way of the *Windows* file system.
- Keep track of multiple rows simultaneously.
- Switch between existing rows. Can be done both by pressing the "burger" button on the top right or the `m` key. This will show a "Select Row" popup, in case more than 1 row exists, requiring the user to select the desired row.
- Delete rows.
- Prevent the application from deleting the final remaining row and automatically select another row when the current row is deleted.

### Row Selection

The application provides a dedicated row-selection popup.

- Display all existing rows in a scrollable list.
- Select a row by clicking on its name.
- Delete rows directly from the selection popup by clicking the "Trash" button in front of the row.

### Persistent Data

To save your Row data, simpy click the `Save` button or the `s` key. Row data is stored locally so that application state can be restored between sessions.

The application supports:

- Saving row information.
- Loading previously saved rows.

Data persistence is handled separately from the application logic through a dedicated storage service.

### Error Logging

The application includes a dedicated logging service for error handling.

- Support logging both handled and unhandled exceptions.
- Automatically create the `logs` directory when necessary.
- Save complete exception tracebacks in a dedicated log file for each error.
- Include timestamps in log filenames.

### Graphical User Interface

The application uses Tkinter to provide a desktop graphical interface.

---

<h1 align="center">Setup & Build Guide</h1>

This section explains how to run the Crochet Stitch Count application by building a standalone executable for **Windows** or **macOS**.

### Application Builder

The repository also contains a custom build system for creating standalone applications.

The builder is separate from the application itself and is located in `builder/`. It provides platform-specific build scripts for:

- Windows
- macOS

# Technologies

The project is built using:

- **Python**
- **Tkinter**
- **PyInstaller**
- **JSON** for persistent application data

---

# Building the Application

The repository contains platform-specific build scripts:

    builder/
    ├── build.bat
    └── build.command

The build scripts automatically:

1. Check whether Python is installed.
2. Check whether PyInstaller is installed.
3. Install PyInstaller if necessary.
4. Validate the required project files.
5. Remove previous build files.
6. Build the standalone application.

# Requirements

- Python 3

PyInstaller does not need to be installed manually. The build scripts check for it and install it if necessary.

---

# Windows Build

From Windows, double-click:

    builder/build.bat

The script will create:

    dist/StitchCount.exe

The resulting `StitchCount.exe` can be run without manually starting the Python application.

---

# macOS Build

In the macOS, double-click the build script file in Finder:

    builder/build.command

If necessary, make the script executable on Terminal and/or double-click with:

    chmod +x builder/build.command

The resulting application will be created in:

    dist/StitchCount.app

---

# Notes

- The Windows and macOS applications must be built separately.
- The build scripts are located in the `builder` directory.
- PyInstaller is used to package the Python application.
- The source code remains available in the repository for development and portfolio purposes.
- The macOS build must be performed on a Mac.
- The Windows build must be performed on Windows.