import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

cursos_grupos = {
    'ARQUITETURA E URBANISMO': 'ARQUITETURA E URBANISMO E DESIGN',
    'DESIGN': 'ARQUITETURA E URBANISMO E DESIGN',
    'DESIGN DE ANIMACAO': 'ARQUITETURA E URBANISMO E DESIGN',
    'DESIGN DE GAMES': 'ARQUITETURA E URBANISMO E DESIGN',
    'DESIGN DE INTERIORES': 'ARQUITETURA E URBANISMO E DESIGN',
    'DESIGN DE MODA': 'ARQUITETURA E URBANISMO E DESIGN',
    'DESIGN DE PRODUTO': 'ARQUITETURA E URBANISMO E DESIGN',
    'DESIGN GRAFICO': 'ARQUITETURA E URBANISMO E DESIGN',
    'GESTAO AMBIENTAL': 'CIENCIAS AGRARIAS E MEIO AMBIENTE',
    'GESTAO DO AGRONEGOCIO': 'CIENCIAS AGRARIAS E MEIO AMBIENTE',
    'MEDICINA VETERINARIA': 'CIENCIAS AGRARIAS E MEIO AMBIENTE',
    'BIOMEDICINA': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'CIENCIAS BIOLOGICAS (LICENCIATURA)': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'EDUCACAO FISICA': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'ENFERMAGEM': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'ESTETICA E COMESTICA': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'FARMACIA': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'FISIOTERAPIA': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'FONOAUDIOLOGIA': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'GESTAO HOSPITALAR': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'NUTRICAO': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'ARTES VISUAIS': 'CIENCIAS BIOLOGICAS E DA SAUDE',
    'CIENCIAS SOCIAIS': 'CIENCIAS HUMANAS',
    'FILOSOFIA': 'CIENCIAS HUMANAS',
    'FISICA': 'CIENCIAS HUMANAS',
    'GEOGRAFIA': 'CIENCIAS HUMANAS',
    'HISTORIA': 'CIENCIAS HUMANAS',
    'LETRAS - INGLES': 'CIENCIAS HUMANAS',
    'LETRAS - LINGUA PORTUGUESA': 'CIENCIAS HUMANAS',
    'MATEMATICA (BACHARELADO)': 'CIENCIAS HUMANAS',
    'MATEMATICA (LICENCIATURA)': 'CIENCIAS HUMANAS',
    'PEDAGOGIA': 'CIENCIAS HUMANAS',
    'PSICOLOGIA': 'CIENCIAS HUMANAS',
    'QUIMICA': 'CIENCIAS HUMANAS',
    'SERVICO SOCIAL': 'CIENCIAS HUMANAS',
    'DIREITO': 'CIENCIAS JURIDICAS',
    'MEDIACAO': 'CIENCIAS JURIDICAS',
    'SEGURANCA NO TRANSITO': 'CIENCIAS JURIDICAS',
    'SEGURANCA PRIVADA': 'CIENCIAS JURIDICAS',
    'SEGURANCA PUBLICA': 'CIENCIAS JURIDICAS',
    'SERVIÇOS JUDICIAIS': 'CIENCIAS JURIDICAS',
    'SERVIÇOS NOTARIAIS E REGISTRAIS': 'CIENCIAS JURIDICAS',
    'SERVIÇOS PENAIS': 'CIENCIAS JURIDICAS',
    'CINEMA E AUDIOVISUAL': 'COMUNICACAO E ARTES',
    'COMUNICACAO E INTELIGENCIA DE MERCADO': 'COMUNICACAO E ARTES',
    'JORNALISMO': 'COMUNICACAO E ARTES',
    'PRODUCAO AUDIOVISUAL': 'COMUNICACAO E ARTES',
    'PRODUCACAO MULTIMIDIA EM REALIDADE AUMENTADA': 'COMUNICACAO E ARTES',
    'PUBLICIDADE E PROPAGANDA': 'COMUNICACAO E ARTES',
    'RELACOES PUBLICAS': 'COMUNICACAO E ARTES',
    'ENGENHARIA AMBIENTAL': 'ENGENHARIAS',
    'ENGENHARIA CIVIL': 'ENGENHARIAS',
    'ENGENHARIA DA COMPUTACAO': 'ENGENHARIAS',
    'ENGENHARIA DE CONTROLE E AUTOMACAO': 'ENGENHARIAS',
    'ENGENHARIA DE PRODUCAO': 'ENGENHARIAS',
    'ENGENHARIA ELETRICA': 'ENGENHARIAS',
    'ENGENHARIA MECANICA': 'ENGENHARIAS',
    'ESTATISTICA': 'ENGENHARIAS',
    'GESTAO DA PRODUCAO INDUSTRIAL': 'ENGENHARIAS',
    'ADMINISTRACAO': 'GESTAO E NEGOCIOS',
    'CIENCIAS CONTABEIS': 'GESTAO E NEGOCIOS',
    'COMERCIO EXTERIOR': 'GESTAO E NEGOCIOS',
    'GESTAO COMERCIAL': 'GESTAO E NEGOCIOS',
    'GESTAO DA QUALIDADE': 'GESTAO E NEGOCIOS',
    'GESTAO DE NEGOCIOS DIGITAIS': 'GESTAO E NEGOCIOS',
    'GESTAO DE RECURSOS HUMANOS': 'GESTAO E NEGOCIOS',
    'GESTAO FINANCEIRA': 'GESTAO E NEGOCIOS',
    'GESTAO PUBLICA': 'GESTAO E NEGOCIOS',
    'LOGISTICA': 'GESTAO E NEGOCIOS',
    'MARKETING (BACHARELADO)': 'GESTAO E NEGOCIOS',
    'MARKETING (TECNOLOGO)': 'GESTAO E NEGOCIOS',
    'MARKETING DIGITAL': 'GESTAO E NEGOCIOS',
    'NEGOCIOS IMOBILIARIOS': 'GESTAO E NEGOCIOS',
    'PROCESSOS GERENCIAIS': 'GESTAO E NEGOCIOS',
    'RELACOES INTERNACIONAIS (BACHARELADO)': 'GESTAO E NEGOCIOS',
    'ANALISE E DESENVOLVIMENTO DE SISTEMAS': 'TI E COMPUTACAO',
    'BIG DATA E INTELIGENCIA ANALITICA': 'TI E COMPUTACAO',
    'CIENCIA DA COMPUTACAO': 'TI E COMPUTACAO',
    'GESTAO DA TECNOLOGIA DA INFORMACAO': 'TI E COMPUTACAO',
    'JOGOS DIGITAIS': 'TI E COMPUTACAO',
    'REDES DE COMPUTADORES': 'TI E COMPUTACAO',
    'SEGURANCA DA INFORMACAO': 'TI E COMPUTACAO',
    'SISTEMAS DE INFORMACAO': 'TI E COMPUTACAO',
    'SISTEMAS PARA INTERNET': 'TI E COMPUTACAO',
    'EVENTOS': 'TURISMO E HOSPITALIDADE',
    'GASTRONOMIA': 'TURISMO E HOSPITALIDADE',
    'GESTAO DE TURISMO': 'TURISMO E HOSPITALIDADE'
}

modalidades = ['PRESENCIAL', 'SEMIPRESENCIAL', 'EAD']

turnos = ['MANHA', 'TARDE', 'NOITE']

status_matricula = ['MATRICULADO', 'CANCELADO', 'FORMADO', 'TRANCADO']

motivos_cancelamento = ['EMPREGO', 'INADIMPLENCIA', 'INSATISFACAO', 'DESISTENCIA', 'TRANSFERENCIA', 'INTERCAMBIO']

curso_id_map = {curso : idx + 1 for idx, curso in enumerate(cursos_grupos.keys())}
grupo_id_map = {grupo : idx + 1 for idx, grupo in enumerate(set(cursos_grupos.values()))}
modalidade_id_map = {modalidade : idx + 1 for idx, modalidade in enumerate(modalidades)}
turno_id_map = {turno : idx + 1 for idx, turno in enumerate(turnos)}
status_id_map = {status : idx + 1 for idx, status in enumerate(status_matricula)}

def gerar_data_aleatoria(inicio, fim):
    return inicio + timedelta(days = random.randint(0, (fim - inicio).days))

def calcular_mensalidade_paga(mensalidade, desconto) :
    return round(mensalidade * (1 - desconto), 2)

def gerar_status_matricula_e_dt_cancelamento(dt_matricula) :
    status = random.choice(status_matricula)
    dt_cancelamento = None
    if status in ['CANCELADO', 'TRANCADO'] :
        max_cancelamento_date = dt_matricula + timedelta(days = 7 * 365)
        if max_cancelamento_date > data_fim :
            max_cancelamento_date = data_fim
        dt_cancelamento = gerar_data_aleatoria(dt_matricula, max_cancelamento_date)
    return status, dt_cancelamento

n_alunos = 10000

data_inicio = datetime(2013, 1, 1)
data_fim = datetime(2023, 12, 31)

pasta_saida = "base_alunos"
os.makedirs(pasta_saida, exist_ok = True)

alunos_por_mes = n_alunos // ((data_fim.year - data_inicio.year + 1) * 12)

aluno_id = 1

grupo_probabilidades = {
    'CIENCIAS BIOLOGICAS E DA SAUDE': 26,
    'ENGENHARIAS': 16,
    'CIENCIAS JURIDICAS': 13,
    'COMUNICACAO E ARTES': 10,
    'TI E COMPUTACAO': 9,
    'CIENCIAS HUMANAS': 7,
    'ARQUITETURA E URBANISMO E DESIGN': 6,
    'CIENCIAS AGRARIAS E MEIO AMBIENTE': 6,
    'GESTAO E NEGOCIOS': 5,
    'TURISMO E HOSPITALIDADE': 2
}

modalidade_probabilidades = [67, 21, 12]
turno_probabilidades = [11, 37, 52]
status_probabilidades = [34, 29, 21, 16]
motivo_probabilidades = [36, 29, 17, 8, 8, 2]

for ano in range(data_inicio.year, data_fim.year + 1) :
    for mes in range(1, 13) :
        if aluno_id > n_alunos :
            break

        inicio_mes = datetime(ano, mes, 1)
        fim_mes = (inicio_mes + pd.DateOffset(months = 1)).replace(day = 1) - timedelta(days = 1)
        
        if inicio_mes > data_fim :
            break
        
        data = []

        for _ in range(alunos_por_mes) :
            if aluno_id > n_alunos :
                break

            grupo = random.choices(list(grupo_probabilidades.keys()), weights = grupo_probabilidades.values(), k = 1)[0]
            cursos_no_grupo = [curso for curso, g in cursos_grupos.items() if g == grupo]
            curso_escolhido = random.choice(cursos_no_grupo)

            modalidade = random.choices(modalidades, weights = modalidade_probabilidades, k = 1)[0]
            turno = random.choices(turnos, weights = turno_probabilidades, k = 1)[0]
            status = random.choices(status_matricula, weights = status_probabilidades, k = 1)[0]

            mensalidade = round(random.uniform(500, 5000), 2)
            desconto = round(random.uniform(0, 0.6), 2)
            mensalidade_paga = calcular_mensalidade_paga(mensalidade, desconto)

            matricula_data_inicio = max(datetime(2019, 1, 1), inicio_mes)
            matricula_data_fim = min(datetime(2019, 1, 1) + timedelta(days = 7 * 365), inicio_mes)

            if matricula_data_inicio > matricula_data_fim:
                dt_matricula = matricula_data_inicio
            else:
                dt_matricula = gerar_data_aleatoria(matricula_data_inicio, matricula_data_fim)

            status, dt_cancelamento = gerar_status_matricula_e_dt_cancelamento(dt_matricula)

            motivo_cancelamento = random.choices(motivos_cancelamento, weights = motivo_probabilidades, k = 1)[0] if status == 'CANCELADO' else None

            data.append({
                'id_aluno': aluno_id,
                'id_curso': curso_id_map[curso_escolhido],
                'id_grupo': grupo_id_map[grupo],
                'id_modalidade': modalidade_id_map[modalidade],
                'id_turno': turno_id_map[turno],
                'id_status': status_id_map[status],
                'curso': curso_escolhido,
                'grupo': grupo,
                'modalidade': modalidade,
                'turno': turno,
                'status_matricula': status,
                'dt_matricula': dt_matricula,
                'dt_cancelamento': dt_cancelamento if status != 'MATRICULADO' else None,
                'motivo_cancelamento': motivo_cancelamento,
                'idade': random.randint(18, 55),
                'genero': random.choice(['M', 'F']),
                'mensalidade': mensalidade,
                'desconto': desconto,
                'mensalidade_paga': mensalidade_paga
            })

            aluno_id += 1

        df_mes = pd.DataFrame(data)
        
        file_name = os.path.join(pasta_saida, f"matriculas_{ano}_{mes:02d}.csv")
        
        df_mes.to_csv(file_name, index = False, encoding = 'utf-8')

all_files = [os.path.join(pasta_saida, f) for f in os.listdir(pasta_saida) if f.endswith('.csv')]
df_concat = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

df_concat.to_csv("matriculas.csv", index = False, encoding = 'utf-8')