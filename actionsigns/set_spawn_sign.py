from . import register_sign_type, SignBase
from org.bukkit import Location


@register_sign_type('set_spawn')
class TeleportSign(SignBase):
    """
    Format:

    - coordinates: [x, y, z]
      type: set_spawn
      spawn_point: [x, y, z]
    """

    def onLeftClick(self, sign_data, plugin, event, sign):
        player = event.getPlayer()
        player.setSpawnLocation(Location(player.getWorld(),
                                         sign_data['destination'][0],
                                         sign_data['destination'][1],
                                         sign_data['destination'][2]))

    def onRightClick(self, sign_data, plugin, event, sign):
        self.onLeftClick(sign_data, plugin, event, sign)
