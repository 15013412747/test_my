import cv2
import os
import random
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom

img_path = '/home/psdz/下载/test/img/'
save_path = '/home/psdz/下载/test/save_img/'
xml_path = '/home/psdz/下载/test/xml/'
save_xml = '/home/psdz/下载/test/save_xml/'
img_names = os.listdir(img_path)
img_num = len(img_names)
print('img_num:', img_num)

for imgname in img_names:
    imgpath = img_path + imgname
    img = cv2.imread(imgpath)
    img_h, img_w = img.shape[0], img.shape[1]

    i = random.randint(0, img_num - 1)
    print('i:', i)
    add_path = img_path + img_names[i]
    addimg = cv2.imread(add_path)
    add_h, add_w = addimg.shape[0], addimg.shape[1]
    if add_h != img_h or add_w != img_w:
        print('resize!')
        addimg = cv2.resize(addimg, (img_w, img_h), interpolation=cv2.INTER_LINEAR)
    scale_h, scale_w = img_h / add_h, img_w / add_w

    lam = np.random.beta(0.5, 0.5)
    mixed_img = lam * img + (1 - lam) * addimg
    save_img = save_path + imgname[:-4] + '_3.jpg'
    cv2.imwrite(save_img, mixed_img)
    print(save_img)

    if imgname != img_names[i]:
        xmlfile1 = xml_path + imgname[:-4] + '.xml'
        xmlfile2 = xml_path + img_names[i][:-4] + '.xml'

        tree1 = ET.parse(xmlfile1)
        tree2 = ET.parse(xmlfile2)

        doc = xml.dom.minidom.Document()
        root = doc.createElement("annotation")
        doc.appendChild(root)

        nodeframe = doc.createElement("frame")
        nodeframe.appendChild(doc.createTextNode(imgname[:-4] + '_3'))

        objects = []

        for obj in tree1.findall("object"):
            obj_struct = {}
            obj_struct["name"] = obj.find("name").text
            #        obj_struct["pixelcolor"] = obj.find("pixelcolor").text
            #        obj_struct["difficult"] = obj.find("difficult").text
            bbox = obj.find("bndbox")
            obj_struct["bbox"] = [int(bbox.find("xmin").text),
                                  int(bbox.find("ymin").text),
                                  int(bbox.find("xmax").text),
                                  int(bbox.find("ymax").text)]
            objects.append(obj_struct)

        for obj in tree2.findall("object"):
            obj_struct = {}
            obj_struct["name"] = obj.find("name").text
            #        obj_struct["pixelcolor"] = obj.find("pixelcolor").text
            #        obj_struct["difficult"] = obj.find("difficult").text
            bbox = obj.find("bndbox")
            obj_struct["bbox"] = [int(int(bbox.find("xmin").text) * scale_w),
                                  int(int(bbox.find("ymin").text) * scale_h),
                                  int(int(bbox.find("xmax").text) * scale_w),
                                  int(int(bbox.find("ymax").text) * scale_h)]
            objects.append(obj_struct)

        for obj in objects:
            nodeobject = doc.createElement("object")
            nodename = doc.createElement("name")
            #        nodepixelcolor = doc.createElement("pixelcolor")
            #        nodedifficult = doc.createElement("difficult")
            nodebndbox = doc.createElement("bndbox")
            nodexmin = doc.createElement("xmin")
            nodeymin = doc.createElement("ymin")
            nodexmax = doc.createElement("xmax")
            nodeymax = doc.createElement("ymax")
            nodename.appendChild(doc.createTextNode(obj["name"]))
            #        nodepixelcolor.appendChild(doc.createTextNode(obj["pixelcolor"]))
            #        nodedifficult.appendChild(doc.createTextNode(obj["difficult"]))
            nodexmin.appendChild(doc.createTextNode(str(obj["bbox"][0])))
            nodeymin.appendChild(doc.createTextNode(str(obj["bbox"][1])))
            nodexmax.appendChild(doc.createTextNode(str(obj["bbox"][2])))
            nodeymax.appendChild(doc.createTextNode(str(obj["bbox"][3])))

            nodebndbox.appendChild(nodexmin)
            nodebndbox.appendChild(nodeymin)
            nodebndbox.appendChild(nodexmax)
            nodebndbox.appendChild(nodeymax)

            nodeobject.appendChild(nodename)
            #        nodeobject.appendChild(nodepixelcolor)
            #        nodeobject.appendChild(nodedifficult)
            nodeobject.appendChild(nodebndbox)

            root.appendChild(nodeobject)

        fp = open(save_xml + imgname[:-4] + "_3.xml", "w")
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        fp.close()

    else:
        xmlfile1 = xml_path + imgname[:-4] + '.xml'
        tree1 = ET.parse(xmlfile1)

        doc = xml.dom.minidom.Document()
        root = doc.createElement("annotation")
        doc.appendChild(root)

        nodeframe = doc.createElement("frame")
        nodeframe.appendChild(doc.createTextNode(imgname[:-4] + '_3'))

        objects = []

        for obj in tree1.findall("object"):
            obj_struct = {}
            obj_struct["name"] = obj.find("name").text
            #        obj_struct["pixelcolor"] = obj.find("pixelcolor").text
            #        obj_struct["difficult"] = obj.find("difficult").text
            bbox = obj.find("bndbox")
            obj_struct["bbox"] = [int(bbox.find("xmin").text),
                                  int(bbox.find("ymin").text),
                                  int(bbox.find("xmax").text),
                                  int(bbox.find("ymax").text)]
            objects.append(obj_struct)

        for obj in objects:
            nodeobject = doc.createElement("object")
            nodename = doc.createElement("name")
            #        nodepixelcolor = doc.createElement("pixelcolor")
            #        nodedifficult = doc.createElement("difficult")
            nodebndbox = doc.createElement("bndbox")
            nodexmin = doc.createElement("xmin")
            nodeymin = doc.createElement("ymin")
            nodexmax = doc.createElement("xmax")
            nodeymax = doc.createElement("ymax")
            nodename.appendChild(doc.createTextNode(obj["name"]))
            #        nodepixelcolor.appendChild(doc.createTextNode(obj["pixelcolor"]))
            #        nodedifficult.appendChild(doc.createTextNode(obj["difficult"]))
            nodexmin.appendChild(doc.createTextNode(str(obj["bbox"][0])))
            nodeymin.appendChild(doc.createTextNode(str(obj["bbox"][1])))
            nodexmax.appendChild(doc.createTextNode(str(obj["bbox"][2])))
            nodeymax.appendChild(doc.createTextNode(str(obj["bbox"][3])))

            nodebndbox.appendChild(nodexmin)
            nodebndbox.appendChild(nodeymin)
            nodebndbox.appendChild(nodexmax)
            nodebndbox.appendChild(nodeymax)

            nodeobject.appendChild(nodename)
            #        nodeobject.appendChild(nodepixelcolor)
            #        nodeobject.appendChild(nodedifficult)
            nodeobject.appendChild(nodebndbox)

            root.appendChild(nodeobject)

        fp = open(save_xml + imgname[:-4] + "_3.xml", "w")
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        fp.close()

