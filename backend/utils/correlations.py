import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

def cramers_v(x,y):
    confusion_matrix = pd.crosstab(x,y)

    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    r,k = confusion_matrix.shape
    return np.sqrt(chi2/(n*(min(k-1,r-1))))
    
