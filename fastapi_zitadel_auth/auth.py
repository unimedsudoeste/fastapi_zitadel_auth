from fastapi import HTTPException, Request
from httpx import AsyncClient
from base64 import b64encode


class ZitadelAuth:
    """
    Uma classe para lidar com autenticação e verificação de escopos com o ZITADEL.

    Esta classe fornece funcionalidade para verificar tokens JWT usando o endpoint de introspecção de token do ZITADEL.
    Ele suporta a verificação de validade do token, status de atividade e escopos requeridos.

    Atributos:
        credentials (str): Credenciais do cliente codificadas em Base64 para autenticação do ZITADEL.
        introspection_url (str): URL do endpoint de introspecção do ZITADEL.

    Métodos:
        verificar_acessos(scopes_requeridos): Verifica o token para os escopos requeridos.
    """

    def __init__(self, credentials: str, introspection_url: str):
        """
        Constructs all the necessary attributes for the ZitadelAuth object.

        Parameters:
            credentials (str): Client credentials (client_id:client_secret) for ZITADEL authentication.
            introspection_url (str): URL of the ZITADEL introspection endpoint.
        """
        self.credentials = credentials
        self.introspection_url = introspection_url

    def verificar_acessos(self, roles: list = []):
        """
        Método assíncrono para verificar tokens de acesso em relação aos escopos requeridos usando o endpoint de introspecção do ZITADEL.

        Este método verifica se o token de acesso fornecido é válido, ativo e contém todos os escopos requeridos.
        Ele gera uma exceção HTTPException com os códigos de status apropriados para tokens inválidos ou com escopos insuficientes.

        Parâmetros:
            roles (list): Uma lista de strings representando as roles para acessar um recurso.

        Retorna:
            dict: Um dicionário contendo os dados de introspecção do token se a verificação for bem-sucedida.

        Gera:
            HTTPException: 401 se o token estiver ausente, inválido ou inativo.
            HTTPException: 403 se o token não tiver os escopos requeridos.
        """
        async def _verificar_acessos(request: Request):
            authorization = request.headers.get("Authorization")
            if not authorization:
                raise HTTPException(status_code=401, detail="Token ausente")

            token = authorization.split("Bearer ")[1]

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {b64encode(self.credentials.encode()).decode()}"
            }

            data = {"token": token}

            async with AsyncClient() as client:
                response = await client.post(self.introspection_url, data=data, headers=headers)

            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Token inválido")

            token_data = response.json()
            if not token_data.get("active", False):
                raise HTTPException(status_code=401, detail="Token inativo")

            token_roles = token_data.get("urn:zitadel:iam:org:project:roles", {}).keys()

            if not all(roles in token_roles for roles in roles):
                raise HTTPException(status_code=403, detail="Escopos insuficientes")

            return token_data
        return _verificar_acessos
