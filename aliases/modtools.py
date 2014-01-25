from bukkit_helpers import chatcolor
from . import register_alias, Abort


@register_alias(["i", "item"])
def give_item(plugin, event, args):

	player = event.getPlayer()

	block_id = block_data = 0
	amount = 64

	# check if input is valid yo
	if len(args) < 1 or len(args) > 2:
		player.sendMessage("/i <item>[:data] [amount]")
		return

	# parse item/data
	if ":" in args[0]:
		block_id, block_data = args[0].split(":")
	else:
		block_id = args[0]

	# parse amount
	if len(args) == 2:
		amount = int(args[1])

	plugin.getServer().dispatchCommand(event.getPlayer(), "give %s %s %d %s" % (player.getName(), block_id, amount, block_data));

@register_alias("give")
def give_check(plugin, event, args):
	if event.getPlayer().getName().lower() == args[0].lower():
		raise Abort()

	event.getPlayer().sendMessage(chatcolor.RED + "no")

@register_alias("lbrb")
def lbrb(plugin, event, args):
	if len(args) != 1:
		event.getPlayer().sendMessage("Invalid usage, correct is: /lbrb <player>")
		return

	plugin.getServer().dispatchCommand(event.getPlayer(), "lb rollback player %s area 10000 since 30 days" % args[0])

@register_alias("lbrb-r")
def lbrb(plugin, event, args):
	if len(args) != 2:
		event.getPlayer().sendMessage("Invalid usage, correct is: /lbrb-r <player> <radius>")
		return

	plugin.getServer().dispatchCommand(event.getPlayer(), "lb rollback player %s area %s since 30 days" % (args[0], args[1]))

@register_alias("rbban")
def lbrb(plugin, event, args):
	if len(args) != 2:
		event.getPlayer().sendMessage("Invalid usage, correct is: /rbban <player> <reason>")
		return

	plugin.getServer().dispatchCommand(event.getPlayer(), "ban %s %S" % (args[0], args[1]))
	plugin.getServer().dispatchCommand(event.getPlayer(), "lb rollback player %s area 10000 since 30 days" % args[0])

@register_alias("trace")
def lbrb(plugin, event, args):
	if len(args) != 1:
		event.getPlayer().sendMessage("Invalid usage, correct is: /trace <player>")
		return

	plugin.getServer().dispatchCommand(event.getPlayer(), "lb lookup player %s sum blocks" % args[0])

@register_alias("trace-xray")
def lbrb(plugin, event, args):
	if len(args) < 1:
		event.getPlayer().sendMessage("Invalid usage, correct is: /trace-xray <player> [<days>]")
		return
	if len(args) == 1:
		plugin.getServer().dispatchCommand(event.getPlayer(), "lb lookup player %s sum blocks block 1 block 56 block 14 block 129" % args[0])
		return
	if len(args) == 2:
		plugin.getServer().dispatchCommand(event.getPlayer(), "lb lookup player %s sum blocks block 1 block 56 block 14 block 129 since %s days" % (args[0], args[1]))
		return

@register_alias("staffchest")
def staffchest(plugin, event, args):
	plugin.getServer().dispatchCommand(event.getPlayer(), "cmodify g:base_assistance")

@register_alias("unstaff")
def unstaffchest(plugin, event, args):
	plugin.getServer().dispatchCommand(event.getPlayer(), "cmodify -g:base_assistance")
