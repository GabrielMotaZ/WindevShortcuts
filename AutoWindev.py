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

print("-------------------------------")
print("Auto assign dados com objeto\n\n")

select = select.replace("	", "")
select = select.replace("\n", "")

select = select.replace(" ","")

select = select.split(",")

for i in select:
    print(objeto+"."+i+" = dados."+i)





print("-------------------------------")
print("Auto insert\n\n")


selectList = select.copy()

print("insert into {}(".format(nomeTabela))

for idx, x in enumerate(select):
    print(x, end = "")
    if idx == len(select) - 1:
        print("")
    else:
        print(",")


print(")\nVALUES(")

for x in range(len(selectList)):
    selectList[x] = "'%" + str(x+1) + "'"

for idx, x in enumerate(selectList):
    print(x, end = "")
    if idx == len(select) - 1:
        print("")
    else:
        print(",")

print(")")





print("-------------------------------")
print("Auto if variavel <> 0\n\n")


for i in select:
    print("""IF linhaTelefonica.{0} <> 0 AND linhaTelefonica.{0} <> "" THEN
	str += CR + "AND {0} LIKE '%" + linhaTelefonica.{0} + "%'"
END""".format(i) + "\n")



