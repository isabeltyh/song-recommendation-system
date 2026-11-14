"""
User Profile Manager
Manages user preferences and learning history.
"""

import json
import os
from typing import Dict, List
from datetime import datetime


class UserProfile:
    """
    Manages individual user profiles including preferences and learning history.
    """
    
    def __init__(self, user_id: str, profiles_dir: str = "data/profiles"):
        """
        Initialize or load a user profile.
        
        Args:
            user_id: Unique identifier for the user
            profiles_dir: Directory to store user profiles
        """
        self.user_id = user_id
        self.profiles_dir = profiles_dir
        self.profile_path = os.path.join(profiles_dir, f"{user_id}.json")
        
        # Create profiles directory if it doesn't exist
        os.makedirs(profiles_dir, exist_ok=True)
        
        # Initialize or load profile
        self.profile = self._load_or_create_profile()
    
    def _load_or_create_profile(self) -> Dict:
        """Load existing profile or create a new one."""
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "user_id": self.user_id,
                "created_at": datetime.now().isoformat(),
                "preferences": {
                    "subject": "programming",
                    "difficulty": "beginner",
                    "format": "mixed",
                    "tags": []
                },
                "learning_history": [],
                "completed_resources": [],
                "bookmarks": []
            }
    
    def set_preferences(self, preferences: Dict):
        """
        Update user preferences.
        
        Args:
            preferences: Dictionary with keys like subject, difficulty, format, tags
        """
        self.profile["preferences"].update(preferences)
        self.save()
    
    def get_preferences(self) -> Dict:
        """Get current user preferences."""
        return self.profile.get("preferences", {})
    
    def add_to_learning_history(self, resource_id: str, action: str = "viewed"):
        """
        Add an entry to the user's learning history.
        
        Args:
            resource_id: ID of the resource
            action: Type of action (viewed, started, completed, rated)
        """
        entry = {
            "resource_id": resource_id,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        self.profile["learning_history"].append(entry)
        self.save()
    
    def mark_resource_completed(self, resource_id: str):
        """Mark a resource as completed."""
        if resource_id not in self.profile["completed_resources"]:
            self.profile["completed_resources"].append(resource_id)
            self.add_to_learning_history(resource_id, "completed")
    
    def bookmark_resource(self, resource_id: str):
        """Add a resource to bookmarks."""
        if resource_id not in self.profile["bookmarks"]:
            self.profile["bookmarks"].append(resource_id)
            self.save()
    
    def unbookmark_resource(self, resource_id: str):
        """Remove a resource from bookmarks."""
        if resource_id in self.profile["bookmarks"]:
            self.profile["bookmarks"].remove(resource_id)
            self.save()
    
    def get_bookmarks(self) -> List[str]:
        """Get list of bookmarked resource IDs."""
        return self.profile.get("bookmarks", [])
    
    def get_completed_resources(self) -> List[str]:
        """Get list of completed resource IDs."""
        return self.profile.get("completed_resources", [])
    
    def get_learning_history(self, limit: int = None) -> List[Dict]:
        """Get user's learning history."""
        history = self.profile.get("learning_history", [])
        if limit:
            return history[-limit:]
        return history
    
    def save(self):
        """Save profile to file."""
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=4)
    
    def get_profile_summary(self) -> Dict:
        """Get a summary of the user profile."""
        return {
            "user_id": self.user_id,
            "preferences": self.profile.get("preferences", {}),
            "total_resources_viewed": len(self.profile.get("learning_history", [])),
            "completed_resources": len(self.profile.get("completed_resources", [])),
            "bookmarks": len(self.profile.get("bookmarks", []))
        }
