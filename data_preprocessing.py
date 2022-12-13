# kfashion 데이터타입을 coco 데이터 타입으로 바꾸는 매서드 작성
import json
import zipfile
import os
import shutil
import re
import random

# try:
#     print("*")
#     shutil.rmtree("./tmp")
# except:
#     pass
# os.mkdir("./tmp")
# try:
#     print("**")
#     shutil.rmtree("./kfashion")
# except:
#     pass
# os.mkdir("./kfashion")
# os.mkdir("./kfashion/train")
# os.mkdir("./kfashion/val")
def split_train_and_val():
    train_annotations, val_annotations=[], []
    train_images, val_images=[], []
    categories=[]
    for (_, _, files) in os.walk("./datasetzips"):
        for i, f in enumerate(files):
            shutil.unpack_archive("./datasetzips/"+f, f"tmp/{i}", "zip")

    category_id, categories_name=0, []
    train_image_id, val_image_id, image_file_name=0, 0,{}
    train_annotation_id, val_annotation_id=0,0
    listdir=os.listdir(f"./tmp")
    listdir.sort(key = lambda x: int(x) )
    for dir in listdir:
        train_img_id_list={}
        val_img_id_list={}
        for f_name in os.listdir(f"./tmp/"+dir+"/annotations"):
            with open(f"./tmp/"+dir+"/annotations/"+f_name, "r") as file:
                label=json.load(file)
                if label["categories"][0]["name"] not in categories_name:
                    categories.append({"id" : category_id, "name": label["categories"][0]["name"]})
                    categories_name.append(label["categories"][0]["name"])
                    category_id+=1
                # print(label["images"])
                random.shuffle(label["images"])
                len_images=len(label["images"])
                # init_train_image_id=train_image_id
                for img in label["images"][:int(len_images*0.9)]:
                    train_img_id_list[img["id"]]= train_image_id
                    img["id"]=train_image_id
                    image_file_name[re.sub("/.*/","",img["file_name"])]=(0, train_image_id)
                    img["file_name"]=str(train_image_id)+".jpg"
                    train_images.append(img)
                    train_image_id+=1      

                # init_val_image_id=val_image_id
                for img in label["images"][int(len_images*0.9):]:
                    val_img_id_list[img["id"]]=val_image_id
                    img["id"]=val_image_id
                    image_file_name[re.sub("/.*/","",img["file_name"])]=(1, val_image_id)
                    img["file_name"]=str(val_image_id)+".jpg"
                    val_images.append(img)
                    val_image_id+=1

                for ann in label["annotations"]:
                    if ann["image_id"] in train_img_id_list.keys():
                        ann["id"]=train_annotation_id
                        ann["image_id"]=train_img_id_list[ann["image_id"]]
                        ann["category_id"]=category_id-1
                        train_annotations.append(ann)
                        train_annotation_id+=1
                    else:
                        ann["id"]=val_annotation_id
                        ann["image_id"]=val_img_id_list[ann["image_id"]]
                        ann["category_id"]=category_id-1
                        val_annotations.append(ann)
                        val_annotation_id+=1
                


        jsondata=dict([("categories", categories), ("images", train_images), ("annotations", train_annotations) ])
        with open("./kfashion/train/annotation_kfashion.json", "w") as f:
            json.dump(jsondata, f)

        jsondata=dict([("categories", categories), ("images", val_images), ("annotations", val_annotations) ])
        with open("./kfashion/val/annotation_kfashion.json", "w") as f:
            json.dump(jsondata, f)

    for dir in listdir:  
        for img_f in os.listdir(f"./tmp/"+dir+"/images"):
            file_name=str(image_file_name[img_f][1])
            if image_file_name[img_f][0]==0:
                shutil.move("./tmp/"+dir+"/images/"+img_f, f"./kfashion/train/{file_name}.jpg")
            else:
                shutil.move("./tmp/"+dir+"/images/"+img_f, f"./kfashion/val/{file_name}.jpg")                
              
# split_train_and_val()

# try:
#     shutil.rmtree("./tmp")
# except:
#     pass


