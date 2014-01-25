from baselistener import BaseListener
from org.bukkit import Bukkit
from org.bukkit.event.world import PortalCreateEvent
from bukkit_helpers import chatcolor


class PortalListener(BaseListener):

    def __init__(self, plugin):
        self.plugin = plugin

    def onEnable(self):
        self.register_event(self.onPortalCreateEvent, PortalCreateEvent)

    def onPortalCreateEvent(self, event):

        #Check to make sure that it's a portal being lit, not one automatically created by a teleport.
        if event.getReason() == PortalCreateEvent.CreateReason.FIRE:

            #Check if the player near has the permission to light, if so light it.
            for player in Bukkit.getServer().getOnlinePlayers():
                if player.hasPermission("omneity.portal.light"):
                    distance = player.getLocation().distanceSquared(event.getBlocks()[0].getLocation())
                    if distance > 5:
                        event.setCancelled(True)
                        player.sendMessage("-")
                        player.sendMessage(chatcolor.YELLOW + "You, or someone quite near, tried to light a portal.")
                        player.sendMessage(chatcolor.GREEN + "You were able to light that portal!")
                        player.sendMessage(chatcolor.RED + "If it was you that tried to light the portal,")
                        player.sendMessage(chatcolor.RED + "stand inside the portal and light it.")
                        player.sendMessage(chatcolor.GRAY + "This is very finicky - you might have to move up or sideways,")
                        player.sendMessage(chatcolor.GRAY + "especially for really large portals.")
                        player.sendMessage(chatcolor.GRAY + str(distance) + " square meters off - need to be under 5.")
                        player.sendMessage(chatcolor.YELLOW + "Otherwise, ask them to request your assistance in lighting it.")
                        player.sendMessage("-")
                        return
                    player.sendMessage(chatcolor.GREEN + "Portal successfully lit.")
                    return

            #Not able to light - continue on.
            event.setCancelled(True)

            for player in Bukkit.getServer().getOnlinePlayers():
                if player.getLocation().distanceSquared(event.getBlocks()[0].getLocation()) < 25:
                    player.sendMessage("-")
                    player.sendMessage(chatcolor.YELLOW + "You, or someone quite near, tried to light a portal.")
                    player.sendMessage(chatcolor.RED + "You'll have to modreq for one, as lighting your own is disabled.")
                    player.sendMessage("-")
                    return


listener = PortalListener
