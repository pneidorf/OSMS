% Определение длины последовательности
SIZE = 5;
length_seq = 2^SIZE - 1;

% Инициализация регистров Голда
register_x = [0, 1, 1, 0, 0];
register_y = [1, 0, 0, 1, 1];
register_x1 = [0, 1, 1, 0, 1];
register_y1 = [0, 1, 1, 1, 0];

% Генерация последовательности Голда и измененной последовательности
fprintf('\nFirst Gold''s sequence (x = 12, y = 12+7=19):\n');
random_sequence = Gold_sequence(register_x, register_y, length_seq);

fprintf('Second Gold''s sequence (x = 12+1, y = 19 - 5 = 14):\n');
modified_sequence = Gold_sequence(register_x1, register_y1, length_seq);

fprintf('\n');

% Генерация сдвинутых последовательностей для вычисления автокорреляции

%shifted_sequence = zeros(length_seq, length_seq);
shifted_sequence = random_sequence;
fprintf('Shift |');
for shift_idx = 1:length_seq
    fprintf('%2d|', shift_idx);
    %shifted_sequence(shift_idx, :) = circshift(random_sequence, [0, shift_idx-1]);
end
fprintf('\n');

% Вычисление автокорреляции

fprintf('Autocorrelation:\n');
[cor, lag]=xcorr(random_sequence,random_sequence);
for i = 0:length_seq
    fprintf(' %5d|', i);
    for j = 1:length_seq
        fprintf('%2d|', shifted_sequence(j));
    end
    if i == length_seq
        fprintf('%.3f\n', cor(length_seq));
    else
        fprintf('%.3f\n', cor(i+31));

    end

    shifted_sequence = circshift(random_sequence, [0, i+1]);
end

fprintf('\n');

% Вычисление взаимной корреляции

[cor1, lag1]=xcorr(random_sequence,modified_sequence);
fprintf("\nThe cross-correlation of two gold sequences is equal to >> %.3f\n", cor1(length_seq));

subplot(1, 1, 1);
plot(lag,cor);
xlabel("lag");
ylabel("Amplitude");
title("Замена автокорреляции xcorr(x,x)");


% Функция для генерации последовательности Голда
function sequence = Gold_sequence(register_x, register_y, length)
    sequence = zeros(1, length);
    fprintf('Gold''s sequence equals: ');
    for i = 1:length
        sequence(i) = mod(register_x(5) + register_y(5), 2);
        fprintf('%d', sequence(i));
        [register_x, register_y] = custom_shift(register_x, register_y);
    end
    fprintf('\n\n');
end


% Функция для сдвига регистра
function [register_x, register_y] = custom_shift(register_x, register_y)
    res_x = mod(register_x(3) + register_x(4), 2);
    res_y = mod(register_y(2) + register_y(3), 2);
    register_x(2:end) = register_x(1:end-1);
    register_x(1) = res_x;
    register_y(2:end) = register_y(1:end-1);
    register_y(1) = res_y;
end
