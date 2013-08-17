from command import register_command
from baselistener import BaseListener
from bukkit_helpers import chatcolor
from org.bukkit.entity import Player
from org.bukkit import ChatColor


class MessageListener(BaseListener):

	def __init__(self, plugin):
		self.plugin = plugin

	def onEnable(self):
		self.reply_states = dict()

		register_command(self.messageCommand, 'message', aliases=['m', 'msg'], description="Send a message to a online player.", usage="/<command> <player> <message>")
		register_command(self.replyCommand, 'reply', aliases=['r'], description="Reply to a message.", usage="/<command> <message>")

	def onDisable(self):
		self.config_manager.save_config()

	def messageCommand(self, sender, alias, args):

		if isinstance(sender, Player):
			if len(args < 2):
				return False

			destination = self.getPlayerByShortName(args.pop(0))
			if destination is None:
				sender.sendMessage(chatcolor.RED + "Could not find that player.")

			self.reply_states[sender.getName()] = destination.getName()

			message = ' '.join(args)

			self.sendNiceMessage(sender, destination, message)
		else:
			sender.sendMessage("Only players may use this command.")

	def replyCommand(self, sender, alias, args):
		if isinstance(sender, Player):
			if len(args < 1):
				return False

			destinationName = self.reply_states.get(sender.getName(), None)
			if destinationName is None:
				sender.sendMessage(chatcolor.RED + "There is nothing to reply to.")
			destination = self.plugin.getServer().getPlayerExact(destinationName)
			if destination is None:
				sender.sendMessage(chatcolor.RED + "%s is no longer online." % destinationName)

			message = ' '.join(args)

			self.sendNiceMessage(sender, destination, message)
		else:
			sender.sendMessage("Only players may use this command.")


	def sendNiceMessage(self, source, destination, message):
		source.sendMessage(self.formatMessage("Me", destination.getName(), message))
		destination.sendMessage(self.formatMessage(source.getName(), "Me", message))

	def formatMessage(self, source, destination, message):
		return "[" + \
			chatcolor.RED + source +\
			chatcolor.WHITE + " -> " +\
			chatcolor.GOLD + destination +\
			chatcolor.WHITE + "] " +\
			message

	def getPlayerByShortName(self, name):
		players = self.plugin.getServer().getOnlinePlayers()

		lowername = name.lower()
		found = None
		delta = 9001
		for player in players:
			if ChatColor.stripColor(plauer.getName()).lower().startswith(lowername):
				curdelta = len(player.getName()) - len(lowername)
				if curdelta < delta:
					found = player
					delta = curdelta
				if curdelta == 0:
					break

		return found


listener = MessageListener