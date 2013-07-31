from __future__ import with_statement
from org.bukkit.event.player import PlayerInteractEvent
from org.bukkit.block import Sign
from org.bukkit.event.block import Action
from baselistener import BaseListener
from command import register_command
from config import ConfigManager

import yaml
from os import path


class SignBase(object):
	def onLeftClick(self, sign_data, plugin, event, sign):
		pass

	def onRightClick(self, sign_data, plugin, event, sign):
		pass


sign_types = dict()

def register_sign_type(sign_type):
	def wrap(cls):
		sign_types[sign_type] = cls()
	return wrap

import teleport_sign, trade_sign

class ActionSignListener(BaseListener):

	default_data = {
			'signs': [
				{
					'coordinates': [0, 0, 0],
					'type': 'teleport',
					'destination': [0, 0, 0]
				}
			]
		}

	def __init__(self, plugin):
		self.plugin = plugin

		self.register_event(self.onPlayerInteract, PlayerInteractEvent)

		register_command(self.reload_command, 'reload-sign-config', permission="omneity.actionsigns.reload")

	def onEnable(self):
		self.config_manager = ConfigManager(path.join(self.getDataFolder().getAbsolutePath(), 'signs.yml'), default=self.default_config)
		self.config_manager.load_config()

	def onDisable(self):
		self.config_manager.save_config()

	def onPlayerInteract(self, event):

		block = event.getClickedBlock()

		if block is None:
			return
		
		block_state = block.getState()

		if not isinstance(block_state, Sign):
			return

		sign = block_state

		if not sign.getLine(0).lower().endswith("sign"):
			return

		sign_coords = [block.getX(), block.getY(), block.getZ()]

		for sign_instance in self.config_manager.config['signs']:
			if sign_instance['coordinates'] == sign_coords:
				type_handler = sign_types[sign_instance['type']]

				if event.getAction() == Action.LEFT_CLICK_BLOCK:
					type_handler.onLeftClick(sign_instance, self.plugin, event, sign)
				elif event.getAction() == Action.RIGHT_CLICK_BLOCK:
					type_handler.onRightClick(sign_instance, self.plugin, event, sign)
				else:
					return #Something is fucked, should raise a exception

		event.setCancelled(True)

	def reload_command(self, sender, label, args):
		self.config_manager.reload_config()
		sender.sendMessage("Reloaded sign config")

listener = ActionSignListener