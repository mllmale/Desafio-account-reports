from datetime import datetime
from config import *
from clients.ploomes_client import PloomesClient
from clients.gemini_client import GeminiClient
from clients.zapi_client import ZAPIClient


def main():
    try:
        # Validar configurações
        validate_config()
        print(" Configurações validadas")

        # Inicializar clientes
        ploomes = PloomesClient(PLOOMES_USER_KEY)
        gemini = GeminiClient(GEMINI_API_KEY)
        zapi = ZAPIClient(ZAPI_INSTANCE, ZAPI_TOKEN, ZAPI_SECURITY_TOKEN)

        # 1. Verificar conexões
        print("\n Verificando conexões...")

        if not ploomes.test_connection():
            raise Exception("Falha na conexão com Ploomes")
        print(" Ploomes conectado")

        if not zapi.test_connection():
            raise Exception("WhatsApp não conectado no Z-API")
        print(" WhatsApp conectado")

        # 2. Buscar dados do Ploomes
        print(f"\nBuscando interações dos últimos {DAYS_TO_SEARCH} dias...")
        interactions = ploomes.get_interactions(DAYS_TO_SEARCH, MAX_INTERACTIONS)

        if not interactions:
            print(" Nenhuma interação encontrada")
            return

        print(f" {len(interactions)} interações coletadas")

        # 3. Formatar dados
        formatted_data = ploomes.format_interactions(interactions)

        # 4. Gerar análise com Gemini
        print(" Gerando análise com IA...")
        analysis = gemini.analyze_interactions(formatted_data)
        print(" Análise gerada")

        # 5. Preparar relatório final
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M")

        report = f"""
         *RELATÓRIO SEMANAL DE VENDAS*
         Gerado automaticamente em {timestamp}
        
        {analysis}
                """.strip()

        # 6. Enviar via WhatsApp
        print(" Enviando relatório via WhatsApp...")

        result = zapi.send_message(WHATSAPP_NUMBER, report)

        if result['success']:
            print(" INTEGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print(f" Relatório enviado para {WHATSAPP_NUMBER}")
        else:
            print(f" Falha no envio: {result['error']}")

    except Exception as e:
        print(f" Erro na integração: {e}")


if __name__ == "__main__":
    main()