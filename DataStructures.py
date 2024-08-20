from util import *

BRAKE = 0
ACCELERATION = 1

# for BN research
MORNING_PEAK = 'MorningPeak'
DAYTIME = 'Daytime'
EVENING_PEAK = 'EveningPeak'
NIGHTTIME = 'Nighttime'
TimePeriods = [MORNING_PEAK, DAYTIME, EVENING_PEAK, NIGHTTIME]

# for MB event
NONE_EVENT = 'NoneEvent'
NORMAL_BRAKE = 'NormalBrake'
HASH_BRAKE = 'HashBrake'    # TODO 这里拼写错了，后面把贝叶斯代码里的也统一改成HardBrake
HARSH_BRAKE = 'HarshBrake'
NORMAL_ACCELERATION = 'NormalAcceleration'
RAPID_ACCELERATION = 'RapidAcceleration'
NORMAL_TURN = 'NormalTurn'
SHARP_TURN = 'SharpTurn'

# for traffic event
CONGESTION = '4'
ACCIDENT = '101'
CONSTRUCTION = '201'
SEVERE_ACCIDENT = '102'
ROAD_CLOSURE = '302'

class TrafficEvent():
    def __init__(self, start_time, end_time, lon, lat, link_id, event_type, event_desc):
        self.start_time = start_time # datetime 格式
        self.end_time = end_time # datetime 格式
        # 用法：
        # from datetime import datetime
        # t.year/month/day/hour/minute
        self.lon = lon
        self.lat = lat
        self.link_id = link_id  # int
        self.event_type = event_type
        self.event_desc = event_desc

        self.lixel_id = None

class MBEvent():
    def __init__(self, vin, uuid, time, lon=None, lat=None, speed=None, event_type=None,time_str=None):
        self.vin = vin
        self.uuid = uuid
        # 之前的贝叶斯研究中，这里的time是时间戳；STNKDE中，这里的time是datetime对象
        self.time = time

        self.lon =  lon
        self.lat = lat
        self.speed = speed

        self.event_type = event_type
        self.brake_torque = None
        self.lateral_acc = None
        self.longitudinal_acc = None
        self.risk=None
        self.time_str=time_str

        # 20231119新加，供STNKDE分析使用
        self.lixel_id = None

class Link():
    def __init__(self, id, fnode, tnode, link_dir=0, link_width=0, link_length=0, numLanes=1, shape=None, name='UnnamedRoad', max_speed=60, road_class=None):
        self.id = id    # link_id (int)
        self.fnode = fnode  # 起点node id (int)
        self.tnode = tnode  # 终点node id (int)
        self.link_dir = link_dir    # link方向
        self.numLanes = numLanes    # 车道数
        self.link_width = link_width    # link宽度
        self.link_length = link_length  # link 长度
        self.shape = shape  # 线形（多段线的关键点）
        self.name = name    # 路名
        self.centroid = None    # 中心点
        self.risk = 0       # 累加的风险值
        self.max_speed = max_speed  # 限速km/h
        self.road_class = road_class    # 道路等级
        self.intersection_link = None   # 对应简化路网中的link_id

        # for Bayesian Network, possibility of the risky events on the link with a certain driver style
        self.p_acceleration_agg = None
        self.p_brake_agg = None
        self.p_turn_agg = None

        self.p_acceleration_calm = None
        self.p_brake_calm = None
        self.p_turn_calm = None

class Node():
    def __init__(self, id, x=None, y=None, lon=None, lat=None):
        self.id = id    # node id (int)
        self.x = x      # 平面坐标，单位应该是m
        self.y = y      # 平面坐标，单位应该是m
        self.lon = lon
        self.lat = lat
        self.num_link = 1

class Lixel():
    def __init__(self, id, link_id, flxnode, tlxnode, fx, fy, tx, ty):
        self.id = id
        self.link_id = link_id  # original link id
        self.flxnode = flxnode  # from lxnode id
        self.tlxnode = tlxnode  # to lxnode id
        self.fx = fx    # from x
        self.fy = fy
        self.tx = tx    # to y
        self.ty = ty
        self.cx = (fx + tx) / 2  # center x
        self.cy = (fy + ty) / 2
        self.length = distance(fx, fy, tx, ty)
        
        self.f_connection = []
        self.t_connection = []

        self.diffusion_lixels = {}
        
        self.raw_risk = 0
        self.risk_density = 0

        self.raw_risk_at_timeperiod = []    # 时间扩散之后的raw risk
        self.risk_density_at_timeperiod = []    # 空间扩散后的risk density
        self.risk_at_timeperiod = []    # 最终的risk

        self.risk_st = []
        self.risk_t = []
        self.time_st = []
        self.time_t = []


class Lxnode():
    def __init__(self, id, x, y, node_id=None):
        self.id = id    # node id
        self.x = x      # 平面坐标，单位应该是m
        self.y = y      # 平面坐标，单位应该是m
        self.node_id = node_id    # 对应路网的node_id
        self.lixels = []