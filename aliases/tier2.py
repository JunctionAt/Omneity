from bukkit_helpers import chatcolor
from . import register_alias, Abort


@register_alias("tpc")
def tpc(plugin, event, args):
	plugin.getServer().dispatchCommand(event.getPlayer(), "tpclaim %s" % ' '.join(args))

@register_alias("modmode")
def tpc(plugin, event, args):
	plugin.getServer().dispatchCommand(event.getPlayer(), "mode")

@register_alias("modlist")
def tpc(plugin, event, args):
	plugin.getServer().dispatchCommand(event.getPlayer(), "staff")
