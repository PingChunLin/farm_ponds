# how to run whole pond_main_kadwanchi from scratch

1. image_cut.py image (to test), mask (to test mask) 
    1. extra step to use image_null_detector py to get rid of borders in slider_all for test_kadwanchi after step 8
2. keep masks with non zero data (test_masks_filter)
3. copy paste test_mask to train_new nask and test to train_new
4. make the trainset and the train mask match in the train_new and train_new mask files (train_selection)
5. run create val_new to random select 5 out of 59 as val set vals_new mask created at the same time
6. invert color to the opposite so that white is the target for both train_mask and val_mask (image_color_invert) 
7. create custom coco dataset ipynb and put the jsons in corresponding folders (train_new val_new)
8. pond_main_kadwanchi
9. instance filter py
10. array_merge_tiles.py
11. georeference.py to set GPS (the lat longs are off as for 11/14)
12. area_calculator.py to produce csv
