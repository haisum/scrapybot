import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from imdbcrawl.items import ShowItem, EpisodeItem

class ImdbSpider(BaseSpider):
	name = "imdb"
	allowed_domains = ["imdb.com"]
	currentRequestCount = {}
	"""
	add more comma separated urls as you want
	but do remember, to keep same sequence in torrent crawler
	for example if here first is game of thrones, and second url is for supernatural
	same order of urls should be inside torrent spider's start_urls
	This order, is used to determine which torrent belongs to which show
	"""
	start_urls = [
		"http://www.imdb.com/title/tt0944947/?ref_=sr_1",# Game of thrones
		"http://www.imdb.com/title/tt0460681/?ref_=fn_al_tt_1",# Supernatural
		"http://www.imdb.com/title/tt0773262/?ref_=sr_1",#Dexter
		"http://www.imdb.com/title/tt1520211/?ref_=sr_1",#Walking dead
		"http://www.imdb.com/title/tt0898266/?ref_=sr_1",#The Big Bang Theory
		"http://www.imdb.com/title/tt0460649/?ref_=sr_1"#HIMYM
	]

	def parse(self, response):
		"""
		parse first imdb page for show and grab links for season wise listings
		"""
		hxs = HtmlXPathSelector(response)
		show = ShowItem()
		show["itemId"] = str(self.start_urls.index(response.url))
		show["itemName"] = "show"
		show["title"] = hxs.select('//*[@id="overview-top"]/h1/span[1]/text()').extract()[0]
		self.currentRequestCount[show["title"]] = 0
		show["years"] = hxs.select('//*[@id="overview-top"]/h1/span[2]/text()').extract()[0]
		show["rating"] = hxs.select('//*[@id="overview-top"]/div[2]/div[1]/text()').extract()[0]
		show["imdbUrl"] = response.url
		show["summary"] = hxs.select('//*[@id="overview-top"]/p[2]/text()').extract()[0]
		show["image"] = hxs.select('//*[@id="img_primary"]/div/a/img/@src').extract()[0]
		show["showId"] = re.search(r"title/tt(\d+)/" ,response.url).group(1)
		
		seasons = hxs.select('//*[@id="titleTVSeries"]/div[2]/span/a')
		totalSeasons = len(seasons)
		show["seasons"] = {}
		for season in seasons:
			url = "http://" + self.allowed_domains[0] + season.select("@href").extract()[0]
			"""
			create dictionary in seasons and let keys be season numbers
			To fix, proper json parsing for js, we are prepending season so that object name starts with a string
			"""
			currentSeason = season.select("text()").extract()[0]
			show["seasons"].update({"season" + currentSeason : []})
			#request season page, and parse episode data in each season object
			yield Request(url , callback = self.parseEpisode, meta = {"show" : show, "totalSeasons" : totalSeasons, "currentSeason" : currentSeason})
	
	def parseEpisode(self, response):
		hxs = HtmlXPathSelector(response)
		items = hxs.select('//*[@id="episodes_content"]/div[2]/div[2]/div')
		for item in items:
			episode = EpisodeItem()
			episode["itemName"] = "episode"
			episode["itemId"] = response.meta["show"]["itemId"]
			episode["title"] = item.select("div[2]/strong/a/text()").extract()[0]
			"""
			Sometimes summary isn't available on imdb
			"""
			try:
				episode["summary"] = item.select('div[2]/div[2]/text()').extract()[0]
			except IndexError:
				episode["summary"] = ""
			episode["date"] = item.select('div[2]/div[1]/text()').extract()[0]
			episode["episode"] = item.select('div[1]/a/div/div/text()').re('\d+')[1]
			episode["season"] = response.meta["currentSeason"]
			episode["image"] = item.select('div[1]/a/div/img/@src').extract()[0]
			episode["imdbUrl"] = response.url
			response.meta["show"]["seasons"]["season"+response.meta["currentSeason"]].append(episode)
		"""
		Only return response when this request is final request, otherwise we will return 
		incomplete objects multiple times
		"""
		self.currentRequestCount[response.meta["show"]["title"]] = self.currentRequestCount[response.meta["show"]["title"]]+ 1
		if(self.currentRequestCount[response.meta["show"]["title"]] == response.meta["totalSeasons"]):
			return response.meta["show"]
		else:
			return None