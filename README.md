# PyRSAEncrypt
银杏黄项目--基于非对称加密算法的Python源码保护

关键部分在**pythonrun**的**PyParser_ASTFromFile**内，对每次import生成语法树前对源码解密



_ _ _
6.20更新
###### 加入了对pyc文件的处理
###### 加入了对解密后源码的处理
_ _ _



编译
```
./configure
```

**复制本页的Makefile覆盖生成的Makefile**

安装
```
sudo make install
```

运行
```
./python xx.py
```

