import numpy as np
import json

def gerar_dados_videos_json(tempo_total_simulacao, num_videos, a_zipf, num_usuarios):
    """
    Gera dados simulados de sessões de vídeo e salva em um arquivo JSON com detalhes das requisições dos usuários.
    """
    # Ajustar o número de intervalos com base no tempo total de simulação
    num_intervalos = np.random.randint(2, min(10, tempo_total_simulacao + 1))  # Definir entre 2 a 10 intervalos ou tempo_total_simulacao + 1

    # Gerar tempos únicos para o particionamento
    possible_times = np.arange(1, tempo_total_simulacao)
    num_times = min(len(possible_times), num_intervalos - 1)
    if num_times > 0:
        particionamento_interm = np.sort(np.random.choice(possible_times, size=num_times, replace=False))
        particionamento = np.concatenate(([0], particionamento_interm, [tempo_total_simulacao]))  # Inclui o tempo 0 e total
    else:
        particionamento = np.array([0, tempo_total_simulacao])

    # Gerar distribuição Zipf para determinar a popularidade dos vídeos
    ranks = np.arange(1, num_videos + 1)
    probabilities = 1 / np.power(ranks, a_zipf)
    probabilities /= probabilities.sum()  # Normalizar para somar 1

    # Atribuir vídeos aos usuários com base na distribuição Zipf
    video_ids = np.random.choice(ranks, size=num_usuarios, p=probabilities)
    user_ids = np.arange(num_usuarios)

    # Mapear usuários aos vídeos
    user_video_map = dict(zip(user_ids, video_ids))

    # Criar a estrutura para armazenar os dados das sessões de vídeo
    dados_videos = []
    taxas_poisson = []

    # Primeiro, garantir que cada usuário tenha pelo menos uma sessão
    for user_id in user_ids:
        video_id = user_video_map[user_id]

        # Gerar o tempo de chegada (start_time)
        start_time = np.random.randint(0, tempo_total_simulacao)
        session_duration = np.random.randint(1, 10)  # Duração da sessão entre 1 e 10 segundos

        # Adicionar o registro da sessão
        dados_videos.append({
            "video_id": int(video_id),
            "user_id": int(user_id),
            "start_time": start_time,
            "end_time": start_time + session_duration  # Tempo final da sessão
        })

    # Agora, simular acessos adicionais usando processos de Poisson
    for i in range(len(particionamento) - 1):
        inicio_intervalo = particionamento[i]
        fim_intervalo = particionamento[i + 1]

        # Verificar se o intervalo é válido
        if fim_intervalo <= inicio_intervalo:
            continue  # Pular intervalos inválidos

        # Gerar uma taxa de Poisson para cada intervalo
        lambda_acesso = np.random.uniform(0.5, 5)  # Variação aleatória da taxa de Poisson entre os intervalos
        taxas_poisson.append(lambda_acesso)

        # Número de acessos neste intervalo
        num_acessos = np.random.poisson(lambda_acesso)

        # Selecionar usuários aleatoriamente (com repetição)
        usuarios_selecionados = np.random.choice(user_ids, size=num_acessos, replace=True)

        for user_id in usuarios_selecionados:
            video_id = user_video_map[user_id]

            # Gerar o tempo de chegada (start_time)
            start_time = np.random.randint(inicio_intervalo, fim_intervalo)
            session_duration = np.random.randint(1, 10)  # Duração da sessão entre 1 e 10 segundos

            # Adicionar o registro da sessão
            dados_videos.append({
                "video_id": int(video_id),
                "user_id": int(user_id),
                "start_time": start_time,
                "end_time": start_time + session_duration  # Tempo final da sessão
            })

    # Organizar os dados por ordem de chegada (start_time)
    dados_videos = sorted(dados_videos, key=lambda x: x['start_time'])

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
    a_zipf = float(input("Informe o parâmetro 'a' da distribuição de Zipf (maior valor significa mais desbalanceamento): "))
    num_usuarios = int(input("Informe o número de usuários únicos: "))

    # Chamar a função com os parâmetros fornecidos
    gerar_dados_videos_json(tempo_total_simulacao, num_videos, a_zipf, num_usuarios)
