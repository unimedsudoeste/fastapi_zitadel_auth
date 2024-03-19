# FastAPI ZITADEL Auth

Uma utilidade FastAPI para autenticação e autorização usando o recurso de introspecção de token do ZITADEL.

## Recursos

- Valida tokens de acesso com o ZITADEL.
- Verifica o token para escopos e funções necessárias.

## Instalação

Para instalar `fastapi_zitadel_auth`, execute:

```bash
pip install fastapi_zitadel_auth
```

## Uso

Aqui está um exemplo simples de como usar o fastapi_zitadel_auth:

```python
from fastapi import FastAPI, Depends
from fastapi_zitadel_auth import ZitadelAuth

app = FastAPI()

# Inicialize ZitadelAuth com suas credenciais e URL de introspecção
zitadel_auth = ZitadelAuth("cient_id:client_secret", "url_de_introspeccao")

# Use-o como uma dependência em suas rotas
@app.get("/protegido")
async def rota_protegida(user=Depends(zitadel_auth.verificar_acessos(["read:protected"]))):
    return {"message": "Esta é uma rota protegida"}
```