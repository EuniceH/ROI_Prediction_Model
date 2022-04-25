# ROI Prediction Model

This software was developed by Nicklaus Danialy, Eunice Huang, Magdalena Švimberská, Saina Azimi and Thomas Brierton
  
It is an application that pulls historical stock data, and economic indicators for securities in the S&P500 index, then uses a variety of data analysis and machine learning methods in order to predict the future ROI of said security.

---

## Technologies

This project uses Jupyter Lab in addition to the following libraries and add ons:

* [streamlit](https://docs.streamlit.io/library/get-started?msclkid=d0e4542fc41111ec998ac26c21f5a09b) for creating the user interface.

* [pathlib](https://docs.python.org/3/library/pathlib.html) for the path functions to locate the csv files.

* [pandas](https://pandas.pydata.org/docs/) for working with dataframes.

* [matplotlib](https://docs.python.org/3/library/pathlib.html) for the data visualization.

* [holoviews](https://holoviews.org/user_guide/index.html?msclkid=1ed7efd6c2b911ecacd48fb5ba3288de) for more data visualization.

* [numpy](https://numpy.org/doc/) for certain numericalfunctions.

* [sklearn](https://scikit-learn.org/stable/user_guide.html) for the logistical regression.

* [tensorflow](https://www.tensorflow.org/api_docs/) for the neural network creation.

* [keras](https://keras.io/guides/?msclkid=f73e0a16c2b411ec879e189908dd6986) to interface with the neural network.

* [dotenv](https://openbase.com/js/dotenv/documentation?msclkid=2c19536ec2b911ec9c16c146d0de2ec6) for the environmental variables.

* [fbprophet](https://facebook.github.io/prophet/docs/quick_start.html?msclkid=9db86c8ec40b11ec893fb73ab463e691) for the environmental variables.

---

## Installation Guide

The following dependencies need to be installed in order to run the software. 

First install the Conda software according to your OS, then run the following commands in your terminal before running the app:

```
pip install jupyterlab

pip install python-dotenv

pip install sklearn

pip install tensorflow

pip install fbprophet

pip install hvplot

pip install streamlit

pip install pystan

pip install holoviews

pip install plotly

```

---

## Usage

The application requires API key from https://www.alphavantage.co/.
To use the application, users can simply download the files from this github pages.
To run, please type steamlit run app.py in the main directory:

```python
steamlit run stlit_main.py 
```

The home page of the streamlit application gives the user a flow chart of the applications logic, and a few fields to fill in with drop doens including "Sector", "Ticker", and "Quarter End Date":

![home](https://user-images.githubusercontent.com/96391748/164954792-8d9d0b3f-60a8-4350-9085-c6cabbd7f250.PNG)

After sector, ticker, and date are selected and the project buttion is clicked, multiple charts are generated and displayed on the page. However, they are initially hidden and the user can select the ones they would like displayed. 
The first of these is the linear regression method:

![regression_table](https://user-images.githubusercontent.com/96391748/164965032-78dc4025-5547-4b00-9c5e-783f1c7a2fc3.PNG)

![regression_plot](https://user-images.githubusercontent.com/96391748/164965091-43b76039-022e-46b9-bfcb-694158a21cd8.PNG)

The second field of data displayed is the table for the gradient boosted results:

![gradient](https://user-images.githubusercontent.com/96391748/164965135-29ded511-96b6-46af-b238-a9823a456cb0.PNG)

The binary model comparison summary - based on the classification reports, the accuracy scores are very similar between the two models; however, the precision and recall scores are mixed results. Based on the support counts of negative ROI, there is opportunity to apply oversampling techniques to both models.

Followed by the graphed results from the neural network prediction:

![neural_network](https://user-images.githubusercontent.com/96391748/164965222-10107c79-a4a5-46ee-aaef-c147f9eb61b5.PNG)

Next are the time series forcasting with Prophet:

![prophet](https://user-images.githubusercontent.com/96391748/164965279-1fab72cb-54e0-49ec-8b54-eaf89040aa58.PNG)

As well as a graphical representation of the results:

![line_graph](https://user-images.githubusercontent.com/96391748/164996950-5b48f9c3-d49f-40fd-8975-fc570e13ada0.PNG)

Finally, a daily percentage chart and inflation chart are generated for the users reference:

![daily_percentage](https://user-images.githubusercontent.com/96391748/164965343-37b9b1d9-1382-4644-a227-07058628cae9.PNG)

![inflation](https://user-images.githubusercontent.com/96391748/164965351-e6334321-ccbc-4da1-8de8-e75f990226f8.PNG)

---

## Roadmap
Here are some functionalities we would like to add to the application in the future: 
* Experiment with more models, different datasets and prediction goals, and further tune the model.
* Give the Streamlit side an API call function that allows the user to pull data.
* Allow users to build a portfolio in streamlit so that they can predict its ROI, and compare the results from the different Machine Learning models. 
* Work on better methods for displaying the results via overlay plots based off updated user input. 

---

## Contributors

* Nicklaus Danialy - nickdanialy@gmail.com 
* Eunice Huang - eunicehuang184@gmail.com
* Magdalena Švimberská - magdalena.svimberska@gmail.com
* Saina Azimi - azimi.sainaa@gmail.com
* Thomas Brierton - tbrierton@gmail.com

---

## License

Copyright (c) [2021] [Nicklaus Danialy, Eunice Huang, Magdalena Švimberská, Saina Azimi, Thomas Brierton]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
