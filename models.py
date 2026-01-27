# models.py
from datetime import datetime
import uuid


class FAQ:
    """Encapsulation: FAQ knowledge base (Abstraction of support content)."""
    def __init__(self, faq_id, question, answer, category):
        self.faq_id = faq_id
        self.question = question
        self.answer = answer
        self.category = category  # billing, account, product, technical
        self.created_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        return {
            "faq_id": self.faq_id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "created_date": self.created_date
        }


class KnowledgeBaseArticle:
    """Encapsulation: Knowledge base articles for troubleshooting."""
    def __init__(self, article_id, title, content, category, difficulty):
        self.article_id = article_id
        self.title = title
        self.content = content
        self.category = category  # troubleshooting, tutorial, guide
        self.difficulty = difficulty  # beginner, intermediate, advanced
        self.created_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        return {
            "article_id": self.article_id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "difficulty": self.difficulty,
            "created_date": self.created_date
        }


class SupportTicket:
    """Encapsulation: Customer support ticket with full submission details."""
    def __init__(self, name, email, issue_type, description, phone=""):
        self.ticket_id = str(uuid.uuid4())[:8].upper()
        self.name = name
        self.email = email
        self.phone = phone
        self.issue_type = issue_type  # billing, technical, account, general
        self.description = description
        self.status = "Open"
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "issue_type": self.issue_type,
            "description": self.description,
            "status": self.status,
            "created_date": self.created_date
        }


class StatusUpdate:
    """Encapsulation: Service status and maintenance updates."""
    def __init__(self, update_id, title, message, status_type, severity):
        self.update_id = update_id
        self.title = title
        self.message = message
        self.status_type = status_type  # operational, maintenance, degraded, outage
        self.severity = severity  # low, medium, high, critical
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            "update_id": self.update_id,
            "title": self.title,
            "message": self.message,
            "status_type": self.status_type,
            "severity": self.severity,
            "created_date": self.created_date
        }
