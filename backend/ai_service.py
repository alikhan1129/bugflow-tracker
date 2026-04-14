import os
import json
import google.generativeai as genai
from backend.schemas import AITriageResponse

class AIService:
    def __init__(self):
        self._model = None

    @property
    def model(self):
        """Lazy initialization of the Gemini model with a balanced temperature."""
        if self._model is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                # temperature=0.2 avoids rigid outputs while maintaining precision
                self._model = genai.GenerativeModel(
                    'gemini-pro',
                    generation_config={"temperature": 0.2}
                )
        return self._model

    def _smart_fallback(self, title, description):
        """Intelligent fallback based on keywords if AI fails or returns invalid data."""
        text = (title + " " + description).lower()
        
        # Determine Category
        if any(k in text for k in ["slow", "delay", "timeout", "lag", "performance", "speed", "load", "loading", "wait", "seconds"]):
            category = "performance"
        elif any(k in text for k in ["payment", "login", "api", "database", "auth", "server", "logic", "error 500", "500", "crash", "bug", "process", "order"]):
            category = "backend"
        elif any(k in text for k in ["ui", "layout", "button", "color", "font", "css", "visual", "misaligned", "overlap", "responsive", "mobile", "icon", "text"]):
            category = "ui"
        else:
            category = "backend"

        # Determine Severity
        if any(k in text for k in ["critical", "crash", "blocks", "data loss", "failure", "broken", "payment", "high", "security", "exploit"]):
            severity = "high"
        elif any(k in text for k in ["annoyance", "slight", "minor", "low", "misaligned", "small", "typo"]):
            severity = "low"
        else:
            severity = "medium"

        print(f"DEBUG: Smart Fallback used: category={category}, severity={severity}")
        return category, severity

    def triage_bug(self, title: str, description: str) -> AITriageResponse:
        """
        Expert bug triage with balanced prompting and smart keyword fallback.
        """
        model = self.model
        if not model:
            print("DEBUG: No AI model available, using smart fallback.")
            cat, sev = self._smart_fallback(title, description)
            return AITriageResponse(severity=sev, category=cat, title=f"[MOCK] {title}")

        prompt = f"""
You are an expert bug triage system.

Classify the bug into ONE category:
- UI → visual/layout issues only
- backend → API, database, logic, authentication, payment issues
- performance → slowness, delays, timeouts

Assign severity:
- low → minor issue, does not block usage
- medium → affects functionality but has workaround
- high → blocks core feature, causes failure, or data loss

IMPORTANT:
- Do NOT default to backend or medium. Use reasoning based on the description.
- Be decisive and vary outputs appropriately based on the issue type.

Guidelines:
- Payment, login, API failures → backend + high
- Slow loading → performance (medium or low)
- Visual misalignment → UI + low
- Broken UI affecting usage → UI + medium

Examples:
1. "Payment deducted but order not created" -> {{ "category": "backend", "severity": "high", "title": "Resolve Payment-Order Desync" }}
2. "Dashboard takes 10 seconds to load" -> {{ "category": "performance", "severity": "medium", "title": "Optimize Dashboard Loading Speed" }}
3. "Button slightly misaligned" -> {{ "category": "UI", "severity": "low", "title": "Fix Button Alignment in Header" }}
4. "Form overlaps and cannot be used" -> {{ "category": "UI", "severity": "medium", "title": "Fix Form Layout Overlap" }}

Return ONLY valid JSON:
{{
  "category": "UI | backend | performance",
  "severity": "low | medium | high",
  "title": "short improved title"
}}

Bug Report:
Title: {title}
Description: {description}
"""

        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            
            # Robust JSON parsing
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start == -1: raise ValueError("Invalid AI response")
            
            data = json.loads(content[json_start:json_end])
            
            # Validation layer
            valid_cats = ["ui", "backend", "performance"]
            valid_sevs = ["low", "medium", "high"]
            
            cat = str(data.get("category", "")).lower().strip()
            sev = str(data.get("severity", "")).lower().strip()
            new_title = data.get("title", title)

            # Intelligent correction if AI output is invalid
            if cat not in valid_cats or sev not in valid_sevs:
                fallback_cat, fallback_sev = self._smart_fallback(title, description)
                cat = cat if cat in valid_cats else fallback_cat
                sev = sev if sev in valid_sevs else fallback_sev
            
            return AITriageResponse(severity=sev, category=cat, title=new_title)

        except Exception as e:
            # Smart fallback for malformed JSON or networking errors
            print(f"AI Triage Error: {str(e)}")
            fallback_cat, fallback_sev = self._smart_fallback(title, description)
            return AITriageResponse(severity=fallback_sev, category=fallback_cat, title=title)

ai_service = AIService()
