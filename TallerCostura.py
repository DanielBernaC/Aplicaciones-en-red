import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-2s) %(message)s')

###############################################################

class Taller(object):
    def __init__(self, start=0):
        self.MangasMax = threading.Condition()
        self.MangasMin = threading.Condition()
        self.mangas = 0
        self.cuerpos = 0
        self.prenda = 0

    def incremenManga(self):
        with self.MangasMax:
            if self.mangas >= 10:
                logging.debug("No hay espacio para almacenar mas mangas")
                self.MangasMax.wait()
            else:
                self.mangas += 1
                logging.debug("Manga creada, Numero de mangas=%s", self.mangas)
        with self.MangasMin:
            if self.mangas >= 2:
                logging.debug("Mangas suficientes en cesto")
                self.MangasMin.notify()

    def decremenManga(self):
        with self.MangasMin:
            while not self.mangas >= 2:
                logging.debug("Esperando mangas")
                self.MangasMin.wait()
            self.mangas -= 2
            logging.debug("Mangas tomadas, Numero de mangas=%s", self.mangas)
        with self.MangasMax:
            logging.debug("Hay espacio para mangas en el cesto")
            self.MangasMax.notify()

    def getMangas(self):
        return (self.mangas)

    def getCuerpos(self):
        return (self.cuerpos)


    def incremenCuerpo(self):
        # verificar que la cesta de cuerpos no esté llena
        with self.MangasMax:
                if self.cuerpos >= 5 :
                    logging.debug("No hay espacio para mas cuerpos")
                    self.MangasMax.wait()
                else:
                    self.cuerpos += 1
                    logging.debug("Cuerpo creado, Numero de cuerpo = %s", self.cuerpos)
        # notificar que hay cuerpos disponibles
        with self.MangasMin:
            logging.debug("Cuerpos suficientes en el cesto")
            self.MangasMin.notify()


    def incremenPrenda(self):
         with self.MangasMin:
             while self.cuerpos == 0:
                logging.debug("Esperando cuerpos")
                self.MangasMin.wait()
             self.prenda += 1
             self.cuerpos -= 1
             logging.debug("Prenda completa creada, Numero de prenda = %s", self.prenda)


def crearManga(Taller):
    while (Taller.getMangas() <= 10):
        Taller.incremenManga()
        time.sleep(3)


def crearCuerpo(Taller):
    while (taller.getMangas() >= 0):
        # incrementarCuerpo (antes de decrementar
        # manga se debe validar que haya cupo en
        # la canasta de cuerpos)
        Taller.decremenManga()
        Taller.incremenCuerpo()
        time.sleep(3)


def ensamblaPrenda(Taller):
    while (taller.getCuerpos() >= 0):
        Taller.incremenPrenda()
        logging.debug('Ensamblando todo')
        time.sleep(3)


taller = Taller()

Costurera1 = threading.Thread(name='Costurera1(mangas)', target=crearManga, args=(taller,))
Costurera2 = threading.Thread(name='Costurera2(cuerpos)', target=crearCuerpo, args=(taller,))
Costurera3 = threading.Thread(name='Costurera3(prenda)', target=ensamblaPrenda, args=(taller,))

Costurera1.start()
Costurera2.start()
Costurera3.start()

Costurera1.join()
Costurera2.join()
Costurera3.join()