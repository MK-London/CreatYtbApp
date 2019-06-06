import sys
import io
import urllib.request as rq

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

imgUrl ="http://post.phinf.naver.net/20160621_169/1466482468068lmSHj_JPEG/If7GeIbOPZuYwI-GI3xU7ENRrlfI.jpg"
htmlURL ="http://google.com"

savePath1 ="/Users/moon/Downloads/IMGSave.jpg"
savePath2 ="/Users/moon/Downloads/IMGSave1.png"

rq.urlretrieve(imgUrl, savePath1)
rq.urlretrieve(htmlURL, savePath2)
print("complete download!")
