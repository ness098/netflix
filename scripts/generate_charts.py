"""
generate_charts.py
Generates publication-quality charts for the Netflix Data Analysis project
using Matplotlib and Seaborn with a Netflix-inspired dark aesthetic.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure charts directory exists
os.makedirs('charts', exist_ok=True)

# Set global aesthetics
plt.style.use('dark_background')
NETFLIX_RED = '#E50914'
NETFLIX_DARK_RED = '#B81D24'
ACCENT_GRAY = '#808080'
LIGHT_GRAY = '#E5E5E5'
BG_COLOR = '#141414'
CARD_COLOR = '#1F1F1F'

plt.rcParams['figure.facecolor'] = BG_COLOR
plt.rcParams['axes.facecolor'] = CARD_COLOR
plt.rcParams['text.color'] = LIGHT_GRAY
plt.rcParams['axes.labelcolor'] = LIGHT_GRAY
plt.rcParams['xtick.color'] = LIGHT_GRAY
plt.rcParams['ytick.color'] = LIGHT_GRAY
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.size'] = 11

def load_and_preprocess():
    df = pd.read_csv('data/netflix_titles.csv', encoding='utf-8')
    # Replace corrupted character in director/cast names if present
    for col in ['director', 'cast', 'title']:
        df[col] = df[col].astype(str).str.replace('Ral', 'Raúl')
        df[col] = df[col].replace('nan', np.nan)
        
    df['date_added_clean'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')
    df['year_added'] = df['date_added_clean'].dt.year
    df['duration_min'] = df[df['type'] == 'Movie']['duration'].str.extract(r'(\d+)').astype(float)
    return df

def generate_content_type_chart(df):
    """1. content_type.png - Movies vs TV Shows Bar Chart"""
    fig, ax = plt.subplots(figsize=(8, 6))
    type_counts = df['type'].value_counts()
    
    colors = [NETFLIX_RED, '#564d4d']
    bars = ax.bar(type_counts.index, type_counts.values, color=colors, width=0.5, edgecolor='#333333', linewidth=1.2)
    
    for bar in bars:
        height = bar.get_height()
        pct = (height / len(df)) * 100
        ax.annotate(f'{height:,}\n({pct:.1f}%)',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold', color=LIGHT_GRAY)
        
    ax.set_title('Catalogue Distribution: Movies vs TV Shows', fontsize=15, fontweight='bold', pad=20, color='white')
    ax.set_ylabel('Number of Titles', fontsize=12, labelpad=10)
    ax.set_ylim(0, max(type_counts.values) * 1.15)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig('charts/content_type.png', dpi=300)
    plt.close()
    print("Saved charts/content_type.png")

def generate_donut_chart(df):
    """type_distribution_donut.png - Movies vs TV Shows Donut Chart"""
    fig, ax = plt.subplots(figsize=(7, 7))
    type_counts = df['type'].value_counts()
    colors = [NETFLIX_RED, '#404040']
    
    wedges, texts, autotexts = ax.pie(
        type_counts.values, 
        labels=type_counts.index, 
        autopct='%1.1f%%',
        startangle=140, 
        colors=colors,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor=BG_COLOR, linewidth=2),
        textprops=dict(color=LIGHT_GRAY, fontsize=13, fontweight='bold')
    )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(13)
        autotext.set_weight('bold')
        
    ax.set_title('Catalogue Proportion by Content Type', fontsize=15, fontweight='bold', pad=20, color='white')
    plt.tight_layout()
    fig.savefig('charts/type_distribution_donut.png', dpi=300)
    plt.close()
    print("Saved charts/type_distribution_donut.png")

def generate_top_genres_chart(df):
    """2. top_genres.png - Top 10 Genres Horizontal Bar Chart"""
    genres_series = df['listed_in'].dropna().apply(lambda x: [g.strip() for g in x.split(',')]).explode()
    top_10 = genres_series.value_counts().head(10).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6.5))
    norm = plt.Normalize(top_10.values.min(), top_10.values.max())
    colors = plt.cm.Reds(norm(top_10.values) * 0.7 + 0.3)
    
    bars = ax.barh(top_10.index, top_10.values, color=colors, edgecolor='#333333', height=0.65)
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f' {width:,}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=11, fontweight='bold', color=LIGHT_GRAY)
        
    ax.set_title('Top 10 Genres Across Entire Catalogue', fontsize=15, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Number of Titles', fontsize=12, labelpad=10)
    ax.set_xlim(0, max(top_10.values) * 1.15)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig('charts/top_genres.png', dpi=300)
    plt.close()
    print("Saved charts/top_genres.png")

def generate_yearly_trend_chart(df):
    """3. yearly_trend.png - Content Added Over Time vs Release Year"""
    added_trend = df['year_added'].value_counts().sort_index()
    # Filter reasonable range for added (e.g. >= 2010)
    added_trend = added_trend[added_trend.index >= 2010]
    
    release_trend = df[df['release_year'] >= 2010]['release_year'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(added_trend.index, added_trend.values, marker='o', color=NETFLIX_RED, linewidth=2.5, label='Titles Added to Netflix', markersize=6)
    ax.plot(release_trend.index, release_trend.values, marker='s', color='#FFA500', linewidth=2, linestyle='--', label='Titles by Release Year', markersize=5)
    
    for x, y in zip(added_trend.index, added_trend.values):
        ax.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9, color=LIGHT_GRAY)
        
    ax.set_title('Content Expansion Trend (2010 – 2021)', fontsize=15, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Year', fontsize=12, labelpad=10)
    ax.set_ylabel('Number of Titles', fontsize=12, labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(frameon=True, facecolor=CARD_COLOR, edgecolor='#444444', loc='upper left')
    plt.tight_layout()
    fig.savefig('charts/yearly_trend.png', dpi=300)
    plt.close()
    print("Saved charts/yearly_trend.png")

def generate_rating_distribution_chart(df):
    """4. rating_distribution.png - Rating Distribution Bar Chart"""
    ratings = df['rating'].fillna('Unknown').value_counts()
    top_ratings = ratings.head(10)
    
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.bar(top_ratings.index, top_ratings.values, color=NETFLIX_RED, width=0.6, edgecolor='#333333')
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color=LIGHT_GRAY)
        
    ax.set_title('Distribution of Content Maturity Ratings', fontsize=15, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Maturity Rating', fontsize=12, labelpad=10)
    ax.set_ylabel('Number of Titles', fontsize=12, labelpad=10)
    ax.set_ylim(0, max(top_ratings.values) * 1.12)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.xticks(rotation=30)
    plt.tight_layout()
    fig.savefig('charts/rating_distribution.png', dpi=300)
    plt.close()
    print("Saved charts/rating_distribution.png")

def generate_country_distribution_chart(df):
    """5. country_distribution.png - Top 10 Countries Horizontal Bar Chart"""
    countries_series = df['country'].dropna().apply(lambda x: [c.strip() for c in x.split(',')]).explode()
    countries_series = countries_series[countries_series != '']
    top_10 = countries_series.value_counts().head(10).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6.5))
    norm = plt.Normalize(top_10.values.min(), top_10.values.max())
    colors = plt.cm.Reds(norm(top_10.values) * 0.7 + 0.3)
    
    bars = ax.barh(top_10.index, top_10.values, color=colors, edgecolor='#333333', height=0.65)
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f' {width:,}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=11, fontweight='bold', color=LIGHT_GRAY)
        
    ax.set_title('Top 10 Content-Producing Countries', fontsize=15, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Number of Titles', fontsize=12, labelpad=10)
    ax.set_xlim(0, max(top_10.values) * 1.15)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig('charts/country_distribution.png', dpi=300)
    plt.close()
    print("Saved charts/country_distribution.png")

def generate_movies_duration_chart(df):
    """6. movies_duration.png - Movie Duration Distribution Histogram"""
    movies = df[df['type'] == 'Movie'].copy()
    durations = movies['duration_min'].dropna()
    
    mean_val = durations.mean()
    median_val = durations.median()
    
    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.histplot(durations, bins=35, kde=True, color=NETFLIX_RED, edgecolor='#222222', ax=ax, alpha=0.7)
    
    ax.axvline(mean_val, color='#00FFFF', linestyle='--', linewidth=2, label=f'Mean Duration: {mean_val:.1f} min')
    ax.axvline(median_val, color='#FFA500', linestyle='-', linewidth=2, label=f'Median Duration: {median_val:.0f} min')
    
    ax.set_title('Movie Duration Distribution', fontsize=15, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Duration (minutes)', fontsize=12, labelpad=10)
    ax.set_ylabel('Number of Movies', fontsize=12, labelpad=10)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(frameon=True, facecolor=CARD_COLOR, edgecolor='#444444', loc='upper right')
    plt.tight_layout()
    fig.savefig('charts/movies_duration.png', dpi=300)
    plt.close()
    print("Saved charts/movies_duration.png")

def generate_release_year_distribution_chart(df):
    """7. release_year_distribution.png - Release Year Distribution"""
    recent_releases = df[df['release_year'] >= 1990]['release_year'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.fill_between(recent_releases.index, recent_releases.values, color=NETFLIX_RED, alpha=0.35)
    ax.plot(recent_releases.index, recent_releases.values, color=NETFLIX_RED, linewidth=2.5, marker='o', markersize=4)
    
    peak_year = recent_releases.idxmax()
    peak_val = recent_releases.max()
    ax.annotate(f'Peak: {peak_year} ({peak_val:,} titles)',
                xy=(peak_year, peak_val), xytext=(peak_year - 8, peak_val + 40),
                arrowprops=dict(facecolor='white', shrink=0.08, width=1.5, headwidth=8),
                fontsize=11, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.4", fc=CARD_COLOR, ec=NETFLIX_RED, lw=1.5))
    
    ax.set_title('Content Distribution by Original Release Year (1990 – 2021)', fontsize=15, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Release Year', fontsize=12, labelpad=10)
    ax.set_ylabel('Number of Titles', fontsize=12, labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig('charts/release_year_distribution.png', dpi=300)
    plt.close()
    print("Saved charts/release_year_distribution.png")

def generate_top_directors_chart(df):
    """top_directors.png - Top 10 Directors Horizontal Bar Chart"""
    directors_series = df['director'].dropna().apply(lambda x: [d.strip() for d in x.split(',')]).explode()
    directors_series = directors_series[directors_series != '']
    top_10 = directors_series.value_counts().head(10).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top_10.index, top_10.values, color=NETFLIX_RED, edgecolor='#333333', height=0.6)
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f' {width}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=11, fontweight='bold', color=LIGHT_GRAY)
        
    ax.set_title('Top 10 Most Prolific Directors', fontsize=15, fontweight='bold', pad=20, color='white')
    ax.set_xlabel('Number of Directed Titles', fontsize=12, labelpad=10)
    ax.set_xlim(0, max(top_10.values) + 3)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig('charts/top_directors.png', dpi=300)
    plt.close()
    print("Saved charts/top_directors.png")

def generate_genre_comparison_chart(df):
    """genre_comparison.png - Movie vs TV Show Top Genres Comparison"""
    movie_genres = df[df['type'] == 'Movie']['listed_in'].dropna().apply(lambda x: [g.strip() for g in x.split(',')]).explode().value_counts().head(7)
    tv_genres = df[df['type'] == 'TV Show']['listed_in'].dropna().apply(lambda x: [g.strip() for g in x.split(',')]).explode().value_counts().head(7)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Movie genres
    ax1.barh(movie_genres.sort_values().index, movie_genres.sort_values().values, color=NETFLIX_RED, height=0.6)
    for bar in ax1.patches:
        ax1.annotate(f' {bar.get_width():,}', (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                     xytext=(4, 0), textcoords="offset points", ha='left', va='center', fontsize=10, color=LIGHT_GRAY)
    ax1.set_title('Top Movie Genres', fontsize=13, fontweight='bold', color='white')
    ax1.set_xlabel('Titles', fontsize=11)
    ax1.grid(axis='x', linestyle='--', alpha=0.3)
    
    # TV genres
    ax2.barh(tv_genres.sort_values().index, tv_genres.sort_values().values, color='#00A8E8', height=0.6)
    for bar in ax2.patches:
        ax2.annotate(f' {bar.get_width():,}', (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                     xytext=(4, 0), textcoords="offset points", ha='left', va='center', fontsize=10, color=LIGHT_GRAY)
    ax2.set_title('Top TV Show Genres', fontsize=13, fontweight='bold', color='white')
    ax2.set_xlabel('Titles', fontsize=11)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    
    fig.suptitle('Genre Comparison: Movies vs TV Shows', fontsize=16, fontweight='bold', color='white', y=1.02)
    plt.tight_layout()
    fig.savefig('charts/genre_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved charts/genre_comparison.png")

if __name__ == '__main__':
    print("Loading data and generating all project charts...")
    df = load_and_preprocess()
    generate_content_type_chart(df)
    generate_donut_chart(df)
    generate_top_genres_chart(df)
    generate_yearly_trend_chart(df)
    generate_rating_distribution_chart(df)
    generate_country_distribution_chart(df)
    generate_movies_duration_chart(df)
    generate_release_year_distribution_chart(df)
    generate_top_directors_chart(df)
    generate_genre_comparison_chart(df)
    print("All charts successfully generated!")
