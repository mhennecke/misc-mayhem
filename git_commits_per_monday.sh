#!/bin/bash

# Get the date of the initial commit
initial_commit_date=$(git log --reverse --format=%cs | head -n 1)

# Get the date of the last commit
last_commit_date=$(git log -1 --format=%cs)

# Convert dates to seconds since epoch (compatible with macOS)
initial_commit_seconds=$(date -j -f "%Y-%m-%d" "$initial_commit_date" "+%s")
last_commit_seconds=$(date -j -f "%Y-%m-%d" "$last_commit_date" "+%s")

# Calculate the number of seconds in a week
week_seconds=$((7 * 24 * 60 * 60))

# Initialize the current date to the initial commit date
current_date_seconds=$initial_commit_seconds

# Initialize the cumulative commit count
cumulative_commits=0

# Loop through each Monday from the initial commit date to the last commit date
while (( "$current_date_seconds" <= "$last_commit_seconds" )); do
    # Convert the current date in seconds to yyyy-mm-dd format (compatible with macOS)
    current_date=$(date -j -f "%s" "$current_date_seconds" "+%Y-%m-%d")

    # Count the cumulative number of commits up to the current date
    cumulative_commits=$(git rev-list --count --before="$current_date 23:59:59" HEAD)

    # Print the current date and the cumulative number of commits
    echo "$current_date $cumulative_commits"

    # Move to the next Monday
    current_date_seconds=$((current_date_seconds + week_seconds))
done
