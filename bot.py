from javascript import require, On, Once, AsyncTask, once, off
from simple_chalk import chalk
from utils.vec3_conversion import vec3_to_str
import time
# Requires ./utils/vec3_conversion.py

# Import the javascript libraries
mineflayer = require("mineflayer")
mineflayer_pathfinder = require("mineflayer-pathfinder")
vec3 = require("vec3")

# Global bot parameters
server_host = "anarchia.gg"
server_port = 25565
reconnect = True


class MCBot:

    def __init__(self, bot_name):
        self.bot_args = {
            "host": server_host,
            "port": server_port,
            "username": bot_name,
            "onlineMode": False,
            "version": "1.18.2",
            "hideErrors": False,
        }
        self.reconnect = reconnect
        self.bot_name = bot_name
        self.onserver = 0
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
            if self.onserver == 0:
                print("ssdsa")
                time.sleep(1)
                self.onserver = 1
                self.bot.chat("/login dfdW5f2@")
                self.log("/login dfdW5f2@")
                self.pathfind_to_goal({"x": 1, "y": 400, "z": 0})
                time.sleep(1)
                print("-------sds--")

        # Spawn event: Triggers on bot entity spawn
        @On(self.bot, "spawn")
        def spawn(this):
            print("----------------")
            if self.onserver == 1:
                self.onserver = 2
                time.sleep(5)
                self.pathfind_to_goal({"x": 62, "y": 130, "z": 230})
                time.sleep(10)
                self.bot.setQuickBarSlot(4);
                time.sleep(0.1)
                self.bot.activateItem();
                time.sleep(1)
                self.bot.clickWindow(1, 0, 0);
            elif self.onserver == 2:
                time.sleep(5)
                self.bot.chat("/msg supermanEnjoy hej")

        # Kicked event: Triggers on kick from server
        @On(self.bot, "kicked")
        def kicked(this, reason, loggedIn):
            if loggedIn:
                self.log(chalk.redBright(f"Kicked whilst trying to connect: {reason}"))

        # Chat event: Triggers on chat message
        @On(self.bot, "messagestr")
        def messagestr(this, message, messagePosition, jsonMsg, sender, verified=None):
            self.log(chalk.white(message))
            if "secret" in message:
                if "quit" in message:
                    self.bot.chat("Goodbye!")
                    self.reconnect = False
                    this.quit()
            if self.onserver == 0:
                if "/login" in message and False:
                    time.sleep(1)
                    self.onserver = 1
                    self.bot.chat("/login dfdW5f2@")
                    self.log("/login dfdW5f2@")
                    
                    time.sleep(1)
                    print("---------")


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
                self.log(chalk.cyanBright(f"Attempting to reconnect"))
                self.start_bot()

            # Last event listener
            off(self.bot, "end", end)
        


# Run function that starts the bot(s)
bot1 = MCBot("DerProfi14511")
