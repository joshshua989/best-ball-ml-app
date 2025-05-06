---

# 🏈 Best Ball ML App

---

## 🧠 What the App Does

**Best Ball ML App** is a fantasy football analytics tool that uses machine learning to predict quarterback (QB) performance for Best Ball fantasy formats. The application scrapes QB statistics from online sources, processes the data, and employs machine learning models—specifically, `RandomForestRegressor` and `RandomForestClassifier` from scikit-learn—to generate performance predictions. These predictions are then displayed through an interactive Streamlit dashboard.



## 🗂️ Key Files

- **`app.py`**: The main script that initializes and runs the Streamlit web application.
- **`load_stats.py`**: Handles data scraping and preprocessing using `pandas.read_html` to extract QB statistics from HTML tables and prepares the data for model training and prediction.



## 🔍 Features

- 🧠 Predicts QB performance using `RandomForestRegressor` and `RandomForestClassifier`.
- 📊 Scrapes and processes live QB stats from the web.
- 📈 Displays data and predictions in an interactive Streamlit dashboard.
- ⚙️ Simple setup and execution in a virtual environment.



## ⚙️ How It Works

- **Data Collection**: Scrapes QB statistics from online sources using `pandas.read_html`.
- **Data Preprocessing**: Cleans and structures the data for modeling.
- **Model Training**: Trains `RandomForestRegressor` and `RandomForestClassifier` models on the processed data to predict QB performance metrics.
- **Prediction Display**: Predicted performance metrics are presented in an interactive dashboard built with Streamlit.

---

## 🧪 Dependencies

Ensure the following Python packages are installed in your environment:

- `streamlit`
- `pandas`
- `scikit-learn`
- `lxml`

Install them via pip:

```bash
pip install streamlit pandas scikit-learn lxml
```



## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/joshshua989/best-ball-ml-app.git
cd best-ball-ml-app
```



### 2. Running the App

- Activate your virtual environment (if applicable).
- Navigate to the project directory.
- Run the Streamlit app:

```bash
streamlit run app.py
```

- This will launch the application in your default web browser at http://localhost:8501. Network URL: http://10.0.0.54:8501 for devices on the same wifi network.

---

## 🛠️ Roadmap / TODO

- Add support for other positions (RB, WR, TE)
- Export predictions to CSV
- Integrate live game data via API
- Deploy app via Streamlit Cloud or Heroku



## 🤝 Contributing

- Pull requests are welcome! If you have suggestions or feature requests, feel free to open an issue or fork the repo and submit a PR.



## 📄 License

- This project is licensed under the MIT License.



📬 Contact
Created by @joshshua989 — for questions, feedback, or collaboration, reach out via GitHub or email.
