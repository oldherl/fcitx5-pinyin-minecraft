MOEGIRL_API_ENDPOINT="https://zh.moegirl.org.cn/api.php"
MINECRAFT_API_ENDPOINT="https://minecraft-zh.gamepedia.com/api.php"


all: build

build: moegirl.dict

.PRECIOUS: titles.txt

titles.txt:
	python ./fetch.py get_all_titles $(MOEGIRL_API_ENDPOINT) titles.txt
	
mc-titles.txt:
	python ./fetch.py get_all_titles $(MINECRAFT_API_ENDPOINT) mc-titles.txt

results.txt: titles.txt
	python ./collate_moegirl.py titles.txt

moegirl.raw: results.txt
	python ./convert.py results.txt > moegirl.raw

moegirl.dict: moegirl.raw
	libime_pinyindict moegirl.raw moegirl.dict

install: moegirl.dict
	install -Dm644 moegirl.dict -t $(DESTDIR)/usr/share/fcitx5/pinyin/dictionaries/

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
