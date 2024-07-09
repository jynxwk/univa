# UNIVA
A little python program that makes it simple to create your own little command line window with functionality

## Docs

### Introduction
Open the app.py file. It should look something like this:
```py
from univa.main import Univa

app = Univa()

@app.on("start")
def start():
    print("Welcome to Univa!")
    print("You can customize this message by changing the 'start' event")

# Your code here

app.start()
```
You can change this later on as you like (for example changing the name of the "app" variable) but for the documentation we will be going after it this way to make it as easily understandable as possible.

### Settings
Currently there are 2 customizable settings:
`debug:boolean` - enables debug mode (prints event and command registration, etc)
`prompt:str` - set the user prompt

You can enable settings either by passing them as an argument when creating the univa object like this:
```py
app = Univa(debug=True, prompt="> ")
```
or at any time by using the `set()` function:
```py
app.set("debug", True)
app.set("prompt", "> ")
```

### Events
Events are functions that are being executed when specific things happen.
```py
@Univa.on(event)
def function() # The function to be executed
```

For example:
```py
@app.on("start")
def start():
    print("Welcome to Univa!")
```

This snippet adds a "start" event. This event will be fired whenever the app starts up.
When running it, it should look something like this:
```
Welcome to Univa!
>
```
Events are optional. If you don't add a start event, a default one will be executed. (I will add a way to disable this later on)

You can remove events at any time using the `remove_event()` function:
```py
Univa.remove_event(event)
```

This can be used to run events only once:
```py
@app.on("before")
def start():
    print("This text only appears once before a function is executed and then never again!")
    app.remove_event("before")
```

Here is a list of all available events:
`start` - executed when the user starts the program
`exit` - executed when the users exits the program
`before` - executed each time before a command is executed
`after` - executed each time after a command is executed
`error` - executed when an error occurs
`unknown_command` - executed when an unknown command is called

### Commands
Commands are functions that are being executed when the user types them in.
```py
@Univa.command(name:str, description:str)
def function() # The function to be executed
```
_You can use `cmd` for short_

For example:
```py
@app.cmd()
def hello():
    print("Hello World")
```

The execution should look something like this:
```
Welcome to Univa!
> hello
Hello World
```

As you noticed I didn't give the "cmd" decorator a parameter this time, so it automatically took the name of the function.

Commands can also be removed:
```py
@app.command("once")
def once():
    print("You can only execute me one time")
    app.remove_command("once")
```

You can get all commands by using the `get_commands()` function, for example to make a dynamic help command:
```py
@app.cmd('help', 'Displays a list of commands')
def help():
    commands = app.get_commands()
    for command in commands:
        if commands[command].args:
            arg_str = ""
            for arg in commands[command].args:
                arg_name = arg
                arg_default = commands[command].args[arg]
                arg_str += f"[{arg_name}={arg_default}] "
            print(f"{command} {arg_str}- {commands[command].description}")
        else:
            print(f"{command} - {app.commands[command].description}")
```

The output looks like this:
```
> help
help - Displays a list of commands
```

### Utils
Utils are functions you can import that just make the coding process a little simpler and quicker
For example:
```py
from univa.utils import clear

#...

# Clear the console before executing a command
@app.on("before")
def before():
    clear()
```
Currently `clear()` is the only function but I'm planning on adding more.
_As the name says `clear()` clears the console (but it has been optimized to work for windows and linux, just so you can save some code)_

This is practically all the information you need to start programming! 
This "framework", as well as this documentation is very early access and will be updated over time.