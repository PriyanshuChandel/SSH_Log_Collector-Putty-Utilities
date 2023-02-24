from subprocess import Popen, PIPE
from os import makedirs
from os.path import abspath, exists, join, dirname
from tkinter import Tk, Label, Entry, Button, Checkbutton, IntVar, StringVar, Frame
from tkinter.scrolledtext import ScrolledText
from threading import Thread
from bs4 import BeautifulSoup
from datetime import datetime

Icon_File = join(dirname(__file__), 'icon.ico')
Plink_File = join(dirname(__file__), 'plink.exe')
Psftp_File = join(dirname(__file__), 'psftp.exe')
My_Key = abspath('conf/ospf_ssh_private_key.ppk')
Data_Path = 'conf/data_path.conf'
Eqpt_XML = 'conf/EQPT.xml'
User_Detail = 'conf/usr.conf'
Port_Detail = 'conf/port.conf'

Basic_Log_Path = open(Data_Path, "r").readlines()[0].split(' = ')[1].strip()
Sys_Log_Path = open(Data_Path, "r").readlines()[1].split(' = ')[1].strip()

window = Tk()
window.config(bg='grey')
window.title('LLC - Developed by Priyanshu')
window.minsize(width=426, height=475)
window.maxsize(width=426, height=475)
window.iconbitmap(Icon_File)
window.resizable(False, False)

if not exists('log'):
    makedirs('log')
file_handler = open(f"log/logs_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", 'a')


def command_execute(command1, command2, command3, command4, host_name, log_name):
    sp1 = Popen(command1, stdout=PIPE, stderr=PIPE, shell=True)
    output1 = sp1.stdout.read().decode().strip()
    error1 = sp1.stderr.read().decode().strip()
    if len(output1) != 0 or len(error1) != 0:
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Output {host_name} <ZIP_REMOVE> {output1}\n')
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Error {host_name} <ZIP_REMOVE> {error1}\n')
    sp2 = Popen(command2, stdout=PIPE, stderr=PIPE, shell=True)
    output2 = sp2.stdout.read().decode().strip()
    error2 = sp2.stderr.read().decode().strip()
    if len(output2) != 0 or len(error2) != 0:
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Output {host_name} <ZIPPING> {output2}\n')
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Error {host_name} <ZIPPING> {error2}\n')
    sp3 = Popen(command3, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    sp3.stdin.write(command4)
    sp3.stdin.close()
    output3 = sp3.stdout.read().strip()
    error3 = sp3.stderr.read().strip()
    if len(output3) == 0 or len(error3) > 28:
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Output {host_name} <GETTING ZIP> {output3}\n')
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Error {host_name} <GETTING ZIP> {error3}\n')
    else:
        file_handler.write(
            f"{datetime.now().replace(microsecond=0)} {log_name.split('_')[0]} log collected for {host_name}.\n")


def commands_construct(ip, log_name, log_path, host_name):
    User_Name = open(User_Detail, "r").readline()
    Port = int(open(Port_Detail, "r").readline())
    existing_file_remove = f'{Plink_File} -batch -ssh {ip} -l {User_Name} -i {My_Key} -P {Port} "rm -f ' \
                           f'/tmp/{log_name}.zip"'
    zip_basic_logs = f'{Plink_File} -batch -ssh {ip} -l {User_Name} -i {My_Key} -P {Port} "zip -q -r -o ' \
                     f'/tmp/{log_name}.zip {log_path}"'
    basic_log_copy_psftp_1 = f'{Psftp_File} {User_Name}@{ip} -i {My_Key} -P {Port}'
    basic_log_copy_psftp_2 = f'get /tmp/{log_name}.zip'
    command_execute(existing_file_remove, zip_basic_logs, basic_log_copy_psftp_1, basic_log_copy_psftp_2, host_name,
                    log_name)


def threading_btn5():
    thread_btn5 = Thread(target=btn5_func)
    thread_btn5.start()


def btn5_func():
    labl10.config(text='Logs collection started...')
    try:
        for ip in ip_list:
            host_name = {v: k for k, v in eqpt_dict.items()}.get(ip)
            log_name = f'Basic_Logs_{host_name}'
            commands_construct(ip, log_name, Basic_Log_Path, host_name)
    except Exception as e:
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Error <FUNCTIONAL> {e}\n')
    labl10.config(text='Logs collection completed, check logs file for status.')

def threading_btn6():
    thread_btn6 = Thread(target=btn6_func)
    thread_btn6.start()


def btn6_func():
    labl10.config(text='Logs collection started...')
    try:
        for ip in ip_list:
            host_name = {v: k for k, v in eqpt_dict.items()}.get(ip)
            log_name = f'Sys_Logs_{host_name}'
            commands_construct(ip, log_name, Sys_Log_Path, host_name)
    except Exception as e:
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Error <FUNCTIONAL> {e}\n')
    labl10.config(text='Logs collection completed, check logs file for status.')

def threading_btn7():
    thread_btn4 = Thread(target=btn7_func)
    thread_btn4.start()


def btn7_func():
    labl10.config(text='Logs collection started...')
    Copy_From = str(ent7.get())
    try:
        for ip in ip_list:
            host_name = {v: k for k, v in eqpt_dict.items()}.get(ip)
            log_name = f'Additional_Logs_{host_name}'
            commands_construct(ip, log_name, Copy_From, host_name)
    except Exception as e:
        file_handler.write(f'{datetime.now().replace(microsecond=0)} Error <FUNCTIONAL> {e}\n')
    labl10.config(text='Logs collection completed, check logs file for status.')

labl1 = Label(window, text='Log Collection', font=(None, 12, 'bold'), bg='grey').place(x=145, y=1)
lab2 = Label(window, text='Enter IP address of host (press spacebar to enter)', wraplength=170, justify='left',
             font=(None, 8, 'bold'), bg='grey').place(x=6, y=26)
stringvar_2 = StringVar()


def add_additional_ip(self):
    if not len(stringvar_2.get()) == 0:
        eqpt_dict['Additional_Host'] = stringvar_2.get()
        var_dict['Additional_Host'] = IntVar(value=1)
        ip_list.append(eqpt_dict.get('Additional_Host'))
    if len(stringvar_2.get()) == 0:
        ip_list.remove(eqpt_dict.get('Additional_Host'))
        eqpt_dict.pop('Additional_Host')
        var_dict.pop('Additional_Host')


ent2 = Entry(window, bd=4, width=32, bg='lavender', textvariable=stringvar_2)
ent2.place(x=153, y=30)
ent2.bind("<space>", add_additional_ip)
lab3 = Label(window, text='OR', font=(None, 9, 'bold'), bg='grey').place(x=380, y=31)
labl4 = Label(window, text='Select host from below', font=(None, 9, 'bold'), bg='grey').place(x=150, y=60)
text4 = ScrolledText(window, width=14, height=12, bg='white', bd=4)
text4.place(x=145, y=80)
eqpt_dict = dict()
for eqpt, ip in zip(BeautifulSoup(open(Eqpt_XML).read(), 'xml')('equipment'),
                    BeautifulSoup(open(Eqpt_XML).read(), 'xml').findAll('ip')):
    eqpt_dict[eqpt.get('Name')] = ip.text
ip_list = list()


def checkbox_command():
    global ip_list
    ip_list = [eqpt_dict[key] for key in eqpt_dict.keys() if var_dict[key].get() == 1]


var_dict = dict()
for eqpts in eqpt_dict.keys():
    var_dict[eqpts] = IntVar(value=0)
    checkbutton4 = Checkbutton(text4, text=eqpts, variable=var_dict[eqpts], onvalue=1, offvalue=0, bg='white',
                               cursor="hand2", command=checkbox_command)
    checkbutton4.pack()
    text4.window_create('end', window=checkbutton4)


labl5 = Label(window, text='Click here if you want to collect basic logs from </data/logs/>',
              font=(None, 9, 'bold'), bg='grey').place(x=6, y=290)
btn5 = Button(window, text='Pack', command=threading_btn5, bg='green')
btn5.place(x=380, y=288)

labl6 = Label(window, text='Click here if you want to collect syslog from </var/log/>', font=(None, 9, 'bold'),
              bg='grey').place(x=6, y=320)
btn6 = Button(window, text='Pack', command=threading_btn6, bg='green')
btn6.place(x=380, y=318)

labl7 = Label(window, text='Specify directory to collect anything else', font=(None, 9, 'bold'), bg='grey',
              wraplength=178, justify='left').place(x=6, y=350)
ent7 = Entry(window, bd=4, width=32, bg='lavender')
ent7.place(x=167, y=354)
btn7 = Button(window, text='Pack', command=threading_btn7, bg='green')
btn7.place(x=380, y=354)

labl8 = Label(window, text='Note: This option depends on the permissions', font=(None, 9, 'bold'), bg='grey')
labl8.place(x=6, y=384)

frame9 = Frame(window, bg="white", bd=20, width=410,
               height=60, cursor="target").place(x=6, y=406)
labl9 = Label(frame9, text='Status:', font=(None, 9, 'bold'), bg='white')
labl9.place(x=6, y=406)

labl10 = Label(window, font=(None, 9, 'bold'), bg='white', wraplength=300, justify='left')
labl10.place(x=6, y=426)

window.mainloop()