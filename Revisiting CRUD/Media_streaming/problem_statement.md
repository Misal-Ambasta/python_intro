# Q: 1 - Media Streaming Platform with Abstraction & Polymorphism

## Problem Statement
Create a comprehensive media streaming platform that handles different types of media content (Movies, TV Shows, Podcasts, Music) using abstract base classes and polymorphism. The system should manage user subscriptions, content recommendations, and playbook functionality.

## Requirements

### Abstract Base Classes:

#### MediaContent(ABC): Base class for all media types
- **Abstract methods**: `play()`, `get_duration()`, `get_file_size()`, `calculate_streaming_cost()`
- **Concrete methods**: `add_rating()`, `get_average_rating()`, `is_premium_content()`

#### StreamingDevice(ABC): Base class for different devices
- **Abstract methods**: `connect()`, `stream_content()`, `adjust_quality()`
- **Concrete methods**: `get_device_info()`, `check_compatibility()`

### Concrete Classes:

#### Media Content Types:
- **Movie**: Has duration, resolution, genre, director
- **TVShow**: Has episodes, seasons, current_episode
- **Podcast**: Has episode_number, transcript_available
- **Music**: Has artist, album, lyrics_available

#### Streaming Devices:
- **SmartTV**: Large screen, 4K support, surround sound
- **Laptop**: Medium screen, headphone support
- **Mobile**: Small screen, battery optimization
- **SmartSpeaker**: Audio only, voice control

### Additional Classes:
- **User**: Manages subscription, watch history, preferences
- **StreamingPlatform**: Orchestrates everything using polymorphism

## Advanced Features to Implement
- Content recommendation engine based on user preferences
- Subscription tier management (Free, Premium, Family)
- Device-specific quality optimization
- Parental controls and content filtering
- Watch time analytics and reporting