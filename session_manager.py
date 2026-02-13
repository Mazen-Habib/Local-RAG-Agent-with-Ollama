"""
Session Manager
Handles conversation context and history per WhatsApp user
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from whatsapp_config import SESSION_TIMEOUT, MAX_SESSION_MESSAGES


@dataclass
class ConversationMessage:
    """Single message in a conversation"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class UserSession:
    """Session data for a single user"""
    user_id: str
    name: str
    messages: List[ConversationMessage] = field(default_factory=list)
    last_activity: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        message = ConversationMessage(role=role, content=content)
        self.messages.append(message)
        self.last_activity = time.time()
        
        # Keep only last N messages
        if len(self.messages) > MAX_SESSION_MESSAGES:
            self.messages = self.messages[-MAX_SESSION_MESSAGES:]
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history as list of dicts"""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]
    
    def is_expired(self) -> bool:
        """Check if session has expired"""
        return (time.time() - self.last_activity) > SESSION_TIMEOUT
    
    def clear(self):
        """Clear conversation history"""
        self.messages = []
        self.last_activity = time.time()


class SessionManager:
    """Manages user sessions for WhatsApp conversations"""
    
    def __init__(self):
        """Initialize session manager"""
        self.sessions: Dict[str, UserSession] = {}
        print("✅ Session manager initialized")
    
    def get_session(self, user_id: str, name: str = "User") -> UserSession:
        """
        Get or create a session for a user
        
        Args:
            user_id: WhatsApp user ID (phone number)
            name: User's name
            
        Returns:
            UserSession object
        """
        # Check if session exists and is not expired
        if user_id in self.sessions:
            session = self.sessions[user_id]
            
            if session.is_expired():
                print(f"♻️  Session expired for {user_id}, creating new session")
                session.clear()
            
            # Update last activity
            session.last_activity = time.time()
            session.name = name  # Update name if changed
            
            return session
        
        # Create new session
        print(f"🆕 Creating new session for {user_id}")
        session = UserSession(user_id=user_id, name=name)
        self.sessions[user_id] = session
        
        return session
    
    def add_user_message(self, user_id: str, message: str, name: str = "User"):
        """
        Add a user message to the session
        
        Args:
            user_id: User's WhatsApp ID
            message: User's message
            name: User's name
        """
        session = self.get_session(user_id, name)
        session.add_message("user", message)
        print(f"💬 User message added to session {user_id}")
    
    def add_assistant_message(self, user_id: str, message: str):
        """
        Add an assistant response to the session
        
        Args:
            user_id: User's WhatsApp ID
            message: Assistant's response
        """
        if user_id in self.sessions:
            session = self.sessions[user_id]
            session.add_message("assistant", message)
            print(f"🤖 Assistant message added to session {user_id}")
    
    def get_conversation_history(self, user_id: str) -> List[Dict[str, str]]:
        """
        Get conversation history for a user
        
        Args:
            user_id: User's WhatsApp ID
            
        Returns:
            List of message dictionaries
        """
        if user_id in self.sessions:
            return self.sessions[user_id].get_conversation_history()
        return []
    
    def clear_session(self, user_id: str):
        """
        Clear a user's session
        
        Args:
            user_id: User's WhatsApp ID
        """
        if user_id in self.sessions:
            self.sessions[user_id].clear()
            print(f"🗑️  Session cleared for {user_id}")
    
    def delete_session(self, user_id: str):
        """
        Delete a user's session completely
        
        Args:
            user_id: User's WhatsApp ID
        """
        if user_id in self.sessions:
            del self.sessions[user_id]
            print(f"🗑️  Session deleted for {user_id}")
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions"""
        expired_users = [
            user_id for user_id, session in self.sessions.items()
            if session.is_expired()
        ]
        
        for user_id in expired_users:
            del self.sessions[user_id]
        
        if expired_users:
            print(f"🧹 Cleaned up {len(expired_users)} expired session(s)")
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        return len(self.sessions)
    
    def get_session_info(self, user_id: str) -> Optional[Dict]:
        """
        Get information about a session
        
        Args:
            user_id: User's WhatsApp ID
            
        Returns:
            Session info dictionary or None
        """
        if user_id not in self.sessions:
            return None
        
        session = self.sessions[user_id]
        return {
            "user_id": session.user_id,
            "name": session.name,
            "message_count": len(session.messages),
            "last_activity": datetime.fromtimestamp(session.last_activity).strftime("%Y-%m-%d %H:%M:%S"),
            "is_expired": session.is_expired(),
            "session_age_minutes": (time.time() - session.last_activity) / 60
        }
    
    def get_all_sessions_info(self) -> List[Dict]:
        """Get information about all sessions"""
        return [
            self.get_session_info(user_id)
            for user_id in self.sessions.keys()
        ]


def test_session_manager():
    """Test session manager functionality"""
    print("\n" + "="*60)
    print("🧪 Testing Session Manager")
    print("="*60)
    
    manager = SessionManager()
    
    # Test 1: Create session
    print("\n1️⃣ Creating session...")
    manager.add_user_message("923335231335", "Hello!", "Test User")
    
    # Test 2: Add messages
    print("\n2️⃣ Adding messages...")
    manager.add_assistant_message("923335231335", "Hi! How can I help?")
    manager.add_user_message("923335231335", "What documents do you have?")
    
    # Test 3: Get history
    print("\n3️⃣ Getting conversation history...")
    history = manager.get_conversation_history("923335231335")
    print(f"   Messages in history: {len(history)}")
    for msg in history:
        print(f"   {msg['role']}: {msg['content']}")
    
    # Test 4: Session info
    print("\n4️⃣ Getting session info...")
    info = manager.get_session_info("923335231335")
    print(f"   User: {info['name']}")
    print(f"   Messages: {info['message_count']}")
    print(f"   Last activity: {info['last_activity']}")
    
    # Test 5: Multiple sessions
    print("\n5️⃣ Creating multiple sessions...")
    manager.add_user_message("111111111", "Test 1", "User 1")
    manager.add_user_message("222222222", "Test 2", "User 2")
    print(f"   Active sessions: {manager.get_active_sessions_count()}")
    
    # Test 6: Clear session
    print("\n6️⃣ Clearing session...")
    manager.clear_session("923335231335")
    history = manager.get_conversation_history("923335231335")
    print(f"   Messages after clear: {len(history)}")
    
    print("\n" + "="*60)
    print("✅ Session Manager Tests Complete")
    print("="*60)


if __name__ == "__main__":
    test_session_manager()
