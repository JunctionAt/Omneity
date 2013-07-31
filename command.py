from org.bukkit.command import Command
from org.bukkit import Bukkit
from org.bukkit.plugin import SimplePluginManager
from org.bukkit.command import Command


_commandmap_field = SimplePluginManager.getDeclaredField("commandMap")
_commandmap_field.setAccessible(True)
commandmap = _commandmap_field.get(Bukkit.getPluginManager())


class PythonCommand(Command):

	def __init__(self, name, description, usage, aliases):
		super(Command, self).__init__(name, description, usage, aliases)
	
	def execute(self, sender, label, args):
		print label
		print args


def register_command(command_name, description="", usage="/<command>", aliases=[]):
	command = PythonCommand(command_name, description, usage, aliases)
	commandmap.register("/", command)