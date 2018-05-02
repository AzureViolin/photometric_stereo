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
surface(2*recsurf);
[x_grid, y_grid] = meshgrid(1:M,1:N);
figure
scatter3(x_grid(:), y_grid(:), recsurf(:))


end