"""매일 유튜브 채널 수치(구독자·누적 조회수·영상 수)를 받아 index.html에 반영한다."""
import json, re, sys, urllib.request, datetime, pathlib

CHANNEL_ID = "UCpK3pzteRFEGgnUGI4o5a5g"  # 과학하는 박건수 (@박건수과학)
URL = f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}"
page = pathlib.Path(__file__).resolve().parent.parent / "index.html"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.load(r)

c = data.get("counters", {})
src = c.get("api") or c.get("estimation") or {}
subs, views, videos = src.get("subscriberCount"), src.get("viewCount"), src.get("videoCount")
if not all(isinstance(v, (int, float)) and v > 0 for v in (subs, views, videos)):
    print("수치를 읽지 못해 이번에는 건너뜁니다:", src)
    sys.exit(0)

kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
html = page.read_text(encoding="utf-8")
def put(key, text):
    global html
    html = re.sub(rf'(data-yt="{key}">)[^<]*(<)', rf'\g<1>{text}\g<2>', html, count=1)
put("subs", f"{int(subs):,}")
put("views", f"{int(views):,}")
put("videos", f"{int(videos):,}")
put("date", f"{kst.month}월 {kst.day}일 업데이트")
page.write_text(html, encoding="utf-8")
print("업데이트:", int(subs), int(views), int(videos))
