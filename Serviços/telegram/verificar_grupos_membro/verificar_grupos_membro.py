from telethon import TelegramClient, events

# Substitua pelas suas credenciais do Telegram
api_id = '28698037'  # Seu API ID
api_hash = 'cc1088237cdc02c6f5de83a7decef6b5'  # Seu API Hash
phone_number = '55 45 991489290'  # Seu número de telefone

# Token do seu bot
bot_token = '7934178769:AAFYTzK1E46ArXUeWGo379i2r5XBhxOTkdk'  # Substitua pelo token do seu bot

# Inicialize o cliente com o bot
client = TelegramClient('verificar_grupos_membro', api_id, api_hash).start(bot_token=bot_token)

# Lista de grupos específicos (nomes ou IDs dos grupos)
grupos_especificos = [
    -1001295637493,
    -1001737491832,
    -1001439564566,
    -1001185026220,
    -1001621172225,
    -1001863477941,
    -1001295796700,
    -1001881735344,
    -1001887418205,
    -1001848637348,
    -1001275424897,
    -1001830658148,
    -1001280097505
]

# Função para verificar a presença do usuário nos grupos
async def verificar_usuario_em_grupos(target_username):
    resultado = f"Verificando a presença de {target_username} nos grupos:\n\n"
    
    # Usando sua conta pessoal para verificar os grupos
    async with TelegramClient('verificar_conta_pessoal', api_id, api_hash) as personal_client:
        try:
            await personal_client.start(phone_number)  # Iniciar a autenticação com a conta pessoal
            grupos_com_usuario = []
            grupos_sem_usuario = []

            for grupo in grupos_especificos:
                try:
                    chat = await personal_client.get_entity(grupo)
                    participantes = await personal_client.get_participants(chat)
                    
                    if any(part.username == target_username for part in participantes):
                        grupos_com_usuario.append(chat.title)
                    else:
                        grupos_sem_usuario.append(chat.title)
                except Exception as e:
                    resultado += f"Erro ao verificar o grupo '{grupo}': {e}\n"

            if grupos_com_usuario:
                resultado += f"\n{target_username} está nos seguintes grupos:\n"
                resultado += "\n".join(grupos_com_usuario)
            else:
                resultado += f"\n{target_username} NÃO está em nenhum dos grupos especificados."
            
            if grupos_sem_usuario:
                resultado += f"\n\n{target_username} NÃO está nos seguintes grupos:\n"
                resultado += "\n".join(grupos_sem_usuario)
            else:
                resultado += f"\n\n{target_username} está em todos os grupos especificados."

        except Exception as e:
            resultado += f"Erro ao usar a conta pessoal: {e}"
    
    return resultado


# Bot do Telegram que escuta comandos
@client.on(events.NewMessage(pattern='/verificar'))
async def handler(event):
    user = event.sender_id  # Captura o ID do usuário que enviou o comando
    username = event.text.split(' ', 1)  # Divide o comando para pegar o nome do usuário
    
    if len(username) > 1:
        target_username = username[1]  # Nome de usuário a ser verificado
    else:
        await event.reply('Por favor, forneça o nome de usuário após o comando, como: /verificar username')
        return
    
    # Chama a função de verificação
    resposta = await verificar_usuario_em_grupos(target_username)
    
    # Envia a resposta para o usuário no bot
    await client.send_message(user, resposta)


# Execute o script
client.run_until_disconnected()
