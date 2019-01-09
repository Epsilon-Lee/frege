from frege.weaver.googletrans_api import GoogleTransAPI

api = GoogleTransAPI()
src='zh-CN'
dest='en'
s = "我们都有一个家，名字叫中国。"
print(api.translate(s, src=src, dest=dest))
