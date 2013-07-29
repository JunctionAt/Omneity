from __future__ import with_statement
from org.bukkit.event.player import PlayerInteractEvent
from org.bukkit.block import Sign
from org.bukkit.event.block import Action
from baselistener import BaseListener

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

	def __init__(self, plugin):
		self.plugin = plugin
		self.data_path = path.join(self.plugin.getDataFolder().getAbsolutePath(), 'signs.yml')

		self.register_event(self.onPlayerInteract, PlayerInteractEvent)

		if not path.exists(self.data_path):
			with open(self.data_path, 'w+') as f:
				f.write(yaml.dump(
					{
						'signs': [
							{
								'coordinates': [0, 0, 0],
								'type': 'teleport',
								'destination': [0, 0, 0]
							}
						]
					}))

	def onEnable(self):
		with open(self.data_path, 'r') as f:
			self.data = yaml.load(f)
		self.data_modified = False

	def onDisable(self):
		if self.data_modified:
			with open(self.data_path, 'w+') as f:
				f.write(yaml.dump(self.data))

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
		print sign_coords

		for sign_instance in self.data['signs']:
			if sign_instance['coordinates'] == sign_coords:
				type_handler = sign_types[sign_instance['type']]

				if event.getAction() == Action.LEFT_CLICK_BLOCK:
					type_handler.onLeftClick(sign_instance, self.plugin, event, sign)
				elif event.getAction() == Action.RIGHT_CLICK_BLOCK:
					type_handler.onRightClick(sign_instance, self.plugin, event, sign)
				else:
					return #Something is fucked, should raise a exception

		event.setCancelled(True)