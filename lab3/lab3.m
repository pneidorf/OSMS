pi = 3.14;
t = [0:100-1]/100;
s1 = cos(2 * pi * 12 * t);
s2 = cos(2 * pi * 16 * t);
s3 = cos(2 * pi * 25 * t);

a = 4 * s1 + 4 * s2 + s3;
b = 2 * s1 + s2 + 2*s3;

corsa = 0;
for n = 1:100
    corsa = corsa + s1(n) * a(n);
end
disp(corsa);

corsb = 0;
for n = 1:100
    corsb = corsb + s1(n) * b(n);
end
disp(corsb);

normcorskef = 0;
for n = 1:100
    %normcorskef = normcorskef + (s1(n) * s1(n));
    normcorskef = normcorskef + pow(s1(n),2);
end

normcora = 0;
for n = 1:100
    normcora = normcora + pow(a(n),2)
end

normcorb = 0;
for n = 1:100
    normcorb = normcorb + pow(b(n),2)
end

final_normcor_a = (corsa/sqrt(normcorskef*normcora));
final_normcor_b = (corsb/sqrt(normcorskef*normcorb));

dis = sprintf("\n---\nОбычная корреляция\n---\n\\ |   A    |    B   |\ns1|%.4f|%.4f|\n",cors1a, cors1b);
disp(dis);
dis = sprintf("\n---\nНормализованная корреляция\n---\n\\ |   A    |    B   |\ns1|%.4f|%.4f|\n",normcors1a, normcors1b);
disp(dis);

