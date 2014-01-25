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
                if (player.getLocation().distanceSquared(event.getBlocks()[0].getLocation()) < 25) and player.hasPermission("omneity.portal.light"):
                    return

            #Not able to light - continue on.
            event.setCancelled(True)

            for player in Bukkit.getServer().getOnlinePlayers():
                if player.getLocation().distanceSquared(event.getBlocks()[0].getLocation()) < 25:
                    player.sendMessage(chatcolor.YELLOW + "You, or someone quite near, tried to light a portal.")
                    player.sendMessage(chatcolor.RED + "You'll have to modreq for one, as lighting your own is disabled.")


listener = PortalListener
