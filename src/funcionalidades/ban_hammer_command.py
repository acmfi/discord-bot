from funcionalidades.command import Command
class BanHammerCommand(Command):
    def __init__(self):
        super().__init__("censor", ["censura", "censurar"])
    
    