function test_syntax_errors()
    % Тест синтаксических ошибок для проверки LSP MATLAB

    % Ошибка 1: неопределенная переменная
    x = 10;
    y = undefined_var;

    % Ошибка 2: неопределенная функция
    z = fake_function(x);

    % Ошибка 3: синтаксическая ошибка в имени функции
    result = my function with spaces();
end
