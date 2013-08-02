from org.bukkit.event.player import PlayerExpChangeEvent
from org.bukkit import Location
from baselistener import BaseListener
from config import ConfigManager
from os import path


class XpListener(BaseListener):

	default_config = {
			'xp_buff': 5
		}

	def __init__(self, plugin):
		self.plugin = plugin

	def onEnable(self):
		self.config_manager = ConfigManager(path.join(self.plugin.getDataFolder().getAbsolutePath(), 'xp.yml'), default=self.default_config)
		self.config_manager.load_config()

		self.register_event(self.onPlayerMoveEvent, PlayerExpChangeEvent)

	def onDisable(self):
		self.config_manager.save_config()

	def onPlayerExpChangeEvent(self, event):

		event.setAmount(event.getAmount()*self.config_manager.config['xp_buff'])


listener = XpListener