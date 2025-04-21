from urllib.parse import urlencode
from typing import Dict, List, Optional, Any, Union

class ConsoleView:
    """View for displaying messages to the console"""
    @staticmethod
    def display_message(message: str) -> None:
        print(message)
    
    @staticmethod
    def display_error(message: str) -> None:
        print(f"Error: {message}")
    
    @staticmethod
    def display_success(message: str) -> None:
        print(f"Success: {message}")
    
    @staticmethod
    def display_parameters(params: Dict) -> None:
        print("Current parameters:")
        for key, value in params.items():
            print(f"  {key}: {value}")