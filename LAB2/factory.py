from datetime import datetime
from player import Player
import xml.etree.ElementTree as ET
import player_pb2 as protoplayer


class PlayerFactory:
    def to_json(self, players):
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''
        result = []
        for i in players:
            result.append({
                "nickname": i.nickname,
                "email": i.email,
                "date_of_birth": datetime.strftime(i.date_of_birth, "%Y-%m-%d"),
                "xp": i.xp,
                "class": i.cls
            })
        return result
        pass

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        result = []
        for i in list_of_dict:
            player = Player(i.get("nickname"), i.get("email"), i.get(
                "date_of_birth"), i.get("xp"), i.get("class"))
            result.append(player)
        return result
        pass

    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''
        result = []
        root = ET.fromstring(xml_string)
        for i in root:
            values = []
            for child in i:
                values.append(child.text)
            player = Player(values[0], values[1],
                            values[2], int(values[3]), values[4])
            result.append(player)
        return result
        pass

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''
        root = ET.Element('data')
        for i in list_of_players:
            player = ET.SubElement(root, 'player')
            nickname = ET.SubElement(player, 'nickname')
            nickname.text = i.nickname
            email = ET.SubElement(player, 'email')
            email.text = i.email
            date_of_birth = ET.SubElement(player, 'date_of_birth')
            date_of_birth.text = datetime.strftime(i.date_of_birth, "%Y-%m-%d")
            xp = ET.SubElement(player, 'xp')
            xp.text = str(i.xp)
            clas = ET.SubElement(player, 'class')
            clas.text = i.cls

        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
        return xml_string
        pass

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        list = protoplayer.PlayersList()
        list.ParseFromString(binary)

        playerobj = list.player
        players = []

        for i in playerobj:
            match i.cls:
                case 0:
                    classType = "Berserk"
                case 1:
                    classType = "Tank"
                case 3:
                    classType = "Paladin"
                case 4:
                    classType = "Mage"
            player = Player(
                nickname=i.nickname,
                email=i.email,
                date_of_birth=i.date_of_birth,
                xp=i.xp,
                cls=classType
            )
            players.append(player)

        return players
        pass

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects intoa binary protobuf string.
        '''
        objs = protoplayer.PlayersList()
        for i in list_of_players:
            player = objs.player.add()
            player.nickname = i.nickname
            player.email = i.email
            player.date_of_birth = datetime.strftime(
                i.date_of_birth, "%Y-%m-%d")
            player.xp = i.xp
            match i.cls:
                case "Berserk":
                    player.cls = protoplayer.Class.Berserk
                case "Tank":
                    player.cls = protoplayer.Class.Tank
                case "Paladin":
                    player.cls = protoplayer.Class.Paladin
                case "Mage":
                    player.cls = protoplayer.Class.Mage
        binary_protobuf_string = objs.SerializeToString()
        return binary_protobuf_string
        pass
