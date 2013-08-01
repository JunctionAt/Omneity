from org.bukkit.event.player import PlayerCommandPreprocessEvent
from org.bukkit.event.server import ServerCommandEvent
from bukkit_helpers import chatcolor
from baselistener import BaseListener


aliases = dict()
aliases_console = dict()

def register_alias(command_name, permission=None, console=False):
	def wrap(func):

		pack = dict(func=func, permission=permission)

		if console:
			alias_dict = aliases_console
		else:
			alias_dict = aliases

		if isinstance(command_name, str):
			alias_dict[command_name.lower()] = pack
		elif isinstance(command_name, list):
			for command in command_name:
				alias_dict[command.lower()] = pack
		else:
			raise AttributeError()

	return wrap


class Abort(Exception):
	pass

#@register_alias("test")
#def test_alias(plugin, event, args):
#	plugin.getServer().dispatchCommand(event.getPlayer(), "/what");
#	event.getPlayer().sendMessage("Works")

import modtools, help, debug, stupid, tier2


class AliasListener(BaseListener):

	def __init__(self, plugin):
		self.plugin = plugin

	def onEnable(self):
		self.register_event(self.onPlayerCommandPreprocess, PlayerCommandPreprocessEvent)
		self.register_event(self.onServerCommand, ServerCommandEvent, priority="highest")

	def onPlayerCommandPreprocess(self, event):

		args = event.getMessage().split(" ")
		alias = aliases.get(args[0][1:].lower())

		if alias is None:
			return

		if alias.get("permission") and not event.getPlayer().hasPermission(alias.get("permission")):
			event.getPlayer().sendMessage(chatcolor.RED + "You don't have permission for this command")
			event.setCancelled(True) 
			return

		try:
			alias.get("func")(self.plugin, event, args[1:])
		except Abort:
			return

		event.setCancelled(True) 

	def onServerCommand(self, event):

		args = event.getCommand().split(" ")
		alias = aliases_console.get(args[0].lower())

		if alias is None:
			return

		try:
			alias.get("func")(self.plugin, event, args[1:])
		except Abort:
			return

		event.setCommand("nullcommand")

listener = AliasListener