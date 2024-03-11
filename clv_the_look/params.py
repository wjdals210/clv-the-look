import os

##################  VARIABLES  ##################
MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_REGION = os.environ.get("GCP_REGION")

##################  CONSTANTS  ##################
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
LOCAL_REGISTRY_PATH = os.path.join(ROOT_PATH, "training")
