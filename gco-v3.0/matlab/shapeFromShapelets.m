function recsurf = shapeFromShapelets(surfaceNormal)
[M, N, ~] = size(surfaceNormal);
slant = zeros(M, N);
tilt = zeros(M, N);
for i = 1:M
    for j = 1:N
        x = surfaceNormal(i, j ,1);
        y = surfaceNormal(i, j ,2);
        z = surfaceNormal(i, j ,3);
        slant(i, j) = x;%-atan(sqrt(x^2+y^2)/z);
        tilt(i, j)  = y;%acos(x/sqrt(x^2+y^2))+pi*(y<0);
    end
end
recsurf = shapeletsurf(slant, tilt, 6, 3, 2);

%[x_grid, y_grid] = meshgrid(1:N,1:M);
%display(x_grid);
%display(y_grid);
%display(recsurf);
figure(2)
surface(recsurf);
view(3)
%figure
%x_grid;
%y_grid;
%scatter3(x_grid(:), y_grid(:), recsurf(:))

%figure
%surface(X, 2*recsurf);

%figure
%x_grid;
%y_grid;


end