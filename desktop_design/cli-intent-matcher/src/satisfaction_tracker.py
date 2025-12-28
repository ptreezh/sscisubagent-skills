import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class SatisfactionTracker:
    """
    Tracks user satisfaction with CLI intent matching and provides feedback collection.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.feedback_file = os.path.join(data_dir, "satisfaction_feedback.json")
        self.conversation_file = os.path.join(data_dir, "conversations.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize feedback and conversation data
        self.feedback_data = self._load_feedback_data()
        self.conversation_data = self._load_conversation_data()
    
    def _load_feedback_data(self) -> List[Dict]:
        """Load existing satisfaction feedback data."""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                return []
        return []
    
    def _load_conversation_data(self) -> List[Dict]:
        """Load existing conversation data."""
        if os.path.exists(self.conversation_file):
            try:
                with open(self.conversation_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                return []
        return []
    
    def save_feedback_data(self):
        """Save satisfaction feedback data to file."""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
    
    def save_conversation_data(self):
        """Save conversation data to file."""
        with open(self.conversation_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_data, f, ensure_ascii=False, indent=2)
    
    def add_conversation(self, user_input: str, cli_intent: str, cli_command: str, timestamp: Optional[float] = None) -> str:
        """Add a conversation entry with a unique ID."""
        if timestamp is None:
            timestamp = time.time()
        
        conversation_id = f"conv_{int(timestamp)}_{len(self.conversation_data)}"
        
        conversation_entry = {
            "id": conversation_id,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "user_input": user_input,
            "cli_intent": cli_intent,
            "cli_command": cli_command,
            "feedback": None,
            "satisfaction_score": None,
            "follow_up_analyzed": False
        }
        
        self.conversation_data.append(conversation_entry)
        self.save_conversation_data()
        
        return conversation_id
    
    def add_satisfaction_feedback(self, conversation_id: str, satisfaction_score: int, feedback_text: str = ""):
        """Add satisfaction feedback for a conversation."""
        if satisfaction_score < 1 or satisfaction_score > 5:
            raise ValueError("Satisfaction score must be between 1 and 5")
        
        # Find the conversation
        conversation = None
        for conv in self.conversation_data:
            if conv["id"] == conversation_id:
                conversation = conv
                break
        
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        # Add feedback to conversation
        feedback_entry = {
            "conversation_id": conversation_id,
            "timestamp": time.time(),
            "satisfaction_score": satisfaction_score,
            "feedback_text": feedback_text,
            "datetime": datetime.fromtimestamp(time.time()).isoformat()
        }
        
        conversation["feedback"] = feedback_entry
        conversation["satisfaction_score"] = satisfaction_score
        
        # Add to feedback data
        self.feedback_data.append(feedback_entry)
        self.save_feedback_data()
        self.save_conversation_data()
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations sorted by timestamp."""
        sorted_convs = sorted(self.conversation_data, key=lambda x: x["timestamp"], reverse=True)
        return sorted_convs[:limit]
    
    def get_unsatisfied_conversations(self) -> List[Dict]:
        """Get conversations with low satisfaction scores (1-2) or no feedback."""
        unsatisfied = []
        for conv in self.conversation_data:
            if conv.get("satisfaction_score") is not None and conv["satisfaction_score"] <= 2:
                unsatisfied.append(conv)
            elif conv.get("satisfaction_score") is None:
                unsatisfied.append(conv)
        return unsatisfied
    
    def calculate_overall_satisfaction(self) -> float:
        """Calculate overall satisfaction score based on all feedback."""
        if not self.feedback_data:
            return 0.0
        
        total_score = sum(feedback["satisfaction_score"] for feedback in self.feedback_data)
        return total_score / len(self.feedback_data)
    
    def get_satisfaction_trends(self) -> Dict[str, float]:
        """Get satisfaction trends over time."""
        if not self.feedback_data:
            return {}
        
        # Calculate average satisfaction by day
        daily_scores = {}
        for feedback in self.feedback_data:
            date = feedback["datetime"][:10]  # Extract date part
            if date not in daily_scores:
                daily_scores[date] = []
            daily_scores[date].append(feedback["satisfaction_score"])
        
        daily_averages = {date: sum(scores) / len(scores) for date, scores in daily_scores.items()}
        return daily_averages


class SatisfactionFeedbackInterface:
    """
    Interface for collecting user satisfaction feedback.
    """
    
    def __init__(self, tracker: SatisfactionTracker):
        self.tracker = tracker
    
    def request_satisfaction_feedback(self, conversation_id: str) -> Optional[int]:
        """Request satisfaction feedback from user (simulated interface)."""
        print(f"\n--- Satisfaction Feedback Request ---")
        print(f"Conversation ID: {conversation_id}")
        print("How satisfied are you with the CLI command suggestion?")
        print("1 - Very Dissatisfied")
        print("2 - Dissatisfied") 
        print("3 - Neutral")
        print("4 - Satisfied")
        print("5 - Very Satisfied")
        print("-----------------------------------")
        
        # In a real implementation, this would wait for user input
        # For now, we'll return None to indicate no feedback given
        return None
    
    def collect_feedback_from_user(self, conversation_id: str) -> bool:
        """Collect feedback from user and add to tracker."""
        try:
            satisfaction_score = self.request_satisfaction_feedback(conversation_id)
            if satisfaction_score is not None:
                feedback_text = input("Please provide additional feedback (optional): ")
                self.tracker.add_satisfaction_feedback(conversation_id, satisfaction_score, feedback_text)
                return True
        except (ValueError, KeyboardInterrupt):
            print("Feedback collection cancelled.")
        return False