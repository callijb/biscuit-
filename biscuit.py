import pygame 
import random 
import sys, os
import math 

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def main(): 
    #Initialisieren aller Pygame-Module 
    pygame.init()
    #Fenster erstellen 
    screen = pygame.display.set_mode((800,600))

    #Titel des Fensters setzen 
    pygame.display.set_caption("Flippy")

    #Mauszeiger nicht verstecken 
    pygame.mouse.set_visible(1)

    #Tastendrücke wiederholt senden
    pygame.key.set_repeat(100,100) 

    #Nachrichtenschleife: das Fenster soll länger als ein Frame angezeigt werden 
    clock = pygame.time.Clock()
   
    

    #Hintergrund: Wohnzimmer 
    background = pygame.image.load(resource_path("Wohnzimmer5.png")).convert()
    background = pygame.transform.scale(background, (800,600))
    dark = pygame.Surface((800,600))
    dark.set_alpha(120)
    dark.fill((0,0,0))

    # Start- Button 
    start_font = pygame.font.Font(resource_path('Pixel Game.otf'),60)
    start = start_font.render("Press ENTER to feed Biscuit",1, (0,153,0))
    green = pygame.Surface((800,600))
    green.set_alpha(30)
    green.fill((0,153,0))


    # score als text 
    score = 0
    font = pygame.font.Font(resource_path('Pixel Game.otf'),30)
    text = font.render("SCORE: %d" %score,1, (0,0,205)) 
    text_rect = text.get_rect()
    

    # Funktion: Highscore in einer Text-Datei speichern 
    def save_highscore(highscore): 
        path = os.path.join(os.path.expanduser("~"), "biscuit_highscore.txt")
        with open(path, "w") as file: 
            file.write(str(highscore))

    # Funktion: Highscore laden
    def load_highscore():
        try:
            path = os.path.join(os.path.expanduser("~"), "biscuit_highscore.txt")
            with open(path, "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    # Highscore als Text darstellen 
    font_highscore = pygame.font.Font(resource_path('Pixel Game.otf'), 30)
    highscore = load_highscore()
    text_highscore = font_highscore.render(f"{highscore}",1, (255,140,0)) 
    star = pygame.image.load(resource_path("stars.png")).convert_alpha()
    star = pygame.transform.scale(star,(30,30) )
    
    # New Highscore 
    font_new_highscore = pygame.font.Font(resource_path('Pixel Game.otf'), 60)
    text_new_highscore = font_new_highscore.render("NEW HIGHSCORE!",1, (255,140,0)) 
    celebration = pygame.mixer.Sound(resource_path('celebration.mp3'))
    celebration.set_volume(0.5)
    show_new_highscore = False 
    new_highscore_time = 0 
    DISPLAY_TIME = 2500

    #Highscore nur einmal pro Runde triggern 
    highscore_triggered = False

    # Konfetti generieren 
    def create_confetti(): 
        confetti_particles = []
        for i in range(100): 
            particle = {
                "x" : randint(0,800), 
                "y" : randint (-600,0),
                "speed" : random.uniform(2,6),
                "size" : random.randint(4,8),
                "color" : random.choice([(255,140,0),
                                         (255,69,0),
                                         (220,20,60),
                                         (0,0,205),
                                         (0,153,0)
                                         ])
                
            }
            
            confetti_particles.append(particle)
        return confetti_particles 
    confetti= []
    confetti_active = False     

    # Bild von Biscuit laden 
    biscuit_image = pygame.image.load(resource_path("Biscuit.png")).convert_alpha()
    biscuit_image = pygame.transform.scale(biscuit_image,(100,150) )

    # die Position von Biscuit festlegen 
    biscuit_spalte = 8 
    biscuit_reihe = 9 

    # Bild von fressender Biscuit laden 
    bisfrisst_image = pygame.image.load(resource_path("Biscuitfrisst.png")).convert_alpha()
    bisfrisst_image = pygame.transform.scale(bisfrisst_image,(100,150) )
    
    # Bild von trauriger Biscuit laden 
    bissad_image = pygame.image.load(resource_path("Biscuittraurig.png")).convert_alpha()
    bissad_image = pygame.transform.scale(bissad_image,(100,150) )

    #Variable für Biscuit-Bild erstellen: 
    current_biscuit = biscuit_image

    # Bild von flip laden 
    flip1_image = pygame.image.load(resource_path("Flip.png")).convert_alpha()
    flip1_image = pygame.transform.scale(flip1_image,(50,50))
    flip2_image = pygame.image.load(resource_path("flip2.png")).convert_alpha()
    flip2_image = pygame.transform.scale(flip2_image,(50,50))
    flip3_image = pygame.image.load(resource_path("flip3.png")).convert_alpha()
    flip3_image = pygame.transform.scale(flip3_image,(50,50))
    flip_images = [flip1_image, flip2_image,flip3_image]
  

    
    # mehrere flips generieren 
    from random import randint 
    flips = []
    flip = {
        "spalte": 0.5 + randint(0,14), 
        "reihe":  0.0,
        "image": random.choice(flip_images),
        "speed": 0.1
        }
    flips.append(flip)
    

    #crunch sound erstellen 
    crunch = pygame.mixer.Sound(resource_path('crunch.mp3'))
    crunch.set_volume(0.5)

    
    #Game over 
    font_gameover = pygame.font.Font(resource_path('Pixel Game.otf'),100)
    game_over = font_gameover.render("GAME OVER",1, (174,32,41)) 
    red = pygame.Surface((800,600))
    red.set_alpha(70)
    red.fill((174,32,41))




    # Die Schleife, damit das Spiel läuft, solange running == TRUE 
    play = False 
    gameover = False 
    running = 1 
    while running: 
        #Framerate auf 30 Frames pro Sekunde beschränken 
        # Pygame wartet, falls das Programm schneller läuft 
        clock.tick(30) 

        #screen-Surface mit Wohnzimmer-Bild füllen 
        screen.blit(background,(0,0))
        screen.blit(dark,(0,0))


        # Biscuit Bild aussuchen 
        if gameover: 
            current_biscuit = bissad_image 
        elif any(flip["reihe"] >= biscuit_reihe -1 for flip in flips): 
            current_biscuit = bisfrisst_image
        else: 
            current_biscuit = biscuit_image 
        
        # Biscuit zeichnen 
        screen.blit(current_biscuit, (biscuit_spalte * 50, biscuit_reihe *50))

        
        #display start    
        if not play:  
            screen.blit(start,(100,250))
            screen.blit(green,(0,0))
        


        if play and not gameover: 
            #flip generieren 
            if len(flips) < 2 and any(flip["reihe"]>= 7 for flip in flips):
                new_flip = {
                    "spalte": 0.5 + randint(0,14), 
                    "reihe":  0.0,
                    "image": random.choice(flip_images),
                    "speed": 0.05 }
                flips.append(new_flip) 

            for flip in flips[:]: 
                #zeichnen 
                screen.blit(flip["image"], (flip["spalte"] * 50, flip["reihe"] *50))

                #flip nur alle paar frames fallen lassen  
                flip["reihe"] +=  flip ["speed"] + 0.015 * math.sqrt(score)

                # Der Score geht hoch, pro gefangener Flip 
                if flip["reihe"] >= biscuit_reihe and flip["spalte"] == 0.5 + biscuit_spalte: 
                    score += 1 
                    text = font.render("Score: %d" %score,1, (0,0,205)) 
                # crunch sound wird gespielt 
                    crunch.play(0)
                #flip wird aus der Liste gelöscht 
                    flips.remove(flip)
                
                
                # highscore berechnen
                if score > highscore and score > 5: 
                    highscore = score 
                    save_highscore(score) 
                    
                    if not highscore_triggered: 
                        # new highscore, timer, celebration sound 
                        if not show_new_highscore: 
                            show_new_highscore = True 
                            new_highscore_time = pygame.time.get_ticks()
                            celebration.play(0)
                       
                            #Konfetti
                            confetti = create_confetti()
                            confetti_active = True 

                if flip["reihe"] > biscuit_reihe + 1: 
                    gameover = True

            #Konfetti zeichnen und bewegen 
            if confetti_active: 
                for particle in confetti: 
                    pygame.draw.rect(screen, particle["color"], 
                                     (particle["x"], particle["y"], particle["size"], particle["size"])) 
                    particle["y"] += particle["speed"]

            
            
           
        
        # Display score 
        text_rect.center = (700,50)
        pygame.draw.rect(screen,(0,0,205),text_rect.inflate(40,20),2,10)
        screen.blit(text,text_rect)
         

        # display high score 
        text_highscore = font_highscore.render(f"{highscore}",1, (255,140,0))
        screen.blit(text_highscore, (730,80))
        screen.blit(star,(690,80))
        
        #disply new high score 
        if show_new_highscore: 
            current_time = pygame.time.get_ticks()
            highscore_triggered = True 

            if current_time - new_highscore_time < DISPLAY_TIME: 
                screen.blit(text_new_highscore,(220,250))
            else: 
                show_new_highscore = False 
                confetti_active = False 

    
        
        # display game over  
        if gameover: 
            screen.blit(game_over,(220,250))  
            screen.blit(red,(0,0))
       

        
        


        # Alle aufgelaufenen Events holen und abarbeiten. 
        for event in pygame.event.get(): 
            #Spiel beenden, wenn wir ein QUIT-Event finden 
            if event.type == pygame.QUIT: 
             running = False 

            # Wir interessieren uns auch für "Taste gedrückt"- Events     
            if event.type == pygame.KEYDOWN: 

                # ENTER drücken, um Spiel zu starten 
                if event.key == pygame.K_RETURN and not play:
                    play = True 


                # Biscuit bewegen 
                if play and not gameover: 
                    if event.key == pygame.K_LEFT and biscuit_spalte > 0:
                        biscuit_spalte -= 1 
                    if event.key == pygame.K_RIGHT and biscuit_spalte < 14: 
                        biscuit_spalte += 1 

                # ENTER drücken, um Spiel nach gameover neu zu starten 
                if event.key == pygame.K_RETURN and gameover:
                    score = 0 
                    text = font.render("Score: %d" %score,1, (0,0,205)) 
                    flips = []
                    new_flip = {
                        "spalte": 0.5 + randint(0,14), 
                        "reihe":  0.0,
                        "image": random.choice(flip_images),
                        "speed": 0.05 }
                    flips.append(new_flip) 
                    
                    biscuit_spalte = 8 
                    confetti_active = False
                    show_new_highscore = False
                    highscore_triggered = False
                    play = True 
                    gameover = False 
                
                # Wenn Escape gedrückt wird, posten wir ein QUIT-Event
                # in Pygames Event-Warteschleife 
                if event.key == pygame.K_ESCAPE: 
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        #Inhalt von screen anzeigen 
        pygame.display.flip() 

        
#Überprüfen, ob dieses Modul als Programm läuft und nicht in einem anderen Modul importiert wird 
if __name__ == '__main__':
    # Unsere Main-Funktion aufrufen.
    main()









  