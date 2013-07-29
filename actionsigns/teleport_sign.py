from . import register_sign_type, SignBase
from org.bukkit import Location


@register_sign_type('teleport')
class TeleportSign(SignBase):
	"""
	Format:

	- location: [x, y, z]
	  type: teleport
	  destination: [x, y, z]
	"""
	
	def onLeftClick(self, sign_data, plugin, event, sign):
		self.teleport_player(event.getPlayer(), sign_data['destination'])

	def onRightClick(self, sign_data, plugin, event, sign):
		self.teleport_player(event.getPlayer(), sign_data['destination'])

	def teleport_player(self, player, location_array):
		player.teleport(Location(player.getWorld(), location_array[0], location_array[1], location_array[2]))