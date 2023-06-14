# VBS-Macro-XOR-Generator

The `VBS-Macro-XOR-Generator` is a Python script designed to automate the process of shellcode generation, modification, and execution, specifically tailored for the Offensive Security Experienced Penetration Tester (OSEP) certification challenges and the final exam. This script greatly enhances the efficiency and speed of macro payload generation and delivery, thereby facilitating the process of exploiting a network during the exam.

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
cd OSEP-Shellcode-Generator
```

3. Run the script with the necessary arguments.

```sh
python3 vbs_macro_xor.py -lhost 10.10.10.10 -lport 4444
```

Replace `10.10.10.10` with your actual LHOST (Local Host) IP and `4444` with your desired LPORT (Local Port).

## Requirements

- Python 3.8 or higher
- Metasploit Framework
- Mono (for running the compiled C# executable)
- Git (for cloning the repository)
- A Kali Linux environment (or similar) is recommended, as the connection to the exam network is expected to be done with Kali Linux using OpenVPN【32†source】.

## Limitations

- This script is tailored for a Windows target, using a reverse HTTPS payload. 
- It is recommended to review and modify the script as necessary for different payload types or target systems.

## Contributing

Please fork the project, create a new branch, and submit a pull request. For major changes, please open an issue first to discuss the proposed change.

## License

This project is licensed under the MIT License.

## Disclaimer

This script is for educational purposes and preparing for the OSEP certification exam. It should only be used in environments where you have permission to perform penetration testing.
