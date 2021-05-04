import re
import scrapy
from scrapy.selector import Selector
from datetime import datetime, timedelta


def extract_news(html: str, xpath: str) -> str:
    return Selector(text=html).xpath(xpath).get()


def abs_url(rel_url: str) -> str:
    return f"https://zingnews.vn{rel_url}"


def extract_id_from_url(url: str) -> str:
    result = re.search("post\d{1,}.html", url)
    post_id = re.findall("\d", result.group(0))
    return ''.join(post_id)


def convert_datetime(datetime: str, now: datetime) -> str:
    ''' Convert "{n} hour(s) ago" or "{n} minute(s) ago" to approximate datetime '''
    extracted_datetime = datetime.split()
    if (extracted_datetime[1].find("giờ") == 0):
        return (now - timedelta(hours=int(extracted_datetime[0]))).strftime("%H:%M %#d/%#m/%Y")
    elif (extracted_datetime[1].find("phút") == 0):
        return (now - timedelta(minutes=int(extracted_datetime[0]))).strftime("%H:%M %#d/%#m/%Y")
    return datetime


class ZingnewsSpider(scrapy.Spider):
    name = 'zingnews_spider'
    allowed_domains = ['https://zingnews.vn']

    # target urls
    start_urls = [
        'https://zingnews.vn/thoi-su.html',
        'https://zingnews.vn/chinh-tri.html',
        'https://zingnews.vn/nhan-su-moi.html',
        'https://zingnews.vn/giao-thong.html',
        'https://zingnews.vn/do-thi.html',
        'https://zingnews.vn/phap-luat.html',
        'https://zingnews.vn/vu-an.html',
        'https://zingnews.vn/phap-dinh.html',
        'https://zingnews.vn/the-gioi.html',
        'https://zingnews.vn/tu-lieu-the-gioi.html',
        'https://zingnews.vn/phan-tich-the-gioi.html',
        'https://zingnews.vn/nguoi-viet-4-phuong.html',
        'https://zingnews.vn/chuyen-la-the-gioi.html',
        'https://zingnews.vn/kinh-doanh-tai-chinh.html',
        'https://zingnews.vn/hang-khong.html',
        'https://zingnews.vn/bat-dong-san.html',
        'https://zingnews.vn/tieu-dung.html',
        'https://zingnews.vn/thuong-mai-dien-tu.html',
        'https://zingnews.vn/ttdn.html',
        'https://zingnews.vn/cong-nghe.html',
        'https://zingnews.vn/mobile.html',
        'https://zingnews.vn/internet.html',
        'https://zingnews.vn/esports.html',
        'https://zingnews.vn/suc-khoe.html',
        'https://zingnews.vn/khoe-dep.html',
        'https://zingnews.vn/dinh-duong.html',
        'https://zingnews.vn/me-va-be.html',
        'https://zingnews.vn/benh-thuong-gap.html',
        'https://zingnews.vn/the-thao.html',
        'https://zingnews.vn/bong-da-viet-nam.html',
        'https://zingnews.vn/bong-da-anh.html',
        'https://zingnews.vn/vo-thuat.html',
        'https://zingnews.vn/esports-the-thao.html',
        'https://zingnews.vn/giai-tri.html',
        'https://zingnews.vn/sao-viet.html',
        'https://zingnews.vn/am-nhac.html',
        'https://zingnews.vn/thoi-trang.html',
        'https://zingnews.vn/phim-anh.html',
        'https://zingnews.vn/doi-song.html',
        'https://zingnews.vn/gioi-tre.html',
        'https://zingnews.vn/xu-huong.html',
        'https://zingnews.vn/song-dep.html',
        'https://zingnews.vn/su-kien.html',
        'https://zingnews.vn/giao-duc.html',
        'https://zingnews.vn/tuyen-sinh-dai-hoc.html',
        'https://zingnews.vn/tu-van-giao-duc.html',
        'https://zingnews.vn/du-hoc.html',
        'https://zingnews.vn/tieu-diem/hoc-tieng-anh.html',
        'https://zingnews.vn/du-lich.html',
        'https://zingnews.vn/dia-diem-du-lich.html',
        'https://zingnews.vn/am-thuc.html',
        'https://zingnews.vn/phuot.html',
        'https://zingnews.vn/tieu-diem/du-lich-theo-mua.html',
        'https://zingnews.vn/oto-xe-may.html',
        'https://zingnews.vn/oto.html',
        'https://zingnews.vn/xe-dien.html',
        'https://zingnews.vn/danh-gia.html',
        'https://zingnews.vn/xe-may.html',
        'https://zingnews.vn/du-thuyen.html'
    ]

    def parse(self, response):
        now = datetime.now()
        articles = response.xpath('//*[@id="news-latest"]//article')
        for article in articles:
            rel_url = extract_news(
                article.get(), '//p[@class="article-title"]/a/@href')
            yield {
                'id': extract_id_from_url(rel_url),
                'title': extract_news(article.get(), '//p[@class="article-title"]/a/text()'),
                'url': abs_url(rel_url),
                'description': extract_news(article.get(), '//p[@class="article-summary"]/text()'),
                'thumbnail': extract_news(article.get(), '//p[@class="article-thumbnail"]/a/img/@data-src'),
                'category_parent': extract_news(article.get(), '//span[@class="category-parent"]/text()'),
                'category': extract_news(article.get(), '//span[@class="category"]/text()'),
                'time': convert_datetime(extract_news(article.get(), '//span[@class="friendly-time"]/text()'), now)
            }
