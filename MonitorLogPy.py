import random
import datetime

def menu():
    nome_arq = 'log.txt'
    while True:
        print('MENU\n')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e analisar logs')
        print('4 - SAIR')
        opc = int(input('Escolha uma opção: '))
        if opc == 1:
            try:
                qtd = int(input('Quantidade de logs(registros): '))
                gerarArquivo(nome_arq, qtd)
            except:
                print('Entrada inválida.')
        elif opc == 2:
            analisarLogs(nome_arq)
        elif opc == 3:
            try:
                qtd = int(input('Quantidade de logs(registros): '))
                gerarArquivo(nome_arq, qtd)
                analisarLogs(nome_arq)
            except:
                print('Entrada inválida.')
        elif opc == 4:
            print('Até mais')
            break
        else:
            print('Opção inválida')
            
def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, 'w', encoding='UTF-8') as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + '\n')
        print('Log gerado')
        
def montarLog(i):
    data      = gerarData(i)
    ip        = gerarIp(i)
    recurso   = gerarRecurso(i)
    metodo    = gerarMetodo(i)
    status    = gerarStatus(i)
    tempo     = gerarTempo(i)
    agente    = gerarAgente(i)
    protocolo = gerarProtocolo(i)
    tamanho   = gerarTamanho(i)
    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - {tamanho} - {protocolo} - {agente} - /home'

def gerarData(i):
    base  = datetime.datetime.now()
    delta = datetime.timedelta(seconds= i * random.randint(5,20) )
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')

def gerarIp(i):
    r = random.randint(1,6)
    if i >= 20 and i <= 50:
        return '203.120.45.7'
    
    if r == 1:
        return '192.168.12.1'
    elif r == 2:
        return '192.168.12.3'
    elif r == 3:
        return '192.100.12.3'
    elif r == 4:
        return '192.168.162.3'
    elif r == 5:
        return '192.168.23.3'
    elif r == 6:
        return '192.168.0.3'

def gerarRecurso(i):
    r = random.randint(1, 6)

    if r == 1:
        return "/home"
    elif r == 2:
        return "/login"
    elif r == 3:
        return "/admin"
    elif r == 4:
        return "/produtos"
    elif r == 5:
        return "/backup"
    else:
        return "/config"
    
def gerarMetodo(i):
    if i % 2 == 0:
        return "GET"
    else:
        return "POST"
    
def gerarStatus(i):
    r = random.randint(1, 10)

    if r == 1:
        return 200
    elif r == 2:
        return 403
    elif r == 3:
        return 404
    elif r == 4:
        return 500
    elif r == 5:
        return 200
    elif r == 6:
        return 200
    elif r == 7:
        return 403
    elif r == 8:
        return 404
    elif r == 9:
        return 200
    else:
        return 500
    
def gerarTempo(i):
    if i >= 30 and i <= 40:
        return 100 + (i * 30)
    return random.randint(50, 1000)

def gerarAgente(i):
    if i % 10 == 0:
        return "Bot"
    elif i % 7 == 0:
        return "Crawler"
    else:
        return "Chrome"
    
def gerarProtocolo(i):
    if i % 3 == 0:
        return "HTTP/1.0"
    elif i % 3 == 1:
        return "HTTP/1.1"
    else:
        return "HTTP/2"
    
def gerarTamanho(i):
    return random.randint(200, 5000)

# =========================
# extração
# =========================

def extrairCampos(linha):
    data = ''
    ip = ''
    metodo = ''
    status = ''
    recurso = ''
    tempo = ''
    tamanho = ''
    protocolo = ''
    agente = ''
    referer = ''

    parte = 0

    for c in linha:
        if c == ']':
            parte = 1
            continue

        if c == '-' and parte < 9:
            parte += 1
            continue

        if parte == 0:
            data += c
        elif parte == 1:
            ip += c
        elif parte == 2:
            metodo += c
        elif parte == 3:
            status += c
        elif parte == 4:
            recurso += c
        elif parte == 5:
            tempo += c
        elif parte == 6:
            tamanho += c
        elif parte == 7:
            protocolo += c
        elif parte == 8:
            agente += c
        else:
            referer += c

    return data, ip.strip(), metodo.strip(), status.strip(), recurso.strip(), tempo.strip(), tamanho.strip(), protocolo.strip(), agente.strip(), referer.strip()


# =========================
# classificações
# =========================

def classificarTempo(t):
    if t < 200:
        return 'rapido'
    elif t < 800:
        return 'normal'
    else:
        return 'lento'


def classificarEstado(disp, falha, lento, bot):
    if falha > 0 or disp < 70:
        return 'CRÍTICO'
    elif disp < 85 or lento > 30:
        return 'INSTÁVEL'
    elif disp < 95 or bot > 0:
        return 'ATENÇÃO'
    else:
        return 'SAUDÁVEL'


# =========================
# análise
# =========================

def analisarLogs(nome_arq):

    try:
        with open(nome_arq, 'r', encoding='UTF-8') as arq:

            total = sucesso = erro = erro500 = 0
            somaTempo = 0
            maior = 0
            menor = None

            rapido = normal = lento = 0

            s200 = s403 = s404 = s500 = 0

            recurso_top = ''
            recurso_top_cont = 0
            recurso_atual = ''
            recurso_cont = 0

            ip_top = ''
            ip_top_cont = 0
            ip_atual = ''
            ip_cont = 0

            ip_erro_top = ''
            ip_erro_top_cont = 0
            ip_erro_atual = ''
            ip_erro_cont = 0

            forca_bruta = 0
            ultimo_forca = ''
            seq_login = 0

            admin_erro = 0

            tempo_ant = -1
            crescente = 0
            degradacao = 0

            erro500_seq = 0
            falha_critica = 0

            bot = 0
            ultimo_bot = ''
            seq_ip = 0
            ip_ant = ''

            rotas = 0
            rotas_falha = 0

            for linha in arq:

                if linha.strip() == '':
                    continue

                total += 1

                data, ip, metodo, status, recurso, tempo, tamanho, protocolo, agente, referer = extrairCampos(linha)

                status = int(status)
                tempo = int(tempo.replace('ms', ''))

                somaTempo += tempo

                if tempo > maior:
                    maior = tempo

                if menor is None or tempo < menor:
                    menor = tempo

                # STATUS
                if status == 200:
                    sucesso += 1
                    s200 += 1
                else:
                    erro += 1

                if status == 403:
                    s403 += 1
                elif status == 404:
                    s404 += 1
                elif status == 500:
                    s500 += 1
                    erro500 += 1

                # TEMPO
                tipo = classificarTempo(tempo)
                if tipo == 'rapido':
                    rapido += 1
                elif tipo == 'normal':
                    normal += 1
                else:
                    lento += 1

                # RECURSO MAIS ACESSADO (aproximação)
                if recurso == recurso_atual:
                    recurso_cont += 1
                else:
                    recurso_atual = recurso
                    recurso_cont = 1

                if recurso_cont > recurso_top_cont:
                    recurso_top = recurso_atual
                    recurso_top_cont = recurso_cont

                # IP MAIS ATIVO
                if ip == ip_atual:
                    ip_cont += 1
                else:
                    ip_atual = ip
                    ip_cont = 1

                if ip_cont > ip_top_cont:
                    ip_top = ip_atual
                    ip_top_cont = ip_cont

                # IP COM MAIS ERROS
                if status != 200:
                    if ip == ip_erro_atual:
                        ip_erro_cont += 1
                    else:
                        ip_erro_atual = ip
                        ip_erro_cont = 1

                    if ip_erro_cont > ip_erro_top_cont:
                        ip_erro_top = ip_erro_atual
                        ip_erro_top_cont = ip_erro_cont

                # FORÇA BRUTA
                if recurso == '/login' and status == 403 and ip == ip_ant:
                    seq_login += 1
                    if seq_login == 3:
                        forca_bruta += 1
                        ultimo_forca = ip
                        seq_login = 0
                else:
                    seq_login = 0

                # ADMIN
                if recurso == '/admin' and status != 200:
                    admin_erro += 1

                # DEGRADAÇÃO
                if tempo > tempo_ant:
                    crescente += 1
                    if crescente >= 3:
                        degradacao += 1
                        crescente = 0
                else:
                    crescente = 0

                tempo_ant = tempo

                # ERRO 500
                if status == 500:
                    erro500_seq += 1
                    if erro500_seq == 3:
                        falha_critica += 1
                        erro500_seq = 0
                else:
                    erro500_seq = 0

                # BOT
                if ip == ip_ant:
                    seq_ip += 1
                else:
                    seq_ip = 1

                if seq_ip >= 5 or 'Bot' in agente or 'Crawler' in agente:
                    bot += 1
                    ultimo_bot = ip

                ip_ant = ip

                # ROTAS SENSÍVEIS
                if recurso == '/admin' or recurso == '/backup' or recurso == '/config':
                    rotas += 1
                    if status != 200:
                        rotas_falha += 1

        disp = (sucesso / total) * 100
        taxa = (erro / total) * 100
        media = somaTempo / total

        estado = classificarEstado(disp, falha_critica, lento, bot)

        print('\n===== RELATÓRIO =====')
        print('Total acessos:', total)
        print('Sucessos:', sucesso)
        print('Erros:', erro)
        print('Erros 500:', erro500)
        print('Disponibilidade:', disp)
        print('Taxa erro:', taxa)
        print('Tempo médio:', media)
        print('Maior tempo:', maior)
        print('Menor tempo:', menor)

        print('Rápidos:', rapido)
        print('Normais:', normal)
        print('Lentos:', lento)

        print('200:', s200)
        print('403:', s403)
        print('404:', s404)
        print('500:', s500)

        print('Recurso mais acessado:', recurso_top)
        print('IP mais ativo:', ip_top)
        print('IP com mais erros:', ip_erro_top)

        print('Força bruta:', forca_bruta)
        print('Último IP força bruta:', ultimo_forca)

        print('Acessos indevidos /admin:', admin_erro)

        print('Degradação:', degradacao)
        print('Falhas críticas:', falha_critica)

        print('Bots:', bot)
        print('Último bot:', ultimo_bot)

        print('Rotas sensíveis:', rotas)
        print('Falhas rotas sensíveis:', rotas_falha)

        print('Estado final:', estado)
    except:
        print('Erro ao analisar arquivo')

menu()