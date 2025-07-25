monday_visitors = {"user1", "user2", "user3", "user4", "user5"}
tuesday_visitors = {"user2", "user4", "user6", "user7", "user8"}
wednesday_visitors = {"user1", "user3", "user6", "user9", "user10"}

# Find the total number of unique visitors who visited on any of the three days.
total_unique_visitors = monday_visitors.union(tuesday_visitors, wednesday_visitors)
print(f"Total unique visitors over the three days: {len(total_unique_visitors)}")

# Identify users who visited on both Monday and Tuesday.
common_monday_tuesday = monday_visitors.intersection(tuesday_visitors)
print(f"Users who visited on both Monday and Tuesday: {common_monday_tuesday}")

# Determine which users visited for the first time each day (i.e., not seen on previous days).
def first_time_visitors(monday, tuesday, wednesday):
    first_monday = monday - (tuesday.union(wednesday))
    first_tuesday = tuesday - (monday.union(wednesday))
    first_wednesday = wednesday - (monday.union(tuesday))
    
    print(f"First-time visitors on Monday: {first_monday}")
    print(f"First-time visitors on Tuesday: {first_tuesday}")
    print(f"First-time visitors on Wednesday: {first_wednesday}")

first_time_visitors(monday_visitors, tuesday_visitors, wednesday_visitors)

# Find users who visited the site on all three days.
all_three_days = monday_visitors.intersection(tuesday_visitors, wednesday_visitors)
print(f"Users who visited on all three days: {all_three_days}")

# Compare and print overlaps between each pair of days (e.g., Monday-Tuesday, Tuesday-Wednesday, etc.).

def compare_day_overlaps(monday, tuesday, wednesday):
    monday_tuesday_overlap = monday.intersection(tuesday)
    tuesday_wednesday_overlap = tuesday.intersection(wednesday)
    monday_wednesday_overlap = monday.intersection(wednesday)
    
    print(f"Overlap between Monday and Tuesday: {monday_tuesday_overlap}")
    print(f"Overlap between Tuesday and Wednesday: {tuesday_wednesday_overlap}")
    print(f"Overlap between Monday and Wednesday: {monday_wednesday_overlap}")

compare_day_overlaps(monday_visitors, tuesday_visitors, wednesday_visitors)