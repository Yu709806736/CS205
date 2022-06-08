# CS205 Project 2 
Feature Selection for Nearest Neighbor Classifier
### Files
- [feature_selection.py](https://github.com/Yu709806736/CS205/blob/main/Proj2/feature_selection.py): forward selection / backward elimination algorithm
- [nearest_neighbor.py](https://github.com/Yu709806736/CS205/blob/main/Proj2/nearest_neighbor.py): knn classifier
- [main.py](https://github.com/Yu709806736/CS205/blob/main/Proj2/main.py): input, method call, and visualize
- [in.txt](https://github.com/Yu709806736/CS205/blob/main/Proj2/in.txt): input test case
### Usage
    python main.py < in.txt
and  

    python main.py
### Result - output text files and bar charts
time:  
|  | small dataset (10 features, 300 instances) | large dataset (40 features, 1000 instances) |
| :---: | :---: | :---: |
| Forward selection | 33.0 seconds | 1.51 hours |
| Backward elimination | 33.4 seconds | 1.51 hours |

bar charts:  
- small dataset & forward selection
![image1](https://github.com/Yu709806736/CS205/blob/main/Proj2/output/small_forward_32.891.jpg)
- small dataset & backward elimination
![image2](https://github.com/Yu709806736/CS205/blob/main/Proj2/output/small_backward_33.408.jpg)
- large dataset & forward selection
![image3](https://github.com/Yu709806736/CS205/blob/main/Proj2/output/large_forward_5446.461.jpg)
- large dataset & backward elimination
![image4](https://github.com/Yu709806736/CS205/blob/main/Proj2/output/large_backward_5417.736.jpg)

See other files in the [output](https://github.com/Yu709806736/CS205/tree/main/Proj2/output) directory
