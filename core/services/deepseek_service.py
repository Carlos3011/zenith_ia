from django.conf import settings
import requests
from typing import Dict, List, Optional

class MentalHealthChatbot:
    PHQ8_QUESTIONS = [
        "Durante las últimas 2 semanas, ¿con qué frecuencia te has sentido con poco interés o placer en hacer cosas?",
        "¿Con qué frecuencia te has sentido decaído/a, deprimido/a o sin esperanza?",
        "¿Cómo ha sido tu sueño en términos de dificultad para dormir o dormir demasiado?",
        "¿Con qué frecuencia te has sentido cansado/a o con poca energía?",
        "¿Cómo ha sido tu apetito (poco apetito o comer en exceso)?",
        "¿Te has sentido mal contigo mismo/a o que eres un fracaso?",
        "¿Has tenido dificultad para concentrarte en actividades como leer o ver TV?",
        "¿Cómo han sido tus movimientos (muy lentos o inquietos hasta el punto que otros lo notarían)?"
    ]
    
    SCORE_MAP = {
        "nunca": 0,
        "varios días": 1,
        "mitad": 2,
        "casi todos": 3
    }

    @staticmethod
    def get_phq8_question(session) -> Optional[str]:
        current_question = session.get('current_question', 0)
        if current_question < len(MentalHealthChatbot.PHQ8_QUESTIONS):
            return MentalHealthChatbot.PHQ8_QUESTIONS[current_question]
        return None

    @staticmethod
    def process_answer(session, answer: str) -> Dict:
        current_question = session.get('current_question', 0)
        answers = session.get('phq8_answers', [])
        
        # Mapear respuesta a puntaje
        score = next((v for k, v in MentalHealthChatbot.SCORE_MAP.items() if k in answer.lower()), 0)
        answers.append(score)
        
        session['phq8_answers'] = answers
        session['current_question'] = current_question + 1
        
        if MentalHealthChatbot.get_phq8_question(session):
            return {'type': 'question', 'text': MentalHealthChatbot.get_phq8_question(session)}
        
        # Calcular resultados finales
        total = sum(answers)
        return MentalHealthChatbot.get_assessment_result(total)

    @staticmethod
    def get_assessment_result(score: int) -> Dict:
        interpretations = {
            (0, 4): ("Ninguna depresión", "bg-green-100 text-green-800"),
            (5, 9): ("Depresión leve", "bg-yellow-100 text-yellow-800"),
            (10, 14): ("Depresión moderada", "bg-orange-100 text-orange-800"),
            (15, 19): ("Depresión moderadamente grave", "bg-red-100 text-red-800"),
            (20, 24): ("Depresión grave", "bg-red-600 text-white")
        }
        
        for (min_s, max_s), (label, style) in interpretations.items():
            if min_s <= score <= max_s:
                return {
                    'type': 'result',
                    'score': score,
                    'diagnosis': label,
                    'style': style,
                    'recommendation': MentalHealthChatbot.get_recommendation(score)
                }

    @staticmethod
    def get_recommendation(score: int) -> str:
        if score < 10: return "Sigue monitoreando tu estado de ánimo regularmente."
        if score < 15: return "Recomendamos una consulta con un profesional."
        if score < 20: return "Consulta urgente con un especialista."
        return "Atención inmediata requerida. Por favor contacta a un profesional."

    @staticmethod
    def get_chat_response(prompt: str) -> str:
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=10
            )
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Disculpa, estoy teniendo dificultades técnicas. Error: {str(e)}"