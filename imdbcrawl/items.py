# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ShowItem(Item):
	itemName = Field()
	itemId = Field()
	showId = Field()
	title = Field()
	rating = Field()
	summary = Field()
	years = Field()
	imdbUrl = Field()
	image = Field()
	seasons = Field()

class EpisodeItem(Item):
	itemName = Field()
	itemId = Field()
	title = Field()
	imdbUrl = Field()
	summary = Field()
	date = Field()
	episode = Field()
	season = Field()
	image = Field()

class EpisodeTorrentItem(Item):
	itemName = Field()
	itemId = Field()
	episode = Field()
	season = Field()
	torrents = Field()
	"""
	You can access following properties via torrents dictionary 
	example: following will give you title and torrent link of first torrent of current episode:
	myEpisodeTorrentItem["torrents"]["titles"][0] + episodeTorrentItem["torrents"]["torrents"][0] 
	"""
	# titles = []
	# sizes = []
	# seeds = []
	# leachs = []
	# magnets = []
	# torrents = []