import os
import argparse
from random import shuffle
import xml.etree.ElementTree as ET
from core.config import cfg


def convert_voc_annotation(data_path,images_path,annotations_path, image_type,ratio=0.8, use_difficult_bbox=True):
    data_path=data_path.replace('\\','/')
    # cfg_path=cfg.YOLO.CLASSES 
    classes = []
    with open('./data/classes/new.names','w') as n:

    # with open(cfg_path,'r') as f:
    #     for names in f.readlines():
    #         classes.append(names.replace('\n','').replace(' ','_'))
    #     print(classes)


        file_path=data_path+annotations_path
        filename=os.listdir(file_path)

        total_list=[]
        for image_ind in os.listdir(file_path):
            if not image_ind.endswith('.xml'):
                continue
            image_ind=image_ind.replace('.xml','')
            print(image_ind)
            image_path = os.path.join(data_path, images_path, image_ind + '.'+image_type)
            annotation = image_path
            label_path = os.path.join(data_path, annotations_path, image_ind + '.xml')
            root = ET.parse(label_path).getroot()
            objects = root.findall('object')
            # img_size=root.findall('size')
            # for size in img_size:
            #     width=float(size.find('width').text.strip())
            #     height=float(size.find('height').text.strip())
            #     print(width)
            for obj in objects:
                names=obj.find('name').text.strip().replace(' ','_')
                if names not in classes:
                    classes.append(names)
                    n.write(names.replace('\n','').replace(' ','_')+'\n')
                difficult = obj.find('difficult').text.strip()
                if (not use_difficult_bbox) and(int(difficult) == 1):
                    continue
                bbox = obj.find('bndbox')
                class_ind = classes.index(obj.find('name').text.strip())
                xmin = bbox.find('xmin').text.strip()

                xmax = bbox.find('xmax').text.strip()

                ymin = bbox.find('ymin').text.strip()
                
                ymax = bbox.find('ymax').text.strip()

                annotation += ' ' + ','.join([xmin, ymin, xmax, ymax, str(class_ind)])
            print(annotation)
            total_list.append(annotation)
            


    shuffle(total_list)
    train_list = total_list[:int(ratio*len(total_list))]
    test_list = total_list[int(ratio*len(total_list)):]

    with open('./data/dataset/train_data.txt', 'w') as f:
        for i in train_list:
            f.write(i+'\n')

    with open('./data/dataset/test_data.txt', 'w') as f:
        for i in test_list:
            f.write(i+'\n')

    return len(train_list),len(test_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    
    parser.add_argument("-d","--data_path", default='/workspace/work/tensorflow-yolov3/data/dataset/six_face/')
    parser.add_argument("-i","--images_path", default='JPEGImages')
    parser.add_argument("-x","--annotations_path",  default="Annotations")
    parser.add_argument("-t","--image_type",  default="jpg")

    flags = parser.parse_args()

    # if os.path.exists(flags.train_annotation):os.remove(flags.train_annotation)
    # if os.path.exists(flags.test_annotation):os.remove(flags.test_annotation)

    num1,num2 = convert_voc_annotation(flags.data_path,flags.images_path,flags.annotations_path, flags.image_type, 0.7, False)
    # num3 = convert_voc_annotation(os.path.join(flags.data_path, 'test/'),  'test', flags.test_annotation, False)
    print('=> The number of image for train is: %d\tThe number of image for test is:%d' %(num1, num2))

