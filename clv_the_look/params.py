import os
import numpy as np

##################  VARIABLES  ##################
MODEL_TARGET = os.environ.get("MODEL_TARGET")

##################  CONSTANTS  ##################
#LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), "code", "wjdals210", "clv-the-look", "clv_the_look",)
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
LOCAL_REGISTRY_PATH = os.path.join(ROOT_PATH, "training")
