def menu_principal():
    while True:
        if mouse.is_button_pressed(1):
            if mouse.is_over_object(menusair):
                janela.close()
        if mouse.is_button_pressed(1):
            if mouse.is_over_object(menuiniciar):
                
                jogo()
            
        fundomenu = GameImage("fundo_menu_magnak.jpg")
        titulomenu = Sprite("titulo_magnak.png")
        menuiniciar = Sprite("menu_iniciar_magnak.png")
        menusair = Sprite("menu_sair_magnak.png")
        menuiniciar.x = janela.width - menuiniciar.width - 100 
        menuiniciar.y = janela.height/2 - menuiniciar.height/2
        menusair.x = janela.width - menusair.width - 100
        menusair.y = janela.height/2 - menusair.height/2 + menuiniciar.height
        titulomenu.x = 100
        titulomenu.y = 100
        fundomenu.draw()
        titulomenu.draw()
        menuiniciar.draw()
        menusair.draw()
        janela.update()
