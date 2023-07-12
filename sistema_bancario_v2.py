import textwrap

def menu():
  menu = '''\n
  ==================== MENU ====================
  [d]\tDepositar
  [s]\tSacar
  [e]\tExtrato
  [u]\tCriar Usuario
  [c]\tCriar conta
  [l]\tListar Contas
  [q]\tSair
  
  => '''
  return input(textwrap.dedent(menu))

def saque(*,numero_saques,saldo,limite,LIMITE_SAQUES,extrato):
  if numero_saques < LIMITE_SAQUES:
    valor = float(input("Quanto deseja sacar? \n=>"))
    if valor > 0:   
        if valor <= limite:
            if valor < saldo:
                saldo -= valor
                extrato += f"Saque:\t\tR${valor: .2f}\n"
                numero_saques += 1
                print('=== Saque realizado com sucesso! ===')
            else:
                print(f"### Saldo Insuficiente! ###\n### O valor ultrapassa o saldo atual de R$ {saldo: .2f} ###")
        else:
            print(f"### Limite Excedido! ###\n### O valor ultrapassa o limite atual de R$ {limite: .2f} ###")
    else:
        print("### Operação Falhou! ###\n### O valor informado não é válido. ###")
  else:
    print("### Limite de saques diários excedido! ###")
  return extrato, saldo, numero_saques
  
def deposito(saldo, extrato):
  valor = float(input("Quanto deseja depositar? \n=>"))
  if valor > 0:   
    saldo += valor
    extrato += f"Depósito:\t\tR${valor: .2f}\n"
    print('=== Depósito realizado com sucesso! ===')
  else:
     print("### Operação Falhou! ###\n### O valor informado não é válido. ###")
  return saldo, extrato
  
def extrato_conta(saldo, *, extrato):
  print(' EXTRATO '.center(50,'='))
  if extrato:
    print(f"{extrato}\nSaldo:\t\tR${saldo: .2f}")
  else:
     print(f"Não foram realizadas movimentações.\nSaldo: R${saldo: .2f}")
  print("="*50)
  
def cria_user(USERS):
  cpf = input('Digite seu cpf: ')
  cpf = format_cpf(cpf)
  if verifica_cpf(cpf, USERS) == True:
    nome = input('Digite o seu nome: ')
    data_nasc = input('Digite sua data de nascimento: ')
    log = input('Digite seu logradouro: ')
    num = input('Digite o n°: ')
    bairro = input('Digite seu bairro: ')
    cidade = input('Digite sua cidade: ')
    uf = input('Digite sua UF: ')
    end = log + ' - ' + num + ' - ' + bairro + ' - ' + cidade + '/' + uf.upper()
    new_user = [cpf, nome, data_nasc, end]
    print("=== Usuário criado com sucesso! ===")
    return new_user
  else:
    print('### Cpf já cadastrado! ###')
    return False

def cria_conta(new_account, USERS):
  user = input('Digite o cpf do usuario: ')
  user = format_cpf(user)
  if verifica_cpf(user, USERS) == False:
    new_account += 1 
    return new_account, user
    print('=== Conta criada com sucesso! ===')
  else:
    print('### Usuário não cadastrado! ###')
    return False, False
  
def verifica_cpf(cpf, USERS):
  if USERS.get(cpf) == None:
    return True
  else:
    return False

def format_cpf(cpf):
  cpf = cpf.replace('.','')
  return cpf.replace('-','')

def list_contas(contas):
  for conta in contas:
    linha = f'''\
      Agência:\t{conta['agencia']}
      C/C:\t\t{conta['numero_conta']}
      Titular:\t{conta['usuario']['nome']}
    '''
    print('='*100)
    print(textwrap.dedent(linha))

  if len(contas) == 0:
    print('### Não há contas cadastradas! ###')

def main():
  saldo, limite, numero_saques, num_conta = 0, 500, 0, 0
  extrato = ""
  AGENCIA = '0001'
  LIMITE_SAQUES = 3
  USERS = {}
  contas = []
  
  while True:
    option = menu()
    match option:
        case "d":
          saldo, extrato = deposito(saldo, extrato)
            
        case "s":
          extrato, saldo, numero_saques = saque(numero_saques = numero_saques, saldo = saldo, limite = limite, LIMITE_SAQUES = LIMITE_SAQUES, extrato = extrato)
          
        case "e":
          extrato_conta(saldo, extrato = extrato)

        case "u":
          new_user = cria_user(USERS)
          if new_user != False:
            USERS[new_user[0]] = {'nome' : new_user[1], 'data_de_nascimento' : new_user[2], 'endereço' : new_user[3], 'contas' : {}}

        case "c":
          new_account, user = cria_conta(num_conta, USERS)
          if new_account != False:
            num_conta = new_account
            pos = len(contas)
            USERS[user]['contas'][pos] =  {'agencia' : AGENCIA, 'conta' : new_account}
            contas.append({'agencia' : AGENCIA, 'numero_conta' : new_account, 'usuario' : { 'nome' : USERS[user]['nome'] } })

        case "l":
          list_contas(contas)
    
        case "q":
            break
        case _:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()