from . import register_sign_type, SignBase
from org.bukkit import Location


@register_sign_type('teleport')
class TeleportSign(SignBase):
    """
    Format:

    - coordinates: [x, y, z]
      type: teleport
      destination: [x, y, z]
      clear_inventory: true   [default: false]
    """

    def onLeftClick(self, sign_data, plugin, event, sign):
        player = event.getPlayer()
        clear_inventory = sign_data.get("clear_inventory", False)
        if clear_inventory:
            inventory = player.getInventory()
            inventory.clear()
            inventory.setBoots(None)
            inventory.setChestplate(None)
            inventory.setLeggings(None)
            inventory.setHelmet(None)
            player.updateInventory()
        self.teleport_player(player, sign_data['destination'])

    def onRightClick(self, sign_data, plugin, event, sign):
        self.onLeftClick(sign_data, plugin, event, sign)

    def teleport_player(self, player, location_array):
        player.teleport(Location(player.getWorld(), location_array[0], location_array[1], location_array[2]))
