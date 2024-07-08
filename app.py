from univa.main import Univa

app = Univa()

@app.on("start")
def start():
    print("Welcome to Univa!")
    print("You can customize this message by changing the 'start' event")

# Your code here

app.start()