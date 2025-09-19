#!/usr/bin/env python3
"""
Secure configuration management for Bank of Anthos AI Agents
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class that securely manages environment variables"""
    
    def __init__(self):
        # Gemini AI API Key - DO NOT HARDCODE IN PRODUCTION
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyCeizzUpE6L6b4-WPYCQoCVoSkVAYEV3Rw')
        
        # MCP Configuration
        self.MCP_API_KEY = os.getenv('MCP_API_KEY', 'mcp-demo-key-123')
        
        # Service URLs
        self.BALANCEREADER_URL = os.getenv('BALANCEREADER_URL', 'http://balancereader.default:8080')
        self.TRANSACTIONHISTORY_URL = os.getenv('TRANSACTIONHISTORY_URL', 'http://transactionhistory.default:8080')
        self.USERSERVICE_URL = os.getenv('USERSERVICE_URL', 'http://userservice.default:8080')
        self.CONTACTS_URL = os.getenv('CONTACTS_URL', 'http://contacts.default:8080')
        
        # AI Agent URLs
        self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://boa-mcp:8080')
        self.RISK_AGENT_URL = os.getenv('RISK_AGENT_URL', 'http://risk-agent:8081')
        self.TERMS_AGENT_URL = os.getenv('TERMS_AGENT_URL', 'http://terms-agent:8082')
        
        # Demo settings
        self.DEMO_MODE = os.getenv('DEMO_MODE', 'true').lower() == 'true'
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
    def is_gemini_enabled(self) -> bool:
        """Check if Gemini AI is properly configured"""
        return self.GEMINI_API_KEY and self.GEMINI_API_KEY != 'demo-key'
    
    def get_service_urls(self) -> Dict[str, str]:
        """Get all service URLs"""
        return {
            'balancereader': self.BALANCEREADER_URL,
            'transactionhistory': self.TRANSACTIONHISTORY_URL,
            'userservice': self.USERSERVICE_URL,
            'contacts': self.CONTACTS_URL
        }

# Global config instance
config = Config()
