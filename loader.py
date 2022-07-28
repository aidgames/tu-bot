import importlib.abc
import requests
from requests_file import FileAdapter
import pathlib
from config import CONFIG_CUSTOM_REPOS_ENABLE


curr_dir=pathlib.Path(__file__).parent.resolve()

requests=requests.Session()
requests.mount('file://', FileAdapter())



repos=['https://raw.githubusercontent.com/aidgames/ti-bot/master/modules/repo.json']

if CONFIG_CUSTOM_REPOS_ENABLE:
    try:
        from config import CONFIG_CUSTOM_REPOS
    except:
        CONFIG_CUSTOM_REPOS=[]
        print("you don't add CONFIG_CUSTOM_REPOS in config but CONFIG_CUSTOM_REPOS_ENABLE enabled!")
    repos+=CONFIG_CUSTOM_REPOS

class StringLoader(importlib.abc.SourceLoader):
    def __init__(self, data):
        self.data = data

    def get_source(self, fullname):
        return self.data

    def get_source(self, fullname):
        return self.data

    def get_data(self, path):
        return self.data.encode("utf-8")

    def get_filename(self, fullname):
        return fullname


class Loader:
    loaded={}
    def __init__(self, bot, commands):
        self.bot=bot
        self.commands=commands
    def load(self, module_url):
        if module_url in self.loaded:
            return 4
        try:
            r=requests.get(module_url)
        except:
            return 1
        if r.status_code==404:
            return 2
        code=r.text
        try:
            tmp_loader=StringLoader(code)
        except:
            return 3
        spec=importlib.util.spec_from_loader(module_url, tmp_loader, origin="built-in")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module=module.Module(self.bot, self.commands)
        self.loaded[module_url]=[]
        for i in dir(module):
            if i.endswith("cmd"):
                self.commands.command(i[:-3], group=module.group or "other")(module.__getattribute__(i))
                self.loaded[module_url].append(i[:-3])
    def unload(self, module_url):
        if module_url not in self.loaded:
            return 1
        for cmd in self.loaded.get(module_url):
            del self.commands.commands[cmd]
        del self.loaded[module_url]

def setup(bot,commands):
    loader=Loader(bot, commands)
    for repo in repos:
        r=requests.get(repo)
        if r.status_code==404:
            print(f"[ERROR] repo '{repo}' not found")
            continue
        repo_root="/".join(repo.split("/")[:-1])+"/"
        for module in r.json():
            module_url=repo_root+module
            loader.load(module_url)
    return loader
