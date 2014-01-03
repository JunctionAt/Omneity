from . import register_sign_type, SignBase
from bukkit_helpers import chatcolor
from org.bukkit.inventory import ItemStack


@register_sign_type('give')
class GiveSign(SignBase):
    """
    Format:

    - location: [x, y, z]
      type: give
      give_item: 2
      give_item_data: 0            [default: 0]
      give_item_amount: 1          [default: 1]
      give_item_desc: 64 Diamonds  [default: an item]
    """

    def onLeftClick(self, sign_data, plugin, event, sign):
        pass


    def onRightClick(self, sign_data, plugin, event, sign):
        player = event.getPlayer()

        give_item = sign_data["give_item"]
        give_item_data = sign_data.get("give_item_data", 0)
        give_item_amount = sign_data.get("give_item_amount", 1)
        give_item_desc = sign_data.get("give_item_desc", "an item")

        if self.safe_give(player, ItemStack(give_item, give_item_amount, give_item_data)):
            self.message(player, "You've been given %s!" % give_item_description)
        else:
            self.message(player, "Please clean up your inventory a bit, there is no space :(")

        player.updateInventory()


    def safe_give(self, player, itemstack):
        inventory = player.getInventory()

        not_added = inventory.addItem(itemstack)
        if not not_added.isEmpty():
            amount = 0
            for entry in not_added.entrySet():
                amount += entry.getValue().getAmount()
            itemstack.setAmount(itemstack.getAmount() - amount)
            inventory.removeItem(itemstack)

            return False
        return True


    def message(self, player, message):
        player.sendMessage(
            chatcolor.GOLD + "[SIGN] " +
            chatcolor.WHITE + message
        )
