import numpy as np

def gerar_dados_videos(num_videos, base_rate, amplitude, periodo):
    """
    Gera dados simulados de sessões de vídeo e salva em um arquivo TXT.

    Parâmetros:
    - num_videos: Número de vídeos/sessões a serem gerados.
    - base_rate: Taxa base de abertura de sessões.
    - amplitude: Amplitude da variação diária na taxa de chegada (0 a 1).
    - periodo: Período para a variação diária (horas).
    """

    def lambda_t(t):
        # Taxa de chegada varia ao longo do dia
        return base_rate * (1 + amplitude * np.sin(2 * np.pi * (t % periodo) / periodo))

    # Gerar instantes de abertura (AS)
    as_values = []
    t = 0
    while len(as_values) < num_videos:
        current_lambda = lambda_t(t)
        # Evitar valores negativos ou zero para lambda
        current_lambda = max(current_lambda, 0.0001)
        t += np.random.exponential(scale=1/current_lambda)
        as_values.append(t)

    as_values = np.array(as_values)

    # Gerar durações das sessões usando distribuição log-normal
    mean_duration = 0.1  # Média das durações
    sigma_duration = 0.05  # Desvio padrão das durações
    durations = np.random.lognormal(mean=np.log(mean_duration), sigma=sigma_duration, size=num_videos)

    # Calcular instantes de fechamento (FS)
    fs_values = as_values + durations

    # Gerar IDs aleatórios
    ids = np.random.randint(0, 1000, num_videos)

    # Criar o arquivo TXT com os dados no formato solicitado
    with open('dados_videos_aprimorado.txt', 'w') as file:
        file.write(" ID     AS       FS\n")
        for i in range(num_videos):
            file.write(f"{ids[i]:03d}    {as_values[i]:.3f}    {fs_values[i]:.3f}\n")

    print(f"Arquivo 'dados_videos_aprimorado.txt' criado com sucesso com {num_videos} vídeos!")

# Exemplo de chamada da função
if __name__ == "__main__":
    # Solicitar parâmetros ao usuário
    print("=== Gerador de Dados de Vídeos ===")
    num_videos = int(input("Informe o número de vídeos/sessões a serem gerados: "))
    base_rate = float(input("Informe a taxa base de abertura de sessões: "))
    amplitude = float(input("Informe a amplitude da variação diária (0 a 1): "))
    periodo = float(input("Informe o período para a variação diária (horas): "))

    # Chamar a função com os parâmetros fornecidos
    gerar_dados_videos(num_videos, base_rate, amplitude, periodo)
