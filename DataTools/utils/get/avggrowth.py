import pandas as pd

def avggrowth(table):
    """
    Assuming that the x-axis of the table is the years
    """
    df = pd.DataFrame(table)

    df['Growth_Rate'] = df[1].pct_change(periods=1) * 100

    print(df['Growth_Rate'])

    nums = [x for x in df['Growth_Rate'] if str(x) != 'nan']
    
    print(nums)

    return (sum(nums) / len(nums))

    

    

    