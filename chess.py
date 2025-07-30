import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('games.csv', encoding='ascii')

# --- Preprocessing ---
def parse_time_control(code):
    try:
        base, inc = code.split('+')
        return int(base)
    except:
        return None

df['base_minutes'] = df['increment_code'].apply(parse_time_control)
bins = [-1, 2, 8, 15, 60]
labels = ['Bullet', 'Blitz', 'Rapid', 'Classical']
df['time_category'] = pd.cut(df['base_minutes'], bins=bins, labels=labels)
df['white_win'] = df['winner'] == 'white'
df['black_win'] = df['winner'] == 'black'

# ---------- PAGE 1 ----------
plt.figure(figsize=(11, 8.5))
plt.suptitle('Chess Games Overview: Player Performance & Ratings', fontsize=16, weight='bold')

# Rating distribution
plt.subplot(2, 2, 1)
sns.histplot(df['white_rating'], color='skyblue', kde=True, bins=30, alpha=0.6, label='White')
sns.histplot(df['black_rating'], color='salmon', kde=True, bins=30, alpha=0.6, label='Black')
plt.xlabel('Rating')
plt.title('Rating Distribution')
plt.legend()

# Win rate by rating bucket
rating_bins = pd.cut(pd.concat([df['white_rating'], df['black_rating']]), bins=5, retbins=True)[1]
df['white_rating_bucket'] = pd.cut(df['white_rating'], bins=rating_bins)
bucket_win = df.groupby('white_rating_bucket')['white_win'].mean()
plt.subplot(2, 2, 2)
bucket_win.plot(kind='bar', color='seagreen')
plt.ylabel('Win rate (White)')
plt.title('White win rate by rating bucket')
plt.xticks(rotation=45, ha='right')

# Top players by volume
plt.subplot(2, 1, 2)
player_counts = df['white_id'].value_counts().head(10)
bar = sns.barplot(x=player_counts.index, y=player_counts.values, palette='Blues_d')
for i, val in enumerate(player_counts.values):
    bar.text(i, val, str(val), ha='center', va='bottom', fontsize=8)
plt.ylabel('Games as White')
plt.title('Top 10 most active players (as White)')
plt.xticks(rotation=45, ha='right')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('report_page1.png', dpi=300)
plt.close()

# ---------- PAGE 2 ----------
plt.figure(figsize=(11, 8.5))
plt.suptitle('Game Outcomes & Opening Popularity', fontsize=16, weight='bold')

# Victory status
plt.subplot(2, 2, 1)
outcome = df['victory_status'].value_counts()
colors = sns.color_palette('pastel')[0:len(outcome)]
plt.pie(outcome.values, labels=outcome.index, autopct='%1.0f%%', colors=colors, startangle=140)
plt.title('Game End Status')

# Top 10 openings
plt.subplot(2, 2, 2)
open_counts = df['opening_name'].value_counts().head(10)
sns.barplot(y=open_counts.index, x=open_counts.values, palette='viridis')
plt.xlabel('Games played')
plt.title('Top 10 Openings')

# White win rate by opening
plt.subplot(2, 1, 2)
open_win = df.groupby('opening_name')['white_win'].mean().loc[open_counts.index]
bar = sns.barplot(x=open_win.index, y=open_win.values, palette='rocket')
plt.ylabel('White win rate')
plt.title('White win rate for popular openings')
plt.xticks(rotation=45, ha='right')
for i, val in enumerate(open_win.values):
    bar.text(i, val, '{:.0%}'.format(val), ha='center', va='bottom', fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('report_page2.png', dpi=300)
plt.close()

# ---------- PAGE 3 ----------
plt.figure(figsize=(11, 8.5))
plt.suptitle('Impact of Time Controls', fontsize=16, weight='bold')

# Turns by time category
plt.subplot(2, 2, 1)
sns.boxplot(x='time_category', y='turns', data=df, palette='Set2')
plt.xlabel('Time category')
plt.ylabel('Turns')
plt.title('Game length by time control')

# Win rate by time control
plt.subplot(2, 2, 2)
cat_win = df.groupby('time_category')['white_win'].mean()
sns.barplot(x=cat_win.index, y=cat_win.values, palette='coolwarm')
plt.ylabel('White win rate')
plt.title('White win rate by time control')

# Outlier game lengths
plt.subplot(2, 1, 2)
long_games = df[df['turns'] > df['turns'].quantile(0.95)]
short_games = df[df['turns'] < df['turns'].quantile(0.05)]
counts = [short_games.shape[0], long_games.shape[0]]
labels = ['Very short (<5th percentile)', 'Very long (>95th percentile)']
plt.bar(labels, counts, color=['gold', 'purple'])
plt.ylabel('Number of games')
plt.title('Outlier Game Counts')
for i, val in enumerate(counts):
    plt.text(i, val, str(val), ha='center', va='bottom')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('report_page3.png', dpi=300)
plt.close()

print('Pages saved:', ['report_page1.png', 'report_page2.png', 'report_page3.png'])
