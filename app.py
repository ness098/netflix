import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MovieHub | Movie Data Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #111111;
    color: #E5E5E5;
}

.main {
    background-color: #111111;
}

h1, h2, h3, h4 {
    color: white !important;
}

.metric-card {
    background-color: #1D1D1D;
    border: 1px solid #333333;
    border-radius: 10px;
    padding: 18px;
    text-align: center;
    min-height: 110px;
}

.metric-title {
    color: #AAAAAA;
    font-size: 13px;
    text-transform: uppercase;
    font-weight: bold;
}

.metric-value {
    color: white;
    font-size: 28px;
    font-weight: bold;
    margin-top: 8px;
}

.metric-subtitle {
    color: #E50914;
    font-size: 12px;
    margin-top: 5px;
}

.insight-box {
    background-color: #1C1C1C;
    border-left: 4px solid #E50914;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 5px;
}

[data-testid="stSidebar"] {
    background-color: #181818;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# COLORS
# =========================================================

RED = "#E50914"
DARK = "#111111"
CARD = "#1D1D1D"
WHITE = "#FFFFFF"
GRAY = "#AAAAAA"


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = Path("data/netflix_titles.csv")

    if not file_path.exists():
        st.error(
            "Dataset not found. Please make sure the file exists at: "
            "data/netflix_titles.csv"
        )
        st.stop()

    df = pd.read_csv(file_path, encoding="utf-8")

    # Remove duplicate rows
    df = df.drop_duplicates().copy()

    # -----------------------------------------------------
    # Make sure important columns exist
    # -----------------------------------------------------

    required_columns = [
        "show_id",
        "type",
        "title",
        "director",
        "cast",
        "country",
        "date_added",
        "release_year",
        "rating",
        "duration",
        "listed_in",
        "description"
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = np.nan

    # -----------------------------------------------------
    # Clean text columns
    # -----------------------------------------------------

    text_columns = [
        "type",
        "title",
        "director",
        "cast",
        "country",
        "rating",
        "duration",
        "listed_in",
        "description"
    ]

    for column in text_columns:
        df[column] = df[column].fillna("").astype(str).str.strip()

    # -----------------------------------------------------
    # Release year
    # -----------------------------------------------------

    df["release_year"] = pd.to_numeric(
        df["release_year"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # Date added
    # -----------------------------------------------------

    df["date_added_clean"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    df["year_added"] = df["date_added_clean"].dt.year

    # -----------------------------------------------------
    # Duration
    # -----------------------------------------------------

    df["duration_num"] = pd.to_numeric(
        df["duration"].str.extract(r"(\d+)")[0],
        errors="coerce"
    )

    df["duration_unit"] = (
        df["duration"]
        .str.extract(r"([A-Za-z]+)")[0]
        .fillna("")
    )

    # -----------------------------------------------------
    # Country
    # -----------------------------------------------------

    df["country_list"] = df["country"].apply(
        lambda x: [
            item.strip()
            for item in x.split(",")
            if item.strip()
        ]
    )

    # -----------------------------------------------------
    # Genre
    # -----------------------------------------------------

    df["genre_list"] = df["listed_in"].apply(
        lambda x: [
            item.strip()
            for item in x.split(",")
            if item.strip()
        ]
    )

    # -----------------------------------------------------
    # Primary genre/country
    # -----------------------------------------------------

    df["primary_genre"] = df["genre_list"].apply(
        lambda x: x[0] if x else "Unknown"
    )

    df["primary_country"] = df["country_list"].apply(
        lambda x: x[0] if x else "Unknown"
    )

    # -----------------------------------------------------
    # Display columns
    # -----------------------------------------------------

    df["director_display"] = df["director"].replace(
        "", "Unknown Director"
    )

    df["country_display"] = df["country"].replace(
        "", "Unknown"
    )

    df["rating_display"] = df["rating"].replace(
        "", "Unknown"
    )

    return df


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎬 MOVIEHUB")
st.sidebar.markdown("### Dashboard Filters")

# Content Type
types = sorted(
    df["type"].dropna().unique().tolist()
)

selected_types = st.sidebar.multiselect(
    "Content Type",
    types,
    default=types
)


# Release year
valid_years = df["release_year"].dropna()

if not valid_years.empty:

    min_year = int(valid_years.min())
    max_year = int(valid_years.max())

    selected_years = st.sidebar.slider(
        "Release Year",
        min_year,
        max_year,
        (min_year, max_year)
    )

else:

    selected_years = (1900, 2100)


# Countries
countries = sorted(
    {
        country
        for values in df["country_list"]
        for country in values
        if country
    }
)

selected_countries = st.sidebar.multiselect(
    "Country",
    countries
)


# Ratings
ratings = sorted(
    [
        rating
        for rating in df["rating_display"].unique()
        if rating
    ]
)

selected_ratings = st.sidebar.multiselect(
    "Rating",
    ratings
)


# Genres
genres = sorted(
    {
        genre
        for values in df["genre_list"]
        for genre in values
        if genre
    }
)

selected_genres = st.sidebar.multiselect(
    "Genre",
    genres
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


# Type
if selected_types:
    filtered_df = filtered_df[
        filtered_df["type"].isin(selected_types)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]


# Year
filtered_df = filtered_df[
    filtered_df["release_year"].between(
        selected_years[0],
        selected_years[1],
        inclusive="both"
    )
]


# Country
if selected_countries:

    filtered_df = filtered_df[
        filtered_df["country_list"].apply(
            lambda x: any(
                country in selected_countries
                for country in x
            )
        )
    ]


# Rating
if selected_ratings:

    filtered_df = filtered_df[
        filtered_df["rating_display"].isin(
            selected_ratings
        )
    ]


# Genre
if selected_genres:

    filtered_df = filtered_df[
        filtered_df["genre_list"].apply(
            lambda x: any(
                genre in selected_genres
                for genre in x
            )
        )
    ]


st.sidebar.divider()

st.sidebar.write(
    f"Showing **{len(filtered_df):,}** "
    f"of **{len(df):,}** titles"
)


# =========================================================
# HEADER
# =========================================================

st.title("🎬 MovieHub")
st.markdown(
    "### Movie & TV Show Data Analytics Platform"
)

st.write(
    "Explore movies and TV shows using interactive filters, "
    "charts, ratings, genres, countries and release trends."
)


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "No content matches the selected filters."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_titles = len(filtered_df)

movies = int(
    (filtered_df["type"] == "Movie").sum()
)

tv_shows = int(
    (filtered_df["type"] == "TV Show").sum()
)

countries_count = len(
    {
        country
        for values in filtered_df["country_list"]
        for country in values
        if country
    }
)

genres_count = len(
    {
        genre
        for values in filtered_df["genre_list"]
        for genre in values
        if genre
    }
)

valid_release_years = filtered_df[
    "release_year"
].dropna()

latest_year = (
    int(valid_release_years.max())
    if not valid_release_years.empty
    else "N/A"
)


# =========================================================
# KPI CARDS
# =========================================================

c1, c2, c3, c4, c5 = st.columns(5)


with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Total Titles</div>
            <div class="metric-value">{total_titles:,}</div>
            <div class="metric-subtitle">Catalogue</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Movies</div>
            <div class="metric-value">{movies:,}</div>
            <div class="metric-subtitle">Films</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">TV Shows</div>
            <div class="metric-value">{tv_shows:,}</div>
            <div class="metric-subtitle">Series</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Countries</div>
            <div class="metric-value">{countries_count:,}</div>
            <div class="metric-subtitle">Represented</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Genres</div>
            <div class="metric-value">{genres_count:,}</div>
            <div class="metric-subtitle">Categories</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================================================
# CONTENT TYPE
# =========================================================

st.header("📊 Content Overview")

col1, col2 = st.columns(2)

type_counts = filtered_df["type"].value_counts()


with col1:

    st.subheader("Movies vs TV Shows")

    fig, ax = plt.subplots(figsize=(7, 4))

    colors = [
        RED if value == "Movie"
        else "#555555"
        for value in type_counts.index
    ]

    bars = ax.bar(
        type_counts.index,
        type_counts.values,
        color=colors
    )

    ax.set_ylabel("Number of Titles")
    ax.set_facecolor(CARD)
    fig.patch.set_facecolor(DARK)

    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height):,}",
            ha="center",
            va="bottom",
            color="white"
        )

    st.pyplot(fig)
    plt.close(fig)


with col2:

    st.subheader("Catalogue Percentage")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.pie(
        type_counts.values,
        labels=type_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=[
            RED,
            "#555555"
        ],
        textprops={"color": "white"}
    )

    fig.patch.set_facecolor(DARK)

    st.pyplot(fig)
    plt.close(fig)


st.divider()


# =========================================================
# GENRE ANALYSIS
# =========================================================

st.header("🎭 Genre Analysis")

genre_series = pd.Series(
    [
        genre
        for values in filtered_df["genre_list"]
        for genre in values
    ]
)

top_genres = (
    genre_series
    .value_counts()
    .head(10)
    .sort_values()
)


if not top_genres.empty:

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(
        top_genres.index,
        top_genres.values,
        color=RED
    )

    ax.set_xlabel("Number of Titles")
    ax.set_facecolor(CARD)
    fig.patch.set_facecolor(DARK)

    for i, value in enumerate(top_genres.values):

        ax.text(
            value,
            i,
            f" {value:,}",
            va="center",
            color="white"
        )

    st.pyplot(fig)
    plt.close(fig)


st.divider()


# =========================================================
# COUNTRY ANALYSIS
# =========================================================

st.header("🌍 Country Analysis")

country_series = pd.Series(
    [
        country
        for values in filtered_df["country_list"]
        for country in values
    ]
)

top_countries = (
    country_series
    .value_counts()
    .head(10)
    .sort_values()
)


if not top_countries.empty:

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(
        top_countries.index,
        top_countries.values,
        color=RED
    )

    ax.set_xlabel("Number of Titles")
    ax.set_facecolor(CARD)
    fig.patch.set_facecolor(DARK)

    st.pyplot(fig)
    plt.close(fig)


st.divider()


# =========================================================
# TIME ANALYSIS
# =========================================================

st.header("📈 Release Trends")

release_data = (
    filtered_df["release_year"]
    .dropna()
    .astype(int)
    .value_counts()
    .sort_index()
)


if not release_data.empty:

    fig, ax = plt.subplots(figsize=(11, 4))

    ax.plot(
        release_data.index,
        release_data.values,
        marker="o",
        color=RED,
        linewidth=2
    )

    ax.set_xlabel("Release Year")
    ax.set_ylabel("Number of Titles")

    ax.set_facecolor(CARD)
    fig.patch.set_facecolor(DARK)

    st.pyplot(fig)
    plt.close(fig)


st.divider()


# =========================================================
# RATING ANALYSIS
# =========================================================

st.header("🎯 Rating Analysis")

rating_data = (
    filtered_df["rating_display"]
    .value_counts()
    .head(10)
)


if not rating_data.empty:

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.bar(
        rating_data.index,
        rating_data.values,
        color=RED
    )

    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of Titles")

    plt.xticks(rotation=45)

    ax.set_facecolor(CARD)
    fig.patch.set_facecolor(DARK)

    st.pyplot(fig)
    plt.close(fig)


st.divider()


# =========================================================
# MOVIE DURATION
# =========================================================

st.header("🎥 Movie Duration")

movie_data = filtered_df[
    filtered_df["type"] == "Movie"
]

durations = movie_data[
    "duration_num"
].dropna()


if not durations.empty:

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(8, 4))

        sns.histplot(
            durations,
            bins=30,
            kde=True,
            color=RED,
            ax=ax
        )

        ax.set_xlabel("Duration (minutes)")
        ax.set_ylabel("Movies")

        ax.set_facecolor(CARD)
        fig.patch.set_facecolor(DARK)

        st.pyplot(fig)
        plt.close(fig)


    with col2:

        st.metric(
            "Average Runtime",
            f"{durations.mean():.1f} min"
        )

        st.metric(
            "Median Runtime",
            f"{durations.median():.0f} min"
        )

        st.metric(
            "Shortest Movie",
            f"{durations.min():.0f} min"
        )

        st.metric(
            "Longest Movie",
            f"{durations.max():.0f} min"
        )


st.divider()


# =========================================================
# SEARCH
# =========================================================

st.header("🔎 Movie Explorer")

search = st.text_input(
    "Search by title, director, country or genre"
)


display_df = filtered_df[
    [
        "show_id",
        "type",
        "title",
        "director_display",
        "country_display",
        "release_year",
        "rating_display",
        "duration",
        "listed_in",
        "date_added"
    ]
].copy()


display_df.columns = [
    "ID",
    "Type",
    "Title",
    "Director",
    "Country",
    "Release Year",
    "Rating",
    "Duration",
    "Genre",
    "Date Added"
]


if search:

    mask = (
        display_df["Title"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
        |
        display_df["Director"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
        |
        display_df["Country"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
        |
        display_df["Genre"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    )

    display_df = display_df[mask]


display_df = display_df.sort_values(
    "Release Year",
    ascending=False
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CSV DOWNLOAD
# =========================================================

csv = display_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    "📥 Download Movie Data",
    data=csv,
    file_name="movie_data.csv",
    mime="text/csv"
)


st.divider()


# =========================================================
# INSIGHTS
# =========================================================

st.header("💡 Key Insights")


top_genre = (
    genre_series.value_counts().index[0]
    if not genre_series.empty
    else "N/A"
)

top_country = (
    country_series.value_counts().index[0]
    if not country_series.empty
    else "N/A"
)

top_rating = (
    filtered_df["rating_display"]
    .value_counts().index[0]
    if not filtered_df.empty
    else "N/A"
)


movie_percentage = (
    movies / total_titles * 100
    if total_titles > 0
    else 0
)


tv_percentage = (
    tv_shows / total_titles * 100
    if total_titles > 0
    else 0
)


st.markdown(
    f"""
    <div class="insight-box">
    🎬 <b>Content Split:</b>
    Movies represent {movie_percentage:.1f}% of the selected catalogue,
    while TV Shows represent {tv_percentage:.1f}%.
    </div>

    <div class="insight-box">
    🎭 <b>Popular Genre:</b>
    {top_genre} is the most frequently represented genre.
    </div>

    <div class="insight-box">
    🌍 <b>Top Country:</b>
    {top_country} has the highest number of represented titles.
    </div>

    <div class="insight-box">
    ⭐ <b>Popular Rating:</b>
    {top_rating} is the most common content rating.
    </div>

    <div class="insight-box">
    📅 <b>Latest Release Year:</b>
    {latest_year}.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🎬 MovieHub — Interactive Movie & TV Show Analytics Platform"
)
