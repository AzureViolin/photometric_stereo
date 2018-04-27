[row, column, ~] = size(normal);
slant=reshape(acos(reshape(normal(:,:,3),row*column,1)),row,column);
tn=normr(reshape(normal(:,:,1:2),row*column,2));
tilt=reshape(acos(tn(:,1)),row,column);
recsurf = shapeletsurf(slant, tilt, 6, 1, 2, 'slanttilt');
surf(recsurf);
% surfnorm(recsurf);

%     [dx, dy] = gradient(recsurf);
%     [s,t] = grad2slanttilt(dx,dy);


X = deal(1:column);
Y = deal(1:row);
stlwrite('surf.stl',X,Y,recsurf,'mode','ascii')
% 
% figure
% surf(ones(row,column),'VertexNormals',normal,'EdgeColor','none');
% lighting gouraud
% camlight
% 
% U = normal(:,:,1);
% V = normal(:,:,2);
% W = normal(:,:,3);
% X = deal(1:column);
% Y = deal(1:row);
% Z = zeros(row,colum);
% 
% figure
% 
% quiver3(X,Y,Z,U,V,W,0.5)
% 
% hold on
% surf(X,Y,Z)
% view(-35,45)
% axis([-2 2 -1 1 -.1 .1])
% hold off