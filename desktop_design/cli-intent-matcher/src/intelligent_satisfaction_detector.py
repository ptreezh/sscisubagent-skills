import re
from typing import Dict, List, Optional, Tuple
from .satisfaction_tracker import SatisfactionTracker


class FollowUpAnalyzer:
    """
    Analyzes user follow-up conversations to intelligently detect satisfaction.
    """
    
    def __init__(self, tracker: SatisfactionTracker):
        self.tracker = tracker
        # Define patterns that indicate dissatisfaction
        self.dissatisfaction_patterns = [
            # Negative sentiment patterns
            r"(not|don't|doesn't|did not|didnt|cant|can't|won't|will not).*work",
            r"(bad|poor|terrible|awful|horrible|useless|worthless|failed|fail|wrong|incorrect)",
            r"(fix|change|redo|restart|try again|retry|different|alternative)",
            r"(still|yet|again|repeat|repeating).*not",
            r"(error|problem|issue|bug|broken|crash|stuck|hang|frozen)",
            r"(frustrated|annoyed|disappointed|upset|mad|angry|irritated)",
            r"(no good|no use|no help|not helpful|not useful|pointless|waste of time)",
            r"(need help|help me|assistance|support|troubleshoot|debug|troubleshooting)",
            # Command adjustment patterns
            r"(modify|update|adjust|tweak|tune|optimize|improve|enhance).*command",
            r"(add|include|append|extend|expand).*parameter",
            r"(remove|delete|exclude|omit).*parameter",
            r"(change|switch|replace|substitute).*model|tool|skill|agent",
            r"(try|use|run).*different|other|alternative",
            # Negative response patterns
            r"(no,?|nope|nah|not really|not exactly|not quite|not quite right|partially)",
            r"(close|close enough|almost|nearly|sort of|kind of|somewhat).*but",
            r"(yes,? but|yeah,? but|true,? but|correct,? but)",
        ]
        
        # Define patterns that indicate satisfaction
        self.satisfaction_patterns = [
            r"(good|great|excellent|amazing|wonderful|fantastic|perfect|awesome)",
            r"(thank you|thanks|appreciate|grateful|appreciated)",
            r"(works|working|work well|perfect|exactly|exactly right|just right)",
            r"(continue|proceed|go ahead|carry on|move forward|next step)",
            r"(yes,?|yep|yeah|yup|correct|right|exactly|perfect|exactly what i wanted)",
            r"(nice|beautiful|elegant|clean|simple|straightforward|easy|clear)",
        ]
    
    def analyze_follow_up(self, original_conversation_id: str, follow_up_input: str) -> Tuple[Optional[int], str]:
        """
        Analyze follow-up input to determine satisfaction level.
        Returns (satisfaction_score, reason) or (None, reason) if inconclusive.
        """
        # Check for dissatisfaction patterns
        for pattern in self.dissatisfaction_patterns:
            if re.search(pattern, follow_up_input, re.IGNORECASE):
                # Determine score based on pattern strength
                if any(keyword in follow_up_input.lower() for keyword in 
                      ["error", "problem", "issue", "bug", "broken", "crash", "failed", "wrong", "incorrect"]):
                    return 1, f"Detected strong dissatisfaction pattern: {pattern}"
                elif any(keyword in follow_up_input.lower() for keyword in 
                        ["not work", "doesn't work", "fix", "change", "redo", "try again"]):
                    return 2, f"Detected dissatisfaction pattern: {pattern}"
                else:
                    return 2, f"Detected dissatisfaction pattern: {pattern}"
        
        # Check for satisfaction patterns
        for pattern in self.satisfaction_patterns:
            if re.search(pattern, follow_up_input, re.IGNORECASE):
                if any(keyword in follow_up_input.lower() for keyword in 
                      ["thank you", "thanks", "perfect", "exactly", "works", "working well"]):
                    return 5, f"Detected strong satisfaction pattern: {pattern}"
                else:
                    return 4, f"Detected satisfaction pattern: {pattern}"
        
        # Check for command adjustment patterns (usually indicate dissatisfaction)
        adjustment_patterns = [
            r"add.*parameter",
            r"change.*parameter", 
            r"use.*different",
            r"try.*different",
            r"modify.*command",
            r"update.*command"
        ]
        
        for pattern in adjustment_patterns:
            if re.search(pattern, follow_up_input, re.IGNORECASE):
                return 2, f"Detected command adjustment request: {pattern}"
        
        # If no clear pattern found, return None (inconclusive)
        return None, "No clear satisfaction/dissatisfaction pattern detected"
    
    def detect_satisfaction_from_conversation_flow(self, conversation_id: str, follow_up_inputs: List[str]) -> Optional[int]:
        """
        Analyze multiple follow-up inputs to determine overall satisfaction.
        """
        satisfaction_scores = []
        reasons = []
        
        for follow_up in follow_up_inputs:
            score, reason = self.analyze_follow_up(conversation_id, follow_up)
            if score is not None:
                satisfaction_scores.append(score)
                reasons.append(reason)
        
        if not satisfaction_scores:
            return None
        
        # Calculate average satisfaction, but be sensitive to strong negative signals
        avg_score = sum(satisfaction_scores) / len(satisfaction_scores)
        
        # If any response was strongly negative (score 1), return 1
        if 1 in satisfaction_scores:
            return 1
        
        # Round to nearest integer
        return round(avg_score)
    
    def process_conversation_sequence(self, original_conversation_id: str, follow_up_sequence: List[str]):
        """
        Process a sequence of follow-up conversations and update satisfaction if needed.
        """
        conversation = None
        for conv in self.tracker.conversation_data:
            if conv["id"] == original_conversation_id:
                conversation = conv
                break
        
        if not conversation:
            return False
        
        # Skip if feedback already exists
        if conversation.get("feedback") is not None:
            return False
        
        # Analyze follow-up sequence
        satisfaction_score = self.detect_satisfaction_from_conversation_flow(
            original_conversation_id, follow_up_sequence
        )
        
        if satisfaction_score is not None:
            reason = f"Auto-detected from follow-up conversation sequence (score: {satisfaction_score})"
            self.tracker.add_satisfaction_feedback(original_conversation_id, satisfaction_score, reason)
            conversation["follow_up_analyzed"] = True
            self.tracker.save_conversation_data()
            return True
        
        return False


class IntelligentSatisfactionDetector:
    """
    Main class for intelligent satisfaction detection based on conversation patterns.
    """
    
    def __init__(self, tracker: SatisfactionTracker):
        self.tracker = tracker
        self.analyzer = FollowUpAnalyzer(tracker)
        self.pending_follow_ups = {}  # conversation_id -> list of follow_up_inputs
    
    def register_follow_up(self, original_conversation_id: str, follow_up_input: str):
        """
        Register a follow-up input for later analysis.
        """
        if original_conversation_id not in self.pending_follow_ups:
            self.pending_follow_ups[original_conversation_id] = []
        
        self.pending_follow_ups[original_conversation_id].append(follow_up_input)
    
    def analyze_and_update_satisfaction(self, conversation_id: str = None):
        """
        Analyze all pending follow-ups or a specific conversation and update satisfaction.
        """
        if conversation_id:
            # Analyze specific conversation
            if conversation_id in self.pending_follow_ups:
                follow_ups = self.pending_follow_ups[conversation_id]
                result = self.analyzer.process_conversation_sequence(conversation_id, follow_ups)
                if result:
                    del self.pending_follow_ups[conversation_id]
                return result
        else:
            # Analyze all pending conversations
            completed = []
            for conv_id, follow_ups in self.pending_follow_ups.items():
                result = self.analyzer.process_conversation_sequence(conv_id, follow_ups)
                if result:
                    completed.append(conv_id)
            
            # Remove completed conversations
            for conv_id in completed:
                del self.pending_follow_ups[conv_id]
            
            return len(completed) > 0
    
    def get_satisfaction_insights(self) -> Dict:
        """
        Get insights about satisfaction detection patterns.
        """
        total_conversations = len(self.tracker.conversation_data)
        conversations_with_feedback = len([c for c in self.tracker.conversation_data if c.get("feedback")])
        auto_detected_count = len([c for c in self.tracker.conversation_data 
                                 if c.get("feedback") and "Auto-detected" in c["feedback"].get("feedback_text", "")])
        
        return {
            "total_conversations": total_conversations,
            "conversations_with_feedback": conversations_with_feedback,
            "auto_detected_satisfaction": auto_detected_count,
            "pending_follow_ups": len(self.pending_follow_ups)
        }