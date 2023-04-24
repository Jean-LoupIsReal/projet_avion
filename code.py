# pyright: reportShadowedImports=false
from InitProjet import *
import time
import math


#========================================== Déclaration Fonctions Lecture Données ==========================================
def lectSonar():
    try:
        if sonar.distance < 10:
            return etat1()
    except:
        pass


def valeurJoystick(joystickValeur):
    #transforme valeur potentiometre en valeur entre -1 et 1
    if joystickValeur < 29000:
        valeur = ((30000-joystickValeur-500)/25000)*1
    elif joystickValeur > 38000:
        valeur = ((joystickValeur - 38000)/(52000-38000))*-1
    else:
        valeur = 0
    
    #s'assure que les valeurs soient bien entre -1 et 1
    if valeur < -1:
        valeur = -1
    elif valeur > 1:
        valeur = 1
    
    return valeur


#========================================== Déclaration Fonctions Mathematiques ==========================================
#Calcul l'angle du joystick selon arctan2 (cercle trigonometrique)
def angleJoystick(x, y):
    angle = math.degrees(math.atan2(y, x))
    return angle % 360


#========================================== Déclaration Fonctions Control Electronique ==========================================
#controle de l'anneau neopixel
def controleAnneau(x , y):
    #prend l'angle du joystick
    angle = angleJoystick(x,y)
    #vérifie si le joystick est au repos
    
    if x == 0  and y == 0:
        for i in range(8):
            anneauNeo[i] = couleurNeo["noir"]
    else:
        nbLed = round(angle/45, 0)
        for i in range(8):
            if i == nbLed:
                anneauNeo[i] = couleurNeo["blanc"]
            else:
                anneauNeo[i] = couleurNeo["noir"]
        #pour tests
    anneauNeo.show()


#controle du moteur DC avec joystick (en y)
def DCMoteurJoystickY(joystickValeur):
    vitesse = joystickValeur
    DCMotor.throttle = vitesse
    return vitesse


#Controle le servomoteur avec joystick (en x)
def ServomoteurJoystickX(joystickValeur):
    #la valeur du joystick en X determine l'angle du moteur
    angle = joystickValeur * 90 + 90
    servoMoteur.angle = angle
    return angle


#========================================== Déclaration Fonction Lecture données ==========================================
# Lecture du sonar
def lectSonar():
    try:
        if sonar.distance < 10:
            return etat1()
    except:
        pass



#========================================== Déclaration Fonction Boucle ==========================================
#Boucle qui demande 
def demandeSW():
    print("Veuillez allumer l'interrupteur")
    while True:
        interruteurAllume = not tca.input_value[switch]
        if interruteurAllume:
            return etat3()
        else:
            pass
        time.sleep(0.1)




#========================================== Déclaration Fonctions états ==========================================
#Étape1 
def etat1():
    # S'assure que les moteurs et l'anneau reviennent a leurs valeurs initiales.
    servoMoteur.angle = 90
    controleAnneau(0,0)
    vitesse = DCMoteurJoystickY(0)

    # Définie la LED neopixel en rouge.
    neoLed[0] = couleurNeo["rouge"]

    #Imprime un message a l'utilisateur
    print("\n",
       "Veuillez valider votre carte :",
       "\n")

    while True:
        (stat, tag_type) = RFID.request(RFID.REQIDL)
        # Vérifie si une carte est devant le lecteur.
        if stat == RFID.OK:
            print("clée detecte")
            # Donne les valeurs de la carte.
            (stat, raw_uid) = RFID.anticoll()
            # Vérifie le code de la carte.
            if raw_uid == codeCarte: 
                # Entre dans l'etape 2.
                return etat2()
        #envois l'info de la dht a thingspeak
        envoisWifi()
        time.sleep(0.1)
        
                    

def etat2():
    global destination
    print("\n",
        "Veuillez entrer le code de l'aeroport",
        "\n")
    neoLed[0] = couleurNeo["jaune"]
    code = ""

    while True:
        if tca.key_int:
            # Regarde si plusieurs touches ont été appuiyé en meme temps.
            events = tca.events_count
            # Execute le ou les evenements.
            for _ in range(events):
                keyevent = tca.next_event
                #Strip keyevent
                event = keyevent & 0x7F
                event -= 1
                # Lit le numero de la row.
                row = event // 10
                # Lit le numero de la colonne.
                col = event % 10
                # Définit le nom de la touche.
                touche = keymap[col][row]
                # S'assure que le chiffre est entré qu'une seule fois par appui.
                if keyevent & 0x80:
                    # La touche "#" ramène l'utilisateur a l'etape 1.
                    if touche == "#":
                        print("\n",
                            "De retour a l'etape 1",
                            "\n")
                        return etat1()

                    # La touche "*" suprime le dernier charactère entré.
                    elif touche == "*":
                        code = code[:-1]
                    
                    # Ajoute la touche appuiyé au code. (obligatoirement un chiffre)
                    else:
                        code += touche

                    # Imprime le code entré pour l'utilisateur.
                    print(code)

                    # Vérifie si le code entrée est valide.
                    if len(code) == 3:
                        if code in aeroports:
                            destination = aeroports[code]
                            print("\n",
                            "Votre destination est :", destination,
                            "\n")
                            return demandeSW()
                        else:
                            print("\n",
                            f"Le code {code} est invalide veuillez l'entrer de nouveau",
                            "\n")
                            code = ""
            tca.key_int = True  # clear the IRQ by writing 1 to it.
        #envois l'info de la dht a thingspeak
        envoisWifi()
        # S'assure de ne pas bruler la chip.
        time.sleep(0.005)


def etat3():
    # Change la couleur de la neopixel.
    neoLed[0] = couleurNeo["vert"]

    # Déclare les variables necessaire aux fonctionnement du code.
    autopilote = 0
    valBoutonDerniereBoucle = 0
    tempsAffichage = time.monotonic()
    while True:
        # S'assure que le bonton active le if qu'une seule fois.
        valBouton = not joystickSW.value
        # Prends la valeur de l'interrupteur.
        interrupteurAllume = not tca.input_value[switch]
        
        # Prend la temperature et l'humidite du dht.
        try:
            temperature = dhtDevice.temperature
            humidite = dhtDevice.humidity
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going.
            print(error.args[0])
            time.sleep(2.0)
        except Exception as error:
            dhtDevice.exit()
            raise error

        # Si le bouton du joystick est appuyé, puis relaché, active l'autopilote.
        if valBoutonDerniereBoucle == 1 and valBouton == 0:
            autopilote = not autopilote
        
        # Change la valeur de la variable apres qu'elle soit utilisé pour preparer prochaine loop.
        valBoutonDerniereBoucle = valBouton

        # Si l'autopilote est activé, le programe ne change pas les valeurs du joystick.
        if not autopilote:
            #Crée des valeurs normalisés a partir des valeurs du joystick. (de -1 à 1).
            valeurJoystickX = valeurJoystick(joystickX.value)
            valeurJoystickY = valeurJoystick(joystickY.value)
        
        
        # Controle l'anneau de LED.
        controleAnneau(valeurJoystickX, valeurJoystickY)
        
        # Controle le servomoteur et retourne son angle.
        angleServo = ServomoteurJoystickX(valeurJoystickX)
        
        # Controle le moteur DC et retourne sa vitesse.
        vitesse = DCMoteurJoystickY(valeurJoystickY)
        vitesse = vitesse * 100

        # Donne la valeur du sonar.
        #distSonar = lectSonar()

        # Affiche les parametres toutes les 100ms.
        if tempsAffichage + 0.1 <= time.monotonic(): #si le timer est plus grand ou = a 100ms.
            print(
                f"vit = {vitesse}%, servo = {angleServo}°, destination = {destination}, Temp = {temperature}°, Hum= {humidite}%"
                )
            # Réinitialise le temps pour la condition
            tempsAffichage = time.monotonic()
        
        # Si l'interrupteur se ferme, remet tout a la valeur de départ et reviens a l'étape 1
        if not interrupteurAllume:
            return etat1()
        #envois l'info de la dht a thingspeak
        envoisWifi()
        time.sleep(0.01)
        
def etatInitial():
    etat = etat1()

etatInitial()
