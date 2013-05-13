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

class EpisodeItem(Item):
	itemName = Field()
	showId = Field()
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
	# title = Field()
	# size = Field()
	# seed = Field()
	# leach = Field()
	# magnet = Field()
	# torrent = Field()