# -*- coding: utf-8 -*-

# 获取客户端引擎API模块
import mod.client.extraClientApi as clientApi

# 获取客户端system的基类ClientSystem
from tutorialScripts.common.Interface import CLIENT_SHOOT_EVENT, CLIENT_R_EVENT

ClientSystem = clientApi.GetClientSystemCls()


# 在modMain中注册的Client System类
class PeaceClientSystem(ClientSystem):

    # 客户端System的初始化函数
    def __init__(self, namespace, systemName):
        # 首先初始化TutorialClientSystem的基类ClientSystem
        super(PeaceClientSystem, self).__init__(namespace, systemName)

        self.DefineEvent(CLIENT_SHOOT_EVENT)
        self.DefineEvent(CLIENT_R_EVENT)

        # 鼠标左键点击监听
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),
                            'LeftClickBeforeClientEvent', self, self.onLeftMouseClick)

        # 鼠标右键点击监听
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),
                            'RightClickBeforeClientEvent', self, self.onRightMouseClick)

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),
                              'LeftClickBeforeClientEvent', self, self.onLeftMouseClick)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),
                              'RightClickBeforeClientEvent', self, self.onLeftMouseClick)

    def onLeftMouseClick(self, data):
        sendData = self.CreateEventData()
        sendData['playerId'] = clientApi.GetLocalPlayerId()
        self.NotifyToServer(CLIENT_SHOOT_EVENT, sendData)

    def onRightMouseClick(self, data):
        sendData = self.CreateEventData()
        sendData['playerId'] = clientApi.GetLocalPlayerId()
        self.NotifyToServer(CLIENT_R_EVENT, sendData)
