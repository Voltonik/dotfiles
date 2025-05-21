import decman

class ParuWrapperCommands(decman.config.Commands):
    def __init__(self, username):
        super().__init__()
        self.username = username

    def list_pkgs(self) -> list[str]:
        return ["paru", "-Qeq"]

    def install_pkgs(self, pkgs: list[str]) -> list[str]:
        return ["paru", "-S"] + pkgs

    def upgrade(self) -> list[str]:
        return ["paru", "-Syu"]

    def remove(self, pkgs: list[str]) -> list[str]:
        return ["paru", "-Rs"] + pkgs