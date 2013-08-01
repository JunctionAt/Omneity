from org.bukkit import TravelAgent
from portal_util import PortalException, find_portal_block


class OtOTravelAgent(TravelAgent):

	portal_build_z_offset = -1
	portal_build = [
		[
			[1, 1, 1, 1],
			[49, 49, 49, 49],
			[1, 1, 1, 1]
		],
		[
			[0, 0, 0, 0],
			[49, 90, 90, 49],
			[0, 0, 0, 0]
		],
		[
			[0, 0, 0, 0],
			[49, 90, 90, 49],
			[0, 0, 0, 0]
		],
		[
			[0, 0, 0, 0],
			[49, 90, 90, 49],
			[0, 0, 0, 0]
		],
		[
			[0, 0, 0, 0],
			[49, 49, 49, 49],
			[0, 0, 0, 0]
		]
	]

	def __init__(self, server):
		self.server = server

	def setSearchRadius(self, radius):
		print "setSearchRadius(" + radius + ")"
		return self
		#return TravelAgent

	def getSearchRadius(self):
		return 1
		#return int

	def setCreationRadius(self, radius):
		print "setCreationRadius(" + radius + ")"
		return self
		#return TravelAgent

	def getCreationRadius(self):
		return 1
		#return int

	def setCanCreatePortal(self, boolean):
		print "setCanCreatePortal(" + boolean + ")"
		#return void

	def getCanCreatePortal(self):
		return False
		#return boolean

	def findOrCreate(self, location):
		print "findOrCreate"

		portal = self.findPortal(location)

		if not portal:
			portal = self.createPortal(location)

		if portal:
			portal.setPitch(location.getPitch())
			portal.setYaw(location.getYaw())

		return portal
		#return location

	def findPortal(self, location):
		print "findPortal"

		portal = find_portal_block(location, 2)

		if not portal:
			portal = None

		if portal:
			portal.setPitch(location.getPitch())
			portal.setYaw(location.getYaw())

		return portal
		#return location

	def createPortal(self, location):
		print "createPortal"

		if location.portalcorner == None or location.portaldirection == None:
			raise PortalException()

		startloc = location.portalcorner

		#Apply the schematic offset to the start location
		if location.portaldirection == 0:
			startloc = location.portalcorner.subtract(0, 0, self.portal_build_z_offset)
		elif location.portaldirection == 1:
			startloc = location.portalcorner.subtract(self.portal_build_z_offset, 0, 0)

		world = location.getWorld()
		direction = location.portaldirection

		#Build the portal
		for y_index, y_data in enumerate(self.portal_build):
			for z_index, z_data in enumerate(y_data):
				for x_index, x_data in enumerate(z_data):
					if direction == 0:
						world.getBlockAt(startloc.getBlockX() + x_index, startloc.getBlockY() + y_index, startloc.getBlockZ() - z_index).setTypeIdAndData(x_data, 0, False)
					elif direction == 1:
						world.getBlockAt(startloc.getBlockX() - z_index, startloc.getBlockY() + y_index, startloc.getBlockZ() + x_index).setTypeIdAndData(x_data, 0, False)

		return location
		#return location