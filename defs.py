import json
from discord import Guild, Role, TextChannel

class bot_config():
    def __init__(self, filename: str):
        self.filename = filename
        self.property: dict = {}
        self.config: dict = {}

    def load_def(self, guild: Guild):
        property: dict = {}
        config: dict = {}
        with open(self.filename) as file:
            config = json.load(file)

        if config.get('admin'):
            property['admin'] = guild.get_role(config['admin'])
        if config.get('gamming'):
            property['gamming'] = guild.get_role(config['gamming'])
        if config.get('log_channel'):
            property['log_channel'] = guild.get_channel(config['log_channel'])

        self.property = property
        self.config = config

    def set_def(self, key: str, value):
        self.property[key] = value
        if isinstance(value, Role) or isinstance(value, TextChannel):
            self.config[key] = value.id
        else:
            self.config[key] = value
        
        with open(self.filename, 'w') as file:
            json.dump(self.config, file)
        
