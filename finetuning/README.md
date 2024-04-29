### Fine Tuning the model to improve training results

Detectron2 pre-trained baseline COCO models 

| Model             | bbox AP | Segm AP | time |
|------------------ |---------|---------|------|
| Mask-RCNN R50-FPN |         |         |      | 
| Mask-RCNN X101-FPN|         |         |      |
| Cascade-RCNN      |         |         |      |
| Point-Rend        |         |         |      |
| DeepLab           |         |         |      |
| Faster-RCNN       |         |         |      |

MMDetection pre-trained baseline COCO models

| Model             | bbox AP | Segm AP | time |
|------------------ |---------|---------|------|
| Co-DETR (SOTA)    |         |         |      |
| YOLACT            |         |         |      |


Models for Object Detection:
- [Detectron2 Model Zoo](https://github.com/facebookresearch/detectron2/blob/main/MODEL_ZOO.md)
- [MMDetection Model Zoo](https://mmdetection.readthedocs.io/en/latest/model_zoo.html)
- [COCO Object detection models](https://paperswithcode.com/sota/object-detection-on-coco)

### Fine-tuning process

Random Search (hyperparameter tuning) 
- Learning rate between (0.0001, 0.001)
- Batch size between (2, 16)

Then find the config/model with highest Segm AP on the validation dataset.