function create_surface(dataset_num)
% Usage: create_surface('2')
% Parameter can be any number in STRING from '2' to '10'

normal = load(strcat('./normal_dataset',dataset_num,'.mat'),strcat('normal_dataset',dataset_num));
normal = normal.(strcat('normal_dataset',dataset_num));

% slant=reshape(acos(reshape(normal(:,:,3),row*column,1)),row,column);
% tn=normr(reshape(normal(:,:,1:2),row*column,2));
% tilt=reshape(acos(tn(:,1)),row,column);
% 
 [row, column, ~] = size(normal);
% renorm = reshape(normal(:,:,3),row*column,1);
% acos_renorm = acos(renorm);
% slant = reshape(acos_renorm, row, column);
% 
% t = reshape(normal(:,:,1:2),row*column,2);
% tangent = t(:,1)./t(:,2);
% tilt=reshape(atan(tangent(:,1)),row,column);

  slant = asin( sqrt(normal(:,:,1).^2 + normal(:,:,2).^2));
  
  tilt = acos(normal(:,:,1)./sin(slant));
  for x = 1:row
      for y = 1:column
          if (normal(x,y,2) > 0 )
              tilt(x,y) = -tilt(x,y);
          end
      end
  end

figure(22),needleplotst(slant,tilt,5,3), axis('off')

%   opt can be the string:
%           'slanttilt' - reconstruct using both slant and tilt (default).
%           'tiltamb'   - reconstruct assuming tilt ambiguity of pi.
%           'slant'     - reconstruct with slant only.
%           'tilt'      - reconstruct with tilt only.
recsurf = shapeletsurf(slant, tilt, 6, 1, 2, 'slanttilt');
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
% 
% column = 81;
% row = 60;
% X = deal(1:column);
% Y = deal(1:row);
% stlwrite('test_surf.stl',X,Y,recsurf,'mode','ascii')
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
%  