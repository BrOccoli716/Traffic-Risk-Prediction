from datetime import datetime, timedelta
import numpy as np
import math

pi = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323
CONSTANTS_RADIUS_OF_EARTH = 6371000

def printlog(s, pre='', end='\n'):
    output = pre + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " " + s
    print(output, end=end)

def to_percent(temp, position):
    return '%2.2f'%(100*temp) + '%'

def smooth(data, sm=1):
    smooth_data = data

    if sm > 1:
        y = np.ones(sm)*1.0/sm
        smooth_data = np.convolve(y, data)[sm-1: -sm+1]

    return smooth_data

def millerToXY (lon, lat):
    """
    :param lon: 经度
    :param lat: 维度
    :return:
    """
    L = 6381372*math.pi*2    #地球周长
    W = L                    #平面展开，将周长视为X轴
    H = L/2                  #Y轴约等于周长一般
    mill = 2.3               #米勒投影中的一个常数，范围大约在正负2.3之间  
    x = lon*math.pi/180      #将经度从度数转换为弧度
    y = lat*math.pi/180      #将纬度从度数转换为弧度 
    y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))  #这里是米勒投影的转换 
    
    # 这里将弧度转为实际距离 ，转换结果的单位是米
    x = (W/2)+(W/(2*math.pi))*x
    y = (H/2)-(H/(2*mill))*y
    return x, y

def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

def GPStoXY(lon, lat, ref_lon=116.326793, ref_lat=40.003017):
    # input GPS and Reference GPS in degrees
    # output XY in meters (m) X:North Y:East
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    ref_lat_rad = math.radians(ref_lat)
    ref_lon_rad = math.radians(ref_lon)

    sin_lat = math.sin(lat_rad)
    cos_lat = math.cos(lat_rad)
    ref_sin_lat = math.sin(ref_lat_rad)
    ref_cos_lat = math.cos(ref_lat_rad)

    cos_d_lon = math.cos(lon_rad - ref_lon_rad)

    arg = np.clip(ref_sin_lat * sin_lat + ref_cos_lat * cos_lat * cos_d_lon, -1.0, 1.0)
    c = math.acos(arg)

    k = 1.0
    if abs(c) > 0:
        k = (c / math.sin(c))

    x = float(k * cos_lat * math.sin(lon_rad - ref_lon_rad) * CONSTANTS_RADIUS_OF_EARTH)
    y = float(k * (ref_cos_lat * sin_lat - ref_sin_lat * cos_lat * cos_d_lon) * CONSTANTS_RADIUS_OF_EARTH)

    return x, y

def GPS2XY_new(lon, lat, lon0=116.326793, lat0=40.003017):
    lon_scale = 111319.490793434
    lat_scale = 110946.252132894
    lat_div = 57.295779513
    x = (lon - lon0) * lon_scale * math.cos(lat / lat_div)
    y = (lat - lat0) * lat_scale
    return x, y

def isInBound(lon, lat):
    # 范围经纬坐标
    # x1 = 116.455111 113.582000
    x1 = 113.57000
    # x2 = 116.490000 113.692000 113.725
    x2 = 113.7
    # y1 = 39.981500 22.80 22.78
    y1 = 22.795
    # y2 = 40.012472 22.887900 22.925
    y2 = 22.9
    if lon > x1 and lon < x2 and lat > y1 and lat < y2:
        return True
    else:
        return False

def _gcj2xy(lon, lat):
    lon,lat = gcj02_to_wgs84(lon, lat)
    x, y = GPS2XY_new(lon, lat)
    return int(x), int(y)

class Coords():
    def __init__(self) -> None:
        self.x0 = 0
        self.y0 = 0
        self.set = False
    
    def gcj2xy(self, lon, lat):
        x, y = _gcj2xy(lon, lat)
        if self.set:
            return x-self.x0, y-self.y0
        else:
            self.set = True
            self.x0 = x
            self.y0 = y
            return 0,0

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret
 
 
def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def gcj02towgs84(lng, lat):
    """
    GCJ02(⽕星坐标系)转GPS84
    :param lng:⽕星坐标系的经度
    :param lat:⽕星坐标系纬度
    :return:
    """

    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    # radlat = lat / 180.0 * pi
 
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
  
    return [lng  - dlng, lat - dlat]
 
# def GCJ02_to_BD09(gcj_lng, gcj_lat):
#         """
#         实现GCJ02向BD09坐标系的转换
#         :param lng: GCJ02坐标系下的经度
#         :param lat: GCJ02坐标系下的纬度
#         :return: 转换后的BD09下经纬度
#         """
#         z = math.sqrt(gcj_lng * gcj_lng + gcj_lat * gcj_lat) + 0.00002 * math.sin(gcj_lat * self.x_pi)
#         theta = math.atan2(gcj_lat, gcj_lng) + 0.000003 * math.cos(gcj_lng * self.x_pi)
#         bd_lng = z * math.cos(theta) + 0.0065
#         bd_lat = z * math.sin(theta) + 0.006
#         return bd_lng, bd_lat

#计算点到线段距离
def point_to_line_distance(x,y,x1,y1,x2,y2):
    cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)
    if (cross <= 0):
        return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
    d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    if (cross >= d2):
        return math.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2))
    r = cross / d2
    px = x1 + (x2 - x1) * r
    py = y1 + (y2 - y1) * r
    return math.sqrt((x - px) * (x - px) + (py - y) * (py - y))


def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def wgs84_to_gcj02(lon, lat):
    """
    将WGS-84坐标转换为GCJ-02坐标

    :param lat: WGS-84纬度
    :param lon: WGS-84经度
    :return: (gcj_lat, gcj_lon) GCJ-02坐标
    """
    a = 6378245.0  # 长半轴
    ee = 0.00669342162296594323  # 偏心率平方
    dLat = transformLat(lon - 105.0, lat - 35.0)
    dLon = transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * math.pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * math.pi)
    gcjLat = lat + dLat
    gcjLon = lon + dLon
    return gcjLon, gcjLat