[row, column, ~] = size(normal);
slant=reshape(acos(reshape(normal(:,:,3),row*column,1)),row,column);
tn=normr(reshape(normal(:,:,1:2),row*column,2));
tilt=reshape(acos(tn(:,1)),row,column);
recsurf = shapeletsurf(slant, tilt, 6, 1, 2, 'slanttilt');
surf(recsurf);
X = deal(1:column);
Y = deal(1:row);
stlwrite('surf.stl',X,Y,recsurf,'mode','ascii')