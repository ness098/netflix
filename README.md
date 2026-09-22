# 🎬 Netflix Data Analysis
### *Exploratory Data Analysis and Interactive Dashboard*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557c.svg)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-4c72b0.svg)](https://seaborn.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626.svg)](https://jupyter.org/)

---

## Project Overview
Over the past decade, Netflix has fundamentally disrupted the global entertainment landscape, transitioning from a domestic DVD rental service into an international media powerhouse with over 200 million paid memberships spanning more than 190 countries. 

This project delivers a comprehensive, college-submission-ready Exploratory Data Analysis (EDA) and interactive dashboard that explores the composition, growth, geographical reach, genre dynamics, maturity ratings, and runtime characteristics of Netflix's content catalogue.

---

## Problem Statement
Streaming media markets are hyper-competitive. Content platforms must continuously optimize their licensing expenditures and original production strategies to maximize subscriber retention and acquisition. However, raw streaming catalogue metadata often arrives semi-structured with multi-valued attributes (e.g. multi-genre classifications, international co-productions, multi-director credits), irregular date strings, and missing attributes.

The core challenge is:
1. Cleaning, standardizing, and parsing raw catalogue records into structured analytical entities.
2. Deriving empirical insights regarding content formats, regional contributions, and temporal trends.
3. Building an accessible, interactive tool enabling non-technical stakeholders to explore this data seamlessly.

---

## Objectives
- **Data Preprocessing & Cleaning:** Handle missing values, parse multi-value comma-separated attributes (genres, countries, directors), standardize temporal fields, and extract numerical runtime components.
- **Exploratory Data Analysis:** Conduct quantitative investigations to evaluate content distributions, release trends, and audience demographics.
- **Statistical Visualization:** Generate publication-standard figures utilizing Matplotlib and Seaborn adhering to a cohesive Netflix-inspired visual aesthetic.
- **Interactive Web Dashboard:** Build a high-performance Streamlit dashboard featuring multi-dimensional filtering, dynamic KPI cards, and instant data export capabilities.
- **Academic Documentation:** Provide a complete 23-section Jupyter notebook and interview/viva preparation material.

---

## Dataset
The project analyzes the authentic public Netflix titles dataset (originating from Flixable and archived via TidyTuesday).

- **Total Records:** 7,787 titles
- **Attributes:** 12 columns
- **File Location:** `data/netflix_titles.csv`

### Feature Schema:
| Column | Type | Description |
| :--- | :--- | :--- |
| `show_id` | String | Unique record identifier (e.g., `s1`, `s2`) |
| `type` | String | Format classification (`Movie` or `TV Show`) |
| `title` | String | Title of the film or television series |
| `director` | String | Director name(s) (comma-separated if multiple) |
| `cast` | String | Featured cast members (comma-separated) |
| `country` | String | Producing country / co-producing territories |
| `date_added` | String | Date ingested onto the Netflix streaming platform |
| `release_year`| Integer| Original theatrical or broadcast release year |
| `rating` | String | Content maturity rating (e.g., `TV-MA`, `TV-14`, `R`) |
| `duration` | String | Runtime (minutes for movies, seasons for TV shows) |
| `listed_in` | String | Assigned categories and genres |
| `description`| String | Synopsis / plot premise |

---

## Data Cleaning
Rigorous data preprocessing steps were implemented using Pandas:

1. **Duplicate Verification:** Checked for duplicated rows and verified uniqueness of `show_id` (0 duplicates identified; 7,787 unique IDs).
2. **Missing Value Treatment:**
   - `director`: 2,389 missing values (30.7%) imputed with `'Unknown Director'` (common for unscripted/reality shows).
   - `cast`: 718 missing values (9.2%) imputed with `'Unknown Cast'`.
   - `country`: 507 missing values (6.5%) imputed with `'Unknown Country'`.
   - `rating`: 7 missing values (0.1%) imputed with `'Unknown'`.
   - `date_added`: 10 missing values (0.1%) handled cleanly with `errors='coerce'`.
3. **Date Standardization:** Stripped irregular leading/trailing whitespaces and parsed `date_added` to Pandas datetime format. Extracted `year_added` and `month_added`.
4. **Encoding Artifact Sanitization:** Sanitized Latin-1 corrupted character patterns (e.g. converting `Ral Campos` to `Raúl Campos`).
5. **Duration Parsing:** Split composite duration strings into `duration_int` (numeric value) and `duration_unit` (`min` vs. `Season`/`Seasons`).
6. **Multi-Valued Field Exploding:** Split comma-separated strings in `listed_in`, `country`, and `director` into discrete Python lists to prevent comma-separated grouping biases during aggregation.

---

## Exploratory Data Analysis
Comprehensive statistical analyses were conducted across all dimensions of the library. All metrics are calculated directly from verified data.

### Key Questions & Answers:

1. **How many total titles are present?**
   - **7,787 titles** are present in the catalogue.

2. **How many Movies vs TV Shows?**
   - **5,377 Movies** and **2,410 TV Shows**.

3. **What percentage of the catalogue is Movies vs TV Shows?**
   - **69.05% Movies** and **30.95% TV Shows** (approximately a 7:3 ratio).

4. **Which genres are most common across the entire catalogue?**
   - `International Movies` (2,437)
   - `Dramas` (2,106)
   - `Comedies` (1,471)
   - `International TV Shows` (1,199)
   - `Documentaries` (786)

5. **Which countries contribute the most titles?**
   - **United States**: 3,297 titles
   - **India**: 990 titles
   - **United Kingdom**: 723 titles
   - **Canada**: 412 titles
   - **France**: 349 titles

6. **Which years have the highest number of releases?**
   - **2018**: 1,121 titles
   - **2017**: 1,012 titles
   - **2019**: 996 titles
   - **2016**: 882 titles
   - **2020**: 868 titles

7. **How has Netflix content changed over the years?**
   - Before 2015, Netflix primarily licensed existing theatrical movies from the US. From 2016 onward, Netflix initiated aggressive international expansion, commissioning localized productions in India, South Korea, Latin America, and Europe while dramatically growing episodic TV series.

8. **What are the most common content ratings?**
   - **TV-MA**: 2,863 titles (36.8%)
   - **TV-14**: 1,931 titles (24.8%)
   - **TV-PG**: 806 titles (10.4%)
   - **R**: 665 titles (8.5%)
   - **PG-13**: 386 titles (5.0%)

9. **What is the distribution of movie durations?**
   - Follows a normal distribution centered around an **average runtime of 99.31 minutes** (median: 98 minutes; standard deviation: 28.5 minutes). Runtimes range from 3 minutes (short animations) to 312 minutes (*Black Mirror: Bandersnatch*).

10. **Which directors appear most frequently?**
    - **Jan Suter**: 21 titles
    - **Raúl Campos**: 19 titles
    - **Marcus Raboy**: 16 titles
    - **Jay Karas**: 15 titles
    - **Cathy Garcia-Molina**: 13 titles
    - **Martin Scorsese**: 12 titles
    - **Youssef Chahine**: 12 titles

11. **Which release years contain the most content?**
    - The five-year window between **2016 and 2020** accounts for over 62% of all catalogue entries, peaking in **2018** (1,121 releases).

12. **Which genres are common among Movies?**
    - `International Movies` (2,437), `Dramas` (2,106), `Comedies` (1,471), `Documentaries` (786), `Action & Adventure` (721).

13. **Which genres are common among TV Shows?**
    - `International TV Shows` (1,199), `TV Dramas` (704), `TV Comedies` (525), `Crime TV Shows` (427), `Kids' TV` (414).

14. **How many titles were added to Netflix by year?**
    - 2008: 2 | 2009: 2 | 2010: 1 | 2011: 13 | 2012: 3 | 2013: 11 | 2014: 25 | 2015: 88 | 2016: 443 | 2017: 1,225 | 2018: 1,685 | **2019: 2,153 (Peak)** | 2020: 2,009 | 2021: 117.

15. **Which countries have the largest catalogue representation?**
    - United States (42.3%), India (12.7%), United Kingdom (9.3%), Canada (5.3%), France (4.5%), Japan (3.7%), Spain (2.8%), South Korea (2.7%).

---

## Visualizations
All charts are pre-generated at 300 DPI using a custom dark Netflix-inspired theme with restrained red highlights. Stored in `charts/`:

- `charts/content_type.png`: Direct comparison of Movies vs TV Shows with count and percentage annotations.
- `charts/type_distribution_donut.png`: Donut chart illustrating catalogue share breakdown.
- `charts/top_genres.png`: Horizontal bar chart ranking the top 10 catalogue genres.
- `charts/yearly_trend.png`: Multi-line comparison of titles added to Netflix vs original production release years.
- `charts/rating_distribution.png`: Bar chart of the 10 most common content maturity ratings.
- `charts/country_distribution.png`: Horizontal bar chart of the top 10 content-producing nations.
- `charts/movies_duration.png`: Histogram with KDE curve and mean/median reference lines for movie runtimes.
- `charts/release_year_distribution.png`: Area chart tracing content production volume from 1990 to 2021 with peak callout.
- `charts/top_directors.png`: Ranking of the top 10 most prolific directors.
- `charts/genre_comparison.png`: Dual-panel comparative analysis of top Movie genres vs TV Show genres.

---

## Dashboard
The interactive Streamlit dashboard (`app.py`) provides an intuitive, high-performance interface:

- **Theme:** Dark Netflix aesthetic (`#141414` background, `#1F1F1F` cards, `#E50914` accents).
- **Dynamic KPI Cards:** Displays Live Counts for Total Titles, Movies, TV Shows, Countries Represented, Unique Genres, and Latest Production Year.
- **Multidimensional Sidebar Filters:**
  - Content Type (Movie / TV Show)
  - Release Year Slider (1925 – 2021)
  - Producing Country Selector (with "All" shortcut)
  - Content Maturity Rating Selector (with "All" shortcut)
  - Genre Selector (with "All" shortcut)
  - **Reset Filters Button** to restore default views instantly.
- **8 Organized Sections:**
  1. Overview (KPIs & Format Breakdown)
  2. Genre Analysis (Top 10 Genres & Format Comparison)
  3. Geographic Distribution (Top Nations & Share Table)
  4. Temporal Trends (Addition Timeline & Release Distribution)
  5. Maturity Ratings (Distribution & Format Cross-tabulation)
  6. Movie Analysis (Duration Histogram, Director Rankings, Runtime Stats)
  7. Interactive Data Explorer (Global Search Bar & CSV Download)
  8. Key Analytical Insights (Dynamic Bulletins)

---

## Technologies Used
- **Python 3.9+**: Core programming language.
- **Pandas**: High-performance data manipulation, filtering, string parsing, and aggregation.
- **NumPy**: Vectorized numerical calculations and statistical summaries.
- **Matplotlib**: Low-level chart construction, layout configuration, and figure export.
- **Seaborn**: Statistical data visualizations, histograms, and styled palettes.
- **Streamlit**: Web application framework for interactive dashboarding.
- **Jupyter Notebook**: Reproducible computational notebook for EDA workflows.
- **OpenPyXL**: Spreadsheet format reading and writing compatibility.

---

## Project Structure
```
Netflix-Data-Analysis/
│
├── data/
│   └── netflix_titles.csv               # Cleaned real Netflix catalogue dataset (7,787 rows)
│
├── notebooks/
│   └── Netflix_Data_Analysis.ipynb      # Complete 23-section executed analytical notebook
│
├── charts/                              # Pre-generated 300-DPI publication charts
│   ├── content_type.png
│   ├── type_distribution_donut.png
│   ├── top_genres.png
│   ├── yearly_trend.png
│   ├── rating_distribution.png
│   ├── country_distribution.png
│   ├── movies_duration.png
│   ├── release_year_distribution.png
│   ├── top_directors.png
│   └── genre_comparison.png
│
├── scripts/                             # Utility & pipeline generation scripts
│   ├── generate_charts.py               # Generates and saves all Matplotlib/Seaborn figures
│   └── build_notebook.py                # Constructs the 23-section Jupyter notebook
│
├── app.py                               # Interactive Streamlit dashboard application
├── requirements.txt                     # Project dependencies and minimum versions
├── README.md                            # Comprehensive project documentation & Viva guide
└── .gitignore                           # Git ignore rules for Python, Jupyter, and Streamlit
```

---

## Installation
Clone or navigate to the repository directory, create a virtual environment, and install dependencies:

```bash
# Optional: Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## How to Run

### 1. Launch the Streamlit Dashboard:
```bash
streamlit run app.py
```
Open your web browser at `http://localhost:8501`.

### 2. View or Execute the Jupyter Notebook:
```bash
jupyter notebook notebooks/Netflix_Data_Analysis.ipynb
```
Or launch JupyterLab:
```bash
jupyter lab
```

### 3. Regenerate Charts (Optional):
```bash
python scripts/generate_charts.py
```

---

## Key Insights
*Empirically computed from the verified dataset:*
1. **Catalog Bias Toward Feature Films:** Movies represent **69.1%** (5,377 titles) of the entire library, while TV Shows comprise **30.9%** (2,410 titles).
2. **Internationalization is Paramount:** Over **31.3%** of all movies are classified under `International Movies`, reflecting Netflix's localization strategy for non-English markets.
3. **The United States and India Lead Production:** The US accounts for 3,297 titles (42.3%), while India is the second largest contributor with 990 titles (12.7%), primarily driven by Bollywood films.
4. **2019 Ingestion High-Water Mark:** Ingestions peaked in **2019 with 2,153 additions**, followed by a plateau in 2020 (2,009 titles) as production schedules were impacted globally.
5. **Mature Demographics Dominate:** Over **61.6%** of the catalogue carries mature ratings (`TV-MA` with 2,863 titles and `TV-14` with 1,931 titles), reinforcing Netflix's brand identity as an adult-focused prestige entertainment destination.
6. **Consistent Movie Durations:** Feature films tightly cluster around an average runtime of **99.3 minutes**, demonstrating strict adherence to traditional theatrical runtime standards.

---

## Future Scope
This project establishes a clean foundation for advanced data science and machine learning enhancements:
- **Recommendation Systems:** Implementing collaborative filtering (matrix factorization) and content-based recommendation systems using TF-IDF / Cosine Similarity on title synopses.
- **Natural Language Processing (NLP):** Performing sentiment analysis and Latent Dirichlet Allocation (LDA) topic modeling on descriptions to reveal hidden thematic clusters.
- **External Metric Integration:** Connecting with the OMDb / TMDB API to enrich records with user review scores (IMDb, Rotten Tomatoes) and box-office financials.
- **Time-Series Forecasting:** Deploying ARIMA or Prophet models to project catalog growth and format shifts over future quarters.
- **User Behavior Analytics:** Integrating anonymized clickstream and completion-rate data to evaluate watch-time decay curves.

*(Note: The above items represent planned future enhancements and are not part of this core exploratory release).*

---

## How to Explain This Project in Viva

When presenting this project during a college viva or technical interview, use these structured answers:

### Q1. Why did you choose this project?
> *"The streaming entertainment sector is driven by data-informed decisions regarding multi-million dollar licensing and original production investments. Analyzing Netflix's catalogue allows us to explore how a major platform balances movies versus episodic TV shows, caters to global markets, and structures content for specific age demographics using standard Python data science tools."*

### Q2. What dataset did you use and where did it come from?
> *"We utilized the real public Netflix catalogue dataset collected from Flixable and archived via TidyTuesday. It comprises 7,787 rows and 12 features spanning titles from 1925 through 2021, detailing cast, directors, release years, platform ingestion dates, duration, countries, ratings, and genre tags."*

### Q3. Why did you select Pandas over SQL or Excel for data cleaning?
> *"While SQL is excellent for relational joins and Excel is good for quick manual inspections, Pandas is significantly superior for complex semi-structured data manipulation. In this dataset, fields like `country`, `listed_in`, and `director` contain comma-separated multiple values. Pandas allows vectorized string operations, list conversions, and the `.explode()` method to normalize these multi-valued features without complex SQL cross-joins."*

### Q4. What is Exploratory Data Analysis (EDA) and why is it essential?
> *"EDA is the foundational process in data science where statistical summaries and visual representations are used to uncover patterns, detect anomalies, test hypotheses, and verify assumptions before any modeling or business decisions occur. In this project, EDA exposed crucial patterns like the 69:31 Movie-to-TV split and the 2019 content ingestion peak."*

### Q5. What major data cleaning challenges did you encounter and resolve?
> *"First, handling high missingness in `director` (30.7%) and `country` (6.5%) by imputing descriptive labels rather than dropping rows, which would have discarded over 2,000 valid titles. Second, parsing inconsistent date strings with trailing spaces into proper datetimes. Third, separating duration strings into numeric quantities and units to enable mathematical calculations on movie runtimes."*

### Q6. What were the most surprising or significant findings from the data?
> *"Two major insights stood out: First, the heavy concentration of TV-MA content (over 36%), proving Netflix is fundamentally an adult-oriented service rather than a family cartoon hub. Second, while the US represents the largest producer, India is a very strong second with nearly 1,000 titles, highlighting the critical importance of the South Asian market to Netflix's global subscriber growth."*

### Q7. Why did you choose Streamlit for the dashboard?
> *"Streamlit allows pure Python code to be converted directly into an interactive, reactive web dashboard without requiring a complex separate frontend stack (like React or HTML/JS). It provides native caching (`@st.cache_data`) for instantaneous filter responsiveness, reactive KPI components, and clean browser-based CSV downloads."*

### Q8. What are the limitations of this dataset and analysis?
> *"This dataset represents a catalogue snapshot of what was available on the platform up to 2021; it does not include viewership metrics (such as hours viewed or completion rates) or user ratings (like IMDb scores). As a result, our analysis reflects Netflix's catalog supply rather than consumer demand."*

### Q9. What would you build next if given more time?
> *"I would build a content-based recommendation engine using TF-IDF vectorization and Cosine Similarity on the title descriptions, enabling users to enter a favorite movie and receive top-5 recommendations. I would also integrate the TMDB API to pull real-time viewer ratings and budget data."*

---

## Author & Acknowledgements
- **Author:** Data Analytics Project
- **Dataset:** Public Netflix Titles Catalog (Flixable / TidyTuesday)
- **Frameworks:** Python, Pandas, Matplotlib, Seaborn, Streamlit, Jupyter
