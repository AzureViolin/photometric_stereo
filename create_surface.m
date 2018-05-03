function create_surface(dataset_num)
% Usage: create_surface('2')
% Parameter can be any number in STRING from '2' to '10'

normal = load(strcat('./normal_dataset',dataset_num,'.mat'),strcat('normal_dataset',dataset_num));
normal = normal.(strcat('normal_dataset',dataset_num));

 [row, column, ~] = size(normal);

  slant = asin( sqrt(normal(:,:,1).^2 + normal(:,:,2).^2));
  
  tilt = acos(normal(:,:,1)./sin(slant));
  for x = 1:row
      for y = 1:column
          if (normal(x,y,2) > 0 )
              tilt(x,y) = -tilt(x,y);
          end
      end
  end

figure(11),needleplotst(slant,tilt,5,3), axis('off')

recsurf = shapeletsurf(slant, tilt, 6, 1, 2, 'slanttilt');
figure(22),surf(recsurf);


X = deal(1:column);
Y = deal(1:row);
stlwrite(strcat('dataset',dataset_num,'_surf.stl'),X,Y,recsurf,'mode','ascii')

normal = load(strcat('./refine_',dataset_num,'.mat'),strcat('refine_',dataset_num));
normal = normal.(strcat('refine_',dataset_num));

 [row, column, ~] = size(normal);

  %slant = asin( sqrt(normal(:,:,1).^2 + normal(:,:,2).^2));
  %tilt = acos(normal(:,:,1)./sin(slant));
  slant=reshape(acos(reshape(normal(:,:,3),row*column,1)),row,column);
  tn=normr(reshape(normal(:,:,1:2),row*column,2));
  tilt=reshape(acos(tn(:,1)),row,column);
  
  %if sin(slant) < 0.0000001
  %    tilt=0;
  %end
  for x = 1:row
      for y = 1:column
          if (normal(x,y,2) > 0 )
              tilt(x,y) = -tilt(x,y);
          end
      end
  end

figure(33),needleplotst(slant,tilt,5,3), axis('off')

recsurf = shapeletsurf(slant, tilt, 6, 1, 2, 'slanttilt');
figure(44),surf(recsurf);


X = deal(1:column);
Y = deal(1:row);
stlwrite(strcat('refine',dataset_num,'_surf.stl'),X,Y,recsurf,'mode','ascii')



