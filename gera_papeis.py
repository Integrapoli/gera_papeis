from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import random
import string
import qrcode

# ------ você só precisa alterar isso
n_cols = 3
n_rows = 9
n_pags_validas = 19
n_pags_invalidas = 1
tamanho_senha = 8

# obs: imagem tem que ter fundo branco, não transparente
image = 'tras.png'
im_h = 60
im_w = 60
qr_h = 60
qr_w = 60
# ------

senhas_validas = []
senhas_invalidas = []
qtde_senhas_validas = n_cols * n_rows * n_pags_validas  # 513 papeis
qtde_senhas_invalidas = n_cols * n_rows * n_pags_invalidas  # 27 papeis
chars_permitidos = string.ascii_letters + string.digits


# gerando lista de senhas aleatórias
for _ in range(qtde_senhas_validas):
    senha = ''.join(random.SystemRandom().choice(chars_permitidos) for _ in range(tamanho_senha))
    senhas_validas.append(senha)

for _ in range(qtde_senhas_invalidas):
    senha = ''.join(random.SystemRandom().choice(chars_permitidos) for _ in range(tamanho_senha))
    senhas_invalidas.append(senha)

# guarda senhas em arquivo txt
f_validas = open('senhas_validas.txt', 'w')
for s in senhas_validas:
    f_validas.write(s + '\n')
f_validas.close()
f_invalidas = open('senhas_invalidas.txt', 'w')
for s in senhas_invalidas:
    f_invalidas.write(s + '\n')
f_invalidas.close()


def cria_pdf(senhas, n_pags, apendice):
    pdfmetrics.registerFont(TTFont('source-code-pro', 'source-code-pro.regular.ttf'))
    pdf_frente = canvas.Canvas(f'papeis_frente_{apendice}.pdf')
    pdf_tras = canvas.Canvas(f'papeis_tras_{apendice}.pdf')
    width, height = A4

    for p in range(n_pags):
        pdf_frente.grid([x * width / n_cols for x in range(n_cols + 1)],
                        [y * height / n_rows for y in range(n_rows + 1)])
        pdf_tras.grid([x * width / n_cols for x in range(n_cols + 1)],
                      [y * height / n_rows for y in range(n_rows + 1)])

        for y in range(n_rows):
            for x in range(n_cols):

                pos_x = (x + 0.5) * width / n_cols
                pos_y = (y + 0.5) * height / n_rows

                # desenhando as imagens na página de trás
                pdf_tras.drawImage(image, pos_x - im_w / 2, pos_y - im_h / 2, width=im_w, height=im_h)

                # texto na página da frente
                i = p * n_rows * n_cols + y * n_cols + x
                if i < len(senhas):
                    # gambiarra a frente
                    texto = pdf_frente.beginText(pos_x - 10, pos_y - 7)
                    texto.setFont('source-code-pro', 16)
                    texto.textLine(senhas[i])
                    pdf_frente.drawText(texto)

                    img = qrcode.make(senhas[i])
                    img.save(f'qr/qr{i}.png')
                    pdf_frente.drawImage(f'qr/qr{i}.png', pos_x - 75, pos_y - qr_h / 2, width=qr_w, height=qr_h)

        # vai para a próxima página
        pdf_frente.showPage()
        pdf_tras.showPage()

    pdf_frente.save()
    pdf_tras.save()


cria_pdf(senhas_validas, n_pags_validas, "validas")
cria_pdf(senhas_invalidas, n_pags_invalidas, "invalidas")
