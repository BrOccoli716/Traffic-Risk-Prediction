# Traffic Risk Prediction Model Based on Time-Space Graph Convolution Network
> This is the implementation of a paper for my graduate design at Tsinghua University.

![](C:\Users\fuym20\Desktop\Python\2024Final\TrafficRiskPrediction\Procedure.png)


## 
## Abstract   
With the process of urbanization, the vehicle possessing quantity of city dwellers has increased remarkably, which unfortunately leads to the constant rise of traffic accident risk, causing severe economic losses and casualties. Therefore, performing accurate prediction on traffic risk, along with discerning traffic risk hot zones, has vital researching significance to effectively reduce the damage caused by traffic accidents.

First, the paper conducts statistical analysis of current urban traffic accident situation and clarifies the definition of traffic risk, explaining the significance and necessity of traffic risk prediction. Then, it generally introduces the primary research methods of predicting traffic risk. The paper also describes the datasets used in detail and conducts statistical analysis.

Based on previous theoretical research, the paper proposes a complete procedure of establishing traffic risk predicting model. Using the theory of Deep Learning, the paper builds up nodal adjacency matrices of multiple dimensions and extracts nodal feature, thus establishing a multi-view spatial and temporal graph convolutional network model. Then, it elaborates the computational formulas within the model and sets up evaluation indexes for model prediction, as well as describing the application scenarios of the model.

After establishing the overall process and evaluation indexes of the model, the paper trains and tests the model on given datasets. Comparison between the prediction result and the baseline result helps determine existing problems of the model and relevant reasons. Then, the paper optimizes the model via various Deep Learning methods and verifies that its result can meet the demands. The paper also visualizes the prediction result of the model, and conducts ablation experiments to evaluate the importance of different dimensions to the model, summarizing the entire research process and reflecting upon potential improvements and expectations eventually.  

## Model Performance
|             Model             | Train Loss | Train Accu | Test Loss  | Test Accu  |
| :---------------------------: | :--------: | :--------: | :--------: | :--------: |
| Historical Average (Contrast) |   0.9460   |   59.48%   |   0.9023   |   59.44%   |
|         **My Model**          | **0.1951** | **81.92%** | **0.4089** | **74.33%** |

## Notes

- Owing to the confidentiality agreement which is required by the data provider, I feel really sorry for not being authorized to provide any data for testing.
- The model performance is recorded authentically, which demonstrates the better performance of the model I have proposed in the paper.