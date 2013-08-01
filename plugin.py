from os import path
from config import ConfigManager


class Omneity(PythonPlugin):

	default_config = {
			'modules': [
				'aliases',
				'actionsigns'
			]
		}

	def onEnable(self):
		# Config stuffs
		self.getDataFolder().mkdirs()

		self.config_manager = ConfigManager(path.join(self.getDataFolder().getAbsolutePath(), 'config.yml'), default=self.default_config)
		self.config_manager.load_config()

		# Register listeners
		self.listeners = list()

		for module_name in self.config_manager.config['modules']:
			listener = __import__(module_name).listener(self)

			self.listeners.append(listener)
			listener.onEnable()
			
			self.getServer().getPluginManager().registerEvents(listener, self);

		print "Omneity Enabled"

	def onDisable(self):
		for listener in self.listeners:
			listener.onDisable()

		self.config_manager.save_config()

		print "Omneity Disabled"