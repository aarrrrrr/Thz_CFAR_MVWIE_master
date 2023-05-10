p=imread('thz1.bmp');
p=rgb2gray(p);
realp=imread('thz3_real.bmp');
realp=rgb2gray(realp);
p=imresize(p,[500,200]);
realp=imresize(realp,[500,200]);
level=graythresh(p);
p=im2bw(p,level);
realp=imresize(realp,[500,170]);
%%
out=zeros(size(p));
for i=1:500
    for j=1:170
        out(i,j)=~xor(p(i,j),realp(i,j));
    end
end
imshow(p);   










