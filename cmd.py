from pyrogram import filters
from pyrogram.errors import SlowmodeWait
import time

class Commands:
	def __init__(self, prefix, show_logs:bool=True):
		self.prefix=prefix
		self.commands={}
		self.logs=[]
		self.show_logs=show_logs

	def add_events(self, client, loader):
		@client.on_message(filters.me)
		def on_message(client, message):
			if not message.text or not message.text.startswith(self.prefix):
				return
			client.logs=self.logs
			client.cmds=self.commands
			client.loader=loader
			content=message.text.split(" ")
			#print(content)
			message.reply_text_1=message.reply_text
			def reply_text(*args, **kwargs):
				try:
					return message.reply_text_1(*args, **kwargs)
				except SlowmodeWait as e:
					time.sleep(e.x)
					return reply_text(*args, **kwargs)
			message.reply_text=reply_text
			content[0]=content[0][len(self.prefix):]
			if content[0] in self.commands:
				cmd=self.commands[content[0]]
				client.delete_messages(chat_id=message.chat.id, message_ids=message.id)
				cmd["function"](client, message, content[1:])
			else:
				self.log(f"[WARNING] {content[0]} not found", self.show_logs)

	def command(self, name:str, description:str=None, group:str="other"):
		def __wrapper__(fn):
			if name not in self.commands:
				self.commands[name]={"function": fn, "desc": description, "group":group}
			else:
				self.log("[WARNING] command {name} exists and cann't recreate!", self.show_logs)

		return __wrapper__

	def log(self, msg:str, show=False):
		self.logs.append(str(msg))
		if show!=False:
			print(self.logs[-1])

	def add(self, commands):
		if type(commands)!=type(self):
			return self.log("[ERROR:commands.add] Arg not command class", True)
		for i in commands.commands:
			self.commands[i]=commands.commands[i]
