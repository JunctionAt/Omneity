from org.bukkit import Material, Location


class PortalException(Exception):
	pass

def find_portal_block(location, radius):
	"""
	Find a nearby portal block. Not necessarily the closest.
	"""

	world = location.getWorld()
	x = location.getBlockX()
	y = location.getBlockY()
	z = location.getBlockZ()

	for xran in range(-radius, radius):
		for yran in range(-radius, radius):
			for zran in range(-radius, radius):
				if world.getBlockAt(x+xran, y+yran, z+zran).getType() == Material.PORTAL:
					return Location(world, x+xran, y+yran, z+zran)

	return False