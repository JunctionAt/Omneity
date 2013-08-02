from baselistener import BaseListener
from config import ConfigManager
from org.bukkit import Material
from org.bukkit.inventory import ItemStack, FurnaceRecipe, ShapedRecipe, ShapelessRecipe
from org.bukkit.material import MaterialData

from os import path


class RecipeListener(BaseListener):

	default_config = {
			'furnace': [
				{
					'result': {
						'id': 1,
						'amount': 1,    #default: 1
						'data': -1     #default: -1
					},
					'source': {
						'id': 1,
						'data': -1     #default: -1
					}
				}
			],
			'shape': [
				{
					'result': {
						'id': 1,
						'amount': 1,    #default: 1
						'data': -1     #default: -1
					},
					'shape': [
						"ABA",
						"BAB",
						"ABA"
					],
					'ingredients': {
						'A': {
							'id': 2,
							'data': -1     #default: -1
						}, 
						'B': {
							'id': 3,
							'data': -1     #default: -1
						}
					}
				}
			],
			'shapeless': [
				{
					'result': {
						'id': 1,
						'amount': 1,    #default: 1
						'data': -1     #default: -1
					},
					'ingredients': [
						{
							'id': 1,
							'amount': 1,    #default: 1 max: 9
							'data': -1     #default: 1-
						}
					]
				}
			]
		}

	def __init__(self, plugin):
		self.plugin = plugin

	def onEnable(self):
		self.config_manager = ConfigManager(path.join(self.plugin.getDataFolder().getAbsolutePath(), 'recipes.yml'), default=self.default_config)
		self.config_manager.load_config()

		server = self.plugin.getServer()

		for recipe_data in self.config_manager.config['furnace']:
			recipe = FurnaceRecipe(self.parse_itemstack(recipe_data['result']), self.parse_materialdata(recipe_data['source']))
			server.addRecipe(recipe)

		for recipe_data in self.config_manager.config['shape']:
			recipe = ShapedRecipe(self.parse_itemstack(recipe_data['result']))
			recipe.shape(recipe_data['shape'])
			for key, ingredient in recipe_data['ingredients'].iteritems():
				recipe.setIngredient(key, self.parse_materialdata(ingredient))
			server.addRecipe(recipe)

		for recipe_data in self.config_manager.config['shapeless']:
			recipe = ShapelessRecipe(self.parse_itemstack(recipe_data['result']))
			for ingredient in recipe_data['ingredients']:
				recipe.addIngredient(ingredient.get('amount', 1), self.parse_materialdata(ingredient))
			server.addRecipe(recipe)


	def parse_itemstack(self, data):
		return ItemStack(data['id'], data.get('amount', 1), data.get('data', -1))

	def parse_materialdata(self, data):
		return MaterialData(data['id'], data.get('data', -1))

	def onDisable(self):
		self.config_manager.save_config()


listener = RecipeListener