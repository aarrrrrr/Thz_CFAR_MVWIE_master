clear;
p0=imread("SAR图像2.tif");
p0=im2uint8(p0);
%imshow(p0);
%% LCM
p=double(p0);
[x,y]=size(p);
c=5;%层数5
n=4;%6
pc=zeros(x,y,c);
for k=1:c
    %每个patch大小9*L*L
    L=n*k+1;
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
% k1=2.5;%经验选取
% I=mean2(p1);
% sigma=std2(p1);
% T=I+k1*sigma;
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
i=n*c/2+1;
chuang=zeros(x*y,1);
cc=1;
while(i<=x-n*c/2)
    j=n*c/2+1;
    while(j<=y-n*c/2)
%         findc=find(max(pc(i,j,:)));
        [ma,findc]=max(pc(i,j,:));
        L=n*findc+1;%局部最优窗长
        chuang(cc)=L;
        cc=cc+1;
        uk=p2(i-n*findc/2:i+n*findc/2,j-n*findc/2:j+n*findc/2);
        %候选区域灰度平均值
        Ik=mean2(uk);
        %寻找灰度概率Pi
        arr=unique(uk);
        m=length(arr);
        Pi=zeros(m,1);
        for ii=1:m
            Pi(ii)=length(find(uk==arr(ii)))/(L*L);
        end
        %计算E值
        if(uk(1+n*findc/2,1+n*findc/2)<=Ik)%%%%%%%%%%%%%%%%%
            uk(1+n*findc/2,1+n*findc/2)=0;
            %p2(i,j)=0;
        else
            E=0;
            for iii=1:m
                if (Pi(iii)~=0)
                    E=E-(arr(iii)-Ik)^2*Pi(iii)*log2(Pi(iii));
                end
            end
            uk(1+n*findc/2,1+n*findc/2)=E;
        end
        p2out(i,j)=uk(1+n*findc/2,1+n*findc/2);
        j=j+1;
    end
    i=i+1;
end
p2outgui=255*p2out/max(p2out(:));
%imshow(uint8(p2outgui))
%% VWIE阈值
p3=p2out;
p3out=p3;
k2=1.05;
meanEntropy=mean2(p3);
Eth = k2 * meanEntropy + 3000;
%Eth = 25000;
for i=1:x
    for j=1:y
        if(p3(i,j)<=Eth)
            p3out(i,j)=0;
        else
            p3out(i,j)=70000;
        end
    end
end

out=uint16(p3out);
imshow(out);
         

