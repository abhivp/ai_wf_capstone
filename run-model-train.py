from model import model_train
from model import model_load

import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

base_dir = Path(__file__).parent
DATA_DIR = Path(base_dir / "data" / "cs-train").resolve()

def main():

    ## train the model
    model_train(data_dir=DATA_DIR, prefix='sl', test=False)

    ## load the model
    all_data, all_models = model_load(country='all', prefix='sl', data_dir=DATA_DIR, training=False)
    print("... models loaded: ", ",".join(all_models.keys()))
    
    print("model training complete.")


if __name__ == "__main__":

    main()
