from add_state import *

# 状態作成
def make_observe(fr):# 2箇所(2音+開放弦)まで:18112個
    lf = 2
    states = []
    tf = temp_forms(fr) # 典型フォームを作成する関数
    for n1 in range(-1, fr+1):
        for n2 in range(-1, fr+1):
            for n3 in range(-1, fr+1):
                for n4 in range(-1, fr+1):
                    for n5 in range(-1, fr+1):
                        for n6 in range(-1, fr+1):
                            m = [n1, n2, n3, n4, n5, n6]
                            # 休符
                            if m.count(-1) == 6:
                                states.append(m)
                            # 押弦箇所が1箇所（1音のみ or 1音+開放弦）
                            elif len(list(set(m))) <= 3 and sum(i > 0 for i in m) <= 1:
                            # elif m.count(-1) == 5 or (m.count(-1) == 4 and min2nd(m) == 0):
                                states.append(m)
                            # 押弦箇所が2箇所（2音のみ or 2音+開放弦）
                            elif len(list(set(m))) <= 4 and sum(i > 0 for i in m) <= 2:
                            # elif m.count(-1) == 4 or (m.count(-1) == 3 and min2nd(m) == 0):
                                n = sorted(list(set(m)))
                                if len(n) == 4:
                                    if abs(n[-1]-n[-2]) <= lf: # 1箇所のフレット位置が○以内なら
                                        states.append(m)
                                elif len(n) == 3:
                                    if min2nd(m) == 0:
                                        states.append(m)
                                    elif abs(n[-1]-n[-2]) <= 2:
                                        states.append(m)
                                else:
                                    states.append(m)

    ttf = []
    for item in tf:
        # 典型フォームリストから6次元ベクトルを作成し、ベクトルに対して1~2箇所変更したものをappend
        states.append(make6dim(item))
        ttf.append(make6dim(item))
        states, ttf = make_many_states(states, ttf, item)
    return states, ttf


# 典型フォームリスト
def temp_forms(fr):# 274個の状態が作成される
    fin = []
    lim = fr-1# fr=15:13fretまで
    
    # fin = [(s,e,f),(s,e,f),(s,e,f),(s,e,f),(s,e,f),[n1,..]]
    # -> ex1). [(0,0,0),(2,2,1),(4,4,2),(5,5,3),(0,0,0),[6]]
    # -> ex2). [(0,0,0),(1,6,x),(3,3,x+1),(5,5,x+2),(4,4,x+2),[-1]
    # -> (0,0,0):未使用 n1:演奏しない弦
    # 指情報から6次元ベクトルを作成できるようにする
    
    # low-chords
    fin.append([(0,0,0),(2,2,1),(4,4,2),(5,5,3),(0,0,0),[6]])# C
    fin.append([(0,0,0),(2,2,1),(4,4,2),(5,5,3),(3,3,3),[6]])# C7
    fin.append([(0,0,0),(0,0,0),(4,4,2),(5,5,3),(2,2,3),[6]])# Cadd9
    fin.append([(0,0,0),(1,2,1),(4,4,2),(5,5,3),(0,0,0),[6]])# Csus4
    fin.append([(0,0,0),(2,2,1),(4,4,2),(3,3,2),(0,0,0),[6]])# Am
    fin.append([(0,0,0),(2,2,1),(4,4,2),(0,0,0),(0,0,0),[6]])# Am7

    fin.append([(0,0,0),(3,3,2),(1,1,2),(2,2,3),(0,0,0),[5,6]])# D
    fin.append([(6,6,2),(3,3,2),(1,1,2),(2,2,3),(0,0,0),[5]])# D/F#
    fin.append([(0,0,0),(3,3,2),(0,0,0),(2,2,3),(1,1,3),[5,6]])# Dsus4
    
    fin.append([(0,0,0),(1,1,1),(3,3,2),(2,2,3),(0,0,0),[5,6]])# Dm
    fin.append([(0,0,0),(2,2,1),(3,3,2),(1,1,2),(0,0,0),[5,6]])# D7
    fin.append([(0,0,0),(1,3,2),(0,0,0),(0,0,0),(0,0,0),[5,6]])# DM7
    fin.append([(0,0,0),(2,2,1),(1,1,1),(3,3,2),(0,0,0),[5,6]])# Dm7
    
    fin.append([(0,0,0),(3,3,1),(5,5,2),(4,4,2),(0,0,0),[-1]])# E
    fin.append([(0,0,0),(3,3,1),(5,5,2),(0,0,0),(0,0,0),[-1]])# E7
    fin.append([(0,0,0),(0,0,0),(5,5,2),(4,4,2),(0,0,0),[-1]])# Em
    fin.append([(0,0,0),(0,0,0),(5,5,2),(0,0,0),(0,0,0),[-1]])# Em7
    fin.append([(0,0,0),(0,0,0),(5,5,2),(4,4,2),(3,3,2),[-1]])# EM7
    
    fin.append([(0,0,0),(1,1,2),(2,2,3),(3,3,4),(0,0,0),[5,6]])# FM7
    
    fin.append([(0,0,0),(0,0,0),(5,5,2),(6,6,3),(1,1,3),[-1]])# G
    fin.append([(0,0,0),(1,1,2),(5,5,2),(6,6,3),(0,0,0),[-1]])# GM7
    fin.append([(0,0,0),(1,1,1),(5,5,2),(6,6,3),(0,0,0),[-1]])# G7
    
    fin.append([(0,0,0),(2,4,2),(0,0,0),(0,0,0),(0,0,0),[6]])# A
    fin.append([(0,0,0),(2,2,1),(4,4,2),(3,3,2),(0,0,0),[6]])# Am
    fin.append([(0,0,0),(2,2,1),(4,4,2),(0,0,0),(0,0,0),[6]])# Am7
    fin.append([(0,0,0),(4,4,2),(0,0,0),(2,2,2),(0,0,0),[6]])# A7
    fin.append([(0,0,0),(3,3,1),(4,4,2),(2,2,2),(0,0,0),[6]])# AM7
    fin.append([(0,0,0),(0,0,0),(2,2,2),(3,3,3),(0,0,0),[4,5,6]])# A#dim
    
    # Hi-chords
    # pattern 1(6弦セーハ)
    # 1. 6弦ルートのFコード
    li_major_1 = [ [(0,0,0),(1,6,x),(3,3,x+1),(5,5,x+2),(4,4,x+2),[-1]] for x in range(1,lim)]
    for item in li_major_1:
        fin.append(item)
    # 2. 6弦ルートのFmコード
    li_minor_1 = [ [(0,0,0),(1,6,x),(0,0,0),(5,5,x+2),(4,4,x+2),[-1]] for x in range(1,lim)]
    for item in li_minor_1:
        fin.append(item)
    # 3. 6弦ルートのF7コード
    li_7th_1 = [ [(0,0,0),(1,6,x),(3,3,x+1),(5,5,x+2),(0,0,0),[-1]]  for x in range(1,lim)]
    for item in li_7th_1:
        fin.append(item)
    # 4. 6弦ルートのFm7コード
    li_m7_1 = [ [(0,0,0),(1,6,x),(0,0,0),(5,5,x+2),(0,0,0),[-1]] for x in range(1,lim)]
    for item in li_m7_1:
        fin.append(item)
        
    # pattern 2
    # 5弦セーハ
    # 1. 5弦ルートのA#コード
    li_major_2 = [ [(0,0,0),(1,5,x),(0,0,0),(2,4,x+2),(0,0,0),[6]] for x in range(1,lim)]
    for item in li_major_2:
        fin.append(item)
    # 2. 5弦ルートのA#mコード
    li_minor_2 = [ [(0,0,0),(1,5,x),(2,2,x+1),(4,4,x+2),(3,3,x+2),[6]] for x in range(1,lim)]
    for item in li_minor_2:
        fin.append(item)
    # 3. 5弦ルートのA#maj7コード
    li_M7_1 = [ [(0,0,0),(1,5,x),(2,2,x+1),(4,4,x+2),(4,4,x+2),[6]] for x in range(1,lim)]
    for item in li_M7_1:
        fin.append(item)
    # 4. 5弦ルートのA#m7コード
    li_m7_2 = [ [(0,0,0),(1,5,x),(2,2,x+1),(4,4,x+2),(0,0,0),[6]] for x in range(1,lim)]
    for item in li_m7_2:
        fin.append(item)
    # 5. 5弦ルートのA#7コード
    li_7th_2 = [ [(0,0,0),(1,5,x),(0,0,0),(4,4,x+2),(4,4,x+2),[6]] for x in range(1,lim)]
    for item in li_7th_2:
        fin.append(item)
    
    # pattern 3
    # 人差し指2-4弦、中指6弦
    # 1. 特殊なFm7コード
    li_m7_3 = [ [(0,0,0),(2,4,x),(6,6,x),(0,0,0),(0,0,0),[1,5]] for x in range(1,lim)]
    for item in li_m7_3:
        fin.append(item)
    # 2. 特殊なF7コード
    li_7th_3 = [ [(0,0,0),(2,4,x),(6,6,x),(3,3,x+1),(0,0,0),[1,5]] for x in range(1,lim)]
    for item in li_7th_3:
        fin.append(item)
    # 3. 特殊なFdim7コード
    li_dim7_1 = [ [(0,0,0),(2,4,x),(6,6,x+1),(3,3,x+1),(0,0,0),[1,5]] for x in range(lim)]
    for item in li_dim7_1:
        fin.append(item)
    
    # others
    # majorコードの1~3弦を押弦
    # 1. 4弦ルートのFコード
    li_major_3 = [ [(0,0,0),(1,2,x),(3,3,x+1),(4,4,x+2),(0,0,0),[5,6]] for x in range(1,lim)]
    for item in li_major_3:
        fin.append(item)
    # 2. 6弦ルートの特殊なC#m
    li_minor_4 = [ [(0,0,0),(6,6,x),(3,3,x),(2,2,x),(1,1,x),[4,5]] for x in range(1,lim)]
    for item in li_minor_4:
        fin.append(item)
    # 3. 6弦ルートの特殊なFm7-5
    li_m75_1 = [ [(0,0,0),(2,2,x),(6,6,x+1),(4,4,x+1),(3,3,x+1),[1,5]] for x in range(lim)]
    for item in li_m75_1:
        fin.append(item)
    # 4. 6弦ルートの特殊なFmaj7
    li_M7_2 = [ [(6,6,x),(2,2,x),(4,4,x+1),(3,3,x+1),(0,0,0),[1,5]] for x in range(1,lim)]
    for item in li_M7_2:
        fin.append(item)
    # 5. 4弦ルートのD#maj7
    li_M7_3 = [ [(0,0,0),(4,4,x),(1,3,x+2),(0,0,0),(0,0,0),[5,6]] for x in range(3,lim)]
    for item in li_M7_3:
        fin.append(item)
    
    # 4弦ルートのF#dim7
    li_dim7_2 = [ [(0,0,0),(4,4,x),(2,2,x),(3,3,x+1),(1,1,x+1),[5,6]] for x  in range(lim)]
    for item in li_dim7_2:
        fin.append(item)
    # 6弦ルート, 1-6セーハのB-dim7
    li_dim7_3 = [ [(0,0,0),(1,6,x),(5,5,x+1),(4,4,x+2),(2,2,x+2),[-1]] for x in range(lim)]
    for item in li_dim7_3:
        fin.append(item)
    # 4弦ルートのDdim
    li_dim_1 = [ [(0,0,0),(4,4,x),(0,0,0),(3,3,x+1),(1,1,x+1),[2,5,6]] for x  in range(lim)]
    for item in li_dim_1:
        fin.append(item)
    
    # 1-5セーハのOnコード
    li_on1 = [ [(0,0,0),(2,4,x),(0,0,0),(5,5,x+2),(0,0,0),[1,6]] for x in range(1,lim)]
    for item in li_on1:
        fin.append(item)
    # 5弦ルートのAm7-5
    li_m75_2 = [ [(0,0,0),(5,5,x),(3,3,x),(4,4,x+1),(2,2,x+1),[1,6]] for x  in range(1,lim)]
    for item in li_m75_2:
        fin.append(item)
    # 6弦ルートのF6
    li_6 = [ [(6,6,x),(0,0,0),(3,3,x+1),(5,5,x+2),(2,2,x+2),[1,4]] for x in range(1,lim)]
    for item in li_6:
        fin.append(item)
    
    # augコード
    li_aug1 = [ [(0,0,0),(1,1,x),(3,3,x+1),(2,2,x+1),(4,4,x+2),[5,6]] for x in range(1, lim)]
    for item in li_aug1:
        fin.append(item)
    li_aug2 = [ [(0,0,0),(2,3,x),(4,4,x+1),(5,5,x+2),(0,0,0),[1,6]] for x in range(1,lim)]
    for item in li_aug2:
        fin.append(item)
    
    return fin


# 配列の2番目に小さい要素を返す
def min2nd(l):
    ls = list(set(l))
    buf = min(ls)
    ls.remove(buf)
    if len(ls) == 0:
        return buf
    return min(ls)


def guitar_frets():
    # 開放弦から15フレット分
    frets = [# sf = s + 6f 
        #           0  """"""          1                   ""          2                   ""          3                   ""          4                   ""         5   ""          6                   ""          7                   ""          8                   ""          9                   ""         10  ""           11                    ""         12   ""          13                    ""          14                  ""          15                    ""rest
        [("E5", 64, 0),    ("F5" , 65, 1),                 ("F#5", 66, 2), ("G-5", 66, 2), ("G5" , 67, 3),                 ("G#5", 68, 4), ("A-5", 68, 4), ("A5", 69, 5), ("A#5", 70, 6), ("B-5", 70, 6), ("B5" , 71, 7),                 ("C6" , 72, 8),                 ("C#6", 73, 9), ("D-6", 73, 9), ("D6", 74, 10), ("D#6", 75, 11), ("E-6", 75, 11), ("E6", 76, 12), ("F6" , 77, 13),                  ("F#6", 78, 14), ("G-6", 78,14),("G6" , 79, 15),                  ("rest", -1, -1)],
        [("B4", 59, 0),    ("C5" , 60, 1),                 ("C#5", 61, 2), ("D-5", 61, 2), ("D5" , 62, 3),                 ("D#5", 63, 4), ("E-5", 63, 4), ("E5", 64, 5), ("F5" , 65, 6),                 ("F#5", 66, 7), ("G-5", 66, 7), ("G5" , 67, 8),                 ("G#5", 68, 9), ("A-5", 68, 9), ("A5", 69, 10), ("A#5", 70, 11), ("B-5", 70, 11), ("B5", 71, 12), ("C6" , 72, 13),                  ("C#6", 73, 14), ("D-6", 73,14),("D6" , 74, 15),                  ("rest", -1, -1)],
        [("G4", 55, 0),    ("G#4", 56, 1), ("A-4", 56, 1), ("A4" , 57, 2),                 ("A#4", 58, 3), ("B-4", 58, 3), ("B4" , 59, 4),                 ("C5", 60, 5), ("C#5", 61, 6), ("D-5", 61, 6), ("D5" , 62, 7),                 ("D#5", 63, 8), ("E-5", 63, 8), ("E5" , 64, 9),                 ("F5", 65, 10), ("F#5", 66, 11), ("G-5", 66, 11), ("G5", 67, 12), ("G#5", 68, 13), ("A-5", 68, 13), ("A5" , 69, 14)                ,("A#5", 70, 15), ("B-5", 70, 15), ("rest", -1, -1)],
        [("D4", 50, 0),    ("D#4", 51, 1), ("E-4", 51, 1), ("E4" , 52, 2),                 ("F4" , 53, 3),                 ("F#4", 54, 4), ("G-4", 54, 4), ("G4", 55, 5), ("G#4", 56, 6), ("A-4", 56, 6), ("A4" , 57, 7),                 ("A#4", 58, 8), ("B-4", 58, 8), ("B4" , 59, 9),                 ("C5", 60, 10), ("C#5", 61, 11), ("D-5", 61, 11), ("D5", 62, 12), ("D#5", 63, 13), ("E-5", 63, 13), ("E5" , 64, 14)                ,("F5" , 65, 15),                  ("rest", -1, -1)],
        [("A3", 45, 0),    ("A#3", 46, 1), ("B-3", 46, 1), ("B3" , 47, 2),                 ("C4" , 48, 3),                 ("C#4", 49, 4), ("D-4", 49, 4), ("D4", 50, 5), ("D#4", 51, 6), ("E-4", 51, 6), ("E4" , 52, 7),                 ("F4" , 53, 8),                 ("F#4", 54, 9), ("G-4", 54, 9), ("G4", 55, 10), ("G#4", 56, 11), ("A-4", 56, 11), ("A4", 57, 12), ("A#4", 58, 13), ("B-4", 58, 13), ("B4" , 59, 14)                ,("C5" , 60, 15),                  ("rest", -1, -1)],
        [("E3", 40, 0),    ("F3" , 41, 1),                 ("F#3", 42, 2), ("G-3", 42, 2), ("G3" , 43, 3),                 ("G#3", 44, 4), ("A-3", 44, 4), ("A3", 45, 5), ("A#3", 46, 6), ("B-3", 46, 6), ("B3" , 47, 7),                 ("C4" , 48, 8),                 ("C#4", 49, 9), ("D-4", 49, 9), ("D4", 50, 10), ("D#4", 51, 11), ("E-4", 51, 11), ("E4", 52, 12), ("F4" , 53, 13),                  ("F#4", 54, 14), ("G-4", 54,14),("G4" , 55, 15),                  ("rest", -1, -1)]
    ]
    sf_state, ttf = make_observe(fr=14)
    return frets, sf_state, ttf