# -*- coding: utf-8 -*-
import scrapy
from textblob import TextBlob

class ReviewsScraperSpider(scrapy.Spider):
    name = 'reviews_scraper'
    allowed_domains = ['amazon.com']

    # Product reviews URL
    product_url = 'https://www.amazon.com/' \
                  'GT-Speaker-Surround-Complete-Concealment/' \
                  'product-reviews/B01AMFJ9JA' \
                  '?ie=UTF8&pageNumber={}&reviewerType=all_reviews'
    page = 1
    start_urls = [product_url.format(page)]

    def parse(self, response):
        self.log('Current URL : ' + response.url)

        # Get all reviews
        reviews = response.css('div.review')
        for review in reviews:
            title = review.css('a.review-title::text').extract_first()
            text = review.css('span.review-text::text').extract_first()
            sentiment = self.sentiment_classification(text)

            yield {
                'sentiment' : sentiment,
                'title': title,
                'text': text,
            }

        # Pagination handler
        if self.page != response.css('li.page-button > a::text')[-1].extract():
            self.page += 1
            next_page = self.product_url.format(self.page)
            yield scrapy.Request(url=next_page, callback=self.parse)


    def sentiment_classification(self, text):
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0:
            return 'positive'
        elif polarity < 0:
            return 'negative'
        else:
            return 'neutral'