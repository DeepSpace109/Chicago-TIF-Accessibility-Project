from scipy.stats import linregress

def getRegression(table) -> dict:
    
    x = []
    y = []

    for rows in table:
        x.append(rows[0])
        y.append(rows[1])

    data = linregress(x,y)

    return data