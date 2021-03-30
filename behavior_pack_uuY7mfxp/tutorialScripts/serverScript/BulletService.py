# coding=utf-8
import random

import mod.server.extraServerApi as serverApi
from tutorialScripts.common.Service import Service
from tutorialScripts.common.Vector import Vector
from tutorialScripts.serverScript.BulletConfig import DROP_DISTANCE, DROP_HEIGHT, DROP_RANGE, DROP_TIMES, \
    DROP_FREQUENCY, R_ROTATION, R_ROTATION_INTERVAL
from tutorialScripts.serverScript.PlayerService import playerService
from tutorialScripts.serverScript.Scedule import schedule


class BulletService(Service):
    def __init__(self):
        super(BulletService, self).__init__()

    def createSimpleBullet(self, playerId, pos, direct, **kwargs):
        '''
        创建一个子弹
        :param playerId:
        :param pos:
        :param direct:
        :return:
        '''
        bulletComp = serverApi.GetEngineCompFactory().CreateProjectile(playerService.getLevelId())
        param = {
            'position': pos,
            'direction': direct,
            'power': 3
        }

        if kwargs:
            param.update(kwargs)

        bulletId = bulletComp.CreateProjectileEntity(playerId, "minecraft:snowball", param)

    def runRangeSkill(self, playerId, middlePos, leftNum):
        '''
        创建一个枪林弹雨技能效果，用leftNum指定技能波数，会递归调用
        :param playerId:
        :param middlePos:
        :param leftNum:
        :return:
        '''
        # 根据技能中心点随机生成一个弹药降落点
        randomDis = random.uniform(0.0, DROP_RANGE)
        basDirect = random.random()
        randomDirect = basDirect, (1 - basDirect ** 2) ** 0.5

        # 实际的弹药落地点
        realPos = middlePos[0] + randomDirect[0] * randomDis, middlePos[1], middlePos[2] + randomDirect[1] * randomDis
        self.createSimpleBullet(playerId, realPos, Vector.down())

        # 提交下一次轰炸任务
        if leftNum > 0:
            schedule.runTaskDelay(DROP_FREQUENCY, self.runRangeSkill, playerId, middlePos, leftNum - 1)

    def createRangeBullet(self, playerId):
        '''
        客户端请求施放枪林弹雨
        :param playerId:
        :return:
        '''
        pos = playerService.getPlayerPosition(playerId)
        direct = playerService.getPlayerDirect(playerId)
        skillPos = (pos[0] + direct[0] * DROP_DISTANCE, pos[1] + DROP_HEIGHT, pos[2] + direct[2] * DROP_DISTANCE)

        self.runRangeSkill(playerId, skillPos, DROP_TIMES)

    def shootRLine(self, playerId, leftNum):
        '''
        射出一排弹幕时间
        :param playerId:
        :param leftNum:
        :return:
        '''
        rot = playerService.getPlayerRotation(playerId)
        pos = playerService.getPlayerPosition(playerId)
        for offerSet in range(-R_ROTATION, R_ROTATION, R_ROTATION_INTERVAL):
            # 粒子发射角度微微往上3°
            direct = serverApi.GetDirFromRot((-3, rot[1] + offerSet))
            self.createSimpleBullet(playerId, pos, direct)

        if leftNum > 0:
            schedule.runTaskDelay(10, self.shootRLine, playerId, leftNum - 1)

    def createRSkill(self, playerId):
        '''
        客户端请求施放弹幕时间技能
        :param playerId:
        :return:
        '''
        self.shootRLine(playerId, 4)

    def createGrenade(self, playerId):
        '''
        客户端请求施放手榴弹技能
        :param playerId:
        :return:
        '''
        rot = playerService.getPlayerRotation(playerId)
        pos = playerService.getPlayerPosition(playerId)
        # 投掷偏移量，往上30°
        rot = ((rot[0] - 30), rot[1])
        direct = serverApi.GetDirFromRot(rot)
        self.createSimpleBullet(playerId, pos, direct, power=1)

    def createSimpleBomb(self, playerId, bulletId, pos):
        '''
        创建一次爆炸，带火且影响方块
        :param playerId:
        :param bulletId:
        :param pos:
        :return:
        '''
        comp = serverApi.GetEngineCompFactory().CreateExplosion(playerService.getLevelId())
        comp.CreateExplosion(pos, 2, True, True, bulletId, playerId)


bulletService = BulletService()
