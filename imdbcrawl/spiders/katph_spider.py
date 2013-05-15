import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from imdbcrawl.items import EpisodeTorrentItem

class KatphSpider(BaseSpider):
	name = "katph"
	episodeUrl = "http://kat.ph/media/getepisode/"
	allowed_domains = ["kat.ph"]
	#index of these urls will be used as primary key for linking related data
	start_urls = [
		"http://kat.ph/how-i-met-your-mother-tv3918/"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		data = dict()
		data["itemId"] = str(self.start_urls.index(response.url))
		data["itemName"] = "episodeTorrent"
		seasons = hxs.select("/html/body/div[4]/table/tr/td[1]/h3/text()").re('\d+')
		elemContainers = hxs.select("/html/body/div[4]/table/tr/td[1]/div[not(@class='advertising horizontalAdvert') and not(@class='torrentMediaInfo')]")
		for index , elemContainer in enumerate(elemContainers):
			episodes = elemContainer.select('div/div[1]/a/span[@class="versionsEpNo"]/text()').re("\d+")
			data["season"] = seasons[index]
			pageIds = elemContainer.select('div/div[1]/a/@onclick').re("\d+")

			for episodeIndex, pageId in enumerate(pageIds):
				data["episode"] = episodes[episodeIndex]
				yield Request(self.episodeUrl + pageId, meta = {"item" : data}, callback = self.parseTorrent)

	def parseTorrent(self, response):
		hxs = HtmlXPathSelector(response)
		item = EpisodeTorrentItem()
		item.update(response.meta["item"])
		item["torrents"] = {"titles" : hxs.select('/html/body/div/table/tr[not(@class="firstr")]/td[1]/div[2]/a[2]/text()').extract()}
		item["torrents"].update({"sizes" : hxs.select('/html/body/div/table/tr/td[2]/text()').extract()})
		item["torrents"].update({"units" : hxs.select('/html/body/div/table/tr/td[2]/span/text()').extract()})
		item["torrents"].update({"torrents" : hxs.select('/html/body/div/table/tr/td[1]/div[1]/a[5]/@href').extract()})
		item["torrents"].update({"leeches" : hxs.select('/html/body/div/table/tr/td[6]/text()').extract()})
		item["torrents"].update({"seeds" : hxs.select('/html/body/div/table/tr/td[5]/text()').extract()})
		item["torrents"].update({"magnets" : hxs.select('/html/body/div/table/tr/td[1]/div[1]/a[4]/@href').extract()})
		return item