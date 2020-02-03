import os
import ctypes, sys

# Enable the Developer mode to modify the script, without effecting your operating systems lookup tables.
_dev = False

def clear():
    if sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')

def is_admin(retry = False):
    if sys.platform == "win32":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            if (retry):
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    return False

def DNSExists(lines, needle):
    for line in lines:
        line = str(line)
        if (line.startswith('#')):
            continue # We can ignore this, since it's already marked non-usable!
        args = line.split(' ')
        _direction = str(args[0])
        if (len(args) > 1):
            _fulldomain = str(args[1]).split('.')
            if ('.'.join(_fulldomain).find(needle) != -1):
                return True
    return False
    
if __name__ == "__main__":
    if _dev:
        _hostfile = "./hostname-test.txt"
    else:
        _hostfile = "C:/Windows/System32/drivers/etc/hosts"

    while(True):
        if not _dev:
            if is_admin(True):
                pass
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                print("Accessiblity problem, exit and elevate UAC access!")
                break

        _in = input('Enter help for information or quit to exit the program: ')
        if (_in.lower() == 'x' or _in.lower() == 'quit'):
            break

        if (_in.lower() == 'add'):
            _domain = input('Enter Domain name: ')
            _subdomain = input('Enter Subdomain name: ')
            _direction = input('Enter Direction Address(127.0.0.1): ')

            if (_direction.replace(' ', '') == ''): # Set default direction address...
                _direction = '127.0.0.1'
            while (_domain.replace(' ', '') == ''):
                print('Domain is empty, it must have something!')
                _domain = input('Enter Domain name: ')
            
            _fulldomain = ('' if _subdomain.replace(' ', '') == '' else _subdomain.replace(' ', '') + '.') + _domain.replace(' ', '')
            
            f=open(_hostfile, "a+")
            fread=open(_hostfile, "r")

            if not DNSExists(fread.readlines(), (_subdomain + '.' if _subdomain.replace(' ', '') != "" else '') + _domain):
                f.write(_direction.replace(' ', '').replace(',', '.') + " " + _fulldomain + " \n")
            else:
                print("`"+ (_subdomain + '.' if _subdomain.replace(' ', '') != "" else '') + _domain +"` already exists!")
            
            fread.close()
            f.close()
        elif (_in.lower() == 'remove'):
            _Searchdomain = input('Enter Domain name: ')

            fread=open(_hostfile, 'r')

            lines = fread.readlines()

            fwriter = open(_hostfile, 'w')

            final = []
            for line in lines:
                line = str(line)
                if (line.startswith('#')):
                    continue # We can ignore this, since it's already marked non-usable!
                args = line.split(' ')
                _direction = str(args[0])
                if (len(args) > 1):
                    _fulldomain = str(args[1]).split('.')
                    print('.'.join(_fulldomain))
                    if ('.'.join(_fulldomain).find('friendlybots') != -1):
                        print("Removing `"+ '.'.join(_fulldomain) +"` from the Local DNS Lookup Table...")
                    else:
                        final.append(line)

            fwriter.writelines(final)

            fread.close()
            fwriter.close()
        elif (_in.lower() == 'list'):
            print(":: [Hostname Manager - List Local DNS] ::")
            fread=open(_hostfile, 'r')

            lines = fread.readlines()

            for line in lines:
                line = str(line)
                if (line.startswith('#')):
                    continue # We can ignore this, since it's already marked non-usable!
                args = line.split(' ')
                _direction = str(args[0])
                if (len(args) > 1):
                    _fulldomain = str(args[1]).split('.')
                    _subdomain = str(_fulldomain[0]) if len(_fulldomain) > 2 else ''
                    _domain = str(_fulldomain[1]) if len(_fulldomain) > 2 else str(_fulldomain[0])
                    print('.'.join(_fulldomain) + " -> " + _direction)
            fread.close()
        elif (_in.lower() == 'clear'):
            clear()
        elif (_in.lower() == 'dev' or _in.lower() == 'prod'):
            _dev = True if _in.lower() == 'dev' else False
            if _dev:
                print("Development Mode Enabled!")
                _hostfile = "./hostname-test.txt"
            else:
                print("Development Mode Disabled!")
                _hostfile = "C:/Windows/System32/drivers/etc/hosts"
            
        else:
            if (_in.lower() != 'help'):
                print("Invalid command `"+ _in.lower() +"`")
            print(":: [Hostname Manager - Help] ::")
            print("==================================")
            print("add - Adds a new Local DNS Route.")
            print("remove - Removes a Local DNS Route.")
            print("list - Lists all the Local DNS Routes.")
            print("clear - Clears the Screen.")
            print("dev/prod - Enable/Disable developer mode while live. [This doesn't live update the script...]")
            print("quit or x - To close the application without false-errors.")


