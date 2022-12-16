from flask import Flask, render_template, request, redirect, session, flash, url_for
from database import usuari, reserva
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/', methods = ['POST', 'GET'])
def index():
    #Si arriben dades per post
    if request.method == 'POST':
        #Comprova que la data s'hagui inserit
        data = request.form['data']
        #Es comprova que el camp de la data no estigui buit
        if data =="":
            flash('No está la data definida', 'error')
            return redirect(url_for('index')) 
        else:            
            hora = request.form['hora']
            nom = request.form['nom']
            instalacio = request.form['instalacio']        
            nom = int(nom)
            #La data es descomposa per treure el dia, el mes i l'any
            dataD = data.split("-")
            dia = dataD[2]
            mes = dataD[1]
            anyo = dataD[0]     
            #Es torna composar amb la forma correcta per enmagazenar a la base de dades       
            dt = datetime.strptime(
            dia + '/' + mes +'/' + anyo[2] + anyo[3] +' ' + hora, "%d/%m/%y %H:%M")
            formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            #S'enmagazena a quina setmana pertany
            setmana = dt.isocalendar().week
            diaSetmana = dt.weekday()

        #Es comproba que no sigui dissabte ni diumenge
        if diaSetmana == 5 or diaSetmana == 6:            
            flash('Els caps de setmana no hi ha reserves', 'error')
            return redirect(url_for('index')) 

        else: 
            #Es comprova que no existeix la reserva 
            totesReserves=reserva.carregaReserves()             
            for reservaComp in totesReserves: 
                if reservaComp['data']==dt and reservaComp['tipus']==int(instalacio):
                    flash('Aquesta data ja està reservada', 'error')
                    return redirect(url_for('index', seccio="nova-reserva")) 
            #Si no está duplicada enmagazena les dades a la base de dades  
            novaReserva=reserva.guardaReserva(formatted_date, nom, instalacio, setmana)            
            flash('Reserva afegida de forma satisfactoria', 'exit')
            return redirect(url_for('index', seccio="reserves"))     
    #Si les dades arriben per get
    else:  
        avui = datetime.now()  
        seccio = request.args.get("seccio") 
        #Si seccio esta definit determinará a quina pestanya es situarà
        if seccio is None:
            seccio = ""
        else:
            seccio = request.args.get("seccio") 
        #Si la setmana esta definida mostrara la setmana pertinent
        setm = request.args.get("setmana") 
        if setm is None:
            setm = avui.isocalendar().week
        else:
            setm = request.args.get("setmana")                      
         
        #Carrega els usuaris i les dades de les reserves segons la setmana
        llistaUsuaris=usuari.carregaUsuaris()   
        llistaReserves=reserva.carregaReservesPerSetmana(int(setm))         
        #Es crea un diccionari amb les dades de les reserves segons la setmana
        taula=[]	
        for fila in range(0,5):
            filaTemp=[]
            for columna in range(0,6):
                tempVal=[]
                for res in llistaReserves:
                    if int(res['data'].weekday())==fila and int(res['data'].hour)==columna+15:
                        if res['tipus'] == 0:
                            instalacio = "Coberta"
                        else:
                            instalacio = "Exterior"    
                        for usu in llistaUsuaris:
                            if int(usu['id_usuari'])==int(res['id_usuari']):
                                usuario = usu['nom'] + " " + usu['llinatges'] + " [" + instalacio + "]" 
                        tempVal.append(usuario)
                filaTemp.append(tempVal) 
            taula.append(filaTemp)

        return render_template('home.html',usuaris=llistaUsuaris,reserves=taula, setmanaActual=int(setm), seccio=seccio)

@app.route('/nou-usuari', methods = ['POST', 'GET'])
def nouUsuari():
    #Si les dades arriben per post es que s'ha onplit un formulari previament
    if request.method == 'POST':
        nom = request.form['nom']
        llinatges = request.form['llinatges']
        telefon = request.form['telefon']
        #S'enmagazena la informació del nou usuari a la base de dades
        nouUsuari=usuari.guardaUsuari(nom,llinatges,telefon)        
        flash('Nou usuari afegit corretament', 'exit')
        #Redirigeix a la pàgina inicial amb un missatge flash
        return redirect(url_for('index', seccio="usuaris"))         
    
    else:
        # Si les dades arriben per GET mostra el formulari
        return render_template('nou-usuari.html')

#Rutes per borrar, editar i actualitzar l'usuari
@app.route('/del-usuari')
def deleteUsuari():
    idusuari= request.args.get('id_u')	
    usuari.eliminaUsuari(idusuari)    
    flash('Usuari esborrat amb èxit', 'exit')    
    return redirect(url_for('index', seccio="usuaris"))  

@app.route('/edit-usuari')
def editUsuari():
    idusuari= request.args.get('id_u')	
    llistaUsuari=usuari.editarUsuari(idusuari)  
    return render_template('edit-usuari.html', usuari=llistaUsuari)
    
@app.route('/update-usuari', methods = ['POST', 'GET'])
def updateUsuari():
    if request.method == 'POST':
        nom = request.form['nom']
        llinatges = request.form['llinatges']
        telefon = request.form['telefon']
        id_us = request.form['id_usuari']
        nouUsuari=usuari.actualitzarUsuari(id_us,nom,llinatges,telefon)
        
        flash('Usuari editat de forma correta', 'exit')
        return redirect(url_for('index', seccio="usuaris"))  
    else:
        flash('No se qué ha passat')
        flash('nova-reserva', 'seccio')
        return redirect(url_for('index'))
     

if __name__ == '__main__':
    app.run(debug=True)
