import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def graph(table,xname="",yname="") -> None:
    """
    Takes a table, and returns a dictionary containing information about a linear regression of that plot.
    """

    x = []
    y = []

    for rows in table:
        x.append(rows[0])
        y.append(rows[1])
    
    plt.bar(x,y, color="blue")
    plt.xlabel(xname)
    plt.ylabel(yname)

    plt.show()

    return None





