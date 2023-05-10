clear all;
load('data_cube.mat'); 
cube1=data_cube(:,:,10);

figure(1);
imagesc(cube1);
title("原图像");

tr=8;%训练单元距离维
td=8;%方位维
gr=5;%保卫单元距离维
gd=5;%方位维
PFA=0.002;%虚警概率

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
for i=td+gd+1:x
    for j=tr+gr+1:y
        %总块数和
        sum1=0;
        for ii=i-td-gd:i-td-gd+xx-1
            for jj=j-tr-gr:j-tr-gr+yy-1
                sum1=sum1+t(ii,jj);
            end
        end
        %保护区和CUT之和
        sum2=0;
        for iii=i-gd:i-gd+xxx-1
            for jjj=j-gr:j-gr+yyy-1
                sum2=sum2+t(iii,jjj);
            end
        end
        %T区均值
        aver_t=(sum1-sum2)/n;
        alpha=n*(PFA^(-1/n)-1);
        yu=alpha*aver_t;
        %判别
        if t(i,j)>=yu
            out(i,j)=1;
        else
            out(i,j)=0;
        end
    end
end
toc;

figure(2);
imagesc(out);
title("CFAR图像");

fprintf("tr=%d;td=%d;gr=%d;gd=%d;\n",tr,td,gr,gd);


