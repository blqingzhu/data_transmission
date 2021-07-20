# -*- coding:utf-8 -*-
# -*- 经纬度转换 -*-

from math import radians, sin, cos, degrees, atan2, atan, tan, acos, sqrt, pi


# 两个经纬点的方位角
def getDegree(latA, lonA, latB, lonB):
    """
    Args:
        point p1(latA, lonA)
        point p2(latB, lonB)
    Returns:
        bearing between the two GPS points,
        default: the basis of heading direction is north
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng


# 两个经纬点的距离
def getDistance(latA, lonA, latB, lonB):
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)

    pA = atan(rb / ra * tan(radLatA))
    pB = atan(rb / ra * tan(radLatB))
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
    c1 = (sin(x) - x) * (sin(pA) + sin(pB)) ** 2 / cos(x / 2) ** 2
    c2 = (sin(x) + x) * (sin(pA) - sin(pB)) ** 2 / sin(x / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    return distance


# 经纬度、距离dist和方向角brng，求另外一点经纬度函数分享
def computerOffsetPosition(lon, lat, brng, dist):
    lat1 = lat * pi / 180
    lon1 = lon * pi / 180
    brg = brng * pi / 180

    # 扁率
    flat = 298.257223563
    # 地球 半长轴
    a = 6378137.0
    # 地球 半短轴
    b = 6356752.314245

    f = 1 / flat
    sb = sin(brg)
    cb = cos(brg)
    tu1 = (1 - f) * tan(lat1)
    cu1 = 1 / sqrt((1 + tu1 * tu1))
    su1 = tu1 * cu1
    s2 = atan2(tu1, cb)
    sa = cu1 * sb
    csa = 1 - sa * sa
    us = csa * (a * a - b * b) / (b * b)
    A = 1 + us / 16384 * (4096 + us * (-768 + us * (320 - 175 * us)))
    B = us / 1024 * (256 + us * (-128 + us * (74 - 47 * us)))
    s1 = dist / (b * A)
    s1p = 2 * pi
    cs1m = 0.0
    ss1 = 0.0
    cs1 = 0.0
    ds1 = 0.0
    #
    while abs(s1 - s1p) > 1e-12:
        cs1m = cos(2 * s2 + s1)
        ss1 = sin(s1)
        cs1 = cos(s1)
        ds1 = B * ss1 * (cs1m + B / 4 * (
                    cs1 * (-1 + 2 * cs1m * cs1m) - B / 6 * cs1m * (-3 + 4 * ss1 * ss1) * (-3 + 4 * cs1m * cs1m)))
        s1p = s1
        s1 = dist / (b * A) + ds1

    t = su1 * ss1 - cu1 * cs1 * cb
    lat2 = atan2(su1 * cs1 + cu1 * ss1 * cb, (1 - f) * sqrt(sa * sa + t * t))
    l2 = atan2(ss1 * sb, cu1 * cs1 - su1 * ss1 * cb)
    c = f / 16 * csa * (4 + f * (4 - 3 * csa))
    l = l2 - (1 - c) * f * sa * (s1 + c * ss1 * (cs1m + c * cs1 * (-1 + 2 * cs1m * cs1m)))
    lon2 = lon1 + l
    Longitude = lon2 * 180 / pi
    Latitude = lat2 * 180 / pi
    return (Longitude, Latitude)
