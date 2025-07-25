from collections import Counter

posts = [
    {"id": 1, "user": "alice", "content": "Love Python programming!", "likes": 15, "tags": ["python", "coding"]},
    {"id": 2, "user": "bob", "content": "Great weather today", "likes": 8, "tags": ["weather", "life"]},
    {"id": 3, "user": "alice", "content": "Data structures are fun", "likes": 22, "tags": ["python", "learning"]},
]

users = {
    "alice": {"followers": 150, "following": 75},
    "bob": {"followers": 89, "following": 120},
}

# Use collections.Counter to find the most frequent tags across posts
def most_frequent_tags(posts):
    tag_counter = Counter()
    for post in posts:
        tag_counter.update(post["tags"])
    return tag_counter.most_common()

print("Most frequent tags:", most_frequent_tags(posts))

# Use defaultdict to compute total likes per user.
from collections import defaultdict
def total_likes_per_user(posts):
    likes_counter = defaultdict(int)
    for post in posts:
        likes_counter[post["user"]] += post["likes"]
    return likes_counter

print("Total likes per user:", total_likes_per_user(posts))

# Use sorted() to list posts in descending order of likes.
def posts_by_likes(posts):
    return sorted(posts, key=lambda x: x["likes"], reverse=True)

print("Posts sorted by likes:", posts_by_likes(posts))

# Combine post and user data to generate a summary per user (posts count, likes, followers, etc.).
def user_summary(posts, users):
    summary = {}
    for post in posts:
        user = post["user"]
        if user not in summary:
            summary[user] = {
                "posts_count": 0,
                "total_likes": 0,
                "followers": users[user]["followers"],
                "following": users[user]["following"]
            }
        summary[user]["posts_count"] += 1
        summary[user]["total_likes"] += post["likes"]
    
    return summary
