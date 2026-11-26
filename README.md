# 🛒 E-Commerce Sales & Customer Intelligence

<p align="center">
  <strong>Turn retail transactions into actionable business insights.</strong><br/>
  An end-to-end analytics and machine learning project built with Python, Streamlit, SQL and interactive visualizations.
</p>

<p align="center">
  <a href="https://e-commerce-sales-customer-intelligence.onrender.com"><img src="https://img.shields.io/badge/Live%20Dashboard-Visit%20App-16745E?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Dashboard"/></a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12"/>
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Machine Learning"/>
  <img src="https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
</p>

---

## 🌐 Live Application

**[Open the E-Commerce Sales & Customer Intelligence Dashboard](https://e-commerce-sales-customer-intelligence.onrender.com)**

The application is deployed as a Docker-based Streamlit web service on Render. On the free hosting tier, the service may sleep after a period of inactivity, so the first visit can take a little longer while it starts.

## 📌 Project Overview

E-commerce transaction data contains valuable information about sales performance, customer purchasing patterns, product demand and business growth. This project transforms retail transaction records into an interactive business intelligence dashboard.

The application combines data preparation, exploratory analysis and machine learning techniques to help explore questions such as:

- How are sales changing over time?
- Which products and countries contribute most to revenue?
- Which customers generate the highest value?
- Which customers may be at risk of becoming inactive?
- What sales trends might be expected in the future?
- Which products are frequently purchased together?

## 🎯 Project Objectives

- Clean and prepare retail transaction data for analysis.
- Measure sales performance and identify important trends.
- Understand customer purchasing behaviour using RFM analysis.
- Explore customer churn risk and sales forecasting.
- Identify product associations using market basket analysis.
- Present analytical results through an interactive dashboard.

## ✨ Dashboard Modules

The Streamlit application is organized into six main modules:

| Module | What it covers |
|---|---|
| **1. Dashboard Overview** | A consolidated view of important business and sales indicators. |
| **2. Sales Analysis** | Sales trends and transaction performance over time. |
| **3. Customer Intelligence** | Customer behaviour, value analysis and RFM segmentation. |
| **4. Product Analysis** | Product-level performance and sales contribution. |
| **5. Forecast & Churn** | Forecasting future sales and examining customer churn risk. |
| **6. Market Basket Analysis** | Frequent itemsets and association rules for products purchased together. |

## 🧰 Technology Stack

| Technology | Role in the project |
|---|---|
| **Python 3.12** | Main programming language |
| **Pandas** | Data cleaning, manipulation and analysis |
| **NumPy** | Numerical operations |
| **Plotly** | Interactive charts and visualizations |
| **Matplotlib & Seaborn** | Data visualization |
| **Scikit-learn** | Machine learning workflows |
| **MLxtend** | Frequent itemsets and association-rule analysis |
| **Streamlit** | Interactive web dashboard |
| **MySQL / SQLAlchemy** | Relational database workflow and SQL integration |
| **Docker** | Containerization |
| **Render** | Cloud deployment |
| **Git & GitHub** | Version control and project hosting |

## 📂 Repository Structure

```text
E-Commerce-Sales-Customer-Intelligence/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
│
├── Data/
│   ├── Raw/
│   │   └── Online Retail.xlsx
│   └── processed/
│       ├── cleaned_sales.csv
│       └── cancellations_returns_review.csv
│
├── src/
│   ├── data_cleaning.py
│   ├── load_mysql.py
│   ├── sales_analysis.py
│   ├── rfm_segmentation.py
│   ├── churn_prediction.py
│   ├── sales_forecasting.py
│   ├── recommendations.py
│   └── market_basket.py
│
└── outputs/
    ├── charts/
    ├── churn_risk.csv
    ├── customer_analysis.csv
    ├── country_sales.csv
    ├── frequent_itemsets.csv
    ├── market_basket_rules.csv
    ├── monthly_sales.csv
    ├── rfm_segments.csv
    ├── sales_forecast.csv
    └── top_products.csv
```

## 📊 Dataset

This project uses the **Online Retail** dataset, which contains transactional records from a UK-based online retail business.

- **Raw dataset:** `Data/Raw/Online Retail.xlsx`
- **Processed dataset:** `Data/processed/cleaned_sales.csv`
- **Data type:** Invoice-level retail transactions and product purchases.
- **Currency displayed in the dashboard:** Pound sterling (£), as formatted by the application.

The transaction data includes fields such as invoice number, product/stock code, product description, quantity, invoice date, unit price, customer ID and country.

**Dataset source:** [UCI Machine Learning Repository – Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

## 🔄 Project Workflow

```text
Raw Online Retail Dataset
          │
          ▼
   Data Cleaning & Preparation
          │
          ▼
  Processed Transaction Dataset
          │
          ▼
   Exploratory Data Analysis
          │
          ├──────── Sales Analysis
          ├──────── Customer / RFM Analysis
          ├──────── Product Analysis
          ├──────── Churn Risk Analysis
          ├──────── Sales Forecasting
          └──────── Market Basket Analysis
                         │
                         ▼
              Streamlit Dashboard
                         │
                         ▼
                Docker Container
                         │
                         ▼
                 Render Deployment
```

## ⚙️ Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Ruchika-Natiye/E-Commerce-Sales-Customer-Intelligence.git
cd E-Commerce-Sales-Customer-Intelligence
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the Streamlit application

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, normally:

```text
http://localhost:8501
```

### 5. Run with Docker (optional)

Build the image:

```bash
docker build -t ecommerce-dashboard .
```

Run the container:

```bash
docker run -p 8501:8501 ecommerce-dashboard
```

Then open `http://localhost:8501`.

## 🧪 Machine Learning & Analytics

The project includes analytical workflows for:

- **RFM segmentation:** groups customers using Recency, Frequency and Monetary value.
- **Churn risk analysis:** estimates which customers may be at risk of becoming inactive.
- **Sales forecasting:** generates a forecast from historical sales data.
- **Market basket analysis:** discovers product combinations through frequent itemsets and association rules.
- **Product and customer analysis:** summarizes purchasing patterns and contribution to sales.

These outputs are intended to support exploration and business decision-making. Forecasts and churn scores are analytical estimates, not guarantees of future behaviour.

## 🖼️ Screenshots

Dashboard screenshots can be added here as the project evolves. To display an image stored in the repository, add it under `outputs/charts/` or a dedicated `screenshots/` folder and embed it like this:

```markdown
![Dashboard Overview](screenshots/dashboard-overview.png)
```

## ⚠️ Data Path Note

The repository stores the processed dataset under `Data/processed/` (capital **D**). Linux-based hosts such as Render use case-sensitive paths. Ensure the `DATA_PATH` setting in `app.py` uses the exact repository path:

```python
DATA_PATH = ROOT / "Data" / "processed" / "cleaned_sales.csv"
```

This is important because a lowercase `data` path may work on some Windows setups but fail on Linux.

## 🚀 Deployment

The project includes a `Dockerfile` and is deployed on Render.

- **Live dashboard:** https://e-commerce-sales-customer-intelligence.onrender.com
- **Container port:** 8501 (the Docker command also supports Render's `PORT` environment variable).
- **Source repository:** https://github.com/Ruchika-Natiye/E-Commerce-Sales-Customer-Intelligence

## 🔮 Possible Future Improvements

- Add more dashboard screenshots and a project walkthrough.
- Improve caching and memory efficiency for low-memory hosting environments.
- Add automated data validation and model evaluation reports.
- Add tests for data processing and analytical modules.
- Add scheduled data refresh and model monitoring.

## 👩‍💻 Author

**Ruchika Natiye**

- GitHub: [@Ruchika-Natiye](https://github.com/Ruchika-Natiye)
- Project: [E-Commerce Sales & Customer Intelligence](https://github.com/Ruchika-Natiye/E-Commerce-Sales-Customer-Intelligence)

---

<p align="center">
  If you find this project useful, consider giving the repository a ⭐.
  <br/>
  <strong>Built with Python, analytics and a focus on turning data into decisions.</strong>
</p>
