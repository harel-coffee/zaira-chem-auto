import os
import sys

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "../bidd-molmap/"))

import pandas as pd
import numpy as np

from molmap.model import load_model

file_name = sys.argv[1]
x1_path = sys.argv[2]
x2_path = sys.argv[3]
model_path = sys.argv[4]
path = os.path.dirname(file_name)

SMILES_COLUMN = "smiles"

data = pd.read_csv(file_name)

smiles_list = list(data[SMILES_COLUMN])

with open(x1_path, "rb") as f:
    X1 = np.load(f)

with open(x2_path, "rb") as f:
    X2 = np.load(f)

# Load regression
if os.path.exists(os.path.join(model_path, "reg")):
    reg = load_model(os.path.join(model_path, "reg"))
    reg_preds = reg.predict((X1, X2))[:, 0]
    np.save(os.path.join(path, "reg_preds.npy"), reg_preds)

# Load classification
if os.path.exists(os.path.join(model_path, "clf")):
    clf = load_model(os.path.join(model_path, "clf"))
    clf_preds = clf.predict_proba((X1, X2))[:, 1]
    np.save(os.path.join(path, "clf_preds.npy"), clf_preds)
