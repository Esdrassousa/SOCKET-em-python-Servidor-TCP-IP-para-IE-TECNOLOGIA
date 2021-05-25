import socket, threading
from datetime import datetime
from pymongo import MongoClient
import re

client  = MongoClient('localhost', 27017)
db_id2 = client['corrente_id=2']
db_id3 = client['corrente_id=3']
def run(conn):
    while True:
        data = conn.recv(400) # receber informacao
        data = conn.recv(400)
        if not data: # se o cliente tiver desligado
            conns.remove(conn)
            break
        else:
            data_e_hora_atuais = datetime.now()
            data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
            # print(data[id])
            resposta = data.decode()
            divide_dados = resposta.split('&')
            SomenteNumerosCorrente = re.sub('[^0-9]', '', divide_dados[4])
            transFormaCorrenteInt = int(SomenteNumerosCorrente)/100
            print(data_e_hora_em_texto)
            print(transFormaCorrenteInt)
            
            if divide_dados[0]=='id=2':
                corrente = {
                "_id":data_e_hora_em_texto,
                "corrente":transFormaCorrenteInt
                }
            
                correntes = db_id2.correntes
                correntes.insert(corrente)
            else:
                
                corrente = {
                    "_id":data_e_hora_em_texto,
                    "corrente":transFormaCorrenteInt
                    }
                
                correntes = db_id3.correntes
                correntes.insert(corrente)
                
conns = set() # armazenar conxoes aqui
host, port = ('192.168.100.201', 1883)
with socket.socket() as sock: # ligacao TCP
    socket.socket(socket.AF_INET, socket.SOCK_STREAM)# reutilizar endereco logo a seguir a fechar o servidor
    sock.bind((host, port))
    sock.listen(2) # servidor ativo
    print('Server started at {}:{}\n'.format(host, port))
    while True:
        conn, addr = sock.accept() # esperar que alguem se conect
        conns.add(conn) # adicionar conexao ao nosso set de coneccoes
        threading.Thread(target=run, args=(conn,)).start() # esta coneccao vai ser independente das outra a partir de agora, vamos correr a thread na funcao run

