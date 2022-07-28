import requests
from requests_file import FileAdapter
import pathlib

curr_dir=pathlib.Path(__file__).parent.resolve()
requests=requests.Session()
requests.mount('file://', FileAdapter())
dlmod_repo=f"file://{curr_dir}/dlmod.repo.json"
dlmod_json=requests.get(dlmod_repo).json()



class Module:
    group="loader"
    def __init__(self, bot, commands):
        self.commands=commands

    def dlmodcmd(self, bot, message, args):
        for url in args:
            match bot.loader.load(url):
                case 1:
                    message.reply_text(f"[dlmod] module '{url}' error loading, unknown error")
                    continue
                case 2:
                    message.reply_text(f"[dlmod] module '{url}' error loading, return http code 404/not found")
                    continue
                case 3:
                    message.reply_text(f"[dlmod] module '{url}' error loading, invalid/non python code")
                    continue
                case 4:
                    message.reply_text(f"[dlmod] module '{url}' error loading, module loaded")
                    continue
            message.reply_text(f"[dlmod] module '{url}' successful loading!")
            dlmod_json.append(module_url)
        open('dlmod.repo.json', 'w').write(str(dlmod_json))

    def rmmodcmd(self, bot, message, args):
        for url in args:
            match bot.loader.unload(url):
                case 1:
                    message.reply_text(f"[rmmod] module '{url}' error unloading, module not loaded!")
                    continue
            message.reply_text(f"[rmmod] module '{url}' successful unloading!")
            dlmod_json.pop(dlmod_json.index(module_url))
        open('dlmod.repo.json', 'w').write(str(dlmod_json))

    def rlmodcmd(self,bot,message,args):
        for url in args:
            match bot.loader.unload(url):
                case 1:
                    message.reply_text(f"[rlmod] module '{url}' error unloading, module not loaded")
                    continue
            a=bot.loader.load(url)
            message.reply_text(f"[rlmod] module '{url}' successful reloading!" if a==None else f"[rlmod] module '{url}' error loading, please use dlmod for get error!")
