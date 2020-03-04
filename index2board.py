from scrapy.selector import Selector
import requests


DEFAULT_DCARD = ['happynewyear', 'relationship', 'youtuber', 'smallgoodthings', 'freshman', 'makeup', 'manicure', 'fragrance', 'hairsalon', 'orthodontics', 'contact_lens', 'dressup', 'sneakers', 'buyonline', 'boutique', 'mood', 'talk', 'funny', 'joke', 'girl', 'menstrual', 'marriage', 'parentchild', 'rainbow', 'trans', 'otokonoko', 'lesbian', 'pet', 'photography', 'plant', 'vehicle', 'heavy_motorcycle', 'railway', 'marvel', 'food', 'go_vege', 'fastfood', 'snack', 'cvs', 'travel', 'movie', 'tvepisode', 'marvel_studios', 'jp_drama', 'music', 'palmar_drama', 'game', 'board_game', 'hearthstone', 'minecraft', 'lol', 'acg', 'girlslove', 'cosplay', 'pokemon', 'conan', 'onepiece', 'kanahei', 'shin_chan', 'sport', 'baseball', 'cpbl', 'basketball', 'badminton', 'volleyball', 'dance', 'fitness', 'weight_loss', 'sportsevents', 'boy', 'military', '3c', 'apple', 'av_equipment', 'savemoney', 'trending', 'job', 'med', 'parttime', 'intern', 'novel', 'literature', 'disaster', 'sex', 'sex_literature', 'ero_manga', 'bdsm']


class BaseIdxNameConverter:
    def __init__(self):
        pass

    def to_name(self, idx: int):
        raise NameError('you must define to_name function')

    def to_idx(self, name: str):
        raise NameError('you must define to_idx function')


class DcardIdxNameConverter(BaseIdxNameConverter):
    def __init__(self):
        resp = requests.get('https://www.dcard.tw/f')
        self.__call_back(resp)

    def __call_back(self, response):
        self.names = Selector(response).css(
            '.ForumEntryGroup_list_cdSR2f>li ::text').getall()
        idx = Selector(response).css(
            '.ForumEntryGroup_list_cdSR2f>li>a::attr(href)').getall()

        def spliter(x): return x.split('/')[-1]
        self.idxs = list(map(spliter, idx))

    def to_name(self, idx: int):
        for i, tmp_idx in enumerate(self.idxs):
            if tmp_idx == idx:
                return self.name[i]
        raise ValueError("Not found")

    def to_idx(self, name: str):
        for i, tmp_name in enumerate(self.names):
            if tmp_name == name:
                return self.idxs[i]
        raise ValueError("Not found")

    def pair_view(self):
        return [(name, idx) for name, idx in zip(self.names, self.idxs)]


if __name__ == '__main__':
    dic = DcardIdxNameConverter()
    print(dic.idxs)
