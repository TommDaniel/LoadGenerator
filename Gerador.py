import numpy as np
import json


def gerar_dados_videos_json(tempo_total_simulacao, num_videos, a_zipf, num_usuarios):
    """
    Gera dados simulados de sessões de vídeo e salva em um arquivo JSON com detalhes das requisições dos usuários.

    Parâmetros:
    - tempo_total_simulacao: Tempo total de simulação (em segundos).
    - num_videos: Número total de vídeos disponíveis.
    - a_zipf: Parâmetro de inclinação da distribuição de Zipf.
    - num_usuarios: Número total de usuários únicos.
    """

    # Gerar particionamento aleatório do tempo total de simulação
    num_intervalos = np.random.randint(2, 10)  # Definir entre 2 a 10 intervalos
    particionamento = np.sort(np.random.randint(1, tempo_total_simulacao, num_intervalos - 1))
    particionamento = np.concatenate(([0], particionamento, [tempo_total_simulacao]))  # Inclui o tempo 0 e total

    # Gerar distribuição Zipf para determinar a quantidade de pessoas por vídeo
    video_popularity = np.random.zipf(a_zipf, num_usuarios)
    video_popularity = video_popularity % num_videos  # Garantir IDs dentro do limite de vídeos
    unique, counts = np.unique(video_popularity, return_counts=True)

    # Mapear o número de usuários para cada vídeo
    video_user_map = {video: count for video, count in zip(unique, counts)}

    # Criar a estrutura para armazenar os dados das sessões de vídeo
    dados_videos = []
    taxas_poisson = []

    # Simular para cada intervalo de tempo
    for i in range(len(particionamento) - 1):
        inicio_intervalo = particionamento[i]
        fim_intervalo = particionamento[i + 1]

        # Gerar IDs de usuários aleatórios sem repetição para cada intervalo
        usuarios_disponiveis = list(np.random.permutation(np.arange(0, num_usuarios)))

        # Gerar uma taxa de Poisson para cada intervalo
        lambda_acesso = np.random.uniform(0.5, 5)  # Variação aleatória da taxa de Poisson entre os intervalos
        taxas_poisson.append(lambda_acesso)

        # Para cada vídeo, gerar acessos de acordo com a distribuição de Poisson
        for video_id, num_pessoas in video_user_map.items():
            if len(usuarios_disponiveis) == 0:
                break

            # Quantos acessos ocorrerão neste intervalo (Poisson)
            num_acessos = np.random.poisson(lambda_acesso)

            # O número de acessos não pode exceder o número de pessoas disponíveis
            num_acessos = min(num_acessos, num_pessoas, len(usuarios_disponiveis))

            # Selecionar usuários para este vídeo
            usuarios_selecionados = usuarios_disponiveis[:num_acessos]
            usuarios_disponiveis = usuarios_disponiveis[num_acessos:]  # Remover esses usuários da lista

            for user_id in usuarios_selecionados:
                # Gerar o tempo de chegada (start_time) e a duração da sessão (end_time)
                start_time = np.random.randint(inicio_intervalo, fim_intervalo)
                session_duration = np.random.randint(1, 10)  # Duração da sessão entre 1 e 10 segundos

                # Adicionar o registro da sessão
                dados_videos.append({
                    "video_id": int(video_id),
                    "user_id": int(user_id),
                    "start_time": start_time,
                    "end_time": session_duration  # Duração em segundos
                })

    # Criar a estrutura final de saída, incluindo as informações do particionamento, Zipf e Poisson
    dados_saida = {
        "zipf_param": a_zipf,
        "taxas_poisson": taxas_poisson,
        "particionamento": particionamento.tolist(),
        "dados_videos": dados_videos
    }

    # Salvar os dados no formato JSON
    with open('dados_videos_aprimorado_simulacao.json', 'w') as json_file:
        json.dump(dados_saida, json_file, indent=4)

    print(f"Arquivo 'dados_videos_aprimorado_simulacao.json' criado com sucesso com dados de {num_usuarios} usuários!")


# Exemplo de chamada da função
if __name__ == "__main__":
    # Solicitar parâmetros ao usuário
    print("=== Gerador de Carga de Vídeos com Distribuição Zipf e Acessos Poisson ===")

    tempo_total_simulacao = int(input("Informe o tempo total de simulação (em segundos): "))
    num_videos = int(input("Informe o número total de vídeos: "))
    a_zipf = float(
        input("Informe o parâmetro 'a' da distribuição de Zipf (maior valor significa mais desbalanceamento): "))
    num_usuarios = int(input("Informe o número de usuários únicos: "))

    # Chamar a função com os parâmetros fornecidos
    gerar_dados_videos_json(tempo_total_simulacao, num_videos, a_zipf, num_usuarios)
