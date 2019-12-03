# bus arrival time
Show china bus arrival status.

## Usage
1. Clone this repo to `config/custom_components`
2. Open [this link](https://web.chelaile.net.cn/ch5/?src=webapp_qqwallet&utm_source=webapp_qqwallet&utm_medium=entrance&hideFooter=1&showFav=0&homePage=around&_wv=1027&showTopLogo=0&supportSubway=1&cityId=018&cityName=%E5%8D%97%E4%BA%AC&cityVersion=2#!/linedetail/2557257721/1/%E6%98%9F%E7%81%AB%E8%B7%AF%C2%B7%E6%B1%87%E6%96%87%E8%B7%AF/%E6%98%9F%E7%81%AB%E8%B7%AF%E5%9C%B0%E9%93%81%E7%AB%99%E4%B8%9C/6/668), choose your city, your bus line, and get the url.
3. Paste the url into `value_extract.py`, get the yaml config.
4. Paste yaml config into `configuration.yaml`, like below: 

```yaml
# Example configuration.yaml entry  
sensor:
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
    #timerange: '083000-093000,174500-183000'
```


## Extra
Integrate bus status into index panel, add this to `configuration.yaml`

```yaml
panel_iframe:
  bus_arrialtime:
    title: 'Bus'
    icon: 'mdi:bus'
    url: 'https://web.chelaile.net.cn/ch5/?src=webapp_qqwallet&utm_source=webapp_qqwallet&utm_medium=entrance&hideFooter=1&showFav=0&homePage=around&_wv=1027&showTopLogo=0&supportSubway=1&cityId=018&cityName=%E5%8D%97%E4%BA%AC&cityVersion=2#!/linearound'
    # url: 'https://web.chelaile.net.cn/ch5/?src=webapp_qqwallet&utm_source=webapp_qqwallet&utm_medium=entrance&hideFooter=1&showFav=0&homePage=around&_wv=1027&showTopLogo=0&supportSubway=1&cityId=018&cityName=%E5%8D%97%E4%BA%AC&cityVersion=2#!/linedetail/2557257721/1/%E6%98%9F%E7%81%AB%E8%B7%AF%C2%B7%E6%B1%87%E6%96%87%E8%B7%AF/%E6%98%9F%E7%81%AB%E8%B7%AF%E5%9C%B0%E9%93%81%E7%AB%99%E4%B8%9C/6/668'
```


reference:
[快上车【实时公交】【到站时间】【sensor】【修复bug】](https://bbs.hassbian.com/forum.php?mod=viewthread&tid=2381&highlight=%E5%85%AC%E4%BA%A4)