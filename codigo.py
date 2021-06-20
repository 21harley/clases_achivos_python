class Turno:
    def __init__(self,id_turno,hora_inicio,hora_fin):
        self.id_turno=id_turno
        self.hora_inicio=hora_inicio
        self.hora_fin=hora_fin
        
    def __repr__(self):
        return str(self.__dict__)

class Turno_Dia(Turno):
    
    def __init__(self,id_turno,hora_inicio,hora_fin,minuto_atras_o_permitido):
        Turno.__init__(self,id_turno,hora_inicio,hora_fin)
        self.minuto_atras_o_permitido=minuto_atras_o_permitido
        

class Turno_Tarde(Turno):
    def __init__(self,id_turno,hora_inicio,hora_fin,minuto_retiro_anticipado):
        Turno.__init__(self,id_turno,hora_inicio,hora_fin)
        self.minuto_retiro_anticipado=minuto_retiro_anticipado


class Planificacion:
    def __init__(self,dia,estado,atraso,retirno_antisipado):
        self.Dia=dia
        self.estado=estado
        self.atraso=atraso #listas
        self.retirno_antisipado=retirno_antisipado #listas

    def __repr__(self):
        return str(self.__dict__)

class Marca:
    def __init__(self,dia,hora,tipo):
        self.Dia=dia
        self.hora=hora
        self.tipo=tipo
        
    def __repr__(self):
        return str(self.__dict__)

class Usuario:
    def __init__(self,identificador,nombre,marcas,planificacion):
        self.identificador=identificador
        self.nombre=nombre
        self.marcas=marcas #lista
        self.planificacion=planificacion #lista

    def __repr__(self):
        return str(self.__dict__)    
        #marcar retorna los dias y  minutos trabajados 
    def Marca(self):
        aux=list()
        ultF=""
        horaE=""
        horaS=""
        for item in self.marcas:
            if(item.Dia!=ultF and item.tipo=='1'):
                ultF=item.Dia
                horaE=item.hora.split(":")
            elif(item.Dia==ultF and item.tipo=='2'):
                horaS=item.hora.split(":")
                token1=ultF.split("-")
                orden=0
                for orden1 in self.planificacion:
                    fechaP=orden1.Dia.split("-")
                    if(int(token1[2])==int(fechaP[2])):
                        orden=orden1
                        break
                hora=(int(horaS[0])-int(horaE[0]))*60
                v1=0
                v2=0
                timeR=orden.retirno_antisipado
                timeA=orden.atraso
                if(type(timeR)==str):
                    timeR=int(timeR)
                else:
                    timeR=int(timeR.minuto_retiro_anticipado)
                if(type(timeA)==str):
                    timeA=int(timeA)
                else:
                    timeA=int(timeA.minuto_atras_o_permitido)
                if(60-int(horaS[1])<=timeR and timeR>0 ):
                    v1=timeR
                if(int(horaE[1])<=timeA):
                    v2=timeA
                minuto=(int(horaS[1])+v2)-(int(horaE[1])+v1)
                totalM=hora+minuto
                aux.append([ultF,totalM])
        return aux;
        
    def Informe(self):
        listR=list()
        diasTra=self.Marca()
        #cargo datos solicitados en listR
        for item in self.planificacion:
            estado=0
            horaInicio=""
            horaFinal=""
            timeR=item.retirno_antisipado
            timeA=item.atraso
            if(type(timeR)!=str):
                horaInicio=timeR.hora_inicio
                horaFinal=timeR.hora_fin
            if(type(timeA)!=str):
                horaInicio=timeA.hora_inicio
                horaFinal=timeA.hora_fin
            for dia in diasTra:
                token1=item.Dia.split("-")
                token2=dia[0].split("-")
                if(token1[2]==token2[2] and token1[1]==token2[1]):
                    estado=1
                    listR.append([item.Dia,horaInicio,horaFinal,"True",dia[1]])
            if(estado==0):
                listR.append([item.Dia,horaInicio,horaFinal,"False","0"])
        #cargo datos en rut.txt
        textfile=open(self.identificador+".txt","w")
        for d in listR:
            textfile.write(d[0]+";"+d[1]+";"+d[2]+";"+d[3]+";"+str(d[4])+"\n")
        textfile.close()

class Administrador(Usuario):
    def __init__(self,identificador,nombre,marcas,planificacion):
        Usuario.__init__(self,identificador,nombre,marcas,planificacion)
        
    def Asiganar_turnos(self):
        #cargar archivos
        usuarios=list()
        with open("Usuarios.txt") as f:
            for linea in f:
                usuarios.append(linea.replace("\n",""))
        
        marcas=list()
        with open("Marcas.txt") as f:
            for linea in f:
                marcas.append(linea.replace("\n",""))
        
        planificacion=list()
        with open("Planificacion.txt") as f:
            for linea in f:
                planificacion.append(linea.replace("\n",""))
        
        turnos=list()
        with open("Turnos.txt") as f:
            for linea in f:
                turnos.append(linea.replace("\n",""))

        #cargo turno
        atraso=list()
        retirno_antisipado=list()
        for turno in turnos:
            token=turno.split(";")
            if(token[4]=="1"):
               aux=Turno_Dia(token[0],token[1],token[2],token[3])
               atraso.append(aux)
            else:
               aux=Turno_Tarde(token[0],token[1],token[2],token[3])
               retirno_antisipado.append(aux)
       
        #cargo planificacion
        tuplasP=list()
        ultU=""
        cont=-1
        for p in planificacion:
            token=p.split(";")
            if(ultU!=token[5]):
                tuplasP.append([token[5],list()])
                ultU=token[5]
                cont+=1
        
            if(ultU==token[5]):
                resp,valor1=consulta(atraso,retirno_antisipado,token[0])
            if(resp==1):
                aux=Planificacion(token[1],token[2],valor1,token[4])
                tuplasP[cont][1].append(aux)
            else:
                aux=Planificacion(token[1],token[2],token[3],valor1)
                tuplasP[cont][1].append(aux)

        #cargo marcas
        tuplasM=list()
        ultU=""
        cont=-1
        for m in marcas:
            token=m.split(";")
            if(ultU!=token[0]):
                tuplasM.append([token[0],list()])
                ultU=token[0]
                cont+=1
        
            if(ultU==token[0]):
                aux=Marca(token[1],token[2],token[3])
                tuplasM[cont][1].append(aux)

        #cargar usuarios
        listaUsuarios=list()
        for usuario in usuarios:
            token=usuario.split(";")
            lis1,lis2=consulta1(tuplasM,tuplasP,token[0])
            aux=Administrador(token[0],token[1],lis1,lis2)
            listaUsuarios.append(aux)
        for Usuario in listaUsuarios:
            Usuario.Informe()
        
#consulta tipo de turno
def consulta(atraso,retirno_antisipado,codigo):
    for a in atraso:
        if(a.id_turno==codigo):
            return 1,a
    for r in retirno_antisipado:
        if(r.id_turno==codigo):
            return 2,r
        
#consulta para datos de lista de marcas y planificacion
def consulta1(tuplasM,tuplasP,codigo):
    respM=list()
    respP=list()
    for m in tuplasM:
        if(m[0]==codigo):
            respM=m[1]
    for p in tuplasP:
        if(p[0]==codigo):
            respP=p[1]
    return respM,respP

#creo el administrador y activo Asiganar_turnos
luis=Administrador("14251F","Luis",0,0)
luis.Asiganar_turnos()
