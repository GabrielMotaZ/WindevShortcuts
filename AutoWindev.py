objeto = "linhaTelefonica" # nome da classe
select = """
	id,
	bitAtivo,
	chipMovel,
	linhaFixa,
	pacoteDados,
	operadora,
	idFuncionario,
	idFornecedor,
	idEquipamento,
	idDepartamento
""" # select do banco de dados
nomeTabela = "LinhaTelefonica"

#
#Listar
#

print("""Listar(array{0} is array of {0}, {1} is {0})

base is BaseDeDados
conexao is connection = base.conectar()
dados is data source

str is string = [""".format(objeto.capitalize(),objeto))
print(select)
print("""FROM {0}]\n\n""".format(nomeTabela))

select = select.replace("	", "")
select = select.replace("\n", "")

select = select.replace(" ","")

select = select.split(",")

for i in select:
    print("""IF {0}.{1} <> 0 AND {0}.{1} <> "" THEN
	str += CR + "AND {1} LIKE '%" + {0}.{1} + "%'"
END""".format(objeto, i) + "\n")

print("""hreadfirst
for each dados""")

for i in select:
    print("	"+objeto+"."+i+" = dados."+i)

print("\n	ArrayAdd(" + objeto.capitalize() + ", " + objeto + ")")
print("end")

print("""\nbase.desconectar(conexao)

RESULT resultado\n\n\n""")


#
#Cadastrar
#


print("""Cadastrar({0} is {1})

base is BaseDeDados
conexao is connection = base.conectar()

str is string = [""".format(objeto, objeto.capitalize()))


selectList = select.copy()

print("\ninsert into {}(".format(nomeTabela))

for idx, x in enumerate(select):
    print("	"+x, end = "")
    if idx == len(select) - 1:
        print("")
    else:
        print(",")


print(")\nVALUES(")

for x in range(len(selectList)):
    selectList[x] = "	'%" + str(x+1) + "'"

for idx, x in enumerate(selectList):
    print(x, end = "")
    if idx == len(select) - 1:
        print("")
    else:
        print(",")

print(")")

print("""]

resultado is boolean = base.ExecutarComando(str,conexao)

base.desconectar(conexao)

RESULT resultado\n\n\n""")


#
#Atualizar
#

print("""Atualizar(teste* is Teste*)

if teste.id = 0 then
    RESULT False
end

base is BaseDeDados
conexao is connection = base.conectar()

str is string = [
    UPDATE {0}
    SET""".format(nomeTabela))

for i in select:
    print("""IF {0}.{1} <> 0 AND {0}.{1} <> "" THEN
	str += "{1} = " + {0}.{1}
END""".format(objeto, i) + "\n")

print("""
str += CR + "WHERE id = " + teste.id

resultado is boolean = base.ExecutarComando(str,conexao)

RESULT resultado
""")
