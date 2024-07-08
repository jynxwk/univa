import inspect
import os
from functools import wraps
from .classes import Command

class Univa:
    def __init__(self, debug=False, prompt=">"):
        self.debug = debug
        self.commands = {}
        self.events = {}
        self.available_events = ['start', 'exit', 'before', 'after', 'error', 'unknown_command']
        self.settings = {
            "prompt": prompt,
        }

    def on(self, event):
        def decorator(func):
            if event not in self.available_events:
                raise ValueError(f"Event '{event}' is not a valid event")
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.events[event] = wrapper
            if self.debug:
                print(f"Event '{event}' registered")
            return wrapper
        return decorator
    
    def add(self, name='', description=''):
        def decorator(func):
            sig = inspect.signature(func)
            cmd_args = {}
            for param_name, param in sig.parameters.items():
                default_value = param.default if param.default is not inspect.Parameter.empty else None
                cmd_args[param_name] = default_value
                print(f"Parameter name: {param_name}, Default value: {default_value}")
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            cmd_name = name
            if cmd_name == '':
                cmd_name = func.__name__
            self.commands[cmd_name] = Command(cmd_name, description, wrapper, cmd_args)
            if self.debug:
                print(f"Command '{name}' registered")
            return wrapper
        return decorator
    
    def set(self, setting, value):
        self.settings[setting] = value
        if self.debug:
            print(f"Setting '{setting}' set to '{value}'")
    
    def start(self):
        if 'start' in self.events:
            self.events['start']()
        else:
            print("Welcome to Univa!")
            print("You can customize this message by adding a 'start' event")
        while True:
            cmd = input(f"{self.settings['prompt']}")
            args = cmd.split(' ')[1:]
            cmd = cmd.split(' ')[0]
            if cmd == 'exit':
                if 'exit' in self.events:
                    self.events['exit']()
                break
            if cmd in self.commands:
                try:
                    if 'before' in self.events:
                        self.events['before'](cmd, *args)
                    self.commands[cmd].execute(*args)
                    if 'after' in self.events:
                        self.events['after'](cmd, *args)
                except TypeError as e:
                    if 'error' in self.events:
                        self.events['error'](cmd, e)
                    else:
                        print(f"Error executing command '{cmd}': {e}")
            else:
                if 'unknown_command' in self.events:
                    self.events['unknown_command'](cmd)
                else:
                    print(f"Unknown command: {cmd}")