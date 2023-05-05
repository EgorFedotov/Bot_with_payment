
# Теоеграм Бот
Бот принимает принимает оплату через QIWI, создает счет оплаты, после проведения операции пополняет баланс пользователя,
***

## Стек
Python3, aiogram, pyQiwiP2P
***

## Инструкция по запуску
* Клонируем репозиторий

	`
	git clone git@github.com:EgorFedotov/Bot_with_payment.git
	`


* Устанавливаем и активируем виртуальное окружение  

	`
    py -3.7 -m venv venv
    `
    `
    source venv/Scripts/activate
    `
   
   
* Устанавливаем зависимости из файла requirements.txt
 
	`
    pip install -r requirements.txt
    `
 

* В корне проекта создать файл .env и в него записать:

    - токен телеграм-бота

    - токен qiwi 


* запускаем сервер 

    `
	python main.py
    `
***