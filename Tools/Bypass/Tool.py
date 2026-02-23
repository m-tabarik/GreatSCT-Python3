import os
import sys
import importlib.util

class Tool:
    def __init__(self):
        self.name = "GreatSCT Bypass Tool"
        self.description = "Application Whitelisting Bypass Tool"
        self.payloads = {}
        self.cli_options = None
        self.load_payload()
        
    def load_payload(self):
        """Load available payloads"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        payloads_dir = os.path.join(base_dir, "Payloads")
        
        print("[*] Loading payloads from: {}".format(payloads_dir))
        
        if os.path.exists(payloads_dir):
            for root, dirs, files in os.walk(payloads_dir):
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        full_path = os.path.join(root, file)
                        # Get relative path from payloads_dir
                        rel_path = os.path.relpath(full_path, payloads_dir)
                        # Convert to module format (remove .py, replace slashes with dots)
                        module_name = rel_path.replace('.py', '').replace('/', '.')
                        self.payloads[module_name] = full_path
                        print("[+] Loaded payload: {}".format(module_name))
        else:
            print("[-] Payloads directory not found: {}".format(payloads_dir))
            
    def list_payloads(self):
        """List available payloads"""
        print("\n[*] Available payloads for {}:".format(self.name))
        if not self.payloads:
            print("    No payloads found")
            return
            
        for payload_name in sorted(self.payloads.keys()):
            print("    - {}".format(payload_name))
            
    def generate(self, payload_name, lhost, lport, output_name):
        """Generate the payload"""
        print("\n[*] Generating payload...")
        print("[*] Payload: {}".format(payload_name))
        print("[*] LHOST: {}".format(lhost))
        print("[*] LPORT: {}".format(lport))
        print("[*] Output: {}".format(output_name))
        
        if payload_name in self.payloads:
            payload_path = self.payloads[payload_name]
            
            try:
                # Load the payload module
                spec = importlib.util.spec_from_file_location("payload_module", payload_path)
                payload_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(payload_module)
                
                # Check if the payload has a main function
                if hasattr(payload_module, 'main'):
                    # Call the payload's main function
                    result = payload_module.main(lhost, lport, output_name)
                    
                    # Check where the output might be
                    possible_paths = [
                        "/usr/share/greatsct-output/compiled/{}.exe".format(output_name),
                        "/usr/share/greatsct-output/compiled/{}.dll".format(output_name),
                        "/root/greatsct-output/compiled/{}.exe".format(output_name),
                        "/root/greatsct-output/compiled/{}.dll".format(output_name),
                        os.path.join(os.getcwd(), "output", "{}.exe".format(output_name)),
                        os.path.join(os.getcwd(), "{}.exe".format(output_name)),
                        os.path.join(os.getcwd(), "{}.dll".format(output_name))
                    ]
                    
                    found = False
                    for path in possible_paths:
                        if os.path.exists(path):
                            print("\n[+] Payload generated successfully!")
                            print("[+] File saved to: {}".format(path))
                            found = True
                            break
                    
                    if not found:
                        print("\n[+] Payload generated but location unknown")
                        print("[*] Check /usr/share/greatsct-output/compiled/")
                        
                else:
                    print("[-] Payload module has no main function")
                    
                    # Try to see what functions it does have
                    functions = [f for f in dir(payload_module) if not f.startswith('__')]
                    print("[*] Available functions in payload: {}".format(functions))
                    
            except Exception as e:
                print("[-] Error generating payload: {}".format(e))
                import traceback
                traceback.print_exc()
        else:
            print("[-] Payload '{}' not found".format(payload_name))
            self.list_payloads()
            
    def execute(self):
        """Execute the tool with CLI options"""
        print("[*] Executing tool with CLI options")
        if self.cli_options:
            if hasattr(self.cli_options, 'list_payloads') and self.cli_options.list_payloads:
                self.list_payloads()
            elif hasattr(self.cli_options, 'payload') and self.cli_options.payload:
                if self.cli_options.payload == 'list':
                    self.list_payloads()
                else:
                    self.generate(
                        self.cli_options.payload,
                        self.cli_options.ip,
                        self.cli_options.port,
                        self.cli_options.output
                    )
            else:
                print("[-] No payload specified")
                self.list_payloads()
        else:
            self.interactive()
            
    def interactive(self):
        """Interactive mode"""
        print("\n" + "="*60)
        print("{} - Interactive Mode".format(self.name))
        print("="*60)
        
        while True:
            print("\nOptions:")
            print("  1. List payloads")
            print("  2. Generate payload")
            print("  3. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "1":
                self.list_payloads()
            elif choice == "2":
                self.list_payloads()
                payload = input("\nEnter payload name: ").strip()
                lhost = input("Enter LHOST: ").strip()
                lport = input("Enter LPORT: ").strip()
                output = input("Enter output name: ").strip()
                self.generate(payload, lhost, lport, output)
            elif choice == "3":
                break
            else:
                print("[-] Invalid choice")
