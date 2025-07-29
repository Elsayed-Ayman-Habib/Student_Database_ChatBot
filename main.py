from Chatbot import Chatbot

bot = Chatbot()

while True:
    cmd = input("\nEnter command (or 'exit'): ")
    if cmd.lower() == "exit":
        bot.close()
        break
    bot.handle_command(cmd)
