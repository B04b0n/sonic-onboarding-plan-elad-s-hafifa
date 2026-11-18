import pandas as pd
import numpy as np

print(pd.__version__)

# ============================================================
# PART 1: LOAD AND EXPLORE
# ============================================================

# Step 1: Load the CSV
df = pd.read_csv('events_raw.csv')

# Step 2: Initial exploration
print("=" * 60)
print("PART 1: LOAD AND EXPLORE")
print("=" * 60)
print(f"Original shape: {df.shape}")
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
print(f"\nColumn names: {list(df.columns)}")

print("\nFirst 5 rows:")
print(df.head())

print("\n\nData Info:")
print(df.info())

print("\n\nMissing Values Summary:")
print(df.isnull().sum())

# Step 3: Examine columns
print("\n\nUnique Event Types (with counts):")
print(df['event_type'].value_counts(dropna=False))

print("\n\nUnique Statuses (with counts):")
print(df['status'].value_counts(dropna=False))

print("\n\nLatency_ms column sample:")
print(df['latency_ms'].value_counts(dropna=False).head(15))

# Check data types issue
print(f"\n\nLatency dtype: {df['latency_ms'].dtype}")


# ============================================================
# PART 2: DATA CLEANING
# ============================================================

print("\n\n" + "=" * 60)
print("PART 2: DATA CLEANING")
print("=" * 60)

# Store original count
original_count = len(df)
print(f"Original row count: {original_count}")

# Step 4: Fix data types
print("\n\nStep 4: Converting data types...")

df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df['latency_ms'] = pd.to_numeric(df['latency_ms'], errors='coerce')
df['event_id'] = df['event_id'].astype('int64')

print("✓ Converted timestamp to datetime")
print("✓ Converted latency_ms to numeric")
print(f"  (Invalid latencies became NaN: {df['latency_ms'].isnull().sum()})")
print("✓ Converted event_id to int64")

# Step 5: Handle missing values
print("\n\nStep 5: Handling missing values...")

# Before dropping
before_drop = len(df)
print(f"Before cleaning: {before_drop} rows")

# Drop rows with missing critical fields
df = df.dropna(subset=['event_id', 'timestamp', 'event_type'])

after_drop = len(df)
dropped = before_drop - after_drop
print(f"After dropping missing critical fields: {after_drop} rows")
print(f"  (Dropped {dropped} rows with missing event_id, timestamp, or event_type)")

# Fill missing values in optional columns
print(f"\nBefore filling optional fields: {df['status'].isnull().sum()} missing status")
df['status'] = df['status'].fillna('unknown')
print(f"After filling: {df['status'].isnull().sum()} missing status")

print(f"\nBefore filling latency: {df['latency_ms'].isnull().sum()} missing latency")
# Option 1: Fill with mean (better for analysis)
df['latency_ms'] = df['latency_ms'].fillna(df['latency_ms'].mean())
print(f"After filling with mean: {df['latency_ms'].isnull().sum()} missing latency")

# Step 6: Remove duplicates
print("\n\nStep 6: Removing duplicates...")
before_dedup = len(df)
df = df.drop_duplicates()
after_dedup = len(df)
duplicates_removed = before_dedup - after_dedup
print(f"Before removing duplicates: {before_dedup} rows")
print(f"After removing duplicates: {after_dedup} rows")
print(f"  (Removed {duplicates_removed} duplicate rows)")

# Step 7: Validate event types
print("\n\nStep 7: Validating event types...")
valid_event_types = {"purchase", "login", "checkout", "view"}
unique_types = set(df['event_type'].dropna().unique())
invalid_types = unique_types - valid_event_types

if invalid_types:
    print(f"Found invalid event types: {invalid_types}")
    print(f"  Removing {len(df[df['event_type'].isin(invalid_types)])} rows with invalid types")
    df = df[df['event_type'].isin(valid_event_types)]
else:
    print("✓ All event types are valid")

# Step 8: Validate status values
print("\n\nStep 8: Validating status values...")
valid_statuses = {"ok", "error", "timeout", "unknown"}
current_statuses = set(df['status'].unique())
invalid_statuses = current_statuses - valid_statuses

if invalid_statuses:
    print(f"Found invalid statuses: {invalid_statuses}")
    print(f"  Removing {len(df[df['status'].isin(invalid_statuses)])} rows with invalid statuses")
    df = df[df['status'].isin(valid_statuses)]
else:
    print("✓ All statuses are valid")

print(f"\n\nFinal row count after cleaning: {len(df)}")


# ============================================================
# PART 3: DATA QUALITY CHECKS
# ============================================================

print("\n\n" + "=" * 60)
print("PART 3: DATA QUALITY CHECKS")
print("=" * 60)

# Step 9: Verify data quality
print("\nData Quality Summary:")
print(df.info())

print("\n\nMissing Values (should be minimal):")
print(df.isnull().sum())

print("\n\nNumeric Summary:")
print(df.describe())

# Check timestamp range
print("\n\nTimestamp Range:")
print(f"Earliest: {df['timestamp'].min()}")
print(f"Latest: {df['timestamp'].max()}")

# Step 10: Show cleaning impact
print("\n\nCleaning Impact Summary:")
print("=" * 40)
print(f"Original row count:    {original_count}")
print(f"Final row count:       {len(df)}")
print(f"Rows removed:          {original_count - len(df)}")
print(f"Data retained:         {len(df)/original_count*100:.1f}%")
print(f"Data removed:          {(1 - len(df)/original_count)*100:.1f}%")


# ============================================================
# PART 4: ANSWER BUSINESS QUESTIONS
# ============================================================

print("\n\n" + "=" * 60)
print("PART 4: BUSINESS QUESTIONS")
print("=" * 60)

# Step 11: Calculate key metrics
total_events = len(df)
error_count = (df['status'] == 'error').sum()
error_rate = (error_count / total_events) * 100

print(f"\n1. Total Event Volume: {total_events:,} events")

print(f"\n2. Error Rate: {error_rate:.2f}%")
print(f"   Error events: {error_count}")
print(f"   Success events: {total_events - error_count}")

print(f"\n3. Events by Event Type:")
event_type_counts = df['event_type'].value_counts()
for event_type, count in event_type_counts.items():
    pct = (count / total_events) * 100
    print(f"   {event_type}: {count} events ({pct:.1f}%)")

print(f"\n4. Events by Status:")
status_counts = df['status'].value_counts()
for status, count in status_counts.items():
    pct = (count / total_events) * 100
    print(f"   {status}: {count} events ({pct:.1f}%)")

print(f"\n5. Average Latency by Event Type:")
avg_latency_by_type = df.groupby('event_type')['latency_ms'].mean().sort_values(ascending=False)
for event_type, avg_latency in avg_latency_by_type.items():
    print(f"   {event_type}: {avg_latency:.2f} ms")

# Step 12: Identify insights
print("\n\n" + "=" * 60)
print("PART 5: KEY INSIGHTS")
print("=" * 60)

# Error rate by event type
print("\nError Rate by Event Type:")
for event_type in df['event_type'].unique():
    subset = df[df['event_type'] == event_type]
    error_pct = (subset['status'] == 'error').sum() / len(subset) * 100
    print(f"  {event_type}: {error_pct:.2f}%")

# Slowest event types
print("\nSlowest Event Types (by average latency):")
slowest = df.groupby('event_type')['latency_ms'].agg(['mean', 'max', 'count']).sort_values('mean', ascending=False)
print(slowest)

# Most common event type
most_common = df['event_type'].value_counts().index[0]
most_common_pct = (df['event_type'] == most_common).sum() / total_events * 100
print(f"\nMost Common Event Type: {most_common} ({most_common_pct:.1f}% of events)")


# ============================================================
# PART 5: SAVE AND REPORT
# ============================================================

print("\n\n" + "=" * 60)
print("PART 5: SAVE AND REPORT")
print("=" * 60)

# Step 13: Save cleaned data
df.to_csv('events_cleaned.csv', index=False)
print("✓ Saved cleaned data to events_cleaned.csv")

# Step 14: Verification
df_verify = pd.read_csv('events_cleaned.csv')
print(f"✓ Verified saved file has {len(df_verify)} rows")

# Final report
print("\n\nFinal Data Quality Report:")
print("=" * 40)
print(f"Total events: {len(df):,}")
print(f"Complete records: {(df.isnull().sum() == 0).sum()} / {len(df.columns)} columns")
print(f"Error rate: {error_rate:.2f}%")
print(f"Slowest event: {avg_latency_by_type.index[0]}")
print(f"Data quality: {'✓ GOOD' if original_count - len(df) < original_count * 0.2 else '⚠ CHECK'}")
