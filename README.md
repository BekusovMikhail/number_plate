# Number plate
Целью данного проекта является разработка и реализация системы компьютерного зрения, способной автоматически распознавать номерные знаки на машинах. Это включает в себя детектирование и распознавание номеров, а также извлечение текстовой информации с номерных знаков для последующей обработки и анализа

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Ограничения](#Ограничения)
- [Масштабирование](#Масштабирование)

## Технологии
- [?] - Распознование номера на машине
- [Efficientnet-b3](https://pytorch.org/vision/main/models/generated/torchvision.models.efficientnet_b3) - Распознование текста номера
- [FastAPI](https://fastapi.tiangolo.com/) - Backend
- [Streamlit](https://streamlit.io/) - Frontend

## Использование
Чтобы запустить наш сервис необходимо использовать команды:
```sh
git clone https://github.com/BekusovMikhail/number_plate.git
cd number_plate
docker compose build
docker compose up
http://127.0.0.1:8501/
```

Скачать папку [triton_model_repo](https://drive.google.com/drive/folders/1etL6BM7iIQgXSx4qYWuxnKZDSDmAFVNB?usp=drive_link) и перенести ее в **.../number_plate**

## Ограничения

1. Система разработана для локального развертывания и работает с изображениями.
2. Рекомендуется наличие минимальной вычислительной мощности, необходимой для запуска докеризированной среды, а также достаточное количество оперативной памяти для эффективной обработки изображений и обучения моделей.
3. Система предполагает обработку изображений поштучно (батчом 1).
4. Сервис работает с изображениями номерных знаков, предполагая установленные параметры (номер не слишком близко, определенное разрешение и пропорции).

**Пример фотографии для модели**

![Пример фото машины](https://user-images.githubusercontent.com/78909279/279159171-2a8922e4-e513-4797-aa8d-0a3fb4f3eb73.jpg)


## Масштабирование

1. Непрерывное совершенствование моделей с целью повышения их качества и эффективности.
2. Расширение системы для поддержки разных языков и форматов номерных знаков. Это позволит использовать технологию в разных странах.
3. Связь системы с базами данных о зарегистрированных автомобилях и водителях для автоматической проверки номеров машин и выдачи соответствующей информации.
4. Доработка сервиса с целью повышения его производительности, качества и скорости обработки данных.
5. Предоставление возможности сторонним разработчикам интегрировать технологию в свои продукты с использованием API, а также продажа лицензий на использование системы.
6. Разработка системы, которая способна адаптироваться к различным условиям освещения, погодным условиям и другим переменным, которые могут повлиять на качество распознавания.
7. Исследование возможности использования технологии в смежных отраслях, таких как парковочные системы, логистика и мониторинг автопарков.
8. Разработка мобильных приложений для смартфонов, которые позволят пользователям фотографировать номерные знаки и отправлять их на обработку.
