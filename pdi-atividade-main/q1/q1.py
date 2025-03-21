import cv2
import numpy as np

def verifica_colisao(video_path):
    cap = cv2.VideoCapture(video_path)
    colisao_ocorreu = False  # Variável para controlar se houve colisão
    ultrapassagem_ocorreu = False  # Variável para controlar ultrapassagem
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detecta a cor vermelha
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        
        # Detecta a cor azul
        lower_blue = np.array([100, 150, 50])
        upper_blue = np.array([140, 255, 255])
        
        # Cria a máscara
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Encontra os contornos das formas
        contorno_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contorno_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        formas_encontradas = []

        # Processa os contornos das formas detectadas
        for contorno in contorno_red + contorno_blue:
            if cv2.contourArea(contorno) > 500:
                pos_x, pos_y, largura, altura = cv2.boundingRect(contorno)
                formas_encontradas.append((pos_x, pos_y, largura, altura, cv2.contourArea(contorno)))

        # Ordena as formas encontradas pela área, da maior para a menor
        formas_encontradas.sort(key=lambda forma: forma[4], reverse=True)

        if len(formas_encontradas) >= 2:
            # Maior forma detectada
            pos_x1, pos_y1, largura1, altura1, _ = formas_encontradas[0]
            # Segunda maior forma detectada
            pos_x2, pos_y2, largura2, altura2, _ = formas_encontradas[1]

            # Desenha um retângulo verde na maior forma
            cv2.rectangle(frame, (pos_x1, pos_y1), (pos_x1 + largura1, pos_y1 + altura1), (0, 255, 0), 2)

            # Verifica colisao entre as formas
            if not colisao_ocorreu and (pos_x1 < pos_x2 + largura2 and pos_x1 + largura1 > pos_x2 and pos_y1 < pos_y2 + altura2 and pos_y1 + altura1 > pos_y2):
                colisao_ocorreu = True  

            # Se houve colisao
            if colisao_ocorreu:
                cv2.putText(frame, "COLISAO DETECTADA", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Verifica ultrapassagem apos a colisão
            if colisao_ocorreu and (pos_x1 > pos_x2 + largura2 or pos_x1 + largura1 < pos_x2 or pos_y1 > pos_y2 + altura2 or pos_y1 + altura1 < pos_y2):
                ultrapassagem_ocorreu = True  

        
            if ultrapassagem_ocorreu:
                cv2.putText(frame, "ULTRAPASSAGEM DETECTADA", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        

        cv2.imshow('Detecção', frame)
        
        # Aguarda tecla 'ESC' para sair
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

video_file = "q1/q1A.mp4"
verifica_colisao(video_file)