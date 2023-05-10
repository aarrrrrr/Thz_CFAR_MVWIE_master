clear;
p0=imread("SAR图像1.tif");
%imshow(p0);
%% LCM
p=double(p0);
[x,y]=size(p);
c=4;%层数
pc=zeros(x,y,c);
for k=1:c
    %每个patch大小9*L*L
    L=3*k;
    p=double(p0);
    for i=1:L:x+1-3*L
        for j=1:L:y+1-3*L
            patch=p(i:i+3*L-1,j:j+3*L-1);
            %计算中心格的最大值
            central=patch(L+1:2*L,L+1:2*L);
            Ln=max(max(central));
            %计算B1B2B3B4
            B1=patch(1:L,1:L);
            B2=patch(2*L+1:3*L,1:L);
            B3=patch(1:L,2*L+1:3*L);
            B4=patch(2*L+1:3*L,2*L+1:3*L);
            m1=(sum(B1(:))/(L*L));
            m2=(sum(B2(:))/(L*L));
            m3=(sum(B3(:))/(L*L));
            m4=(sum(B4(:))/(L*L));
            maxmi=max([m1,m2,m3,m4]);
            %更新central
            Cn=(Ln*Ln/maxmi);
            p(i+L:i+2*L-1,j+L:j+2*L-1)=Cn;
        end
    end
    pc(:,:,k)=p;
end
%% LCM阈值
% p1=pc(:,:,1);%23);
% k=2.5;%经验选取
% I=mean2(p1);
% sigma=std2(p1);
% T=I+k*sigma;
% 
% for i=1:x
%     for j=1:y
%         if (p1(i,j)<=T)
%             p1(i,j)=0;
%         else
%             p1(i,j)=70000;
%         end
%     end
% end
% 
% imshow(uint16(p1));
%% VWIE
p2=double(p0);
p2out=double(p0);
i=3*c+1;
while(i<=x-3*c)
    j=3*c+1;
    while(j<=y-3*c)
%         findc=find(max(pc(i,j,:)));
        [ma,findc]=max(pc(i,j,:));
        L=3*findc;%局部最优窗长
        uk=p2(i:i+L-1,j:j+L-1);
        %候选区域灰度平均值
        Ik=mean2(uk);
        %寻找灰度概率Pi和灰度等级Ii
        arr_grey=zeros(L,L);
        n=256;%65535/n个灰度等级
        for ii=1:L
            for jj=1:L
                Ii=floor(uk(ii,jj)/n);
                arr_grey(ii,jj)=Ii;
            end
        end
        arr=unique(arr_grey);
        m=length(arr);
        Pi=zeros(m,1);
        for ii=1:m
            Pi(ii)=length(find(arr_grey==arr(ii)))/(L*L);
        end
        %计算E值
        for ii=1:L
            for jj=1:L
                if(uk(ii,jj)<Ik)
                    uk(ii,jj)=0;
                else
                    E=0;
                    for iii=1:m
                        if (Pi(iii)~=0)
                            E=E-(arr(iii)*n-Ik)^2*Pi(iii)*log2(Pi(iii));
                        end
                    end
                    uk(ii,jj)=E;
                end
            end
        end
        p2out(i:i+L-1,j:j+L-1)=uk;
        j=j+L;
    end
    i=i+L;
end
p2outgui=65535*p2out/max(p2out(:));
%imshow(uint16(p2outgui))
%% VWIE阈值
p3=p2outgui;
k2=1.05;
meanEntropy=mean2(p3);
Eth = k2 * meanEntropy + 3000;
for i=1:x
    for j=1:y
        if(p3(i,j)<=Eth)
            p3(i,j)=0;
        else
            p3(i,j)=70000;
        end
    end
end

out=uint16(p3);
imshow(out);
         

