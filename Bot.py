import discord
from discord.ext import commands
import random
import json
import os


intents = discord.Intents.default()
intents.messages = True  
intents.guilds = True  


bot = commands.Bot(command_prefix='!', intents=intents)

# Экономика
users_data = {}


data_file = 'D:\\Bot script\\users_data.json' 

# Загрузка данных о пользователях
def load_data():
    global users_data
    print("Проверка наличия файла...")
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as file:
                users_data = json.load(file)
                print("Данные загружены успешно:", users_data)
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
    else:
        print("Файл users_data.json не найден. Будет создан новый файл.")


def save_data():
    try:
        with open(data_file, 'w') as file:
            json.dump(users_data, file, indent=4)
            print("Данные сохранены успешно.")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")


def init_user(user_id, user_name):
    if str(user_id) not in users_data:  # Приведение к строке для соответствия JSON
        users_data[str(user_id)] = {
            "name": user_name,
            "balance": 1000  # Начальный баланс (ИЗМЕНИТЬ НА НУЖНОЕ ВАМ КОЛ-ВО)
        }
        print(f"Создан новый пользователь: {users_data[str(user_id)]}")  
        save_data()
    else:
        print(f"Пользователь найден: {users_data[str(user_id)]}")  


@bot.command(name='баланс', case_insensitive=True)
async def баланс(ctx):
    user_id = ctx.author.id
    user = users_data.get(str(user_id))  # Приведение к строке для соответствия JSON
    if user:
        await ctx.send(f'{ctx.author.name}, ваш баланс: {user["balance"]} монет.')
    else:
        await ctx.send('Пользователь не найден.')

# !РАБОТА
@bot.command(name='работа', case_insensitive=True)
async def работа(ctx):
    await ctx.send('Доступные Вам работы:\n1. Слесарь\n2. Грузчик\n3. Дворник')

# !РАБОТАТЬ
@bot.command(name='работать', case_insensitive=True)
async def работать(ctx, работа_id: int):
    user_id = ctx.author.id
    user_name = ctx.author.name


    init_user(user_id, user_name)

    user = users_data.get(str(user_id))

    # Проверка на валидность номера работы
    if работа_id < 1 or работа_id > 3:
        await ctx.send('Неправильный номер работы. Пожалуйста, выберите номер от 1 до 3.')
        return

    # Определение коэффициентов для каждой работы
    коэффициенты = {
        1: (2000, 5000),  # Слесарь
        2: (1000, 4000),  # Грузчик
        3: (1500, 3500),  # Дворник
    }

    # Получение диапазона заработка для выбранной работы
    мин_заработок, макс_заработок = коэффициенты[работа_id]
    заработок = random.randint(мин_заработок, макс_заработок)

    # Обновление баланса пользователя
    user["balance"] += заработок
    await ctx.send(f'{ctx.author.name}, вы подмели двор, заработали {заработок} монет.')
    await ctx.send(f'Ваш баланс: {user["balance"]} монет.')

    save_data()  # Сохраняем обновленные данные пользователя
    
# !Казино
@bot.command(name='казино', case_insensitive=True)
async def казино(ctx, ставка: int):
    user_id = ctx.author.id
    user_name = ctx.author.name
    

    init_user(user_id, user_name)

    user = users_data.get(str(user_id))

    # Проверка ставки
    if ставка <= 0:
        await ctx.send('Ставка должна быть больше 0.')
        return
    
    if ставка > user["balance"]:
        await ctx.send(f'У вас недостаточно средств для ставки. Ваш баланс: {user["balance"]} монет.')
        return

    # Списки коэффициентов для выигрыша и проигрыша
    коэффициенты_выигрыш = [2, 10, 50, 100]
    коэффициенты_проигрыш = [0.25, 0.5, 0.75, 1]

    # Рандомное определение: игрок выиграл или проиграл
    результат = random.choice(["выигрыш", "проигрыш"])

    if результат == "выигрыш":
        коэффициент = random.choice(коэффициенты_выигрыш)
        выигрыш = ставка * коэффициент
        выигрыш = round(выигрыш, 2)  
        user["balance"] += выигрыш
        await ctx.send(f'{ctx.author.name}, поздравляю! Вы выиграли {выигрыш:.2f} ({коэффициент}x)')
        await ctx.send(f'Баланс: {user["balance"]:.2f}')
    else:
        коэффициент = random.choice(коэффициенты_проигрыш)
        проигрыш = ставка * коэффициент
        проигрыш = round(проигрыш, 2)
        user["balance"] -= проигрыш
        await ctx.send(f'{ctx.author.name}, вы проиграли {проигрыш:.2f} ({коэффициент}x)')
        await ctx.send(f'Баланс: {user["balance"]:.2f}')

    save_data()  


load_data()

bot.run('TOKEN')
