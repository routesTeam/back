-- Пример создания строки в БД. Использовать только для теста, пока не вносим данные из результата алгоритма
INSERT INTO main_route VALUES
	(2, 'Мадрид', 'Астрахань', '{
  "time": 12,
  "coast": 20000,
  "cities": [
    {
      "name": "Мадрид",
      "time": 0,
      "type": null
    },
    {
      "name": "Москва",
      "time": 6,
      "type": "Самолет"
    },
    {
      "name": "Астрахань",
      "time": 8,
      "type": "Поезд"
    }
  ]
}')