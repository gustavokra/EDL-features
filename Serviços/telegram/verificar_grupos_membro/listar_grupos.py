from telethon import TelegramClient

# Substitua pelas suas credenciais do Telegram
api_id = '28698037'
api_hash = 'cc1088237cdc02c6f5de83a7decef6b5'
phone_number = '+55 45 991489290'

# Inicialize o cliente
client = TelegramClient('session_name', api_id, api_hash)

async def listar_grupos():
    await client.start(phone=phone_number)
    
    print("Listando todos os grupos:")
    
    # Itera sobre todos os diálogos (conversas)
    async for dialog in client.iter_dialogs():
        # Verifica se o diálogo é um grupo
        if dialog.is_group:
            print(f"Grupo: {dialog.title} (ID: {dialog.id})")

# Execute o script
with client:
    client.loop.run_until_complete(listar_grupos())