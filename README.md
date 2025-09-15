🌍 Environmental Impact of Food Production Dashboard


Interactive data analysis of greenhouse gas emissions, land use, water use, and supply chain impacts of different foods.

📌 Project Overview

This project analyzes the environmental impacts of food production using the dataset from Our World in Data.
It follows the CRISP-DM methodology and addresses 7 key business questions with interactive visualizations.

The dashboard is built with Streamlit and Plotly, enabling decision-makers to explore product-specific sustainability metrics and policy scenarios.

📊 Business Questions Answered

* Which foods have the highest greenhouse gas emissions per kilogram?

* On average, which lifecycle stages drive emissions across foods?

* How do lifecycle emissions break down for the top 5 emitters?

* Which foods are both water-intensive and high-emitting?

* Which foods use the most land per kilogram?

* How closely are scarcity-weighted water use and emissions related?

* What is the potential impact of reducing Transport & Packaging emissions by 50%?

🛠️ Tech Stack

Python 3.9+

Streamlit (frontend dashboard)

Plotly Express (interactive visualizations)

Pandas & NumPy (data cleaning & analysis)

📂 Project Structure
├── app.py                 # Streamlit dashboard frontend
├── Food_Production.csv    # Dataset
├── requirements.txt       # Dependencies
├── README.md              # Project documentation


🚀 Getting Started
1️⃣ Clone the repo
git clone (https://github.com/iamjustkay/Environment_Impact_of_Food_Production_Analysis)
cd iamjustkay

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the dashboard
streamlit run app.py


The app will open in your browser at http://localhost:8501/.

🌐 Dashboard Preview

👉 View deployed Streamlit app
 (if hosted)

📈 Key Insights

Beef, lamb, chocolate, and coffee are the highest emitters per kg.

Farm stage & land use change dominate emissions across foods.

Packaging & transport cuts provide incremental but smaller benefits.

Water-scarce crops (nuts, rice, coffee) require region-specific strategies.

🔗 Links

📊 Dashboard Code: app.py

🌱 Data Source: Our World in Data – Environmental Impacts of Food Production

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

📜 License

This project is released under the MIT License.
