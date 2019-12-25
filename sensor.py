"""
Support for chelaile BusTravelTimeSensor
# Author:
    lidicn
# Created:
    2018-1-09
"""
import logging
from homeassistant.const import (
    CONF_API_KEY, CONF_NAME, ATTR_ATTRIBUTION, CONF_ID
    )
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
import requests
import json
from datetime import datetime
import time

_Log=logging.getLogger(__name__)

DEFAULT_NAME = 'bus_arrivaltime'
CONF_LINEID = 'lineid'
CONF_LINENAME = 'linename'
CONF_DIRECTION = 'direction'
CONF_STATIONNAME = 'stationname'
CONF_NEXTSTATIONNAME = 'nextstationname'
CONF_LINENO = 'lineno'
CONF_TARGETORDER = 'targetorder'
CONF_CITYID = 'cityid'
CONF_TIMERANGE = 'timerange'
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LINEID): cv.string,
    vol.Required(CONF_LINENAME): cv.string,
    vol.Required(CONF_DIRECTION): cv.string,
    vol.Required(CONF_STATIONNAME): cv.string,
    vol.Required(CONF_NEXTSTATIONNAME): cv.string,
    vol.Required(CONF_LINENO): cv.string,
    vol.Required(CONF_TARGETORDER): cv.string,
    vol.Required(CONF_CITYID): cv.string,
    vol.Optional(CONF_NAME, default= DEFAULT_NAME): cv.string,
    vol.Optional(CONF_TIMERANGE, default='000000-120000,120001-235900'): cv.string,
})
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 8.0; MIX 2 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060133) NetType/WIFI Language/zh_CN MicroMessenger/6.6.1.1220(0x26060133) NetType/WIFI Language/zh_CN',
    'charset':'utf-8',
    'Accept-Encoding':'gzip',
    'referer':'https://web.chelaile.net.cn/ch5/?src=webapp_qqwallet&utm_source=webapp_qqwallet&utm_medium=entrance&hideFooter=1&showFav=0&homePage=around&_wv=1027&showTopLogo=0',
    'content-type':'text',
    'Host':'web.chelaile.net.cn',
    'Connection':'Keep-Alive'
}
API_URL = "https://web.chelaile.net.cn/api/bus/line!lineDetail.action"
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    lineid = config.get(CONF_LINEID)
    linename = config.get(CONF_LINENAME)
    direction = config.get(CONF_DIRECTION)
    stationName = config.get(CONF_STATIONNAME)
    nextStationName = config.get(CONF_NEXTSTATIONNAME)
    lineNo = config.get(CONF_LINENO)
    targetOrder = config.get(CONF_TARGETORDER)
    cityId = config.get(CONF_CITYID)
    sensor_name = config.get(CONF_NAME)
    timerange = config.get(CONF_TIMERANGE)
    query_dict = {
        'lineId': lineid,
        'lineName': linename,
        'direction': direction,
        'stationName': stationName,
        'nextStationName': nextStationName,
        'lineNo': lineNo,
        'targetOrder': targetOrder,
        's': 'h5',
        'v': '3.3.16',
        'src': 'webapp_qqwallet',
        'userId': 'browser_1515407929568',
        'h5Id': 'browser_1515407929568',
        'sign': '1',
        'cityId': cityId,
    }
    add_devices([BusTravelTimeSensor(sensor_name,query_dict,timerange)])

class BusTravelTimeSensor(Entity):
    """Representation of a Bus travel time sensor."""
    def __init__(self,sensor_name,query_dict,timerange):
        self.attributes = {}
        self._state = None
        self._query_dict = query_dict
        self._name = sensor_name
        self._timerange = timerange

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """返回mdi图标."""
        return 'mdi:bus'

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.attributes

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return "min"

    def in_time_range(self,ranges):
        now = time.strptime(time.strftime("%H%M%S"),"%H%M%S")
        ranges = ranges.split(",")
        for range in ranges:
            r = range.split("-")
            if time.strptime(r[0],"%H%M%S") <= now <= time.strptime(r[1],"%H%M%S") or time.strptime(r[0],"%H%M%S") >= now >=time.strptime(r[1],"%H%M%S"):
                return True
        return False


    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        if self.in_time_range(self._timerange):

            try:
                response = requests.get(API_URL,params=self._query_dict,headers = HEADERS)
            except requests.ReadTimeout:
                _Log.error("快上车：连接超时！")
            except requests.ConnectionError:
                _Log.error("快上车：连接错误！")
            except requests.RequestException:
                _Log.error("快上车：发生未知错误！")
            res = response.content.decode('utf-8').replace('**YGKJ','').replace('YGKJ##','')
            json_obj = json.loads(res)
            if 'buses' in json_obj['jsonr']['data']:
                bus_list = []
                for i in range(len(json_obj['jsonr']['data']['buses'])-1,-1,-1):
                    #print(json_obj['jsonr']['data']['buses'][i])
                    if len(json_obj['jsonr']['data']['buses'][i]['travels']) !=0:
                        bus_arrialtime = datetime.fromtimestamp(json_obj['jsonr']['data']['buses'][i]['travels'][0]['arrivalTime']//1000.0)
                        bus_traveltime = round(json_obj['jsonr']['data']['buses'][i]['travels'][0]['travelTime']/60,2)
                        bus_list.append({'bus_arrialtime':bus_arrialtime,'bus_traveltime':bus_traveltime})
                for i in range(len(bus_list)):
                    self.attributes['第{}台'.format(i+1)] = bus_list[i]['bus_traveltime']
                if len(bus_list) != 0:
                    self._state = bus_list[0]['bus_traveltime']
                    self.attributes['预计到站时间'] = str(bus_list[0]['bus_arrialtime'])[-8:]
                    if len(bus_list) >= 2:
                        self.attributes['快上车'] = bus_list[1]['bus_traveltime'] - bus_list[0]['bus_traveltime']
                    elif len(bus_list) < 2:
                        self.attributes['快上车'] = '仅有一台车'
                else:
                    self._state = '暂未发车'
                    self.attributes['预计到站时间'] = '暂未发车'
                    self.attributes['快上车'] = '暂未发车'
            else:
                self._state = '暂未发车'
                self.attributes['预计到站时间'] = '暂未发车'
                self.attributes['快上车'] = '暂未发车'
        else:
            self._state = '系统处于休眠期'
            self.attributes['预计到站时间'] = '系统处于休眠期'
