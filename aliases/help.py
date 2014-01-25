from bukkit_helpers import chatcolor
from . import register_alias, Abort


@register_alias("bukkit-help")
def bukkit_help(plugin, event, args):
	plugin.getServer().dispatchCommand(event.getPlayer(), "help %s" % ' '.join(args))


@register_alias("help")
def help(plugin, event, args):
	event.getPlayer().sendMessage(
		chatcolor.GOLD + "Please see " +
		chatcolor.WHITE + "https://junction.at/wiki/help" +
		chatcolor.GOLD + " for the help page"
		)

	if event.getPlayer().hasPermission("bukkit.command.help"):
		event.getPlayer().sendMessage(
			chatcolor.GOLD + "or " +
			chatcolor.WHITE + "/bukkit-help" +
			chatcolor.GOLD + " for Bukkit's /help listing."
			)
