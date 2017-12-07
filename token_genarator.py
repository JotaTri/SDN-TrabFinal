import jose.jwt as jwt
import datetime

usuario = 'Guestavo Henrique'
nivel_acesso = 1 #2
senha = 'SenhaSuperMegaDificil'

token_acesso = jwt.encode({
    'user': {'usuario': usuario, 'nivel_de_acesso': nivel_acesso},
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
    senha,
    algorithm='HS256'
)

print('Seu Token e: ' + token_acesso)
