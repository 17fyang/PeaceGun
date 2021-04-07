# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from tutorialScripts.common.Interface import MOD_NAME, CLIENT_SYSTEM, CLIENT_SHOOT_EVENT, CLIENT_R_EVENT, \
    CLIENT_GRENADE_EVENT
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

        # 抛射物碰撞事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
                            "ProjectileDoHitEffectEvent", self, self.onBulletHit)

        # 客户端请求施放普通炸弹
        self.ListenForEvent(MOD_NAME, CLIENT_SYSTEM, CLIENT_GRENADE_EVENT, self, self.onClientRequestGrenade)

        # 客户端请求施放轰炸区
        self.ListenForEvent(MOD_NAME, CLIENT_SYSTEM, CLIENT_SHOOT_EVENT, self, self.onClientRequestShoot)

        # 客户端请求施放弹幕时间技能
        self.ListenForEvent(MOD_NAME, CLIENT_SYSTEM, CLIENT_R_EVENT, self, self.onClientRequestR)

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        print "===== TutorialServerSystem Destroy ====="
        self.UnListenForEvent(MOD_NAME, CLIENT_SYSTEM, CLIENT_SHOOT_EVENT, self, self.onClientRequestGrenade)
        self.UnListenForEvent(MOD_NAME, CLIENT_SYSTEM, CLIENT_R_EVENT, self, self.onClientRequestShoot)
        self.UnListenForEvent(MOD_NAME, CLIENT_SYSTEM, CLIENT_R_EVENT, self, self.onClientRequestR)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer",
                              self, self.tick)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
                              "ProjectileDoHitEffectEvent", self, self.onBulletHit)

    def tick(self):
        schedule.tick()

    def onBulletHit(self, data):
        playerId = data['srcId']
        bulletId = data['id']
        if "ENTITY" == data['hitTargetType']:
            pos = (data['x'], data['y'], data['z'])
        else:
            pos = (data['blockPosX'], data['blockPosY'], data['blockPosZ'])

        comp = serverApi.GetEngineCompFactory().CreateEngineType(bulletId)
        if str(comp.GetEngineTypeStr()) == 'peacegun:boom':
            bulletService.createSimpleBomb(playerId, bulletId, pos)

    def onClientRequestGrenade(self, data):
        playerId = data['playerId']
        bulletService.createGrenade(playerId)

    def onClientRequestShoot(self, data):
        playerId = data['playerId']
        bulletService.createRangeBullet(playerId)

    def onClientRequestR(self, data):
        playerId = data['playerId']
        bulletService.createRSkill(playerId)
