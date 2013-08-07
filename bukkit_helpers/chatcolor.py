from org.bukkit import ChatColor

class ColorObj(dict):

	def __setattr__(self, name, color):
		self[name] = color
		#super(dict, self).__setitem__(name, color)

	def __getattr__(self, name):
		return self[name]

colors = ColorObj()

colors.BOLD = BOLD = unicode(ChatColor.BOLD)
colors.ITALIC = ITALIC = unicode(ChatColor.ITALIC)
colors.MAGIC = MAGIC = unicode(ChatColor.MAGIC)
colors.RESET = RESET = unicode(ChatColor.RESET)
colors.STRIKETHROUGH = STRIKETHROUGH = unicode(ChatColor.STRIKETHROUGH)
colors.UNDERLINE = UNDERLINE = unicode(ChatColor.UNDERLINE)

colors.AQUA = AQUA = unicode(ChatColor.AQUA)
colors.BLACK = BLACK = unicode(ChatColor.BLACK)
colors.BLUE = BLUE = unicode(ChatColor.BLUE)
colors.GOLD = GOLD = unicode(ChatColor.GOLD)
colors.GRAY = GRAY = unicode(ChatColor.GRAY)
colors.GREEN = GREEN = unicode(ChatColor.GREEN)
colors.RED = RED = unicode(ChatColor.RED)
colors.WHITE = WHITE = unicode(ChatColor.WHITE)
colors.YELLOW = YELLOW = unicode(ChatColor.YELLOW)

colors.LIGHT_PURPLE = LIGHT_PURPLE = unicode(ChatColor.LIGHT_PURPLE)

colors.DARK_AQUA = DARK_AQUA = unicode(ChatColor.DARK_AQUA)
colors.DARK_BLUE = DARK_BLUE = unicode(ChatColor.DARK_BLUE)
colors.DARK_GRAY = DARK_GRAY = unicode(ChatColor.DARK_GRAY)
colors.DARK_GREEN = DARK_GREEN = unicode(ChatColor.DARK_GREEN)
colors.DARK_PURPLE = DARK_PURPLE = unicode(ChatColor.DARK_PURPLE)
colors.DARK_RED = DARK_RED = unicode(ChatColor.DARK_RED)