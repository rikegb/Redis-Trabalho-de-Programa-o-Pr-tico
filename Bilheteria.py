import redis

class FilaDeIngressos:
    def __init__(self):
        self.redis_cliente = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.chave_fila = 'fila_de_ingressos'

    def adicionar_pessoa(self, nome):
        """Adiciona uma pessoa à fila."""
        if not self.redis_cliente.exists(self.chave_fila):
            self.redis_cliente.hset(self.chave_fila, '0', 0)  # Cria a chave como um hash com valor 0
        posicao = int(self.redis_cliente.hget(self.chave_fila, '0') or 0) + 1
        self.redis_cliente.hset(self.chave_fila, '0', posicao)
        self.redis_cliente.hset(self.chave_fila, posicao, nome)
        return posicao

    def exibir_fila(self):
        """Exibe a fila."""
        dados_fila = self.redis_cliente.hgetall(self.chave_fila)
        for posicao, nome in sorted(dados_fila.items(), key=lambda x: int(x[0])):
            print(f'Posição: {posicao.decode()}, Nome: {nome.decode()}')

    def remover_pessoa(self):
        """Remove a primeira pessoa da fila e exibe seus dados."""
        posicao = self.redis_cliente.hget(self.chave_fila, '0')
        if posicao:
            posicao = int(posicao)
            if posicao > 0:  # Verifica se há alguém na fila
                nome = self.redis_cliente.hget(self.chave_fila, '1')  # Obtém o nome da primeira pessoa da fila
                if nome:  # Verifica se há alguém na fila
                    print(f'Pessoa removida: Nome: {nome.decode()}, Posição: 1')
                    self.redis_cliente.hdel(self.chave_fila, '1')  # Remove a primeira pessoa da fila
                    # Atualiza a posição
                    self.redis_cliente.hset(self.chave_fila, '0', posicao - 1)
                else:
                    print('Fila vazia')
            else:
                print('Fila vazia')
        else:
            print('Fila vazia')

def principal():
    fila_de_ingressos = FilaDeIngressos()

    while True:
        print("\n1. Adicionar pessoa à fila")
        print("2. Exibir fila")
        print("3. Remover pessoa do topo da fila")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Digite o nome da pessoa: ")
            posicao = fila_de_ingressos.adicionar_pessoa(nome)
            print(f'{nome} adicionado à fila na posição {posicao}')
        elif escolha == '2':
            print("\nFila de ingressos:")
            fila_de_ingressos.exibir_fila()
        elif escolha == '3':
            fila_de_ingressos.remover_pessoa()
        elif escolha == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    principal()
