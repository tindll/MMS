from urllib.request import urlopen

url = input("ENTER URL:")
print(url)
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)
