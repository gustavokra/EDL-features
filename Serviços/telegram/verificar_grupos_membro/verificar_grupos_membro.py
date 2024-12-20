import asyncio
from telethon import TelegramClient, events

# Substitua pelas suas credenciais do Telegram
api_id = '28698037'  # Seu API ID
api_hash = 'cc1088237cdc02c6f5de83a7decef6b5'  # Seu API Hash
phone_number = '55 45 991489290'  # Seu número de telefone
bot_token = '7934178769:AAFYTzK1E46ArXUeWGo379i2r5XBhxOTkdk'  # Token do seu bot

# Inicialize o cliente com o bot
client = TelegramClient('verificar_grupos_membro', api_id, api_hash).start(bot_token=bot_token)

# Listas de grupos e canais na ordem especificada
grupos_especificos = [
    {"id": -1001295637493, "nome": "PORTARIA"},
    {"id": -1001436112187, "nome": "CONGRESSO"},
    {"id": -1001737491832, "nome": "ALUNOS"},
    {"id": -1001439564566, "nome": "MEMBROS"},
    {"id": -1001185026220, "nome": "AMOR E HONRA - MEMBROS MENSALISTAS"},
    {"id": -1001621172225, "nome": "FILOSOFIA"},
    {"id": -1001863477941, "nome": "CONSCIENCIOLOGIA"},
    {"id": -1001295796700, "nome": "TEOLOGIA"},
    {"id": -1001881735344, "nome": "POLÍTICA"},
    {"id": -1001887418205, "nome": "MAGIA E ALQUIMIA"},
    {"id": -1001848637348, "nome": "TERITOCRACIA"},
    {"id": -1001275424897, "nome": "HISTORIA"},
    {"id": -1001830658148, "nome": "REINO"},
    {"id": -1001280097505, "nome": "SATANÁS ZOEIRO"}
]

canais_especificos = [
    {"id": -1002068473331, "nome": "TV GRATIDÃO"},
    {"id": -1001203749156, "nome": "TV EDL"},
    {"id": -1001230858033, "nome": "TV MEMBROS"},
    {"id": -1001161981334, "nome": "TV MEMBROS - AMOR"},
    {"id": -1002031044448, "nome": "CINEMA EDL"},
    {"id": -1002229549472, "nome": "BÁSICO 1"},
    {"id": -1001227353680, "nome": "MOVIMENTO NAS REDES"}
]

# Função para verificar presença em grupos/canais
async def verificar_presenca(target_username):
    resultado = f"\ud83d\udc64 [{target_username}](http://t.me/{target_username})\n\n"
    grupos_com_usuario = []
    grupos_sem_usuario = []
    canais_com_usuario = []
    canais_sem_usuario = []

    async with TelegramClient('verificar_conta_pessoal', api_id, api_hash) as personal_client:
        await personal_client.start(phone_number)

        # Verifica grupos
        for grupo in grupos_especificos:
            try:
                chat = await personal_client.get_entity(grupo["id"])
                participantes = await personal_client.get_participants(chat)

                if any(part.username == target_username for part in participantes):
                    grupos_com_usuario.append(grupo["nome"])
                else:
                    grupos_sem_usuario.append(grupo["nome"])
            except Exception as e:
                print(f"Erro ao verificar o grupo {grupo['nome']}: {e}")
                await asyncio.sleep(0.1)  # Adiciona um pequeno delay para evitar bloqueio

        # Verifica canais
        for canal in canais_especificos:
            try:
                chat = await personal_client.get_entity(canal["id"])
                participantes = await personal_client.get_participants(chat)

                if any(part.username == target_username for part in participantes):
                    canais_com_usuario.append(canal["nome"])
                else:
                    canais_sem_usuario.append(canal["nome"])
            except Exception as e:
                print(f"Erro ao verificar o canal {canal['nome']}: {e}")
                await asyncio.sleep(0.1)  # Adiciona um pequeno delay para evitar bloqueio

    # Monta a resposta
    resultado += f"\u2705 {' / '.join(grupos_com_usuario)}\n\n"
    resultado += f"\u274c {' / '.join(grupos_sem_usuario)}\n\n"
    resultado += f"\u2734\ufe0f {' / '.join(canais_com_usuario)}\n\n"
    resultado += f"\u274c {' / '.join(canais_sem_usuario)}\n"

    return resultado

# Bot que escuta comandos
@client.on(events.NewMessage(pattern='/verificar'))
async def handler(event):
    user = event.sender_id
    message_parts = event.text.split(' ', 1)

    await event.reply("Verificando, aguarde a resposta...")

    if len(message_parts) > 1:
        target_username = message_parts[1].strip()
        resposta = await verificar_presenca(target_username)
        await event.reply(resposta, parse_mode='md')
    else:
        await event.reply("Por favor, forneça o nome de usuário após o comando, como: /verificar username")

@client.on(events.NewMessage(pattern='/membros'))
async def verificar_membros(event):
    try:
        await event.reply("Obtendo os membros do grupo 'MEMBROS' e verificando presença...")

        # Obter o ID do grupo "MEMBROS"
        grupo_membros_id = next(grupo["id"] for grupo in grupos_especificos if grupo["nome"] == "MEMBROS")
        
        async with TelegramClient('verificar_conta_pessoal', api_id, api_hash) as personal_client:
            await personal_client.start(phone_number)
            
            # Obter os membros do grupo "MEMBROS"
            grupo_membros = await personal_client.get_entity(grupo_membros_id)
            participantes = await personal_client.get_participants(grupo_membros)

        # Iterar sobre cada membro e verificar presença
        respostas = []
        for participante in participantes:
            print(f"{participante.username}")
            username = f"{participante.first_name or ''} {participante.last_name or ''}".strip()
            if not username:
                continue  # Ignorar participantes sem nome de usuário ou nome visível
            
            resposta = await verificar_presenca(username)
            await asyncio.sleep(0.1)
            # Enviar as respostas em mensagens separadas (Telegram tem limites de caracteres)
            await event.reply(resposta, parse_mode='md')

    except Exception as e:
        await event.reply(f"Erro ao processar: {str(e)}")

# Comando /listar
@client.on(events.NewMessage(pattern='/listar'))
async def listar_usuarios(event):
    try:
        await event.reply("Listando membros de todos os grupos, aguarde...")

        personal_client = TelegramClient('verificar_conta_pessoal', api_id, api_hash)
        await personal_client.start(phone_number)

        # Iterar sobre todos os grupos
        for grupo in grupos_especificos:
            grupo_nome = grupo["nome"]
            grupo_id = grupo["id"]
            chat = await personal_client.get_entity(grupo_id)
            participantes = await personal_client.get_participants(chat)

            membros = []
            for participante in participantes:
                username = participante.username or ""
                nome = f"{participante.first_name or ''} {participante.last_name or ''}".strip()
                if username:
                    membros.append(f"{nome} (@{username})")
                elif nome:
                    membros.append(f"{nome} (sem username)")

            if membros:
                # Montar a resposta no formato desejado
                resposta = f"**{grupo_nome}**\n\n" + "\n".join(membros)
                
                # Dividir mensagens muito longas
                while len(resposta) > 4000:
                    corte = resposta[:4000].rfind("\n")
                    await event.reply(resposta[:corte], parse_mode='md')
                    resposta = resposta[corte:].strip()
                
                # Enviar o restante
                await event.reply(resposta, parse_mode='md')
            else:
                await event.reply(f"**{grupo_nome}**\n\nNenhum membro encontrado.", parse_mode='md')

        await personal_client.disconnect()

    except Exception as e:
        await event.reply(f"Erro ao listar membros: {str(e)}")

# Execute o bot
client.run_until_disconnected()
