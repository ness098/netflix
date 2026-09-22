"""
Netflix Data Analysis - Interactive Dashboard
Built with Streamlit, Pandas, Matplotlib, and Seaborn.
Features a Netflix-inspired dark UI with restrained red accents.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# Page Configuration & Netflix Dark Theme Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Netflix Data Analysis | EDA & Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished dark Netflix aesthetic
st.markdown("""
<style>
    .main { background-color: #141414; color: #E5E5E5; }
    .stApp { background-color: #141414; }
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h1 { font-size: 2.15rem !important; margin-bottom: 0.25rem !important; }
    h2 { font-size: 1.55rem !important; margin-top: 0.4rem !important; margin-bottom: 0.35rem !important; }
    h3 { font-size: 1.2rem !important; margin-top: 0.35rem !important; margin-bottom: 0.3rem !important; }

    .metric-card {
        background: #1F1F1F;
        border: 1px solid #2B2B2B;
        border-radius: 10px;
        padding: 13px 10px;
        min-height: 108px;
        text-align: center;
        box-sizing: border-box;
        overflow: hidden;
    }
    .metric-title {
        color: #999999;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
        white-space: nowrap;
    }
    .metric-value {
        color: #FFFFFF;
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.15;
        margin: 0;
    }
    .metric-subtitle {
        color: #E50914;
        font-size: 0.68rem;
        margin-top: 4px;
        font-weight: 500;
    }

    .section-gap { height: 0.35rem; }
    .insight-box {
        background: #1A1A1A;
        border-left: 3px solid #E50914;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        margin-bottom: 8px;
        color: #E5E5E5;
        font-size: 0.88rem;
    }
    [data-testid="stSidebar"] {
        background-color: #181818;
        border-right: 1px solid #282828;
    }
    [data-testid="stSidebar"] h2 { color: #E50914 !important; letter-spacing: 0.05em; }
    div[data-testid="stVerticalBlock"] > div { max-width: 100%; }
    .stPlotlyChart, [data-testid="stImage"], .element-container { max-width: 100%; }
    [data-testid="stDataFrame"] { max-width: 100%; }

    @media (max-width: 900px) {
        h1 { font-size: 1.75rem !important; }
        .metric-value { font-size: 1.3rem; }
        .metric-card { min-height: 96px; padding: 10px 7px; }
    }
</style>
""", unsafe_allow_html=True)

# Visual theme constants
NETFLIX_RED = '#E50914'
NETFLIX_DARK_RED = '#B81D24'
ACCENT_GRAY = '#606060'
LIGHT_GRAY = '#E5E5E5'
BG_COLOR = '#141414'
CARD_COLOR = '#1F1F1F'

def set_plot_style():
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = BG_COLOR
    plt.rcParams['axes.facecolor'] = CARD_COLOR
    plt.rcParams['text.color'] = LIGHT_GRAY
    plt.rcParams['axes.labelcolor'] = LIGHT_GRAY
    plt.rcParams['xtick.color'] = LIGHT_GRAY
    plt.rcParams['ytick.color'] = LIGHT_GRAY
    plt.rcParams['grid.color'] = '#333333'

set_plot_style()

# ---------------------------------------------------------
# Data Ingestion & Robust Preprocessing
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_titles.csv", encoding="utf-8")
    
    # Drop full duplicates if any
    df = df.drop_duplicates()
    
    # Sanitize corrupted characters in director/cast
    for col in ['director', 'cast', 'title']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('Ral', 'Raúl')
            df[col] = df[col].replace('nan', np.nan)
            
    # Datetime conversion & year/month extraction
    df['date_added_clean'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')
    df['year_added'] = df['date_added_clean'].dt.year
    df['month_added'] = df['date_added_clean'].dt.month_name()
    
    # Numeric release year
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    
    # Duration parsing (numeric value & unit)
    df['duration_num'] = pd.to_numeric(df['duration'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
    df['duration_unit'] = df['duration'].astype(str).str.extract(r'([A-Za-z]+)')[0]
    
    # Missing values imputation for presentation
    df['country_imputed'] = df['country'].fillna('Unknown')
    df['director_imputed'] = df['director'].fillna('Unknown Director')
    df['rating_imputed'] = df['rating'].fillna('Unknown')
    
    # Unpack helper columns
    df['genre_list'] = df['listed_in'].fillna('').apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])
    df['country_list'] = df['country'].fillna('').apply(lambda x: [c.strip() for c in x.split(',') if c.strip()])
    df['primary_genre'] = df['genre_list'].apply(lambda x: x[0] if len(x) > 0 else 'Unknown')
    df['primary_country'] = df['country_list'].apply(lambda x: x[0] if len(x) > 0 else 'Unknown')
    
    return df

df_raw = load_data()

# ---------------------------------------------------------
# Sidebar Filter Controls
# ---------------------------------------------------------
st.sidebar.markdown("## NETFLIX")
st.sidebar.markdown("### 🎛️ Dashboard Filters")

# Reset Filters mechanism
if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    for key in ["filter_types", "filter_years", "filter_countries", "filter_ratings", "filter_genres"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# 1. Content Type Filter
all_types = sorted(df_raw['type'].dropna().unique().tolist())
selected_types = st.sidebar.multiselect(
    "Content Type",
    options=all_types,
    default=all_types,
    key="filter_types"
)

# 2. Release Year Range
min_yr = int(df_raw['release_year'].min())
max_yr = int(df_raw['release_year'].max())
selected_years = st.sidebar.slider(
    "Release Year Range",
    min_value=min_yr,
    max_value=max_yr,
    value=(min_yr, max_yr),
    key="filter_years"
)

# 3. Country Filter (Unpacked top countries + All)
all_unique_countries = sorted(list({c for sublist in df_raw['country_list'] for c in sublist if c}))
selected_countries = st.sidebar.multiselect(
    "Country",
    options=["All"] + all_unique_countries,
    default=["All"],
    key="filter_countries"
)

# 4. Rating Filter
all_ratings = sorted(df_raw['rating_imputed'].unique().tolist())
selected_ratings = st.sidebar.multiselect(
    "Content Rating",
    options=["All"] + all_ratings,
    default=["All"],
    key="filter_ratings"
)

# 5. Genre Filter (Unpacked all genres)
all_unique_genres = sorted(list({g for sublist in df_raw['genre_list'] for g in sublist if g}))
selected_genres = st.sidebar.multiselect(
    "Genre",
    options=["All"] + all_unique_genres,
    default=["All"],
    key="filter_genres"
)

# Filtering logic
filtered_df = df_raw.copy()

# Type filter
if selected_types:
    filtered_df = filtered_df[filtered_df['type'].isin(selected_types)]
else:
    filtered_df = filtered_df.iloc[0:0]

# Year filter
filtered_df = filtered_df[
    (filtered_df['release_year'] >= selected_years[0]) & 
    (filtered_df['release_year'] <= selected_years[1])
]

# Country filter
if "All" not in selected_countries and len(selected_countries) > 0:
    filtered_df = filtered_df[filtered_df['country_list'].apply(lambda lst: any(c in selected_countries for c in lst))]

# Rating filter
if "All" not in selected_ratings and len(selected_ratings) > 0:
    filtered_df = filtered_df[filtered_df['rating_imputed'].isin(selected_ratings)]

# Genre filter
if "All" not in selected_genres and len(selected_genres) > 0:
    filtered_df = filtered_df[filtered_df['genre_list'].apply(lambda lst: any(g in selected_genres for g in lst))]

# Sidebar info
st.sidebar.divider()
st.sidebar.caption(f"Showing **{len(filtered_df):,}** of **{len(df_raw):,}** total titles")
st.sidebar.caption("Dataset source: Public Netflix Catalog (TidyTuesday)")

# ---------------------------------------------------------
# Main App Header
# ---------------------------------------------------------
st.title("🎬 Netflix Data Analysis")
st.markdown("#### *Exploratory Data Analysis and Interactive Dashboard*")
st.markdown("Analyze content trends, geographical distribution, genre dynamics, maturity ratings, and movie runtimes across the Netflix catalogue.")

# Check for empty filter result
if filtered_df.empty:
    st.warning("⚠️ No titles match the current filter selection. Please adjust your filters in the sidebar or click 'Reset Filters'.")
    st.stop()

# ---------------------------------------------------------
# Dynamic KPI Cards
# ---------------------------------------------------------
total_titles = len(filtered_df)
movies_cnt = int((filtered_df['type'] == 'Movie').sum())
tv_cnt = int((filtered_df['type'] == 'TV Show').sum())
countries_cnt = len({c for sublist in filtered_df['country_list'] for c in sublist if c})
genres_cnt = len({g for sublist in filtered_df['genre_list'] for g in sublist if g})
latest_release = int(filtered_df['release_year'].max()) if not filtered_df['release_year'].isna().all() else "N/A"

movie_pct = (movies_cnt / total_titles * 100) if total_titles > 0 else 0
tv_pct = (tv_cnt / total_titles * 100) if total_titles > 0 else 0

# Responsive KPI layout: 3 cards per row to prevent horizontal clipping.
kpi_row1 = st.columns(3)
kpi_row2 = st.columns(3)

with kpi_row1[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Titles</div>
        <div class="metric-value">{total_titles:,}</div>
        <div class="metric-subtitle">Filtered Catalogue</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_row1[1]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Movies</div>
        <div class="metric-value">{movies_cnt:,}</div>
        <div class="metric-subtitle">{movie_pct:.1f}% of total</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_row1[2]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TV Shows</div>
        <div class="metric-value">{tv_cnt:,}</div>
        <div class="metric-subtitle">{tv_pct:.1f}% of total</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_row2[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Countries</div>
        <div class="metric-value">{countries_cnt:,}</div>
        <div class="metric-subtitle">Represented</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_row2[1]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Genres</div>
        <div class="metric-value">{genres_cnt:,}</div>
        <div class="metric-subtitle">Unique Categories</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_row2[2]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Latest Release</div>
        <div class="metric-value">{latest_release}</div>
        <div class="metric-subtitle">Release Year</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: Overview
# ---------------------------------------------------------
st.markdown("### 📊 Content Type Overview")

col_ov1, col_ov2 = st.columns([1, 1])

with col_ov1:
    st.subheader("Movies vs TV Shows Count")
    type_counts = filtered_df['type'].value_counts()
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    colors = [NETFLIX_RED if t == 'Movie' else '#505050' for t in type_counts.index]
    bars = ax.bar(type_counts.index, type_counts.values, color=colors, width=0.45, edgecolor='#2E2E2E', linewidth=1.2)
    for b in bars:
        h = b.get_height()
        ax.annotate(f'{h:,}\n({h/total_titles*100:.1f}%)',
                    xy=(b.get_x() + b.get_width()/2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color=LIGHT_GRAY)
    ax.set_ylabel("Number of Titles", fontsize=10)
    ax.set_ylim(0, max(type_counts.values) * 1.2 if len(type_counts) > 0 else 10)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    st.pyplot(fig, clear_figure=True)

with col_ov2:
    st.subheader("Catalogue Share (%)")
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    colors = [NETFLIX_RED if t == 'Movie' else '#404040' for t in type_counts.index]
    wedges, texts, autotexts = ax.pie(
        type_counts.values,
        labels=type_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor=BG_COLOR, linewidth=2),
        textprops=dict(color=LIGHT_GRAY, fontsize=11, fontweight='bold')
    )
    for at in autotexts:
        at.set_color('white')
        at.set_weight('bold')
    st.pyplot(fig, clear_figure=True)

st.divider()

# ---------------------------------------------------------
# SECTION 2: Genre Analysis
# ---------------------------------------------------------
st.markdown("### 🎭 Genre Analysis")

col_g1, col_g2 = st.columns([1.1, 1.2])

all_filtered_genres = pd.Series([g for sublist in filtered_df['genre_list'] for g in sublist])
top_10_genres = all_filtered_genres.value_counts().head(10).sort_values(ascending=True)

with col_g1:
    st.subheader("Top 10 Overall Genres")
    if not top_10_genres.empty:
        fig, ax = plt.subplots(figsize=(6.0, 3.8))
        norm = plt.Normalize(top_10_genres.values.min(), top_10_genres.values.max())
        colors = plt.cm.Reds(norm(top_10_genres.values) * 0.7 + 0.3)
        bars = ax.barh(top_10_genres.index, top_10_genres.values, color=colors, height=0.6)
        for b in bars:
            w = b.get_width()
            ax.annotate(f' {w:,}', xy=(w, b.get_y() + b.get_height()/2),
                        xytext=(3, 0), textcoords="offset points", ha='left', va='center', fontsize=9, color=LIGHT_GRAY)
        ax.set_xlabel("Number of Titles", fontsize=10)
        ax.set_xlim(0, max(top_10_genres.values) * 1.15)
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("No genre data available.")

with col_g2:
    st.subheader("Movie vs TV Show Top Genres")
    m_genres = pd.Series([g for sublist in filtered_df[filtered_df['type']=='Movie']['genre_list'] for g in sublist]).value_counts().head(5)
    t_genres = pd.Series([g for sublist in filtered_df[filtered_df['type']=='TV Show']['genre_list'] for g in sublist]).value_counts().head(5)
    
    fig, (ax_m, ax_t) = plt.subplots(1, 2, figsize=(7.5, 3.8))
    if not m_genres.empty:
        ax_m.barh(m_genres.sort_values().index, m_genres.sort_values().values, color=NETFLIX_RED, height=0.55)
        ax_m.set_title("Movies", fontsize=11, fontweight='bold', color='white')
        ax_m.grid(axis='x', linestyle='--', alpha=0.3)
    if not t_genres.empty:
        ax_t.barh(t_genres.sort_values().index, t_genres.sort_values().values, color='#00A8E8', height=0.55)
        ax_t.set_title("TV Shows", fontsize=11, fontweight='bold', color='white')
        ax_t.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

st.divider()

# ---------------------------------------------------------
# SECTION 3: Geographic Analysis
# ---------------------------------------------------------
st.markdown("### 🌍 Geographic Distribution")

col_geo1, col_geo2 = st.columns([1.2, 1])

all_filtered_countries = pd.Series([c for sublist in filtered_df['country_list'] for c in sublist if c])
top_10_countries = all_filtered_countries.value_counts().head(10).sort_values(ascending=True)

with col_geo1:
    st.subheader("Top 10 Content Producing Countries")
    if not top_10_countries.empty:
        fig, ax = plt.subplots(figsize=(6.0, 3.6))
        norm = plt.Normalize(top_10_countries.values.min(), top_10_countries.values.max())
        colors = plt.cm.Reds(norm(top_10_countries.values) * 0.7 + 0.3)
        bars = ax.barh(top_10_countries.index, top_10_countries.values, color=colors, height=0.6)
        for b in bars:
            w = b.get_width()
            ax.annotate(f' {w:,}', xy=(w, b.get_y() + b.get_height()/2),
                        xytext=(4, 0), textcoords="offset points", ha='left', va='center', fontsize=9, color=LIGHT_GRAY)
        ax.set_xlabel("Number of Titles", fontsize=10)
        ax.set_xlim(0, max(top_10_countries.values) * 1.15)
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("No country data available.")

with col_geo2:
    st.subheader("Country Share Table")
    if not top_10_countries.empty:
        country_df = top_10_countries.sort_values(ascending=False).reset_index()
        country_df.columns = ["Country", "Titles"]
        country_df["Percentage"] = (country_df["Titles"] / total_titles * 100).map("{:.1f}%".format)
        st.dataframe(country_df, use_container_width=True, hide_index=True)
    else:
        st.info("No country data available.")

st.divider()

# ---------------------------------------------------------
# SECTION 4: Time Analysis
# ---------------------------------------------------------
st.markdown("### 📈 Temporal Trends & Content Growth")

col_t1, col_t2 = st.columns([1.2, 1])

with col_t1:
    st.subheader("Content Added Over Time (by Year)")
    added_trend = filtered_df['year_added'].dropna().value_counts().sort_index()
    if not added_trend.empty:
        fig, ax = plt.subplots(figsize=(6.5, 3.5))
        ax.plot(added_trend.index.astype(int), added_trend.values, marker='o', color=NETFLIX_RED, linewidth=2.5, markersize=5)
        ax.fill_between(added_trend.index.astype(int), added_trend.values, color=NETFLIX_RED, alpha=0.25)
        for x, y in zip(added_trend.index.astype(int), added_trend.values):
            ax.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8, color=LIGHT_GRAY)
        ax.set_xlabel("Year Added", fontsize=10)
        ax.set_ylabel("Titles Added", fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("Date added information not available for selected subset.")

with col_t2:
    st.subheader("Original Release Year Distribution")
    release_trend = filtered_df[filtered_df['release_year'] >= 2000]['release_year'].value_counts().sort_index()
    if not release_trend.empty:
        fig, ax = plt.subplots(figsize=(6.0, 3.5))
        ax.bar(release_trend.index.astype(int), release_trend.values, color='#454545', edgecolor=NETFLIX_RED, linewidth=1)
        ax.set_xlabel("Release Year (>= 2000)", fontsize=10)
        ax.set_ylabel("Titles Released", fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("No release year data.")

st.divider()

# ---------------------------------------------------------
# SECTION 5: Ratings
# ---------------------------------------------------------
st.markdown("### 🎯 Maturity Ratings Analysis")

col_r1, col_r2 = st.columns([1.1, 1.2])

with col_r1:
    st.subheader("Rating Distribution")
    top_ratings = filtered_df['rating_imputed'].value_counts().head(10)
    if not top_ratings.empty:
        fig, ax = plt.subplots(figsize=(6.0, 3.5))
        bars = ax.bar(top_ratings.index, top_ratings.values, color=NETFLIX_RED, width=0.6, edgecolor='#333333')
        for b in bars:
            h = b.get_height()
            ax.annotate(f'{h:,}', xy=(b.get_x() + b.get_width()/2, h),
                        xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=8, color=LIGHT_GRAY)
        ax.set_xlabel("Rating", fontsize=10)
        ax.set_ylabel("Titles", fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig, clear_figure=True)

with col_r2:
    st.subheader("Rating Breakdown by Type")
    rating_by_type = pd.crosstab(filtered_df['rating_imputed'], filtered_df['type'])
    # Pick top 8 overall ratings
    top_8_ratings = top_ratings.head(8).index
    rating_by_type = rating_by_type.reindex(top_8_ratings).fillna(0)
    
    if not rating_by_type.empty:
        fig, ax = plt.subplots(figsize=(6.5, 3.5))
        rating_by_type.plot(kind='bar', stacked=True, color=[NETFLIX_RED, '#00A8E8'], ax=ax, width=0.65)
        ax.set_xlabel("Rating", fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.legend(title="", frameon=True, facecolor=CARD_COLOR, edgecolor='#444444')
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig, clear_figure=True)

st.divider()

# ---------------------------------------------------------
# SECTION 6: Movie Analysis
# ---------------------------------------------------------
st.markdown("### 🎥 Movie Analysis")

movies_subset = filtered_df[filtered_df['type'] == 'Movie']

if not movies_subset.empty:
    durations = movies_subset['duration_num'].dropna()
    col_m1, col_m2 = st.columns([1.2, 1])
    
    with col_m1:
        st.subheader("Movie Duration Distribution (minutes)")
        if not durations.empty:
            fig, ax = plt.subplots(figsize=(6.5, 3.5))
            sns.histplot(durations, bins=30, kde=True, color=NETFLIX_RED, edgecolor='#222222', ax=ax, alpha=0.7)
            mean_d = durations.mean()
            median_d = durations.median()
            ax.axvline(mean_d, color='#00FFFF', linestyle='--', linewidth=1.5, label=f'Mean: {mean_d:.1f}m')
            ax.axvline(median_d, color='#FFA500', linestyle='-', linewidth=1.5, label=f'Median: {median_d:.0f}m')
            ax.set_xlabel("Duration (min)", fontsize=10)
            ax.set_ylabel("Count", fontsize=10)
            ax.legend(frameon=True, facecolor=CARD_COLOR, edgecolor='#444444')
            ax.grid(axis='y', linestyle='--', alpha=0.3)
            st.pyplot(fig, clear_figure=True)
            
    with col_m2:
        st.subheader("Top Movie Directors")
        all_directors = pd.Series([d.strip() for d in movies_subset['director'].dropna().astype(str).str.split(',').explode() if d.strip() and d.strip() != 'Unknown Director'])
        top_directors = all_directors.value_counts().head(8).sort_values(ascending=True)
        if not top_directors.empty:
            fig, ax = plt.subplots(figsize=(6.0, 3.5))
            bars = ax.barh(top_directors.index, top_directors.values, color=NETFLIX_RED, height=0.6)
            for b in bars:
                w = b.get_width()
                ax.annotate(f' {w}', xy=(w, b.get_y() + b.get_height()/2),
                            xytext=(3, 0), textcoords="offset points", ha='left', va='center', fontsize=9, color=LIGHT_GRAY)
            ax.set_xlabel("Directed Movies", fontsize=10)
            ax.set_xlim(0, max(top_directors.values) + 3)
            ax.grid(axis='x', linestyle='--', alpha=0.3)
            st.pyplot(fig, clear_figure=True)
        else:
            st.info("No director data found.")
            
    # Movie stats summary
    if not durations.empty:
        ms1, ms2, ms3, ms4 = st.columns(4)
        ms1.metric("Average Duration", f"{durations.mean():.1f} min")
        ms2.metric("Median Duration", f"{durations.median():.0f} min")
        ms3.metric("Shortest Movie", f"{int(durations.min())} min")
        ms4.metric("Longest Movie", f"{int(durations.max())} min")
else:
    st.info("No movie content available in the selected filter range.")

st.divider()

# ---------------------------------------------------------
# SECTION 7: Searchable Data Table & CSV Download
# ---------------------------------------------------------
st.markdown("### 📑 Interactive Data Explorer")

search_term = st.text_input("🔍 Search catalogue by title, director, country, or genre:", "")
table_display_df = filtered_df[['show_id', 'type', 'title', 'director_imputed', 'country_imputed', 'release_year', 'rating_imputed', 'duration', 'listed_in', 'date_added']]
table_display_df = table_display_df.rename(columns={
    'director_imputed': 'director',
    'country_imputed': 'country',
    'rating_imputed': 'rating'
})

if search_term:
    mask = (
        table_display_df['title'].astype(str).str.contains(search_term, case=False, na=False) |
        table_display_df['director'].astype(str).str.contains(search_term, case=False, na=False) |
        table_display_df['country'].astype(str).str.contains(search_term, case=False, na=False) |
        table_display_df['listed_in'].astype(str).str.contains(search_term, case=False, na=False)
    )
    table_display_df = table_display_df[mask]

st.dataframe(
    table_display_df.sort_values('release_year', ascending=False),
    use_container_width=True,
    hide_index=True
)

csv_data = table_display_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv_data,
    file_name="netflix_filtered_data.csv",
    mime="text/csv",
    use_container_width=False
)

st.divider()

# ---------------------------------------------------------
# SECTION 8: Key Insights (Dynamically Computed)
# ---------------------------------------------------------
st.markdown("### 💡 Key Analytical Insights")

# Calculate dynamic statistics
total_cnt = len(filtered_df)
pct_movies = (movies_cnt / total_cnt * 100) if total_cnt > 0 else 0
pct_tv = (tv_cnt / total_cnt * 100) if total_cnt > 0 else 0

top_genre_name = all_filtered_genres.value_counts().index[0] if not all_filtered_genres.empty else "N/A"
top_genre_count = all_filtered_genres.value_counts().values[0] if not all_filtered_genres.empty else 0

top_country_name = all_filtered_countries.value_counts().index[0] if not all_filtered_countries.empty else "N/A"
top_country_count = all_filtered_countries.value_counts().values[0] if not all_filtered_countries.empty else 0

peak_rel_year = filtered_df['release_year'].value_counts().index[0] if not filtered_df.empty else "N/A"
peak_rel_count = filtered_df['release_year'].value_counts().values[0] if not filtered_df.empty else 0

top_rating_name = filtered_df['rating_imputed'].value_counts().index[0] if not filtered_df.empty else "N/A"
top_rating_count = filtered_df['rating_imputed'].value_counts().values[0] if not filtered_df.empty else 0

avg_runtime = filtered_df[filtered_df['type']=='Movie']['duration_num'].mean()

st.markdown(f"""
<div class="insight-box">
    <strong>1. Catalogue Split:</strong> Movies represent <strong>{pct_movies:.1f}%</strong> ({movies_cnt:,} titles) of the catalogue, while TV Shows comprise <strong>{pct_tv:.1f}%</strong> ({tv_cnt:,} titles).
</div>
<div class="insight-box">
    <strong>2. Dominant Genre:</strong> The most frequent content category is <strong>{top_genre_name}</strong>, appearing in <strong>{top_genre_count:,}</strong> titles.
</div>
<div class="insight-box">
    <strong>3. Content Production Hub:</strong> <strong>{top_country_name}</strong> is the primary source country with <strong>{top_country_count:,}</strong> titles represented.
</div>
<div class="insight-box">
    <strong>4. Peak Release Production:</strong> The year with the highest volume of original content is <strong>{peak_rel_year}</strong> with <strong>{peak_rel_count:,}</strong> releases.
</div>
<div class="insight-box">
    <strong>5. Maturity Ratings:</strong> The predominant content rating is <strong>{top_rating_name}</strong> with <strong>{top_rating_count:,}</strong> titles, indicating a catalogue strongly targeted toward mature audiences.
</div>
""", unsafe_allow_html=True)

if not np.isnan(avg_runtime):
    st.markdown(f"""
    <div class="insight-box">
        <strong>6. Average Movie Runtime:</strong> Feature films in this selection average <strong>{avg_runtime:.1f} minutes</strong>, providing a useful summary of movie runtime patterns in the filtered dataset.
    </div>
    """, unsafe_allow_html=True)
