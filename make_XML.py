import xml.etree.ElementTree as ET

def make_xml(title, c_list):
    path = "../kenkyu/XML/実験使用楽譜2/作成楽譜/"
    tree = ET.parse(path + title + ".musicxml")
    root = tree.getroot()# 最上階のタグを見れる

    score = root.find("part")# 楽譜情報部を取得

    i = 0
    for measure in score:# 楽譜情報部全体
        for note in measure:# ある小節内の要素を探索
            if note.tag == "note":# noteタグにフォーカス
                if note.find("rest") is None:# 条件に合うタグに運指情報を付与
                    n_notations = ET.SubElement(note, "notations")
                    n_technical = ET.SubElement(n_notations, "technical")
                    t_string = ET.SubElement(n_technical, "string")
                    t_fret = ET.SubElement(n_technical, "fret")
                
                    t_string.text = str(c_list[i][0])
                    t_fret.text = str(c_list[i][1])
                    if i < len(c_list)-1:
                        i += 1


    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(path + title + ".musicxml", encoding="UTF-8", xml_declaration=True)
