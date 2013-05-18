import copy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from imdbcrawl.items import TorrentItem

class KatphSpider(BaseSpider):
	name = "katph"
	episodeUrl = "http://kat.ph/media/getepisode/"
	allowed_domains = ["kat.ph"]
	#index of these urls will be used as primary key for linking related data
	start_urls = [
		"http://kat.ph/the-vampire-diaries-tv21766/",
		"http://kat.ph/breaking-bad-tv18164/",
		"http://kat.ph/prison-break-tv4895/",
		"http://kat.ph/sherlock-tv23433/",
		"http://kat.ph/house-tv3908/",
		"http://kat.ph/californication-tv15319/"
	]
	"""
	This number is added in itemId
	"""
	start_index = 6

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		torrent = TorrentItem()
		torrent["itemId"] = str(self.start_urls.index(response.url) + self.start_index)
		torrent["itemName"] = "torrent"
		seasons = hxs.select("/html/body/div[4]/table/tr/td[1]/h3/text()").re('\d+')
		elemContainers = hxs.select("/html/body/div[4]/table/tr/td[1]/div[not(@class='advertising horizontalAdvert') and not(@class='torrentMediaInfo')]")
		for index , elemContainer in enumerate(elemContainers):
			episodes = elemContainer.select('div/div[1]/a/span[@class="versionsEpNo"]/text()').re("\d+")
			torrent["season"] = seasons[index]
			pageIds = elemContainer.select('div/div[1]/a/@onclick').re("\d+")

			for episodeIndex, pageId in enumerate(pageIds):
				torrent["episode"] = episodes[episodeIndex]
				yield Request(self.episodeUrl + pageId, meta = {"torrent" : copy.deepcopy(torrent)}, callback = self.parseTorrent)

	def parseTorrent(self, response):
		hxs = HtmlXPathSelector(response)
		torrent = response.meta["torrent"]
		torrents = []
		item = {"titles" : hxs.select('/html/body/div/table/tr[not(@class="firstr")]/td[1]/div[2]/a[2]/text()').extract()}
		item.update({"sizes" : hxs.select('/html/body/div/table/tr/td[2]/text()').extract()})
		item.update({"units" : hxs.select('/html/body/div/table/tr/td[2]/span/text()').extract()})
		item.update({"torrents" : hxs.select('/html/body/div/table/tr/td[1]/div[1]/a[5]/@href').extract()})
		item.update({"leeches" : hxs.select('/html/body/div/table/tr/td[6]/text()').extract()})
		item.update({"seeds" : hxs.select('/html/body/div/table/tr/td[5]/text()').extract()})
		item.update({"magnets" : hxs.select('/html/body/div/table/tr/td[1]/div[1]/a[4]/@href').extract()})
		for index in xrange(0 , len(item["titles"])-1):
			tempTorrent = copy.deepcopy(torrent)
			tempTorrent["title"] = item["titles"][index]
			tempTorrent["size"] = item["sizes"][index]
			tempTorrent["unit"] = item["units"][index]
			tempTorrent["seeds"] = item["seeds"][index]
			tempTorrent["leeches"] = item["leeches"][index]
			tempTorrent["magnet"] = item["magnets"][index]
			tempTorrent["torrent"] = item["torrents"][index]
			torrents.append(tempTorrent)
		return torrents