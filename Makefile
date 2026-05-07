MOEGIRL_API_ENDPOINT="https://zh.moegirl.org.cn/api.php"
MINECRAFT_API_ENDPOINT="https://zh.minecraft.wiki/api.php"
ARCHWIKI_API_ENDPOINT="https://wiki.archlinux.org/api.php"


all: build

build: minecraft-cn.dict

mc-titles.txt:
	python ./fetch.py get_all_titles $(MINECRAFT_API_ENDPOINT) mc-titles.txt
mc-titles-cn.txt:
	python ./fetch.py get_all_titles_in_variant $(MINECRAFT_API_ENDPOINT) mc-titles-cn.txt zh-cn

mc-results-cn.txt: mc-titles-cn.txt
	python ./collate_moegirl.py mc-titles-cn.txt mc-results-cn.txt
	
mc-cn.raw: mc-results-cn.txt
	python ./convert.py mc-results-cn.txt > mc-cn.raw

minecraft-cn.dict: mc-cn.raw
	libime_pinyindict mc-cn.raw minecraft-cn.dict


clean:
	rm -f mc-titles{,-cn}.txt
	rm mc-cn.raw
	rm minecraft-cn.dict
