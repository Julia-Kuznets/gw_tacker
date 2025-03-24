import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных из CSV-файла
npcs_df = pd.read_csv('npcs.csv')

# Уникальные локации для выпадающего списка
locations = npcs_df['location'].tolist()


def home_page():
    # Пример изменения стиля текста с помощью HTML и CSS
    st.markdown("""
        <style>
            .big-font {
                font-size: 64px !important;
                font-style: Inter;
                font-weight: bold;
                color: #000000;
            }
            .medium-font {
                font-size: 24px !important;
                font-style: Inter;
                color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)



    # Использование кастомных стилей
    st.title('Данные об играх в Гвинт')
    st.write('Здесь можно вносить результаты своих похождений')
#    st.markdown('<p class="big-font">Это статистика из Ведьмака 3!</p>', unsafe_allow_html=True)
#    st.markdown('<p class="medium-font">Вноси здесь свои результаты, гэмблер.</p>', unsafe_allow_html=True)
    st.image("https://playmarketgames.ru/upload/iblock/6ac/ptn20nokys4evs0w0urrotyr3ddwaz4w.jpg",
             caption="Изображение из интернета", use_container_width =True)
    st.title('Гвинт')
    st.write('В этом разделе можно записать данные о сыгранных партиях и посмотреть свою статистику')
    st.image("https://www.playgwent.com/build/img/wallpapers/thumbs/Ciri_CGI_RU-65707a94.jpg",
             caption="Изображение из интернета", use_container_width=True)
    st.title('Кулачные бои')
    st.write('В этом разделе можно записать данные о пройденных боях и посмотреть свою статистику')
    st.image("https://www.playgwent.com/build/img/wallpapers/thumbs/Geralt_CGI_RU-241dba2d.jpg",
             caption="Изображение из интернета", use_container_width=True)


def gw_stat():
    # Заголовок приложения
    st.title('Данные об играх в Гвинт')

    # Форма для ввода данных
    with st.form("gw_form"):
        game_result = st.selectbox('Результат игры', ['Выигрыш', 'Проигрыш'])
        # Выбор локации с использованием on_change
        selected_location = st.selectbox('Выберите локацию', locations)

        # Выбор NPC
        enemy = st.text_input('Введите имя NPC')

        # Другие поля формы
        date = st.date_input('Выберите дату')
        bet_amount = st.number_input('Введите сумму', min_value=0)


        # Кнопка отправки
        submitted = st.form_submit_button('Отправить')

    # Обработка отправки формы
    if submitted:
        new_entry = pd.DataFrame({
            'result':[game_result],
            'date': [date],
            'bet_amount': [bet_amount],
            'location': [selected_location],
            'enemy': [enemy],
            'total':[bet_amount * 2],
        })

        # Сохранение в CSV-файл
        new_entry.to_csv('gwent_games.csv', mode='a', header=False, index=False)
        st.write("Запись сохранена")

    @st.cache_data
    def load_data():
        return pd.read_csv('gwent_games.csv', header=None, names=['Результат', 'Дата', 'Ставка', 'Локация', 'Противник', 'Сумма'])

    data = load_data()

    #Преобразовываю данные
    data['Дата'] = pd.to_datetime(data['Дата'])
    data["Сумма"] = data.apply(lambda x: x["Ставка"] if x["Результат"] == "Выигрыш" else -x["Ставка"], axis=1)
    data["Баланс"] = data["Ставка"].cumsum()  # Кумулятивная сумма


    # Группируем по дате и считаем кумулятивный баланс
    daily_balance = data.groupby("Дата")["Ставка"].sum().cumsum().reset_index()
    daily_balance.columns = ["Дата", "Баланс"]

    wins = len(data[data['Результат'] == 'Выигрыш'])
    losses = len(data[data['Результат'] == 'Проигрыш'])
    data = data.sort_values("Дата")

    #Настройка данных для пирога
    labels = ['Выигрыши', 'Проигрыши']
    sizes = [wins, losses]
    colors = ['#156A5F', '#9E331C']
    explode = (0.1, 0)

    #Создание диаграммы
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Чтобы диаграмма была круглой
    st.title('Соотношение выигрышей и проигрышей')

    st.pyplot(fig)

    #Кривая по ставкам
    st.title("Кривая по ставкам - Динамика баланса")
    st.subheader("Линейный график")
    st.line_chart(daily_balance.set_index("Дата")["Баланс"])

    st.write("Данные по дням:", daily_balance)

def fight_stat():

    st.title('Данные о кулачных боях')

    with st.form('ft_form'):
        game_result = st.selectbox('Результат игры', ['Выигрыш', 'Проигрыш'])
        selected_location = st.selectbox('Выберите локацию', locations)
        enemy = st.text_input('Введите имя NPC')

        date = st.date_input('Выберите дату')
        bet_amount = st.number_input('Введите сумму', min_value=0)

        submitted = st.form_submit_button('Отправить')

        if submitted:
            new_entry = pd.DataFrame({
                'result': [game_result],
                'date': [date],
                'bet_amount': [bet_amount],
                'location': [selected_location],
                'enemy': [enemy],
                'total': [bet_amount * 2],
            })

            new_entry.to_csv('fights.csv', mode='a', header=False, index=False)
            st.write("Запись сохранена")
    @st.cache_data
    def load_data():
        return pd.read_csv('fights.csv', header=None, names=['Результат', 'Дата', 'Ставка', 'Локация', 'Противник', 'Сумма'])

    data = load_data()

    #Преобразовываю данные
    data['Дата'] = pd.to_datetime(data['Дата'])
    data["Сумма"] = data.apply(lambda x: x["Ставка"] if x["Результат"] == "Выигрыш" else -x["Ставка"], axis=1)
    data["Баланс"] = data["Ставка"].cumsum()  # Кумулятивная сумма

    # Группируем по дате и считаем кумулятивный баланс
    daily_balance = data.groupby("Дата")["Ставка"].sum().cumsum().reset_index()
    daily_balance.columns = ["Дата", "Баланс"]

    wins = len(data[data['Результат'] == 'Выигрыш'])
    losses = len(data[data['Результат'] == 'Проигрыш'])
    data = data.sort_values("Дата")

    #Настройка данных для пирога
    labels = ['Выигрыши', 'Проигрыши']
    sizes = [wins, losses]
    colors = ['#156A5F', '#9E331C']
    explode = (0.1, 0)

    #Создание диаграммы
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Чтобы диаграмма была круглой
    st.title('Соотношение выигрышей и проигрышей')

    st.pyplot(fig)

    #Кривая по ставкам
    st.title("Кривая по ставкам - Динамика баланса")
    st.subheader("Линейный график")
    st.line_chart(daily_balance.set_index("Дата")["Баланс"])

    st.write("Данные по дням:", daily_balance)


if 'page' not in st.session_state:
    st.session_state.page = 'home'

with st.sidebar:
    st.title('меню')
    if st.button('Домашняя страница'):
        st.session_state.page = 'home'
    if st.button("Гвинт"):
        st.session_state.page = 'gwent'
    if st.button("Кулачный бой"):
        st.session_state.page = 'fight'

if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'gwent':
    gw_stat()
elif st.session_state.page == 'fight':
    fight_stat()