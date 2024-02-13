from music21 import *
from Viterbi import *
from make_XML import make_xml
import time as t


def makeTab(Input, St, k, tmp, notes, length):
    def Init(k, tmp, m, Input):
        # 楽譜のレイアウトを決定
        Layout = layout.SystemLayout()
        m.append(Layout)
            
        # テンポ
        num = Input.metronomeMarkBoundaries()[0][2].number
        tmp_ = tempo.MetronomeMark(number = num, referent=tmp)
        m.append(tmp_)

        # StaffLayoutで、五線譜やTABの六線譜を描画
        Staff_Layout = layout.StaffLayout(staffLines=6)
        m.append(Staff_Layout)

        # ここで表示する形式をTabにしている
        clf = clef.TabClef()
        clf.line = 6
        m.append(clf)

        # 調と拍子の情報
        keys = key.KeySignature(k)
        m.append(keys)
        t_Signature = meter.TimeSignature()
        m.append(t_Signature)
        
        return m
    index = 0
    
    k_ = 0
    for i in range(1, length):
        m = stream.Measure(number=i)
        # 1小節目(初期情報入力)
        if i == 1:
            m = Init(k[k_], tmp, m, Input)
            k_ += 1
        if i % 4 == 1:
            # 4小節ごとに改行
            m.append(layout.SystemLayout(isNew=True))
        d = 0.0
        while d < 4.0 and index < len(notes):# 1小節内には4拍子分の音しか入らない
            sub_note = []# 音符格納用の配列
            d += notes[index].duration.quarterLength
            if type(notes[index]) == harmony.ChordSymbol \
                or type(notes[index]) == chord.Chord:# コードなら
                if type(notes[index]) == harmony.ChordSymbol:# ChordSymbolなら
                    n = harmony.ChordSymbol(notes[index].figure)
                elif type(notes[index]) == chord.Chord:# Chordなら
                    C = [str(item) for item in notes[index].pitches]
                    n = chord.Chord(notes=C, quarterLength = notes[index].duration.quarterLength)
                if not notes[index].tie is None:# タイ記号があれば
                    n.tie = tie.Tie(notes[index].tie.type)
                sub_note.append(n)
            elif type(notes[index]) == note.Note:# 音符なら
                n = note.Note(notes[index].nameWithOctave, quarterLength = notes[index].duration.quarterLength)
                n.articulations = notes[index].articulations
                if not notes[index].tie is None:# タイ記号があれば
                    n.tie = tie.Tie(notes[index].tie.type)
                sub_note.append(n)
            elif type(notes[index]) == note.Rest:# 休符なら
                sub_note.append(note.Rest(notes[index].duration.quarterLength))
            elif type(notes[index]) == key.KeySignature:# key情報なら
                sub_note.append(key.KeySignature(k[k_]))
                k_ += 1
            m.append(sub_note)
            index += 1
        if i == length-1:# 最後の小節に線を入れる
            line = bar.Barline(type="final")
            m.insert(0, line)
        St.append(m)


def getNotes(n):
    obserb = []
    for i in range(len(n)):
        if type(n[i]) == note.Note:
            oct_name = n[i].nameWithOctave
            if type(n[i-1]) == harmony.ChordSymbol:
                if n[i].name not in elm:
                    elm.append(n[i].name)
                elm.insert(0, note.Note(oct_name))
                obserb.append([elm, n[i].duration.quarterLength, "chord"])
            else:
                obserb.append([n[i], n[i].duration.quarterLength, "note"])
        elif type(n[i]) == note.Rest:
            if type(n[i-1]) == harmony.ChordSymbol:
                obserb.append([elm, n[i].duration.quarterLength, "chord"])
            else:
                obserb.append([n[i], n[i].duration.quarterLength, "rest"])
        elif type(n[i]) == harmony.ChordSymbol:
            elm = [str(item)[:-1] for item in n[i].pitches]
        elif type(n[i]) == key.KeySignature:
            obserb.append([n[i].sharps, [str(k)[:-1] for k in key.Key(key.sharpsToPitch(n[i].sharps)).pitches], "scale"])
    return obserb


def makeTabInfo(obserb, notes_list):
    Unshi = Viterbi_guitar(obserb)
    chords = []
    i, u = 0, 0
    new_notes = []
    print(">>Making Tablature...")
    st_marcov = t.perf_counter()
    while i <= len(notes_list)-1 and u <= len(Unshi)-1:
        if type(notes_list[i]) == harmony.ChordSymbol:
            new_notes.append(notes_list[i])
        else:
            if Unshi[u][-1] == "note":
                n = note.Note(*Unshi[u][0], quarterLength = Unshi[u][-2])
                s,f = Unshi[u][1][0][0], Unshi[u][1][0][1]
                n.articulations = [articulations.StringIndication(s), articulations.FretIndication(f)]
                if not notes_list[i].tie is None:
                    n.tie = tie.Tie(notes_list[i].tie.type)
                new_notes.append(n)
                chords.append((s,f))
            elif Unshi[u][-1] == "chord":
                c = chord.Chord(notes=Unshi[u][0], quarterLength = Unshi[u][-2])
                for item in Unshi[u][1]:
                    chords.append((item[0], item[1]))
                new_notes.append(c)
            elif Unshi[u][-1] == "rest":
                r = note.Rest(quarterLength = Unshi[u][-2])
                new_notes.append(r)
            elif Unshi[u][-1] == "scale":
                s = key.KeySignature(Unshi[u][0])
                new_notes.append(s)
            u += 1
        i += 1
    en_marcov = t.perf_counter()
    
    print(">>done: {:.2f}s\n".format(en_marcov - st_marcov))
    return new_notes, chords


def main():
    st_p = t.perf_counter()
    print("Program start...")
    path = "XML/"
    title = "TEST11"
    
    Input = converter.parse(path + title + ".musicxml")
    # 必要情報の格納
    # 調とスケールを取得
    notes, key_name, scale_list = [], [], []
    tmp = ""
    for nar in Input.flat:
        if type(nar) == key.KeySignature:
            k_ = nar.sharps
            key_name.append(k_)
            scale_list.append([str(k)[:-1] for k in key.Key(key.sharpsToPitch(k_)).pitches])
            notes.append(nar)
        if type(nar) == tempo.MetronomeMark:
            tmp = nar.referent.type
        elif type(nar) == harmony.ChordSymbol or type(nar) == note.Note \
            or type(nar) == note.Rest or type(nar) == chord.Chord:
            notes.append(nar)
    
    # 楽譜の基盤
    score = stream.Score()

    # ここで楽器情報をギターにする
    inst = instrument.AcousticGuitar()
    stream1 = stream.Stream()
    stream1.insert(0, inst)

    # 小節情報を探す
    num = 0
    for i in range(len(Input)):
        if type(Input[i]) == stream.Part:
            num = i
            break

    # 取得した楽譜の小節数        
    length = len(Input[num])
    
    # 主旋律(観測値)
    obserb = getNotes(notes)

    # 楽譜情報の作成
    score_elm, c_list = makeTabInfo(obserb, notes)

    # 楽譜の作成
    makeTab(Input, stream1, key_name, tmp, score_elm[1:], length)
    score.append(stream1)
    score.insert(0, metadata.Metadata())
    
    score.metadata.title = Input.flat.metadata.title + "(変換後)"
    score.metadata.composer = Input.flat.metadata.composer
    score.append(layout.ScoreLayout())

    score.write("musicxml", fp= path + score.metadata.title + ".musicxml")
    make_xml(score.metadata.title, c_list)

    en_p = t.perf_counter()
    print("done: {:.2f}s".format(en_p - st_p))

main()
