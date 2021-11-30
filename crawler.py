import requests
from bs4 import BeautifulSoup
import codecs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

yahooData = [
    [
        # NEW ARRIVAL 6個商品
        'https://store.shopping.yahoo.co.jp/',

        # NEW ARRIVAL 10個slider
        'https://store.shopping.yahoo.co.jp/',
    ],
    [
        # RECOMMEND ITEM 6個商品
        'https://store.shopping.yahoo.co.jp/',

        # RECOMMEND ITEM 10個slider
        'https://store.shopping.yahoo.co.jp/',
    ]
]

class Crawler():
    def __init__(self, data):
        self.data = data                 
        
    def run_data(self, url):
        r = requests.get(url,  headers=headers)

        if self.data == "rakutenData" :
            r.encoding = "EUC-JP"
        elif self.data == "rakutenData" :
            r.encoding = "UTF-8"

        soup = BeautifulSoup(r.text, "html.parser")
        return soup

class YahooCrawler(Crawler):
    def __init__(self, data):
        super().__init__(data)

    def get_detail(self, type):
        self.type = type
        if(type == "arrival"):
            self.data = self.data[0]
        elif(type == "recommend"):
            self.data = self.data[1]

        result = []
        detail = {}
        for url in self.data:
            detail = {}
            soup = self.run_data(url)

            # 手錶名
            # name = soup.find('p', class_="elName").text
            # detail["name"] = name
            # 商品名
            brand_name = soup.find('div', class_="mdItemDescription")
            brand_name = brand_name.text.split("-■")[1].split("｜")[1]
            detail["brand_name"] = brand_name
            # 價錢
            price = soup.find(class_="elPriceNumber").text
            detail["price"] = price
            # 新舊程度
            mode = soup.find('span', class_="elLabel").text
            detail["mode"] = mode
            # 品牌
            brand = soup.find('div', class_="mdItemDescription")
            brand = brand.text.split("■")[1].split('｜')[1].replace('-','')
            detail["brand"] = brand
            # 英文品牌名
            en_brand = soup.find("p", class_="elCatchCopy")
            en_brand = en_brand.text.split("/")[0].replace("[",'')
            detail["en_brand"] = en_brand
            # 圖片
            imgSrc = soup.find(class_='elPanelImage')
            imgSrc = imgSrc['src']
            detail["imgSrc"] = imgSrc

            result.append(detail)

        return result

    def render_new_arrival_html(self):
        result = self.get_detail("arrival")
        html= """
            <section id="new_arrival" style="background: #1b1b1b;">
                <h1 style="color: #fff;">NEW ARRIVAL</h1>
                <ul> """

        for index, item in enumerate(result):
            

            if ( index <= 5):
                html += f"""
                <li><a target="_top" href="{yahooData[0][index]}">
                    <p class="pic"><img src="{item["imgSrc"]}_2" width="100%"></p>
                    <p class="name">{item["brand"]} <br class="pc">{item["en_brand"]}</p>
                    <p class="mode"><span>{item["mode"]}</span></p>
                    <p class="cont">{item["brand_name"]}</p>
                    <p class="price">&yen; <span>{item["price"]}</span>(税込)</p>
                </a></li>"""
                if ( index == 5):
                    html+= """
                    </ul>
        
                    <div class="slider watch_slider"> """

            elif ( index > 5):
                html += f"""
                <div class="show_watch">
                    <a target="_top" href="{yahooData[0][index]}">
                        <img src="{item["imgSrc"]}_1" width="100%" alt="">
                        <p class="name">{item["en_brand"]}/{item["brand"]}</p>
                        <p class="mode"><span>{item["mode"]}</span></p>
                        <p class="cont">{item["brand_name"]}</p>
                        <p class="price">&yen; <span>{item["price"]}</span>(税込)</p>
                    </a>
                </div>"""
            
        html += """
            </div>
            <a target="_top" href="https://store.shopping.yahoo.co.jp/evance-web/newarrival.html" class="btn">⇒ 新着商品一覧を見る</a>
        </section>"""
        print(html)

        with open("new_arrival.html", "w", encoding='UTF-8') as file:
            file.write(html)

    def render_recommend_item_html(self):
        result = self.get_detail("recommend")
        html = """
        <section id="recommend" style="background: #f6f6f6;">
            <h1 style="color: #000;">RECOMMEND ITEM</h1>
            <ul class="item_list">"""

        for index, item in enumerate(result):
            if ( index <= 5):
                html += f"""
                <li><a target="_top" href="{yahooData[1][index]}">
                    <img src="images/item_0{index + 1}.jpg" width="100%">
                    <img src="images/item_0{index + 1}w.png" width="100%" class="float">
                    <div class="text">
                        <p class="name">{item["en_brand"]}/{item["brand"]}/p>
                        <p class="mode"><span>{item["mode"]}</span></p>
                        <p class="cont">{item["brand_name"]}<br class="pc"></p>
                        <p class="price">&yen; <span>{item["price"]}</span>(税込)</p>
                    </div>
                </a></li>"""

                if( index == 5):
                    html += """
                        </ul>
                    <div class="slider watch_slider">"""

            elif ( index > 5):
                html += f"""
                <div class="show_watch">
                    <a target="_top" href="{yahooData[1][index]}">
                        <img src="{item["imgSrc"]}_1" width="100%" alt="">
                        <p class="name">{item["en_brand"]}/{item["brand"]}</p>
                        <p class="mode"><span>{item["mode"]}</span></p>
                        <p class="cont">{item["brand_name"]}</p>
                        <p class="price">&yen; <span>{item["price"]}</span>(税込)</p>
                    </a>
                </div>"""

        html += """
            </div>
                <a target="_top" href="https://store.shopping.yahoo.co.jp/evance-web/recommendi.html" class="btn">⇒ 厳選商品一覧を見る</a>
            </section>"""

        print(html)
        with open("recommend_item.html", "w", encoding='UTF-8') as file:
            file.write(html)

ra = YahooCrawler(yahooData)
ra.render_new_arrival_html()
# ra.render_recommend_item_html()