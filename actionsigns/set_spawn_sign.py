from . import register_sign_type, SignBase
from org.bukkit import Location


@register_sign_type('set_spawn')
class TeleportSign(SignBase):
    """
    Note: Spawn module must be enabled with allow-bed-spawn set to true.

    Format:

    - coordinates: [x, y, z]
      type: set_spawn
      spawn_point: [x, y, z]
    """

    def onLeftClick(self, sign_data, plugin, event, sign):
        player = event.getPlayer()
        sp = sign_data['spawn_point']
        player.setBedSpawnLocation(Location(player.getWorld(), sp[0], sp[1], sp[2]), True)

    def onRightClick(self, sign_data, plugin, event, sign):
        self.onLeftClick(sign_data, plugin, event, sign)
