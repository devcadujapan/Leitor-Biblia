import json, os

INPUT_FILE  = "acf.json"
OUTPUT_DIR  = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "biblia_acf.json")

BOOK_NAMES = {
    "gn":"Gênesis","ex":"Êxodo","lv":"Levítico","nm":"Números","dt":"Deuteronômio",
    "js":"Josué","jz":"Juízes","rt":"Rute","1sm":"1 Samuel","2sm":"2 Samuel",
    "1rs":"1 Reis","2rs":"2 Reis","1cr":"1 Crônicas","2cr":"2 Crônicas","ed":"Esdras",
    "ne":"Neemias","et":"Ester","jo":"Jó","jó":"Jó","sl":"Salmos","pv":"Provérbios",
    "ec":"Eclesiastes","ct":"Cantares","is":"Isaías","jr":"Jeremias","lm":"Lamentações",
    "ez":"Ezequiel","dn":"Daniel","os":"Oséias","jl":"Joel","am":"Amós","ob":"Obadias",
    "jn":"Jonas","mq":"Miquéias","na":"Naum","hc":"Habacuque","sf":"Sofonias",
    "ag":"Ageu","zc":"Zacarias","ml":"Malaquias","mt":"Mateus","mc":"Marcos",
    "lc":"Lucas","jo":"João","at":"Atos","atos":"Atos","rm":"Romanos","1co":"1 Coríntios",
    "2co":"2 Coríntios","gl":"Gálatas","ef":"Efésios","fp":"Filipenses","cl":"Colossenses",
    "1ts":"1 Tessalonicenses","2ts":"2 Tessalonicenses","1tm":"1 Timóteo","2tm":"2 Timóteo",
    "tt":"Tito","fm":"Filemom","hb":"Hebreus","tg":"Tiago","1pe":"1 Pedro","2pe":"2 Pedro",
    "1jo":"1 João","2jo":"2 João","3jo":"3 João","jd":"Judas","ap":"Apocalipse",
}

if not os.path.exists(INPUT_FILE):
    print(f"Arquivo {INPUT_FILE} nao encontrado! Baixe em:")
    print("https://raw.githubusercontent.com/thiagobodruk/biblia/master/json/acf.json")
else:
    with open(INPUT_FILE, encoding="utf-8-sig") as f:
        source = json.load(f)
    output = {}
    for book in source:
        abbrev = book.get("abbrev","").lower()
        name = BOOK_NAMES.get(abbrev) or book.get("book","")
        if name:
            output[name] = {str(i+1): v for i, v in enumerate(book.get("chapters",[]))}
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8-sig") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Concluido! {len(output)} livros salvos em {OUTPUT_FILE}")

