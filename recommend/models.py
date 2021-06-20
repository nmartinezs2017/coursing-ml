from typing import List
from pydantic import BaseModel

class UserContext(BaseModel):
    discarded_courses: List[int] = []
    language_list: List[str] = ["English", "German", "Portuguese", "Romanian", "Arabic", "Italian",
       "Hungarian", "French", "Persian", "Turkish", "Spanish",
       "Indonesian", "Simplified Chinese", "Japanese", "Polish", "Hindi",
       "Russian", "Vietnamese", "Thai", "Dutch", "Kazakh",
       "Traditional Chinese", "Hebrew", "Urdu", "Bengali", "Tamil",
       "Telugu", "Norwegian", "Korean", "Czech", "Greek", "Burmese",
       "Serbian", "Finnish", "Filipino", "Pashto", "Malayalam",
       "Croatian", "Kannada", "Danish", "Marathi", "Azeri", "Georgian",
       "Afrikaans", "Bulgarian", "Ukrainian", "Slovenian", "Punjabi",
       "Mongolian", "Swahili", "Catalan", "Albanian", "Slovak", "Somali",
       "Irish", "Estonian", "Uzbek", "Gujarati", "Lithuanian", "Latvian",
       "Armenian", "Swedish", "Kurdish", "Aymara", "Khmer", "Malay",
       "Nepali", "Tatar"]

class UserProfile(BaseModel):
    description: str = " "
    difficulty: str = 'beginner'
    duration: int = 18.050667
    free: int = 1
    students: int = 383077.8
    rating: float = 4.5
    institution: str = "Coursera"
    cost: float = 57.394100