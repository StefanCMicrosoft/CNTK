# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Fast R-CNN config system.

This file specifies default config options for Fast R-CNN. You should not
change values in this file. Instead, you should write a config file (in yaml)
and use cfg_from_file(yaml_file) to load it and override the default options.

Most tools in $ROOT/tools take a --cfg option to specify an override file.
    - See tools/{train,test}_net.py for example code that uses cfg_from_file()
    - See experiments/cfgs/*.yml for example YAML config override files
"""

import os
import os.path as osp
import numpy as np
# `pip install easydict` if you don't have it
from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
#   from fast_rcnn_config import cfg
cfg = __C

#
# CNTK parameters
#

__C.CNTK = edict()

__C.CNTK.FORCE_DETERMINISTIC = True
__C.CNTK.FAST_MODE = False
__C.CNTK.MAKE_MODE = False
__C.CNTK.TRAIN_E2E = False
__C.CNTK.DEBUG_OUTPUT = True
__C.CNTK.USE_MEAN_GRADIENT = True
__C.CNTK.TRAIN_CONV_LAYERS = True

__C.CNTK.DATASET = "Grocery" # "Grocery" or "Pascal"
__C.CNTK.BASE_MODEL = "AlexNet" # "VGG16" or "AlexNet"
__C.CNTK.CONV_BIAS_INIT = 0.0
__C.CNTK.SIGMA_RPN_L1 = 3.0
__C.CNTK.SIGMA_DET_L1 = 1.0
__C.CNTK.BIAS_LR_MULT = 2.0

# Learning parameters
__C.CNTK.L2_REG_WEIGHT = 0.0005
__C.CNTK.MOMENTUM_PER_MB = 0.9

# E2E config
# Caffe Faster R-CNN parameters are: base_lr: 0.001, lr_policy: "step", gamma: 0.1, stepsize: 50000, momentum: 0.9, weight_decay: 0.0005
# ==> CNTK: lr_per_sample = [0.001] * 10 + [0.0001] * 10 + [0.00001]
__C.CNTK.E2E_MAX_EPOCHS = 20
__C.CNTK.E2E_LR_PER_SAMPLE = [0.001] * 10 + [0.0001] * 10 + [0.00001]

# caffe rpn training: lr = [0.001] * 12 + [0.0001] * 4, momentum = 0.9, weight decay = 0.0005 (cf. stage1_rpn_solver60k80k.pt)
__C.CNTK.RPN_EPOCHS = 28 # 12 + 16 ?
__C.CNTK.RPN_LR_PER_SAMPLE = [0.001] * 12 + [0.0001] * 4

# caffe frcn training: lr = [0.001] * 6 + [0.0001] * 2, momentum = 0.9, weight decay = 0.0005 (cf. stage1_fast_rcnn_solver30k40k.pt)
__C.CNTK.FRCN_EPOCHS = 28 # 8 # 6 + 8 ?
__C.CNTK.FRCN_LR_PER_SAMPLE = [0.001] * 6 + [0.0001] * 2
# Current setting for CNTK:
#__C.CNTK.FRCN_EPOCHS = 20
#__C.CNTK.FRCN_LR_PER_SAMPLE = [0.001] * 6 + [0.0005] * 6 + [0.0001]

__C.CNTK.INPUT_ROIS_PER_IMAGE = 50
__C.CNTK.IMAGE_WIDTH = 850
__C.CNTK.IMAGE_HEIGHT = 850

__C.CNTK.RESULTS_NMS_THRESHOLD = 0.3 # see also: __C.TEST.NMS = 0.3
__C.CNTK.RESULTS_NMS_CONF_THRESHOLD = 0.0
__C.CNTK.RESULTS_BGR_PLOT_THRESHOLD = 0.1

__C.CNTK.GRAPH_TYPE = "png" # "png" or "pdf"
__C.CNTK.VISUALIZE_RESULTS = True
__C.CNTK.DRAW_NEGATIVE_ROIS = False
__C.CNTK.DRAW_UNREGRESSED_ROIS = False

__C.CNTK.FEATURE_STREAM_NAME = 'features'
__C.CNTK.ROI_STREAM_NAME = 'roiAndLabel'
__C.CNTK.DIMS_STREAM_NAME = 'dims'


#
# Data sets
#
if __C.CNTK.DATASET == "Grocery":
    __C.CNTK.CLASSES = ('__background__',  # always index 0
                        'avocado', 'orange', 'butter', 'champagne', 'eggBox', 'gerkin', 'joghurt', 'ketchup',
                        'orangeJuice', 'onion', 'pepper', 'tomato', 'water', 'milk', 'tabasco', 'mustard')
    __C.CNTK.MAP_FILE_PATH = "../../DataSets/Grocery"
    __C.CNTK.TRAIN_MAP_FILE = "train_img_file.txt"
    __C.CNTK.TEST_MAP_FILE = "test_img_file.txt"
    __C.CNTK.TRAIN_ROI_FILE = "train_roi_file.txt"
    __C.CNTK.TEST_ROI_FILE = "test_roi_file.txt"
    __C.CNTK.NUM_TRAIN_IMAGES = 20
    __C.CNTK.NUM_TEST_IMAGES = 5
    __C.CNTK.PROPOSAL_LAYER_PARAMS = "'feat_stride': 16\n'scales':\n - 4 \n - 8 \n - 12"

if __C.CNTK.DATASET == "Pascal":
    __C.CNTK.CLASSES = ('__background__',  # always index 0
                        'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable',
                        'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor')
    __C.CNTK.MAP_FILE_PATH = "../../DataSets/Pascal/mappings"
    __C.CNTK.TRAIN_MAP_FILE = "trainval2007.txt"
    __C.CNTK.TRAIN_ROI_FILE = "trainval2007_rois_abs-xyxy_noPad_skipDif.txt"
    __C.CNTK.TEST_MAP_FILE = "test2007.txt"
    __C.CNTK.TEST_ROI_FILE = "test2007_rois_abs-xyxy_noPad_skipDif.txt"
    __C.CNTK.NUM_TRAIN_IMAGES = 5010
    __C.CNTK.NUM_TEST_IMAGES = 4952
    __C.CNTK.PROPOSAL_LAYER_PARAMS = "'feat_stride': 16\n'scales':\n - 8 \n - 16 \n - 32"

#
# Base models
#

if __C.CNTK.BASE_MODEL == "AlexNet":
    __C.CNTK.BASE_MODEL_FILE = "AlexNet.model"
    __C.CNTK.FEATURE_NODE_NAME = "features"
    __C.CNTK.LAST_CONV_NODE_NAME = "conv5.y" # == relu
    __C.CNTK.START_TRAIN_CONV_NODE_NAME = "conv3.y"
    __C.CNTK.POOL_NODE_NAME = "pool3"
    __C.CNTK.LAST_HIDDEN_NODE_NAME = "h2_d"
    __C.CNTK.RPN_NUM_CHANNELS = 256
    __C.CNTK.ROI_DIM = 6
    # 1.0: 84.17|88.85|79.79|86.25|84.9 --- det: 89.64|89.64 --- mean grad: 89.64 --- conv layers: 75.10
    # after merging to latest master:
    # (1.0, det, conv): 0.6983, (1.0, det): 89.55
    __C.CNTK.E2E_LR_FACTOR = 1.0
    # 1.0: 85.83|85.27|94.10|94.06 --- det: 89.06
    # after merging to latest master:
    # (1.0, det, conv): 91.67, (1.0, det): 82.96, (1.0, det, higher_20): 83.54 +conv: 94.8, caffe 16|20: 93.54, 28|14: 94.01, 28|28:
    __C.CNTK.RPN_LR_FACTOR = 1.0
    __C.CNTK.FRCN_LR_FACTOR = 1.0

if __C.CNTK.BASE_MODEL == "VGG16":
    __C.CNTK.BASE_MODEL_FILE = "VGG16_ImageNet_Caffe.model" # == "VGG16_ImageNet.cntkmodel"
    __C.CNTK.FEATURE_NODE_NAME = "data"
    __C.CNTK.LAST_CONV_NODE_NAME = "relu5_3"
    __C.CNTK.START_TRAIN_CONV_NODE_NAME = "pool2"
    __C.CNTK.POOL_NODE_NAME = "pool5"
    __C.CNTK.LAST_HIDDEN_NODE_NAME = "drop7"
    __C.CNTK.RPN_NUM_CHANNELS = 512
    __C.CNTK.ROI_DIM = 7
    # det: 90.48
    # after merging to latest master:
    # (1.0, det, conv): 66.96, (1.0, det): 77.8, (2.0, det): 75.53
    __C.CNTK.E2E_LR_FACTOR = 1.0
    # Cuda OOM
    __C.CNTK.RPN_LR_FACTOR = 1.0
    __C.CNTK.FRCN_LR_FACTOR = 1.0

#
# Training options
#

__C.TRAIN = edict()

# Scales to use during training (can list multiple scales)
# Each scale is the pixel size of an image's shortest side
__C.TRAIN.SCALES = (600,)

# Max pixel size of the longest side of a scaled input image
__C.TRAIN.MAX_SIZE = 1000

# Images to use per minibatch
__C.TRAIN.IMS_PER_BATCH = 2

# Minibatch size (number of regions of interest [ROIs])
__C.TRAIN.BATCH_SIZE = 128

# Fraction of minibatch that is labeled foreground (i.e. class > 0)
__C.TRAIN.FG_FRACTION = 0.25

# Overlap threshold for a ROI to be considered foreground (if >= FG_THRESH)
__C.TRAIN.FG_THRESH = 0.5

# Overlap threshold for a ROI to be considered background (class = 0 if
# overlap in [LO, HI))
__C.TRAIN.BG_THRESH_HI = 0.5
__C.TRAIN.BG_THRESH_LO = 0.0

# Use horizontally-flipped images during training?
__C.TRAIN.USE_FLIPPED = True

# Train bounding-box regressors
__C.TRAIN.BBOX_REG = True

# Overlap required between a ROI and ground-truth box in order for that ROI to
# be used as a bounding-box regression training example
__C.TRAIN.BBOX_THRESH = 0.5

# Iterations between snapshots
__C.TRAIN.SNAPSHOT_ITERS = 10000

# solver.prototxt specifies the snapshot path prefix, this adds an optional
# infix to yield the path: <prefix>[_<infix>]_iters_XYZ.caffemodel
__C.TRAIN.SNAPSHOT_INFIX = ''

# Use a prefetch thread in roi_data_layer.layer
# So far I haven't found this useful; likely more engineering work is required
__C.TRAIN.USE_PREFETCH = False

# Normalize the targets (subtract empirical mean, divide by empirical stddev)
__C.TRAIN.BBOX_NORMALIZE_TARGETS = True
# Deprecated (inside weights)
__C.TRAIN.BBOX_INSIDE_WEIGHTS = (1.0, 1.0, 1.0, 1.0)
# Normalize the targets using "precomputed" (or made up) means and stdevs
# (BBOX_NORMALIZE_TARGETS must also be True)
__C.TRAIN.BBOX_NORMALIZE_TARGETS_PRECOMPUTED = True # TODO: do these means make sense for other data sets than Pascal?
__C.TRAIN.BBOX_NORMALIZE_MEANS = (0.0, 0.0, 0.0, 0.0)
__C.TRAIN.BBOX_NORMALIZE_STDS = (0.1, 0.1, 0.2, 0.2)

# Train using these proposals
__C.TRAIN.PROPOSAL_METHOD = 'selective_search'

# Make minibatches from images that have similar aspect ratios (i.e. both
# tall and thin or both short and wide) in order to avoid wasting computation
# on zero-padding.
__C.TRAIN.ASPECT_GROUPING = True

# IOU >= thresh: positive example
__C.TRAIN.RPN_POSITIVE_OVERLAP = 0.7
# IOU < thresh: negative example
__C.TRAIN.RPN_NEGATIVE_OVERLAP = 0.3
# If an anchor statisfied by positive and negative conditions set to negative
__C.TRAIN.RPN_CLOBBER_POSITIVES = False
# Max number of foreground examples
__C.TRAIN.RPN_FG_FRACTION = 0.5
# Total number of examples
__C.TRAIN.RPN_BATCHSIZE = 256
# NMS threshold used on RPN proposals
__C.TRAIN.RPN_NMS_THRESH = 0.7
# Number of top scoring boxes to keep before apply NMS to RPN proposals
__C.TRAIN.RPN_PRE_NMS_TOP_N = 12000
# Number of top scoring boxes to keep after applying NMS to RPN proposals
__C.TRAIN.RPN_POST_NMS_TOP_N = 2000
# Proposal height and width both need to be greater than RPN_MIN_SIZE (at orig image scale)
__C.TRAIN.RPN_MIN_SIZE = 16
# Deprecated (outside weights)
__C.TRAIN.RPN_BBOX_INSIDE_WEIGHTS = (1.0, 1.0, 1.0, 1.0)
# Give the positive RPN examples weight of p * 1 / {num positives}
# and give negatives a weight of (1 - p)
# Set to -1.0 to use uniform example weighting
__C.TRAIN.RPN_POSITIVE_WEIGHT = -1.0


#
# Testing options
#

__C.TEST = edict()

# Scales to use during testing (can list multiple scales)
# Each scale is the pixel size of an image's shortest side
__C.TEST.SCALES = (600,)

# Max pixel size of the longest side of a scaled input image
__C.TEST.MAX_SIZE = 1000

# Overlap threshold used for non-maximum suppression (suppress boxes with
# IoU >= this threshold)
__C.TEST.NMS = 0.3

# Experimental: treat the (K+1) units in the cls_score layer as linear
# predictors (trained, eg, with one-vs-rest SVMs).
__C.TEST.SVM = False

# Test using bounding-box regressors
__C.TEST.BBOX_REG = True

# Propose boxes
__C.TEST.HAS_RPN = False

# Test using these proposals
__C.TEST.PROPOSAL_METHOD = 'selective_search'

## NMS threshold used on RPN proposals
__C.TEST.RPN_NMS_THRESH = 0.7
## Number of top scoring boxes to keep before apply NMS to RPN proposals
__C.TEST.RPN_PRE_NMS_TOP_N = 6000 # 12000 # caffe: 6000
## Number of top scoring boxes to keep after applying NMS to RPN proposals
__C.TEST.RPN_POST_NMS_TOP_N = 300 # 2000 # caffe: 300
# Proposal height and width both need to be greater than RPN_MIN_SIZE (at orig image scale)
__C.TEST.RPN_MIN_SIZE = 16


#
# MISC
#

# The mapping from image coordinates to feature map coordinates might cause
# some boxes that are distinct in image space to become identical in feature
# coordinates. If DEDUP_BOXES > 0, then DEDUP_BOXES is used as the scale factor
# for identifying duplicate boxes.
# 1/16 is correct for {Alex,Caffe}Net, VGG_CNN_M_1024, and VGG16
__C.DEDUP_BOXES = 1./16.

# Pixel mean values (BGR order) as a (1, 1, 3) array
# We use the same pixel mean for all networks even though it's not exactly what
# they were trained with
__C.PIXEL_MEANS = np.array([[[102.9801, 115.9465, 122.7717]]])

# For reproducibility
__C.RNG_SEED = 3

# A small number that's used many times
__C.EPS = 1e-14

# Root directory of project
__C.ROOT_DIR = osp.abspath(osp.join(osp.dirname(__file__), '..', '..'))

# Data directory
__C.DATA_DIR = osp.abspath(osp.join(__C.ROOT_DIR, 'data'))

# Model directory
__C.MODELS_DIR = osp.abspath(osp.join(__C.ROOT_DIR, 'models', 'pascal_voc'))

# Name (or path to) the matlab executable
__C.MATLAB = 'matlab'

# Place outputs under an experiments directory
__C.EXP_DIR = 'default'

# Use GPU implementation of non-maximum suppression
__C.USE_GPU_NMS = True

# Default GPU device id
__C.GPU_ID = 0


def get_output_dir(imdb, net=None):
    """Return the directory where experimental artifacts are placed.
    If the directory does not exist, it is created.

    A canonical path is built using the name from an imdb and a network
    (if not None).
    """
    outdir = osp.abspath(osp.join(__C.ROOT_DIR, 'output', __C.EXP_DIR, imdb.name))
    if net is not None:
        outdir = osp.join(outdir, net.name)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    return outdir

def _merge_a_into_b(a, b):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    if type(a) is not edict:
        return

    for k, v in a.iteritems():
        # a must specify keys that are in b
        if not b.has_key(k):
            raise KeyError('{} is not a valid config key'.format(k))

        # the types must match, too
        old_type = type(b[k])
        if old_type is not type(v):
            if isinstance(b[k], np.ndarray):
                v = np.array(v, dtype=b[k].dtype)
            else:
                raise ValueError(('Type mismatch ({} vs. {}) '
                                'for config key: {}').format(type(b[k]),
                                                            type(v), k))

        # recursively merge dicts
        if type(v) is edict:
            try:
                _merge_a_into_b(a[k], b[k])
            except:
                print('Error under config key: {}'.format(k))
                raise
        else:
            b[k] = v

def cfg_from_file(filename):
    """Load a config file and merge it into the default options."""
    import yaml
    with open(filename, 'r') as f:
        yaml_cfg = edict(yaml.load(f))

    _merge_a_into_b(yaml_cfg, __C)

def cfg_from_list(cfg_list):
    """Set config keys via list (e.g., from command line)."""
    from ast import literal_eval
    assert len(cfg_list) % 2 == 0
    for k, v in zip(cfg_list[0::2], cfg_list[1::2]):
        key_list = k.split('.')
        d = __C
        for subkey in key_list[:-1]:
            assert d.has_key(subkey)
            d = d[subkey]
        subkey = key_list[-1]
        assert d.has_key(subkey)
        try:
            value = literal_eval(v)
        except:
            # handle the case when v is a string literal
            value = v
        assert type(value) == type(d[subkey]), \
            'type {} does not match original type {}'.format(
            type(value), type(d[subkey]))
        d[subkey] = value
