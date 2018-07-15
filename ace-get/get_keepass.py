import time,subprocess,pyperclip
import win32com.client as comclt

def get_keepass(name):
    subprocess.call(r"C:\Program Files (x86)\KeePass Password Safe 2\KeePass.exe")
    time.sleep(0.2)
    for command in [name,'{ENTER}','^c']:
        comclt.Dispatch("WScript.Shell").SendKeys(command)
        time.sleep(0.2)
    return pyperclip.paste()
	
# print(get_keepass('DAS'))