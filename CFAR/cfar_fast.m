clear all;
load('data_cube.mat'); 
cube1=data_cube(:,:,1);

figure(1);
imagesc(cube1);
title("原图像");

tr=12;%训练单元距离维
td=12;%方位维
gr=10;%保卫单元距离维
gd=10;%方位维
PFA=0.01;%虚警概率

[x,y]=size(cube1);
t=zeros(td+gd+x+td+gd,tr+gr+y+tr+gr);
t(1+td+gd:td+gd+x,1+tr+gr:tr+gr+y)=cube1;
xx=2*(td+gd)+1;
yy=2*(tr+gr)+1;
xxx=2*gd+1;
yyy=2*gr+1;
n=(xx*yy-xxx*yyy);
out=zeros(td+gd+x+td+gd,tr+gr+y+tr+gr);

tic;
for i=1:x-1
    kuai=t(i:xx+i-1,1:yy);
    sum1=sum(sum(kuai));
    sum2=sum(sum(kuai(td+gd:td+xxx,tr+gr:tr+yyy)));
    for j=1:y-1
        aver_t=(sum1-sum2)/n;
        alpha=n*(PFA^(-1/n)-1);
        yu=alpha*aver_t;
        %判别
        if t(td+gd+i,tr+gr+j)>=yu
            out(td+gd+i,tr+gr+j)=1;
        else
            out(td+gd+i,tr+gr+j)=0;
        end
        sum1=sum1+sum(t(i:xx+i-1,yy+j))-sum(t(i:xx+i-1,j));
        sum2=sum2+sum(t(i+td:xxx+i+td-1,yyy+tr+j))-sum(t(i+td:xxx+i+td-1,tr+j));
    end
end
toc;

figure(2);
imagesc(out);
title("CFAR图像");

fprintf("tr=%d;td=%d;gr=%d;gd=%d;\n",tr,td,gr,gd);

