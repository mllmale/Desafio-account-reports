import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro"):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def format_data_for_analysis(self, interactions: list, limit: int = 5) -> str:
        formatted_text = "Segue abaixo as interações coletadas para análise:\n\n"
        for idx, interaction in enumerate(interactions[:limit], 1):
            formatted_text += (
                f"Interação {idx}:\n"
                f"Data: {interaction['Date']}\n"
                f"Tipo: {interaction['TypeId']}\n"
                f"Conteúdo: {interaction['Content'][:800]}...\n\n"  # aumenta o limite do conteúdo para melhor contexto
            )
        return formatted_text

    def analyze_interactions(self, formatted_data: str) -> str:
        
        prompt = (
            "Você é um assistente especializado em análise de interações comerciais.\n"
            "Analise criticamente o seguinte conjunto de interações.\n\n"
            "Para cada interação, identifique claramente:\n"
            "- O ASSUNTO PRINCIPAL da conversa (por exemplo: venda de imóvel, dúvida técnica, reclamação, etc.).\n"
            "- O DESEMPENHO DO VENDEDOR: avaliar tom de voz, cordialidade, proatividade, conhecimento do produto e assertividade.\n\n"
            "Depois, forneça um RESUMO GERAL contendo:\n"
            "- Temas predominantes nas conversas.\n"
            "- Padrões de comportamento dos vendedores.\n"
            "- Oportunidades comerciais detectadas.\n"
            "- Recomendações específicas para treinamento ou ajustes na abordagem comercial.\n\n"
            f"{formatted_data}\n\n"
            "Por favor, forneça um relatório analítico bem estruturado, objetivo e com foco na melhoria contínua do atendimento."
        )

        response = self.model.generate_content(prompt)

        return response.text
