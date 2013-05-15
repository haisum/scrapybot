# Scrapy settings for imdbcrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'imdbcrawl'

SPIDER_MODULES = ['imdbcrawl.spiders']
NEWSPIDER_MODULE = 'imdbcrawl.spiders'
LOG_FILE = "log.txt"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'imdbcrawl (+http://www.yourdomain.com)'
