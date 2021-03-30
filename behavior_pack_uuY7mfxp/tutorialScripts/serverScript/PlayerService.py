# coding=utf-8
import mod.server.extraServerApi as serverApi
from tutorialScripts.common.Service import Service

# 获取组件工厂，用来创建组件
compFactory = serverApi.GetEngineCompFactory()


class PlayerService(Service):

    def getLevelId(self):
        '''
        获取当前Server的世界id
        :return:
        '''
        return serverApi.GetLevelId()

    def getPlayerPosition(self, playerId):
        '''
        获取玩家位置
        :param playerId:
        :return:
        '''
        posComp = compFactory.CreatePos(playerId)
        return posComp.GetPos()

    def getPlayerDirect(self, playerId):
        '''
        获取玩家朝向
        :param playerId:
        :return:
        '''
        rotComp = compFactory.CreateRot(playerId)
        rot = rotComp.GetRot()
        return serverApi.GetDirFromRot(rot)


playerService = PlayerService()
