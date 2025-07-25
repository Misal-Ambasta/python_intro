def analyze_friendships():    
    """
    Analyze friendships across multiple social media platforms.
    """
    # User friends on different platforms
    facebook_friends = {"alice", "bob", "charlie", "diana", "eve", "frank"}
    instagram_friends = {"bob", "charlie", "grace", "henry", "alice", "ivan"}
    twitter_friends = {"alice", "diana", "grace", "jack", "bob", "karen"}
    linkedin_friends = {"charlie", "diana", "frank", "grace", "luke", "mary"}

    # Your tasks:
    # 1. Find friends who are on ALL four platforms
    all_platforms = facebook_friends & instagram_friends & twitter_friends & linkedin_friends
    # 2. Find friends who are ONLY on Facebook (not on any other platform)
    facebook_only = facebook_friends - (instagram_friends | twitter_friends | linkedin_friends)
    # 3. Find friends who are on Instagram OR Twitter but NOT on both
    instagram_or_twitter = (instagram_friends | twitter_friends) - (instagram_friends & twitter_friends)
    # 4. Find the total unique friends across all platforms
    unique_friends = facebook_friends | instagram_friends | twitter_friends | linkedin_friends
    total_unique = len(unique_friends)
    # 5. Find friends who are on exactly 2 platforms
    from collections import Counter
    all_friends = list(facebook_friends) + list(instagram_friends) + list(twitter_friends) + list(linkedin_friends)
    counts = Counter(all_friends)
    exactly_two_platforms = {friend for friend, count in counts.items() if count == 2}

    # Return a dictionary with all results
    return {
        "all_platforms": all_platforms,
        "facebook_only": facebook_only,
        "instagram_xor_twitter": instagram_or_twitter,
        "total_unique": total_unique,
        "exactly_two_platforms": exactly_two_platforms
    }

# Test your function
result = analyze_friendships()
print("All platforms:", result.get('all_platforms'))
print("Facebook only:", result.get('facebook_only'))
print("Instagram XOR Twitter:", result.get('instagram_xor_twitter'))
print("Total unique friends:", result.get('total_unique'))
print("Exactly 2 platforms:", result.get('exactly_two_platforms'))
