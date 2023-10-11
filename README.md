# SFC_Capillary_Setter-Python
Данный репозиторий посвещен программе настройки Сканирующего Проточного Цитометра (СПЦ), а именно контролю положения струи частиц, луча лазера в капилляре.
Скрипт позволяет:
- Работать с двумя двумя проекциями капилляра при помощи вебкамер
- Определять границы капилляра, луча или струи при помощи подгонки линейной регрессией робастными методами с возможностью настройки параметров определения
- Регулировать параметры обработки изображения с камер (обрабабываемый цветовой канал (R, G, B, GrayScale), экспозиция кадра и др.)
Программа имеет графический интерфейс на основе PyQt5 и pyqtgraph. 
