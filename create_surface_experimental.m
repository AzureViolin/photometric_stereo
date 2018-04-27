function create_surface(dataset_num)
% Usage: create_surface('2')
% Parameter can be any number in STRING from '2' to '10'

normal = load(strcat('./normal_dataset',dataset_num,'.mat'),strcat('normal_dataset',dataset_num));
normal = normal.(strcat('normal_dataset',dataset_num));

[row, column, ~] = size(normal);
slant=reshape(acos(reshape(normal(:,:,3),row*column,1)),row,column);
tn=normr(reshape(normal(:,:,1:2),row*column,2));
tilt=reshape(acos(tn(:,1)),row,column);

view_direction = [0 0 1];
for i = 1:row
    i
    for j = 1:column
        j
%         norm_at_pixel = (normal(row,column,:),1,3);
        if (normal(row,column,3) < 0)
            't'
            normal(row,column,1) = -normal(row,column,1);
            normal(row,column,2) = -normal(row,column,2);
            normal(row,column,3) = -normal(row,column,3);
%         if slant(i,j) > pi/2
%             slant(i,j) = pi - slant(i,j);
%         end
        end
    end
end

re_norm = reshape(normal(:,:,:),row*column,3);





figure(2),needleplotst(slant,tilt,5,2), axis('off')

%   opt can be the string:
%           'slanttilt' - reconstruct using both slant and tilt (default).
%           'tiltamb'   - reconstruct assuming tilt ambiguity of pi.
%           'slant'     - reconstruct with slant only.
%           'tilt'      - reconstruct with tilt only.
recsurf = shapeletsurf(slant, tilt, 6, 1, 2, 'slant');
figure(3),surf(recsurf);

% surfnorm(recsurf);

%     [dx, dy] = gradient(recsurf);
%     [s,t] = grad2slanttilt(dx,dy);


X = deal(1:column);
Y = deal(1:row);
stlwrite(strcat('dataset',dataset_num,'_surf.stl'),X,Y,recsurf,'mode','ascii')
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
% Z = zeros(row,column);
% 
% figure
% 
% quiver3(X,Y,Z,U,V,W,0.5)

% hold on
% surf(X,Y,Z)
% view(-35,45)
% axis([-2 2 -1 1 -.1 .1])
% hold off

column = 81;
row = 60;
X = deal(1:column);
Y = deal(1:row);
stlwrite('test_surf.stl',X,Y,recsurf,'mode','ascii')

U = normal(:,:,1);
V = normal(:,:,2);
W = normal(:,:,3);
X = deal(1:column);
Y = deal(1:row);
Z = zeros(row,column);

figure

quiver3(X,Y,Z,U,V,W,0.5)
 