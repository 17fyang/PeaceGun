# -*- coding: utf-8 -*-
# 上面这行是让这个文件按utf-8进行编码，这样就可以在注释中写中文了

# 这行import到的是引擎客户端的API模块
import mod.client.extraClientApi as clientApi
# 这行import到的是引擎服务端的API模块
import mod.server.extraServerApi as serverApi
# 这行是import到MOD的绑定类Mod，用于绑定类和函数
from mod.common.mod import Mod

# 用Mod.Binding来绑定MOD的类，引擎从而能够识别这个类是MOD的入口类
from tutorialScripts.common.Interface import MOD_NAME, SERVER_SYSTEM, CLIENT_SYSTEM


@Mod.Binding(name="peaceGunMod", version="0.0.1")
class TutorialMod(object):

    # 类的初始化函数
    def __init__(self):
        print "===== init tutorial mod ====="

    @Mod.InitServer()
    def TutorialServerInit(self):
        print "===== init tutorial server ====="
        serverApi.RegisterSystem(MOD_NAME, SERVER_SYSTEM,
                                 "tutorialScripts.serverScript.peaceServerSystem.PeaceServerSystem")

    # DestroyServer绑定的函数作为服务端脚本退出的时候执行的析构函数，通常用来反注册一些内容,可为空
    @Mod.DestroyServer()
    def TutorialServerDestroy(self):
        print "===== destroy tutorial server ====="

    # InitClient绑定的函数作为客户端脚本初始化的入口函数，通常用来注册客户端系统system和组件component
    @Mod.InitClient()
    def TutorialClientInit(self):
        print "===== init hugo fps clientScript ====="
        # 函数可以将System注册到客户端引擎中，实例的创建和销毁交给引擎处理。第一个参数是MOD名称，第二个是System名称，第三个是自定义MOD System类的路径
        clientApi.RegisterSystem(MOD_NAME, CLIENT_SYSTEM,
                                 "tutorialScripts.clientScript.peaceClientSystem.PeaceClientSystem")

    # DestroyClient绑定的函数作为客户端脚本退出的时候执行的析构函数，通常用来反注册一些内容,可为空
    @Mod.DestroyClient()
    def TutorialClientDestroy(self):
        print "===== destroy hugo fps clientScript ====="
