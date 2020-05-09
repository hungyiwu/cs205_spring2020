ncores = [1:1:8];
t=[0.931347,0.77330,0.7172522,0.675983,0.799086,0.820735,0.763917,0.724940];
su = t(1)./t;

figure;
box on
subplot(1,2,1)
plot(ncores,t,'-s','LineWidth',2,'MarkerSize',10)
xlabel('N cores')
ylabel('Spark execution time (s)')
ylim([0.1 1])

subplot(1,2,2)
plot(ncores,su,'-s','LineWidth',2,'MarkerSize',10)
xlabel('N cores')
ylabel('Speedup')
box on