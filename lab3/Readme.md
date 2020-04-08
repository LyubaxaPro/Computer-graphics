ПРОГРАММНАЯ РЕАЛИЗАЦИЯ ОСНОВНЫХ АЛГОРИТМОВ ПОСТРОЕНИЯ ОТРЕЗКОВ И ИССЛЕДОВАНИЕ ИХ ВРЕМЕННЫХ И ВИЗУАЛЬНЫХ ХАРАКТЕРИСТИК


Цель работы: реализация алгоритмов построения отрезков по методу цифрового дифференциального анализатора (ЦДА) и алгоритмов
Брезенхема (действительного, целочисленного и с устранением ступенчатости) и исследование их характеристик и сравнение
полученных результатов.

В ходе выполнения практической части этой лабораторной работы необходимо выполнить следующие пункты задания:\

1.Реализовать алгоритмы ЦДА, Брезенхема (действительный, целочисленный, с устранением ступенчатости), Ву.

2.Сравнить визуально отрезки, построенные в соответствии с каждым алгоритмом, а также с отрезком,
построенным процедурой языка высокого уровня. Проверить попадание отрезка в заданную конечную точку.

3.Определить время, затрачиваемое на построение отрезка по каждому из алгоритмов.

4.Для заданного алгоритма получить зависимость длины максимальной ступеньки от угла наклона отрезка и отобразить ее в виде
графика или гистограммы.

Программы, реализующие алгоритмы, должны обеспечивать построение произвольного отрезка, то есть располагающегося в любом
из восьми октантов, включая горизонтальный и вертикальный, а также предусматривать высвечивание точки в случае вырожденного
отрезка. Визуальное сравнение отрезков, построенных по разным алгоритмам, можно осуществить либо высвечиванием близко
расположенных параллельных отрезков, либо рисованием на одном и том же месте одного отрезка разными алгоритмами. 
При этом каждый раз новый отрезок высвечивается новым цветом. В случае несовпадения результатов не все старые пиксели
высветятся новым цветом, что и будет свидетельствовать о различающихся результатах. Проверку попадания отрезка в требуемую 
конечную точку можно осуществить путем сравнения цвета конечной точки с цветом рисования отрезка.
Исследование временных характеристик построения отрезков в силу высокой скорости построения одного отрезка следует проводить
путем замера времени, затрачиваемого на высвечивание нескольких десятков отрезков (например, пятидесяти или ста отрезков).
При этом целесообразно сначала установить текущее время в ноль, а затем снять показания текущего времени. При этом достаточно
учитывать значения сотых, десятых долей и целых значений секунд, так как в силу высокого быстродействия процесс рисования не 
превысит минуты. Если же не устанавливать предварительно время в ноль, то необходимо будет учитывать возможное изменение минут 
и даже часов.
Для выполнения последнего пункта задания достаточно исследовать отрезки, расположенные в пределах одного октанта. При этом
ступеньку будут образовывать те пиксели, у которых значение одной из координат остается неизменным при изменяющейся другой 
координате. Построенный график (гистограмма) должны и­меть обозначение и оцифровку осей координат.