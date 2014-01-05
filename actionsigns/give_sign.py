from . import register_sign_type, SignBase
from bukkit_helpers import chatcolor
from org.bukkit.inventory import ItemStack
from org.bukkit.inventory.meta import LeatherArmorMeta
from org.bukkit import Color


@register_sign_type('give')
class GiveSign(SignBase):
    """
    items is a list of items to give the user.  Each item may have a
    description, and/or a single comment can be left to say to the player after
    all items have been delivered.

    give_item_color currently only works for leather armor.

    Format:

    - coordinates: [x, y, z]
      type: give
      items:
      - give_item: 2
        give_item_data: 0          [default: 0]
        give_item_amount: 1        [default: 1]
        give_item_desc: one grass  [default: null]
      - give_item: 276
        give_item_data: 0
        give_item_amount: 1
        give_item_desc: a sword
      - give_item: 299
        give_item_color: [255, 0, 0]
        give_item_desc: red armor
      comment: You get a car!      [default: null]
    """

    def onLeftClick(self, sign_data, plugin, event, sign):
        pass


    def onRightClick(self, sign_data, plugin, event, sign):
        player = event.getPlayer()

        given_items = []

        for item in sign_data["items"]:
            give_item = item["give_item"]
            give_item_data = item.get("give_item_data", 0)
            give_item_amount = item.get("give_item_amount", 1)
            give_item_desc = item.get("give_item_desc", None)
            give_item_color = item.get("give_item_color", None)

            itemstack = ItemStack(give_item, give_item_amount, give_item_data)

            if give_item_color is not None:
                red, green, blue = give_item_color
                if give_item >= 298 and give_item <= 301:
                    # Leather armor falls in this range
                    larmor = LeatherArmorMeta(itemstack.getItemMeta())
                    larmor.setColor(Color.fromRGB(red, green, blue))
                    itemstack.setItemMeta(larmor)

            if self.safe_give(player, itemstack):
                given_items.append(itemstack)
                if give_item_desc is not None:
                    self.message(player, "You've been given %s!" % give_item_desc)
            else:
                inventory = player.getInventory()
                for bad_item in given_items:
                    not_removed = inventory.removeItem(bad_item)
                    while not not_removed.isEmpty():
                        amount = 0
                        for entry in not_removed.entrySet():
                            amount += entry.getValue().getAmount()
                        bad_item.setAmount(bad_item.getAmount() - amount)
                        not_removed = inventory.removeItem(bad_item)
                player.updateInventory()
                self.message(player, "Please clean up your inventory a bit, there is no space :(")
                return
        
        player.updateInventory()

        comment = sign_data.get("comment", None)
        if comment is not None:
            self.message(player, comment)


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
