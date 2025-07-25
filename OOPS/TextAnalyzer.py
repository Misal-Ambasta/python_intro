from collections import Counter
import re

class TextAnalyzer:
    def __init__(self, text):
        """
        Initialize with text to analyze
        Args:
            text (str): Text to analyze
        """
        self.original_text = text
        self.text = text.lower()
        
    def get_character_frequency(self, include_spaces=False):
        """
        Get frequency of each character
        Args:
            include_spaces (bool): Whether to include spaces in count
        Returns:
            Counter: Character frequencies
        """
        if include_spaces:
            return Counter(self.text)
        else:
            return Counter(char for char in self.text if char != ' ')
    
    def get_word_frequency(self, min_length=1):
        """
        Get frequency of each word (minimum length filter)
        Args:
            min_length (int): Minimum word length to include
        Returns:
            Counter: Word frequencies
        """
        # Extract words using regex to handle punctuation
        words = re.findall(r'\b[a-zA-Z]+\b', self.text)
        return Counter(word for word in words if len(word) >= min_length)
    
    def get_sentence_length_distribution(self):
        """
        Analyze sentence lengths (in words)
        Returns:
            dict: Contains 'lengths' (Counter), 'average', 'longest', 'shortest'
        """
        # Split by sentence endings, clean up
        sentences = re.split(r'[.!?]+', self.original_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {
                'lengths': Counter(),
                'average': 0,
                'longest': 0,
                'shortest': 0
            }
        
        # Count words in each sentence
        sentence_lengths = []
        for sentence in sentences:
            words = re.findall(r'\b[a-zA-Z]+\b', sentence)
            sentence_lengths.append(len(words))
        
        return {
            'lengths': Counter(sentence_lengths),
            'average': sum(sentence_lengths) / len(sentence_lengths),
            'longest': max(sentence_lengths),
            'shortest': min(sentence_lengths)
        }
    
    def find_common_words(self, n=10, exclude_common=True):
        """
        Find most common words, optionally excluding very common English words
        Args:
            n (int): Number of words to return
            exclude_common (bool): Exclude common words like 'the', 'and', etc.
        Returns:
            list: List of tuples (word, count)
        """
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                       'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                       'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'him',
                       'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        word_freq = self.get_word_frequency()
        
        if exclude_common:
            # Filter out common words
            filtered_freq = {word: count for word, count in word_freq.items() 
                           if word not in common_words}
            return Counter(filtered_freq).most_common(n)
        else:
            return word_freq.most_common(n)
    
    def get_reading_statistics(self):
        """
        Get comprehensive reading statistics
        Returns:
            dict: Contains character_count, word_count, sentence_count,
                  average_word_length, reading_time_minutes (assume 200 WPM)
        """
        # Count characters (excluding spaces)
        char_count = len([c for c in self.text if c != ' '])
        
        # Count words
        words = re.findall(r'\b[a-zA-Z]+\b', self.text)
        word_count = len(words)
        
        # Count sentences
        sentences = re.split(r'[.!?]+', self.original_text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # Reading time (assuming 200 words per minute)
        reading_time = word_count / 200 if word_count > 0 else 0
        
        return {
            'character_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'average_word_length': avg_word_length,
            'reading_time_minutes': reading_time
        }
    
    def compare_with_text(self, other_text):
        """
        Compare this text with another text
        Args:
            other_text (str): Text to compare with
        Returns:
            dict: Contains 'common_words', 'similarity_score', 'unique_to_first', 'unique_to_second'
        """
        # Create analyzer for other text
        other_analyzer = TextAnalyzer(other_text)
        
        # Get word sets
        words1 = set(self.get_word_frequency().keys())
        words2 = set(other_analyzer.get_word_frequency().keys())
        
        # Find common and unique words
        common_words = words1.intersection(words2)
        unique_to_first = words1 - words2
        unique_to_second = words2 - words1
        
        # Calculate similarity score (Jaccard similarity)
        union_size = len(words1.union(words2))
        similarity_score = len(common_words) / union_size if union_size > 0 else 0
        
        return {
            'common_words': list(common_words),
            'similarity_score': similarity_score,
            'unique_to_first': list(unique_to_first),
            'unique_to_second': list(unique_to_second)
        }

# Test your implementation
sample_text = """
Python is a high-level, interpreted programming language with dynamic semantics.
Its high-level built-in data structures, combined with dynamic typing and dynamic binding,
make it very attractive for Rapid Application Development. Python is simple, easy to learn
syntax emphasizes readability and therefore reduces the cost of program maintenance.
Python supports modules and packages, which encourages program modularity and code reuse.
The Python interpreter and the extensive standard library are available in source or binary
form without charge for all major platforms, and can be freely distributed.
"""

analyzer = TextAnalyzer(sample_text)

print("Character frequency (top 5):", analyzer.get_character_frequency()[0:5])
print("Word frequency (top 5):", analyzer.get_word_frequency().most_common(5))
print("Common words:", analyzer.find_common_words(5))
print("Reading statistics:", analyzer.get_reading_statistics())

# Compare with another text
other_text = "Java is a programming language. Java is object-oriented and platform independent."
comparison = analyzer.compare_with_text(other_text)
print("Comparison results:", comparison)