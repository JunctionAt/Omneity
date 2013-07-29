from org.bukkit.event.player import PlayerCommandPreprocessEvent
from aliases import AliasListener
from actionsigns import ActionSignListener


class Omneity(PythonPlugin):

	def onEnable(self):

		# Config stuffs
		self.getDataFolder().mkdirs()

		# Register listeners
		self.listeners = list()

		self.listeners.append(AliasListener(self))
		self.listeners.append(ActionSignListener(self))

		for listener in self.listeners:
			self.getServer().getPluginManager().registerEvents(listener, self);
			listener.onEnable()

		print "Omneity Enabled"

	def onDisable(self):
		for listener in self.listeners:
			listener.onDisable()

		print "Omneity Disabled"