# lysis_curve.py

This function generates automated lysis curves (OD curves) for bacteriophage research via plotly.  

### Running in Jupyter

First, make sure your x-axis (time) data is your **zeroth (first) column** (this script always plots the first column in the csv file as the x-axis). Next, make sure you save your data in the .csv file format. Finally, navigate to the directory containing your .csv file in Jupyter.
```python
import os
os.chdir('your_path_here')
```
Next, import the lysis_curve.py file or just copy/paste it into a jupyter cell and execute.
#### Generate basic plot
This basic plot is good for cases where you do not wish to visually group your data
```python
lysis_curve('yourcsvfile.csv')
```

#### Generate plot with grouping
This argument is useful if you wish to visually group your data by color. It will automatically set each line in each group the same color, while differentiating them by assigning them different markers ('1', or '2|3' or '2|3|6' being examples of groups passed). Pass the argument to groups as a list of strings, with each column in a group separated by vertical bars.
```python
lysis_curve('yourcsvfile.csv', group=['1', '2|3', '4|5', '6|7|8'])
```

#### Generate plot with custom title
Use the argument ```title='Your Custom Title Here'```
By default, the title will be taken from your csv file name - thus 'yourcsvfile' if 'yourcsvfile.csv' is passed.

#### Generate plot with annotations
Use the argument ```annotations=True``` and follow the prompts.

#### Save as .png
Set the argument ```png=True``` and the function will generate a .png file of the graph in your current directory.

#### Save as .svg
Set the argument ```png=True``` and the function will generate a .svg file of the graph in your current directory.
Requires Orca

### Dependencies

* Python 3.5+
* Pandas ```pip install pandas```
* Plotly ```pip install plotly```
* Requests ```pip install requests```
* Orca (required for .svg output) [Install Orca](https://github.com/plotly/orca) 
