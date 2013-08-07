from baselistener import BaseListener
from config import ConfigManager
from os import path
from org.bukkit.event.player import PlayerJoinEvent, PlayerPortalEvent, PlayerRespawnEvent
from org.bukkit import Location
from bukkit_helpers import chatcolor
from org.bukkit.World import Environment


class SpawnListener(BaseListener):

	default_config = {
			'spawn': {
				'location': [0, 0, 0],
				'orientation': [0, 0],
				'world': 'world'
			},
			'first-join-message': {
				'show': True,
				'message': "%(GOLD)sWelcome %(name)s to the server!"
			},
			'allow-bed-spawn': True
		}

	def __init__(self, plugin):
		self.plugin = plugin

	def onEnable(self):
		self.config_manager = ConfigManager(path.join(self.plugin.getDataFolder().getAbsolutePath(), 'spawn.yml'), default=self.default_config)
		self.config_manager.load_config()

		self.register_event(self.onPlayerJoinEvent, PlayerJoinEvent)
		self.register_event(self.onPlayerPortalEvent, PlayerPortalEvent)
		self.register_event(self.onPlayerRespawnEvent, PlayerRespawnEvent)

	def onDisable(self):
		self.config_manager.save_config()

	def getSpawnLocation(self):
		spawn_info = self.config_manager.config['spawn']

		return Location(
			self.plugin.getServer().getWorld(spawn_info['world']),
			spawn_info['location'][0], spawn_info['location'][1], spawn_info['location'][2],
			spawn_info['orientation'][0], spawn_info['orientation'][1]
			)

	def onPlayerJoinEvent(self, event):
		player = event.getPlayer()

		if not player.hasPlayedBefore():
			player.teleport(self.getSpawnLocation())

		first_join_message_info = self.config_manager.config['first-join-message']
		if first_join_message_info['show']:
			message = first_join_message_info['message'] % dict({'name': event.getPlayer().getName()}.items() + chatcolor.colors.items())
			self.plugin.getServer().broadcastMessage(message)

	def onPlayerPortalEvent(self, event):
		if event.getFrom().getWorld().getEnvironment() == Environment.THE_END and not self.config_manager.config['allow-bed-spawn']:
			event.setTo(self.getSpawnLocation())

	def onPlayerRespawnEvent(self, event):
		if not event.isBedSpawn() or not self.config_manager.config['allow-bed-spawn']:
			event.setRespawnLocation(self.getSpawnLocation())


listener = SpawnListener