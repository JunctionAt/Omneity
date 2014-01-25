from bukkit_helpers import chatcolor
from . import register_alias, Abort

from org.bukkit.World import strikeLightning

@register_alias("thor", permission='omneity.aliases.thor')
def thor(plugin, event, args):
    if len(args) != 1:
        event.getPlayer().sendMessage("Invalid usage, correct is: /thor <player>")
        return

    player = args[0]
    strikeLightning(player.getLocation())
    player.setHealth(0)
    event.getPlayer().sendMessage(chatcolor.LIGHT_PURPLE + "Thou hast smote the evil player " + player + " with thy mighty hand.")
    player.sendMessage(chatcolor.RED + "You have been smote by Thor's Hammer!")
    plugin.getServer().dispatchCommand(event.getPlayer(), "sc I have smitten %s" % player)
