from urllib import parse
from urllib.parse import unquote

parameter_dict = {
    'lineid': '',
    'lineno': '',
    'direction': '',
    'stationname': '',
    'nextstationname': '',
    'cityid': '',
    'targetorder': '',
}

yaml_config_templ = """
  - platform: bus_arrivaltime
    name: {lineno}_bus_arrival
    lineid: '{lineid}'
    linename: '{lineno}'
    direction: '{direction}'
    stationname: '{stationname}'
    nextstationname: '{nextstationname}'
    lineno: '{lineno}'
    targetorder: '{targetorder}'
    cityid: '{cityid}'
"""

link = r'''https://web.chelaile.net.cn/ch5/?src=webapp_qqwallet&utm_source=webapp_qqwallet&utm_medium=entrance&hideFooter=1&showFav=0&homePage=around&_wv=1027&showTopLogo=0&supportSubway=1&cityId=018&cityName=%E5%8D%97%E4%BA%AC&cityVersion=2#!/linedetail/2557257721/1/%E6%98%9F%E7%81%AB%E8%B7%AF%C2%B7%E6%B1%87%E6%96%87%E8%B7%AF/%E6%98%9F%E7%81%AB%E8%B7%AF%E5%9C%B0%E9%93%81%E7%AB%99%E4%B8%9C/6/668'''
link = unquote(link)
# print(link)
parseResult = parse.urlparse(link, scheme='https')
# print(parseResult)
query = parse.parse_qs(parseResult.query)

parameter_dict['cityid'] = query['cityId'][0]
# print(parseResult.fragment)
linedetail = parseResult.fragment.split('/')
linedetail = linedetail[2:]
for x in ['lineid', 'direction', 'stationname', 'nextstationname', 'targetorder', 'lineno']:
    parameter_dict[x] = linedetail.pop(0)

from pprint import pprint
# pprint(parameter_dict)
print(yaml_config_templ.format(**parameter_dict))
'''
  - platform: bus_arrivaltime
    name: 668_bus_arrival
    lineid: '2557257721'
    linename: '668'
    direction: '1'
    stationname: '星火路·汇文路'
    nextstationname: '星火路地铁站东'
    lineno: '668'
    targetorder: '6'
    cityid: '018'
'''