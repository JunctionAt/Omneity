from __future__ import with_statement
import yaml
from os import path


class ConfigManager(object):

	def __init__(self, config_path, default={}):
		self.config_path = config_path
		self.default_config = default
		self.data_modified = False
		self.config = None

	def load_config(self):
		if not path.exists(self.config_path):
			with open(self.config_path, 'w+') as f:
				f.write(yaml.dump(self.default_config))

		with open(self.config_path, 'r') as f:
			self.config = yaml.load(f)
		self.data_modified = False

	def save_config(self):
		if self.data_modified:
			with open(self.config_path, 'w+') as f:
				f.write(yaml.dump(self.config))

	def reload_config(self):
		self.save_config()
		self.load_config()

	def mark_config_dirty(self):
		self.data_modified = True