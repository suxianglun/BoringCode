从豆瓣读书上下载booklist.py中列出的图书的信息

---

### 关于

本来做出来是为了简化我整理看过书目用的

目前扒取
 - 图书标题
 - 作者
 - 图片
 - ISBN

### 依赖

`python3`

`pip3 install beautifulsoup4`

### 使用

请先用浏览器打开豆瓣 然后用浏览器的cookie替换掉代码中的
`'Cookie':'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyooooooooooooooooooooouuuuuuuuuuuuuuuuuurrrrrrrrrrrrrrr cccccccccccccoooooooooookie here',`

修改booklist为你所需要的书名,再执行命令

`python3 getBookInfo.py` 

然后会产生获取到的数据`booksdata.json`

### 工作原理 与 bug和bug修复情况

先通过`https://book.douban.com/subject_search?search_text=书名` 模拟搜索 获取第一个链接中的书在`豆瓣`上的id

再调用`https://api.douban.com/v2/book/书的id`获取json信息 

> bug0 豆瓣有反爬虫机制

目前解决方案
 - 时间间隔 : 请搜索代码`time.sleep`
 - 模拟浏览器 : 即`使用`中的添加cookie
 - 自动判断是否已下载 : 如果第一次被`502`或者`403` 或返回动态网页,则不会被添加到`booksdata.json`记录中,手动再次运行`python3 getBookInfo.py`只会获取尚未获取的图书,这样做的缺点是每本书都在读写文件
 - [未做 : 自动错误矫正]

> bug1 因为程序每次直接获取搜索到的第一个结果 有可能搜到豆瓣推荐的杂志从而报错 或者与我原本读的不是同一本

目前解决方案
 - 新增python : `appendBookByDoubanID.py 图书在豆瓣上的id` [然后发现函数分离做得不太好...



