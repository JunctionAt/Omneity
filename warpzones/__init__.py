from org.bukkit.event.player import PlayerMoveEvent
from org.bukkit import Location
from baselistener import BaseListener
from config import ConfigManager
from os import path


class WarpZoneListener(BaseListener):

	default_config = {
			'warpzones': [
				{
					'area': {
						'min': [0, 0, 0],
						'max': [1, 1, 1],
						'world': 'world'
					},
					'to': {
						'location': [2, 2, 2],
						'world': 'world'
					}
				}
			]
		}

	def __init__(self, plugin):
		self.plugin = plugin

	def onEnable(self):
		self.config_manager = ConfigManager(path.join(self.plugin.getDataFolder().getAbsolutePath(), 'warpzones.yml'), default=self.default_config)
		self.config_manager.load_config()

		self.register_event(self.onPlayerMoveEvent, PlayerMoveEvent)

	def onDisable(self):
		self.config_manager.save_config()

	def onPlayerMoveEvent(self, event):

		if event.getFrom().getBlock() == event.getTo().getBlock():
			return

		to = event.getTo()
		to_arr = [to.getBlockX(), to.getBlockY(), to.getBlockZ()]

		for warp in self.config_manager.config['warpzones']:
			if warp['area']['world'] == event.getPlayer().getLocation().getWorld().getName():
				if self.is_in_range(to_arr, warp['area']['min'], warp['area']['max']): #Should probably do a rtree or something
					to_loc = warp['to']['location']
					event.getPlayer().teleport(Location(self.plugin.getServer().getWorld(warp['to']['world']), to_loc[0], to_loc[1], to_loc[2]))

	def is_in_range(self, loc, mini, maxi):
		return self.arr_gt(loc, mini) and self.arr_lt(loc, maxi)

	def arr_gt(self, arr1, arr2):
		for index in range(0, len(arr1)):
			if not arr1[index] >= arr2[index]:
				return False
		return True

	def arr_lt(self, arr1, arr2):
		for index in range(0, len(arr1)):
			if not arr1[index] <= (arr2[index]):
				return False
		return True

listener = WarpZoneListener