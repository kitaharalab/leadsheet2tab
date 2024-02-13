import copy as cp

# ある状態sに対して、1,2,3の処理を実行する
def make_many_states(state, ttf, fin):
    dim = make6dim(fin)
    r1 = add_sound(fin, dim)
    for item in r1:
        if item not in state:
            state.append(item)
        ttf.append(item)
    
    r2 = ch2openst(fin, dim)
    for item in r2:
        if item not in state:
            state.append(item)
        ttf.append(item)
        
    r3 = ch2rest(fin, dim)
    for item in r3:
        if item not in state:
            state.append(item)
        ttf.append(item)
        
    r4 = ch_fingering_position(fin, dim)
    for item in r4:
        if item != []:
            if item not in state:
                state.append(item)
            ttf.append(item)
    return state, ttf

# 1: 押弦位置を増やす
def add_sound(fin, dim):
    # 押弦していない指を押弦可能な位置に新しく置くようにする
    res = []
    if fin[4] == (0,0,0):# 小指がフリー
        rf = fin[3]# 薬指の指情報
        s5, f5 = rf[0], rf[2]
        for lf in range(1, s5):
            new_fin = make_new_fp(fin,[[],[],[],[],[4, lf, lf, f5],[fin[-1]]])
            d = make6dim(new_fin)
            if d != dim and d not in res:
                res.append(d)
    return res

# 2: 押弦位置を減らす
    # 2.1: 開放弦を増やす（指を離す）
def ch2openst(fin, dim):
    res = []
    if abs(fin[1][0] - fin[1][1]) == 4:
        for i in range(fin[1][1]):
            c = cp.copy(dim)
            if dim[i] != 0:
                c[i] = fin[1][2]
            if c not in res:
                res.append(c)
    else:
        for i in range(len(dim)):
            c = cp.copy(dim)
            if dim[i] != 0:
                if fin[1][0] != fin[1][1]:
                    if fin[1][1] - fin[1][0] > 3:
                        c[i] = fin[1][2]
                    elif fin[1][1] - fin[1][0] == 1:
                        c[i] = 0
                else:
                    c[i] = 0
            if c not in res:
                res.append(c)
    return res

# 2: 押弦位置を減らす
    # 2.2: 弾かない部分を増やす
def ch2rest(fin, dim):
    res = []
    # print(dim, abs(fin[1][0] - fin[1][1]))
    if abs(fin[1][0] - fin[1][1]) == 4:# 1,5セーハ
        p15_1 = [2,3,5]# 3,4,6弦をミュート
        c15_1 = cp.copy(dim)
        for i in p15_1:
            c15_1[i] = -1
        res.append(c15_1)

        p15_2 = [0,5]# 1,6弦をミュート
        c15_2 = cp.copy(dim)
        for i in p15_2:
            c15_2[i] = -1
        if c15_2 not in res:
            res.append(c15_2)
    elif abs(fin[1][0] - fin[1][1]) == 5:# 1,6セーハ
        p16_1 = [2,3,4]# 3,4,5弦をミュート
        c16_1 = cp.copy(dim)
        for i in p16_1:
            c16_1[i] = -1
        res.append(c16_1)
        p16_2 = [0,5]# 1,5弦をミュート
        c16_2 = cp.copy(dim)
        for i in p16_2:
            c16_2[i] = -1
        if c16_2 not in res:
            res.append(c16_2)
        p16_3 = [0,1]# 1,2弦をミュート
        c16_3 = cp.copy(dim)
        for i in p16_3:
            c16_3[i] = -1
        if c16_3 not in res:
            res.append(c16_3)
        p16_4 = 0# 1弦をミュート
        c16_4 = cp.copy(dim)
        c16_4[p16_4] = -1
        if c16_4 not in res:
            res.append(c16_4)
        
    else:
        for i in range(len(dim)):# 1箇所ずつ変更
            c1 = cp.copy(dim)
            c1[i] = -1
            if c1 not in res:
                res.append(c1)
        p2 = [0,1]# 1,2弦をミュート
        c2 = cp.copy(dim)
        for i in p2:
            c2[i] = -1
        if c2 not in res:
            res.append(c2)
        
        p3 = [4,5]# 5,6弦をミュート
        c3 = cp.copy(dim)
        for i in p3:
            c3[i] = -1
        if c3 not in res:
            res.append(c3)
        
        p4 = [0,5]# 1,6弦をミュート
        c4 = cp.copy(dim)
        for i in p4:
            c4[i] = -1
        if c4 not in res:
            res.append(c4)
    return res
   
# 3: 押弦位置をずらす
def ch_fingering_position(fin, dim):
    # 元々置いてある指を別の場所に移動させる
    res = []
    if fin[1][0] != fin[1][1]:# セーハしているなら
        if fin[1][1] - fin[1][0] == 5:# 1~6弦セーハ
            # ずらす余裕はない
            None
        elif fin[1][1] - fin[1][0] == 4:# 1~5弦セーハ
            # if fin[3][0] == fin[3][1]:# 薬指はセーハしない
            if fin[3][0] != fin[3][1]:# 薬指もセーハ
                # ずらさない
                None
            else:
                # 中指と小指を以下の条件でずらす
                # -> 中指 : 2,3弦を押弦
                for mf in range(2,4):
                    # -> 小指 : 2,3弦を押弦
                    for lf in range(2,4):
                        if mf != lf:
                            new_fin = make_new_fp(fin, [[],[],[2,mf,mf,fin[2][2]],[],[4,lf,lf,fin[4][2]],[fin[-1]]])
                            d = make6dim(new_fin)
                            if d != dim and d not in res:
                                res.append(d)
        elif fin[1][1] - fin[1][0] == 3:
            # 中指が人差し指と同じフレットならば、1つ右のフレットを押さえる            
            if fin[1][2] == fin[3][2]:
                new_fin = make_new_fp(fin, [[],[],[2,fin[2][0]+1,fin[2][1]+1,fin[2][2]],[],[],[fin[-1]]])
                d = make6dim(new_fin)
                if d != dim and d not in res:
                    res.append(d)
    else:# セーハしてない
        if dim[0] == 0 and (fin[1][0] == 2 and fin[1][1] == 2):
            new_fin = make_new_fp(fin, [[],[1,fin[1][0]-1,fin[1][1],fin[1][2]],[],[],[],[fin[-1]]])
            d = make6dim(new_fin)
            if d not in res:
                res.append(d)
    return res

# 新しい指情報を作る
def make_new_fp(fin, ch):
    res = []
    for i in range(len(fin)):
        if ch[i] != []:# 指情報を更新
            if i == ch[i][0]:
                res.append(tuple(ch[i][1:]))
            else:
                res.append(fin[i])
        else:# 指情報をそのまま更新
            res.append(fin[i])
    return res
    
# 指情報から6次元ベクトルを作成
def make6dim(tf):
    li = [0]*6
    for i in range(len(tf)):
        item = tf[i]
        if i == 5:
            if len(item) == 1:
                if item[0] > 0:
                    li[item[0]-1] = -1
            elif len(item) > 1:
                for r in item:
                    li[r-1] = -1
        else:
            if item[0] == item[1]:
                if item[0] > 0:
                    li[item[0]-1] = item[-1]
            else:
                for s in range(item[0]-1,item[1]):
                    li[s] = item[-1]
    return li
