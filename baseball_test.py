import pybaseball as pyb
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

pyb.cache.enable()
print("Fetching Statcast data...")

# 1. Pull Data & Define States
data = pyb.statcast(start_dt='2024-03-28', end_dt='2024-04-03')
markov_df = data[['game_date', 'game_pk', 'at_bat_number', 'pitch_number', 'events', 'balls', 'strikes']].copy()
markov_df = markov_df.sort_values(by=['game_pk', 'at_bat_number', 'pitch_number'])
markov_df['count_state'] = markov_df['balls'].astype(str) + '-' + markov_df['strikes'].astype(str)
markov_df['next_state'] = markov_df.groupby(['game_pk', 'at_bat_number'])['count_state'].shift(-1)
markov_df['next_state'] = markov_df['next_state'].fillna(markov_df['events'])

# 2. Build the Transition Matrix
transition_matrix = pd.crosstab(markov_df['count_state'], markov_df['next_state'], normalize='index').fillna(0)

# 3. DEFINE THE RUN VALUES (Linear Weights)
# We assign standard baseball run values to the events that end an at-bat
run_values = {
    'single': 0.47, 'double': 0.77, 'triple': 1.04, 'home_run': 1.40,
    'walk': 0.32, 'hit_by_pitch': 0.33,
    'strikeout': -0.28, 'field_out': -0.28, 'force_out': -0.28,
    'grounded_into_dp': -0.45, 'strikeout_double_play': -0.45,
    'sac_fly': -0.03, 'fielders_choice': -0.28
}

# 4. RUN THE VALUE ITERATION
# This loop mathematically "folds" the event values back into the pitch counts
expected_values = pd.Series(0.0, index=transition_matrix.index)

for _ in range(15):
    new_values = pd.Series(0.0, index=transition_matrix.index)
    for count in transition_matrix.index:
        expected_run = 0
        for next_state, prob in transition_matrix.loc[count].items():
            if prob == 0: continue
            
            if next_state in expected_values.index:
                expected_run += prob * expected_values[next_state]
            else:
                expected_run += prob * run_values.get(next_state, 0.0)
                
        new_values[count] = expected_run
    expected_values = new_values

print("\n--- EXPECTED RUN VALUE OF EVERY PITCH COUNT ---")
print(expected_values.sort_values(ascending=False).round(3))
