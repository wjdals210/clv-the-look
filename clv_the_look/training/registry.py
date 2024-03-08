import glob
import os
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from clv_the_look.params import *

def load_models():
    """
    Return pickled BetaGeo and GammaGamma models
    """

    # Get the latest model version name by the timestamp on disk
    local_model_directory = os.path.join(LOCAL_REGISTRY_PATH)

    print(f"\nLoad latest models...")

    latest_bg_model = BetaGeoFitter()
    latest_bg_model.load_model(os.path.join(local_model_directory, "bg_train_model.pkl"))

    print(f"\n✅ ß-Geo Model loaded")

    latest_gg_model = GammaGammaFitter()
    latest_gg_model.load_model(os.path.join(local_model_directory, "gg_train_model.pkl"))

    print(f"\n✅ γγ Model loaded")

    return latest_bg_model, latest_gg_model
