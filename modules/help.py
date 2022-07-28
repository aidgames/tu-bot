class Module:
    group="help"
    def __init__(self, bot, commands):
        self.commands=commands

    def helpcmd(self, bot, message, args):
        bg={}
        for cmd in  bot.cmds:

            cmd2=bot.cmds[cmd]
            if cmd2['group'] not in bg:
                bg[cmd2['group']] = []
            bg[cmd2['group']].append(cmd)
        ret="**Help Command**\n"
        for group in bg:
            ret+=f"__**{group}**__: " + " ".join(bg[group]) + "\n" 
        message.reply_text(ret)
