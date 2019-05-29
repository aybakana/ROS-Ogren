# ROS-Ogren
ROS'ta kullanılan dosya türlerini biraraya toplayarak sizlerin bu dosya türlerini anlamanıza katkıda bulunmaya çalışacağım.

Öncelikle launch klasöründe konularına göre gruplara ayırdığım .launch uzantılı launch dosyalarını biraraya getirdim ve bunları inceleyerek launch dosya türünün nasıl kullanıldığını daha iyi anlayabilirsiniz.

Launch klasöründe bulunan klasörler:

1- /husky -> husky robotu ile ilgili launch dosyalarını içerir.

2- /jackal -> jackal robotu ile ilgili launch dosyalarını içerir.

3- /hector -> TU Darmstadt'taki hector grubunun paketlerinden topladığım launch dosyalarını içerir. (2 Boyutlu SLAM olarak size tavsiye edebileceğim hector-slam çok güzel çalışmaktadır. )

4- /robot_localization -> robot_localization paketindeki launch dosyalarını içerir.

5- /kobuki -> kobuki robotu ile ilgili launch dosyalarını içerir.

6- /move_base -> move_base paketindeki launch dosyalarını içerir.

Rosbag Filter:

#Removes all tfs except the one that has 'base_footprint' as child frame id
rosbag filter old.bag new.bag "topic != '/tf' or (len(m.transforms)>0 and m.transforms[0].child_frame_id=='base_footprint')"

#Same as above but limiting other topics to '/odom' and '/scan'
rosbag filter old.bag new.bag "topic == '/odom' or topic == '/scan' or (topic == '/tf' and len(m.transforms)>0 and m.transforms[0].child_frame_id=='imu_link')"

