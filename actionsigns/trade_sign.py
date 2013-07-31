from . import register_sign_type, SignBase
from bukkit_helpers import chatcolor
from org.bukkit.inventory import ItemStack


@register_sign_type('trade')
class TeleportSign(SignBase):
	"""
	Format:

	- location: [x, y, z]
	  type: trade
	  take_item: 1
	  take_item_data: 0     [default: 0]
	  take_item_amount: 1   [default: 1]
	  give_item: 2
	  give_tiem_data: 0     [default: 0]
	  give_item_amount: 1   [default: 1]
	"""
	
	def onLeftClick(self, sign_data, plugin, event, sign):
		pass

	def onRightClick(self, sign_data, plugin, event, sign):
		item = event.getItem()
		player = event.getPlayer()
		inventory = player.getInventory()

		take_item = sign_data["take_item"]
		take_item_data = sign_data.get("take_item_data", 0)
		take_item_amount = sign_data.get("take_item_amount", 1)
		give_item = sign_data["give_item"]
		give_item_data = sign_data.get("give_item_data", 0)
		give_item_amount = sign_data.get("give_item_amount", 1)


		if not item:
			self.message(player, "Please hold the item you want to trade in your hand.")
			return

		# Check if the player holds the correct item
		if item.getTypeId() != take_item or item.getDurability() != take_item_data:
			self.message(player, "Please hold the item you want to trade in your hand.")
			return

		# Check that the player has the correct amount
		if item.getAmount() < take_item_amount:
			self.message(player, "Make sure you have enough of the item you want to trade.")
			return


		if self.safe_give(player, ItemStack(give_item, give_item_amount, give_item_data)):

			if take_item_amount == item.getAmount():
				player.setItemInHand(None)
			else:
				item.setAmount(item.getAmount() - take_item_amount)

			self.message(player, "Trade completed. Please have a nice day!")
		else:
			self.message(player, "Please clean up your inventory a bit, there is no space :(")

		player.updateInventory()

	def safe_give(self, player, itemstack):
		inventory = player.getInventory()

		print itemstack

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