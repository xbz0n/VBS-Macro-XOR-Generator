# VBS-Macro-XOR-Generator "VBS_X0rG3n"

The `VBS_X0rG3n` is a Python script designed to automate the process of XOR+Ceasar macros encrypted shellcode. It uses C# based shellcode encoder that performs two types of encoding on the input shellcode. This tool can be used to modify shellcode in preparation for use in penetration testing scenarios, such as those encountered in the Offensive Security Experienced Penetration Tester (OSEP) exam and its associated challenges.

## Short Description

This C# program takes an input shellcode (which is expected to be replaced in the `buf` variable within the code), performs two encoding steps, and then writes the encoded shellcode to a file named "encoded_shellcode.txt". The two encoding steps are:

1. **Additive encoding**: Each byte of the input shellcode is incremented by 2.
2. **XOR encoding**: Each byte of the shellcode (after the first encoding step) is XOR'd with 0xFA.

The tool also formats the encoded shellcode in a readable format (with a new line inserted every 50 bytes) before writing it to the file.

After the encoded shellcode is written to the file, the program also reads the content of the "encoded_shellcode.txt" file and prints it to the console.



## Note

This tool is intended for educational and legitimate penetration testing purposes. It should not be used for illegal activities. Use responsibly and ensure you have proper authorization before using this tool in any network or system.

## What the Script Does

1. Parses the provided command-line arguments for the LHOST and LPORT values.

2. Generates the shellcode using msfvenom with the provided LHOST and LPORT, specifying a reverse HTTPS payload for a windows target. This shellcode is saved to a file named `vbs.txt`.

3. Reads the shellcode from `vbs.txt` and a helper C# file named `VBS-Helper.cs`.

4. Replaces the placeholder `!!!SHELLCODE!!!` in the helper C# file with the shellcode read from `vbs.txt`. 

5. Writes the modified C# code to a new file named `VBS-Helper_modified.cs`.

6. Compiles the modified C# file into a Windows executable named `VBS-Helper.exe`.

7. Runs the newly compiled `VBS-Helper.exe` program using mono, which generates `encoded_shellcode.txt`.

8. Reads the content of `encoded_shellcode.txt` and `macros.txt`.

9. Replaces the `!!!ENCRYPTEDSHELLCODE!!!` placeholder in `macros.txt` with the encoded shellcode read from `encoded_shellcode.txt`.

10. Writes the modified macro content to a new file named `macro_encrypted.txt`.

11. Creates a `met64.rc` file with necessary commands to set up the Metasploit handler for the generated payload.

By executing these steps, the script automates the process of creating a macros payload, inserting it into a helper file, executing the file to get encoded shellcode, and preparing the shellcode for use within a macro, all while setting up the corresponding Metasploit handler. This automation is invaluable for efficiently completing OSEP challenges and the exam.


## How to Use

1. Clone the repository to your local machine.

```sh
git clone https://github.com/username/VBS-Macro-XOR-Generator.git
```

2. Navigate into the repository directory.

```sh
cd VBS-Macro-XOR-Generator
```

3. Run the script with the necessary arguments.

```sh
python3 VBS_X0rG3n.py --LHOST 10.10.10.10 --LPORT 4444
```

Replace `10.10.10.10` with your actual LHOST (Local Host) IP and `4444` with your desired LPORT (Local Port).

## Requirements

- Python 3.8 or higher
- Metasploit Framework
- Mono (for running the compiled C# executable) (mono-devel in kali)
- Git (for cloning the repository)


## Limitations

- This script is tailored for a Windows target, using a reverse HTTPS payload. 
- It is recommended to review and modify the script as necessary for different payload types or target systems.

## Contributing

Please fork the project, create a new branch, and submit a pull request. For major changes, please open an issue first to discuss the proposed change.

## License

This project is licensed under the MIT License.

## Disclaimer

This script is for educational purposes and preparing for the OSEP certification exam. It should only be used in environments where you have permission to perform penetration testing.
