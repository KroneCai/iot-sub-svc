# iot-sub-svc
## 软件开发需求
使用python开发一个运行在linux上的服务，用于订阅指定MQTT服务器特定主题的MQTT消息，并将消息内容存储在数据库内。

## 具体需求
1. 本项目git地址为：https://github.com/KroneCai/iot-sub-svc.git
2. 为项目创建python虚拟环境，项目地址为：/srv/iot-sub-svc/
3. 使用linux systemd管理本项目的订阅服务
4. 需要提供服务运行过程中必要的应用日志，日志存放到/var/log/iot_sub_svc.log文件中
5. 项目中用到的常量都需要被维护在配置文件中，配置文件地址为：/etc/iot-sub-svc/iot-sub-svc.conf
6. MQTT服务器地址为：114.92.179.98，1883端口
7. MQTT服务器的用户名：riot_pub_dev，密码：rent@kil2025
8. 采用sqlalchemy访问数据库，数据库暂时采用SQLite
9. 设计并展示项目目录结构
10. 提供从github直接拉取项目源码进行服务器端部署的的详细步骤及所需要用到的脚本
11. 提供测试的详细步骤及所需要用到的脚本
12. 本系统运行时，需要检测相应数据库、数据表是否存在，如果不存在，则自动创建
13. 需要订阅的消息主题维护在配置文件中，可以是0个或多个主题；当主题为0时，使用通配符订阅所有主题
14. 消息的内容（JSON字串）经过AES-128算法加密，加密类型为 CBC zero padding，密钥和偏移量为key= 'AQRTYUOIFSRBFCEG'，iv= 'AQRTYUOIFSRBFCEG'；在本项目中需要对内容进行解密，但暂时不对JSON字串做解析处理，只需要解密后存入数据库即可，留待后续项目再处理
15. 添加消息到达时的回调机制，方便后续扩展
16. 将数据保存到数据库时，需要保存的信息包括但不限于：当前系统时间，当前消息订阅客户端的client id（需要在配置文件中提供，并在启动时加载）, 消息主题, 原始payload，解密后的payload，MQTT消息的时间， QoS值, Retain值, payload长度，以及message id
17. 加密解密模块、数据访问模块、MQTT消息订阅模块、配置文件存取模块、服务创建管理模块等都需要用独立的python程序文件管理