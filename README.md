# UNIVA
A little python program that makes it simple to create your own little cmd window with functionality

## Docs

### Introduction
To start open the app.py file. It should look something like this:
```py
from univa.main import Univa

app = Univa()

# YOUR CODE HERE

app.start()
```
You can change this later on as you like (for example changing the name of the "app" variable) but for the documentation we will be going after it this way to make it as easily understandable as possible.

### Events
Events are functions that are being executed when specific things happen.
```py
on(event)
def function()
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
add(name, description)
def function()
```

For example:
```py
@app.add()
def hello():
    print("Hello World")
```

The execution should look something like this:
```
Welcome to Univa!
> hello
Hello World
```

As you noticed I didn't give the "add" decorator a parameter this time, so it automatically took the name of the function.

This program, as well as this documentation is very early access.