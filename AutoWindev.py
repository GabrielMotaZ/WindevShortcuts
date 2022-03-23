objeto = "endereco" # nome da classe
select = """
       [IDCliente]
           ,[CEP]
           ,[logradouro]
           ,[numero]
           ,[complemento]
           ,[bairro]
           ,[cidade]
           ,[UF]
           ,[cadastroAtualizadoERP]
           ,[celularContato]
           ,[telefoneContato]
           ,[tipoEndereco]
           ,[principal]
""" # select do banco de dados
select = select.replace("[","")
select = select.replace("]","")
nomeTabela = "Endereco"

#
#Listar
#

print("""PROCEDURE Listar(array{0} is array of {0}, {1} is {0})

base is BaseDeDados
conexao is connection = base.conectar()
dados is data source

str is string = [
SELECT""".format(objeto.capitalize(),objeto))
print(select)
print("""   FROM {0}
	WHERE 1 = 1
]\n\n""".format(nomeTabela))

select = select.replace("	", "")
select = select.replace("\n", "")

select = select.replace(" ","")

select = select.split(",")

for i in select:
    print("""IF {0}.{1} <> 0 AND {0}.{1} <> "" THEN
	str += CR + "AND {1} LIKE '%" + {0}.{1} + "%'"
END""".format(objeto, i) + "\n")

print("resultado is boolean = base.ExecutarComando(str,conexao,dados)")


print("""
IF HNbRec(dados)=0 THEN
    resultado = False
ELSE
    hreadfirst(dados)
    for each dados""")

for i in select:
    print("		"+objeto+"."+i+" = dados."+i)

print("\n	ArrayAdd(array" + nomeTabela + ", " + objeto + ")\n	end")
print("end")

print("""\nbase.desconectar(conexao)

RESULT resultado\n\n\n""")


#
#Cadastrar
#


print("""PROCEDURE Cadastrar({0} is {1})

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

print("""PROCEDURE Atualizar({0} is {0})

if {1}.id = 0 then
    RESULT False
end

base is BaseDeDados
conexao is connection = base.conectar()

str is string = [
    UPDATE {1}
    SET
    """.format(objeto, nomeTabela))


counter = 1
for i in select:
    print("	{0} = %".format(i) + str(counter), end = "")
    if counter != len(select):
        print(",")
    else:
        print("")
    counter += 1

print("""
    where id = %{0}
]

""".format(counter))

print("str = stringbuild(str, ")
counter = 1
for i in select:
    print("	"+objeto+"."+i+' <> "" and '+objeto+"."+i+""" <> 0 ? "'" + """+objeto+"."+i+""" + "'" """, end = "")
    if counter != len(select):
        print(",")
    else:
        print(")")
    counter += 1

print("""
resultado is boolean = base.ExecutarComando(str,conexao)

base.desconectar(conexao)

RESULT resultado
""")
