MOEGIRL_API_ENDPOINT="https://zh.moegirl.org.cn/api.php"
MINECRAFT_API_ENDPOINT="https://zh.minecraft.wiki/api.php"
ARCHWIKI_API_ENDPOINT="https://wiki.archlinux.org/api.php"


all: build

build: moegirl.dict

.PRECIOUS: titles.txt

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

install: moegirl.dict
	install -Dm644 moegirl.dict -t $(DESTDIR)/usr/share/fcitx5/pinyin/dictionaries/
	
install-mc: minecraft.dict
	install -Dm644 minecraft.dict -t $(DESTDIR)/usr/share/fcitx5/pinyin/dictionaries/

moegirl.dict.yaml: moegirl.raw
	sed 's/[ ][ ]*/\t/g' moegirl.raw > moegirl.rime.raw
	sed -i 's/\t0//g' moegirl.rime.raw
	sed -i "s/'/ /g" moegirl.rime.raw
	echo -e '---\nname: moegirl\nversion: "0.1"\nsort: by_weight\n...\n' >> moegirl.dict.yaml
	cat moegirl.rime.raw >> moegirl.dict.yaml

install_rime_dict: moegirl.dict.yaml
	install -Dm644 moegirl.dict.yaml -t $(DESTDIR)/usr/share/rime-data/

clean:
	rm -f results.txt titles.txt
	rm -f mc-titles.txt
	rm -f moegirl.{raw,rime.raw,dict{,.yaml}}
	rm -f PKGBUILD.{pinyin,rime}
	rm -f fcitx5-pinyin-moegirl*
	rm -rf src/ pkg/
