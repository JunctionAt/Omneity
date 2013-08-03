from command import register_command
from baselistener import BaseListener
from config import ConfigManager
from os import path
from bukkit_helpers import chatcolor
from org.bukkit import Location


class WarpListener(BaseListener):

	permission_error = chatcolor.RED + "I'm sorry, but you do not have permission to perform this command. Please contact the server administrators if you believe that this is in error."

	default_config = {
			'warps':{
				'test': {
					'location': [0, 0, 0],
					'orientation': [0, 0],
					'world': 'world'
				}
			}
		}

	def __init__(self, plugin):
		self.plugin = plugin

	def onEnable(self):
		self.config_manager = ConfigManager(path.join(self.plugin.getDataFolder().getAbsolutePath(), 'warps.yml'), default=self.default_config)
		self.config_manager.load_config()

		register_command(self.command_warp, 'warp', description="Warp to places", usage="/<command> <warp> | set <warp> | del <warp> | list", permission="omneity.warp")

	def onDisable(self):
		self.config_manager.save_config()

	def command_warp(self, sender, label, args):
		if len(args) < 1:
			return False

		if args[0] == "set":
			if not sender.hasPermission("omneity.warp.set"):
				sender.sendMessage(self.permission_error)
				return

			if len(args) != 2:
				return False

			location = sender.getLocation()

			self.config_manager.config['warps'][args[1]] = {'location': [location.getX(), location.getY(), location.getZ()], 'orientation': [location.getYaw(), location.getPitch()], 'world': location.getWorld().getName()}
			self.config_manager.mark_dirty()

			sender.sendMessage(chatcolor.GOLD + "Warp set.")

			return True

		if args[0] == "del":
			if not sender.hasPermission("omneity.warp.del"):
				sender.sendMessage(self.permission_error)
				return

			if len(args) != 2:
				return False

			del(self.config_manager.config['warps'][args[1]])
			self.config_manager.mark_dirty()

			sender.sendMessage(chatcolor.GOLD + "Warp deleted.")
			return

		if args[0] == "list":
			sender.sendMessage(chatcolor.GOLD + ', '.join(self.config_manager.config['warps'].keys()))
			return

		if len(args) != 1:
			return False

		try:
			warp_data = self.config_manager.config['warps'][args[0]]
		except KeyError:
			sender.sendMessage(chatcolor.GOLD + "Warp doesn't exist.")
			return

		location = Location(
			self.plugin.getServer().getWorld(warp_data['world']),
			warp_data['location'][0], warp_data['location'][1], warp_data['location'][2],
			warp_data['orientation'][0], warp_data['orientation'][1])

		sender.teleport(location)
		sender.sendMessage(chatcolor.GOLD + "Warped.")


listener = WarpListener