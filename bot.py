from javascript import require, On, Once, AsyncTask, once, off
from simple_chalk import chalk
from utils.vec3_conversion import vec3_to_str
import time
import random
# Requires ./utils/vec3_conversion.py

# Import the javascript libraries
mineflayer = require("mineflayer")
mineflayer_pathfinder = require("mineflayer-pathfinder")
vec3 = require("vec3")

# Global bot parameters
server_host = "anarchia.gg"
server_port = 25565
reconnect = True
onsmp = 0

class MCBot:

    def __init__(self, bot_name):
        self.bot_args = {
            "host": server_host,
            "port": server_port,
            "username": bot_name,
            "onlineMode": False,
            "version": "1.19.2",
            "hideErrors": False,
        }
        self.reconnect = reconnect
        self.bot_name = bot_name
        self.onserver = 0
        self.delay = 40
        self.onsmp = False
        self.start_bot()

    # Tags bot username before console messages
    def log(self, message):
        print(f"[{self.bot.username}] {message}")

    # Mineflayer: Pathfind to goal
    def pathfind_to_goal(self, goal_location):
        print(goal_location)
        try:
            self.bot.pathfinder.setGoal(
                mineflayer_pathfinder.pathfinder.goals.GoalNear(
                    goal_location["x"], goal_location["y"], goal_location["z"], 1
                )
            )

        except Exception as e:
            self.log(f"Error while trying to run pathfind_to_goal: {e}")

    # Start mineflayer bot
    def start_bot(self):
        self.bot = mineflayer.createBot(self.bot_args)
        self.bot.loadPlugin(mineflayer_pathfinder.pathfinder)

        self.start_events()

    # Attach mineflayer events to bot
    def start_events(self):

        # Login event: Triggers on bot login
        @On(self.bot, "login")
        def login(this):

            # Displays which server you are currently connected to
            self.bot_socket = self.bot._client.socket
            self.log(
                chalk.green(
                    f"Logged in to {self.bot_socket.server if self.bot_socket.server else self.bot_socket._host }"
                )
            )
            time.sleep(1)
            self.log("Joined")

        # Spawn event: Triggers on bot entity spawn
        @On(self.bot, "spawn")
        def spawn(this):
            global botnumber
            print("spawn")

        # Kicked event: Triggers on kick from server
        @On(self.bot, "kicked")
        def kicked(this, reason, loggedIn):
            if loggedIn:
                self.log(chalk.redBright(f"Kicked whilst trying to connect: {reason}"))

        # Chat event: Triggers on chat message
        @On(self.bot, "windowOpen")
        def windowOpen(this, window):
            self.bot.clickWindow(11,0,0)

        @On(self.bot, "messagestr")
        def messagestr(this, message, messagePosition, jsonMsg, sender, verified=None):
            global onsmp, botnumber
            if self.onsmp == True and random.randint(1,5) == 2:
                self.bot.chat("/tpa P1nGG75")
            if self.onsmp == False:
                self.log(chalk.white(message))
            if "secret" in message:
                if "quit" in message:
                    self.reconnect = False
                    this.quit()
            if "Weryfikacja" in message:
                self.bot.setControlState("forward", True)
            if "Twoje konto zostało zweryfikowane!" in message:
                if self.delay == 0:
                    self.bot.setControlState("left", True)
                else:
                    self.delay -= 1
            if "tpa" in message:
                if self.onsmp == False:
                    onsmp += 1
                    self.onsmp = True
                self.bot.setControlState("left", False)
                self.bot.setControlState("forward", False)
                if self.delay == 0:
                    self.bot.chat("/tpa P1nGG75")
                    self.delay = 1
            if "Wpisz /tpaccept * aby zaakceptowac wszystkich" in message:
                self.bot.setControlState("left", False)
                self.bot.setControlState("forward", False)
                self.bot.chat("/tpa P1nGG75")
            if "Odczekaj" in message:
                self.delay = 0
            if "/register <hasło> <powtórz hasło>" in message:
                numbers = message[-6:]
                self.bot.chat("/register D623g1!! D623g1!! "+numbers)
            if "Zaloguj się komendą /login <hasło>" in message:
                self.bot.chat("/login D623g1!!")
            if "Gracz P1nGG75 zabił "+self.bot_name in message:
                botname = "Bazuko"+str(botnumber)
                print(botname)
                MCBot(botname)
                self.log(chalk.red("Relog"))
                botnumber += 1
                onsmp -= 1
                self.reconnect = False
                this.quit()


        # End event: Triggers on disconnect from server
        @On(self.bot, "end")
        def end(this, reason):
            self.log(chalk.red(f"Disconnected: {reason}"))

            # Turn off old events
            off(self.bot, "login", login)
            off(self.bot, "spawn", spawn)
            off(self.bot, "kicked", kicked)
            off(self.bot, "messagestr", messagestr)

            # Reconnect
            if self.reconnect:
                if self.onsmp == True:
                    onsmp -= 1
                self.onserver = 0
                self.delay = 40
                self.onsmp = False
                self.tped = False
                self.log(chalk.cyanBright(f"Attempting to reconnect"))
                self.start_bot()

            # Last event listener
            off(self.bot, "end", end)
        

botnumber = 401
# Run function that starts the bot(s)

MCBot("Bazuko"+str(botnumber))
MCBot("Bazuko"+str(botnumber+1))
MCBot("Bazuko"+str(botnumber+2))
MCBot("Bazuko"+str(botnumber+3))
MCBot("Bazuko"+str(botnumber+4))
botnumber += 5
while True:
    time.sleep(0.05)
    print(str(onsmp)+"/5 na serwerze")