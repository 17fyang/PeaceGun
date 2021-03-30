# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from tutorialScripts.common.Interface import MOD_NAME, CLIENT_SYSTEM, CLIENT_SHOOT_EVENT
from tutorialScripts.serverScript.BulletService import bulletService
from tutorialScripts.serverScript.Scedule import schedule

ServerSystem = serverApi.GetServerSystemCls()


class PeaceServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        super(PeaceServerSystem, self).__init__(namespace, systemName)
        print "===== TutorialServerSystem init ====="

        # 服务器tick事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", self,
                            self.tick)

        # 客户端请求射击
        self.ListenForEvent(MOD_NAME, CLIENT_SYSTEM, CLIENT_SHOOT_EVENT, self, self.onClientRequestShoot)

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        print "===== TutorialServerSystem Destroy ====="
        self.UnListenForEvent(MOD_NAME, CLIENT_SYSTEM, CLIENT_SHOOT_EVENT, self, self.onClientRequestShoot)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer",
                              self, self.tick)

    def tick(self):
        schedule.tick()

    def onClientRequestShoot(self, data):
        playerId = data['playerId']
        bulletService.createRangeBullet(playerId)
