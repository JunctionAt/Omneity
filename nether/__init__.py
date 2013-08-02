from baselistener import BaseListener
from config import ConfigManager
from org.bukkit.event.player import PlayerPortalEvent, PlayerTeleportEvent
from org.bukkit.event.world import PortalCreateEvent
from os import path
from org.bukkit import Location, Material
from ototravelagent import OtOTravelAgent
from portal_util import PortalException, find_portal_block


class PortalCoordinates(Location):

	def __init__(self, world, x, y, z, pitch=None, yaw=None, portalcorner=None, portaldirection=None):
		if pitch or yaw:
			super(Location, self).__init__(world, x, y, z, pitch, yaw)
		else:
			super(Location, self).__init__(world, x, y, z)

		if portalcorner is None or portaldirection is None:
			raise AttributeError()

		self.portalcorner = portalcorner
		self.portaldirection = portaldirection


class NetherListener(BaseListener):

	default_config = {
			'create_opposite_portal': True
		}

	def __init__(self, plugin):
		self.plugin = plugin

	def onEnable(self):
		self.config_manager = ConfigManager(path.join(self.plugin.getDataFolder().getAbsolutePath(), 'nether.yml'), default=self.default_config)
		self.config_manager.load_config()

		self.register_event(self.onPlayerPortalEvent, PlayerPortalEvent)
		self.register_event(self.onPortalCreateEvent, PortalCreateEvent)

		self.travelagent = OtOTravelAgent(self.plugin.getServer())

	def onDisable(self):
		self.config_manager.save_config()

	def onPortalCreateEvent(self, event):
		pass

	def onPlayerPortalEvent(self, event):

		if event.getCause() != PlayerTeleportEvent.TeleportCause.NETHER_PORTAL:
			print "not a nether portal"
			return

		fr = event.getFrom()
		to = event.getTo()

		if self.config_manager.config['create_opposite_portal']:
			to_new = self.find_portal_data(fr)
			to_new.setWorld(to.getWorld())

			event.setTo(to_new)

			event.setPortalTravelAgent(self.travelagent)
		else:
			to.setX(fr.getX())
			to.setY(fr.getY())
			to.setZ(fr.getZ())

			event.setTo(to)

			event.setPortalTravelAgent(None)

	def find_portal_data(self, location):
		world = location.getWorld()

		#Coordinates are not always accurate, sometimes they are a block next to it. Check nearby blocks for portal.
		corner = find_portal_block(location, 2)
		if not corner:
			raise PortalException("Unable to find from portal")

		#Find the bottom of the portal.
		while world.getBlockAt(corner).getType() == Material.PORTAL:
			corner.subtract(0, 1, 0)
		if world.getBlockAt(corner).getType() != Material.OBSIDIAN:
			raise PortalException("Portal wasn't really a portal")

		#Find which way the portal is placed, and do final adjustments to the corner.
		if world.getBlockAt(corner.getBlockX()+1, corner.getBlockY()+1, corner.getBlockZ()).getType() == Material.PORTAL:
			direction = 0
			corner.subtract(1, 0, 0)
		elif world.getBlockAt(corner.getBlockX(), corner.getBlockY()+1, corner.getBlockZ()+1).getType() == Material.PORTAL:
			direction = 1
			corner.subtract(0, 0, 1)
		elif world.getBlockAt(corner.getBlockX()-1, corner.getBlockY()+1, corner.getBlockZ()).getType() == Material.PORTAL:
			direction = 0
			corner.subtract(2, 0, 0)
		elif world.getBlockAt(corner.getBlockX(), corner.getBlockY()+1, corner.getBlockZ()-1).getType() == Material.PORTAL:
			direction = 1
			corner.subtract(0, 0, 2)
		else:
			raise PortalException("Unable to find portal direction")

		return PortalCoordinates(world, location.getBlockX(), location.getBlockY(), location.getBlockZ(), location.getYaw(), location.getPitch(), corner, direction)


listener = NetherListener