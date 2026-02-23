#!/usr/bin/env python3
import sys
import os
import argparse

# Add lib directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

try:
    from lib.common import orchestra
except ImportError as e:
    print(f"[-] Error importing modules: {e}")
    print("[*] Make sure you're running from the GreatSCT directory")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='GreatSCT - Application Whitelisting Bypass Generator')
    
    # GreatSCT Options
    parser.add_argument('--update', action='store_true', help='Update the GreatSCT framework')
    parser.add_argument('--version', action='store_true', help='Displays version and quits')
    parser.add_argument('--list-tools', action='store_true', help="List GreatSCT's tools")
    parser.add_argument('-t', '--tool', metavar='Bypass', help='Specify GreatSCT tool to use')
    
    # Callback Settings
    parser.add_argument('--ip', '--domain', dest='ip', help='IP Address to connect back to')
    parser.add_argument('--port', type=int, help='Port number to connect to')
    
    # Payload Settings
    parser.add_argument('--list-payloads', action='store_true', help='Lists all available payloads for that tool')
    parser.add_argument('--generate-awl', action='store_true', help='Generate all bypasses in the framework')
    
    # Great Scott Options
    parser.add_argument('-c', nargs='+', metavar='OPTION=value', help='Custom payload module options')
    parser.add_argument('-o', '--output', metavar='OUTPUT NAME', help='Output file base name')
    parser.add_argument('-p', '--payload', metavar='PAYLOAD', nargs='?', const='list', help='Payload to generate. Lists payloads if none specified')
    parser.add_argument('--clean', action='store_true', help='Clean out payload folders')
    parser.add_argument('--msfoptions', nargs='+', metavar='OPTION=value', help='Options for the specified metasploit payload')
    parser.add_argument('--msfvenom', metavar='windows/meterpreter/reverse_tcp', nargs='?', const='windows/meterpreter/reverse_tcp', help='Metasploit shellcode to generate')
    
    args = parser.parse_args()
    
    # Create conductor and run
    the_conductor = orchestra.Conductor(args)
    the_conductor.run()

if __name__ == "__main__":
    main()
