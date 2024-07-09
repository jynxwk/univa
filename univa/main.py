import inspect
from functools import wraps
from .command import Command

class Univa:
    def __init__(self, debug=False, prompt="> "):
        """
        Initialize Univa

        :param debug: Enable debug mode
        :param prompt: Prompt to display before each command
        """
        self.debug = debug
        self.commands = {}
        self.disabled_commands = {}
        self.events = {}
        self.disabled_events = {}
        self.available_events = ['start', 'exit', 'before', 'after', 'error', 'unknown_command']
        self.settings = {
            "prompt": prompt,
        }

    def set(self, setting, value):
        self.settings[setting] = value
        if self.debug:
            print(f"Setting '{setting}' set to '{value}'")

    def error(self, error:Exception=None):
        frame = inspect.currentframe().f_back
        function_name = frame.f_code.co_name
        if 'error' in self.events:
            self.events['error'](function_name, error)
        else:
            print(f"Error executing '{function_name}': {error}")

    def handleEvent(self, event:str='', *args, **kwargs):
        if event in self.events:
            self.events[event](*args, **kwargs)
        else:
            if self.debug:
                print(f"Event '{event}' not found")

    def on(self, event:str='', disabled:bool=False):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            event_name = event
            if event_name == '':
                event_name = func.__name__
            if event_name not in self.available_events:
                raise ValueError(f"Event '{event_name}' is not a valid event")
            if disabled:
                self.disabled_events[event_name] = wrapper
            else:
                self.events[event_name] = wrapper
            if self.debug:
                print(f"Event '{event_name}' registered")
            return wrapper
        return decorator
    
    def remove_event(self, event:str=''):
        if event in self.events:
            del self.events[event]
            if self.debug:
                print(f"Event '{event}' removed")

    def get_events(self):
        return self.events
    
    def disable_event(self, event:str=''):
        """
        Disable an event.
        
        :param event: The name of the event to disable.
        :return: True if the event was disabled, False if the event was not found.
        """
        if event in self.events:
            self.disabled_events[event] = self.events[event]
            del self.events[event]
            if self.debug:
                print(f"Event '{event}' disabled")
            return True
        else:
            if self.debug:
                raise ValueError(f"Event '{event}' not found")
            return False
        
    def enable_event(self, event:str=''):
        """
        Enable an event.
        
        :param event: The name of the event to enable.
        :return: True if the event was enabled, False if the event was not found.
        """
        if event in self.disabled_events:
            self.events[event] = self.disabled_events[event]
            del self.disabled_events[event]
            if self.debug:
                print(f"Event '{event}' enabled")
            return True
        else:
            if self.debug:
                raise ValueError(f"Event '{event}' not found")
            return False
    
    def command(self, name:str='', description:str='', disabled:bool=False):
        """
        Register a new command.

        :param name: The name of the command.
        :param description: A brief description of the command.
        """
        def decorator(func):
            sig = inspect.signature(func)
            cmd_args = {}
            for param_name, param in sig.parameters.items():
                default_value = param.default if param.default is not inspect.Parameter.empty else None
                cmd_args[param_name] = default_value
                if self.debug:
                    print(f"Argument '{param_name}' with default value '{default_value}' registered for command '{name}'")
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            cmd_name = name
            if cmd_name == '':
                cmd_name = func.__name__
            cmd = Command(cmd_name, description, wrapper, cmd_args)
            if disabled:
                self.disabled_commands[cmd_name] = cmd
            else:
                self.commands[cmd_name] = cmd
            if self.debug:
                print(f"Command '{cmd_name}' registered")
            return wrapper
        return decorator
    
    def cmd(self, name:str='', description:str=''):
        """
        Register a new command.

        :param name: The name of the command.
        :param description: A brief description of the command.
        """
        return self.command(name, description)
    
    def remove_command(self, name:str=''):
        """
        Remove a command.
        
        :param name: The name of the command to remove.
        :return: True if the command was removed, False if the command was not found.
        """
        if name in self.commands:
            del self.commands[name]
            if self.debug:
                print(f"Command '{name}' removed")
            return True
        else:
            if self.debug:
                raise ValueError(f"Command '{name}' not found")
            return False
    
    def get_commands(self):
        """
        Get a list of all registered commands.
        
        :return: A dictionary of all registered commands.
        """
        return self.commands
    
    def disable_command(self, name:str=''):
        """
        Disable a command.
        
        :param name: The name of the command to disable.
        :return: True if the command was disabled, False if the command was not found.
        """
        if name in self.commands:
            self.disabled_commands[name] = self.commands[name]
            del self.commands[name]
            if self.debug:
                print(f"Command '{name}' disabled")
            return True
        else:
            if self.debug:
                raise ValueError(f"Command '{name}' not found")
            return False
        
    def enable_command(self, name:str=''):
        """
        Enable a command.
        
        :param name: The name of the command to enable.
        :return: True if the command was enabled, False if the command was not found.
        """
        if name in self.disabled_commands:
            self.commands[name] = self.disabled_commands[name]
            del self.disabled_commands[name]
            if self.debug:
                print(f"Command '{name}' enabled")
            return True
        else:
            if self.debug:
                raise ValueError(f"Command '{name}' not found")
            return False
    
    def start(self):
        self.handleEvent('start')
        try:
            while True:
                cmd = input(f"{self.settings['prompt']}")
                args = cmd.split(' ')[1:]
                cmd = cmd.split(' ')[0]
                if cmd == 'exit':
                    self.handleEvent('exit')
                    break
                self.handleEvent('before', cmd, *args)
                if cmd in self.commands:
                    try:
                        self.commands[cmd].execute(*args)
                    except Exception as e:
                        if 'error' in self.events:
                            self.events['error'](cmd, e)
                        else:
                            print(f"Error executing command '{cmd}': {e}")
                else:
                    if 'unknown_command' in self.events:
                        self.events['unknown_command'](cmd)
                    else:
                        print(f"Unknown command: {cmd}")
                self.handleEvent('after', cmd, *args)
        except KeyboardInterrupt:
            self.handleEvent('exit')