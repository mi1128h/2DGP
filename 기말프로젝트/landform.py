import gfw
import gobj


def get_floor(target, tx, foot):
    sel_top = 0
    target.floor = None
    for p in gfw.world.objects_at(gfw.layer.platform):
        l, b, r, t = p.get_bb()
        if tx < l or tx > r: continue
        mid = (b + t) // 2
        if foot < mid: continue
        if target.floor is None:
            target.floor = p
            sel_top = t
        else:
            if t > sel_top:
                target.floor = p
                sel_top = t


def get_wall(target):
    left, foot, right, head = target.get_bb_real()
    target.wall_l = 0
    target.wall_r = 7200
    for p in gfw.world.objects_at(gfw.layer.platform):
        l, b, r, t = p.get_bb_real()
        if b >= head and t >= head: continue
        if b <= foot and t <= foot: continue
        if r < left:
            if r > target.wall_l:
                target.wall_l = r
        elif l > right:
            if l < target.wall_r:
                target.wall_r = l

def get_ceiling(target):
    left, foot, right, head = target.get_bb_real()
    target.ceiling = 2400
    for p in gfw.world.objects_at(gfw.layer.platform):
        l, b, r, t = p.get_bb_real()
        if r < left or l > right: continue
        if b > head:
            if b < target.ceiling:
                target.ceiling = b


def move(target):
    tempX, tempY = target.pos
    gobj.move_obj(target)
    l, _, r, _ = target.get_bb_real()
    if l <= target.wall_l or r >= target.wall_r:
        target.pos = tempX, target.pos[1]
