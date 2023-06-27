import requests
from lxml import html

url = 'https://example.com'
response = requests.get(url)
html_content = response.content

tree = html.fromstring(html_content)
xpath_expression = '//*[@id="content"]/div/p[1]'
text = tree.xpath(xpath_expression)[0].text_content()

print(text)
