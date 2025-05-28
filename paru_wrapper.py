import decman

class ParuWrapperCommands(decman.config.Commands):
    def __init__(self, username):
        super().__init__()
        self.username = username
    
    def demoted_command(self, command: list[str]) -> list[str]:
        return ["sudo", "-u", self.username, "-E"] + command 

    def list_pkgs(self) -> list[str]:
        return self.demoted_command(["paru", "-Qeq"])

    def install_pkgs(self, pkgs: list[str]) -> list[str]:
        return self.demoted_command(["paru", "-S"] + pkgs)

    def upgrade(self) -> list[str]:
        return self.demoted_command(["paru", "-Syu"])

    def remove(self, pkgs: list[str]) -> list[str]:
        return self.demoted_command(["paru", "-Rs"] + pkgs)
    