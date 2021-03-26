SOURCE=/media/raphael/Elements/Datasets/cityscapes/leftImg8bit_sequence_trainvaltest/leftImg8bit_sequence
SUBSET=train
CITY=aachen
WEIGHTS=yolov5m_cityscapes.pt
CONF=0.5
IMG_SIZE=1024
OUTPUT=/media/raphael/Elements/Datasets/cityscapes/processed
#python detect.py --source=$SOURCE/$SUBSET/$CITY --weights=$WEIGHTS --conf=$CONF --project=$OUTPUT/$SUBSET --save-crops --save-txt --noinc
for SUBSET_FULL in $SOURCE/*/ ; do
    #echo "$SUBSET"
    SUBSET="$(basename -- $SUBSET_FULL)"
    OUTPUT=/media/raphael/Elements/Datasets/cityscapes/processed
    for CITY_FULL in $SUBSET_FULL*/ ; do
        #echo "$CITY"
        CITY="$(basename -- $CITY_FULL)"
        #parentdir="$(dirname "$CITY")"
        python detect.py --source=$CITY_FULL --weights=$WEIGHTS --conf=$CONF --project=$OUTPUT/$SUBSET --save-crops --save-txt --noinc
        #echo $city
    done
done

#"--source=train/aachen",
#"--weights=yolov5m_cityscapes.pt",
#"--conf=0.50",
#"--img-size=1024",
#"--project=/media/raphael/Elements/Datasets/cityscapes/processed",
#"--save-crops",
#"--save-txt",
#"--noinc"