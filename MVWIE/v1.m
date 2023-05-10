clear;
p1=imread("SAR图像3.tif");
%imshow(p1);
p=double(p1);
[x,y]=size(p);

c=3;
pc=zeros(x,y,c);
for k=1:c
    %每个patch大小9*L*L
    L=3*k;
    p=double(p1);
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

out=zeros(x,y);
for i=1:x
    for j=1:y
        out(i,j)=max(pc(i,j,:));
    end
end

k=3;%经验选取
I=mean2(out);
sigma=std2(out);
T=I+k*sigma;

for i=1:x
    for j=1:y
        if (out(i,j)<=T)
            out(i,j)=0;
        else
            out(i,j)=70000;
        end
    end
end

out=uint16(out);
imshow(out);
         

