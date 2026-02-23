import os
import sys
import importlib.util

sys.path.append(os.path.abspath('lib'))
from lib.common import helpers

class Conductor:
    def __init__(self, cli_args):
        self.cli_args = cli_args
        self.tools = {}
        self.load_tools()
        
    def load_tools(self):
        tools_dir = "Tools/Bypass"
        if not os.path.exists(tools_dir):
            print(f"[-] Tools directory not found: {tools_dir}")
            return
            
        for tool_file in os.listdir(tools_dir):
            if tool_file.endswith(".py") and tool_file != "__init__.py":
                tool_name = tool_file[:-3]
                tool_path = os.path.join(tools_dir, tool_file)
                
                try:
                    spec = importlib.util.spec_from_file_location(tool_name, tool_path)
                    loaded_tool = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(loaded_tool)
                    self.tools[tool_name] = loaded_tool
                    print(f"[+] Loaded tool: {tool_name}")
                except Exception as e:
                    print(f"[-] Failed to load {tool_name}: {e}")
                    
    def list_tools(self):
        """List available tools"""
        print("\n[*] Available tools:")
        if not self.tools:
            print("    No tools found")
        else:
            for tool_name in self.tools.keys():
                print(f"    - {tool_name}")
                
    def list_payloads(self):
        """List payloads for the specified tool"""
        if hasattr(self.cli_args, 'tool') and self.cli_args.tool:
            tool_name = self.cli_args.tool
            if tool_name in self.tools:
                tool_module = self.tools[tool_name]
                if hasattr(tool_module, 'Tool'):
                    tool_instance = tool_module.Tool()
                    tool_instance.list_payloads()
                else:
                    print(f"[-] Tool {tool_name} has no Tool class")
            else:
                print(f"[-] Tool {tool_name} not found")
                self.list_tools()
        else:
            # If no tool specified, list payloads for all tools
            for tool_name, tool_module in self.tools.items():
                if hasattr(tool_module, 'Tool'):
                    print(f"\n[*] Payloads for {tool_name}:")
                    tool_instance = tool_module.Tool()
                    tool_instance.list_payloads()
                
    def command_line_use(self):
        """Handle command line usage"""
        if self.cli_args.tool:
            tool_name = self.cli_args.tool
            if tool_name in self.tools:
                tool_module = self.tools[tool_name]
                if hasattr(tool_module, 'Tool'):
                    tool_instance = tool_module.Tool()
                    tool_instance.cli_options = self.cli_args
                    
                    # Check if we're just listing payloads
                    if hasattr(self.cli_args, 'list_payloads') and self.cli_args.list_payloads:
                        tool_instance.list_payloads()
                    # Generate payload
                    elif hasattr(self.cli_args, 'payload') and self.cli_args.payload:
                        tool_instance.generate(
                            self.cli_args.payload,
                            self.cli_args.ip,
                            self.cli_args.port,
                            self.cli_args.output
                        )
                    else:
                        print("[-] No payload specified")
                        tool_instance.list_payloads()
                else:
                    print(f"[-] Tool {tool_name} has no Tool class")
            else:
                print(f"[-] Tool {tool_name} not found")
                self.list_tools()
        else:
            self.interactive_menu()
            
    def interactive_menu(self):
        """Display interactive menu"""
        print("\n" + "="*80)
        print("GreatSCT - Interactive Mode")
        print("="*80)
        print("\n[*] Available tools:")
        tools_list = list(self.tools.keys())
        for i, tool_name in enumerate(tools_list, 1):
            print(f"  {i}. {tool_name}")
        print("\nCommands: exit, info <tool>, use <tool>")
        
        while True:
            cmd = input("\nGreatSCT > ").strip().lower()
            if cmd == "exit":
                break
            elif cmd.startswith("use "):
                tool_name = cmd[4:].strip()
                if tool_name in self.tools:
                    self.use_tool(tool_name)
                else:
                    print(f"[-] Tool {tool_name} not found")
            elif cmd.startswith("info "):
                tool_name = cmd[5:].strip()
                if tool_name in self.tools:
                    self.show_tool_info(tool_name)
                else:
                    print(f"[-] Tool {tool_name} not found")
            else:
                print("Unknown command")
                
    def use_tool(self, tool_name):
        """Use a specific tool interactively"""
        tool_module = self.tools[tool_name]
        if hasattr(tool_module, 'Tool'):
            tool_instance = tool_module.Tool()
            tool_instance.interactive()
        else:
            print(f"[-] Tool {tool_name} has no Tool class")
            
    def show_tool_info(self, tool_name):
        """Show information about a tool"""
        tool_module = self.tools[tool_name]
        if hasattr(tool_module, 'Tool'):
            tool_instance = tool_module.Tool()
            print(f"\n[*] Tool: {tool_name}")
            print(f"[*] Description: {tool_instance.description if hasattr(tool_instance, 'description') else 'N/A'}")
        else:
            print(f"[-] Tool {tool_name} has no Tool class")
                
    def run(self):
        """Main entry point"""
        if hasattr(self.cli_args, 'list_tools') and self.cli_args.list_tools:
            self.list_tools()
        elif hasattr(self.cli_args, 'list_payloads') and self.cli_args.list_payloads:
            self.list_payloads()
        elif hasattr(self.cli_args, 'tool') and self.cli_args.tool:
            self.command_line_use()
        else:
            self.interactive_menu()
