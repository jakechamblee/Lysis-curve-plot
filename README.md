# lysis_curve.py

This function generates lysis curves for bacteriophage research in an automated fashion via plotly.  

### Running in Jupyter

First, make sure your data is organized so that your x-axis (time) data is your **first** column (this script assumes that will be the case). Next, make sure you save your data in the .csv file format. Finally, navigate to the directory containing your .csv file in Jupyter.
```python
import os
os.chdir('your_path_here')
```
Next, import the lysis_curve.py file or paste it into your jupyter cell and execute.
#### Generate basic plot
This basic plot is good for cases where you do not wish to visually group your data
```python
lysis_curve('yourcsvfile.csv')
```

#### Generate plot with grouping
This argument is useful if you wish to visually group your data by color. It will automatically give each group you set the same color, while differentiating them by assigning them different markers ('1', or '2|3' or '2|3|6' being examples of groups passed).
```python
lysis_curve('yourcsvfile.csv', group=['1', '2|3', '4|5', '6|7', '8|9'])
```

#### Generate plot with custom title
Use the argument title='Your Custom Title Here'
By default, the title will be taken from your csv file name - 'yourcsvfile' if 'yourcsvfile.csv'

#### Generate plot with annotations
Use the argument annotations=True and follow the prompts

### Dependencies

* Python 3.5+
* Pandas ```pip install pandas```
* Plotly ```pip install plotly```
