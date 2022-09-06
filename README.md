实现功能：
1. 不改变代码情况下，通过配置文件或被匹配上的图片名进行操作
2. 实现另一套独立的图片截图/生成工具，进行截取图片，及被匹配后的一些列操作

流程：
1. 点击目标窗口/输入目标窗口 获取窗口句柄
2. 将目标窗口resize成固定大小，如： height: 300, width: 500
3. 循环截图目标窗口，将截图与模板图片进行匹配（模板图片是截图中的一小部分，预处理时需保证分辨率一致）
4. 当匹配上模板文件夹（放置在指定目录下）中的其中一个时，读取该模板图片的文件名， 
5. 解析一些信息
   1. 【delay time】绝对点击时间：匹配上后多久点击（绝对时间ms）
   2. 【random delay time】点击时间随机延迟量：过了绝对点击时间后，随机延迟多久时间（ms）
   3. 【relative click position】要点击的相对与目标窗口的绝对位置坐标 如：Rcp100x200 width x height
   4. 【random right offset】右侧随机偏移量
   5. 【random bottom offset】下侧随机偏移量
   6. 【delay up time】鼠标单机按下(down)之后，多久ms后抬起(up)
   7. 【delay random up time】在delay up time 基础上，再随机延迟多久
   8. 【random offset when up】鼠标down 与 up 期间，随机向各个角度的偏移量，一般几个像素点
   9. 【loop least count】至少循环点击几次
   10. 【loop random count】额外随机点击次数 
   11. 【end delay least time】当点击完后，至少多久不再去匹配模板 (ms)
   12. 【end delay random time】额外等待随机时间ms
   13. 【match event】匹配上后的事件：自定义函数，函数须与当前图片同一文件夹，且函数文件名为：函数名.py
   14. 【finish event】所有操作都执行完后的事件：自定义函数，函数须与当前图片同一文件夹，且函数文件名为：函数名.py 
   如：
       1. Dt1000Rdt200Rcp100x200Rro50Rbo50Dut20Drut5Rob8Llc1Lrc1Edlt1000Edrt100_Me=matchEvent_Fe=finishEvent.png
       2. Dt1000Rdt200Rcp508x517Rro175Rbo38Dut20Drut5Rob3Llc1Lrc1Edlt1000Edrt100_Me=matchEvent_Fe=finishEvent.png
       3. 1000_200_508x517_175_38_20_5_3_1_1_1000_100_matchEvent_finishEvent.png
6. 按照解析信息进行操作

   
   
   
