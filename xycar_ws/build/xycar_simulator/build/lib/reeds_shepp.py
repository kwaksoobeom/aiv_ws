import math

# ========== 유틸리티 함수들 ==========
def mod2pi(theta):
    return theta - 2 * math.pi * math.floor(theta / (2 * math.pi))

def polar(x, y):
    return math.hypot(x, y), math.atan2(y, x)

# ========== 경로 요소 정의 ==========
class PathSegment:
    def __init__(self, length, mode):
        self.length = length
        self.mode = mode  # 'L', 'R', or 'S'

class ReedsSheppPath:
    def __init__(self, segments, total_length):
        self.segments = segments
        self.total_length = total_length

# ========== 기본 경로 후보 생성 ==========
def LSL(alpha, beta, d):
    sa = math.sin(alpha)
    sb = math.sin(beta)
    ca = math.cos(alpha)
    cb = math.cos(beta)
    c_ab = math.cos(alpha - beta)
    tmp = 2 + d**2 - 2*c_ab + 2*d*(sa - sb)
    if tmp < 0: return None
    tmp = math.sqrt(tmp)
    t = mod2pi(math.atan2((cb - ca), (d + sa - sb)))
    u = tmp
    v = mod2pi(beta - math.atan2((cb - ca), (d + sa - sb)))
    return [PathSegment(t, 'L'), PathSegment(u, 'S'), PathSegment(v, 'L')]

# TODO: RSR, LSR, RSL 등 다른 조합도 필요

# ========== 좌표계 변환 ==========
def transform_to_origin(start, goal):
    dx = goal[0] - start[0]
    dy = goal[1] - start[1]
    d = math.hypot(dx, dy)
    theta = mod2pi(start[2])
    x = math.cos(theta) * dx + math.sin(theta) * dy
    y = -math.sin(theta) * dx + math.cos(theta) * dy
    phi = mod2pi(goal[2] - start[2])
    return x, y, phi

# ========== 전체 경로 생성 ==========
def generate_reeds_shepp_path(start, goal, step_size=1.0, radius=20.0):
    gx, gy, gphi = transform_to_origin(start, goal)
    d = math.hypot(gx, gy) / radius
    theta = math.atan2(gy, gx)
    alpha = mod2pi(-theta)
    beta = mod2pi(gphi - theta)

    best_path = None
    best_length = float('inf')

    for primitive in [LSL]:  # 앞으로 RSR, LSR, RSL, LRL, RLR 추가 가능
        segments = primitive(alpha, beta, d)
        if segments:
            length = sum(seg.length for seg in segments)
            if length < best_length:
                best_path = segments
                best_length = length

    if best_path is None:
        return []

    # 샘플링
    path = []
    x, y, yaw = 0.0, 0.0, 0.0
    for seg in best_path:
        n = int(seg.length * radius / step_size)
        for i in range(n):
            if seg.mode == 'S':
                x += step_size * math.cos(yaw)
                y += step_size * math.sin(yaw)
            elif seg.mode == 'L':
                yaw += step_size / radius
                x += step_size * math.cos(yaw)
                y += step_size * math.sin(yaw)
            elif seg.mode == 'R':
                yaw -= step_size / radius
                x += step_size * math.cos(yaw)
                y += step_size * math.sin(yaw)
            path.append((x + start[0], y + start[1], mod2pi(yaw + start[2])))

    return path
