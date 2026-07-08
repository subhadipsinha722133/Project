# 🛍️ Customer Segmentation App

A Streamlit web application for customer segmentation using K-Means clustering algorithm. This app helps businesses identify distinct customer groups based on their demographic and behavioral characteristics.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

## 📊 Features

- **Data Visualization**: Interactive exploration of customer data
- **Elbow Method**: Automated determination of optimal cluster count
- **K-Means Clustering**: Customer segmentation based on income and spending patterns
- **Cluster Analysis**: Detailed statistics for each customer segment
- **3D Visualization**: Advanced clustering with multiple dimensions
- **Data Export**: Download segmentation results as CSV

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/customer-segmentation-app.git
   cd customer-segmentation-app
Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies
```
```bash
pip install -r requirements.txt
Run the application
```
```bash
streamlit run customer_segmentation.py
Open your browser and navigate to http://localhost:8501
```
## 📁 Project Structure
text
customer-segmentation-app/
│
├── customer_segmentation.py  # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
└── Mall_Customers.csv       # Sample dataset (add your own)

## 📈 Usage
1. Data Input
Upload your own CSV file with customer data

Use the sample data structure if you don't have your own data

Required columns: CustomerID, Gender, Age, Annual Income (k$), Spending Score (1-100)

2. Parameter Tuning
Adjust the number of clusters using the slider

Set the random state for reproducible results

Customize visualization settings

3. Analysis
View the elbow method graph to determine optimal clusters

Explore customer segments in 2D and 3D visualizations

Analyze cluster statistics and demographics

4. Export Results
Download the segmented data as a CSV file

Use the results for targeted marketing campaigns

## 🎯 Sample Data Format
Your CSV file should have the following structure:

CustomerID	Gender	Age	Annual Income (k$)	Spending Score (1-100)
1	Male	19	15	39
2	Male	21	15	81
3	Female	20	16	6

## 🔧 Customization
Adding New Features
You can modify the app to include additional clustering algorithms or features:

python
# Example: Adding DBSCAN clustering
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.5, min_samples=5)
customer_data['DBSCAN_Cluster'] = dbscan.fit_predict(X_scaled)
Styling
Customize the app appearance by modifying the CSS in the st.markdown() section:


python
```bash
st.markdown("""
<style>
    .custom-header {
        color: #FF4B4B;
        font-size: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)
```
## 🤝 Contributing
We welcome contributions! Please feel free to submit a Pull Request.

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
Dataset inspired by: Mall_Customers.csv

Built with Streamlit

Clustering with Scikit-learn

## 📞 Support
If you have any questions or issues, please open an issue on GitHub or contact us at sinhasubhadip34@gmail.com.

⭐ If you find this project helpful, please give it a star on GitHub!

text

## Additional Setup Instructions

1. Create a `.gitignore` file to exclude unnecessary files:

```gitignore
# .gitignore
venv/
.env
*.pyc
__pycache__/
.DS_Store
*.log
For deployment to Streamlit Cloud, create a setup.sh file:

bash
#!/bin/bash
# setup.sh
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
Create a Procfile for deployment:

text
web: sh setup.sh && streamlit run customer_segmentation.py
Deployment to Streamlit Cloud
Push your code to GitHub

Go to share.streamlit.io

Connect your GitHub account

Select your repository and main file path

Deploy!