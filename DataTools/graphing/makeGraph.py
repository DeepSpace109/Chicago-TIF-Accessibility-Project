import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

def graph(table,xname="",yname="",title="") -> None:
    """
    Takes a table, and plots a bar graph
    """

    x = []
    y = []

    for rows in table:
        x.append(rows[0])
        y.append(rows[1])
    
    plt.bar(x,y, color="blue")
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.title(str(title))

    plt.show()

    return None





