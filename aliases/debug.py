from bukkit_helpers import chatcolor
from . import register_alias, Abort


@register_alias("ircsay", console=True)
def ircsay(plugin, event, args):
	if len(args) < 2:
		return

	user = args[0]

	args.pop(0)

	plugin.getServer().broadcastMessage(
		chatcolor.GREEN + "IRC " +
		chatcolor.WHITE + "<" + args[0] + "> " + ' '.join(args)
		)

@register_alias("test_permission")
def test_permission(plugin, event, args):
	player = event.getPlayer()

	if player.hasPermission(args[0]):
		plugin.getPlayer().sendMessage("yes")
	else:
		plugin.getPlayer().sendMessage("no")