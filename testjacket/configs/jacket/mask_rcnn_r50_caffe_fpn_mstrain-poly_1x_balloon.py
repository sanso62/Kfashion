# The new config inherits a base config to highlight the necessary modification
_base_ = '../mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco.py'

# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=1),
        mask_head=dict(num_classes=1)))

# Modify dataset related settings
dataset_type = 'COCODataset'
classes = ('jacket',)
data = dict(
    train=dict(
        img_prefix='C:/Users/young/Desktop/mmdetection/configs/data/jacket/train/',
        classes=classes,
        ann_file='C:/Users/young/Desktop/mmdetection/configs/data/jacket/train/instances_default.json'),
    val=dict(
        img_prefix='C:/Users/young/Desktop/mmdetection/configs/data/jacket/val/',
        classes=classes,
        ann_file='C:/Users/young/Desktop/mmdetection/configs/data/jacket/val/instances_default.json'),
    test=dict(
        img_prefix='C:/Users/young/Desktop/mmdetection/configs/data/jacket/val/',
        classes=classes,
        ann_file='C:/Users/young/Desktop/mmdetection/configs/data/jacket/val/instances_default.json'))

# We can use the pre-trained Mask RCNN model to obtain higher performance
load_from = 'C:/Users/young/Desktop/mmdetection/configs/checkpoints/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'