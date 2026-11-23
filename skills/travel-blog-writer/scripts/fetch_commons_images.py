"""Wikimedia Commons에서 자유 라이선스 사진을 찾아 내려받고 출처표를 만든다.
사용법: python -I fetch_commons_images.py <spec.json> <출력폴더>
spec.json: [{"name": "01_bund_night", "queries": ["Lujiazui skyline night from the Bund", "Bund Shanghai night"]}, ...]
결과: <출력폴더>/<name>.jpg|png, _credits.json, _사진출처.md  (이미 받은 name은 건너뜀)
"""
import json, sys, urllib.parse, urllib.request, urllib.error, re, os, time
spec_path, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "blog-draft-helper/1.0 (personal use)"}
OK_LIC = re.compile(r"^(CC0|CC BY|CC BY-SA|Public domain|PD)", re.I)
cred_path = os.path.join(OUT, "_credits.json")
credits = {}
if os.path.exists(cred_path):
    credits = {c["name"]: c for c in json.load(open(cred_path, encoding="utf-8"))}

def get(url, binary=False):
    for i in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            return r if binary else json.loads(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(10 * (i + 1)); continue
            raise
    raise RuntimeError("rate limited")

def save():
    json.dump(list(credits.values()), open(cred_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

used = {c["title"] for c in credits.values()}
# 검수에서 탈락시킨 사진 제목은 _rejected.json (문자열 리스트)에 넣어두면 다시 고르지 않는다
rej_path = os.path.join(OUT, "_rejected.json")
if os.path.exists(rej_path):
    used |= set(json.load(open(rej_path, encoding="utf-8")))
for item in json.load(open(spec_path, encoding="utf-8")):
    name = item["name"]
    if name in credits and os.path.exists(os.path.join(OUT, credits[name]["file"])):
        print(name, "SKIP (exists)"); continue
    chosen = None
    for q in item["queries"]:
        url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
               "&gsrnamespace=6&gsrlimit=15&gsrsearch=" + urllib.parse.quote(q) +
               "&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1200"
               "&iiextmetadatafilter=LicenseShortName|Artist")
        try:
            data = get(url); time.sleep(3)
        except Exception as e:
            print(name, "SEARCH FAILED", e); continue
        for p in sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p["index"]):
            ii = p["imageinfo"][0]; md = ii.get("extmetadata", {})
            lic = md.get("LicenseShortName", {}).get("value", "")
            if p["title"] in used or not OK_LIC.match(lic): continue
            if not p["title"].lower().endswith((".jpg", ".jpeg", ".png")) or ii.get("width", 0) < 800: continue
            artist = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()
            chosen = (p, ii, lic, artist); break
        if chosen: break
    if not chosen:
        print(name, "NONE"); continue
    p, ii, lic, artist = chosen; used.add(p["title"])
    ext = ".png" if p["title"].lower().endswith(".png") else ".jpg"
    try:
        open(os.path.join(OUT, name + ext), "wb").write(get(ii["thumburl"], True)); time.sleep(3)
    except Exception as e:
        print(name, "DOWNLOAD FAILED", e, "- 잠시 후 다시 실행하세요"); continue
    credits[name] = {"name": name, "file": name + ext, "title": p["title"], "license": lic,
                     "artist": artist, "page": ii["descriptionurl"]}
    save()
    print(name, "|", p["title"], "|", lic, "|", artist)

save()
rows = ["# 사진 출처 (Wikimedia Commons, 자유 라이선스)", "",
        "| 파일 | 원본 | 작가 | 라이선스 |", "|---|---|---|---|"]
for c in sorted(credits.values(), key=lambda c: c["file"]):
    rows.append(f"| {c['file']} | [{c['title'][5:]}]({c['page']}) | {c['artist']} | {c['license']} |")
rows += ["", "CC BY / CC BY-SA 사진은 블로그 게시 시 작가명·라이선스·원본 링크 표기가 필수입니다. (CC0는 표기 의무 없음)"]
open(os.path.join(OUT, "_사진출처.md"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
