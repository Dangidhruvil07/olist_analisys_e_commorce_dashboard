# Olist E-Commerce Analytics

I built this project to practise working with real-world e-commerce data
and to understand the business questions that can be answered with it.
The project uses the Brazilian Olist e-commerce dataset and focuses on
orders, delivery, customers, sellers, product categories, payments,
geography, and reviews.

I started the analysis in Jupyter notebooks, where I explored the data
and worked through the calculations. I then brought the main results
into a Streamlit dashboard so they can be explored without opening each
notebook.

## What the dashboard covers

-   **Overall Analysis:** order and revenue trends, order status,
    payment methods, and customer behaviour.
-   **Orders & Delivery:** delivery duration and late deliveries
    compared with estimated dates.
-   **Seller Performance:** seller order volume, revenue, and delivery
    comparisons.
-   **Customer Analysis:** one-time and repeat customers, and order
    frequency.
-   **Product Category:** category revenue, order volume, and category
    comparisons.
-   **Revenue & Payments:** payment types, payment values, and
    installments.
-   **Geographical Analysis:** customer and seller distribution across
    Brazilian states.
-   **Reviews Analysis:** review scores and their relationship with
    delivery outcomes.
-   **Business Insights:** selected comparisons from the category and
    revenue analysis.

A purchase-date filter is available to explore a selected period.

## Dataset

The data comes from the **Brazilian E-Commerce Public Dataset by
Olist**, available on Kaggle:

-   [Olist dataset on
    Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The original CSV files are not included in this repository. Download the
dataset from Kaggle and place the nine CSV files in `data/raw/`, keeping
their original filenames:

-   `olist_customers_dataset.csv`
-   `olist_geolocation_dataset.csv`
-   `olist_order_items_dataset.csv`
-   `olist_order_payments_dataset.csv`
-   `olist_order_reviews_dataset.csv`
-   `olist_orders_dataset.csv`
-   `olist_products_dataset.csv`
-   `olist_sellers_dataset.csv`
-   `product_category_name_translation.csv`

The `data` folder should be beside the `dashboard` folder. The app
expects these files at `data/raw/`.

## Tools

-   Python
-   Pandas
-   Streamlit
-   Plotly
-   Jupyter Notebook

## Project structure

``` text
olist_analisys_e_commorce_dashboard/
├── data/
│   ├── raw/                  # Add the Kaggle CSV files here
│   └── processed/
├── notebooks/                # Data exploration and analysis
├── dashboard/
│   ├── app.py
│   └── assets/
│       └── header_panorama.jpg
├── requirements.txt
└── README.md
```

## Run locally

Open a terminal in the project root---the folder containing
`requirements.txt`---and run:

``` bash
python -m venv .venv
```

On Windows PowerShell, activate the environment:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

``` bash
pip install -r requirements.txt
```

Start the dashboard:

``` bash
python -m streamlit run dashboard/app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`.

## Notes on the analysis

-   Revenue based on order-item `price` is item revenue, not profit, and
    does not include freight.
-   Payment totals can differ from item revenue because they come from a
    separate payment table.
-   An order is treated as late when its actual delivery timestamp is
    later than its estimated delivery timestamp.
-   Customer type classification follows the grouping logic used in the
    analysis notebooks.
-   The results are descriptive. They show patterns in the available
    data and do not, by themselves, prove cause and effect.

I used AI assistance while building and styling the Streamlit interface
and while connecting parts of the notebook analysis to the dashboard.
The analysis work and calculations are documented in the notebooks,
which I use as the reference for the dashboard. I am still checking the
dashboard results against the source data, so I do not claim that every
displayed result has been independently verified.

This is a learning and portfolio project. It reflects my practice with
data analysis and dashboard development, and there is still room to
improve and validate it further.

## Current limitations

-   The Kaggle CSV files must be added locally and must also be
    available in the deployment environment.
-   The dashboard depends on the source data being present and correctly
    named.
-   This is a portfolio project, not a production reporting system.
## Live Demo

https://olist-analytics-e-commerce.streamlit.app


------------------------------------------------------------------------

Made while learning Python, Pandas, exploratory data analysis, and
dashboard development.
