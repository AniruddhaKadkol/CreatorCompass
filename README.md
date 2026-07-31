# Creator Compass
Creator Compass is an AI-powered assistant built using **Flask** and **IBM Granite (watsonx.ai)** to help creators generate ideas, improve their content, and receive AI-powered feedback.

---
# Features
## Content Creator Workspace
Designed for creators on:
- YouTube
- Instagram
- TikTok

Creator Compass can help with:
- Video titles
- Descriptions
- SEO suggestions
- Script ideas
- Branding
- Content strategy
- Thumbnail ideas (text suggestions)

---
## Creative Studio
Designed for artists and creative professionals.
Creator Compass helps with:
- Character concepts
- Environment ideas
- World building
- Illustration concepts
- Comic ideas
- Concept art
- Color palette suggestions
- Scene composition
- Art styles
The Creative Studio focuses on creative guidance rather than image generation.

---
## Creator Dashboard
The Creator Dashboard analyzes user input and provides:
- Overall score
- Title quality
- Hook strength
- SEO quality
- Creativity score
- Audience appeal
- Strengths
- Suggestions for improvement

---
## Conversation History
Creator Compass stores conversations locally using JSON.
Each workspace maintains its own history including:
- Date
- Time
- Preview

---
# Technologies Used
Backend
- Python
- Flask

Frontend
- HTML
- CSS
- JavaScript

Artificial Intelligence
- IBM watsonx.ai
- IBM Granite 4 H Small

Storage
- JSON

---
# Project Structure
```
CreatorCompass/

    ai/
    config/
    data/
    docs/
    models/
    services/
    static/
    templates/

    app.py
    requirements.txt
    README.md
    .gitignore
```

---
# Installation
Clone the repository.
Install dependencies.
```bash
pip install -r requirements.txt
```
Create a `.env` file.
Example:

```env
IBM_API_KEY=YOUR_API_KEY
IBM_PROJECT_ID=YOUR_PROJECT_ID
IBM_URL=https://us-south.ml.cloud.ibm.com
```
Run the application.
```bash
python app.py
```

---
# Future Improvements
- User authentication
- AI-powered Creator Dashboard
- Multi-platform optimization
- Trend analysis
- Export conversations
- Cloud database
- User profiles

---
# Screenshots
(Add screenshots here)
- Home
- Content Creator
- Creative Studio
- Creator Dashboard

---
# License

This project was developed as part of learning and experimentation using IBM watsonx.ai.