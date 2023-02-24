# SSH Log Collector
This python program is designed to collect logs from remote network devices. The program uses the tkinter library for the graphical user interface (GUI) and the subprocess module to execute remote shell commands via SSH and SCP protocols.

### Description
The program consists of a GUI that allows users to input remote device IP addresses, select the types of logs to collect, and initiate the log collection process. The `command_execute()` function executes the remote shell commands to remove any existing log files on the remote device, compress the specified log files, and copy the compressed log files to the local device. The `commands_construct()` function constructs the shell commands to be executed by `command_execute()` based on the IP address of the remote device, the log file name, and the path to the log file on the remote device. The btn5_func() function is executed when the Collect Logs button is clicked, and it initiates the log collection process for all devices in the device list. The `threading_btn5()` function creates a new thread to run the `btn5_func()` function, allowing the GUI to remain responsive during the log collection process. The `threading_btn6()` function creates a new thread to run the `btn6_func()` function, allowing the GUI to remain responsive during the log file extraction process.

### Requirements
- `Python 3`
- `subprocess` module: used for launching and communicating with external processes.
- `os`: For creating directories using makedirs() and finding file paths using abspath(), exists(), join(), and dirname().
- `tkinter`: For the GUI of the program.
- `threading` module: used for creating and managing threads
- `bs4`: For parsing HTML files.
- `datetime` module: used for working with dates and times
- Remote device must be configured to accept SSH and SCP connections.

### Installation
- Download or clone the program files from the GitHub repository.
- Install the `tkinter` and `bs4` libraries by running `pip install tkinter` and `pip install bs4` in the command prompt or terminal.
- Configure the `conf directory` files, such as `usr.conf` (contains the username to access remote devices), `port.conf` (contains the SSH port number for remote devices), `data_path.conf` (contains the paths to the directories for log files to be stored), `ospf_ssh_private_key.ppk` (contains the publick private key to acces the remote host) and `EQPT.xml` (contains the IP addresses of remote devices).
- Ensure that plink.exe and psftp.exe files are present in the project directory. These files can be downloaded from the PuTTY [website](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
- Run the `SSH_Log_Collector.py` file using `python SSH_Log_Collector.py` command.

### Usage
1. Launch the `SSH_Log_Collector.py` file.
2. Enter the IP address of the remote device in the IP Address field or select the host from next field.
3. Click the Collect Logs button for desired logs to initiate the log collection process.
4. The log files will be stored in the project directory.

### Contributions
Contributions to this repo are welcome. If you find a bug or have a suggestion for improvement, please open an issue on the repository. If you would like to make changes to the code, feel free to submit a pull request.

### Acknowledgments
This program was created as a part of a programming challenge. Special thanks to the challenge organizers for the inspiration.
