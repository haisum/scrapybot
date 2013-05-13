import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from imdbcrawl.items import ShowItem, EpisodeItem

class ImdbSpider(BaseSpider):
	name = "imdb"
	allowed_domains = ["imdb.com"]
	#index of these urls will be used as primary key for linking related data
	start_urls = [
		"http://www.imdb.com/title/tt0460681/?ref_=fn_al_tt_1",
		"http://www.imdb.com/title/tt0944947/?ref_=sr_2"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		show = ShowItem()
		show["itemId"] = self.start_urls.index(response.url)
		show["itemName"] = "show"
		show["title"] = hxs.select('//*[@id="overview-top"]/h1/span[1]/text()').extract()[0]
		show["years"] = hxs.select('//*[@id="overview-top"]/h1/span[2]/text()').extract()[0]
		show["rating"] = hxs.select('//*[@id="overview-top"]/div[2]/div[1]/text()').extract()[0]
		show["imdbUrl"] = response.url
		show["summary"] = hxs.select('//*[@id="overview-top"]/p[2]/text()').extract()[0]
		show["image"] = hxs.select('//*[@id="img_primary"]/div/a/img/@src').extract()[0]
		show["showId"] = re.search(r"title/tt(\d+)/" ,response.url).group(1)
		yield show
		
		seasons = hxs.select('//*[@id="titleTVSeries"]/div[2]/span/a')
		for season in seasons:
			url = "http://" + self.allowed_domains[0] + season.select("@href").extract()[0]
			yield Request(url , callback = self.parseEpisode, meta = {"showId" : show["showId"]})
	
	def parseEpisode(self, response):
		hxs = HtmlXPathSelector(response)
		items = hxs.select('//*[@id="episodes_content"]/div[2]/div[2]/div')
		episodes = []
		for item in items:
			episode = EpisodeItem()
			episode["itemName"] = "episode"
			episode["title"] = item.select("div[2]/strong/a/text()").extract()[0]
			episode["summary"] = item.select('div[2]/div[2]/text()').extract()[0]
			episode["date"] = item.select('div[2]/div[1]/text()').extract()[0]
			episode["episode"] = item.select('div[1]/a/div/div/text()').re('\d+')[1]
			episode["season"] = item.select('div[1]/a/div/div/text()').re('\d+')[0]
			episode["image"] = item.select('div[1]/a/div/img/@src').extract()[0]
			episode["imdbUrl"] = response.url
			episode["showId"] = response.meta["showId"]
			episodes.append(episode)
		return episodes
		# items = []
		# for site in sites:
		#     item = DmozItem()
		#     item['title'] = site.select('a/text()').extract()
		#     item['link'] = site.select('a/@href').extract()
		#     item['desc'] = site.select('text()').extract()
		#     items.append(item)
		# return items